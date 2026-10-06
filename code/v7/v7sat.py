"""V7 full completion as one SAT instance (per core).

Seed: the 27-vertex core (fixed).  Outside slots 27..98: grid class and q-value fixed by the slot
(x: 6 Bx + 4 Zx, y: 6 By + 4 Zy, c and d: 2 P0 + 8 Z0, each mate: 1 P0 + 7 Z0).
Unknowns: outside-label adjacencies (B), outside-outside adjacencies (F), the 4 holes among the 13 a-positives.
Constraints: srg(99,14,1,2) on all pairs, the affine equation (A+4I)q = 6*1 at all 99 vertices,
m = e = 0 and no NZZ (Zx, Zy independent, no Zx-Zy edge), lexicographic order of B rows inside each slot group.
UNSAT = exclusion of the core.  SAT = a graph, to be checked independently.
"""
import itertools, json, sys, time
import numpy as np
from srgsat import SRGCompletion, check_srg, TRUE, FALSE

GRID = list(range(8)); MATES = [3, 4, 6, 7]; T = list(range(8, 14)); P13 = list(range(14, 27))
LABELS = T + P13
QG = {0: -1, 1: -1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}


def slots():
    S = []  # (vertex, grid, q, group)
    v = 27
    spec = [(0, [(1, 6), (0, 4)]), (1, [(1, 6), (0, 4)]), (2, [(1, 2), (0, 8)]), (5, [(1, 2), (0, 8)]),
            (3, [(1, 1), (0, 7)]), (4, [(1, 1), (0, 7)]), (6, [(1, 1), (0, 7)]), (7, [(1, 1), (0, 7)])]
    for g, parts in spec:
        for q, cnt in parts:
            for _ in range(cnt):
                S.append((v, g, q, (g, q))); v += 1
    assert v == 99
    return S


def build(core, fix_holes=None, symbreak=True):
    A = np.array(core["adj"])
    SL = slots()
    gof = {v: g for v, g, q, grp in SL}
    qout = {v: q for v, g, q, grp in SL}
    fixed = {}
    for i in range(27):
        for j in range(i + 1, 27):
            fixed[(i, j)] = int(A[i, j])
    for v, g, q, grp in SL:
        for i in GRID:
            fixed[(i, v)] = 1 if i == g else 0
    Zx = [v for v, g, q, grp in SL if g == 0 and q == 0]
    Zy = [v for v, g, q, grp in SL if g == 1 and q == 0]
    for a, b in itertools.combinations(Zx, 2):
        fixed[(a, b)] = 0
    for a, b in itertools.combinations(Zy, 2):
        fixed[(a, b)] = 0
    for a in Zx:
        for b in Zy:
            fixed[(min(a, b), max(a, b))] = 0
    S = SRGCompletion(99, 14, 1, 2, fixed)
    h = {v: S.newvar(("h", v)) for v in P13}
    S.card_eq([h[v] for v in P13], 4)
    if fix_holes is not None:
        for v in P13:
            S.clause([h[v] if v in fix_holes else -h[v]])

    def qlit(w):
        """q(w) as (coefficient, literal) or None if q(w)=0."""
        if w < 8:
            return QG[w]
        if w < 14:
            return 0
        if w < 27:
            return ("var", w)
        return qout[w]

    S.add_degrees()
    S.add_common()
    # affine equation at every vertex: sum_{w~v} q(w) = 6 - 4 q(v)
    for v in range(99):
        terms = []
        rhs = 6
        qv = qlit(v)
        if qv == ("var", v) or isinstance(qv, tuple):
            # v is a 13-vertex: rhs = 6 - 4(1-h_v) = 2 + 4 h_v -> handled with conditional counts below
            pass
        else:
            rhs -= 4 * qv
        for w in range(99):
            if w == v:
                continue
            e = S.adj(v, w)
            if e == FALSE:
                continue
            qw = qlit(w)
            if qw == 0:
                continue
            if isinstance(qw, tuple):
                terms.append((1, S.AND(e, -h[qw[1]])))
            else:
                terms.append((qw, e))
        if isinstance(qv, tuple):
            # sum = 2 + 4 h_v : build lits (+1 terms only? check signs)
            lits = []
            const = 0
            for c, l in terms:
                if c == 1:
                    lits.append(l)
                else:
                    lits.append(S.NOT(l)); const += 1
            o = S.counter(lits, 8)
            # value = count - const ; need value == 2 (h=0) or 6 (h=1)
            for target, cond in ((2, -h[v]), (6, h[v])):
                tc = target + const
                if tc >= 1:
                    S.clause([S.NOT(cond), o[tc]])
                if tc + 1 <= 8:
                    S.clause([S.NOT(cond), S.NOT(o[tc + 1])])
        else:
            S.add_linear(terms, rhs)
    # redundant a-structure rows for outside vertices: #13 nbrs - #t nbrs = 2 - [grid nbr is a mate]
    for v, g, q, grp in SL:
        terms = [(1, S.adj(v, w)) for w in P13] + [(-1, S.adj(v, t)) for t in T]
        S.add_linear(terms, 2 - (1 if g in MATES else 0))
    # symmetry breaking: lexicographic B rows in each slot group
    if symbreak:
        groups = {}
        for v, g, q, grp in SL:
            groups.setdefault(grp, []).append(v)
        for grp, vs in groups.items():
            for a, b in zip(vs, vs[1:]):
                lex_leq(S, [S.adj(a, l) for l in LABELS], [S.adj(b, l) for l in LABELS])
    return S, h


def lex_leq(S, X, Y):
    """X <=_lex Y (bits, most significant first)."""
    eq_prev = TRUE
    for x, y in zip(X, Y):
        if eq_prev == FALSE:
            return
        S.clause([S.NOT(eq_prev), S.NOT(x), y])          # eq_prev -> x <= y
        e = S.pool.id(("lexeq", len(S.cnf.clauses)))       # e <-> eq_prev and (x <-> y)
        if eq_prev != TRUE:
            S.cnf.append([-e, eq_prev])
        S.clause([-e, S.NOT(x), y]); S.clause([-e, x, S.NOT(y)])
        S.clause([e, S.NOT(eq_prev), x, y]); S.clause([e, S.NOT(eq_prev), S.NOT(x), S.NOT(y)])
        eq_prev = e


if __name__ == "__main__":
    cores = json.load(open("cores27.json"))
    k = int(sys.argv[1]); tl = float(sys.argv[2])
    t0 = time.time()
    S, h = build(cores[k])
    print("core", k, "vars", S.pool.top, "clauses", len(S.cnf.clauses), "build", round(time.time() - t0, 1), flush=True)
    S.cnf.to_file(f"v7_core{k}.cnf")
    t1 = time.time()
    res, model = S.solve(time_limit=tl)
    print("core", k, "result", res, "time", round(time.time() - t1, 1), flush=True)
    if res:
        G = S.decode(model)
        print("srg check:", check_srg(G, 99, 14, 1, 2))
        json.dump(G, open(f"v7_core{k}_GRAPH.json", "w"))
