"""The 7-adic obligation of a generic line at rank 37 (LAB 19/10/2026; principle: Codex's September notes 124-127,
"construction complete"; re-derived here).

Conway: M = A - 3I, and mod 7 the eigenvalues 3 and -4 merge.  For a line T with near block N[T] = T u N(T) (39
vertices) and far set F (60), let d(T) = dim ker_7 (3I - G_T) (G_T the cubic graph on N(T)).  If d(T) = 1, ker_7 of
M[N,N] is the 2-dimensional span of the line eigenvectors (-4 e_t + 1_{C_t}, summing to zero), which are genuine
-4-eigenvectors of Gamma supported on N[T]; hence M[F,N] kills them and
    rank_7(A - 3I) = rank_7(M[N,N]) + rank_7(Res_T) = 37 + rank_7(Res_T),
    Res_T = (R_T - 3I) - E_ext X E_ext^T    (X any generalised inverse of M[N,N] mod 7; E_ext = far-near incidence).
Since rank_7(A - 3I) is in {37, 39, 41, 43} (archive), rank_7(Res_T) <= 6 for EVERY generic line, and at rank 37
Res_T = 0: the far graph is forced, R_T(w,w') = e_w^T X e_w' mod 7 for w != w', and e_w^T X e_w = -3 = 4 mod 7.

This script: random connected G_T with d = 1, candidate name triples of far vertices (two non-partner names per class,
lambda/mu filter L2, diagonal condition q(w) = 4), then a backtracking search for 60 far vertices (one per p-pair)
with distinct q- and s-pairs, pairwise forced adjacency in {0,1}, margins K not exceeded, at most one shadow per
transversal 3-set (L3), 8 forced far neighbours per far vertex at the end.  Counts nodes; time limit.
usage: python obligation37.py <seed> <seconds> [count]"""
import itertools
import json
import random
import sys
import time

import numpy as np

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
sys.path.insert(0, __import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)), "..", "reduction_2026-10-19"))
from ll_test import components, gt_matrix, k_matrix, pairs_of, random_gt  # noqa: E402
from rank7_line import ginv_mod, rank_mod  # noqa: E402

P7 = 7


def setup(n, s01, s12, s20):
    G = gt_matrix(n, s01, s12, s20)
    N = 3 * n
    Lap = (3 * np.eye(N, dtype=np.int64) - G) % P7
    d = N - rank_mod(Lap, P7)
    # near block on T (3) + N(T) (36): T points adjacent pairwise; point c adjacent to class c
    A = np.zeros((3 + N, 3 + N), dtype=np.int64)
    for a in range(3):
        for b in range(3):
            if a != b:
                A[a, b] = 1
    for c in range(3):
        for i in range(n):
            A[c, 3 + c * n + i] = A[3 + c * n + i, c] = 1
    A[3:, 3:] = G
    MNN = (A - 3 * np.eye(3 + N, dtype=np.int64)) % P7
    rk = rank_mod(MNN, P7)
    X = ginv_mod(MNN, P7)
    return G, d, rk, X


def candidates(n, s01, s12, s20, G, X):
    P = pairs_of(n)
    N = 3 * n
    cand = {pi: [] for pi in range(len(P))}
    nb = [np.nonzero(G[x])[0] for x in range(N)]
    for pi, pp in enumerate(P):
        for qq in P:
            for ss in P:
                names = [pp[0], pp[1], n + qq[0], n + qq[1], 2 * n + ss[0], 2 * n + ss[1]]
                nm = set(names)
                ok = True
                for x in names:                                  # L2 for x in names: <= 1 G-neighbour among names
                    if sum(1 for y in nb[x] if y in nm) > 1:
                        ok = False
                        break
                if not ok:
                    continue
                # L2 for x not in names: <= 2 (only possible violation: all 3 neighbours are names)
                cnt = {}
                for y in names:
                    for x in nb[y]:
                        if x not in nm:
                            cnt[x] = cnt.get(x, 0) + 1
                if any(c > 2 for c in cnt.values()):
                    continue
                e = np.zeros(3 + N, dtype=np.int64)
                e[[3 + x for x in names]] = 1
                Xe = (X @ e) % P7
                if int(e @ Xe) % P7 != 4:
                    continue
                cand[pi].append((pp, qq, ss, tuple(names), Xe))
    return P, cand


