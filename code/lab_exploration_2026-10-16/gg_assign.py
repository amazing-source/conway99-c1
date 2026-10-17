"""(GG) far design for a line type, assignment encoding (exploration, LAB 17/10/2026).
Exact facts (srg counts) for l = {v,0,1} (see gg_test.py): every far label z (the 60 labels {a,b}, a,b in 2..13) has
exactly 2 neighbours in L_0 and 2 in L_1, and
  - two labels of L_0 that are not mu_0-paired have EXACTLY ONE common far neighbour (their 2nd common neighbour
    after the point 0; none in G_l), mu_0-paired ones none:  z -> (its L_0 pair) is a BIJECTION D -> non-mu_0 pairs;
    same for L_1 (and for the letters, where it is the name of the label);
  - letter a / label {r,b}: number of far labels {a,x} attached to {r,b} = d^r_a(b) (exact, from A_G^2);
  - {0,b} / {1,c}: number of far labels attached to both = t(b,c) (exact);
  - caps: for w in G_l and z far, common neighbours of w, z inside G_l <= lambda / mu.
Variables y^r[z][e] (z far, e a non-mu_r pair): assignment; u^r[z][b] = sum_{e ni b} y^r[z][e].
usage: python gg_assign.py <distinct cache.jsonl> <max> <seconds> [c1] [block]"""
import itertools
import json
import sys
import time

from ortools.sat.python import cp_model

sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else ".")
from gg_test import orient, line_graph, components, group, MATE  # noqa: E402


def model(V, pos, A, fixed=None):
    n = len(V)
    D = [frozenset((a, b)) for a, b in itertools.combinations(range(2, 14), 2) if b != MATE(a)]
    A2 = [[sum(A[i][t] * A[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
    idx = lambda r, b: pos[frozenset((r, b))]
    mu = {r: {} for r in (0, 1)}
    for r in (0, 1):
        for b in range(2, 14):
            for b2 in range(2, 14):
                if b2 != b and A[idx(r, b)][idx(r, b2)]:
                    mu[r][b] = b2
    m = cp_model.CpModel()
    U = {}
    for r in (0, 1):
        E = [(b, b2) for b, b2 in itertools.combinations(range(2, 14), 2) if mu[r][b] != b2]
        assert len(E) == 60, len(E)
        y = {(k, e): m.NewBoolVar("") for k in range(60) for e in range(60)}
        for k in range(60):
            m.AddExactlyOne([y[(k, e)] for e in range(60)])
        for e in range(60):
            m.AddExactlyOne([y[(k, e)] for k in range(60)])
        for k in range(60):
            for b in range(2, 14):
                U[(r, k, b)] = sum(y[(k, e)] for e, (p, q) in enumerate(E) if b in (p, q))
        if fixed is not None:
            for k, z in enumerate(D):
                if z in fixed:
                    att = sorted(x for w in fixed[z] if r in w for x in w if x != r)
                    if len(att) == 2:
                        e = E.index(tuple(att))
                        m.Add(y[(k, e)] == 1)
    # letter / label counts
    for r in (0, 1):
        for a in range(2, 14):
            for b in range(2, 14):
                i, j = pos[("L", a)], idx(r, b)
                tgt = (1 if A[i][j] else 2) - A2[i][j]
                m.Add(sum(U[(r, k, b)] for k, z in enumerate(D) if a in z) == tgt)
    # L_0 / L_1 cross counts
    for b in range(2, 14):
        for c in range(2, 14):
            i, j = idx(0, b), idx(1, c)
            tgt = (1 if A[i][j] else 2) - A2[i][j]
            prods = []
            for k in range(60):
                q = m.NewBoolVar("")
                prods.append((q, k))
            terms = []
            for q, k in prods:
                # q = u0 and u1 (u are 0/1 linear expressions)
                m.Add(q <= U[(0, k, b)])
                m.Add(q <= U[(1, k, c)])
                m.Add(q >= U[(0, k, b)] + U[(1, k, c)] - 1)
                terms.append(q)
            m.Add(sum(terms) == tgt)
    # caps: w in G_l, z far: common neighbours inside G_l <= lambda / mu
    def att(w, k, z):
        x = V[w]
        if isinstance(x, tuple):
            return 1 if x[1] in z else 0
        r = 0 if 0 in x else 1
        b = min(x - {r})
        return U[(r, k, b)]
    for w in range(n):
        nb = [t for t in range(n) if A[w][t]]
        for k, z in enumerate(D):
            s = sum(att(t, k, z) for t in nb)
            e = att(w, k, z)
            m.Add(s <= 2 - e)
    return m


if __name__ == "__main__":
    cache, mx, secs = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
    only_c1 = "c1" in sys.argv[4:]
    mode_block = "block" in sys.argv[4:]
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
                fixed = {z: set(w for w in L if (w & {0, 1}) and frozenset((z, w)) in E) for z in L if not (z & {0, 1})}
            t0 = time.time()
            m = model(V, pos, A, fixed)
            sv = cp_model.CpSolver()
            sv.parameters.num_search_workers = 2
            sv.parameters.max_time_in_seconds = secs
            st = sv.Solve(m)
            print("%s side %d c=%d %s: %s in %.1f s" % (d["src"], side, c, "block" if mode_block else "free",
                                                     sv.StatusName(st), time.time() - t0), flush=True)
            done += 1
