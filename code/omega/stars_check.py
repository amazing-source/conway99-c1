import numpy as np
from graphs_test import bvls243
A = bvls243(); n, r = 243, 4
v = 0; Nv = list(np.nonzero(A[v])[0]); U = [v] + Nv; L = [w for w in range(n) if w not in U]
M = r * np.eye(n) - A
T = M[np.ix_(L, L)] - M[np.ix_(L, U)] @ np.linalg.solve(M[np.ix_(U, U)], M[np.ix_(U, L)])
B = A[np.ix_(Nv, L)]
print("max |B T| =", np.abs(B @ T).max(), " (star sums vanish)")
mate = {a: [c for c in Nv if A[a, c]][0] for a in Nv}
a = Nv[0]; ap = mate[a]
La = [i for i, w in enumerate(L) if A[w, a]]; Lap = [i for i, w in enumerate(L) if A[w, ap]]
S = La + Lap
G = A[np.ix_([L[i] for i in S], [L[i] for i in S])]
degs_in = [G[i, :len(La)].sum() for i in range(len(S))]
print("|L_a|, |L_a'| =", len(La), len(Lap), "; degrees of Gamma on L_a u L_a': within own star / other star:",
      set((G[i, :len(La)].sum(), G[i, len(La):].sum()) for i in range(len(La))),
      set((G[i, :len(La)].sum(), G[i, len(La):].sum()) for i in range(len(La), len(S))))
print("rank of T on L_a u L_a' =", np.linalg.matrix_rank(T[np.ix_(S, S)]), " (= |S| - 2 means only the two star relations)")
