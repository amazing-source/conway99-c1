# Microscope, not a proof step.  Second level for k = e = 0: the support together with the seven inner orbits.
# For a given orbit graph B on m vertices (a line of support_k0_m{m}_survivors.txt), enumerate the D7 labels of the m
# support orbits (in the gauge, p_i is adjacent to the two inner vertices given by the signed root r_i), up to the signed
# permutations of the 7 blocks (first-appearance normal form), under the exact necessary conditions:
#   distinct orbits (r_i != +-r_j);   sum_i r_i = 0 (every inner vertex has as many neighbours in P as in Q);
#   every inner vertex has at most dmax neighbours in P (report 3.3, 3.5);
#   common-neighbour budgets:  agree(i,j) + codeg_B(i,j) <= 2 for i != j;   opposite(i,j) <= 1 if i ~_B j.
# Then tests: (PSD, floating, tolerance 1e-9) the Gram matrices of H and 7I - H on the 7 + m orbits;
#             (DUAL) the dual-norm rule: a vector of norm in {1..10} minus {m} in Z a + sum Z H e_i over these 7 + m
#                    orbits (exact).  Norms 1..7: A.5; 8: T16; 9: T18; 10: T20 (for m = 8, 9, 10 the lemma of size m itself
#                    is of course not used: norm m is allowed).
# usage: python level2_labels.py m line_index [seconds] [max number of PSD configurations tested]
# The run stops at the time cap or at the given number of tested configurations (deterministic), whichever comes first;
# the counts are then those of the first branches of the search only.
import sys, time
import numpy as np
from descent_singular import lattice_basis_gram, short_vectors

def main():
    m = int(sys.argv[1]); idx = int(sys.argv[2]); cap = float(sys.argv[3]) if len(sys.argv) > 3 else 240.0
    maxpsd = int(sys.argv[4]) if len(sys.argv) > 4 else 10 ** 9
    lines = [l for l in open(f"support_k0_m{m}_survivors.txt") if "SINGULAR" not in l]
    edges = lines[idx].split("#")[0].split()
    B = [[0] * m for _ in range(m)]
    for e in edges:
        i, j = map(int, e.split("-"))
        B[i][j] = B[j][i] = 1
    cod = [[sum(B[i][l] * B[j][l] for l in range(m)) for j in range(m)] for i in range(m)]
    dmax = 3 if m in (8, 9, 11) else 4
    roots = []
    for c in range(7):
        for c2 in range(c + 1, 7):
            for s in (1, -1):
                for s2 in (1, -1):
                    roots.append(((c, s), (c2, s2)))
    t0 = time.time()
    lab = [None] * m
    plus = [0] * 7; minus = [0] * 7
    stats = {"labelled": 0, "psd": 0, "dual_killed": 0, "left": 0, "timeout": False}
    examples = []

    def compatible(i, r):
        d = dict(r)
        for j in range(i):
            dj = dict(lab[j])
            agree = sum(1 for c in d if c in dj and dj[c] == d[c])
            opp = sum(1 for c in d if c in dj and dj[c] == -d[c])
            if agree == 2 or opp == 2:
                return False
            if agree + cod[i][j] > 2:
                return False
            if B[i][j] and opp > 1:
                return False
        return True

    def leaf():
        stats["labelled"] += 1
        n = 7 + m
        H = np.zeros((n, n))
        for c in range(7):
            H[c, c] = 4
        for i in range(m):
            H[7 + i, 7 + i] = 3
            for j in range(m):
                if B[i][j]:
                    H[7 + i, 7 + j] = 1
            for (c, s) in lab[i]:
                H[c, 7 + i] = H[7 + i, c] = -s
        if np.linalg.eigvalsh(H)[0] < -1e-9 or np.linalg.eigvalsh(7 * np.eye(n) - H)[0] < -1e-9:
            return
        stats["psd"] += 1
        G = [[0] * (n + 1) for _ in range(n + 1)]
        G[0][0] = m
        for i in range(m):
            G[0][8 + i] = G[8 + i][0] = 7
        for i in range(n):
            for j in range(n):
                G[1 + i][1 + j] = 7 * int(round(H[i, j]))
        Gb = lattice_basis_gram(G)
        sv = [x for x in short_vectors(Gb, 10) if x != m]     # norm m is the vector a itself (and its like)
        if sv:
            stats["dual_killed"] += 1
        else:
            stats["left"] += 1
            if len(examples) < 3:
                examples.append([tuple(l) for l in lab])

    def rec(i, used):
        if time.time() - t0 > cap or stats["psd"] >= maxpsd:
            stats["timeout"] = True
            return
        if i == m:
            if all(plus[c] == minus[c] for c in range(7)):
                leaf()
            return
        rem = m - i
        for r in roots:
            (c, s), (c2, s2) = r
            # first-appearance normal form: new coordinates in increasing order, with sign +
            if c >= used:
                if c != used or s != 1:
                    continue
                if c2 != used + 1 or s2 != 1:
                    continue
                nu = used + 2
            elif c2 >= used:
                if c2 != used or s2 != 1:
                    continue
                nu = used + 1
            else:
                nu = used
            if not compatible(i, r):
                continue
            for (cc, ss) in r:
                if ss == 1: plus[cc] += 1
                else: minus[cc] += 1
            ok = all(plus[x] <= dmax and minus[x] <= dmax for x in (c, c2))
            if ok:
                # the imbalance must be repairable by the remaining rows (each row changes two coordinates by 1)
                imb = sum(abs(plus[x] - minus[x]) for x in range(7))
                if imb <= 2 * (rem - 1):
                    lab[i] = r
                    rec(i + 1, nu)
                    lab[i] = None
            for (cc, ss) in r:
                if ss == 1: plus[cc] -= 1
                else: minus[cc] -= 1

    rec(0, 0)
    print(f"m = {m}, graph #{idx}: {' '.join(edges)}")
    print(f"   label configurations (normal form, budgets): {stats['labelled']};  PSD: {stats['psd']};"
          f"  killed by the dual-norm rule: {stats['dual_killed']};  left: {stats['left']};"
          f"  {'STOPPED AT THE CAP (partial counts)' if stats['timeout'] else 'complete'};  {time.time() - t0:.0f} s")
    for ex in examples:
        print("   example left:", ex)

if __name__ == "__main__":
    main()
