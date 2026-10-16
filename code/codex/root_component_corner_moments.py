"""Couple complete four-corner realizations through global exact moments.

For each fixed Gram, every rectangle has a finite set of contributions to
H^tH and to the prism count. Choose one per rectangle, requiring H^tH=7R
and prism sum<=51. A feasible moment design is not an adjacency completion.
"""

import argparse
from collections import Counter
from itertools import combinations_with_replacement
import json
from pathlib import Path
import sys
import time

from ortools.sat.python import cp_model

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_signature_moments import gram_matrix
from root_rectangle_domains import signature_domains
from root_component_corner_tables import enumerate_corner_rows


def solve(template,matrix,seconds):
    started=time.monotonic()
    edges=[tuple(e) for e in template["nongrid_edges"]]
    raw=[[int(x) for x in row] for row in matrix.tolist()]
    domains={tuple(r["rectangle"]):r for r in signature_domains(edges,raw)}
    anchors=list(matrix.rref()[1])
    small=matrix.extract(anchors,anchors)
    det=int(small.det())
    adj=[[int(x) for x in row] for row in (small.inv()*det).tolist()]
    pairs=list(combinations_with_replacement(range(len(anchors)),2))
    tables=enumerate_corner_rows(edges,matrix,domains,anchors,det,adj)
    choices=[]
    for table in tables:
        e=table["rectangle"]
        signatures=[tuple(h[a] for a in anchors) for h in domains[e]["signatures"]]
        vectors=set()
        for row in table["rows"]:
            moments=tuple(sum(signatures[q][i]*signatures[q][j] for q in row[:4]) for i,j in pairs)
            prism=sum(row[4+b] for b in (0,1,4,5))
            vectors.add(moments+(prism,))
        if not vectors:
            return {"status":"INFEASIBLE","reason":"NO_FOUR_CORNER_REALIZATION","rectangle":e,
                    "seconds":time.monotonic()-started}
        choices.append({"rectangle":e,"vectors":sorted(vectors)})
    model=cp_model.CpModel()
    flags=[]
    for i,choice in enumerate(choices):
        row=[model.new_bool_var(f"choice_{i}_{j}") for j in range(len(choice["vectors"]))]
        model.add_exactly_one(row)
        flags.append(row)
    for q,(i,j) in enumerate(pairs):
        model.add(sum(flag*v[q] for row,choice in zip(flags,choices) for flag,v in zip(row,choice["vectors"]))
                  ==7*int(matrix[anchors[i],anchors[j]]))
    model.add(sum(flag*v[-1] for row,choice in zip(flags,choices) for flag,v in zip(row,choice["vectors"]))<=51)
    assert not model.validate(),model.validate()
    solver=cp_model.CpSolver()
    solver.parameters.num_search_workers=1
    solver.parameters.max_time_in_seconds=seconds
    status=solver.solve(model)
    result={"status":solver.status_name(status),"seconds":time.monotonic()-started,"solver_seconds":solver.wall_time,
            "corner_rows":sum(len(t["rows"]) for t in tables),"moment_choice_count":sum(len(c["vectors"]) for c in choices),
            "maximum_rectangle_choices":max(len(c["vectors"]) for c in choices)}
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        selected=[next(v for flag,v in zip(row,choice["vectors"]) if solver.value(flag)) for row,choice in zip(flags,choices)]
        for q,(i,j) in enumerate(pairs):assert sum(v[q] for v in selected)==7*matrix[anchors[i],anchors[j]]
        assert sum(v[-1] for v in selected)<=51
        result["selected_moment_patterns"]=selected
    else:
        result["moment_domains"]=choices
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    parser.add_argument("--indices",type=int,nargs="+",required=True)
    parser.add_argument("--seconds",type=float,default=2)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    covers={r["template_index"]:r for r in json.loads((args.directory/"root_component_gram_orbits20.json").read_text())["records"]}
    templates=json.loads((args.directory/"root_component_templates.json").read_text())["survivors"]
    previous={}
    for path in sorted(args.directory.glob("root_component_signature_*.json")):
        if path.resolve()==args.output.resolve():continue
        for record in json.loads(path.read_text()).get("records",[]):
            for c in record.get("cases",[]):
                if c["status"]=="INFEASIBLE":previous[record["template_index"],c["gram_index"]]=(c,path.name)
    records=[]
    for index in args.indices:
        cover=covers[index]
        assert cover["exhaustive"] and cover["usable_as_gram_cover"]
        cases=[]
        record={"template_index":index,"complete_source_gram_count":cover["gram_count"],"cases":cases}
        records.append(record)
        for gi,values in enumerate(cover["gram_anchor_values"]):
            old=previous.get((index,gi))
            if old:
                assert old[0]["gram_anchor_values"]==values
                result={"status":"INFEASIBLE","source":old[1]}
            else:
                result=solve(templates[index],gram_matrix(cover,values),args.seconds)
            result.update(gram_index=gi,gram_anchor_values=values)
            cases.append(result)
            record.update(counts=dict(Counter(r["status"] for r in cases)),all_source_grams_processed=len(cases)==cover["gram_count"],
                          excluded=len(cases)==cover["gram_count"] and all(r["status"]=="INFEASIBLE" for r in cases))
            args.output.write_text(json.dumps({"scope":__doc__,"records":records},separators=(",",":"))+"\n",encoding="utf-8")
            if not old:
                print(json.dumps({"template":index,**{k:v for k,v in result.items() if k not in ("moment_domains","selected_moment_patterns")}}),flush=True)
        print(json.dumps({k:v for k,v in record.items() if k!="cases"}),flush=True)


if __name__=="__main__":main()
