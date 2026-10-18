"""Eight vertices forced by opposite columns on disjoint rectangles.

H_A=-H_B for disjoint root rectangles forces Q_A union Q_B to be cubic:
Gamma(P_A+P_B)=W_A+W_B, which equals 3 on those eight vertices.
Enumerate this small induced graph with root-letter quotas and necessary
common-neighbour bounds. No full Gram and no completion solver are used.
"""

import argparse
from collections import Counter
from itertools import combinations, combinations_with_replacement, permutations, product
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write, limit_research_process
from root_rectangle_domains import corner_graphs


LABELS = [(a, b) for a in (0, 1) for b in (2, 3)] + [
    (a, b) for a in (4, 5) for b in (6, 7)]


def enumerate_cores():
    result = []
    counts = Counter()
    for e in range(3):  # E3; equal column norms force equal edge counts.
        for aa, _, _ in corner_graphs(e):
            degrees = [3-sum(row) for row in aa]
            domains = [list(combinations(range(4), d)) for d in degrees]
            for rows in product(*domains):
                cross = [[int(j in row) for j in range(4)] for row in rows]
                for bb, _, _ in corner_graphs(e):
                    if any(sum(cross[i][j] for i in range(4))+sum(bb[j]) != 3 for j in range(4)):
                        continue
                    counts[f'e{e}_cubic'] += 1
                    g = [[0]*8 for _ in range(8)]
                    for i, j in product(range(4), repeat=2):
                        g[i][j] = aa[i][j]
                        g[i+4][j+4] = bb[i][j]
                        g[i][j+4] = g[j+4][i] = cross[i][j]
                    # An upper-star letter has exactly its quota in Gamma.
                    if any(sum(g[w][v] for v in range(8) if a in LABELS[v]) >
                           2-int(a in LABELS[w])-int((a ^ 1) in LABELS[w])
                           for w in range(8) for a in range(8)):
                        continue
                    counts[f'e{e}_quota'] += 1
                    if any(sum(g[u][w]*g[v][w] for w in range(8)) >
                           2-g[u][v]-len(set(LABELS[u]) & set(LABELS[v]))
                           for u, v in combinations(range(8), 2)):
                        continue
                    counts[f'e{e}_C2'] += 1
                    result.append({'internal_edges':e,'adjacency':g})
    return {'scope':__doc__, 'label_pairs':LABELS, 'counts':dict(counts),
            'cores':result, 'whole_template_excluded':False,
            'complete_eight_vertex_enumeration':True}


def opposite_pairs(template):
    """Exact component identities H_A=-H_B for disjoint nongrid A,B."""
    import sympy as sp
    rectangles = list(combinations(range(7), 2))
    rows = []
    for root, parts in enumerate(template['nontrivial_component_groups']):
        used = {j for part in parts for j in part}
        for part in [tuple(p) for p in parts]+[(j,) for j in range(7) if j != root and j not in used]:
            support = {tuple(sorted((root,j))) for j in part}
            rows.append([int(q in support) for q in rectangles])
    kernel = sp.Matrix(rows).nullspace()
    nongrid = {tuple(q) for q in template['nongrid_edges']}
    result = []
    for a,b in combinations(range(21), 2):
        if rectangles[a] not in nongrid or rectangles[b] not in nongrid:
            continue
        if set(rectangles[a]) & set(rectangles[b]):
            continue
        if any(k[a] for k in kernel) and all(k[a]+k[b] == 0 for k in kernel):
            result.append((a,b))
    return rectangles,result


def add_opposite_count_cuts(model, counts, rectangles, template):
    """Uses the established E3 exclusion for nongrid rectangles explicitly."""
    standard, pairs = opposite_pairs(template)
    assert [tuple(q) for q in rectangles] == standard
    for a,b in pairs:
        model.add(counts[a][a] == 4)
        model.add(counts[b][b] == 4)
        model.add(counts[a][b] == 8)
    return {'pairs': [[list(standard[a]),list(standard[b])] for a,b in pairs],
            'uses_E3':True, 'fixed_Gram_required':False, 'constraints':3*len(pairs)}


