"""Letter image L_img of K = ker(3I - A_Omega) and its orthogonal complement (relations among letters), exact."""
import json, sys
sys.path.insert(0, ".")
from r30_kernel_look import S, nullspace_frac, to_int, lll
from c1_newinv import ball
d = json.load(open(sys.argv[1]))
lab = [frozenset(x) for x in d["labels"]]
items = []
if "structures" in d:
    for k in [int(t) for t in sys.argv[2].split(",")]:
        s = d["structures"][k]
        items.append(("obj%d c=%s" % (k, s["c"]), {frozenset((lab[i], lab[j])) for i, j in s["edges"]}))
else:
    items.append((sys.argv[1].split("/")[-1], {frozenset((lab[i], lab[j])) for i, j in d["edges"]}))
for name, EE in items:
    A = ball(EE)
    M = [[(3 if i == j else 0) - int(A[i][j]) for j in range(59)] for i in range(59)]
    K = nullspace_frac(M)
    # letter parts: coords 1..14
    Lp = [[v[1 + a] for a in range(14)] for v in K]
    rel = nullspace_frac(Lp) if Lp else []
    print(name, "nu =", len(K), "dim letter image =", 14 - len(rel))
    R = lll([to_int(v) for v in rel]) if rel else []
    for v in R:
        print("   relation on letters 0..13:", v)
