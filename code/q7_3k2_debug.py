exec(open('q7_3k2_sibrows.py', encoding='utf-8').read().split("import random")[0])
from collections import Counter
(i, j, k) = assign_list = None, None, None
assign = [(i, j, k) for (i, j) in AB for k in range(len(per['C'])) if (j, k) in BC and (k, i) in CA]
i, j, k = assign[0]
sib = {'A': per['A'][i], 'B': per['B'][j], 'C': per['C'][k]}
print('sib shadows A:', sib['A'])
for p in cross_pairs:
    for rep in [((p[0], 1), (p[1], 1)), ((p[0], 1), (p[1], -1))]:
        opts = cross_shadow_options(p)
        fail = Counter()
        nok = 0
        for sh in opts:
            first = None
            for name in 'ABC':
                zs = [Z(orbit_data(name)[t], sib[name][t], rep, sh) for t in range(2)]
                if sib_T_pattern(p, name) == 'zero':
                    if zs != [0, 0]:
                        first = (name, 'zero', tuple(zs)); break
                else:
                    if sorted(1 if z in (1, 6) else (0 if z == 0 else 9) for z in zs) != [0, 1]:
                        first = (name, 'oneof', tuple(zs)); break
            if first is None:
                nok += 1
            else:
                fail[first[:2]] += 1
        print('pair', p, 'rep', rep, 'options', len(opts), 'ok', nok, 'fail reasons', dict(fail))
