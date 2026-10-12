"""Lab session, 2026-10-12. Feasibility checks (exact rational arithmetic) of an intersection array of a distance-regular
graph of diameter d with integral eigenvalues: multiplicities, Krein parameters q^k_ij (must be >= 0), absolute bound
m_i m_j >= sum of m_k over the k with q^k_ij > 0 (i != j), m_i (m_i + 1) / 2 for i = j.
python drg_feasible.py "20,18,3,1;1,3,18,20" "20,5,2,-4,-7"      (array, then the eigenvalues)"""
import sys
from fractions import Fraction as Fr
bs, cs = sys.argv[1].split(";"); b = [int(t) for t in bs.split(",")]; c = [int(t) for t in cs.split(",")]
thetas = [int(t) for t in sys.argv[2].split(",")]; d = len(b); k = b[0]
a = [k - (b[i] if i < d else 0) - (c[i - 1] if i > 0 else 0) for i in range(d + 1)]
kk = [1]
for i in range(d): kk.append(Fr(kk[-1] * b[i], c[i]))
v = sum(kk); print("a_i =", a, " k_i =", [str(t) for t in kk], " v =", v)
def stdseq(th):
    u = [Fr(1), Fr(th, k)]
    for i in range(1, d): u.append((th * u[i] - c[i - 1] * u[i - 1] - a[i] * u[i]) / b[i])
    assert c[d - 1] * u[d - 1] + a[d] * u[d] == th * u[d], "%d is not an eigenvalue" % th
    return u
U = [stdseq(t) for t in thetas]
m = [Fr(v) / sum(kk[l] * U[i][l] ** 2 for l in range(d + 1)) for i in range(d + 1)]
print("eigenvalues", thetas, "multiplicities", [str(t) for t in m], "(sum %s)" % sum(m))
ok = all(t.denominator == 1 and t > 0 for t in m); bad = []
q = {}
for i in range(d + 1):
    for j in range(d + 1):
        for h in range(d + 1):
            q[(i, j, h)] = m[i] * m[j] / v * sum(kk[l] * U[i][l] * U[j][l] * U[h][l] for l in range(d + 1))
            if q[(i, j, h)] < 0: bad.append((thetas[i], thetas[j], thetas[h], str(q[(i, j, h)])))
print("integral multiplicities:", ok); print("negative Krein parameters:", bad if bad else "none")
for i in range(d + 1):
    for j in range(i, d + 1):
        s = sum(m[h] for h in range(d + 1) if q[(i, j, h)] > 0); bound = m[i] * m[j] if i != j else m[i] * (m[i] + 1) / 2
        flag = "" if s <= bound else "   <-- ABSOLUTE BOUND VIOLATED"
        print("  (%3d,%3d): q = %s; sum of m_k = %s <= %s%s" % (thetas[i], thetas[j], [str(q[(i, j, h)]) for h in range(d + 1)], s, bound, flag))
