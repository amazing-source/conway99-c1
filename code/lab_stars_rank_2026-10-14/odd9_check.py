"""ODD9 check (LAB 15/10/2026): rank gain of the m-odd vectors f_y = 1_{2y} - 1_{3y} (y outer) and of the m-even
vectors g_y = 1_{2y} + 1_{3y} beyond X_l (labels meeting the line l = {v,0,1}), exact ranks of 8T Grams; and the same
with l and m exchanged (e_x = 1_{0x} - 1_{1x}).  ODD9 (EVIDENCE only, 15/10 00:45): the odd vectors always add 9.
usage: python odd9_check.py <json> [...]"""
import json
import sys

import numpy as np

from stars_rank import kval
from z5_enum import exact_rank


def gain(M8, base_idx, vecs):
    n = M8.shape[0]
    B = np.zeros((n, len(base_idx) + len(vecs)), dtype=np.int64)
    for k, i in enumerate(base_idx):
        B[i, k] = 1
    for k, v in enumerate(vecs):
        B[:, len(base_idx) + k] = v
    r_all = exact_rank((B.T @ M8 @ B).tolist())
    Bb = B[:, :len(base_idx)]
    r_base = exact_rank((Bb.T @ M8 @ Bb).tolist())
    return r_all - r_base


def _main():
    for f in sys.argv[1:]:
        d = json.load(open(f))
        S = [frozenset(l) for l in d["labels"]]
        n = len(S)
        idx = {s: i for i, s in enumerate(S)}
        G = np.zeros((n, n), dtype=np.int64)
        for i, j in d["edges"]:
            G[i, j] = G[j, i] = 1
        K8 = np.rint(8 * np.array([[kval(a, b) for b in S] for a in S])).astype(np.int64)
        M8 = 24 * np.eye(n, dtype=np.int64) - 8 * G - K8
        out = []
        for (a, a2, b, b2) in ((0, 1, 2, 3), (2, 3, 0, 1)):
            Xl = [i for i in range(n) if S[i] & {a, a2}]
            odd, even = [], []
            for y in range(4, 14):
                v = np.zeros(n, dtype=np.int64)
                w = np.zeros(n, dtype=np.int64)
                v[idx[frozenset((b, y))]] = 1
                v[idx[frozenset((b2, y))]] = -1
                w[idx[frozenset((b, y))]] = 1
                w[idx[frozenset((b2, y))]] = 1
                odd.append(v)
                even.append(w)
            out.append((gain(M8, Xl, odd), gain(M8, Xl, even), gain(M8, Xl, odd + even)))
        print("%s: c %s | beyond X_l: odd %d, even %d, both %d | beyond X_m: odd %d, even %d, both %d"
              % (f, d.get("c"), out[0][0], out[0][1], out[0][2], out[1][0], out[1][1], out[1][2]), flush=True)


if __name__ == "__main__":
    _main()
