# Generalised independent adjacency model: known = core Q01+Q02 (H01=-H02) + grids GR (list of line pairs), in order.
from itertools import combinations
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver
def labels_of(F): a, b = F; return [(2 * a + s, 2 * b + t) for s in range(2) for t in range(2)]
def setup(GR):
    K = labels_of((0, 1)) + labels_of((0, 2))
    for F in GR: K += labels_of(F)
    ALL = [(l, m) for l in range(14) for m in range(l + 1, 14) if l // 2 != m // 2]
    O = [q for q in ALL if q not in K]
    return K, O
def rect(q): return frozenset((q[0] // 2, q[1] // 2))
def base(q, F):
    r = rect(q); F = frozenset(F)
    return 2 if r == F else (0 if r & F else 1)
def sh(a, b): return len(set(a) & set(b))
def regions(GR):
    reg = [("core", list(range(8)), lambda q: base(q, (0, 1)) + base(q, (0, 2)))]
    for i, F in enumerate(GR):
        reg.append((F, list(range(8 + 4 * i, 12 + 4 * i)), (lambda F: lambda q: base(q, F))(F)))
    return reg
def constraints_on_witness(GR, A, X):
    """X: dict (q, u) -> 0/1 for q in O. Returns list of violated constraint names (exact model, no encoding)."""
    K, O = setup(GR); n = len(K); bad = []
    x = lambda q, u: X.get((q, u), 0)
    for q in O:
        for name, us, f in regions(GR):
            if sum(x(q, u) for u in us) != f(q): bad.append(("R", q, name))
    for u in range(n):
        if sum(x(q, u) for q in O) != 12 - A[u].bit_count(): bad.append(("D", u))
        for l in range(14):
            have = sum(1 for v in range(n) if A[u] >> v & 1 and l in K[v])
            if sum(x(q, u) for q in O if l in q) != 2 - (l in K[u]) - ((l ^ 1) in K[u]) - have: bad.append(("Lk", u, l))
    for u, v in combinations(range(n), 2):
        t = 2 - (A[u] >> v & 1) - sh(K[u], K[v]) - (A[u] & A[v]).bit_count()
        if sum(x(q, u) * x(q, v) for q in O) != t: bad.append(("Pk", u, v))
    for q in O:
        for l in range(14):
            if sum(x(q, u) for u in range(n) if l in K[u]) > 2 - (l in q) - ((l ^ 1) in q): bad.append(("Lo", q, l))
        for v in range(n):
            if sum(x(q, u) for u in range(n) if A[v] >> u & 1) > 2 - x(q, v) - sh(q, K[v]): bad.append(("Cko", q, v))
    for a, b in combinations(O, 2):
        if sum(x(a, u) * x(b, u) for u in range(n)) > 2 - sh(a, b): bad.append(("Co", a, b))
    return bad
def solve(GR, A, solver="cadical195", enc=EncType.totalizer):
    K, O = setup(GR); n = len(K)
    vp = IDPool(); cl = []
    def card_eq(lits, t):
        if t < 0 or t > len(lits): cl.append([]); return
        if not lits: return
        cl.extend(CardEnc.equals(lits=lits, bound=t, vpool=vp, encoding=enc).clauses)
    def card_le(lits, t, guard=None):
        if t < 0:
            cl.append([] if guard is None else [-guard]); return
        if t >= len(lits): return
        sub = CardEnc.atmost(lits=lits, bound=t, vpool=vp, encoding=enc).clauses
        cl.extend(sub if guard is None else [c + [-guard] for c in sub])
    X = {}
    REG = regions(GR)
    for q in O:
        for name, us, f in REG:
            if f(q) > 0:
                for u in us: X[q, u] = vp.id(("x", q, u))
    x = lambda q, u: X.get((q, u))
    for q in O:
        for name, us, f in REG:
            if f(q): card_eq([x(q, u) for u in us], f(q))
    for u in range(n):
        card_eq([x(q, u) for q in O if x(q, u)], 12 - A[u].bit_count())
        for l in range(14):
            have = sum(1 for v in range(n) if A[u] >> v & 1 and l in K[v])
            card_eq([x(q, u) for q in O if l in q and x(q, u)], 2 - (l in K[u]) - ((l ^ 1) in K[u]) - have)
    AND = {}
    def conj(a, b):
        key = (min(a, b), max(a, b))
        if key not in AND:
            y = vp.id(("and",) + key); AND[key] = y
            cl.extend([[-y, a], [-y, b], [y, -a, -b]])
        return AND[key]
    for u, v in combinations(range(n), 2):
        t = 2 - (A[u] >> v & 1) - sh(K[u], K[v]) - (A[u] & A[v]).bit_count()
        card_eq([conj(x(q, u), x(q, v)) for q in O if x(q, u) and x(q, v)], t)
    for q in O:
        for l in range(14):
            card_le([x(q, u) for u in range(n) if l in K[u] and x(q, u)], 2 - (l in q) - ((l ^ 1) in q))
        for v in range(n):
            lits = [x(q, u) for u in range(n) if A[v] >> u & 1 and x(q, u)]
            cap = 2 - sh(q, K[v])
            card_le(lits, cap)
            if x(q, v): card_le(lits, cap - 1, guard=x(q, v))
    for a, b in combinations(O, 2):
        card_le([conj(x(a, u), x(b, u)) for u in range(n) if x(a, u) and x(b, u)], 2 - sh(a, b))
    with Solver(name=solver, bootstrap_with=cl) as s:
        r = s.solve()
        model = set(v for v in s.get_model() if v > 0) if r else None
    return r, len(cl), (None if model is None else {k: int(v in model) for k, v in X.items()})
