"""Lab session, 2026-10-13. Mission "C2 without computation", step 1 (forcing a short vector by modular forms).

Setting (Theorem R of the reduction): U odd unimodular of rank 24, J = Z y1 + Z y2 with Gram 7 I_2, N = U n J^perp
(rank 22, odd, determinant 49, discriminant form the anisotropic plane over F_7), N_0 = even sublattice of N.
The theta series of the cosets of N_0 in its dual form a vector-valued modular form of weight 11 for the Weil
representation of A = N_0^*/N_0 = A_2 + A_7:
   A_2 = (Z/2)^2 = {0, o, s, s'} with q = 0, 1/2, 1/4, 1/4 (o: vectors of odd norm; s, s': the two halves of the shadow),
   A_7 = F_7^2 with q(x) = 3 (x1^2 + x2^2) / 7.
Signature 22 = 6 mod 8 (checked on the Gauss sum below).

This script computes dim M_11(rho) on (a) the subspace symmetric under gamma -> -gamma ("fine", dimension 100) and
(b) its part symmetric under the exchange s <-> s' ("coarse", dimension 75), with the formula
   dim M_k = d + d k / 12 - alpha(e^{pi i k/2} rho(S)) - alpha((e^{pi i k/3} rho(ST))^{-1}) - alpha(rho(T)),
alpha(X) = sum of the beta in [0,1) with eigenvalues e^{2 pi i beta}  (checked on the trivial representation, k = 2..14).
python weil_dimension.py        numpy, a few seconds, memory small."""
import numpy as np, itertools, cmath, math
from fractions import Fraction
e = lambda x: cmath.exp(2j * math.pi * x)
A2 = [(0, 0), (1, 1), (1, 0), (0, 1)]                     # 0, o, s, s'  (o = s + s')
q2 = {(0, 0): Fraction(0), (1, 1): Fraction(1, 2), (1, 0): Fraction(1, 4), (0, 1): Fraction(1, 4)}
add2 = lambda a, b: ((a[0] + b[0]) % 2, (a[1] + b[1]) % 2)
b2 = lambda a, b: (q2[add2(a, b)] - q2[a] - q2[b]) % 1
A7 = list(itertools.product(range(7), repeat=2))
q7 = lambda x: Fraction(3 * (x[0] * x[0] + x[1] * x[1]) % 7, 7)
b7 = lambda x, y: Fraction(6 * (x[0] * y[0] + x[1] * y[1]) % 7, 7)
A = [(a, x) for a in A2 for x in A7]; idx = {g: i for i, g in enumerate(A)}; n = len(A)
q = [(q2[a] + q7(x)) % 1 for a, x in A]
gauss = sum(e(float(v)) for v in q) / math.sqrt(n)
print("Gauss sum / sqrt|A| = %.6f%+.6fi   (e(6/8) = %.6f%+.6fi)" % (gauss.real, gauss.imag, e(6 / 8).real, e(6 / 8).imag))
T = np.diag([e(float(v)) for v in q])
S = np.zeros((n, n), dtype=complex)
for i, (a, x) in enumerate(A):
    for j, (c, y) in enumerate(A):
        S[j, i] = e(-6 / 8) / math.sqrt(n) * e(-float(b2(a, c) + b7(x, y)))
neg = lambda g: (g[0], ((-g[1][0]) % 7, (-g[1][1]) % 7))
swap = lambda g: ((g[0][1], g[0][0]), g[1])
print("checks: S^2 = -(gamma -> -gamma): %s ; (ST)^3 = S^2: %s" % (
    np.allclose(S @ S, -np.array([[1.0 if A[i] == neg(A[j]) else 0.0 for j in range(n)] for i in range(n)])),
    np.allclose(np.linalg.matrix_power(S @ T, 3), S @ S)))

def subspace(use_swap):
    seen = set(); cols = []
    for g in A:
        orb = {g, neg(g)}
        if use_swap: orb |= {swap(h) for h in orb}
        key = min(orb)
        if key in seen: continue
        seen.add(key); v = np.zeros(n, dtype=complex)
        for h in orb: v[idx[h]] = 1
        cols.append(v / np.linalg.norm(v))
    return np.array(cols).T

def alpha(X):
    w = np.linalg.eigvals(X); tot = Fraction(0)
    for z in w:
        assert abs(abs(z) - 1) < 1e-8
        b = (cmath.phase(z) / (2 * math.pi)) % 1.0
        f = Fraction(b).limit_denominator(168)
        assert abs(float(f) - b) < 1e-7 or abs(float(f) - b - 1) < 1e-7, (b, f)
        tot += f % 1
    return tot

def dim_M(W, k):
    d = W.shape[1]; Sw = W.conj().T @ S @ W; Tw = W.conj().T @ T @ W
    a1 = alpha(cmath.exp(1j * math.pi * k / 2) * Sw)
    a2 = alpha(np.linalg.inv(cmath.exp(1j * math.pi * k / 3) * Sw @ Tw))
    a3 = alpha(Tw)
    return d + Fraction(d * k, 12) - a1 - a2 - a3, d

for name, sw in (("fine (symmetric under -1)", False), ("coarse (also symmetric under s <-> s')", True)):
    W = subspace(sw); assert np.allclose(S @ W, W @ (W.conj().T @ S @ W)) and np.allclose(T @ W, W @ (W.conj().T @ T @ W))
    for k in (11,):
        dm, d = dim_M(W, k)
        print("%s: dimension of the representation %d ; dim M_%d = %s" % (name, d, k, dm))
