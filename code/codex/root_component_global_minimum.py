"""Separate the GLOBAL minimum-four-components condition on every triangle.

For a genuine SRG(99,14,1,2), the open neighbourhood of a triangle has
36 vertices. Each component has 6s vertices: its three colour classes
have equal size (cross matchings), and even size (internal matchings).
If there are at least four components, sum(s-1) <= 2. Consequently the
neighbourhood cannot contain disjoint connected vertex sets of sizes
(19), (13,7), or (7,7,7). This is true even if some sets merge in a
completion: merging never decreases sum(ceil(size/6)-1).

The generated clauses use only a present triangle, one attachment per
selected vertex, and spanning trees. No absent edge is used as evidence
that two sets must stay disconnected. The cuts are necessary ONLY in
the branch with global min c >= 4; they do not exclude that assumption.
"""

import argparse
from collections import Counter, deque
from itertools import combinations
import json
from pathlib import Path
import sys
import threading
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import limit_research_process
from root_component_signature_joint import build
from root_component_signature_moments import gram_matrix
from root_component_propagation import LABELS, PAIRS
from ortools.sat.python import cp_model


def adjacency99(gamma):
    graph = [[0]*99 for _ in range(99)]
    for a in range(14):
        graph[0][a+1] = graph[a+1][0] = 1
        graph[a+1][(a^1)+1] = 1
    for w, label in enumerate(LABELS):
        for a in label:
            graph[a+1][w+15] = graph[w+15][a+1] = 1
    for u, v in PAIRS:
        graph[u+15][v+15] = graph[v+15][u+15] = gamma[u][v]
    return graph


def minimum_component_cuts(gamma):
    graph = adjacency99(gamma)
    neighbours = [{v for v in range(99) if row[v]} for row in graph]
    found = {}
    histogram = Counter()
    for a in range(99):
        for b in sorted(v for v in neighbours[a] if v > a):
            for c in sorted(v for v in neighbours[a] & neighbours[b] if v > b):
                line = (a,b,c)
                outside = (neighbours[a] | neighbours[b] | neighbours[c]) - set(line)
                remaining = set(outside)
                components = []
                while remaining:
                    start = min(remaining)
                    queue = deque([start])
                    seen, order, tree = {start}, [], []
                    while queue:
                        u = queue.popleft()
                        order.append(u)
                        for v in sorted(neighbours[u] & remaining - seen):
                            seen.add(v)
                            queue.append(v)
                            tree.append((u,v))
                    remaining -= seen
                    components.append((order, tree))
                components.sort(key=lambda x:(-len(x[0]),x[0]))
                sizes = [len(item[0]) for item in components]
                if sizes and sizes[0] >= 19:
                    pattern = [19]
                elif len(sizes)>=2 and sizes[0]>=13 and sizes[1]>=7:
                    pattern = [13,7]
                elif len(sizes)>=3 and sizes[2]>=7:
                    pattern = [7,7,7]
                else:
                    continue
                required = set(combinations(line,2))
                witnesses = []
                for (order,tree), size in zip(components,pattern):
                    vertices = order[:size]
                    chosen = set(vertices)
                    edges = [tuple(sorted((u,v))) for u,v in tree if u in chosen and v in chosen]
                    assert len(edges)==size-1
                    required.update(edges)
                    for v in vertices:
                        root = min(set(line) & neighbours[v])
                        required.add(tuple(sorted((root,v))))
                    witnesses.append({"vertices":vertices,"tree":edges})
                assert all(graph[u][v] for u,v in required)
                variable_edges = tuple(sorted((u-15,v-15) for u,v in required if u>=15))
                histogram[','.join(map(str,pattern))] += 1
                found.setdefault(variable_edges,{"line":line,"pattern":pattern,"sets":witnesses})
    return found, histogram


