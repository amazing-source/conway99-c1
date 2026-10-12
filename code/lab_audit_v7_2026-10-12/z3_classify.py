"""Lab session, 2026-10-12. ALL the Z3-covers of the Brouwer-Haemers graph BH = srg(81,20,1,6) that are srg(243,22,1,2).

Exact formulation (Codex, note NOTE_RELEVEMENT_S3_QUADRATIQUE of 12/10, trivial signing; checked on BvLS by
z3_linear.py): gains t -> t + b_xy with b in F_3, b_yx = -b_xy, and
  (T) b_xy + b_yz + b_zx = 0 on every line {x,y,z} of BH;
  (L) for every non-adjacent pair P, R the six values c_Z = b_PZ + b_ZR (Z a common neighbour) are 0, 1, 2 twice each.
Two gain functions differing by b'_xy = b_xy + a_y - a_x give the same cover.

Method. The vertices of BH are added one at a time (each time the vertex with most neighbours already placed); the
edges are ordered by the moment their later end is placed. Gauge: for every vertex but the first, the edge to its
first placed neighbour has b = 0. The linear consequences of (T), of the first moments sum_Z c_Z = 0 and of the gauge
are put in echelon form with the LAST edge of every relation as pivot, so that along the edge order an edge is either
determined by the earlier ones or free (3 values). Depth-first search on the edges; a pair (P, R) is tested as soon as
its 12 edges are known, and a partial test (no value three times) is applied whenever one of its c_Z becomes known.
Every solution is a cover; its number of flat grids of BH (holonomy trivial on the 3 x 3 grids) identifies it among
the known covers (405: BvLS, 45: twin, 117: Gamma3, 189: Gamma4), and one representative per value is written out as
a 243-vertex edge list for the full audit.

python z3_classify.py <a srg(243,22,1,2) edge list with a regular spread, used only to build BH> <output prefix> [node cap]
One process, below 1 GB."""
import sys, os, itertools, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))      # this folder only (the script is run with -I)
from z3_linear import load, spreads
n = 243

def build_bh(path):
    A = load(path); S, adj = spreads(A); F = S[0]; fib = {}
    for i, l in enumerate(F):
        for p in l: fib[p] = i
    Q = np.zeros((81, 81), dtype=np.int64)
    for i, l1 in enumerate(F):
        for l2 in F[i + 1:]:
            if A[np.ix_(l1, l2)].sum() == 3: Q[i, fib[l2[0]]] = Q[fib[l2[0]], i] = 1
    assert (Q @ Q + 5 * Q == 14 * np.eye(81, dtype=np.int64) + 6).all()
    return Q

