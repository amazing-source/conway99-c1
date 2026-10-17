"""Float control of the ChatGPT note of 17/10/2026 (NOTE_CHATGPT_C1_2026-10-17.pdf), sections 2-3 (LAB, 18/10/2026).
On every positive four-star block of the cache and on the 331 rank-30 objects:
  Th. 2.2  ker N in ker B, with N = 3I - Gamma_S, and N has exactly one negative eigenvalue;
  Th. 3.1  D = B N^+ B^T - H <= 0 and rank T_S = 30 - m3 + rank D0 (D0 = outer 10 x 10 block);
  Th. 3.2  H0 + D0 > 0, with H0 = 3I - M - (7/39) J on the 10 outer letters.
N^+ is built from the eigendecomposition with the SAME threshold as m3 (numpy's default pinv cutoff inverts
eigenvalues of size 1e-13 and gives false failures).  Float check, not a proof: the proofs are in the note.
usage: python check_note_chatgpt_1017.py <distinct_cache.jsonl> <rank30_psd_objects json>"""
import ctypes
import json
import os
import sys
from collections import Counter

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "stars_rank_2026-10-14"))
from stars_rank import kval  # noqa: E402

ZERO = 1e-8
M14 = np.zeros((14, 14))
for x in range(14):
    M14[x, x ^ 1] = 1
H = 3 * np.eye(14) - M14 - np.ones((14, 14)) / 3
E = list(range(4, 14))
H0 = 3 * np.eye(10) - M14[np.ix_(E, E)] - (7 / 39) * np.ones((10, 10))


def check(S, G, K):
    T = 3 * np.eye(44) - G - K
    tw = np.linalg.eigvalsh(T)
    if tw[0] < -1e-9:
        return None
    B = np.zeros((14, 44))
    for k, s in enumerate(S):
        for x in s:
            B[x, k] = 1
    w, V = np.linalg.eigh(3 * np.eye(44) - G)
    nz = np.abs(w) > ZERO
    m3 = int((~nz).sum())
    Np = (V[:, nz] / w[nz]) @ V[:, nz].T
    D = B @ Np @ B.T - H
    D0 = D[np.ix_(E, E)]
    rT = int((np.abs(tw) > ZERO).sum())
    rD0 = int((np.abs(np.linalg.eigvalsh(D0)) > 1e-7).sum())
    return dict(m3=m3, rD0=rD0, formula=rT == 30 - m3 + rD0, negN=int((w < -ZERO).sum()),
                kerB=float(np.abs(B @ V[:, ~nz]).max()) if m3 else 0.0, Dmax=float(np.linalg.eigvalsh(D)[-1]),
                H0D0=float(np.linalg.eigvalsh(H0 + D0)[0]))


def main():
    try:
        ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x40)
    except Exception:
        pass
    blocks = []
    for line in open(sys.argv[1]):
        d = json.loads(line)
        if len(d["labels"]) == 44:
            blocks.append(("cache", d["labels"], d["edges"]))
    r30 = json.load(open(sys.argv[2]))
    blocks += [("rank30", r30["labels"], st["edges"]) for st in r30["structures"]]
    agg = Counter()
    m3hist = Counter()
    worst = dict(kerB=0.0, Dmax=-9.0, H0D0=9.0)
    for kind, labels, edges in blocks:
        S = [frozenset(x) for x in labels]
        idx = {s: i for i, s in enumerate(S)}
        G = np.zeros((44, 44))
        for a, b in edges:
            i, j = (a, b) if isinstance(a, int) else (idx[frozenset(a)], idx[frozenset(b)])
            G[i, j] = G[j, i] = 1
        r = check(S, G, np.array([[kval(a, b) for b in S] for a in S]))
        if r is None:
            continue
        agg[kind + " positive"] += 1
        agg[kind + " rank formula"] += r["formula"]
        agg[kind + " N one negative"] += r["negN"] == 1
        m3hist[(kind, r["m3"], r["rD0"])] += 1
        worst["kerB"] = max(worst["kerB"], r["kerB"])
        worst["Dmax"] = max(worst["Dmax"], r["Dmax"])
        worst["H0D0"] = min(worst["H0D0"], r["H0D0"])
    print(dict(agg))
    print("(kind, m3, rank D0) histogram:", dict(sorted(m3hist.items())))
    print("max |B ker N| %.1e ; max eig D %.1e ; min eig (H0 + D0) %.3f" % (worst["kerB"], worst["Dmax"], worst["H0D0"]))


if __name__ == "__main__":
    main()
