"""For every distinct broken (star matchings not h-related) T, U PSD structure on file with nullity >= 11:
nu = nu(A) + nu(C) + n_1(K) with A, C the h-even / h-odd compressions of T, D the off-diagonal block,
K = A^{+1/2} D C^{+1/2} (T's contraction), K' = A'^{+1/2} D C'^{+1/2} (U's contraction, sign irrelevant).
Prints the distribution of (nu, nu(A), nu(C), n_1(K), rank D, ||K'|| rounded).  usage: python broken_profile.py <glob> [...]"""
import glob, json, sys
from collections import Counter
import numpy as np
sys.path.insert(0, '.')
from stars_rank import kval, LABELS
D84 = np.zeros((14, 84))
for j, l in enumerate(LABELS):
    for y in l: D84[y, j] = 1
Pi = np.eye(84) - D84.T @ np.linalg.inv(D84 @ D84.T) @ D84
pos = {l: i for i, l in enumerate(LABELS)}
hm = {0: 1, 1: 0, 2: 3, 3: 2}
files = []
for g in sys.argv[1:]: files += sorted(glob.glob(g))
def psqrt(M, inv=False):
    w, V = np.linalg.eigh((M + M.T) / 2); keep = w > 1e-9
    d = np.zeros_like(w); d[keep] = (1 / np.sqrt(w[keep])) if inv else np.sqrt(w[keep])
    return (V * d) @ V.T
seen = set(); cnt = Counter(); ex = {}
for f in files:
    try: d = json.load(open(f))
    except Exception: continue
    if not isinstance(d, dict) or "edges" not in d or len(d.get("labels", [])) != 44: continue
    S = [frozenset(l) for l in d["labels"]]; n = 44; idx = {s: i for i, s in enumerate(S)}
    key = frozenset(frozenset((S[a], S[b])) for a, b in d["edges"])
    if key in seen: continue
    seen.add(key)
    G = np.zeros((n, n))
    for a, b in d["edges"]: G[a, b] = G[b, a] = 1
    hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
    sl = [(i, j) for i in range(n) for j in range(i + 1, n) if S[i] & S[j] & {0, 1, 2, 3}]
    if all(G[i, j] == G[hp[i], hp[j]] for (i, j) in sl): continue
    K = np.array([[kval(a, b) for b in S] for a in S]); T = 3 * np.eye(n) - G - K
    w, V = np.linalg.eigh(T); nu = int(np.sum(np.abs(w) < 1e-7))
    if nu < 11: continue
    Z = np.array([[1.0 if y in s_ else 0.0 for s_ in S] for y in (0, 1, 2, 3)]).T
    Q, _ = np.linalg.qr(Z); P = np.eye(n) - Q @ Q.T
    if np.linalg.eigvalsh(P @ T @ P + 50 * Q @ Q.T)[0] < -1e-9: continue
    Us = 7 * Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])] - T
    if np.linalg.eigvalsh(P @ Us @ P + 50 * Q @ Q.T)[0] < -1e-9: continue
    H = np.zeros((n, n))
    for i, j in enumerate(hp): H[j, i] = 1
    U1, s1, _ = np.linalg.svd((np.eye(n) + H) / 2); Be = U1[:, s1 > 0.5]
    U2, s2, _ = np.linalg.svd((np.eye(n) - H) / 2); Bo = U2[:, s2 > 0.5]
    A = Be.T @ T @ Be; C = Bo.T @ T @ Bo; Dm = Be.T @ T @ Bo
    Ap = Be.T @ Us @ Be; Cp = Bo.T @ Us @ Bo; Dp = Be.T @ Us @ Bo
    nA = int(np.sum(np.abs(np.linalg.eigvalsh(A)) < 1e-7)); nC = int(np.sum(np.abs(np.linalg.eigvalsh(C)) < 1e-7))
    Kc = psqrt(A, True) @ Dm @ psqrt(C, True); sv = np.linalg.svd(Kc, compute_uv=False)
    n1 = int(np.sum(sv > 1 - 1e-6))
    Kp = psqrt(Ap, True) @ Dp @ psqrt(Cp, True); svp = np.linalg.svd(Kp, compute_uv=False)
    rD = int(np.sum(np.linalg.svd(Dm, compute_uv=False) > 1e-7))
    k = (nu, nA, nC, n1, rD, round(float(svp[0]), 2))
    cnt[k] += 1; ex.setdefault(k, f)
print("(nu, nu(A), nu(C), n1(K), rank D, ||K'||): count, example")
for k in sorted(cnt): print(" ", k, cnt[k], ex[k])
