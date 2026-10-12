"""Lab session, 2026-10-12. The group orders used in the orbit count of THEOREM_Z3_COVERS.md, computed with the
stabiliser-chain routine of audit243.py (no nauty):
 1. |Aut(BH)| for the quotient BH = srg(81,20,1,6) of the first regular spread of BvLS;
 2. for each of the four graphs: |Aut|, the number of regular spreads and the orbits of Aut on them, hence the order of
    the stabiliser of a regular spread;
 3. the predicted number of gain functions in tree gauge: 2 |Aut(BH)| / (|Aut_S| / 3) for each graph, to compare with
    the numbers found by the exhaustive search (z3cov).

python z3_orbit_check.py <bvls.edges> <twin.edges> <gamma3.edges> <gamma4.edges>        One process, about 3 minutes."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audit243 as AU
import z3_linear as ZL

def group(A, nn):
    AU.n = nn
    return AU.aut_order(A)

def main():
    files = sys.argv[1:5]; names = ["BvLS", "twin", "Gamma3", "Gamma4"]
    # 1. Aut(BH)
    A = ZL.load(files[0]); S, adj = ZL.spreads(A); F = S[0]; fib = {}
    for i, l in enumerate(F):
        for p in l: fib[p] = i
    Q = np.zeros((81, 81), dtype=np.int64)
    for i, l1 in enumerate(F):
        for l2 in F[i + 1:]:
            if A[np.ix_(l1, l2)].sum() == 3: Q[i, fib[l2[0]]] = Q[fib[l2[0]], i] = 1
    assert (Q @ Q + 5 * Q == 14 * np.eye(81, dtype=np.int64) + 6).all()
    obh, base, orbs, gens, calls = group(Q, 81)
    print("BH = srg(81,20,1,6): |Aut| = %d (orbit lengths along the chain %s)" % (obh, orbs), flush=True)
    total = 0
    for name, f in zip(names, files):
        A = ZL.load(f); S, adj = ZL.spreads(A)
        order, base, orbs, gens, calls = group(A, 243)
        keys = [frozenset(frozenset(l) for l in s) for s in S]; idx = {k: i for i, k in enumerate(keys)}; parent = list(range(len(S)))
        def find(x):
            while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
            return x
        for g in gens:
            for i, s in enumerate(S):
                img = frozenset(frozenset(int(g[p]) for p in l) for l in s); j = idx[img]
                ri, rj = find(i), find(j)
                if ri != rj: parent[ri] = rj
        sizes = {}
        for i in range(len(S)): sizes[find(i)] = sizes.get(find(i), 0) + 1
        osz = sorted(sizes.values())
        stab = order // osz[0] if len(osz) == 1 else None
        pred = (2 * obh * 3) // stab if stab else None
        total += pred or 0
        print("%s: |Aut| = %d; regular spreads %d in orbits %s; stabiliser of a spread %s; predicted gain functions in tree gauge (both signs) %s, half %s" % (
            name, order, len(S), osz, stab, pred, pred // 2 if pred else None), flush=True)
    print("predicted total for the four graphs: %d (half: %d)" % (total, total // 2))

if __name__ == "__main__":
    main()
