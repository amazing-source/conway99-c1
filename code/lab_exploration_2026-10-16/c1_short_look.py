import itertools, json, sys, math
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, XL, Y, k8, relabel, build_H, gl_connected
from c1_e3free_floor import e3_free
from sympy import Matrix, ZZ
from sympy.polys.matrices import DomainMatrix

def name(x):
    if isinstance(x, tuple):
        return ("v" if x[1] == "v" else str(x[1])) if x[0] == "P" else "L%d" % x[1]
    return "{" + ",".join(str(t) for t in sorted(x)) + "}"

targets = {"og3_h_c21_NEAR_2.json": 0, "visits_archive_2026-10-14_15": 1}
for line in open(sys.argv[1]):
    d = json.loads(line)
    src = d.get("src", "")
    hit = [k for k in targets if src.startswith(k)]
    if not hit or len(d["labels"]) != 44:
        continue
    side = targets[hit[0]]
    S0 = [frozenset(x) for x in d["labels"]]
    E0 = [(frozenset(a), frozenset(b)) for a, b in d["edges"]]
    L, EE = relabel(S0, E0, side)
    V, A = build_H(EE, with_l=True)
    n = len(V)
    ns = Matrix((A - 3 * np.eye(n, dtype=np.int64)).tolist()).nullspace()
    rows = []
    for v in ns:
        den = 1
        for t in v:
            den = den * t.q // math.gcd(den, t.q)
        rows.append([int(t * den) for t in v])
    red = DomainMatrix([[ZZ(x) for x in r] for r in rows], (len(rows), n), ZZ).lll().to_Matrix().tolist()
    best = min(red, key=lambda r: sum(int(x) ** 2 for x in r))
    nz = [i for i in range(n) if best[i]]
    print("==", src, "side", side, ": shortest vector, norm", sum(int(x) ** 2 for x in best))
    print("   values:", [(name(V[i]), int(best[i])) for i in nz])
    sub = [V[i] for i in nz]
    print("   induced edges on the support:", [(name(a), name(b)) for a, b in itertools.combinations(sub, 2) if A[V.index(a), V.index(b)]])
    # neighbours of the support outside it, with their sums
    out = []
    for j in range(n):
        if j in nz:
            continue
        s = sum(int(best[i]) for i in nz if A[j, i])
        if any(A[j, i] for i in nz):
            out.append((name(V[j]), s))
    print("   outside vertices touching the support (name, sum of values over their support-neighbours = 0 required):", out)
    del targets[hit[0]]
    if not targets:
        break
