"""K_0 = {y on S : Gamma_S y = 3y, B y = 0}: exact basis (Fractions) + LLL, on rank-30 objects or walk files."""
import json, sys
sys.path.insert(0, ".")
from r30_kernel_look import S, nullspace_frac, to_int, lll
Bm = [[1 if r in l else 0 for l in S] for r in range(14)]
def k0(EE):
    G = [[1 if i != j and frozenset((S[i], S[j])) in EE else 0 for j in range(44)] for i in range(44)]
    M = [[(3 if i == j else 0) - G[i][j] for j in range(44)] for i in range(44)] + Bm
    return nullspace_frac(M)
src = sys.argv[1]
d = json.load(open(src))
items = []
if "structures" in d:
    lab = [frozenset(x) for x in d["labels"]]
    for k in [int(t) for t in sys.argv[2].split(",")]:
        s = d["structures"][k]
        items.append(("obj%d c=%s" % (k, s["c"]), {frozenset((lab[i], lab[j])) for i, j in s["edges"]}))
else:
    lab = [frozenset(x) for x in d["labels"]]
    items.append((src.split("/")[-1], {frozenset((lab[i], lab[j])) for i, j in d["edges"]}))
for name, EE in items:
    ker = k0(EE)
    print(name, "dim K_0 =", len(ker))
    if ker:
        R = lll([to_int(v) for v in ker])
        R.sort(key=lambda v: sum(x * x for x in v))
        for v in R:
            supp = [(sorted(S[i]), v[i]) for i in range(44) if v[i]]
            print("   norm %d supp %d :" % (sum(x * x for x in v), len(supp)), " ".join("%d%d:%+d" % (a[0], a[1], c) for a, c in supp))
