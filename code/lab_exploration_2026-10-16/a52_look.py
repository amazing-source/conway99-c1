"""The 52 three-star objects (stars 0,1,2; c(l) = 1; rank 30): kernel of T (34 labels), LLL; rectangle e-values."""
import json, sys, itertools
from fractions import Fraction
sys.path.insert(0, ".")
from r30_kernel_look import nullspace_frac, to_int, lll
from c1_margin56 import k8
d = json.load(open(sys.argv[1]))
lab = [frozenset(x) for x in d["labels"]]
n = len(lab)
K8 = [[k8(a, b) for b in lab] for a in lab]
from collections import Counter
prof = Counter()
for k in [int(t) for t in sys.argv[2].split(",")]:
    s = d["structures"][k]
    EE = {frozenset((lab[i], lab[j])) for i, j in s["edges"]}
    G = [[1 if i != j and frozenset((lab[i], lab[j])) in EE else 0 for j in range(n)] for i in range(n)]
    T8 = [[24 * (i == j) - 8 * G[i][j] - K8[i][j] for j in range(n)] for i in range(n)]
    ker = nullspace_frac(T8)
    R = lll([to_int(v) for v in ker]); R.sort(key=lambda v: sum(x * x for x in v))
    def e(Q): return sum(1 for x, y in itertools.combinations(Q, 2) if frozenset((x, y)) in EE)
    el = [e([frozenset((r, t)) for r in (0, 1) for t in (a, a ^ 1)]) for a in range(2, 14, 2)]
    print("obj", k, "nullity", len(ker), "l-rect e:", el)
    for v in R:
        supp = [(sorted(lab[i]), v[i]) for i in range(n) if v[i]]
        print("   norm %d supp %d :" % (sum(x * x for x in v), len(supp)), " ".join("%d%d:%+d" % (a[0], a[1], c) for a, c in supp))
