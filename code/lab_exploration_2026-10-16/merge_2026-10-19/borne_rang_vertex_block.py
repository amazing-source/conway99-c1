"""Rank-uniform vertex conditions tested on the seven-label (R7) SAT witnesses (LAB, 20/10/2026, NOTE_BORNE_RANG).

For a vertex v of a srg(v, k, 1, 2) with eigenvalues r > s, the 84 (in general k(k-2)/2) non-neighbours are labels
{p, q} (two neighbours of v on different lines).  Let P be the projector on the s-eigenspace and X a set of labels.
Necessary at EVERY 7-rank (proved, NOTE_BORNE_RANG section 2 and 5):
  (R) H := (r-s) P_v[X, X], P_v = P_22 - P_2N P_NN^+ P_N2 (Schur complement on N[v]), is positive semidefinite with
      eigenvalues in [0, r - s] and real rank <= g - k  (30 for Conway);
  (M) for Conway (p = 7): Sigma[X, X] = A_22 - 3I - 2J + 3 Inc + Par (mod 7) has 7-rank <= r_7 - 15 <= 28.
H depends only on the labels and on A_22[X, X].  This script
  * validates the label formula on a REAL srg(243,22,1,2) (full Schur complement computed from the whole graph vs the
    local label formula; eigenvalues; rank), and
  * evaluates (R) and (M) on the R7 witnesses (four exact stars + 7 labels {4,t}, 51 labels, found by SAT without any
    spectral constraint).
usage: python vertex_block_test.py validate <srg243.edges>
       python vertex_block_test.py witness <r7_seed.json> ...
"""
import itertools
import json
import sys

import numpy as np


def rank_mod(M, p):
    M = (np.array(M, dtype=np.int64) % p).copy()
    rows, cols = M.shape
    r = 0
    for c in range(cols):
        if r == rows:
            break
        piv = np.nonzero(M[r:, c])[0]
        if len(piv) == 0:
            continue
        i = r + piv[0]
        M[[r, i]] = M[[i, r]]
        M[r] = (M[r] * pow(int(M[r, c]), p - 2, p)) % p
        nz = np.nonzero(M[:, c])[0]
        nz = nz[nz != r]
        if len(nz):
            M[nz] = (M[nz] - np.outer(M[nz, c], M[r])) % p
        r += 1
    return r


def eig_params(k):
    d = int(round((4 * k - 7) ** 0.5))
    assert d * d == 4 * k - 7
    r, s = (-1 + d) // 2, (-1 - d) // 2
    return r, s


def proj_coeffs(k, r, s, n):
    """P_s = (A - rI)(A - kI) / ((s - r)(s - k)) = a I + b A + c J for a srg(n, k, 1, 2)"""
    # A^2 = (k - 2) I - A + 2 J
    den = (s - r) * (s - k)
    a = ((k - 2) + r * k) / den
    b = (-1 - r - k) / den
    c = 2 / den
    return a, b, c


def local_H(labels, mate, A22, k):
    """(r-s) * Schur complement of P on the labels, from local data only (labels, mates, A22 on the labels)"""
    r, s = eig_params(k)
    n = 1 + k + k * (k - 2) // 2
    a, b, c = proj_coeffs(k, r, s, n)
    t = r - s
    m = len(labels)
    # N[v]: index 0 = v, 1..k = the neighbours 0..k-1
    PNN = np.zeros((k + 1, k + 1))
    for i in range(k + 1):
        for j in range(k + 1):
            adj = 0
            if i != j:
                if i == 0 or j == 0:
                    adj = 1
                elif mate(i - 1) == j - 1:
                    adj = 1
            PNN[i, j] = a * (i == j) + b * adj + c
    P2N = np.zeros((m, k + 1))
    for x, (p, q) in enumerate(labels):
        P2N[x, 0] = c
        for y in range(k):
            P2N[x, 1 + y] = b * (y in (p, q)) + c
    P22 = a * np.eye(m) + b * A22 + c * np.ones((m, m))
    S = P22 - P2N @ np.linalg.pinv(PNN) @ P2N.T
    return t * S, t


