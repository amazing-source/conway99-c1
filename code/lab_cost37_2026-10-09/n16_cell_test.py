"""C1, lab session, 2026-10-10. Rank 37 against ONE world of norm 16 (Codex's typed world: core + D + Z, 35 vertices,
Seidel rank 33): the test of one complete neighbourhood, in the residual form.

Rank 37 <=> the vertices are isotropic vectors of a non-degenerate 36-dimensional space W over F_7, product 6 (= -1)
on edges and 1 on non-edges. The base spans a non-degenerate subspace V of dimension 33 (its Seidel matrix has rank 33
and the two relations f, g are true relations), so a new vertex a is v_a + r_a with v_a in V given by its products with
the base and r_a in the 3-dimensional complement. For a set S of new vertices,
    R[a][b] = t_ab - <v_a, v_b>      (t_aa = 0, t_ab = 6 if a ~ b, 1 otherwise)
is the Gram matrix of the r_a, so rank(R) <= 3 modulo 7 (equivalently: Seidel rank of base + S is 33 + rank R <= 36).

Cell of a core vertex c: its simple neighbours (8 for norm 16). Together with the core and D neighbours of c they are
the whole neighbourhood of c, which induces 7 disjoint edges, and every other base vertex x has its common neighbours
with c inside base + cell:
    number of members adjacent to x  =  (1 if x ~ c else 2) - |N(x) & N(c) & base|          (exact).
A member whose partner is not in the base is matched with another member (the only adjacencies inside the cell).
Two members have at most 2 - [adjacent] common neighbours in the base (c included).

The script lists, for each of the 16 core vertices, the complete cells satisfying the combinatorial rules and
rank(R) <= 3 at every step. ZERO for one cell means: this world does not exist at rank 37. The discriminant of W is
not used. Exploration program (Python): one process, a node cap per cell.

python n16_cell_test.py <typed world json> [node cap per cell] [rank | norank] [cells, e.g. P0,Q3]
(norank: control, the rank is not tested; the complete cells found then show that the combinatorial rules alone are
satisfiable)"""
import sys, json, time, itertools
P7 = 7

def rank_mod7(M):
    M = [[x % P7 for x in r] for r in M]; n = len(M); rk = 0
    for c in range(n):
        p = next((r for r in range(rk, n) if M[r][c]), None)
        if p is None: continue
        M[rk], M[p] = M[p], M[rk]; iv = pow(M[rk][c], P7 - 2, P7); M[rk] = [x * iv % P7 for x in M[rk]]
        for r in range(n):
            if r != rk and M[r][c]:
                f = M[r][c]; M[r] = [(a - f * b) % P7 for a, b in zip(M[r], M[rk])]
        rk += 1
    return rk

def independent_rows(K):
    rows = []; basis = []
    for i in range(len(K)):
        v = [x % P7 for x in K[i]]
        for piv, b in basis:
            if v[piv]:
                f = v[piv]; v = [(a - f * c) % P7 for a, c in zip(v, b)]
        piv = next((j for j, x in enumerate(v) if x), None)
        if piv is None: continue
        iv = pow(v[piv], P7 - 2, P7); basis.append((piv, [x * iv % P7 for x in v])); rows.append(i)
    return rows

def inverse(M):
    n = len(M); A = [[x % P7 for x in r] + [int(i == j) for j in range(n)] for i, r in enumerate(M)]
    for c in range(n):
        p = next(r for r in range(c, n) if A[r][c]); A[c], A[p] = A[p], A[c]
        iv = pow(A[c][c], P7 - 2, P7); A[c] = [x * iv % P7 for x in A[c]]
        for r in range(n):
            if r != c and A[r][c]:
                f = A[r][c]; A[r] = [(a - f * b) % P7 for a, b in zip(A[r], A[c])]
    return [r[n:] for r in A]