def main():
    Q = build_bh(sys.argv[1]); prefix = sys.argv[2]; cap = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 12; t0 = time.time()
    nb = [[int(j) for j in np.nonzero(Q[i])[0]] for i in range(81)]
    # vertex order
    order = [0]; placed = {0}
    while len(order) < 81:
        best = max((v for v in range(81) if v not in placed), key=lambda v: (sum(1 for u in nb[v] if u in placed), -v))
        order.append(best); placed.add(best)
    pos = {v: i for i, v in enumerate(order)}
    edges = []; parent_edge = {}
    for v in order[1:]:
        back = sorted((u for u in nb[v] if pos[u] < pos[v]), key=lambda u: pos[u])
        for k, u in enumerate(back):
            if k == 0: parent_edge[v] = len(edges)
            edges.append((u, v))                              # oriented from the earlier vertex u to the later vertex v
    E = len(edges); eidx = {e: k for k, e in enumerate(edges)}
    def term(x, y):                                           # b_xy as (edge index, coefficient)
        return (eidx[(x, y)], 1) if (x, y) in eidx else (eidx[(y, x)], 2)
    rows = []
    tri = sorted({tuple(sorted((i, j, k))) for i in range(81) for j in nb[i] for k in nb[i] if j < k and Q[j, k]})
    for i, j, k in tri:
        r = np.zeros(E, dtype=np.int64)
        for u, v in ((i, j), (j, k), (k, i)):
            e, c = term(u, v); r[e] = (r[e] + c) % 3
        rows.append(r)
    pairs = [(P, R) for P in range(81) for R in range(P + 1, 81) if not Q[P, R]]
    pterms = []                                               # for every pair: six (e1, c1, e2, c2) with c_Z = c1 b_e1 + c2 b_e2
    for P, R in pairs:
        r = np.zeros(E, dtype=np.int64); six = []
        for Z in range(81):
            if Q[P, Z] and Q[Z, R]:
                e1, c1 = term(P, Z); e2, c2 = term(Z, R); six.append((e1, c1, e2, c2))
                r[e1] = (r[e1] + c1) % 3; r[e2] = (r[e2] + c2) % 3
        rows.append(r); pterms.append(six)
    for v, e in parent_edge.items():
        r = np.zeros(E, dtype=np.int64); r[e] = 1; rows.append(r)
    # echelon form with the last edge of every relation as pivot
    M = np.array(rows) % 3; pivot_row = {}
    r = 0
    for c in range(E - 1, -1, -1):
        p = np.nonzero(M[r:, c])[0]
        if len(p) == 0: continue
        p = p[0] + r
        if p != r: M[[r, p]] = M[[p, r]]
        if M[r, c] == 2: M[r] = (2 * M[r]) % 3
        for q in np.nonzero(M[:, c])[0]:
            if q != r: M[q] = (M[q] - M[q, c] * M[r]) % 3
        pivot_row[c] = r; r += 1
        if r == len(M): break
    rank = r; free = [c for c in range(E) if c not in pivot_row]
    print("BH: %d edges; rank of lines + first moments + gauge: %d; free edges: %d" % (E, rank, len(free)), flush=True)
    # value of a pivot edge c: x_c = - sum_{e < c} M[row][e] x_e   (all other entries of the row are before c)
    dep = {}
    for c, rr in pivot_row.items():
        nz = np.nonzero(M[rr])[0]; assert nz.max() == c
        dep[c] = [(int(e), int(M[rr, e])) for e in nz if e != c]
    # pair bookkeeping: for each edge, the (pair, slot) whose c_Z becomes known at that edge
    ready = [[] for _ in range(E)]
    for pi, six in enumerate(pterms):
        for s, (e1, c1, e2, c2) in enumerate(six): ready[max(e1, e2)].append((pi, s))
    if os.environ.get("Z3_EXPORT"):                          # text model for z3cov.c: the same search in C
        NL = chr(10)
        with open(os.environ["Z3_EXPORT"], "w", newline=NL) as fo:
            fo.write("%d %d" % (E, len(pairs)) + NL)
            for k in range(E):
                fo.write(("D %d " % len(dep[k]) + " ".join("%d %d" % ec for ec in dep[k]) if k in dep else "F") + NL)
            for k in range(E):
                fo.write("%d " % len(ready[k]) + " ".join("%d %d" % ps for ps in ready[k]) + NL)
            for six in pterms:
                fo.write(" ".join("%d %d %d %d" % t4 for t4 in six) + NL)
        print("model written to %s" % os.environ["Z3_EXPORT"])
    if os.environ.get("Z3_SOLUTIONS"):                       # read the solutions found by z3cov.c instead of searching
        sols = [[int(ch) for ch in line.strip()] for line in open(os.environ["Z3_SOLUTIONS"]) if line.strip() and line[0] in "012"]
        assert all(len(v) == E for v in sols); print("solutions read from %s: %d" % (os.environ["Z3_SOLUTIONS"], len(sols)))
        cap = -1
    x = [0] * E; cnt = [[0, 0, 0] for _ in pairs]; nodes = 0; depth_hist = [0] * (E + 1)
    if cap >= 0: sols = []
    sys.setrecursionlimit(10000)
    stopped = [False]
    def assign(k, val):
        """set x[k] = val, update the pairs; returns the list of updates done (for undo) or None if a pair fails"""
        x[k] = val; done = []
        for pi, s in ready[k]:
            e1, c1, e2, c2 = pterms[pi][s]; c = (c1 * x[e1] + c2 * x[e2]) % 3
            cnt[pi][c] += 1; done.append((pi, c))
            if cnt[pi][c] > 2:
                for pj, cc in done: cnt[pj][cc] -= 1
                return None
        return done
    def rec(k):
        nonlocal nodes
        if stopped[0]: return
        if k == E:
            sols.append(list(x)); return
        if k in dep:
            vals = [(-sum(c * x[e] for e, c in dep[k])) % 3]
        else: vals = [0, 1, 2]
        for val in vals:
            nodes += 1
            if nodes > cap: stopped[0] = True; return
            done = assign(k, val)
            if done is None: continue
            depth_hist[k + 1] += 1
            rec(k + 1)
            for pj, cc in done: cnt[pj][cc] -= 1
    if cap >= 0: rec(0)
    print("search: %d nodes, %d solutions%s  [%.0f s]" % (nodes, len(sols), " (STOPPED at the node cap)" if stopped[0] else " (exhaustive)", time.time() - t0), flush=True)
    fr = [depth_hist[c + 1] for c in free]
    print("partial assignments alive after each free edge: %s" % fr)
    # flat grids of BH
    adjQ = [set(nb[i]) for i in range(81)]
    grids = set()
    for xv in range(81):
        L = sorted({tuple(sorted((y, next(iter(adjQ[xv] & adjQ[y]))))) for y in adjQ[xv]})
        for (a, b), (c, d) in itertools.combinations(L, 2):
            e = []
            for p in (a, b):
                for q in (c, d):
                    cn = (adjQ[p] & adjQ[q]) - {xv}
                    cand = [z for z in cn if len(adjQ[z] & {xv, a, b, c, d}) == 2]
                    e.append(cand)
            # grid = 9 vertices inducing K3 x K3: try the combinations of the fourth corners
            for comb in itertools.product(*e):
                S = [xv, a, b, c, d] + list(comb)
                if len(set(S)) == 9 and all(len(adjQ[s] & set(S)) == 4 for s in S): grids.add(tuple(sorted(S)))
    grids = sorted(grids)
    def bval(sol, u, v):
        e, c = term(u, v); return (c * sol[e]) % 3
    def flat(sol, g):
        gs = set(g)
        for a in g:                                           # every 4-cycle a-b-c-d of the grid has holonomy 0
            for b in adjQ[a] & gs:
                for c in adjQ[b] & gs:
                    if c == a or c in adjQ[a]: continue
                    for d in adjQ[c] & adjQ[a] & gs:
                        if d == b: continue
                        if (bval(sol, a, b) + bval(sol, b, c) + bval(sol, c, d) + bval(sol, d, a)) % 3: return False
        return True
    hist = {}; rep = {}
    for sol in sols:
        f = sum(1 for g in grids if flat(sol, g)); hist[f] = hist.get(f, 0) + 1; rep.setdefault(f, sol)
    print("grids of BH: %d; solutions by number of flat grids: %s" % (len(grids), sorted(hist.items())))
    for f, sol in sorted(rep.items()):
        out = "%s_flat%d.edges" % (prefix, f); lines_ = []
        for i in range(81):
            lines_ += ["%d %d" % (3 * i, 3 * i + 1), "%d %d" % (3 * i, 3 * i + 2), "%d %d" % (3 * i + 1, 3 * i + 2)]
        for (u, v) in edges:
            bv = sol[eidx[(u, v)]]
            for t in range(3): lines_.append("%d %d" % (3 * u + t, 3 * v + (t + bv) % 3))
        open(out, "w", newline="\n").write("\n".join(lines_) + "\n"); print("   representative with %d flat grids written to %s" % (f, out))

if __name__ == "__main__":
    main()
