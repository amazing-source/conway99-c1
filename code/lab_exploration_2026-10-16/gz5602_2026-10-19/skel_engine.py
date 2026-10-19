"""General skeleton engine for one c3 template with a forced shared pair (LAB 19/10/2026).
Normal form: the pair H_ab = -H_ac (both non-grid) becomes H01 = -H02; the four other lines become 3..6.
KNOWN rectangles: the core Q01 + Q02 and EVERY grid of the template.  Forced known-known structure (srg(99,14,1,2),
grid = perfect domination z_w(F) = base(w, F), and z_w(01) + z_w(02) = base(w,01) + base(w,02)):
  * core: 2-regular graph on its 8 labels (one of the 114 labelled cores, taken up to letter flips of lines 0,1,2);
  * grid F off {0,1,2} (Y-grid): each label sees a core pair, the 4 pairs partition the core (Codex's catalogue,
    with its forced corner oppositions);
  * grid F through line 1 but not 0, 2 (B): perfect matching F <-> Q02; through 2 but not 0, 1 (C): F <-> Q01;
    grid through line 0, or F = Q12: no core edge;
  * two disjoint grids: perfect matching; two grids sharing a line: no edge.
DFS over all these matchings with pruning by C2 on known pairs (common known neighbours <= 2 - adj - shared letters)
and known letter quotas.  For every complete skeleton: exact SAT on the known-outside adjacency y(q, v):
  * per outside label q and known rectangle F: exactly base(q, F) neighbours (core: base(q,01) + base(q,02));
  * known pairs: number of outside common neighbours = 2 - adj - shared - common known (exact);
  * known letters: exact quotas; template relations at known rows (blocks sum_{j in P} H_aj = 0 and forced two-term
    relations H_A = -H_B, H_A = H_B) give exact counts of outside neighbours;
  * outside rows: common known neighbours with a known v <= 2 - adj - shared; letter quotas <= ; outside pairs:
    common known neighbours <= 2 - shared letters.
UNSAT is RUP-checked (Codex's check_rup).  EXCLUDED_TEMPLATE means: every core type, every skeleton refuted.
usage: python skel_engine.py <codex dir> <catalogue.json.gz> <paircores8.json> <index> [a,b,c] [--limit-leaves=N]"""
import gzip
import json
import sys
import time
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product

codex = sys.argv[1]
sys.path.insert(0, codex)

if sys.platform == "win32":
    # PySAT opens one C stdio stream per solver created with a proof and never fcloses it; the Windows CRT allows 512
    # streams by default ("Cannot create proof file pointer" after ~509 solvers).  Raise the limit (max 8192).
    import ctypes as _ct
    _ct.cdll.ucrtbase._setmaxstdio(8192)
from root_component_shared_k3_boundary import matching_catalogue          # noqa: E402

recs = json.load(gzip.open(sys.argv[2]))["open"]
CORES = json.load(open(sys.argv[3]))
IDX = int(sys.argv[4])
PAIR = tuple(int(x) for x in sys.argv[5].split(",")) if len(sys.argv) > 5 and not sys.argv[5].startswith("--") else None
LIMIT = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--limit-leaves=")), 10 ** 9))
VERBOSE = "--verbose" in sys.argv
t = recs[IDX]["template"]
RECT = list(combinations(range(7), 2)); ridx = {q: i for i, q in enumerate(RECT)}
ng0 = {tuple(e) for e in t["nongrid_edges"]}


# ---------- exact kernel W and forced two-term relations (as in two_term_relations.py) ----------
def W_rows(ng, blocks):
    rows = []
    for q in RECT:
        if q not in ng:
            v = [0] * 21; v[ridx[q]] = 1; rows.append(v)
    for a, groups in enumerate(blocks):
        for P in groups:
            v = [0] * 21
            for j in P:
                v[ridx[tuple(sorted((a, j)))]] = 1
            rows.append(v)
    return rows