def main():
    D = json.load(open(sys.argv[1])); cap = int(sys.argv[2]) if len(sys.argv) > 2 else 2000000; norank = len(sys.argv) > 3 and sys.argv[3] == "norank"
    only = sys.argv[4].split(",") if len(sys.argv) > 4 else None          # optional list of cells, e.g. P0,Q3
    A = D["base_adjacency"]; n = len(A); lab = D["base_labels"]
    K = [[0 if i == j else (6 if A[i][j] else 1) for j in range(n)] for i in range(n)]
    I = independent_rows(K); assert len(I) == 33, len(I)
    Kinv = inverse([[K[i][j] for j in I] for i in I])
    nbr = [sum(1 << j for j in range(n) if A[i][j]) for i in range(n)]
    def vec(mask):
        s = [6 if (mask >> j) & 1 else 1 for j in range(n)]; sI = [s[i] for i in I]
        c = [sum(Kinv[a][b] * sI[b] for b in range(33)) % P7 for a in range(33)]
        ok = all(sum(K[x][I[a]] * c[a] for a in range(33)) % P7 == s[x] for x in range(n))      # the dependent base vertices agree
        return sI, c, ok
    print("world: %s; base %d vertices, Seidel rank %d; D edge %s; %s" % (D["source"], n, len(I), D["source"].get("D_edge"), "CONTROL: rank not tested" if norank else "rank of the residual Gram matrix <= 3 tested"))
    total_dead = 0
    for side, off in (("P", 0), ("Q", 8)):
        for idx in range(8):
            if only and (side + str(idx)) not in only: continue
            c0 = off + idx; t0 = time.time()
            doms = [d for d in D["domains"] if d["cell"][0 if side == "P" else 1] == idx]
            slots = []                                         # (domain index, slot in the domain)
            for di, d in enumerate(doms):
                for k in range(d["multiplicity"]): slots.append((di, k))
            # exact numbers of members adjacent to every other base vertex
            need = {}
            for x in range(n):
                if x == c0: continue
                need[x] = (1 if A[x][c0] else 2) - bin(nbr[x] & nbr[c0]).count("1")
            if min(need.values()) < 0: print("  cell of %s%d: base already over-saturated" % (side, idx)); continue
            inner = nbr[c0]                                    # base neighbours of c0: a member adjacent to one of them has its partner in the base
            cand = []; bad = 0
            for di, d in enumerate(doms):
                lst = []
                for m in d["neighbour_masks"]:
                    if not (m >> c0) & 1: raise SystemExit("mask without the cell vertex")
                    sI, c, ok = vec(m)
                    if not ok: bad += 1; continue
                    if any(((m >> x) & 1) and need[x] == 0 for x in need): continue
                    npart = bin(m & inner).count("1")
                    if npart > 1: continue
                    lst.append((m, sI, c, npart))
                cand.append(lst)
            order = sorted(range(len(doms)), key=lambda di: len(cand[di]))
            seq = [(di, k) for di in order for k in range(doms[di]["multiplicity"])]
            nodes = [0]; sols = [0]; depthmax = [0]; lv = [0] * (len(seq) + 1); stop = [False]; first = [None]
            def prod(a, b): return sum(x * y for x, y in zip(a[1], b[2])) % P7
            def rec(pos, chosen, cnt, partner, R):
                # chosen: list of candidates; partner[i]: -2 base partner, -1 not yet matched, j >= 0 matched with member j
                if stop[0]: return
                if pos == len(seq):
                    if any(cnt.get(x, 0) != need[x] for x in need): return
                    if any(p == -1 for p in partner): return
                    sols[0] += 1
                    if first[0] is None: first[0] = [(doms[seq[i][0]]["cell"], chosen[i][0], partner[i]) for i in range(len(seq))]
                    return
                di, k = seq[pos]; start = 0
                if k > 0: start = chosen_index[pos - 1] + 1          # two vertices of one cell: increasing mask index (their masks differ)
                for ci in range(start, len(cand[di])):
                    cd = cand[di][ci]; m = cd[0]
                    if any(((m >> x) & 1) and cnt.get(x, 0) + 1 > need[x] for x in need): continue
                    # partner options: in the base (npart = 1), or an earlier unmatched member, or later
                    opts = [-2] if cd[3] == 1 else [-1] + [j for j in range(pos) if partner[j] == -1]
                    for op in opts:
                        ok = True; row = []
                        for j in range(pos):
                            adj = (op == j)
                            if bin(m & chosen[j][0]).count("1") > (1 if adj else 2): ok = False; break
                            if seq[j][0] == di and bin(m & chosen[j][0]).count("1") != 2: ok = False; break      # same cell: exactly the two core vertices in common
                            row.append(((6 if adj else 1) - prod(cd, chosen[j])) % P7)
                        if not ok: continue
                        nodes[0] += 1
                        if nodes[0] > cap: stop[0] = True; return
                        R2 = [r + [row[i]] for i, r in enumerate(R)] + [row + [(-prod(cd, cd)) % P7]]
                        if not norank and rank_mod7(R2) > 3: continue
                        lv[pos + 1] += 1
                        if pos + 1 > depthmax[0]: depthmax[0] = pos + 1
                        cnt2 = dict(cnt)
                        for x in need:
                            if (m >> x) & 1: cnt2[x] = cnt2.get(x, 0) + 1
                        p2 = list(partner) + [op]
                        if op >= 0: p2[op] = pos
                        chosen_index.append(ci)
                        rec(pos + 1, chosen + [cd], cnt2, p2, R2)
                        chosen_index.pop()
                        if stop[0]: return
            chosen_index = []
            rec(0, [], {}, [], [])
            status = ("STOPPED at the node cap (%d complete cells so far)" % sols[0]) if stop[0] else ("DEAD" if sols[0] == 0 else "%d complete cells" % sols[0])
            total_dead += (sols[0] == 0 and not stop[0])
            print("  cell of %s%d: %d members, candidates per domain %s (masks contradicting the relations: %d); nodes %d, kept by depth %s; %s  [%.1f s]" % (
                side, idx, len(seq), [len(cand[di]) for di in order], bad, nodes[0], lv[1:], status, time.time() - t0), flush=True)
    print("cells without any admissible completion: %d of 16%s" % (total_dead, "" if norank else "  (one is enough to exclude this world at rank 37)"))

if __name__ == "__main__":
    main()
