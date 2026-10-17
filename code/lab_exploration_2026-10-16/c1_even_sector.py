"""Doubly-even compression of T_S (exploration, LAB 17/10/2026).
Orbits of the formal swaps (0 1) and (2 3) on the 44 labels: {0y,1y} (y outer, 10), {2y,3y} (10), the cross labels
{02,03,12,13} (1), {0,y}? -- labels {0,2},{0,3},{1,2},{1,3} form one orbit; total 21 orbits.  E = normalised orbit
indicators; T_even = E^t T_S E (21 x 21).  T_S >= 0 implies T_even >= 0.  Prints lambda_min of T_even (minus the star
directions) for structures of our data (PSD) and for the best constrained walk structures.
usage: python c1_even_sector.py <structure.json> [...]   (or --cache <distinct cache.jsonl> <max>)"""
import itertools
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "stars_rank_2026-10-14"))
from stars_rank import kval  # noqa: E402

STARS = {0, 1, 2, 3}


def even_min(S, G):
    n = len(S)
    T = 3 * np.eye(n) - G - np.array([[kval(a, b) for b in S] for a in S])
    sw = lambda l: frozenset({0: 1, 1: 0, 2: 3, 3: 2}.get(y, y) for y in l)
    seen, orbs = set(), []
    for l in S:
        if l in seen:
            continue
        o = {l, sw(l)}
        o |= {frozenset({0: 1, 1: 0}.get(y, y) for y in x) for x in list(o)}
        o |= {frozenset({2: 3, 3: 2}.get(y, y) for y in x) for x in list(o)}
        seen |= o
        orbs.append(sorted(o, key=sorted))
    idx = {l: i for i, l in enumerate(S)}
    E = np.zeros((n, len(orbs)))
    for k, o in enumerate(orbs):
        for l in o:
            E[idx[l], k] = 1 / np.sqrt(len(o))
    Te = E.T @ T @ E
    Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in sorted(STARS)]).T
    Ze = E.T @ Z
    Qz, _ = np.linalg.qr(Ze)
    Pp = np.eye(len(orbs)) - Qz @ Qz.T
    ev = np.linalg.eigvalsh(Pp @ Te @ Pp)
    # remove the (near) zero eigenvalues coming from the star directions
    return float(np.sort(ev)[0]), len(orbs), float(np.linalg.eigvalsh(T)[0])


if sys.argv[1] == "--cache":
    cnt = 0
    vals = []
    for line in open(sys.argv[2]):
        d = json.loads(line)
        if len(d["labels"]) != 44:
            continue
        S = [frozenset(x) for x in d["labels"]]
        E = set(frozenset((frozenset(a), frozenset(b))) for a, b in d["edges"])
        G = np.zeros((44, 44))
        for i, j in itertools.combinations(range(44), 2):
            if frozenset((S[i], S[j])) in E:
                G[i, j] = G[j, i] = 1
        em, no, lt = even_min(S, G)
        vals.append((lt > -1e-9, em))
        cnt += 1
        if cnt >= int(sys.argv[3]):
            break
    psd = [v for p, v in vals if p]
    non = [v for p, v in vals if not p]
    print("data: PSD blocks %d, even-sector min over them %.4f ; non-PSD blocks %d with even-sector negative: %d" % (
        len(psd), min(psd) if psd else float("nan"), len(non), sum(1 for v in non if v < -1e-9)))
else:
    for fn in sys.argv[1:]:
        d = json.load(open(fn))
        S = [frozenset(x) for x in d["labels"]]
        G = np.zeros((44, 44))
        for i, j in d["edges"]:
            G[i, j] = G[j, i] = 1
        em, no, lt = even_min(S, G)
        print("%s: orbits %d, lambda_min(T) %.4f, even-sector lambda_min %.4f" % (os.path.basename(fn), no, lt, em))
