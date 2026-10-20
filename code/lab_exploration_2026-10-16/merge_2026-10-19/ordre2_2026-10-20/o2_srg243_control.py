"""Positive control on a REAL srg(v,k,1,2) (here srg(243,22,1,2)): the two far projectors of a line computed from
LOCAL data only (G_T, names of the far vertices, far adjacency R) against the true ones (LAB, NOTE_ORDRE2, 20/10/2026).

For a line T, n = k - 2, classes C_i = N(t_i) - T (n each), G = G_T cubic, F = far set, E = near-far incidence,
eigenvalues r > s of A (r + s = -1, rs = 2 - k).  Claimed (proof in NOTE_ORDRE2_7ADIQUE.md §3):
   (r - s) Pi^(r)_ab = R_ab - s d_ab - 2/(n-2) - 2(r-3)/(n(n-2)) - f_a^T (G - sI)^{-1} f_b
   (r - s) Pi^(s)_ab = r d_ab - R_ab + 2/(n-2) - 2(r+4)/(n(n-2)) - f_a^T (rI - G)^{+} f_b      (r > 3 here)
with f_a = e_a - (2/n) 1 (e_a = indicator of the 6 names of a), Pi^(theta) = orthogonal projector onto the theta
eigenvectors of A supported on F.  Truth: Schur complement of the global projector P_theta on N[T].
usage: python o2_srg243_control.py <edges> [line index] [star vertex index]"""
import sys

import numpy as np


def main():
    path = sys.argv[1]
    li = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    xi = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    ed = [tuple(map(int, l.split())) for l in open(path) if l.strip()]
    v = 1 + max(max(e) for e in ed)
    A = np.zeros((v, v))
    for i, j in ed:
        A[i, j] = A[j, i] = 1
    k = int(A[0].sum())
    disc = np.sqrt(1 + 4 * (k - 2))
    r, s = (-1 + disc) / 2, (-1 - disc) / 2
    assert abs(r - round(r)) < 1e-9
    r, s = int(round(r)), int(round(s))
    adj = [set(np.nonzero(A[i])[0]) for i in range(v)]
    # lines
    lines = []
    seen = set()
    for a in range(v):
        for b in adj[a]:
            c = (adj[a] & adj[b])
            assert len(c) == 1
            t = frozenset((a, b, next(iter(c))))
            if t not in seen:
                seen.add(t)
                lines.append(sorted(t))
    T = lines[li]
    n = k - 2
    C = []
    for i, t in enumerate(T):
        rest = sorted(adj[t] - set(T))
        # order so that partners are consecutive (partner of x = common neighbour of t and x)
        order, used = [], set()
        for x in rest:
            if x in used:
                continue
            p = next(iter(adj[t] & adj[x]))
            order += [x, p]
            used |= {x, p}
        C.append(order)
    Nn = C[0] + C[1] + C[2]
    near = list(T) + Nn
    F = [w for w in range(v) if w not in set(near)]
    assert len(Nn) == 3 * n and len(F) == v - 3 - 3 * n
    G = A[np.ix_(Nn, Nn)]
    assert set(G.sum(1)) == {3.0}
    E = A[np.ix_(Nn, F)]
    R = A[np.ix_(F, F)]
    # global projectors
    I = np.eye(v)
    J = np.ones((v, v))
    Pr = (A - s * I) @ (A - k * I) / ((r - s) * (r - k))
    Ps = (A - r * I) @ (A - k * I) / ((s - r) * (s - k))

    def far_proj(P):
        Pnn = P[np.ix_(near, near)]
        Pfn = P[np.ix_(F, near)]
        return P[np.ix_(F, F)] - Pfn @ np.linalg.pinv(Pnn, rcond=1e-9, hermitian=True) @ Pfn.T

    Pir_true, Pis_true = far_proj(Pr), far_proj(Ps)
    # local formulas
    N3 = 3 * n
    f = E - (2.0 / n)
    Ms = np.linalg.inv(G - s * np.eye(N3))
    Mr = np.linalg.pinv(r * np.eye(N3) - G)
    m = len(F)
    Ir = np.eye(m)
    loc_r = R - s * Ir - 2.0 / (n - 2) - 2.0 * (r - 3) / (n * (n - 2)) - f.T @ Ms @ f
    loc_s = r * Ir - R + 2.0 / (n - 2) - 2.0 * (r + 4) / (n * (n - 2)) - f.T @ Mr @ f
    err_r = np.abs(loc_r - (r - s) * Pir_true).max()
    err_s = np.abs(loc_s - (r - s) * Pis_true).max()
    ev_r = np.linalg.eigvalsh(Pir_true)
    ev_s = np.linalg.eigvalsh(Pis_true)
    rank_r = int((ev_r > 0.5).sum())
    rank_s = int((ev_s > 0.5).sum())
    # components of G
    comp, cc = [-1] * N3, 0
    for st in range(N3):
        if comp[st] >= 0:
            continue
        stack = [st]
        comp[st] = cc
        while stack:
            u = stack.pop()
            for w2 in np.nonzero(G[u])[0]:
                if comp[w2] < 0:
                    comp[w2] = cc
                    stack.append(w2)
        cc += 1
    # star of the near vertex Nn[xi]: far vertices adjacent to it
    x = Nn[xi]
    S = [j for j, w in enumerate(F) if A[x, w]]
    blk_r = loc_r[np.ix_(S, S)]
    blk_s = loc_s[np.ix_(S, S)]
    # the -4-like block must annihilate 1_S; the r-block too (1_S is in the row space of E)
    one = np.ones(len(S))
    print({"graph": path.split("/")[-1].split("\\")[-1], "k": k, "r": r, "s": s, "line": T, "c(G_T)": cc,
           "far": m, "max|local-true| r": float(err_r), "max|local-true| s": float(err_s),
           "rank Pi^(r)": rank_r, "rank Pi^(s)": rank_s,
           "eig Pi^(r) in {0,1}": bool(np.all(np.minimum(np.abs(ev_r), np.abs(ev_r - 1)) < 1e-8)),
           "eig Pi^(s) in {0,1}": bool(np.all(np.minimum(np.abs(ev_s), np.abs(ev_s - 1)) < 1e-8)),
           "star size": len(S), "star block r min eig": float(np.linalg.eigvalsh(blk_r).min()),
           "star block s min eig": float(np.linalg.eigvalsh(blk_s).min()),
           "|blk_r 1|": float(np.abs(blk_r @ one).max()), "|blk_s 1|": float(np.abs(blk_s @ one).max())})


if __name__ == "__main__":
    main()
