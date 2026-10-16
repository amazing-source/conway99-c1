"""Exact necessary tables for the coloured cubic components at root lines."""

from itertools import combinations
from ortools.sat.python import cp_model

from root_component_propagation import LABELS


def canonical_component_codes(record):
    permutations = [tuple(p) for p in record["cross_permutations"]]
    matchings = [tuple(tuple(e) for e in m) for m in record["internal_matchings"]]
    pi_index = {p:i for i,p in enumerate(permutations)}
    mi_index = {m:i for i,m in enumerate(matchings)}
    n = len(permutations[0])
    pmaps, mmaps = [], []
    for bits in range(1 << (n//2)):
        f = [j ^ ((bits >> (j//2)) & 1) for j in range(n)]
        pmaps.append([pi_index[tuple(f[p[f[j]]] for j in range(n))] for p in permutations])
        mmaps.append([mi_index[tuple(sorted(tuple(sorted((f[a],f[b]))) for a,b in m))] for m in matchings])
    inverses = [pi_index[tuple(p.index(j) for j in range(n))] for p in permutations]
    valid = {tuple(c) for c in record["component_code_triples"]}
    representatives = set()
    for p,a,b in valid:
        orbit = set()
        for pp,mm in zip(pmaps,mmaps):
            orbit.add((pp[p],mm[a],mm[b]))
            orbit.add((inverses[pp[p]],mm[b],mm[a]))
        assert orbit.issubset(valid)
        representatives.add(min(orbit))
    return sorted(representatives)


def add_local_component_tables(model, graph, template, data, normalize_first=False):
    library = {r["vertices"]//6:r for r in data["records"]}
    index = {p:i for i,p in enumerate(LABELS)}
    table_count, row_count = 0, 0
    chosen = None
    if normalize_first:
        chosen = min(((-len(part),root,tuple(part)) for root,parts in enumerate(template["nontrivial_component_groups"]) for part in parts))
        chosen = chosen[1:]
    normalized_info = None
    for root, parts in enumerate(template["nontrivial_component_groups"]):
        for part in parts:
            s = len(part)
            record = library[s]
            letters = [2*j+b for j in sorted(part) for b in range(2)]
            n = len(letters)
            stars = [[index[tuple(sorted((2*root+a,b)))] for b in letters] for a in range(2)]
            selectors = [model.new_int_var(0,len(record["cross_permutations"])-1,f"local_P_{root}_{part[0]}")]
            for a in range(2):
                selector = model.new_int_var(0,len(record["internal_matchings"])-1,f"local_M{a}_{root}_{part[0]}")
                selectors.append(selector)
                pairs = list(combinations(range(n),2))
                columns = [graph[stars[a][i]][stars[a][j]] for i,j in pairs]
                rows = []
                for mi,matching in enumerate(record["internal_matchings"]):
                    present = {tuple(e) for e in matching}
                    rows.append([mi]+[int((i,j) in present) for i,j in pairs])
                model.add_allowed_assignments([selector]+columns,rows)
            columns = [graph[u][v] for u in stars[0] for v in stars[1]]
            rows = [[pi]+[int(p[i]==j) for i in range(n) for j in range(n)]
                    for pi,p in enumerate(record["cross_permutations"])]
            model.add_allowed_assignments([selectors[0]]+columns,rows)
            codes = record["component_code_triples"]
            if chosen == (root,tuple(part)):
                codes = canonical_component_codes(record)
                normalized_info = {"root_line":root,"part":part,"original_codes":len(record["component_code_triples"]),
                                   "canonical_codes":len(codes),"action":"Global independent mate flips only; no graph automorphism assumed."}
            model.add_allowed_assignments(selectors,codes)
            table_count += 4
            row_count += len(rows)+2*len(record["internal_matchings"])+len(codes)
    return {"tables":table_count,"rows":row_count,"first_component_normalization":normalized_info,
            "scope":"Every true connected line component is covered; no local witness is fixed."}