def rref(rows):
    rows = [[Fraction(x) for x in r] for r in rows]; piv = []; r = 0
    for c in range(21):
        p = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]; rows[r] = [x / rows[r][c] for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c]; rows[i] = [x - f * y for x, y in zip(rows[i], rows[r])]
        piv.append(c); r += 1
    return rows[:r], piv


def in_W(B, v):
    rows, piv = B; v = [Fraction(x) for x in v]
    for row, c in zip(rows, piv):
        if v[c] != 0:
            f = v[c]; v = [x - f * y for x, y in zip(v, row)]
    return all(x == 0 for x in v)


B0 = rref(W_rows(ng0, t["nontrivial_component_groups"]))
assert 21 - len(B0[0]) == t["kernel_dimension"]
if PAIR is None:                                   # first forced shared pair with both rectangles non-grid
    for a in range(7):
        for b, c in combinations([x for x in range(7) if x != a], 2):
            A_, B_ = tuple(sorted((a, b))), tuple(sorted((a, c)))
            if A_ in ng0 and B_ in ng0:
                v = [0] * 21; v[ridx[A_]] = 1; v[ridx[B_]] = 1
                if in_W(B0, v):
                    PAIR = (a, b, c); break
        if PAIR:
            break
assert PAIR, "no forced shared pair"
a0, b0, c0 = PAIR
D = [x for x in range(7) if x not in PAIR]
LMAP = {a0: 0, b0: 1, c0: 2, **{d: 3 + i for i, d in enumerate(D)}}          # template line -> normal line


def nrect(q):
    return tuple(sorted((LMAP[q[0]], LMAP[q[1]])))


ng = {nrect(q) for q in ng0}
blocks = [[] for _ in range(7)]
for a, groups in enumerate(t["nontrivial_component_groups"]):
    for P in groups:
        blocks[LMAP[a]].append(sorted(LMAP[j] for j in P))
B = rref(W_rows(ng, blocks))
v = [0] * 21; v[ridx[(0, 1)]] = 1; v[ridx[(0, 2)]] = 1
assert (0, 1) in ng and (0, 2) in ng and in_W(B, v), "pair not forced in normal form"
grids = [q for q in RECT if q not in ng]
GSEL = next((a_.split("=")[1] for a_ in sys.argv if a_.startswith("--grids=")), None)
if GSEL is not None:                     # restrict the KNOWN grids (normal-form names), for controls only
    keep = {tuple(int(c) for c in g) for g in GSEL.split(",") if g}
    assert keep <= set(grids), (keep, grids)
    grids = [q for q in grids if q in keep]
NOREL = "--no-rel" in sys.argv
# relations used at known rows: block relations and forced two-term relations (+-1 coefficients)
REL = []
for a in range(7):
    for P in blocks[a]:
        REL.append({tuple(sorted((a, j))): 1 for j in P})
for A, Bq in combinations(sorted(ng), 2):
    for sg in (1, -1):
        w = [0] * 21; w[ridx[A]] = 1; w[ridx[Bq]] = sg
        if in_W(B, w):
            REL.append({A: 1, Bq: sg})
if NOREL:
    REL = []

# ---------- labels ----------
KR = [(0, 1), (0, 2)] + [F for F in grids]           # known rectangles; core first
LAB = []                                               # known labels (letters), 4 per known rectangle, corner 2s+t
for (i, j) in KR:
    for s, u in product(range(2), repeat=2):
        LAB.append((2 * i + s, 2 * j + u))