def search(n, P, cand, K, seconds):
    """backtracking: one triple per p-pair; forward checking on pairwise forced adjacency and bijectivity"""
    t0 = time.time()
    nodes = [0]
    m = len(P)
    K01, K02, K12 = K[0:n, n:2 * n], K[0:n, 2 * n:3 * n], K[n:2 * n, 2 * n:3 * n]
    best = [0]

    def ev(t1, t2):                                              # forced adjacency value e1^T X e2 mod 7
        e2 = np.zeros(3 + 3 * n, dtype=np.int64)
        e2[[3 + x for x in t2[3]]] = 1
        return int(t1[4] @ e2) % P7

    def rec(assigned, domains, used_q, used_s, c01, c02, c12):
        nodes[0] += 1
        if time.time() - t0 > seconds:
            raise TimeoutError
        best[0] = max(best[0], len(assigned))
        if len(assigned) == m:
            return assigned
        # choose the unassigned p-pair with the smallest domain
        pi = min((p for p in range(m) if p not in assigned), key=lambda p: len(domains[p]))
        for t in domains[pi]:
            pp, qq, ss, names, Xe = t
            # margins: adding t increments K-counts for pairs (u,v) in p x q etc.
            ok = True
            for u in pp:
                for v in qq:
                    if c01[u, v] + 1 > K01[u, v]:
                        ok = False
                for w in ss:
                    if c02[u, w] + 1 > K02[u, w]:
                        ok = False
            for v in qq:
                for w in ss:
                    if c12[v, w] + 1 > K12[v, w]:
                        ok = False
            if not ok:
                continue
            nd = {}
            dead = False
            for p2 in range(m):
                if p2 in assigned or p2 == pi:
                    continue
                keep = [t2 for t2 in domains[p2] if t2[1] != qq and t2[2] != ss and ev(t, t2) in (0, 1)
                        and not (len(set(t2[0]) & set(pp)) and len(set(t2[1]) & set(qq)) and len(set(t2[2]) & set(ss)))]
                if not keep:
                    dead = True
                    break
                nd[p2] = keep
            if dead:
                continue
            for u in pp:
                for v in qq:
                    c01[u, v] += 1
                for w in ss:
                    c02[u, w] += 1
            for v in qq:
                for w in ss:
                    c12[v, w] += 1
            nd[pi] = [t]
            assigned[pi] = t
            r = rec(assigned, {**domains, **nd}, used_q | {qq}, used_s | {ss}, c01, c02, c12)
            if r:
                return r
            del assigned[pi]
            for u in pp:
                for v in qq:
                    c01[u, v] -= 1
                for w in ss:
                    c02[u, w] -= 1
            for v in qq:
                for w in ss:
                    c12[v, w] -= 1
        return None

    try:
        sol = rec({}, dict(cand), set(), set(), np.zeros((n, n), int), np.zeros((n, n), int), np.zeros((n, n), int))
        return ("FOUND" if sol else "REFUTED"), nodes[0], best[0], round(time.time() - t0, 2)
    except TimeoutError:
        return "TIMEOUT", nodes[0], best[0], round(time.time() - t0, 2)


def main():
    seed, seconds = int(sys.argv[1]), float(sys.argv[2])
    count = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    rng = random.Random(seed)
    n = 12
    done = 0
    while done < count:
        s01, s12, s20, tries = random_gt(n, rng, 1)
        G, d, rk, X = setup(n, s01, s12, s20)
        rec = {"seed": seed, "instance": done, "d": d, "rank7_near": rk}
        if d != 1:
            rec["skip"] = "non-generic line (d > 1)"
            print(json.dumps(rec), flush=True)
            continue
        t0 = time.time()
        P, cand = candidates(n, s01, s12, s20, G, X)
        sizes = sorted(len(v) for v in cand.values())
        rec.update(cand_min=sizes[0], cand_median=sizes[len(sizes) // 2], cand_max=sizes[-1], cand_s=round(time.time() - t0, 1))
        K = k_matrix(n, G)
        st, nodes, depth, wall = search(n, P, cand, K, seconds)
        rec.update(status=st, nodes=nodes, max_depth=depth, search_s=wall)
        print(json.dumps(rec), flush=True)
        done += 1


if __name__ == "__main__":
    main()
