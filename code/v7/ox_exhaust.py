"""Exhaustive enumeration of the x-fiber O_x for a fixed (core, holes), with incremental pruning.

O_x = the 10 outside neighbours of x (6 Bx with q=1, 4 Zx with q=0).  N(x) is a perfect matching, so O_x is the
union of 5 matched pairs: 4 pairs (Bx, Zx) and 1 pair (Bx, Bx); there are no other edges inside O_x
(Zx is independent in the residual; O_x subset N(x) induces exactly the matching).
Seed after k pairs: core (27) + 2k vertices, adjacency fully known.  Tests at every node (all necessary):
  (a) lambda/mu caps on every seed pair (common neighbours inside the seed <= 1 / 2);
  (b) x-fiber label demands: sum_{u in O_x}[l in b_u] <= M[x,l], with equality at the leaf;
  (c) PSD of the q-Gram and of K on the seed;
  (d) residual class minima (seedcvp): no element of the class of q below (40,35,34,37,44) at levels 0..4.
Pairs are generated in canonical (sorted) order to quotient the symmetry between the four (Bx,Zx) pairs.
A (core, holes) with no surviving leaf is EXCLUDED.
"""
import json, sys, itertools, time
import numpy as np
from bstage import gen_columns, target_matrix, pdeg, P13, T
from seedcvp import class_min_violation

LAB = T + P13


def enumerate_ox(core, holes, test_depths=(1, 2, 3, 4, 5), verbose=False, limit=None):
    A = np.array(core["adj"]); M = target_matrix(A)
    cols = gen_columns(A, set(tuple(p) for p in core["defect"]))
    cand = {1: [], 0: []}
    for b, q in cols:
        if b[0] != 0:
            continue
        if sum(1 for v in b if v in P13 and v not in holes) > pdeg(0, q):
            continue
        cand[q].append(tuple(b))
    demand = np.array([int(M[0, l]) if l >= 8 else 0 for l in range(27)])
    qcore = [-1, -1, 1, 1, 1, 1, 1, 1] + [0] * 6 + [0 if v in holes else 1 for v in P13]
    # pair candidates: (column of first, column of second) with disjoint label sets
    def disjoint(b1, b2):
        return not (set(b1[1:]) & set(b2[1:]))
    stats = {"nodes": 0, "lammu": 0, "demand": 0, "psd": 0, "class": 0, "leaves_alive": 0}
    alive = []
    N = 47  # max seed size
    S = np.zeros((N, N), dtype=np.int64); S[:27, :27] = A
    C2 = np.zeros((N, N), dtype=np.int64)
    used = np.zeros(27, dtype=np.int64)
    qseed = list(qcore)

    def add_vertex(idx, b):
        for v in b:
            S[idx, v] = S[v, idx] = 1

    def remove_vertex(idx):
        S[idx, :] = 0; S[:, idx] = 0

    def lammu_ok(n):
        Sn = S[:n, :n]
        C = Sn @ Sn
        lim = np.where(Sn == 1, 1, 2)
        np.fill_diagonal(lim, 99)
        return bool((C <= lim).all())

    pairs_BZ = [(b1, b2) for b1 in cand[1] for b2 in cand[0] if disjoint(b1, b2)]
    pairs_BB = [(b1, b2) for b1, b2 in itertools.combinations(cand[1], 2) if disjoint(b1, b2)]
    if verbose:
        print("candidate pairs BZ", len(pairs_BZ), "BB", len(pairs_BB), flush=True)

    def fits(p):
        for b in p:
            for v in b[1:]:
                if used[v] + 1 > demand[v]:
                    return False
        # both columns of a pair add to the same labels only if disjoint (already) ; check combined
        u2 = used.copy()
        for b in p:
            for v in b[1:]:
                u2[v] += 1
        return bool((u2 <= demand).all())

    order = []  # depth -> list of chosen pair indices

    def rec(depth, start_bz):
        stats["nodes"] += 1
        if limit and stats["nodes"] > limit:
            return
        n = 27 + 2 * depth
        if depth == 5:
            if not (used == demand).all():
                stats["demand"] += 1; return
            stats["leaves_alive"] += 1
            alive.append(list(order))
            return
        if depth < 4:
            plist = range(start_bz, len(pairs_BZ)); src = pairs_BZ
        else:
            plist = range(len(pairs_BB)); src = pairs_BB
        for pi in plist:
            p = src[pi]
            if not fits(p):
                continue
            i1, i2 = n, n + 1
            add_vertex(i1, p[0]); add_vertex(i2, p[1])
            S[i1, i2] = S[i2, i1] = 1
            for b in p:
                for v in b[1:]:
                    used[v] += 1
            ok = lammu_ok(n + 2)
            if not ok:
                stats["lammu"] += 1
            else:
                qseed.extend([1, 0] if depth < 4 else [1, 1])
                if (depth + 1) in test_depths:
                    bad = class_min_violation(S[:n + 2, :n + 2].copy(), qseed)
                    if bad:
                        if bad[0][0] in ("PSD_qgram", "PSD_K"):
                            stats["psd"] += 1
                        else:
                            stats["class"] += 1
                        ok = False
                if ok:
                    order.append((depth, pi))
                    rec(depth + 1, pi + 1 if depth < 4 else 0)
                    order.pop()
                del qseed[-2:]
            for b in p:
                for v in b[1:]:
                    used[v] -= 1
            remove_vertex(i1); remove_vertex(i2)
            for v in range(27):
                S[v, :27] = A[v]  # restore core rows touched by remove (core-core unchanged anyway)
    rec(0, 0)
    return stats, alive


if __name__ == "__main__":
    cores = json.load(open("cores27.json"))
    k = int(sys.argv[1]); holes = [int(v) for v in sys.argv[2].split(",")]
    lim = int(sys.argv[3]) if len(sys.argv) > 3 else None
    t = time.time()
    st, al = enumerate_ox(cores[k], holes, verbose=True, limit=lim)
    print("core", k, "holes", holes, st, "time", round(time.time() - t, 1), flush=True)