def sigma_mod7(labels, mate, A22):
    m = len(labels)
    inc = np.zeros((m, m), dtype=np.int64)
    par = np.zeros((m, m), dtype=np.int64)
    for i, (p, q) in enumerate(labels):
        for j, (s, u) in enumerate(labels):
            inc[i, j] = len({p, q} & {s, u})
            par[i, j] = len({s, u} & {mate(p), mate(q)})
    return (A22 - 3 * np.eye(m, dtype=np.int64) - 2 + 3 * inc + par) % 7


def validate(path):
    edges = [tuple(map(int, l.split()[:2])) for l in open(path) if l.strip()]
    n = 1 + max(max(e) for e in edges)
    A = np.zeros((n, n))
    for x, y in edges:
        A[x, y] = A[y, x] = 1
    k = int(A[0].sum())
    r, s = eig_params(k)
    a, b, c = proj_coeffs(k, r, s, n)
    P = a * np.eye(n) + b * A + c * np.ones((n, n))
    assert np.allclose(P @ P, P)
    v = 0
    nb = [int(x) for x in np.nonzero(A[v])[0]]
    # mates = lines through v
    idx = {u: i for i, u in enumerate(nb)}
    mate_tab = {}
    for u in nb:
        w = [x for x in nb if A[u, x]]
        assert len(w) == 1
        mate_tab[idx[u]] = idx[w[0]]
    mate = lambda i: mate_tab[i]
    far = [w for w in range(n) if w != v and not A[v, w]]
    labels = []
    for w in far:
        pq = sorted(idx[u] for u in nb if A[w, u])
        assert len(pq) == 2 and mate(pq[0]) != pq[1]
        labels.append(tuple(pq))
    B = [v] + nb
    PNN = P[np.ix_(B, B)]
    true_S = (r - s) * (P[np.ix_(far, far)] - P[np.ix_(far, B)] @ np.linalg.pinv(PNN) @ P[np.ix_(B, far)])
    A22 = A[np.ix_(far, far)]
    H, t = local_H(labels, mate, A22, k)
    ev = np.linalg.eigvalsh(H)
    print("validate %s: k=%d r=%d s=%d |labels|=%d  max|H - true| = %.2e  eigen min %.3e max %.6f  rank %d (expected g-k)"
          % (path.split('/')[-1], k, r, s, len(labels), np.abs(H - true_S).max(), ev.min(), ev.max(),
             int((ev > 1e-6).sum())))


def witness(path):
    d = json.load(open(path))
    k = d["K"]
    mate = lambda i: i ^ 1
    labels = [tuple(l) for l in d["labels"]]
    m = len(labels)
    A22 = np.zeros((m, m))
    for i, j in d["edges"]:
        A22[i, j] = A22[j, i] = 1
    H, t = local_H(labels, mate, A22, k)
    ev = np.linalg.eigvalsh(H)
    neg = int((ev < -1e-9).sum())
    above = int((ev > t + 1e-9).sum())
    rk = int((np.abs(ev) > 1e-9).sum())
    Sig = sigma_mod7(labels, mate, A22.astype(np.int64))
    r7 = rank_mod(Sig, 7)
    # the four exact stars alone (labels meeting {0,1,2,3}) = first block
    base = [i for i, l in enumerate(labels) if set(l) & {0, 1, 2, 3}]
    Hb = H[np.ix_(base, base)]
    evb = np.linalg.eigvalsh(Hb)
    r7b = rank_mod(Sig[np.ix_(base, base)], 7)
    print("%s: %d labels | real block: eigen min %.3f max %.3f, #neg %d, #>%d %d, rank %d (must be <= 30, PSD, <= %d) |"
          " 7-rank %d (must be <= 28) || base %d labels: eigen min %.3f, #neg %d, rank %d, 7-rank %d"
          % (path.replace("\\", "/").split("/")[-1], m, ev.min(), ev.max(), neg, t, above, rk, t, r7,
             len(base), evb.min(), int((evb < -1e-9).sum()), int((np.abs(evb) > 1e-9).sum()), r7b))


if __name__ == "__main__":
    if sys.argv[1] == "validate":
        validate(sys.argv[2])
    else:
        for f in sys.argv[2:]:
            witness(f)
