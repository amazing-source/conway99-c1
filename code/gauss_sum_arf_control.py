"""notes/113 R4 — control of the rule  sum_S (-1)^{|S|+e(S)} = 2^{n - rank/2} (-1)^Arf,  Arf = 1 iff det Lambda_r ≡ 3
(mod 8, up to squares), on T(7) = srg(21,10,5,4): r = 3, s = -2, E_3 = (A+2I)/5 - 4J/35 is 2-integral and ≡ A (mod 2),
the same 2-adic situation as for 99 (E_3 = (A+4I)/7 - 2J/77).  Brute force over all 2^21 subsets.
Negative control: replacing |S|+e(S) by e(S) (wrong refinement) must not give a clean ±2^18."""
import itertools
import numpy as np
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

pairs = list(itertools.combinations(range(7), 2))
n = len(pairs)
A = sp.Matrix(n, n, lambda i, j: 1 if (i != j and set(pairs[i]) & set(pairs[j])) else 0)
# integral basis of Lambda_3 = Z^n ∩ ker(A - 3I): integer kernel vectors, then saturate via the Smith form
K = sp.Matrix.hstack(*[k * sp.lcm([sp.fraction(x)[1] for x in k]) for k in (A - 3 * sp.eye(n)).nullspace()])
snf = smith_normal_form(K, domain=sp.ZZ)
idx = sp.prod([abs(snf[i, i]) for i in range(K.shape[1])])
det = (K.T * K).det() / idx ** 2
print("rank", K.shape[1], "det Lambda_3 =", det, sp.factorint(det), "= ", det % 8, "(mod 8)")
pred = 2 ** (n - K.shape[1] // 2) * (1 if det % 8 == 7 else -1)

adj = [sum(1 << j for j in range(n) if A[i, j]) for i in range(n)]
e = np.zeros(1 << n, dtype=np.int64)
s = np.zeros(1 << n, dtype=np.int64)
for S in range(1, 1 << n):
    v = (S & -S).bit_length() - 1
    R = S & (S - 1)
    e[S] = e[R] + bin(adj[v] & R).count("1")
    s[S] = s[R] + 1
val = int(np.where((e + s) % 2 == 0, 1, -1).sum())
neg = int(np.where(e % 2 == 0, 1, -1).sum())
print("predicted", pred, "| brute force sum (-1)^{|S|+e(S)} =", val, "| negative control sum (-1)^{e(S)} =", neg)
assert val == pred
