"""Exhaustive DFS (notes/131 sec. 6): does a cross block Sigma exist for two full-pivot blocks c, d forming a sib pair?
Sigma: 10x10 over the labels R of the 5 other blocks, entries 0/+-1, exactly two +1 and two -1 in every row and column.
Necessary conditions (c full pivot => g- = 20, R_c = K r K^T of rank 2 with r anisotropic; T = 0 on star(d)):
  (mod 7)  M_D = I - J + 2P_pi + Rm^T (5I + 4P_pi) Rm has rank <= 2, Rm = Sigma + 2(I - P_pi); and M_D = -K_D r K_D^T with r
           anisotropic, so (M_D)_yy = 0 forces row y of M_D to vanish;
  (real)   G_D = (11I - J + P_pi - W_D^T M_c^+ W_D)/4 is PSD of rank <= 4 (principal block of 7 P_4);
  and the same for d (Sigma transposed).
Columns are chosen one by one; every condition is checked on the leading principal block (it only involves chosen columns).
Symmetry: none used (plain exhaustive), so the count of leaves is an honest upper bound."""
import itertools, sys, time
import numpy as np

P = 7
n = 10
Ppi = np.zeros((n, n), int)
for i in range(n):
    Ppi[i, i ^ 1] = 1
I = np.eye(n, dtype=int)
A0 = (I - np.ones((n, n), int) + 2 * Ppi) % P
Wm = (5 * I + 4 * Ppi) % P
N12 = 12
P12 = np.zeros((N12, N12))
for i in range(N12):
    P12[i, i ^ 1] = 1
Mcp = np.linalg.pinv(11 * np.eye(N12) + P12 - np.ones((N12, N12)))
BASE = (11 * np.eye(n) - np.ones((n, n)) + Ppi.astype(float))

cols = []
for plus in itertools.combinations(range(n), 2):
    rest = [i for i in range(n) if i not in plus]
    for minus in itertools.combinations(rest, 2):
        v = np.zeros(n, int)
        v[list(plus)] = 1
        v[list(minus)] = -1
        cols.append(v)
print('column options', len(cols))


def rm_col(v, y):
    r = v.copy()
    r[y] += 2
    r[y ^ 1] -= 2
    return r


def w_col(v, y):
    w = np.zeros(N12)
    w[0], w[1] = 1, -1
    w[2:] = 4 * v
    w[2 + y] += 1
    w[2 + (y ^ 1)] -= 1
    return w


def rank_mod(M):
    M = [[int(x) % P for x in r] for r in M]
    rows, colsn = len(M), len(M[0]) if M else 0
    r = 0
    for c in range(colsn):
        piv = next((i for i in range(r, rows) if M[i][c]), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], P - 2, P)
        M[r] = [x * inv % P for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [(a - f * b) % P for a, b in zip(M[i], M[r])]
        r += 1
    return r


t0 = time.time()
tlim = float(sys.argv[1]) if len(sys.argv) > 1 else 280
nodes = [0]
found = []
stats = {}


def ok_partial(chosen):
    k = len(chosen)
    ys = list(range(k))
    R = np.array([rm_col(v, y) for y, v in enumerate(chosen)]).T          # 10 x k
    MD = (A0[:k, :k] + R.T @ Wm @ R) % P
    if rank_mod(MD.tolist()) > 2:
        return 'rank7'
    for y in ys:
        if MD[y, y] == 0 and any(MD[y, :]):
            return 'aniso'
    Wd = np.array([w_col(v, y) for y, v in enumerate(chosen)]).T          # 12 x k
    G = (BASE[:k, :k] - Wd.T @ Mcp @ Wd) / 4
    ev = np.linalg.eigvalsh(G)
    if ev.min() < -1e-7:
        return 'psd'
    if (ev > 1e-7).sum() > 4:
        return 'rank4'
    return None


def rows_ok(chosen):
    k = len(chosen)
    S = np.array(chosen).T              # 10 x k
    for i in range(n):
        p = int((S[i] == 1).sum())
        m = int((S[i] == -1).sum())
        if p > 2 or m > 2:
            return False
        if (2 - p) + (2 - m) > n - k:
            return False
    return True


def dfs(chosen):
    if time.time() - t0 > tlim:
        return
    nodes[0] += 1
    k = len(chosen)
    if k == n:
        S = np.array(chosen).T
        # condition at d: the same with Sigma transposed
        if ok_full(S.T):
            found.append(S.copy())
        return
    for v in cols:
        c2 = chosen + [v]
        if not rows_ok(c2):
            continue
        why = ok_partial(c2)
        stats[why] = stats.get(why, 0) + 1
        if why is None:
            dfs(c2)


def ok_full(S):
    return ok_partial([S[:, y] for y in range(n)]) is None


dfs([])
print('nodes', nodes[0], 'prune stats', stats, 'found', len(found), '(%.0fs)' % (time.time() - t0),
      'COMPLETE' if time.time() - t0 <= tlim else 'TIME LIMIT (incomplete)')
for S in found[:3]:
    print(S)
