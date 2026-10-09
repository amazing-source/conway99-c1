"""C1, lab, 2026-10-09. Integrality of the order-<=10 census of an srg(99,14,1,2).

The census gives, for every graph H on at most 10 vertices, the number of labelled induced embeddings of H as an
integer affine form in 549 parameters (unlabelled counts of the parameter types). The number of induced copies is
form / |Aut H|, an integer: so form(x) = 0 modulo |Aut H| for every H. This script collects the congruences that are
not identically satisfied and says what they force.

python census_cong.py <census json>      One process, about 1 GB (the json), a few minutes."""
import sys, json, time, collections
from fractions import Fraction as Fr

def aut_order(rows):
    n = len(rows)
    adj = [[(rows[i] >> j) & 1 for j in range(n)] for i in range(n)]
    deg = [sum(a) for a in adj]
    # invariant: degree and sorted neighbour degrees
    inv = [(deg[i], tuple(sorted(deg[j] for j in range(n) if adj[i][j]))) for i in range(n)]
    order = sorted(range(n), key=lambda i: (sum(1 for j in range(n) if inv[j] == inv[i]), inv[i]))
    cnt = 0; img = [-1] * n; used = [False] * n
    def rec(k):
        nonlocal cnt
        if k == n: cnt += 1; return
        v = order[k]
        for w in range(n):
            if used[w] or inv[w] != inv[v]: continue
            ok = True
            for t in range(k):
                u = order[t]
                if adj[v][u] != adj[w][img[u]]: ok = False; break
            if ok:
                img[v] = w; used[w] = True; rec(k + 1); used[w] = False
    rec(0); return cnt

if __name__ == "__main__":
    t0 = time.time(); D = json.load(open(sys.argv[1])); npar = len(D["params"])
    pk = {(p[0], p[1]): i + 1 for i, p in enumerate(D["params"])}
    cong = []; stats = collections.Counter(); chk = 0
    for n in ("6", "7", "8", "9", "10"):
        for key, rows, aut, form in D["types"][n]:
            if not form: stats[(n, "empty form")] += 1; continue
            a = aut_order(rows)
            if aut is not None:
                assert a == aut, (n, key, a, aut)
                chk += 1
            i = pk.get((int(n), key))
            if i is not None: assert form == {str(i): str(a)}, (n, key, form, a)
            f = {int(p): int(Fr(v)) % a for p, v in form.items()}
            f = {p: v for p, v in f.items() if v}
            if f:
                cong.append((a, f, n, key)); stats[(n, "non-trivial congruence")] += 1
            else: stats[(n, "trivial")] += 1
    print("automorphism orders recomputed and equal to the stored ones for %d types" % chk)
    for k, v in sorted(stats.items()): print(k, v)
    print("non-trivial congruences:", len(cong), " [%.0f s]" % (time.time() - t0))
    json.dump([[a, {str(p): v for p, v in f.items()}, n, key] for a, f, n, key in cong], open(sys.argv[2], "w"))
    for a, f, n, key in cong[:10]: print("  modulo", a, ":", dict(list(f.items())[:8]), "order", n)
