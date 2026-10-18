"""Sound binary propagation of root component constraints on all 84 labels.

All root count equations, all component kernel equations, and exact C2
lower/upper bounds are used. A surviving partial assignment is UNKNOWN,
not a graph. No fixed Gram witness or extra matching normalization is used.
"""

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import time

LABELS = tuple((a,b) for a,b in combinations(range(14),2) if b != (a ^ 1))
PAIRS = tuple(combinations(range(84),2))
VARIABLE = {p:i for i,p in enumerate(PAIRS)}
RECTANGLES = {(i,j): [w for w,p in enumerate(LABELS) if tuple(a//2 for a in p) == (i,j)]
              for i,j in combinations(range(7),2)}


def variable(a,b):
    return VARIABLE[tuple(sorted((a,b)))]


def constraints(template):
    equations, bounds, initial = {}, [], {}
    def equation(items, target, reason):
        key = tuple(sorted(items))
        if key in equations and equations[key][0] != target:
            raise ValueError("Inconsistent duplicate component equations.")
        equations[key] = (target, reason)
    for w,p in enumerate(LABELS):
        equation([variable(w,q) for q in range(84) if q!=w],12,["degree",w])
        for a in range(14):
            equation([variable(w,q) for q,label in enumerate(LABELS) if q!=w and a in label],
                     2-int(a in p)-int((a^1) in p),["root_count",w,a])
    nongrid = {tuple(e) for e in template["nongrid_edges"]}
    for root in range(7):
        parts = [tuple(p) for p in template["nontrivial_component_groups"][root]]
        grouped = {j for part in parts for j in part}
        parts += [(j,) for j in range(7) if j!=root and j not in grouped]
        for part in parts:
            support = [q for j in part for q in RECTANGLES[tuple(sorted((root,j)))]]
            for w,p in enumerate(LABELS):
                ends = [a//2 for a in p]
                rhs = 3*int(w in support)+len(part)*(1-int(root in ends))-sum(j in part for j in ends)
                equation([variable(w,q) for q in support if q!=w],rhs,["component",w,root,part])
    for pair,corners in RECTANGLES.items():
        internal = [variable(w,q) for w,q in combinations(corners,2)]
        if pair in nongrid:
            bounds.append((tuple(internal),3,["nongrid",pair]))
        else:
            for w,q in combinations(corners,2):
                initial[variable(w,q)] = int(bool(set(LABELS[w]) & set(LABELS[q])))
    return [(items,target,reason) for items,(target,reason) in equations.items()], bounds, initial


def propagate(template, use_c2=True, extra_initial=None):
    equations, bounds, initial = constraints(template)
    values = [-1]*len(PAIRS)
    steps = []
    conflict = None
    def assign(index,value,reason):
        nonlocal conflict
        if values[index] not in (-1,value):
            conflict = {"kind":"inconsistent_assignment","variable":index,"required":value,"reason":reason}
        elif values[index] == -1:
            values[index] = value
            steps.append([index,value,reason])
    for index,value in initial.items():
        assign(index,value,["grid_rectangle"])
    for index,value in (extra_initial or {}).items():
        assert 0<=index<len(PAIRS) and value in (0,1)
        assign(index,value,["fixed_component_input"])
    rounds = 0
    while conflict is None:
        rounds += 1
        before = len(steps)
        for number,(items,target,_) in enumerate(equations):
            ones = sum(values[i]==1 for i in items)
            unknown = [i for i in items if values[i]==-1]
            needed = target-ones
            if not 0<=needed<=len(unknown):
                conflict = {"kind":"cardinality","equation":number,"target":target,"ones":ones,"unknown":len(unknown)}
                break
            if unknown and needed in (0,len(unknown)):
                for i in unknown:
                    assign(i,int(needed!=0),["cardinality",number])
        if conflict is not None:
            break
        for number,(items,upper,_) in enumerate(bounds):
            ones = sum(values[i]==1 for i in items)
            if ones>upper:
                conflict={"kind":"nongrid_upper","bound":number}
                break
            if ones==upper:
                for i in items:
                    if values[i]==-1:
                        assign(i,0,["upper",number])
        if conflict is not None:
            break
        if use_c2:
            present,possible = [0]*84,[0]*84
            for i,(a,b) in enumerate(PAIRS):
                if values[i] != 0:
                    possible[a] |= 1<<b
                    possible[b] |= 1<<a
                if values[i] == 1:
                    present[a] |= 1<<b
                    present[b] |= 1<<a
            for index,(a,b) in enumerate(PAIRS):
                target = 2-len(set(LABELS[a]) & set(LABELS[b]))
                common = present[a] & present[b]
                candidates = possible[a] & possible[b]
                lo,hi = common.bit_count(),candidates.bit_count()
                state = values[index]
                if lo+int(state==1)>target or hi+int(state!=0)<target:
                    conflict={"kind":"C2","pair":[a,b],"target":target,"lo":lo,"hi":hi,"edge_state":state}
                    break
                if state==-1:
                    if lo==target:
                        assign(index,0,["C2_edge_upper",a,b])
                    elif hi+1==target:
                        assign(index,1,["C2_edge_lower",a,b])
                    state=values[index]
                if lo+int(state==1)==target:
                    forced = ((present[a]&possible[b]) | (present[b]&possible[a])) & ~common
                    while forced:
                        bit = forced & -forced
                        z = bit.bit_length()-1
                        forced ^= bit
                        other = b if present[a]&bit else a
                        assign(variable(other,z),0,["C2_common_upper",a,b,z])
                if hi+int(state!=0)==target:
                    forced = candidates
                    while forced:
                        bit = forced & -forced
                        z=bit.bit_length()-1
                        forced ^= bit
                        assign(variable(a,z),1,["C2_common_lower",a,b,z])
                        assign(variable(b,z),1,["C2_common_lower",a,b,z])
                if conflict is not None:
                    break
        if len(steps)==before:
            break
    return {"status":"PROPAGATION_CONTRADICTION" if conflict else "UNRESOLVED",
            "fixed_edges":sum(v!=-1 for v in values),"ones":sum(v==1 for v in values),
            "unknown_edges":sum(v==-1 for v in values),"rounds":rounds,
            "conflict":conflict,"assignments":steps,
            "cardinality_equations":len(equations),"nongrid_bounds":len(bounds)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("templates",type=Path)
    parser.add_argument("grams",type=Path)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--no-c2",action="store_true")
    args=parser.parse_args()
    templates=json.loads(args.templates.read_text(encoding="utf-8"))["survivors"]
    grams=json.loads(args.grams.read_text(encoding="utf-8"))["records"]
    counts,records=Counter(),[]
    started=time.monotonic()
    for item in grams:
        index=item["template_index"]
        template=templates[index]
        if item["status"]!="QUOTIENT_FEASIBLE" or min(template["component_count_by_root_line"])!=4:
            continue
        result=propagate(template,use_c2=not args.no_c2)
        counts[result["status"]]+=1
        records.append({"template_index":index,**result})
        if len(records)%20==0:
            print(json.dumps({"completed":len(records),"counts":dict(counts)}),flush=True)
    output={"scope":"All remaining min-c=4 component templates, with no fixed Gram witness.",
            "uses_C2":not args.no_c2,"counts":dict(counts),"elapsed_seconds":time.monotonic()-started,
            "records":records}
    args.output.write_text(json.dumps(output,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in output.items() if k!="records"}),flush=True)
    print(json.dumps({"unknown_edges_histogram":dict(sorted(Counter(r['unknown_edges'] for r in records if r['status']=='UNRESOLVED').items()))}),flush=True)


if __name__=="__main__":
    main()
