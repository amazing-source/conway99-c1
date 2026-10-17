"""Exact necessary tables for the coloured cubic components at root lines."""

from itertools import combinations
from ortools.sat.python import cp_model

from root_component_propagation import LABELS, RECTANGLES


def component_pair_relabel_map(record, pair_permutation):
    """Conjugation maps for a root-pair permutation, preserving both bits."""
    permutations = [tuple(p) for p in record['cross_permutations']]
    matchings = [tuple(tuple(e) for e in m) for m in record['internal_matchings']]
    pi_index = {p:i for i,p in enumerate(permutations)}
    mi_index = {m:i for i,m in enumerate(matchings)}
    n=len(permutations[0])
    assert sorted(pair_permutation)==list(range(n//2))
    f=[2*pair_permutation[j//2]+j%2 for j in range(n)]
    inverse=[f.index(j) for j in range(n)]
    pp=[pi_index[tuple(f[p[inverse[j]]] for j in range(n))] for p in permutations]
    mm=[mi_index[tuple(sorted(tuple(sorted((f[a],f[b]))) for a,b in m))] for m in matchings]
    return pp,mm


def canonical_component_codes(record, pair_permutations=None, return_map=False):
    permutations = [tuple(p) for p in record["cross_permutations"]]
    matchings = [tuple(tuple(e) for e in m) for m in record["internal_matchings"]]
    pi_index = {p:i for i,p in enumerate(permutations)}
    mi_index = {m:i for i,m in enumerate(matchings)}
    n = len(permutations[0])
    pmaps, mmaps = [], []
    pair_permutations = pair_permutations or [tuple(range(n//2))]
    for pair_permutation in pair_permutations:
        assert sorted(pair_permutation) == list(range(n//2))
        for bits in range(1 << (n//2)):
            f = [2*pair_permutation[j//2] + ((j%2) ^ ((bits >> (j//2)) & 1)) for j in range(n)]
            inverse = [f.index(j) for j in range(n)]
            pmaps.append([pi_index[tuple(f[p[inverse[j]]] for j in range(n))] for p in permutations])
            mmaps.append([mi_index[tuple(sorted(tuple(sorted((f[a],f[b]))) for a,b in m))] for m in matchings])
    inverses = [pi_index[tuple(p.index(j) for j in range(n))] for p in permutations]
    valid = {tuple(c) for c in record["component_code_triples"]}
    representatives = {}
    for p,a,b in valid:
        orbit = set()
        for pp,mm in zip(pmaps,mmaps):
            orbit.add((pp[p],mm[a],mm[b]))
            orbit.add((inverses[pp[p]],mm[b],mm[a]))
        assert orbit.issubset(valid)
        representatives[p,a,b] = min(orbit)
    return representatives if return_map else sorted(set(representatives.values()))


def compatible_component_codes(record, stars, root, part, corner_patterns):
    """Filter only by the six actual edges of each incident four-corner Q.

    Global corner order may transpose the two local stars when root>j.
    Every mask is therefore assembled using actual vertex identifiers.
    """
    locations = {vertex:(colour,i) for colour,row in enumerate(stars) for i,vertex in enumerate(row)}
    patterns = []
    for other in part:
        rectangle = tuple(sorted((root,other)))
        tests = [(bit, locations[u], locations[v])
                 for bit,(u,v) in enumerate(combinations(RECTANGLES[rectangle],2))]
        cross_masks = []
        for permutation in record["cross_permutations"]:
            mask = 0
            for bit,(cu,i),(cv,j) in tests:
                if cu != cv and (permutation[i] == j if cu == 0 else permutation[j] == i):
                    mask |= 1 << bit
            cross_masks.append(mask)
        internal_masks = []
        for colour in range(2):
            masks = []
            for matching in record["internal_matchings"]:
                present = {tuple(pair) for pair in matching}
                masks.append(sum(1 << bit for bit,(cu,i),(cv,j) in tests
                                 if cu == cv == colour and tuple(sorted((i,j))) in present))
            internal_masks.append(masks)
        patterns.append((cross_masks, internal_masks[0], internal_masks[1], corner_patterns[rectangle]))
    return [code for code in record["component_code_triples"]
            if all((cross[p] | m0[a] | m1[b]) in allowed for cross,m0,m1,allowed in patterns
                   for p,a,b in [code])]


def component_signature_rows(record, codes, stars, root, part, edges, domains, corner_tables):
    """A local code determines H on all coordinates incident with this root.

    At local vertex (colour,i), its two neighbours are its internal mate
    and its cross-permutation neighbour. Thus h_{root,k} is twice the own
    rectangle indicator minus the number of these two neighbours in Q_{root,k}.
    Retain all projected signatures and link them directly to the global H.
    """
    vertices = stars[0] + stars[1]
    n = len(stars[0])
    locations = {vertex:(colour,i) for colour,row in enumerate(stars) for i,vertex in enumerate(row)}
    position = {w:i for i,w in enumerate(vertices)}
    coordinates = [i for i,e in enumerate(edges) if root in e]
    part_coordinates = [coordinates.index(edges.index(tuple(sorted((root,j))))) for j in part]
    by_rectangle = {}
    tables = {t["rectangle"]: t["rows"] for t in corner_tables}
    for other in part:
        rectangle = tuple(sorted((root,other)))
        signatures = domains[rectangle]["signatures"]
        projected = [tuple(h[i] for i in coordinates) for h in signatures]
        unique = sorted(set(projected))
        index = {h:i for i,h in enumerate(unique)}
        allowed = {(sum(bit<<i for i,bit in enumerate(row[4:])), tuple(projected[q] for q in row[:4]))
                   for row in tables[rectangle]}
        by_rectangle[rectangle] = {"projected": projected, "unique": unique, "index": index, "allowed": allowed}
    mate_maps = []
    for matching in record["internal_matchings"]:
        partner = [None] * n
        for i,j in matching:
            partner[i],partner[j] = j,i
        mate_maps.append(partner)
    permutations = record["cross_permutations"]
    inverses = [[p.index(j) for j in range(n)] for p in permutations]
    rows = []
    for p,ma,mb in codes:
        partial, indices = [], []
        valid = True
        for colour,m in enumerate((ma,mb)):
            cross = permutations[p] if colour == 0 else inverses[p]
            for i in range(n):
                h = [0] * len(coordinates)
                h[part_coordinates[i//2]] += 2
                h[part_coordinates[mate_maps[m][i]//2]] -= 1
                h[part_coordinates[cross[i]//2]] -= 1
                h = tuple(h)
                rectangle = tuple(sorted((root,part[i//2])))
                ix = by_rectangle[rectangle]["index"].get(h)
                if ix is None:
                    valid = False
                    break
                partial.append(h)
                indices.append(ix)
            if not valid:
                break
        if not valid:
            continue
        for rectangle,item in by_rectangle.items():
            corners = RECTANGLES[rectangle]
            mask = 0
            for bit,(u,v) in enumerate(combinations(corners,2)):
                cu,i = locations[u]
                cv,j = locations[v]
                if cu == cv:
                    present = mate_maps[ma if cu == 0 else mb][i] == j
                else:
                    present = permutations[p][i] == j if cu == 0 else permutations[p][j] == i
                mask |= int(present) << bit
            key = (mask, tuple(partial[position[w]] for w in corners))
            if key not in item["allowed"]:
                valid = False
                break
        if valid:
            rows.append([p,ma,mb] + indices)
    return rows, by_rectangle, vertices


def add_local_component_tables(model, graph, template, data, normalize_first=False, corner_patterns=None,
                               signature_data=None, branch_context=None, rotated_boundary=False,
                               first_component_relabelings=None):
    library = {r["vertices"]//6:r for r in data["records"]}
    index = {p:i for i,p in enumerate(LABELS)}
    table_count, row_count = 0, 0
    chosen = None
    if normalize_first:
        chosen = min(((-len(part),root,tuple(part)) for root,parts in enumerate(template["nontrivial_component_groups"]) for part in parts))
        chosen = chosen[1:]
    normalized_info = None
    normalization_map = None
    component_records = []
    filtered_info = []
    rotated_info = []
    for root, parts in enumerate(template["nontrivial_component_groups"]):
        for part in parts:
            s = len(part)
            record = library[s]
            letters = [2*j+b for j in sorted(part) for b in range(2)]
            n = len(letters)
            stars = [[index[tuple(sorted((2*root+a,b)))] for b in letters] for a in range(2)]
            codes = record["component_code_triples"]
            if corner_patterns is not None:
                codes = compatible_component_codes(record, stars, root, part, corner_patterns)
                filtered_info.append({"root_line":root,"part":part,"before":len(record["component_code_triples"]),"after":len(codes)})
                if not codes:
                    model.add(False)
                    return {"empty_component_domain": [root,part], "corner_pattern_filters":filtered_info}
            signature_rows = None
            if signature_data is not None:
                edges,domains,corner_tables,global_selectors = signature_data
                signature_rows,projected,vertices = component_signature_rows(
                    record,codes,stars,root,part,edges,domains,corner_tables)
                filtered_info[-1]["after_joint_signature_projection"] = len(signature_rows)
                if not signature_rows:
                    model.add(False)
                    return {"empty_component_signature_domain": [root,part], "corner_pattern_filters":filtered_info}
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
            if chosen == (root,tuple(part)):
                allowed = codes if signature_rows is None else [row[:3] for row in signature_rows]
                # canonical_component_codes checks that EVERY mate-flip orbit
                # stays in this filtered code set before selecting a representative.
                restricted = dict(record, component_code_triples=allowed)
                pair_permutations = None if first_component_relabelings is None else first_component_relabelings['part_permutations']
                normalization_map = canonical_component_codes(restricted, pair_permutations, return_map=True)
                codes = sorted(set(normalization_map.values()))
                if signature_rows is not None:
                    canonical = set(codes)
                    signature_rows = [row for row in signature_rows if tuple(row[:3]) in canonical]
                normalized_info = {"root_line":root,"part":part,"original_codes":len(record["component_code_triples"]),
                                   "filtered_codes":len(allowed),"canonical_codes":len(codes),
                                   "filtered_set_invariance_checked":True,
                                   "action":"Global independent mate flips only; no graph automorphism assumed."}
                if first_component_relabelings is not None:
                    normalized_info['root_stabilizer'] = first_component_relabelings
                    normalized_info['action'] = 'Global mate flips and root relabelings preserving the complete fixed Gram and component template; no completed-graph automorphism assumed.'
                if branch_context is not None:
                    branch_context.update(root=root, part=list(part), selectors=list(selectors), codes=list(codes))
            if signature_rows is None:
                model.add_allowed_assignments(selectors,codes)
            else:
                signature_variables = []
                for w in vertices:
                    rectangle = tuple(a//2 for a in LABELS[w])
                    item = projected[rectangle]
                    variable = model.new_int_var(0,len(item["unique"])-1,f"component_h_{root}_{w}")
                    model.add_allowed_assignments([global_selectors[w],variable],
                        [[i,item["index"][h]] for i,h in enumerate(item["projected"])])
                    signature_variables.append(variable)
                model.add_allowed_assignments(selectors + signature_variables, signature_rows)
            if rotated_boundary:
                from root_component_rotated_boundary import add_code_cuts
                boundary_codes=codes if signature_rows is None else [row[:3] for row in signature_rows]
                rotated_info.append(add_code_cuts(model,graph,record,boundary_codes,selectors,stars,root,part))
            component_records.append({'root':root,'part':list(part),'selectors':list(selectors),
                'codes':codes if signature_rows is None else [row[:3] for row in signature_rows],'record':record})
            table_count += 4
            row_count += len(rows)+2*len(record["internal_matchings"])+(len(codes) if signature_rows is None else len(signature_rows))
    if first_component_relabelings is not None:
        from root_component_stabilizer import add_root_orbit_minimum
        normalized_info['root_orbit_minimum'] = add_root_orbit_minimum(
            model, component_records, first_component_relabelings, normalization_map)
    return {"tables":table_count,"rows":row_count,"first_component_normalization":normalized_info,
            "corner_pattern_filters":filtered_info,"rotated_boundary_triples":rotated_info,
            "scope":"Every true connected line component is covered; no local witness is fixed."}
