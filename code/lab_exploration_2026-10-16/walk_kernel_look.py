import json, sys
sys.path.insert(0, ".")
from r30_kernel_look import S, K8, nullspace_frac, to_int, lll, rank_frac, XL, Y, YP, Q
from c1_margin56 import gl_connected
for f in sys.argv[1:]:
    d = json.load(open(f))
    lab = [frozenset(x) for x in d["labels"]]
    EE = {frozenset((lab[i], lab[j])) for i, j in d["edges"]}
    G = [[1 if i != j and frozenset((S[i], S[j])) in EE else 0 for j in range(44)] for i in range(44)]
    T8 = [[24 * (i == j) - 8 * G[i][j] - K8[i][j] for j in range(44)] for i in range(44)]
    ker = nullspace_frac(T8)
    Ki = [to_int(v) for v in ker]
    print(f.split("/")[-1].split("\\")[-1], "nu =", len(ker), "conn", gl_connected(EE))
    def inter_dim(zero_idx):
        M = [[Ki[b][i] for b in range(len(Ki))] for i in zero_idx]
        return len(Ki) - rank_frac(M)
    print("  vanish on Y:", inter_dim(Y), "| on X_l:", inter_dim(XL), "| on Y':", inter_dim(YP), "| on Q:", inter_dim(Q))
    R = lll(Ki)
    R.sort(key=lambda v: sum(x * x for x in v))
    for v in R:
        supp = [(sorted(S[i]), v[i]) for i in range(44) if v[i]]
        print("   norm %d supp %d :" % (sum(x * x for x in v), len(supp)), " ".join("%d%d:%+d" % (a[0], a[1], c) for a, c in supp))
