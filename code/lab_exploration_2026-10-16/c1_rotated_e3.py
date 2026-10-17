"""Rotated forms of e(Q) != 3 on the c(l) = 1 data (LAB, 17/10/2026 evening, after Codex's rotated boundary lemma).

E3 (Codex, PROVED): at any root a of srg(99,14,1,2), for two lines (a,x1,x2) and (a,y1,y2), the four corners
w(xi,yj) = the common neighbour of xi and yj other than a span a graph with e != 3 edges.  Here E3 is applied at EVERY
vertex a of Omega = {v} u 14 letters u S (the 59 vertices of a four-star block), to every pair of lines through a
lying in Omega whose four corners also lie in Omega (a corner found in Omega is THE corner, by mu = 2).
Codex's rotated boundary lemma (17/10) is the case a in N(l), one line (a, l_a, a') meeting l, the other inside N(l).

Per block side with c(l) = 1 (orientation as in c1_exact_kill.py) it records:
  E3v_l : e = 3 on a rectangle Q_0j at v (what c1_exact_kill.py calls E3; checked against c1_cutfilter.tests);
  E3v_m : e = 3 on a rectangle Q_1j (j >= 2) at v (visible, not used by c1_exact_kill.py);
  ROT   : e = 3 at a root a != v;  CODEX : ROT in Codex's configuration;
  BAD   : a lambda or mu count already broken inside Omega (not expected for admissible blocks).
One process, idle priority, no solver, internal time guard.
usage: py -3 c1_rotated_e3.py <distinct_cache.jsonl> [walk .json files ...]"""
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

TIME_LIMIT = 240.0


def bits(m):
    while m:
        b = m & -m
        yield b.bit_length() - 1
        m ^= b


def omega(L, E):
    """vertex 0 = v, 1 + x = letter x (x = 0..13), 15 + k = label L[k]; neighbourhoods as bit masks."""
    n = 15 + len(L)
    nb = [0] * n

    def link(i, j):
        nb[i] |= 1 << j
        nb[j] |= 1 << i
    for x in range(14):
        link(0, 1 + x)
    for x in range(0, 14, 2):
        link(1 + x, 2 + x)
    idx = {s: 15 + k for k, s in enumerate(L)}
    for s, k in idx.items():
        for x in s:
            link(1 + x, k)
    for e in E:
        s, t = tuple(e)
        link(idx[s], idx[t])
    return n, nb


