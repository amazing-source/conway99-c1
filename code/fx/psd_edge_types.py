"""Euclidean test of the 27-vertex induced subgraph N[x] u N[a], fully determined by the type of B_xa (note 177)."""
import numpy as np, sys

from psd_configs import mins
def partitions(n, mx=None):
    mx = mx or n
    if n == 0: yield (); return
    for p in range(min(n, mx), 0, -1):
        for rest in partitions(n - p, p): yield (p,) + rest
def core(tau, m):
    # vertices: x=0, a=1, a'=2, U = N(x)-T0 (2(m-1)), W = N(a)-T0 (2(m-1))
    M = m - 1; n = 3 + 4 * M; A = np.zeros((n, n))
    def ed(p, q): A[p, q] = A[q, p] = 1
    ed(0, 1); ed(0, 2); ed(1, 2)
    U = list(range(3, 3 + 2 * M)); W = list(range(3 + 2 * M, 3 + 4 * M))
    for u in U: ed(0, u)
    for w in W: ed(1, w)
    for j in range(M): ed(U[2 * j], U[2 * j + 1]); ed(W[2 * j], W[2 * j + 1])   # mates at x, triangles at a
    # bijection f: U -> W realising tau: x-pairs P_j = (U[2j],U[2j+1]), a-pairs Q_j = (W[2j],W[2j+1])
    i = 0
    for l in tau:
        for j in range(l):
            P = (U[2 * (i + j)], U[2 * (i + j) + 1]); Q = (W[2 * (i + j)], W[2 * (i + j) + 1])
            Pn = (U[2 * (i + (j + 1) % l)], U[2 * (i + (j + 1) % l) + 1])
            ed(P[1], Q[0])            # P_j --Q_j
            ed(Q[1], Pn[0])           # Q_j -- P_{j+1}  (for l=1: Q_j -- P_j: double edge = prism)
        i += l
    assert all(A[u].sum() >= 1 for u in range(n))
    return A
for v, m in ((99, 7), (243, 11)):
    print(f"== v={v} (m={m})")
    for tau in partitions(m - 1):
        if v == 243 and len(tau) > 6: continue
        ms, mr = mins(core(tau, m), v)
        print(f"   type {''.join(map(str, tau)):12s} min eig G_s={ms:+.4f} G_r={mr:+.4f} {'IMPOSSIBLE' if min(ms, mr) < -1e-9 else ''}")
