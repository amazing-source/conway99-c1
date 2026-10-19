"""Independent reviewer model of K2BC (H01 = -H02, grids Q45, Q13, Q26; Q12 free).  Own labels, own builder, own
checks, own CP-SAT frontier (adjacency variables, not profiles)."""
import gzip, json, sys, importlib.util
from itertools import combinations, permutations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
SC = HERE.parent
CODEX = SC / 'k3prod_v4' / 'pkg' / 'code' / 'codex'
COVERS = SC / 'pybd_k2bc_all'

def rect_labels(a, b):
    return [(2 * a + s, 2 * b + t) for s in (0, 1) for t in (0, 1)]

KRECTS = [(0, 1), (0, 2), (4, 5), (1, 3), (2, 6)]
KL = [lab for r in KRECTS for lab in rect_labels(*r)]
KIDX = {q: i for i, q in enumerate(KL)}
def RECT_OF(q): return tuple(sorted((q[0] // 2, q[1] // 2)))
OUTR = [r for r in combinations(range(7), 2) if r not in KRECTS]
OL = [lab for r in OUTR for lab in rect_labels(*r)]
def shared(a, b): return len(set(a) & set(b))
def quota(q, l): return 2 - (l in q) - ((l ^ 1) in q)
def base(q, F):
    r = RECT_OF(q)
    return 2 if r == F else (0 if set(r) & set(F) else 1)
SH = [[shared(a, b) for b in KL] for a in KL]
LM = [sum(2 ** i for i, q in enumerate(KL) if l in q) for l in range(14)]
BLOCKS = [((1, 3), (0, 2)), ((2, 6), (0, 1)), ((1, 3), (4, 5)), ((2, 6), (4, 5)), ((1, 3), (2, 6))]
def kid(rect, corner): return KIDX[rect_labels(*rect)[corner]]
def pc(x): return x.bit_count()

def cv(u):
    return KIDX[rect_labels(0, 1)[u]] if u < 4 else KIDX[rect_labels(0, 2)[u - 4]]

def base_rows(core_edges, boundary):
    rows = [0] * 20
    def e(u, v):
        rows[u] |= 2 ** v; rows[v] |= 2 ** u
    for u, v in core_edges:
        e(cv(u), cv(v))
    for r in KRECTS[2:]:
        L = rect_labels(*r)
        for a, b in combinations(L, 2):
            if shared(a, b) == 1:
                e(KIDX[a], KIDX[b])
    for c, mask in enumerate(boundary):
        for u in range(8):
            if mask // (2 ** u) % 2:
                e(cv(u), kid((4, 5), c))
    return rows

def add_block(rows, bi, p):
    rows = rows[:]
    A, B = BLOCKS[bi]
    for c in range(4):
        u, v = kid(A, c), kid(B, p[c])
        rows[u] |= 2 ** v; rows[v] |= 2 ** u
    return rows

def bit(rows, u, v): return rows[u] // (2 ** v) % 2

def full_ok(rows):
    for u in range(20):
        if pc(rows[u]) > 12:
            return False
        for l in range(14):
            if pc(rows[u] & LM[l]) > quota(KL[u], l):
                return False
        for v in range(u + 1, 20):
            if pc(rows[u] & rows[v]) + SH[u][v] > 2 - bit(rows, u, v):
                return False
    return True

def my_attachments(core_edges, boundary):
    P4 = list(permutations(range(4)))
    out = []
    def rec(i, rows, ch):
        if i == 5:
            out.append(tuple(ch)); return
        for p in P4:
            r = add_block(rows, i, p)
            if full_ok(r):
                rec(i + 1, r, ch + [p])
    r0 = base_rows(core_edges, boundary)
    assert full_ok(r0)
    rec(0, r0, [])
    return out

def known_rows(core_edges, boundary, att):
    r = base_rows(core_edges, boundary)
    for i, p in enumerate(att):
        r = add_block(r, i, p)
    return r

def expected_degree(u):
    q = KL[u]; r = RECT_OF(q); d = 0
    if r in ((0, 1), (0, 2)):
        d += 2
    else:
        d += base(q, (0, 1)) + base(q, (0, 2))
    for F in KRECTS[2:]:
        d += base(q, F)
    return d

def cpsat_frontier(rows, plant=None, time_limit=120.0, drop_outside_c2=False):
    from ortools.sat.python import cp_model
    m = cp_model.CpModel()
    possible = []
    for q in OL:
        poss = []
        for u, k in enumerate(KL):
            F = RECT_OF(k)
            if F in ((0, 1), (0, 2)):
                if base(q, (0, 1)) + base(q, (0, 2)) > 0:
                    poss.append(u)
            elif base(q, F) > 0:
                poss.append(u)
        possible.append(poss)
    x = {}
    for qi, poss in enumerate(possible):
        for u in poss:
            x[qi, u] = m.NewBoolVar('')
    def X(qi, u):
        return x.get((qi, u), 0)
    for qi, q in enumerate(OL):
        m.Add(sum(X(qi, u) for u in range(8)) == base(q, (0, 1)) + base(q, (0, 2)))
        for F in KRECTS[2:]:
            m.Add(sum(X(qi, kid(F, c)) for c in range(4)) == base(q, F))
        for l in range(14):
            m.Add(sum(X(qi, u) for u in range(20) if l in KL[u]) <= quota(q, l))
        for u in range(20):
            nb = [w for w in range(20) if bit(rows, u, w)]
            m.Add(sum(X(qi, w) for w in nb) + shared(q, KL[u]) + X(qi, u) <= 2)
    prods = {}
    def AND(a, b):
        y = m.NewBoolVar('')
        m.AddImplication(y, a)
        m.AddImplication(y, b)
        m.AddBoolOr([a.Not(), b.Not(), y])
        return y
    def P(qi, u, v):
        key = (qi, min(u, v), max(u, v))
        if key not in prods:
            if (qi, u) not in x or (qi, v) not in x:
                prods[key] = 0
            else:
                prods[key] = AND(x[qi, u], x[qi, v])
        return prods[key]
    if plant is None:
        deg_t = [12 - pc(rows[u]) for u in range(20)]
        let_t = [[quota(KL[u], l) - pc(rows[u] & LM[l]) for l in range(14)] for u in range(20)]
        pair_t = {(u, v): 2 - bit(rows, u, v) - SH[u][v] - pc(rows[u] & rows[v]) for u, v in combinations(range(20), 2)}
    else:
        deg_t = [sum(plant[qi][u] for qi in range(64)) for u in range(20)]
        let_t = [[sum(plant[qi][u] for qi, q in enumerate(OL) if l in q) for l in range(14)] for u in range(20)]
        pair_t = {(u, v): sum(plant[qi][u] * plant[qi][v] for qi in range(64)) for u, v in combinations(range(20), 2)}
    for u in range(20):
        m.Add(sum(X(qi, u) for qi in range(64)) == deg_t[u])
        for l in range(14):
            m.Add(sum(X(qi, u) for qi, q in enumerate(OL) if l in q) == let_t[u][l])
    for (u, v), t in pair_t.items():
        m.Add(sum(P(qi, u, v) for qi in range(64)) == t)
    if not drop_outside_c2:
        for a, b in combinations(range(64), 2):
            cap = 2 - shared(OL[a], OL[b])
            terms = [AND(x[a, u], x[b, u]) for u in range(20) if (a, u) in x and (b, u) in x]
            if len(terms) > cap:
                m.Add(sum(terms) <= cap)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = time_limit
    s.parameters.num_search_workers = 1
    st = s.Solve(m)
    return s.StatusName(st)

def load_program(cover_path):
    sys.argv = [str(HERE / 'prog_copy.py'), str(CODEX), 'GEN', str(cover_path), '0', '0',
                '--sat', '--lean', '--enc=seq', '--yr=45', '--extra=13,26']
    spec = importlib.util.spec_from_file_location('prog_copy', HERE / 'prog_copy.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def cover(ci):
    return json.loads(gzip.decompress((COVERS / ('core_%03d.json.gz' % ci)).read_bytes()))