def add_opposite_row_cuts(model, rectangles, template, terms):
    """Matching corners when the three complementary root pairs are grids."""
    standard,pairs=opposite_pairs(template)
    assert [tuple(q) for q in rectangles]==standard
    nongrid={tuple(q) for q in template['nongrid_edges']}
    selected=set()
    for a,b in pairs:
        rest=set(range(7))-set(standard[a])-set(standard[b])
        if all(tuple(sorted(q)) not in nongrid for q in combinations(rest,2)):
            selected.update((a,b))
    for q in sorted(selected):
        model.add(sum(x for qi,z,x in terms if qi==q and z[q]!=1)==0)
    return {'matching_rectangles':[list(standard[q]) for q in sorted(selected)],
            'constraints':len(selected),'uses_E3':True,'uses_three_complementary_grids':True}


def core_orbits(cores):
    """Only relabellings preserving the two root pairs and their letters.

    For 5602 these all extend to automorphisms of the component template;
    they are coordinate relabellings, not symmetries of a sought graph.
    """
    lookup = {q:i for i,q in enumerate(LABELS)}
    maps = []
    for p in permutations(range(4)):
        if {frozenset((p[0],p[1])),frozenset((p[2],p[3]))} != {frozenset((0,1)),frozenset((2,3))}:
            continue
        for flips in product(range(2), repeat=4):
            maps.append([lookup[tuple(sorted(2*p[a//2]+((a%2)^flips[a//2]) for a in q))] for q in LABELS])
    pairs = list(combinations(range(8),2)); index = {p:i for i,p in enumerate(pairs)}
    transformations = [[index[tuple(sorted((p[i],p[j])))] for i,j in pairs] for p in maps]
    orbits = Counter()
    source_masks = {sum(1<<k for k,(i,j) in enumerate(pairs) if rec['adjacency'][i][j]) for rec in cores}
    assert len(source_masks) == len(cores)
    for mask in source_masks:
        images = {sum(1<<t[k] for k in range(28) if mask & (1<<k)) for t in transformations}
        assert images <= source_masks
        orbits[min(images)] += 1
    output = []
    for mask,size in sorted(orbits.items()):
        g = [[int(bool(mask & (1<<index[tuple(sorted((i,j)))]))) if i != j else 0 for j in range(8)] for i in range(8)]
        output.append({'mask':mask, 'orbit_size':size, 'representative':g})
    return {'group_order':len(maps),'permutations':maps,'orbits':output}


def perfect_matchings(vertices):
    if not vertices:
        yield (); return
    a,*rest=vertices
    for b in rest:
        for tail in perfect_matchings([v for v in rest if v!=b]):
            yield ((a,b),)+tail


def three_grid_extensions(core):
    """Exact edge-factorization and necessary opposite-corner conditions.

    Applicable when the three other root pairs are grids, as in 5602.
    Matching order is immaterial: the three remaining roots induce S3
    on their three pairs. This does not quotient any letter assignments.
    """
    pairs=list(combinations(range(8),2));lookup={p:i for i,p in enumerate(pairs)}
    demand=[2-core[u][v]-len(set(LABELS[u])&set(LABELS[v]))-
            sum(core[u][w]*core[v][w] for w in range(8)) for u,v in pairs]
    assert min(demand)>=0
    assert all(sum(demand[k] for k,p in enumerate(pairs) if w in p)==3 for w in range(8))
    matchings=[tuple(lookup[p] for p in m) for m in perfect_matchings(list(range(8)))
               if all(demand[lookup[p]] for p in m)]
    factors=[]
    oppositions=((1,0,3,2),(2,3,0,1),(3,2,1,0))
    for i,j,k in combinations_with_replacement(range(len(matchings)),3):
        used=Counter(t for m in (matchings[i],matchings[j],matchings[k]) for t in m)
        if any(used[t]!=demand[t] for t in range(28)):continue
        records=[]
        for mi in (i,j,k):
            m=[pairs[t] for t in matchings[mi]]
            requirements=[{'opposite':[e,f],'witness_vertex':x}
                          for e,edge in enumerate(m) for f,other in enumerate(m)
                          if e!=f for x in edge if all(core[x][y] for y in other)]
            allowed=[opp for opp in oppositions if all(opp[r['opposite'][0]]==r['opposite'][1] for r in requirements)]
            records.append({'edges':m,'forced_oppositions':requirements,'allowed_oppositions':allowed})
        factors.append({'matchings':records,'passes':all(m['allowed_oppositions'] for m in records)})
    return {'residual_edge_multiplicities':[[*p,demand[t]] for t,p in enumerate(pairs) if demand[t]],
            'factorizations':factors,'factorization_count':len(factors),
            'surviving_factorization_count':sum(f['passes'] for f in factors),
            'status':'PASSES' if any(f['passes'] for f in factors) else 'EXCLUDED_CORE',
            'scope':'Eight-vertex core plus three grid rectangles; not the whole template.'}


def grid_boundary_orbits(orbit, permutations_of_core):
    """Complete 20-vertex boundary cover, modulo its explicit relabellings."""
    k=orbit['representative'];data=orbit['three_grids']
    if data['status']=='EXCLUDED_CORE':return {'cases':[],'status':'EXCLUDED_CORE'}
    grid_labels=[(a,b) for i,j in ((0,1),(0,2),(1,2)) for a in (2*i,2*i+1) for b in (2*j,2*j+1)]
    label_index={q:i for i,q in enumerate(grid_labels)}
    grid_permutations=[]
    for p in permutations(range(3)):
        for f in product(range(2),repeat=3):
            grid_permutations.append([label_index[tuple(sorted(2*p[a//2]+((a%2)^f[a//2]) for a in q))] for q in grid_labels])
    core_stabilizer=[p for p in permutations_of_core if all(k[i][j]==k[p[i]][p[j]] for i,j in combinations(range(8),2))]
    positions=list(permutations(range(4)));states=set();before=0
    for factor in data['factorizations']:
        if not factor['passes']:continue
        options=[]
        for m in factor['matchings']:
            current=[]
            for p in positions:
                inverse=[p.index(e) for e in range(4)]
                if any((inverse[r['opposite'][0]]^inverse[r['opposite'][1]])!=3 for r in m['forced_oppositions']):continue
                current.append(tuple(sum(1<<x for x in m['edges'][e]) for e in p))
            options.append(current)
        for choice in product(*options):
            state=sum(choice,());before+=1
            if any((state[u]&state[v]).bit_count()>2-len(set(grid_labels[u])&set(grid_labels[v]))
                   for u,v in combinations(range(12),2) if u//4!=v//4):continue
            states.add(state)
    original=len(states);cases=[]
    while states:
        seed=min(states);images=set()
        for p in core_stabilizer:
            mapped=[sum(1<<p[x] for x in range(8) if mask&(1<<x)) for mask in seed]
            for q in grid_permutations:
                image=[0]*12
                for i,j in enumerate(q):image[j]=mapped[i]
                images.add(tuple(image))
        covered=len(states&images);assert covered
        states.difference_update(images)
        cases.append({'core_mask':orbit['mask'],'core_adjacency':k,
                      'core_neighbours_of_grid_vertices':list(min(images)),
                      'full_orbit_size':len(images),'covered_fixed_color_states':covered})
    cases.sort(key=lambda c:c['core_neighbours_of_grid_vertices'])
    assert sum(c['covered_fixed_color_states'] for c in cases)==original
    return {'status':'COMPLETE_BOUNDARY_COVER','vertices':20,
            'core_stabilizer_order':len(core_stabilizer),'grid_relabellings':len(grid_permutations),
            'assignments_before_cross_grid_C2':before,'fixed_matching_order_states':original,
            'cases':cases,'whole_template_excluded':False,
            'scope':'The three matchings are unordered; S3 on the three complementary roots covers their orders.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--boundaries',action='store_true')
    a=p.parse_args(); assert not a.output.exists()
    resources=limit_research_process(1); started=time.process_time()
    result=enumerate_cores()
    result['orbit_reduction'] = core_orbits(result['cores'])
    for orbit in result['orbit_reduction']['orbits']:
        orbit['three_grids'] = three_grid_extensions(orbit['representative'])
        if a.boundaries:
            orbit['boundaries']=grid_boundary_orbits(orbit,result['orbit_reduction']['permutations'])
    result.update(resources=resources,cpu_seconds=time.process_time()-started)
    atomic_json_write(a.output,result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('cores','scope','label_pairs','orbit_reduction')}))
    print(json.dumps({'orbits':[{'mask':o['mask'],'size':o['orbit_size'],
          'three_grid_status':o['three_grids']['status'],
          'factorizations':o['three_grids']['factorization_count']} for o in result['orbit_reduction']['orbits']]}))


if __name__=='__main__': main()
