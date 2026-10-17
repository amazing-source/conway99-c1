"""Per-column deficits delta_a = 8/3 - z_a^T R z_a (>= 0 on positive blocks, = 0 for all a in Conway) and
local features of the column: e of the l- and m-rectangles of its line, number of Gamma-edges inside the column,
deep attachments sum(n_a), whether the line's 8 labels P_j are closed."""
import itertools, json, sys
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, k8, relabel, gl_connected
IDX = {l: i for i, l in enumerate(S)}
K8 = np.array([[k8(a, b) for b in S] for a in S], dtype=float)
done = 0; feat = defaultdict(list); zero_cols = Counter(); allrows = []
for line in open(sys.argv[1]):
    d = json.loads(line)
    if len(d["labels"]) != 44:
        continue
    S0 = [frozenset(x) for x in d["labels"]]
    E0 = [(frozenset(a), frozenset(b)) for a, b in d["edges"]]
    for side in (0, 1):
        L, EE = relabel(S0, E0, side)
        conn, degok = gl_connected(EE)
        if not (conn and degok):
            continue
        G = np.zeros((44, 44))
        for i, j in itertools.combinations(range(44), 2):
            if frozenset((S[i], S[j])) in EE:
                G[i, j] = G[j, i] = 1
        T = 3 * np.eye(44) - G - K8 / 8
        if np.linalg.eigvalsh(T)[0] < -1e-9:
            continue
        X = 3 * np.eye(44) - G
        if np.min(np.abs(np.linalg.eigvalsh(X))) < 1e-9:
            continue
        R = np.linalg.inv(X)
        nz = 0
        row = []
        for a in range(4, 14):
            col = [IDX[frozenset((r, a))] for r in range(4)]
            za = np.zeros(44); za[col] = 1
            da = 8 / 3 - za @ R @ za
            b = a ^ 1
            Ql = [IDX[frozenset((r, t))] for r in (0, 1) for t in (a, b)]
            Qm = [IDX[frozenset((r, t))] for r in (2, 3) for t in (a, b)]
            el = int(G[np.ix_(Ql, Ql)].sum() / 2); em = int(G[np.ix_(Qm, Qm)].sum() / 2)
            ecol = int(G[np.ix_(col, col)].sum() / 2)
            # deep attachments of column a: count_needed(s,a) - |N(s) cap col|
            cn = np.array([2 - (a in s) - (b in s) for s in S])
            na = cn - G[:, col].sum(1)
            feat[(el, em, ecol)].append(da)
            row.append(round(da, 4))
            if da < 1e-7:
                nz += 1
        zero_cols[nz] += 1
        allrows.append(row)
        done += 1
    if done >= int(sys.argv[2]):
        break
print("positive c=1 sides:", done)
print("number of outer columns with delta_a = 0 (letter e_a extends) per side:", dict(sorted(zero_cols.items())))
print("delta_a by (e(l-rect), e(m-rect), edges inside column): count, min, median, max")
for k in sorted(feat):
    v = feat[k]
    print("   ", k, len(v), "%.4f %.4f %.4f" % (min(v), np.median(v), max(v)))
print("max_a delta_a per side: min %.4f" % min(max(r) for r in allrows))
print("sample rows:", allrows[:3])
