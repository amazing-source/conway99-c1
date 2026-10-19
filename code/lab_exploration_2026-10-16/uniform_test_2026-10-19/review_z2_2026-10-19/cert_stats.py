import gzip, json, sys
from fractions import Fraction
from collections import Counter
from itertools import combinations
CAT = sys.argv[1]; CDIR = sys.argv[2]
d = json.loads(gzip.decompress(open(CAT,'rb').read()))
RECT = list(combinations(range(7),2))
for g in [9748, 5986, 5984, 9997, 5128]:
    T = d['open'][g]['template']
    ng = {tuple(e) for e in T['nongrid_edges']}
    # well-formedness
    ok = True
    from_groups = set()
    for i, groups in enumerate(T['nontrivial_component_groups']):
        flat = [j for P in groups for j in P]
        if len(flat) != len(set(flat)) or i in flat or any(len(P) < 2 for P in groups):
            ok = False
        for j in flat:
            from_groups.add(tuple(sorted((i,j))))
    # symmetric: (i,j) in group at i  <=> j-line group contains i
    sym = all(any(i in P for P in T['nontrivial_component_groups'][j]) == any(j in P for P in T['nontrivial_component_groups'][i]) for i in range(7) for j in range(7) if i != j)
    cf = json.load(open(CDIR + '/z2_%d.json' % g))
    print('gz', g, 'wellformed', ok, 'nongrid==groups', ng == from_groups, 'symmetric', sym, '#nongrid', len(ng),
          'groups', T['nontrivial_component_groups'], 'counts', T.get('component_count_by_root_line'))
    print('   cert keys:', [k for k in cf.keys()], 'status', cf.get('status'), 'idx', cf.get('template_index'), 'sha', cf.get('catalogue_sha256','')[:16])
    if 'certificate_explicit' in cf:
        ce = cf['certificate_explicit']
        fam = Counter()
        for part in ('y_eq','y_ub','y_up'):
            for k,v in ce[part].items():
                fam[(part, k.split('|')[0])] += 1
        print('   families:', dict(fam))
        print('   E3n multipliers:', {k: v for k, v in ce['y_ub'].items()})
