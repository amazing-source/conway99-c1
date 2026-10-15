"""Saturation frontier over a corpus (LAB 15/10/2026, mechanism A, question (ii)).
For every structure file (labels + edges): nu = nullity T, N+ = nullity of the h-even block A, N- = nullity of the
h-odd block C, s = nu - N+ - N- (saturated directions; s = rank(Delta | ker T) when T >= 0), whether the star matchings
are broken (either half), T >= 0, U >= 0 (numerical, complement of the star vectors).  Distinct structures only
(edge-set hash).  Prints, for broken structures, the frontier max(N+ + 2s), max nu per (PSD class, s), and the list of
(N+, s) pairs that occur.
usage: python sat_frontier.py <dir or json> [...]   (directories are searched recursively)"""
import glob, json, os, sys
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')
from stars_rank import kval, LABELS
hm = {0: 1, 1: 0, 2: 3, 3: 2}
D84 = np.zeros((14, 84))
for j, l in enumerate(LABELS):
    for y in l:
        D84[y, j] = 1
Pi = np.eye(84) - D84.T @ np.linalg.inv(D84 @ D84.T) @ D84
pos = {l: i for i, l in enumerate(LABELS)}
files = []
for a in sys.argv[1:]:
    files += (sorted(glob.glob(os.path.join(a, "*.json"))) if os.environ.get("FLAT") else sorted(glob.glob(os.path.join(a, "**", "*.json"), recursive=True))) if os.path.isdir(a) else [a]
seen = set(); rows = []
Kcache = {}
for f in files:
    try:
        d = json.load(open(f))
    except Exception:
        continue
    if not isinstance(d, dict) or "edges" not in d or "labels" not in d or len(d["labels"]) != 44:
        continue
    S = [frozenset(l) for l in d["labels"]]
    key = frozenset(frozenset((S[a], S[b])) for a, b in d["edges"])
    if key in seen:
        continue
    seen.add(key)
    n = 44; idx = {s: i for i, s in enumerate(S)}
    G = np.zeros((n, n))
    for a, b in d["edges"]:
        G[a, b] = G[b, a] = 1
    sk = tuple(sorted(tuple(sorted(s)) for s in S))
    K = np.array([[kval(a, b) for b in S] for a in S])
    T = 3 * np.eye(n) - G - K
    hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
    reps = [i for i in range(n) if (0 in S[i]) or (2 in S[i] and not (S[i] & {0, 1}))]
    Ep = np.zeros((n, 22)); Em = np.zeros((n, 22))
    for k, r in enumerate(reps):
        Ep[r, k] = Ep[hp[r], k] = 1 / np.sqrt(2)
        Em[r, k] = 1 / np.sqrt(2); Em[hp[r], k] = -1 / np.sqrt(2)
    nu = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-7))
    Np = int(np.sum(np.abs(np.linalg.eigvalsh(Ep.T @ T @ Ep)) < 1e-7))
    Nm = int(np.sum(np.abs(np.linalg.eigvalsh(Em.T @ T @ Em)) < 1e-7))
    Z = np.array([[1.0 if y in s_ else 0.0 for s_ in S] for y in (0, 1, 2, 3)]).T
    Q, _ = np.linalg.qr(Z); P = np.eye(n) - Q @ Q.T
    tpsd = np.linalg.eigvalsh(P @ T @ P + 50 * Q @ Q.T)[0] > -1e-7
    U = 7 * Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])] - T
    upsd = np.linalg.eigvalsh(P @ U @ P + 50 * Q @ Q.T)[0] > -1e-7
    broken = False
    for a0, a1 in ((0, 1), (2, 3)):
        M = {}
        for a in (a0, a1):
            pr = set()
            for i in range(n):
                if a in S[i]:
                    for j in range(n):
                        if j > i and a in S[j] and G[i, j]:
                            y = [t for t in S[i] if t != a][0]; z = [t for t in S[j] if t != a][0]
                            pr.add(frozenset((hm.get(y, y), hm.get(z, z)) if a == a1 else (y, z)))
            M[a] = pr
        if M[a0] != M[a1]:
            broken = True
    rows.append((f, nu, Np, Nm, nu - Np - Nm, broken, bool(tpsd), bool(upsd)))
print("distinct structures: %d" % len(rows))
for cls, sel in (("T,U PSD", lambda r: r[6] and r[7]), ("T PSD, U not", lambda r: r[6] and not r[7]),
                 ("T not PSD", lambda r: not r[6])):
    br = [r for r in rows if r[5] and sel(r)]
    ok = [r for r in rows if not r[5] and sel(r)]
    print("== %s: broken %d, h-related %d" % (cls, len(br), len(ok)))
    if br:
        c = Counter((r[2], r[3], r[4], r[1]) for r in br)
        print("   broken (N+, N-, s, nu): count, sorted by nu then N+ + 2s")
        for k, v in sorted(c.items(), key=lambda kv: (-kv[0][3], -(kv[0][0] + 2 * kv[0][2]))):
            print("     ", k, v, " N+ + 2s = %d" % (k[0] + 2 * k[2]))
    if ok:
        c = Counter((r[2], r[3], r[4], r[1]) for r in ok)
        print("   h-related, top nullities:", sorted(c.items(), key=lambda kv: -kv[0][3])[:6])
