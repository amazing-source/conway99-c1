"""(GG) test for a line type (exploration, LAB 17/10/2026).
Line l = {v,0,1}; G_l = cubic graph on its 36 neighbours (letters 2..13, L_0, L_1); D = the 60 far labels {a,b} with
a, b in 2..13 (distance 2 from l).  N = adjacency G_l x D.  For two vertices w != w' of G_l the srg counts give EXACTLY
    (N N^t)_{ww'} = [w ~ w' ? 1 : 2] - [same group] - (A_G^2)_{ww'}                       (GG)
(common neighbours lie in l, in G_l or in D).  Letters are attached to far labels by name; each far label has 2
neighbours in L_0 and 2 in L_1 (its common neighbours with the points 0 and 1); each label of L_0 u L_1 has 10 far
neighbours.  Also, for w in G_l and z in D, common neighbours inside G_l are at most lambda / mu.
(GG) does not involve the far-far edges.  It is a necessary condition on G_l alone (mode free) or on G_l plus the
attachments of the 20 far labels already present in a four-star block (mode block).
usage: python gg_test.py <distinct cache.jsonl> <max blocks> <seconds> [block] [c=1 only: c1]"""
import itertools
import json
import sys
import time

from ortools.sat.python import cp_model

MATE = lambda i: i ^ 1


def orient(labels, edges, side):
    """side 0: l = {v,0,1}; side 1: l = {v,2,3} relabelled to {v,0,1} by 0<->2, 1<->3."""
    perm = list(range(14))
    if side == 1:
        perm[0], perm[2], perm[1], perm[3] = 2, 0, 3, 1
    f = lambda l: frozenset(perm[x] for x in l)
    return [f(l) for l in labels], set(frozenset((f(a), f(b))) for a, b in edges)


def line_graph(L, E):
    X = [("L", a) for a in range(2, 14)]
    L01 = [l for l in L if l & {0, 1}]
    V = X + L01
    pos = {x: i for i, x in enumerate(V)}
    n = len(V)
    A = [[0] * n for _ in range(n)]
    for a in range(2, 14):
        A[pos[("L", a)]][pos[("L", MATE(a))]] = 1
        for r in (0, 1):
            lab = frozenset((r, a))
            A[pos[("L", a)]][pos[lab]] = A[pos[lab]][pos[("L", a)]] = 1
    for x, y in itertools.combinations(L01, 2):
        if frozenset((x, y)) in E:
            A[pos[x]][pos[y]] = A[pos[y]][pos[x]] = 1
    return V, pos, A


def group(x):
    if isinstance(x, tuple):
        return "v"
    return 0 if 0 in x else 1


def components(A):
    n = len(A)
    seen, c = set(), 0
    for s in range(n):
        if s in seen:
            continue
        c += 1
        st = [s]
        seen.add(s)
        while st:
            u = st.pop()
            for w in range(n):
                if A[u][w] and w not in seen:
                    seen.add(w)
                    st.append(w)
    return c


def gg_model(V, pos, A, fixed=None):
    n = len(V)
    D = [frozenset((a, b)) for a, b in itertools.combinations(range(2, 14), 2) if b != MATE(a)]
    m = cp_model.CpModel()
    N = {}
    for i, x in enumerate(V):
        for k, z in enumerate(D):
            if isinstance(x, tuple):
                N[(i, k)] = 1 if x[1] in z else 0
            else:
                if fixed is not None and z in fixed:
                    N[(i, k)] = 1 if x in fixed[z] else 0
                else:
                    N[(i, k)] = m.NewBoolVar("")
    labs = [i for i, x in enumerate(V) if not isinstance(x, tuple)]
    for k, z in enumerate(D):
        for r in (0, 1):
            m.Add(sum(N[(i, k)] for i in labs if group(V[i]) == r) == 2)
    for i in labs:
        m.Add(sum(N[(i, k)] for k in range(len(D))) == 10)
    A2 = [[sum(A[i][t] * A[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
    bad = []
    for i, j in itertools.combinations(range(n), 2):
        tgt = (1 if A[i][j] else 2) - (1 if group(V[i]) == group(V[j]) else 0) - A2[i][j]
        if tgt < 0:
            bad.append((V[i], V[j], tgt))
            continue
        terms = []
        const = 0
        for k in range(len(D)):
            a, b = N[(i, k)], N[(j, k)]
            if isinstance(a, int) and isinstance(b, int):
                const += a * b
            elif isinstance(a, int):
                if a:
                    terms.append(b)
            elif isinstance(b, int):
                if b:
                    terms.append(a)
            else:
                q = m.NewBoolVar("")
                m.AddBoolOr([a.Not(), b.Not(), q])
                m.AddImplication(q, a)
                m.AddImplication(q, b)
                terms.append(q)
        m.Add(sum(terms) + const == tgt)
    # common neighbours inside G_l of w in G_l and z in D: at most lambda / mu
    for i in range(n):
        nb = [t for t in range(n) if A[i][t]]
        for k in range(len(D)):
            s = [N[(t, k)] for t in nb]
            e = N[(i, k)]
            if isinstance(e, int):
                m.Add(sum(s) <= (1 if e else 2))
            else:
                m.Add(sum(s) <= 2 - e)
    return m, D, N, bad


if __name__ == "__main__":
    cache, mx, secs = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
    mode_block = "block" in sys.argv[4:]
    only_c1 = "c1" in sys.argv[4:]
    done = 0
    for line in open(cache):
        if done >= mx:
            break
        d = json.loads(line)
        for side in (0, 1):
            if done >= mx:
                break
            L, E = orient([frozenset(x) for x in d["labels"]], d["edges"], side)
            V, pos, A = line_graph(L, E)
            if any(sum(r) != 3 for r in A):
                continue
            c = components(A)
            if only_c1 and c != 1:
                continue
            fixed = None
            if mode_block:
                fixed = {}
                for z in L:
                    if z & {0, 1}:
                        continue
                    fixed[z] = set(w for w in L if (w & {0, 1}) and frozenset((z, w)) in E)
            m, D, N, bad = gg_model(V, pos, A, fixed)
            t0 = time.time()
            if bad:
                print("%s side %d c=%d: line type violates the caps %s" % (d["src"], side, c, bad[:2]), flush=True)
                done += 1
                continue
            sv = cp_model.CpSolver()
            sv.parameters.num_search_workers = 2
            sv.parameters.max_time_in_seconds = secs
            st = sv.Solve(m)
            print("%s side %d c=%d mode=%s: %s in %.1f s" % (d["src"], side, c, "block" if mode_block else "free",
                                                          sv.StatusName(st), time.time() - t0), flush=True)
            done += 1
