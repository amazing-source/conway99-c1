"""Anatomy of the mod-3 kernel of A_Omega (59 vertices) on c(l) = 1 blocks at the floor rank_3 = 47 (nullity 12)."""
import itertools, json, sys
from collections import Counter
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, XL, Y, rank_mod, relabel, build_H, gl_connected
from c1_hidden import comps_m

def nullspace_mod(M, p):
    A = [[int(x) % p for x in row] for row in M]
    rows, cols = len(A), len(A[0])
    piv, r = [], 0
    for c in range(cols):
        pr = next((i for i in range(r, rows) if A[i][c]), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [(x * inv) % p for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        piv.append(c); r += 1
    free = [c for c in range(cols) if c not in piv]
    basis = []
    for f in free:
        v = [0] * cols
        v[f] = 1
        for i, c in enumerate(piv):
            v[c] = (-A[i][f]) % p
        basis.append(v)
    return basis

def rank_rows(vecs, p):
    return rank_mod(vecs, p) if vecs else 0

def dim_sub(K, coords, p):
    """dim of {x in span K : x vanishes on coords}"""
    if not K:
        return 0
    # solve: combos c with sum c_i K_i [coords] = 0
    M = [[K[i][c] for i in range(len(K))] for c in coords]
    if not M:
        return len(K)
    return len(K) - rank_mod(M, p)

def main():
    want = int(sys.argv[2])
    seen = 0
    agg = Counter()
    for line in open(sys.argv[1]):
        d = json.loads(line)
        if len(d["labels"]) != 44:
            continue
        S0 = [frozenset(x) for x in d["labels"]]
        E0 = [(frozenset(a), frozenset(b)) for a, b in d["edges"]]
        for side in (0, 1):
            L, EE = relabel(S0, E0, side)
            conn, degok = gl_connected(EE)
            if not (conn and degok):
                continue
            V, A = build_H(EE, with_l=True)
            if rank_mod(A.tolist(), 3) != 47:
                continue
            pos = {x: i for i, x in enumerate(V)}
            n = len(V)
            K = nullspace_mod(A.tolist(), 3)
            # coordinates
            lco = [pos[("P", "v")], pos[("P", 0)], pos[("P", 1)]]
            Aco = [pos[("L", a)] for a in range(2, 14)]
            Yco = [pos[y] for y in Y]
            Bco = [pos[w] for w in XL if 0 in w]
            Cco = [pos[w] for w in XL if 1 in w]
            Yp = [pos[w] for w in XL if not (w & {2, 3})]       # far labels of m
            Q01 = [pos[w] for w in XL if w & {2, 3}]
            # psi vectors mod 3: 1_star(r) - 1_{N(v) minus line(r)}
            def star(r):
                return [pos[w] for w in XL + Y if r in w]
            def nv_minus(line):
                out = [pos[("P", 0)], pos[("P", 1)]] + Aco
                lm = {0: (0, 1), 1: (0, 1), 2: (2, 3), 3: (2, 3)}[line]
                drop = [pos[("P", x)] if x in (0, 1) else pos[("L", x)] for x in lm]
                return [c for c in out if c not in drop]
            psis = []
            for r in range(4):
                v = [0] * n
                for c in star(r):
                    v[c] = (v[c] + 1) % 3
                for c in nv_minus(r):
                    v[c] = (v[c] - 1) % 3
                psis.append(v)
            Am = A.tolist()
            ok = all(all(sum(Am[i][j] * p_[j] for j in range(n)) % 3 == 0 for i in range(n)) for p_ in psis)
            rpsi = rank_rows(psis, 3)
            cm, _ = comps_m(EE)
            mQ = {}
            for lam in (3, 0, -3, 6, -6):
                Mq = (A - lam * np.eye(n, dtype=np.int64)).tolist()
                mQ[lam] = n - rank_mod(Mq, 1000000007)
            key = (len(K), rpsi, ok, cm, mQ[3], mQ[0], mQ[-3], mQ[6], mQ[-6],
                   dim_sub(K, Yco, 3), dim_sub(K, Yp, 3), dim_sub(K, Yco + Yp, 3), dim_sub(K, lco, 3))
            agg[key] += 1
            seen += 1
            if seen >= want:
                break
        if seen >= want:
            break
    print("floor blocks (rank_3 = 47):", seen)
    print("(dimK3, rank psi0..3 mod 3, psi in kernel, c(m), multQ(3), multQ(0), multQ(-3), multQ(6), multQ(-6),")
    print(" dim K3 with x_Y=0, with x_Y'=0, with both, with x_l=0) : count")
    for k, v in sorted(agg.items()):
        print("   ", k, v)

main()
