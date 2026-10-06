"""V7 core reconstruction (affine 37 residual, m=e=0, D = C6 + cubic 20).

Independent rebuild from the definitions (passation 06/10, sections 16-17), not from the old scripts.

Labels: 0=x 1=y 2=c 3=alpha_c 4=beta_d 5=d 6=alpha_d 7=beta_c ; mates 3,4,6,7.
t-vertices 8..13 = common neighbour of the mate pairs (3,4),(3,6),(3,7),(4,6),(4,7),(6,7).
14..26 = the 13 a-positives (a = 1 - Q_8), independent, each adjacent to exactly two t's.
Unknowns: the unique t-t edge E and the multigraph H_a (13 t-pairs), degrees 5 at the ends of E, 4 elsewhere.
"""
import itertools, json, sys
import numpy as np

GRID_EDGES = [(0, 2), (0, 5), (0, 3), (0, 6), (1, 2), (1, 5), (1, 4), (1, 7),
              (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 2)]
MATES = [3, 4, 6, 7]
TPAIRS = [(3, 4), (3, 6), (3, 7), (4, 6), (4, 7), (6, 7)]
T = list(range(8, 14))
POS13 = list(range(14, 27))
N = 27


def base_adj():
    A = np.zeros((N, N), dtype=np.int64)
    for i, j in GRID_EDGES:
        A[i, j] = A[j, i] = 1
    for k, (i, j) in enumerate(TPAIRS):
        t = 8 + k
        for m in (i, j):
            A[t, m] = A[m, t] = 1
    return A


def tcap(A0, E):
    """cap(u,v) = lambda/mu of (u,v) minus core common neighbours outside the 13s."""
    cap = {}
    for u, v in itertools.combinations(T, 2):
        adj = 1 if {u, v} == set(E) else 0
        shared = len(set(TPAIRS[u - 8]) & set(TPAIRS[v - 8]))
        cap[(u, v)] = (1 if adj else 2) - shared
    return cap


def core_ok(A):
    """lambda/mu caps on every core pair (common neighbours inside the core)."""
    C2 = A @ A
    for i in range(N):
        for j in range(i + 1, N):
            lim = 1 if A[i, j] else 2
            if C2[i, j] > lim:
                return False
    return True


def enumerate_cores():
    A0 = base_adj()
    tpairs_all = list(itertools.combinations(T, 2))
    out = []
    for E in tpairs_all:
        A1 = A0.copy()
        A1[E[0], E[1]] = A1[E[1], E[0]] = 1
        if not core_ok(A1):
            continue
        cap = tcap(A1, E)
        if min(cap.values()) < 0:
            continue
        deg = {t: (5 if t in E else 4) for t in T}
        # multigraph with given degrees and multiplicities <= cap, 13 edges
        pairs = [p for p in tpairs_all if cap[p] > 0]
        sols = []

        def rec(idx, rem, mult):
            if idx == len(pairs):
                if all(r == 0 for r in rem.values()):
                    sols.append(dict(mult))
                return
            u, v = pairs[idx]
            for m in range(min(cap[(u, v)], rem[u], rem[v]), -1, -1):
                rem[u] -= m; rem[v] -= m
                if m:
                    mult[(u, v)] = m
                rec(idx + 1, rem, mult)
                if m:
                    del mult[(u, v)]
                rem[u] += m; rem[v] += m

        rec(0, dict(deg), {})
        for H in sols:
            A = A1.copy()
            p = 14
            cols = []
            for (u, v), m in sorted(H.items()):
                for _ in range(m):
                    A[p, u] = A[u, p] = 1
                    A[p, v] = A[v, p] = 1
                    cols.append((u - 8, v - 8))
                    p += 1
            assert p == 27
            if not core_ok(A):
                continue
            delta = []
            for (u, v), c in cap.items():
                d = c - H.get((u, v), 0)
                delta += [(u - 8, v - 8)] * d
            out.append({"zero_edge": (E[0] - 8, E[1] - 8), "columns": cols, "defect": delta,
                        "adj": A.tolist()})
    return out


if __name__ == "__main__":
    cores = enumerate_cores()
    print("labelled cores:", len(cores))
    for k, c in enumerate(cores):
        A = np.array(c["adj"])
        K = 27 * np.eye(N) - 9 * A + 1
        ev = np.linalg.eigvalsh(K)
        rk = int((ev > 1e-7).sum())
        c["K_min_eig"] = float(ev.min()); c["K_rank"] = rk
        print(k, "E", c["zero_edge"], "defect", c["defect"], "minEig %.4f" % ev.min(), "rank", rk)
    json.dump(cores, open(sys.argv[1] if len(sys.argv) > 1 else "cores27.json", "w"))
