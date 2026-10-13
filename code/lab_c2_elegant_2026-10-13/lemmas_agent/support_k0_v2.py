# Microscope, not a proof step.  Same question as support_k0.py, with a stronger normalisation so that m = 12
# is reachable:   vertex 0 has the largest number of triangles;  N(0) = {1,2,3,4} carries one of the 8 graphs of
# maximum degree <= 2 on 4 vertices in a fixed labelling;  the far vertices 5..m-1 are sorted by their set of
# neighbours inside N(0) (non-increasing bitmask).  Every isomorphism class has at least one such labelling.
# Control: must give 2, 3, 6, 33 classes for m = 8, 9, 10, 11 (the same as support_k0.py).
#
# usage: python support_k0_v2.py m
import sys, time, itertools
import numpy as np
from support_k0 import canon, is_psd_int, descent_test

LOCAL = {  # graphs with max degree <= 2 on {1,2,3,4}, one labelling per isomorphism type
    "empty": [], "K2": [(1, 2)], "2K2": [(1, 2), (3, 4)], "P3": [(1, 2), (2, 3)],
    "P4": [(1, 2), (2, 3), (3, 4)], "K3": [(1, 2), (2, 3), (1, 3)], "C4": [(1, 2), (2, 3), (3, 4), (1, 4)],
}

def enumerate_graphs(n):
    out = []
    far = list(range(5, n))
    for name, loc in LOCAL.items():
        t0 = len(loc)                       # triangles at vertex 0
        adj = [0] * n
        deg = [0] * n
        cod = [[0] * n for _ in range(n)]

        def add(i, j):
            ni = [w for w in range(n) if adj[i] >> w & 1]
            nj = [w for w in range(n) if adj[j] >> w & 1]
            for w in ni:
                if cod[j][w] >= 2:
                    return False
            for w in nj:
                if cod[i][w] >= 2:
                    return False
            for w in ni:
                cod[j][w] += 1; cod[w][j] += 1
            for w in nj:
                cod[i][w] += 1; cod[w][i] += 1
            adj[i] |= 1 << j; adj[j] |= 1 << i
            deg[i] += 1; deg[j] += 1
            return True

        def rem(i, j):
            adj[i] &= ~(1 << j); adj[j] &= ~(1 << i)
            deg[i] -= 1; deg[j] -= 1
            ni = [w for w in range(n) if adj[i] >> w & 1]
            nj = [w for w in range(n) if adj[j] >> w & 1]
            for w in ni:
                cod[j][w] -= 1; cod[w][j] -= 1
            for w in nj:
                cod[i][w] -= 1; cod[w][i] -= 1

        ok = True
        for j in (1, 2, 3, 4):
            ok = ok and add(0, j)
        for (i, j) in loc:
            ok = ok and add(i, j)
        if not ok:
            continue        # the local graph itself breaks a codegree bound (C4: vertices 1,3 would share 0,2,4)
        need_inner = {i: 4 - deg[i] for i in (1, 2, 3, 4)}   # far neighbours still needed by 1..4
        masks = [frozenset(s) for r in (2, 1, 0) for s in itertools.combinations((1, 2, 3, 4), r)]
        # order of masks = decreasing "bitmask"; we use the list order as the sort key
        mrank = {mk: idx for idx, mk in enumerate(masks)}

        def triangles_ok():
            for v in range(1, n):
                t = 0
                nb = [w for w in range(n) if adj[v] >> w & 1]
                for a in range(len(nb)):
                    for b in range(a + 1, len(nb)):
                        if adj[nb[a]] >> nb[b] & 1:
                            t += 1
                if t > t0:
                    return False
            return True

        def fill_far(i):
            # complete far vertex i using far vertices > i
            if i == n:
                if all(deg[v] == 4 for v in range(n)) and triangles_ok():
                    out.append(tuple(adj))
                return
            need = 4 - deg[i]
            if need < 0:
                return
            cands = [j for j in range(i + 1, n) if deg[j] < 4 and not (adj[i] >> j & 1)]
            if len(cands) < need:
                return
            for c in itertools.combinations(cands, need):
                done = []
                good = True
                for j in c:
                    if add(i, j):
                        done.append(j)
                    else:
                        good = False
                        break
                if good:
                    fill_far(i + 1)
                for j in reversed(done):
                    rem(i, j)

        def assign(pos, last_rank, left):
            # choose the mask of far vertex far[pos], ranks non-decreasing in the list order
            if pos == len(far):
                if all(x == 0 for x in left.values()):
                    fill_far(5)
                return
            v = far[pos]
            for mk in masks[last_rank:]:
                if any(left[i] == 0 for i in mk):
                    continue
                done = []
                good = True
                for i in mk:
                    if add(i, v):
                        done.append(i)
                    else:
                        good = False
                        break
                if good:
                    for i in mk:
                        left[i] -= 1
                    assign(pos + 1, mrank[mk], left)
                    for i in mk:
                        left[i] += 1
                for i in reversed(done):
                    rem(i, v)

        assign(0, 0, dict(need_inner))
    return out

def main():
    m = int(sys.argv[1])
    t0 = time.time()
    labelled = enumerate_graphs(m)
    t1 = time.time()
    print(f"m = {m}: labelled graphs with the normalisation: {len(labelled)}  ({t1 - t0:.1f} s)", flush=True)
    classes = {}
    seen_raw = set()
    for adj in labelled:
        if adj in seen_raw:
            continue
        seen_raw.add(adj)
        c = canon(list(adj), m)
        classes[c] = classes.get(c, 0) + 1
    t2 = time.time()
    print(f"isomorphism classes (4-regular, all codegrees <= 2): {len(classes)}  ({t2 - t1:.1f} s)", flush=True)
    F = min(m - 1, 10)
    n_psd = 0
    surv = []
    killed = []
    for c in sorted(classes):
        B = [[(c[i] >> j) & 1 for j in range(m)] for i in range(m)]
        M3 = [[(3 if i == j else 0) + B[i][j] for j in range(m)] for i in range(m)]
        M4 = [[(4 if i == j else 0) - B[i][j] for j in range(m)] for i in range(m)]
        if not (is_psd_int(M3) and is_psd_int(M4)):
            continue
        n_psd += 1
        ev = np.linalg.eigvalsh(np.array(B, dtype=float))
        if ev[0] < -3 + 1e-9:
            surv.append((c, "SINGULAR 3I+B"))
            continue
        sv = descent_test(B, m, F)
        if sv:
            killed.append((c, sorted(set(x[0] for x in sv))))
        else:
            surv.append((c, ""))
    print(f"classes with 3I+B and 4I-B positive semidefinite (exact): {n_psd}")
    print(f"classes killed by the descent test (a vector of norm 1..{F} in Z a + sum Z He_i): {len(killed)}")
    from collections import Counter
    print("   norms found in the killed classes:", Counter(tuple(k[1]) for k in killed))
    print(f"classes that pass: {len(surv)}")
    with open(f"support_k0_m{m}_survivors.txt", "w") as f:
        for c, note in surv:
            edges = [f"{i}-{j}" for i in range(m) for j in range(i + 1, m) if (c[i] >> j) & 1]
            f.write(" ".join(edges) + (" # " + note if note else "") + "\n")
    print(f"total time {time.time() - t0:.1f} s")

if __name__ == "__main__":
    main()
