"""Integer filters on the rectangle vectors h_Q = T 1_Q of a four-star block (LAB, 18/10/2026; idea relayed by Codex).

In Conway, for every rectangle Q at the root v, h_Q = T 1_Q (labels; 0 on v and on the letters) is an integral
eigenvector of A for -4 with ||h_Q||^2 = 7 R_QQ = 7 (8 - 2 e(Q)): norm 28, 42, 56 for e(Q) = 2, 1, 0.  The visible
coordinates (the 44 labels of S) are known from the block, so these PROVED bounds can be checked on them:
  single  (Codex section 18):     m^2 + 7|m| <= N for every coordinate m;
  pair    (Codex 17b4198 = ChatGPT note Th. 4.1): two coordinates of the same sign a, b > 0 at u != w need
          N >= a^2 + b^2 + 9(a+b) - 2 if u ~ w, a^2 + b^2 + 7(a+b) - 4 if not, plus 2 for each common neighbour of
          u and w whose coordinate is known to be 0 (shared letters, and visible labels with h = 0);
  integral 8 T 1_Q must be divisible by 8 on S.
Visible rectangles: Q_0j (j = 1..6) and Q_1j (j = 2..6); e(Q) = 3 is E3 and e(Q) = 4 gives h_Q = 0.
usage: python c1_hq_pairs.py <distinct_cache.jsonl> [walk .json files ...]"""
import ctypes
import itertools
import json
import os
import sys
from collections import Counter
from fractions import Fraction

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "stars_rank_2026-10-14"))
from stars_rank import kval  # noqa: E402
from gg_test import orient, line_graph, components  # noqa: E402
from c1_cutfilter import tests  # noqa: E402


def rect(i, j):
    return [frozenset((a, b)) for a in (2 * i, 2 * i + 1) for b in (2 * j, 2 * j + 1)]


VISIBLE = [(0, j) for j in range(1, 7)] + [(1, j) for j in range(2, 7)]


def analyse(L, E):
    """returns Counter of violated filters over the visible rectangles of the oriented block (L, E)."""
    S = list(L)
    idx = {s: k for k, s in enumerate(S)}
    adj = [[frozenset((a, b)) in E for b in S] for a in S]
    T8 = [[(24 if i == j else 0) - (8 if adj[i][j] else 0) - int(round(8 * kval(S[i], S[j]))) for j in range(44)]
          for i in range(44)]
    out = Counter()
    for (i, j) in VISIBLE:
        Q = rect(i, j)
        q = [idx[s] for s in Q]
        e = sum(1 for a, b in itertools.combinations(q, 2) if adj[a][b])
        if e >= 3:
            continue
        N = 7 * (8 - 2 * e)
        h8 = [sum(T8[r][c] for c in q) for r in range(44)]
        if any(x % 8 for x in h8):
            out["non-integral"] += 1
            continue
        h = [x // 8 for x in h8]
        if any(m * m + 7 * abs(m) > N for m in h):
            out["single"] += 1
        bad = False
        for u, w in itertools.combinations(range(44), 2):
            a, b = h[u], h[w]
            if a * b <= 0:
                continue
            a, b = abs(a), abs(b)
            if adj[u][w]:
                bound = a * a + b * b + 9 * (a + b) - 2
            else:
                bound = a * a + b * b + 7 * (a + b) - 4
            zeros = len(S[u] & S[w])                                     # shared letter: h = 0 there
            zeros += sum(1 for z in range(44) if z not in (u, w) and adj[u][z] and adj[w][z] and h[z] == 0)
            if bound + 2 * zeros > N:
                bad = True
                break
        if bad:
            out["pair"] += 1
    return out


def load_walk(fn):
    d = json.load(open(fn))
    lab = [frozenset(x) for x in d["labels"]]
    edges = []
    for a, b in d["edges"]:
        edges.append((sorted(lab[a]), sorted(lab[b])) if isinstance(a, int) else (a, b))
    return [sorted(x) for x in lab], edges


def main():
    try:
        ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x40)
    except Exception:
        pass
    agg = Counter()
    for line in open(sys.argv[1]):
        d = json.loads(line)
        if len(d["labels"]) != 44:
            continue
        S = [frozenset(x) for x in d["labels"]]
        E0 = set(frozenset((frozenset(a), frozenset(b))) for a, b in d["edges"])
        G = np.zeros((44, 44))
        for i, j in itertools.combinations(range(44), 2):
            if frozenset((S[i], S[j])) in E0:
                G[i, j] = G[j, i] = 1
        T = 3 * np.eye(44) - G - np.array([[kval(a, b) for b in S] for a in S])
        psd = bool(np.linalg.eigvalsh(T)[0] >= -1e-9)
        for side in (0, 1):
            L, EE = orient(S, d["edges"], side)
            V, pos, A = line_graph(L, EE)
            if not all(sum(r) == 3 for r in A) or components(A) != 1:
                continue
            out, _ = tests(L, EE)
            o = analyse(L, EE)
            key = "PSD" if psd else "nonPSD"
            agg[key + " sides"] += 1
            agg[key + " killed (single/pair)"] += (o["single"] + o["pair"]) > 0
            agg[key + " killed, free of E3v_l and C2a"] += (o["single"] + o["pair"]) > 0 and not out
            agg[key + " free of E3v_l and C2a"] += not out
            agg[key + " non-integral h_Q"] += o["non-integral"] > 0
    print(dict(agg))
    for fn in sys.argv[2:]:
        labels, edges = load_walk(fn)
        L, EE = orient([frozenset(x) for x in labels], edges, 0)
        print("walk %-36s %s" % (os.path.basename(fn), dict(analyse(L, EE)) or "no violation"))


if __name__ == "__main__":
    main()
