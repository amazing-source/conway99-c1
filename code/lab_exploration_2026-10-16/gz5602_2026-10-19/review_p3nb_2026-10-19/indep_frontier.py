# Independent frontier model for P3NB (adjacency formulation, my own derivation; no profiles, no py_extend constraints).
# Known K = 20 labels (core 0..7, Q45, Q46, Q13); outside O = the other 64 labels, generated from letter pairs.
# Vars x[q,u] (q in O adjacent to u in K).  Constraints (all necessary for srg(99,14,1,2) + H01=-H02 + grids 45,46,13):
#  R  : |N(q) & F| = base(q,F) for F = Q45,Q46,Q13; |N(q) & core| = base(q,01)+base(q,02)
#  D  : sum_q x[q,u] = 12 - deg_K(u)
#  Lk : sum_{q: l in q} x[q,u] = 2-[l in u]-[l^1 in u] - #{v in N_K(u): l in v}
#  Pk : sum_q x[q,u]x[q,v] = 2 - adj(u,v) - sh(u,v) - |N_K(u)&N_K(v)|
#  Lo : sum_{u in K, l in u} x[q,u] <= 2-[l in q]-[l^1 in q]
#  Co : sum_u x[q,u]x[q',u] <= 2 - sh(q,q')
#  Cko: sum_{u in N_K(v)} x[q,u] + x[q,v] <= 2 - sh(q,v)
# Compares with py_extend frontier() verdict for every yielded attachment of the chosen boundaries.
import gzip, json, runpy, sys, time, random
from itertools import combinations
pyext, codex, covdir, ci, bis = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]
MAXATT = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--maxatt=")), 1000))
cov = "%s/core_%03d.json.gz" % (covdir, ci)
sys.argv = [pyext, codex, "P3NB", cov, "0", "0", "--sat", "--lean", "--enc=seq"]
ns = runpy.run_path(pyext, run_name="__notmain__")
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver
rec = json.loads(gzip.decompress(open(cov, "rb").read())); core = rec["core"]
K = [(s, 2 + t) for s in range(2) for t in range(2)] + [(s, 4 + t) for s in range(2) for t in range(2)] \
    + [(8 + s, 10 + t) for s in range(2) for t in range(2)] + [(8 + s, 12 + t) for s in range(2) for t in range(2)] \
    + [(2 + s, 6 + t) for s in range(2) for t in range(2)]
ALL = [(l, m) for l in range(14) for m in range(l + 1, 14) if l // 2 != m // 2]
assert len(ALL) == 84
O = [q for q in ALL if q not in K]; assert len(O) == 64
def rect(q): return frozenset((q[0] // 2, q[1] // 2))
def base(q, F):
    r = rect(q); F = frozenset(F)
    return 2 if r == F else (0 if r & F else 1)
def sh(a, b): return len(set(a) & set(b))
REG = {"core": list(range(8)), "45": list(range(8, 12)), "46": list(range(12, 16)), "13": list(range(16, 20))}
def need(q, r):
    if r == "core": return base(q, (0, 1)) + base(q, (0, 2))
    return base(q, {"45": (4, 5), "46": (4, 6), "13": (1, 3)}[r])
def solve(A):
    vp = IDPool(); cl = []
    def card_eq(lits, t):
        if t < 0 or t > len(lits): cl.append([]); return
        if not lits: return
        cl.extend(CardEnc.equals(lits=lits, bound=t, vpool=vp, encoding=EncType.totalizer).clauses)
    def card_le(lits, t):
        if t < 0: cl.append([]); return
        if t >= len(lits): return
        cl.extend(CardEnc.atmost(lits=lits, bound=t, vpool=vp, encoding=EncType.totalizer).clauses)
    X = {}
    for q in O:
        for r, us in REG.items():
            if need(q, r) > 0:
                for u in us: X[q, u] = vp.id(("x", q, u))
            # need 0 -> no variable (x = 0)
    def x(q, u): return X.get((q, u))
    for q in O:
        for r, us in REG.items():
            n = need(q, r)
            if n: card_eq([x(q, u) for u in us], n)
    deg = [A[u].bit_count() for u in range(20)]
    for u in range(20):
        card_eq([x(q, u) for q in O if x(q, u)], 12 - deg[u])
        for l in range(14):
            have = sum(1 for v in range(20) if A[u] >> v & 1 and l in K[v])
            card_eq([x(q, u) for q in O if l in q and x(q, u)], 2 - (l in K[u]) - ((l ^ 1) in K[u]) - have)
    AND = {}
    def conj(a, b):
        key = (min(a, b), max(a, b))
        if key not in AND:
            y = vp.id(("and",) + key); AND[key] = y
            cl.extend([[-y, a], [-y, b], [y, -a, -b]])
        return AND[key]
    for u, v in combinations(range(20), 2):
        t = 2 - (A[u] >> v & 1) - sh(K[u], K[v]) - (A[u] & A[v]).bit_count()
        lits = [conj(x(q, u), x(q, v)) for q in O if x(q, u) and x(q, v)]
        card_eq(lits, t)
    for q in O:
        for l in range(14):
            card_le([x(q, u) for u in range(20) if l in K[u] and x(q, u)], 2 - (l in q) - ((l ^ 1) in q))
        for v in range(20):
            lits = [x(q, u) for u in range(20) if A[v] >> u & 1 and x(q, u)]
            cap = 2 - sh(q, K[v])
            if x(q, v):
                # sum lits <= cap - x[q,v]: encode both cases
                if len(lits) > cap - 1:
                    sub = CardEnc.atmost(lits=lits, bound=max(cap - 1, 0), vpool=vp, encoding=EncType.totalizer).clauses if cap - 1 >= 0 else [[]]
                    cl.extend([c + [-x(q, v)] for c in sub])
                card_le(lits, cap)
            else:
                card_le(lits, cap)
    for a, b in combinations(O, 2):
        cap = 2 - sh(a, b)
        lits = [conj(x(a, u), x(b, u)) for u in range(20) if x(a, u) and x(b, u)]
        card_le(lits, cap)
    with Solver(name="cadical195", bootstrap_with=cl) as s:
        r = s.solve()
    return r, len(cl)
recs = rec["boundaries_hex"]
if bis.startswith("rand"): sel = sorted(random.Random(ci * 104729 + 3).sample(range(len(recs)), min(int(bis[4:]), len(recs))))
else: sel = [int(t) for t in bis.split(",")]
cmp = {"attachments": 0, "both_excluded": 0, "both_open": 0, "theirs_excluded_mine_SAT": 0, "theirs_open_mine_UNSAT": 0}
details = []
t0 = time.time(); natt = 0
for bi in sel:
    bd = tuple(bytes.fromhex(recs[bi]))
    for a, _ in ns["p3nb_attachments"](core, bd):
        if natt >= MAXATT: break
        natt += 1
        rows = ns["materialize"](core, bd, a)
        st = ns["frontier"](rows, True)["status"]
        mine, ncl = solve(list(rows))
        cmp["attachments"] += 1
        te = st.startswith("EXCLUDED")
        if te and not mine: cmp["both_excluded"] += 1
        elif not te and mine: cmp["both_open"] += 1
        elif te and mine: cmp["theirs_excluded_mine_SAT"] += 1; details.append([bi, a, st])
        else: cmp["theirs_open_mine_UNSAT"] += 1; details.append([bi, a, st])
print(json.dumps({"core": ci, "boundaries": sel, **cmp, "discrepancies": details[:10], "sec": round(time.time() - t0, 1)}))
