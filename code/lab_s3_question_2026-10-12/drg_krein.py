"""Lab session, 2026-10-12. A regular-spread srg(243,22,1,2) minus its spread is a distance-regular graph with
intersection array {20,18,4,1; 1,2,18,20} (antipodal 3-cover of the Brouwer-Haemers graph), and conversely.
This script computes, in exact rational arithmetic, the eigenvalues, multiplicities, standard sequences and Krein
parameters q^k_ij of that array, and lists the vanishing ones.
python drg_krein.py"""
from fractions import Fraction as Fr
b = [20, 18, 4, 1]; c = [1, 2, 18, 20]; d = 4; k = 20
a = [k - (b[i] if i < d else 0) - (c[i - 1] if i > 0 else 0) for i in range(d + 1)]
kk = [1]
for i in range(d): kk.append(kk[-1] * b[i] // c[i])
v = sum(kk); print("a_i =", a, " k_i =", kk, " v =", v)
thetas = [20, 5, 2, -4, -7]
def stdseq(th):                      # u_0 = 1, u_1 = th/k, c_i u_{i-1} + a_i u_i + b_i u_{i+1} = th u_i
    u = [Fr(1), Fr(th, k)]
    for i in range(1, d): u.append((th * u[i] - c[i - 1] * u[i - 1] - a[i] * u[i]) / b[i])
    assert c[d - 1] * u[d - 1] + a[d] * u[d] == th * u[d], th
    return u
U = [stdseq(t) for t in thetas]
m = [Fr(v) / sum(kk[l] * U[i][l] ** 2 for l in range(d + 1)) for i in range(d + 1)]
print("eigenvalues", thetas, "multiplicities", [str(x) for x in m])
for i in range(d + 1): print("  theta = %3d: standard sequence %s" % (thetas[i], [str(x) for x in U[i]]))
print("Krein parameters q^k_ij (i <= j), zero ones marked:")
zeros = []
for i in range(d + 1):
    for j in range(i, d + 1):
        row = []
        for h in range(d + 1):
            qv = m[i] * m[j] / v * sum(kk[l] * U[i][l] * U[j][l] * U[h][l] for l in range(d + 1))
            row.append(qv)
            if qv == 0: zeros.append((thetas[i], thetas[j], thetas[h]))
            assert qv >= 0, "Krein condition violated"
        print("  (%3d,%3d): %s" % (thetas[i], thetas[j], ["%s" % x for x in row]))
print("vanishing q^k_ij as (theta_i, theta_j, theta_k):", zeros)