NK = len(LAB)
krect = [KR[k // 4] for k in range(NK)]
OUTR = [q for q in RECT if q not in KR]
OUT = [(2 * i + s, 2 * j + u) for (i, j) in OUTR for s, u in product(range(2), repeat=2)]
orect = [OUTR[k // 4] for k in range(len(OUT))]


def base(q, f):
    return 2 if q == f else (0 if set(q) & set(f) else 1)


def shared(x, y):
    return len(set(x) & set(y))


SHK = [[shared(LAB[u], LAB[v]) for v in range(NK)] for u in range(NK)]
LM = [sum(1 << k for k in range(NK) if l in LAB[k]) for l in range(14)]
QUOTA = [[2 - int(l in LAB[u]) - int((l ^ 1) in LAB[u]) for l in range(14)] for u in range(NK)]
gidx = {F: KR.index(F) for F in KR}


def kind(F):
    s = set(F)
    if F in ((0, 1), (0, 2)):
        return "core"
    if not s & {0, 1, 2}:
        return "Y"
    if 0 in s or s == {1, 2}:
        return "none"
    return "B" if 1 in s else "C"


# ---------- skeleton DFS ----------
def flips_canon(core):
    """canonical form of a labelled core under letter flips of lines 0, 1, 2 (always symmetries)"""
    best = None
    core_labels = LAB[:8]
    look = {q: i for i, q in enumerate(core_labels)}
    for f in product(range(2), repeat=3):
        p = [look[tuple(sorted((x ^ f[x // 2]) for x in q))] for q in core_labels]
        e = tuple(sorted(tuple(sorted((p[u], p[v]))) for u, v in core["edges"]))
        best = e if best is None or e < best else best
    return best


def core_reps():
    seen = {}
    for ci, c in enumerate(CORES):
        k = flips_canon(c)
        seen.setdefault(k, ci)
    return sorted(seen.values())


def bits(m):
    while m:
        b = m & -m
        yield b.bit_length() - 1
        m ^= b


def check(rows):
    for u in range(NK):
        ru = rows[u]
        if ru.bit_count() > 12:
            return False
        for l in range(14):
            if (ru & LM[l]).bit_count() > QUOTA[u][l]:
                return False
        for v in range(u + 1, NK):
            if (ru & rows[v]).bit_count() > 2 - ((ru >> v) & 1) - SHK[u][v]:
                return False
    return True


def skeletons(core):
    rows = [0] * NK

    def edge(r, u, v):
        r[u] |= 1 << v; r[v] |= 1 << u
    for u, v in core["edges"]:
        edge(rows, u, v)
    for g, F in enumerate(KR):
        if g >= 2:
            off = 4 * g
            for i, j in combinations(range(4), 2):
                if i ^ j != 3:
                    edge(rows, off + i, off + j)
    if not check(rows):
        return
    steps = []
    cat = matching_catalogue(core)
    for g, F in enumerate(KR):
        k = kind(F)
        if k == "Y":
            steps.append(("Y", g))
        elif k == "B":
            steps.append(("M", g, 1))            # matched with Q02 (rectangle index 1)
        elif k == "C":
            steps.append(("M", g, 0))            # matched with Q01
    for g, h in combinations(range(2, len(KR)), 2):
        if not set(KR[g]) & set(KR[h]):
            steps.append(("M", g, h))
    P4 = list(permutations(range(4)))

    def rec(i, rows):
        if i == len(steps):
            yield rows
            return
        st = steps[i]
        if st[0] == "Y":
            off = 4 * st[1]
            for entry in cat:
                for lay in entry["layouts"]:
                    r = rows[:]
                    for c, mask in enumerate(lay):
                        for u in bits(mask):
                            edge(r, off + c, u)
                    if check(r):
                        yield from rec(i + 1, r)
        else:
            _, g, h = st
            for p in P4:
                r = rows[:]
                for c in range(4):
                    edge(r, 4 * g + c, 4 * h + p[c])
                if check(r):
                    yield from rec(i + 1, r)
    yield from rec(0, rows)


def check_new(rows, new_edges):
    """incremental version of check(): only the vertices and pairs whose degree, letter count, common-neighbour count or
    bound can have changed when the edges new_edges were added (exactly the same verdict as check() on a state that
    passed check() before the addition)"""
    touched = set()
    for x, y in new_edges:
        touched.add(x); touched.add(y)
    for z in touched:
        rz = rows[z]
        if rz.bit_count() > 12:
            return False
        for l in range(14):
            if (rz & LM[l]).bit_count() > QUOTA[z][l]:
                return False
    for x, y in new_edges:
        rx, ry = rows[x], rows[y]
        if (rx & ry).bit_count() > 1 - SHK[x][y]:
            return False
        for w in bits(rx):                     # x is a new common neighbour of y and w
            if w != y and (ry & rows[w]).bit_count() > 2 - ((ry >> w) & 1) - SHK[y][w]:
                return False
        for w in bits(ry):
            if w != x and (rx & rows[w]).bit_count() > 2 - ((rx >> w) & 1) - SHK[x][w]:
                return False
    return True


def skeletons_mrv(core, stats):
    """same skeleton set as skeletons(core), explored most-constrained-step first with forward checking"""
    rows = [0] * NK

    def edge(r, u, v):
        r[u] |= 1 << v; r[v] |= 1 << u
    for u, v in core["edges"]:
        edge(rows, u, v)
    for g, F in enumerate(KR):
        if g >= 2:
            off = 4 * g
            for i, j in combinations(range(4), 2):
                if i ^ j != 3:
                    edge(rows, off + i, off + j)
    if not check(rows):
        return
    steps = []
    cat = matching_catalogue(core)
    for g, F in enumerate(KR):
        k = kind(F)
        if k == "Y":
            steps.append(("Y", g))
        elif k == "B":
            steps.append(("M", g, 1))
        elif k == "C":
            steps.append(("M", g, 0))
    for g, h in combinations(range(2, len(KR)), 2):
        if not set(KR[g]) & set(KR[h]):
            steps.append(("M", g, h))
    P4 = list(permutations(range(4)))
    ylays = [(tuple(lay)) for entry in cat for lay in entry["layouts"]]

    def options(st, rows):
        out = []
        if st[0] == "Y":
            off = 4 * st[1]
            for lay in ylays:
                r = rows[:]; ne = []
                for c, mask in enumerate(lay):
                    for u in bits(mask):
                        edge(r, off + c, u); ne.append((off + c, u))
                if check_new(r, ne):
                    out.append(r)
        else:
            _, g, h = st
            for p in P4:
                r = rows[:]; ne = []
                for c in range(4):
                    edge(r, 4 * g + c, 4 * h + p[c]); ne.append((4 * g + c, 4 * h + p[c]))
                if check_new(r, ne):
                    out.append(r)
        return out

    def rec(rem, rows):
        stats["nodes"] += 1
        if not rem:
            yield rows
            return
        best = None
        for st in rem:
            o = options(st, rows)
            if not o:
                stats["dead_ends"] += 1
                return
            if best is None or len(o) < len(best[1]):
                best = (st, o)
                if len(o) == 1:
                    break
        nxt = [x for x in rem if x != best[0]]
        for r in best[1]:
            yield from rec(nxt, r)
    yield from rec(steps, rows)


# ---------- exact SAT on the known-outside adjacency ----------
def sat_leaf(rows):
    from pysat.card import CardEnc, EncType
    from pysat.solvers import Solver
    from root_component_shared_k3_profile_sat import check_rup, finished_proof, flush_native_proof
    top = [0]

    def new():
        top[0] += 1
        return top[0]
    cl = []
    y = {}
    for qi, q in enumerate(OUT):
        for g, F in enumerate(KR):
            n = (base(orect[qi], (0, 1)) + base(orect[qi], (0, 2))) if g < 2 else base(orect[qi], F)
            if g == 1:
                continue                               # core handled with g == 0 (both halves together)
            cand = list(range(0, 8)) if g == 0 else list(range(4 * g, 4 * g + 4))
            if n == 0:
                continue
            lits = []
            for v in cand:
                x = new(); y[(qi, v)] = x; lits.append(x)
            cl.extend(card(lits, n, new))
    # helper sets
    nb_out = {v: [qi for qi in range(len(OUT)) if (qi, v) in y] for v in range(NK)}

    def atmost(lits, bound):
        if bound < 0:
            cl.append([]); return
        if bound == 0:
            cl.extend([[-x] for x in lits]); return
        enc = CardEnc.atmost(lits=lits, bound=bound, top_id=top[0], encoding=EncType.seqcounter)
        cl.extend(enc.clauses); top[0] = max(top[0], enc.nv)
    andc = {}

    def AND(a, b):
        k = (a, b) if a < b else (b, a)
        if k not in andc:
            z = new(); andc[k] = z
            cl.extend([[-z, a], [-z, b], [z, -a, -b]])
        return andc[k]
    # known pairs: outside common neighbours exact
    for u in range(NK):
        for v in range(u + 1, NK):
            dem = 2 - ((rows[u] >> v) & 1) - SHK[u][v] - (rows[u] & rows[v]).bit_count()
            if dem < 0:
                return {"status": "EXCLUDED_NEGATIVE_KNOWN_DEFICIT"}
            qs = [qi for qi in nb_out[u] if (qi, v) in y]
            lits = [AND(y[(qi, u)], y[(qi, v)]) for qi in qs]
            if dem > len(lits):
                return {"status": "EXCLUDED_PAIR_CAPACITY"}
            if lits or dem:
                cl.extend(card(lits, dem, new))
    # known letters exact, known degree exact
    for u in range(NK):
        for l in range(14):
            dem = QUOTA[u][l] - (rows[u] & LM[l]).bit_count()
            lits = [y[(qi, u)] for qi in nb_out[u] if l in OUT[qi]]
            if dem < 0 or dem > len(lits):
                return {"status": "EXCLUDED_LETTER_CAPACITY"}
            cl.extend(card(lits, dem, new))
    # template relations at known rows: sum_F c_F (base(u,F) - z_u(F)) = 0 with z_u(F) = known + outside part
    for u in range(NK):
        for rel in REL:
            const = 0; pos = []; neg = []
            for F, cF in rel.items():
                kn = sum(1 for w in bits(rows[u]) if krect[w] == F) if F in KR else 0
                const += cF * (base(krect[u], F) - kn)
                if F not in KR:
                    lits = [y[(qi, u)] for qi in nb_out[u] if orect[qi] == F]
                    (pos if cF > 0 else neg).extend(lits)
            # sum(pos) - sum(neg) = const  <=>  sum(pos) + sum(not neg) = const + len(neg)
            lits = pos + [-x for x in neg]
            tgt = const + len(neg)
            if not lits:
                if tgt != 0:
                    return {"status": "EXCLUDED_KNOWN_ROW_RELATION"}
                continue
            if tgt < 0 or tgt > len(lits):
                return {"status": "EXCLUDED_KNOWN_ROW_RELATION"}
            cl.extend(card(lits, tgt, new))
    # outside rows
    for qi, q in enumerate(OUT):
        mine = [v for v in range(NK) if (qi, v) in y]
        for v in range(NK):
            cap = 2 - shared(q, LAB[v])
            lits = [y[(qi, w)] for w in mine if (rows[v] >> w) & 1]
            if (qi, v) in y:
                lits = lits + [y[(qi, v)]]
            if len(lits) > cap:
                atmost(lits, cap)
        for l in range(14):
            quota = 2 - int(l in q) - int((l ^ 1) in q)
            lits = [y[(qi, w)] for w in mine if l in LAB[w]]
            if len(lits) > quota:
                atmost(lits, quota)
    for qa, qb in combinations(range(len(OUT)), 2):
        cap = 2 - shared(OUT[qa], OUT[qb])
        com = [AND(y[(qa, w)], y[(qb, w)]) for w in range(NK) if (qa, w) in y and (qb, w) in y]
        if len(com) > cap:
            atmost(com, cap)
    out = {"variables": top[0], "clauses": len(cl)}

    class _L:
        clauses = cl
    with Solver(name="g3", bootstrap_with=cl, with_proof=True) as s:
        s.conf_budget(300000)
        ans = s.solve_limited()
        flush_native_proof()
        if ans is None:
            out["status"] = "UNKNOWN_SAT"
        elif ans:
            out["status"] = "SAT_KNOWN_ROWS_COMPLETE"
        else:
            proof = [ln for ln in finished_proof(s) if not ln.startswith("d ")]
            pc = check_rup(_L, proof)
            assert pc["empty_clause_verified"] is True
            out["status"] = "EXCLUDED_UNSAT_RUP"; out["proof_lines"] = len(proof)
    return out


def card(lits, t_, new):
    """exactly t_ of lits, unary counter defined in both directions (exact encoding)"""
    n = len(lits)
    if t_ < 0 or t_ > n:
        return [[]]
    if t_ == 0:
        return [[-x] for x in lits]
    if t_ == n:
        return [[x] for x in lits]
    K = t_ + 1
    cl = []; prev = {}
    for i, x in enumerate(lits):
        cur = {}
        for j in range(1, min(i + 1, K) + 1):
            v = new(); cur[j] = v
            a = prev.get(j); b = prev.get(j - 1) if j > 1 else True
            if a is not None:
                cl.append([-a, v])
            if b is True:
                cl.append([-x, v])
            elif b is not None:
                cl.append([-x, -b, v])
            cl.append([-v, x] + ([a] if a is not None else []))
            if b is not True:
                cl.append([-v] + ([a] if a is not None else []) + ([b] if b is not None else []))
        prev = cur
    cl.append([prev[t_]])
    if K in prev:
        cl.append([-prev[K]])
    return cl


t0 = time.process_time()
summary = {"index": IDX, "pair": PAIR, "normal_grids": ["%d%d" % F for F in grids],
           "kinds": {"%d%d" % F: kind(F) for F in KR[2:]}, "relations_at_known_rows": len(REL),
           "known_labels": NK, "outside_labels": len(OUT)}
reps = core_reps()
CSEL = next((a_.split("=")[1] for a_ in sys.argv if a_.startswith("--cores=")), None)
if CSEL is not None:                     # explicit labelled cores (controls only; NOT a complete run)
    reps = [int(x) for x in CSEL.split(",")]
    summary["cores_restricted"] = reps
summary["core_types"] = len(reps)
stat = Counter(); leaves = 0; open_leaf = None
MRV = "--mrv" in sys.argv
COUNT_ONLY = "--count-only" in sys.argv
STATS = Counter()
for ci in reps:
    for rows in (skeletons_mrv(CORES[ci], STATS) if MRV else skeletons(CORES[ci])):
        leaves += 1
        if COUNT_ONLY:
            stat["SKELETON"] += 1
            if leaves >= LIMIT:
                break
            continue
        r = sat_leaf(rows)
        stat[r["status"]] += 1
        if VERBOSE and (leaves % 200 == 1 or not r["status"].startswith("EXCLUDED")):
            print(json.dumps({"core": ci, "leaf": leaves, **{k: r[k] for k in r if k != 'rows'}}), file=sys.stderr, flush=True)
        if not r["status"].startswith("EXCLUDED"):
            open_leaf = {"core": ci, "rows": rows, **r}
            break
        if leaves >= LIMIT:
            break
    if open_leaf or leaves >= LIMIT:
        break
summary.update(leaves=leaves, statuses=dict(stat), cpu=round(time.process_time() - t0, 1), dfs=dict(STATS),
               verdict=("EXCLUDED_TEMPLATE" if not open_leaf and leaves < LIMIT else
                        ("OPEN_LEAF" if open_leaf else "LIMIT_REACHED")))
if open_leaf:
    summary["open_leaf"] = {k: open_leaf[k] for k in ("core", "status")}
print(json.dumps(summary))