def rotated_e3(L, E):
    """all rectangles of Omega with known corners and e = 3; kinds as in the module docstring."""
    n, nb = omega(L, E)
    l_pts = {0, 1, 2}                                            # v, letter 0, letter 1
    in_Nl = [False] * n                                          # letters 2..13, labels meeting {0,1}
    in_Y = [False] * n                                           # labels not meeting {0,1}
    for x in range(2, 14):
        in_Nl[1 + x] = True
    for k, s in enumerate(L):
        if s & {0, 1}:
            in_Nl[15 + k] = True
        else:
            in_Y[15 + k] = True
    found = Counter()
    bad = 0
    nvis = 0
    for a in range(n):
        lines = []
        seen = 0
        for x in bits(nb[a]):
            if seen >> x & 1:
                continue
            c = nb[a] & nb[x]
            k = bin(c).count("1")
            if k == 1:
                y = c.bit_length() - 1
                lines.append((x, y))
                seen |= (1 << x) | (1 << y)
            else:
                seen |= 1 << x
                if k >= 2:
                    bad += 1
        for P, Q in itertools.combinations(lines, 2):
            corners = []
            ok = True
            for x in P:
                for y in Q:
                    if nb[x] >> y & 1:
                        bad += 1
                        ok = False
                        break
                    c = nb[x] & nb[y] & ~(1 << a)
                    k = bin(c).count("1")
                    if k != 1:
                        bad += k >= 2
                        ok = False
                        break
                    corners.append(c.bit_length() - 1)
                if not ok:
                    break
            if not ok:
                continue
            if len(set(corners)) < 4:
                bad += 1
                continue
            nvis += 1
            e = sum(1 for i, j in itertools.combinations(corners, 2) if nb[i] >> j & 1)
            if e != 3:
                continue
            if a == 0:
                ks = {(P[0] - 1) // 2, (Q[0] - 1) // 2}          # lines through v: k = letter // 2
                found["E3v_l" if 0 in ks else "E3v_m"] += 1
            else:
                found["ROT"] += 1
                meets = [bool(set(R) & l_pts) for R in (P, Q)]
                inside = [all(in_Nl[u] for u in R) for R in (P, Q)]
                if in_Nl[a] and ((meets[0] and inside[1]) or (meets[1] and inside[0])) \
                        and any(in_Y[w] for w in corners):
                    found["CODEX"] += 1
                kind = "letter" if a <= 14 else ("label_Nl" if in_Nl[a] else "label_Y")
                found["ROT@" + kind] += 1
    return found, bad, nvis


def load_walk(fn):
    d = json.load(open(fn))
    lab = [frozenset(x) for x in d["labels"]]
    edges = []
    for a, b in d["edges"]:
        if isinstance(a, int):
            edges.append((sorted(lab[a]), sorted(lab[b])))
        else:
            edges.append((a, b))
    return [sorted(x) for x in lab], edges


def main():
    try:
        ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x40)  # IDLE
    except Exception:
        pass
    t0 = time.time()
    rows = []
    mismatch = 0
    nblocks = 0
    for line in open(sys.argv[1]):
        if time.time() - t0 > TIME_LIMIT:
            print("TIME GUARD: stopped after %d blocks" % nblocks)
            break
        d = json.loads(line)
        if len(d["labels"]) != 44:
            continue
        nblocks += 1
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
            found, bad, nvis = rotated_e3(L, EE)
            if ("E3" in out) != (found["E3v_l"] > 0):
                mismatch += 1
            rows.append((d["src"], side, psd, "E3" in out, "LD" in out, found, bad, nvis))
    print("blocks read %d, c(l) = 1 sides %d, time %.1f s" % (nblocks, len(rows), time.time() - t0))
    print("CHECK E3 at v on Q_0j against c1_cutfilter.tests: %d mismatches" % mismatch)
    for psd in (True, False):
        R = [r for r in rows if r[2] == psd]
        if not R:
            continue
        free = [r for r in R if not r[3] and not r[4]]
        print("\n%s sides: %d   (E3v_l %d, C2a without E3v_l %d, free of both %d)" % (
            "PSD" if psd else "non-PSD", len(R), sum(r[3] for r in R), sum(1 for r in R if r[4] and not r[3]),
            len(free)))
        for name, X in (("all", R), ("free of E3v_l and C2a", free)):
            c = Counter()
            for r in X:
                f = r[5]
                c["E3v_m"] += f["E3v_m"] > 0
                c["ROT"] += f["ROT"] > 0
                c["CODEX"] += f["CODEX"] > 0
                c["ROT only (no e = 3 at v)"] += f["ROT"] > 0 and f["E3v_l"] == 0 and f["E3v_m"] == 0
                c["any new (E3v_m or ROT)"] += f["E3v_m"] > 0 or f["ROT"] > 0
                c["BAD"] += r[6] > 0
                for k in ("ROT@letter", "ROT@label_Nl", "ROT@label_Y"):
                    c[k] += f[k] > 0
            nv = [r[7] for r in X]
            print("  %-24s n = %4d : %s ; visible rectangles per side %s..%s" % (
                name, len(X), dict(c), min(nv) if nv else "-", max(nv) if nv else "-"))
    for fn in sys.argv[2:]:
        labels, edges = load_walk(fn)
        S = [frozenset(x) for x in labels]
        L, EE = orient(S, edges, 0)
        V, pos, A = line_graph(L, EE)
        c_l = components(A) if all(sum(r) == 3 for r in A) else None
        out, _ = tests(L, EE)
        found, bad, nvis = rotated_e3(L, EE)
        print("walk %-36s c(l) %s  E3v_l %s C2a %s | E3v_m %d ROT %d CODEX %d BAD %d visible %d" % (
            os.path.basename(fn), c_l, "E3" in out, "LD" in out, found["E3v_m"], found["ROT"], found["CODEX"],
            bad, nvis))


if __name__ == "__main__":
    main()
