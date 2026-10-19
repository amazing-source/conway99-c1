# Independent P3NB membership: relation space W = span{e_q : q grid} + span{sum_{j in P} e_{aj} : P component group at a}.
# Member iff exists line permutation pi with pi(Q01),pi(Q02) non-grid, e01+e02 in W (relabelled), Q45,Q46,Q13 grids.
# Compares with p3nb_members.json both ways and validates every recorded witness.
import gzip, json, sys
from fractions import Fraction
from itertools import combinations, permutations
cat = json.load(gzip.open(sys.argv[1]))["open"]; mem = json.load(open(sys.argv[2]))["p3nb"]
R = list(combinations(range(7), 2)); ri = {q: i for i, q in enumerate(R)}
def rank(rows):
    rows = [list(map(Fraction, r)) for r in rows]; rk = 0; ncol = 21
    for c in range(ncol):
        p = next((i for i in range(rk, len(rows)) if rows[i][c] != 0), None)
        if p is None: continue
        rows[rk], rows[p] = rows[p], rows[rk]
        for i in range(len(rows)):
            if i != rk and rows[i][c] != 0:
                f = rows[i][c] / rows[rk][c]; rows[i] = [x - f * y for x, y in zip(rows[i], rows[rk])]
        rk += 1
    return rk
def relations(t):
    ng = {tuple(e) for e in t["nongrid_edges"]}
    rows = []
    for q in R:
        if q not in ng:
            v = [0] * 21; v[ri[q]] = 1; rows.append(v)
    for a, gs in enumerate(t["nontrivial_component_groups"]):
        for P in gs:
            v = [0] * 21
            for j in P: v[ri[tuple(sorted((a, j)))]] = 1
            rows.append(v)
    return ng, rows
def forced(rows, base_rank, a, b, c):
    v = [0] * 21; v[ri[tuple(sorted((a, b)))]] = 1; v[ri[tuple(sorted((a, c)))]] = 1
    return rank(rows + [v]) == base_rank
mine = {}
bad_wit = []
for idx, r in enumerate(cat):
    t = r["template"]; ng, rows = relations(t); br = None; cache = {}
    for pi in permutations(range(7)):      # pi[new] = old line
        a, b, c, w, x, y, z = pi
        g = lambda u, v: tuple(sorted((u, v))) not in ng
        if g(a, b) or g(a, c): continue
        if not (g(x, y) and g(x, z) and g(b, w)): continue
        key = (a, frozenset((b, c)))
        if key not in cache:
            if br is None: br = rank(rows)
            cache[key] = forced(rows, br, a, b, c)
        if cache[key]:
            mine[idx] = list(pi); break
    if str(idx) in mem:
        a, b, c, x, y, z, w = mem[str(idx)]      # recorded order [a, side, other, x, y, z, w]
        ok = (not g(a, b)) and (not g(a, c)) and g(x, y) and g(x, z) and g(b, w) and len({a, b, c, x, y, z, w}) == 7
        if br is None: br = rank(rows)
        ok = ok and forced(rows, br, a, b, c)
        if not ok: bad_wit.append(idx)
ms = set(int(k) for k in mem); my = set(mine)
print(json.dumps({"templates": len(cat), "recorded_members": len(ms), "my_members": len(my),
                  "recorded_not_mine": sorted(ms - my)[:20], "mine_not_recorded": sorted(my - ms)[:20],
                  "invalid_recorded_witnesses": bad_wit[:20]}))
