"""Minimum-norm z with T_S z = w_C, rounded, printed with the C4-adjacency of each label (which C4 labels it sees).
usage: python c4do_minnorm.py <json>"""
import json, sys
import numpy as np
from fractions import Fraction as F
sys.path.insert(0, '.'); sys.path.insert(0, 'hmatch_tools_2026-10-15/n9ng_attack')
from stars_rank import kval
f = sys.argv[1]
d = json.load(open(f)); S = [frozenset(l) for l in d["labels"]]; n = 44; idx = {s: i for i, s in enumerate(S)}
G = np.zeros((n, n))
for a, b in d["edges"]: G[a, b] = G[b, a] = 1
K = np.array([[kval(a, b) for b in S] for a in S]); T = 3 * np.eye(n) - G - K
C = [idx[frozenset(p)] for p in ((0, 2), (0, 3), (1, 2), (1, 3))]
w = np.zeros(n); w[C] = [1, -1, -1, 1]
z = np.linalg.pinv(T, rcond=1e-10) @ w
print(f, "residual", np.linalg.norm(T @ z - w))
nm = lambda s: "".join(format(c, 'x') for c in sorted(s))
cn = ["02", "03", "12", "13"]
for i in np.argsort(-np.abs(z)):
    if abs(z[i]) < 1e-9: continue
    fr = F(z[i]).limit_denominator(2000)
    print("  %s z=%8s  sees %s" % (nm(S[i]), str(fr), [cn[k] for k in range(4) if G[i, C[k]]]))
