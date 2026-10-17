"""Every PSD four-star side with c(l) = 1 in our data, against the EXACT integral lemmas only (exploration, LAB 17/10/2026).
No rank, no solver.  For each block (44 labels) with T_S >= 0 and each orientation with c(l) = 1, in this order:
  E3  a rectangle Q_0j at the root l has exactly 3 internal edges (Codex's lemma: impossible);
  C2a the rectangle multigraph M_0 has a 2-cut of a forbidden type (two mu-edges of one star, or two sigma-edges whose
      ends share a letter): 2-cut lemma, aligned version;
  RL  a vector c in {-1,0,1}^11 on the 11 visible rectangles (roots l and m) with c^t R c = 2 gives h = T P c of norm 14
      (co-Heawood, Codex's lemma) whose visible part breaks a co-Heawood rule (c1_rlattice.py);
  C2b a balanced set C of G_l (|C n X_p| = q even) with exactly 2 boundary edges, both in one group (then the two inner
      ends share the point p of l, which is off the support of y = (A - 3I)(1_C - (q/12) 1_{G_l})): co-Heawood forbids it),
      or both between the same two groups with inner ends sharing a neighbour off the support (2-cut lemma, line view).
Output: counts per first killing lemma, and the list of survivors (if any).
usage: python c1_exact_kill.py <distinct cache.jsonl>"""
import itertools
import json
import sys
from collections import Counter

import numpy as np

sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else ".")
sys.path.insert(0, __file__.rsplit("\\", 2)[0] + "\\stars_rank_2026-10-14" if "\\" in __file__ else "../stars_rank_2026-10-14")
from stars_rank import kval  # noqa: E402
from gg_test import orient, line_graph, components, group  # noqa: E402
from c1_cutfilter import tests  # noqa: E402
import c1_rlattice as RL  # noqa: E402
from c1_balcut import min_bal_cut  # noqa: E402


def c2b_kills(V, A, forbid_rounds=6):
    """search balanced even 2-cuts; True if one of a forbidden type is found (first ones found by CP-SAT)."""
    A = np.array(A)
    tried = []
    for _ in range(forbid_rounds):
        b = min_bal_cut(V, A.tolist(), forbid=tried)
        if b is None or b[0] != 2:
            return False
        _, q, C = b
        tried.append(C)
        cut = [(i, j) for i in range(36) for j in range(36) if A[i, j] and (i in C) and (j not in C)]
        inner = [i for i, j in cut]
        outer = [j for i, j in cut]
        for ends in (inner, outer):
            if group(V[ends[0]]) == group(V[ends[1]]):
                return True                     # common neighbour = the point of l of that group
            common = [w for w in range(36) if A[ends[0], w] and A[ends[1], w]]
            if any(w not in inner + outer for w in common):
                return True                     # a common neighbour of two same-sign ends with y = 0 inside G_l
    return False


def main():
    agg = Counter()
    surv = []
    total = 0
    for line in open(sys.argv[1]):
        d = json.loads(line)
        if len(d["labels"]) != 44:
            continue
        S = [frozenset(x) for x in d["labels"]]
        E = set(frozenset((frozenset(a), frozenset(b))) for a, b in d["edges"])
        n = 44
        G = np.zeros((n, n))
        for i, j in itertools.combinations(range(n), 2):
            if frozenset((S[i], S[j])) in E:
                G[i, j] = G[j, i] = 1
        T = 3 * np.eye(n) - G - np.array([[kval(a, b) for b in S] for a in S])
        if np.linalg.eigvalsh(T)[0] < -1e-9:
            continue
        for side in (0, 1):
            L, EE = orient(S, d["edges"], side)
            V, pos, A = line_graph(L, EE)
            if not all(sum(r) == 3 for r in A) or components(A) != 1:
                continue
            total += 1
            out, _ = tests(L, EE)
            if "E3" in out:
                agg["E3"] += 1
                continue
            if "LD" in out:
                agg["C2a"] += 1
                continue
            o = RL.analyse(L, EE)
            if any(k.startswith("killed") for k in o):
                agg["RL"] += 1
                continue
            if c2b_kills(V, A):
                agg["C2b"] += 1
                continue
            agg["survivor"] += 1
            surv.append((d["src"], side))
    print("PSD four-star sides with c(l) = 1: %d" % total)
    print("first killing lemma:", dict(agg))
    for s in surv:
        print("  survivor:", s)


if __name__ == "__main__":
    main()
