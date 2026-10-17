"""Norm-28 rectangle combinations on four-star blocks (LAB, 18/10/2026; continuation of c1_hq_pairs.py).

For c in {-1,0,1}^11 on the 11 visible rectangles at v with c^T R c = 4, h = T P c (0 on v and the letters) is an
integral -4-eigenvector of A of norm 28 in Conway.  The PROVED integer bounds (Codex section 18 and the pair bound,
Codex 17b4198 = ChatGPT note Th. 4.1) give at norm 28, on the visible coordinates (the 44 labels of S):
  (a) |h| <= 2;  (b) at most one +2 and one -2;  (c) no +1 adjacent to a +2, no -1 adjacent to a -2;
  (d) masses: positive (and negative) visible mass <= 14 - [+2 seen] - [-2 seen].
A combination whose visible norm already exceeds 28 is counted apart ("bessel"): that is only a failure of
T_S (7I - T_S) >= 0, i.e. of positivity, not an integer obstruction; "killed_integer" uses combinations with visible
norm <= 28 only.
All vectors c (up to sign) are scanned with numpy.  Same data and orientation as c1_rotated_e3.py.
usage: python c1_h28_combos.py <distinct_cache.jsonl> [walk .json files ...]"""
import ctypes
import itertools
import json
import os
import sys
import time
from collections import Counter

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "stars_rank_2026-10-14"))
from stars_rank import kval  # noqa: E402
from gg_test import orient, line_graph, components  # noqa: E402
from c1_cutfilter import tests  # noqa: E402
from c1_hq_pairs import VISIBLE, rect, load_walk  # noqa: E402

# all c in {-1,0,1}^11 with first nonzero entry +1 (one representative per sign pair)
_all = np.array(list(itertools.product((-1, 0, 1), repeat=11)), dtype=np.int64)
_first = np.array([next((x for x in row if x), 0) for row in _all])
C = _all[_first == 1].T                                           # 11 x 88573
TIME_LIMIT = 270.0


def analyse(L, E):
    S = list(L)
    idx = {s: k for k, s in enumerate(S)}
    A = np.array([[1 if frozenset((a, b)) in E else 0 for b in S] for a in S], dtype=np.int64)
    T8 = 24 * np.eye(44, dtype=np.int64) - 8 * A - np.array([[int(round(8 * kval(a, b))) for b in S] for a in S])
    P = np.zeros((44, 11), dtype=np.int64)
    for k, (i, j) in enumerate(VISIBLE):
        for s in rect(i, j):
            P[idx[s], k] = 1
    H8 = T8 @ P                                                   # 44 x 11, = 8 h_Q
    if (H8 % 8).any():
        return {"non-integral": 1}
    Hq = H8 // 8
    R = P.T @ Hq                                                  # Gram 1_Q^T T 1_Q'
    n = np.einsum("ij,ij->j", R @ C, C)
    sel = C[:, n == 4]
    if sel.shape[1] == 0:
        return {"combos": 0}
    h = Hq @ sel                                                  # 44 x K
    a = (np.abs(h) > 2).any(0)
    p2, m2 = (h == 2), (h == -2)
    b = (p2.sum(0) > 1) | (m2.sum(0) > 1)
    c = ((A @ (h == 1)) * p2).any(0) | ((A @ (h == -1)) * m2).any(0)
    eps = p2.any(0).astype(int) + m2.any(0).astype(int)
    d = (np.where(h > 0, h, 0).sum(0) > 14 - eps) | (np.where(h < 0, -h, 0).sum(0) > 14 - eps)
    bessel = (h * h).sum(0) > 28                                  # visible norm above the exact total norm
    kill = a | b | c | d
    return {"combos": int(sel.shape[1]), "a": int(a.sum()), "b": int(b.sum()), "c": int(c.sum()), "d": int(d.sum()),
            "bessel": int(bessel.sum()), "killed": bool(kill.any()), "killed_integer": bool((kill & ~bessel).any())}


def main():
    try:
        ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x40)
    except Exception:
        pass
    t0 = time.time()
    agg = Counter()
    for line in open(sys.argv[1]):
        if time.time() - t0 > TIME_LIMIT:
            print("TIME GUARD")
            break
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
            V, pos, Ag = line_graph(L, EE)
            if not all(sum(r) == 3 for r in Ag) or components(Ag) != 1:
                continue
            out, _ = tests(L, EE)
            o = analyse(L, EE)
            key = "PSD" if psd else "nonPSD"
            agg[key + " sides"] += 1
            agg[key + " killed"] += bool(o.get("killed"))
            agg[key + " free of E3v_l/C2a"] += not out
            agg[key + " killed & free of E3v_l/C2a"] += bool(o.get("killed")) and not out
            agg[key + " killed_integer (visible norm <= 28)"] += bool(o.get("killed_integer"))
            agg[key + " killed_integer & free of E3v_l/C2a"] += bool(o.get("killed_integer")) and not out
    print("time %.1f s" % (time.time() - t0), dict(agg))
    for fn in sys.argv[2:]:
        labels, edges = load_walk(fn)
        L, EE = orient([frozenset(x) for x in labels], edges, 0)
        print("walk %-36s %s" % (os.path.basename(fn), analyse(L, EE)))


if __name__ == "__main__":
    main()