def solve(template, matrix, local_tables, seconds, per_solve, layer, eigen, checkpoint):
    started, cpu_started = time.monotonic(), time.process_time()
    model, graph, info = build(template,matrix,layer,eigen=eigen,mate_normalize=True,
                               four_corners=True,local_tables=local_tables)
    assert not model.validate(), model.validate()
    cuts, iterations = {}, []
    info.update(status="RUNNING",global_minimum_components=4,iterations=iterations)
    while time.process_time()-cpu_started < seconds:
        solver=cp_model.CpSolver()
        solver.parameters.num_search_workers=1
        solver.parameters.cp_model_probing_level=0
        solver.parameters.symmetry_level=0
        solver.parameters.linearization_level=0
        budget=min(per_solve,seconds-(time.process_time()-cpu_started))
        solver.parameters.max_time_in_seconds=max(600,100*budget)
        cpu_search=time.process_time()
        done=threading.Event()
        def interrupt():
            while not done.wait(.1):
                if time.process_time()-cpu_search>=budget:
                    solver.stop_search()
                    return
        timer=threading.Thread(target=interrupt,daemon=True)
        timer.start()
        try:
            status=solver.solve(model)
        finally:
            done.set()
            timer.join()
        event={"iteration":len(iterations),"status":solver.status_name(status),
               "wall_seconds":solver.wall_time,"cpu_seconds":time.process_time()-cpu_search,
               "branches":solver.num_branches,"conflicts":solver.num_conflicts}
        iterations.append(event)
        if status==cp_model.INFEASIBLE:
            info["status"]="INFEASIBLE"
            break
        if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            info["status"]=solver.status_name(status)
            break
        gamma=[[solver.value(x) for x in row] for row in graph]
        fresh, histogram=minimum_component_cuts(gamma)
        new={key:value for key,value in fresh.items() if key not in cuts}
        assert not fresh or new, "A previously forbidden tree was violated."
        event.update(violations_by_pattern=dict(histogram),new_cuts=len(new))
        if not new:
            info.update(status="FEASIBLE_MINC_RELAXATION",relaxation_edges=[list(p) for p in PAIRS if gamma[p[0]][p[1]]])
            break
        for edges,witness in new.items():
            literals=[]
            for u,v in edges:
                edge=graph[u][v]
                if isinstance(edge,int):
                    assert edge==1
                else:
                    literals.append(edge.Not())
            model.add_bool_or(literals)
            cuts[edges]=witness
        info["cuts"]=[{"edges":list(edges),**witness} for edges,witness in sorted(cuts.items())]
        event["total_cuts"]=len(cuts)
        checkpoint(info)
        print(json.dumps(event),flush=True)
    if info["status"]=="RUNNING":
        info["status"]="UNKNOWN"
    info.update(total_wall_seconds=time.monotonic()-started,total_cpu_seconds=time.process_time()-cpu_started,
                cuts=[{"edges":list(edges),**witness} for edges,witness in sorted(cuts.items())])
    return info


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    parser.add_argument("--index",type=int,required=True)
    parser.add_argument("--gram-index",type=int,required=True)
    parser.add_argument("--seconds",type=float,default=300)
    parser.add_argument("--per-solve",type=float,default=30)
    parser.add_argument("--layer",type=int,default=0,choices=range(5))
    parser.add_argument("--eigen",action="store_true")
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    resources=limit_research_process(4)
    covers={r['template_index']:r for r in json.loads((args.directory/'root_component_gram_orbits20.json').read_text())['records']}
    cover=covers[args.index]
    assert cover['exhaustive'] and cover['usable_as_gram_cover']
    values=cover['gram_anchor_values'][args.gram_index]
    templates=json.loads((args.directory/'root_component_templates.json').read_text())['survivors']
    tables=json.loads((args.directory/'line_component_pattern_tables.json').read_text())
    def checkpoint(result):
        record={'template_index':args.index,'complete_source_gram_count':cover['gram_count'],
                'all_source_grams_processed':False,'excluded':False,
                'cases':[dict(result,gram_index=args.gram_index,gram_anchor_values=values)]}
        data={'scope':__doc__,'resources':resources,'records':[record]}
        temporary=args.output.with_suffix('.json.tmp')
        temporary.write_text(json.dumps(data,separators=(',',':'))+'\n',encoding='utf-8')
        temporary.replace(args.output)
    result=solve(templates[args.index],gram_matrix(cover,values),tables,args.seconds,args.per_solve,args.layer,args.eigen,checkpoint)
    checkpoint(result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('cuts','iterations','relaxation_edges')}),flush=True)


if __name__=='__main__':
    main()
