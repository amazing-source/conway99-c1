"""(py_extend_gen.py: adds the family GEN = --yr=... --extra=..., Q12 outside)
Frontier test of a shared pair core + Q12 grid + Y-grids (LAB 19/10/2026), parameterised version of Codex's
root_component_shared_k3_extend.py (main 30d68c38): family K3 (Y-grids 45, 46, 56; must reproduce Codex's verdicts)
or P3 (Y-grids 45, 46; Q56 becomes an outside rectangle).
Known part: core Q01+Q02 (0..7), Q12 (8..11), Y-grid labels (12..).  Each outside label q has a FORCED number of known
neighbours: base(q,01)+base(q,02) in the core (H01 = -H02), one in Q12 if q avoids the lines 1, 2 (domination), one in
each known Y-grid disjoint from q (domination), none elsewhere among the known vertices.  Its 'profile' is the set of
these known neighbours.  Exact necessary conditions (as in Codex's code, here written in their general form):
  * attachments: Q12 colour factors of the deficit T (colourings), rainbow bijections Y-grid -> colours, distinct
    pairs per colour across grids, C2 between two Y labels of the same colour, forbidden triples with a common letter;
  * known-pair deficits: 2 - adjacency - shared letters - common known neighbours, to be supplied by outside labels;
  * known-vertex letter deficits: quota (1 at each letter of an own line, 2 otherwise) minus known neighbours;
  * per outside label: profile vertices with letter quota left, pairwise unsaturated, C2 between the new label and every
    known vertex (common known neighbours + shared letters <= 2 - adjacency), and the new label's own letter quota;
  * pair capacity and exact cardinality propagation over all outside labels (Codex's propagate_profiles, generalised).
usage: python py_extend.py <codex dir> <K3|P3> <boundary file core_XXX.json.gz> <start> <count> [--no-propagate]
       [--inclusion] [--outside-c2] [--sat [--plant]] [--global]"""
import gzip
import json
import sys
import time
from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations, product

codex, FAMILY, bpath, START, COUNT = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
if sys.flags.optimize:
    raise SystemExit("refusing to run with python -O: proof checks (check_rup, verdict checks) are assert statements")
PROPAGATE = "--no-propagate" not in sys.argv
sys.path.insert(0, codex)

if sys.platform == "win32":
    # PySAT opens one C stdio stream per solver created with a proof and never fcloses it; the Windows CRT allows 512
    # streams by default ("Cannot create proof file pointer" after ~509 solvers).  Raise the limit (max 8192).
    import ctypes as _ct
    _ct.cdll.ucrtbase._setmaxstdio(8192)
from root_component_shared_core_colors import PAIRS, PAIR_ID, colourings          # noqa: E402
from root_component_shared_k3_boundary import matching_catalogue                  # noqa: E402

def _grids(opt):
    v = next((x.split("=", 1)[1] for x in sys.argv if x.startswith(opt)), "")
    return tuple(tuple(sorted((int(g[0]), int(g[1])))) for g in v.split(",") if g)


if FAMILY == "GEN":
    YR = _grids("--yr=")
    EXTRA = _grids("--extra=")
    assert YR and all(not set(F) & {0, 1, 2} for F in YR), YR
    assert all((1 in F) != (2 in F) and 0 not in F for F in EXTRA), EXTRA      # B/C grids only
else:
    YR = {"K3": ((4, 5), (4, 6), (5, 6)), "P3": ((4, 5), (4, 6)), "P3N": ((4, 5), (4, 6)), "K2": ((4, 5),),
          "2K2": ((3, 4), (5, 6)), "2K2N": ((3, 4), (5, 6)), "P3NB": ((4, 5), (4, 6))}[FAMILY]
    EXTRA = ((1, 3),) if FAMILY == "P3NB" else ()
YY = FAMILY in ("2K2", "2K2N")
assert FAMILY != "GEN" or not any(not set(F) & set(G) for F, G in __import__("itertools").combinations(YR, 2)),     "GEN: disjoint Y-grids not supported (use 2K2/2K2N)"       # two DISJOINT Y-grids: a perfect matching between them (each dominates the other)
Q12K = FAMILY not in ("P3N", "2K2N", "P3NB", "GEN")          # P3N: Q12 NOT assumed to be a grid (it is an outside rectangle), no attachments
YOFF = 12 if Q12K else 8
NG = len(YR)
# P3NB: an extra known B-grid Q13 (through b = 1 and the free line 3): perfect matching with the core half Q02
# (base(01,13) = 0, base(02,13) = 1) and with both Y-grids (disjoint): attachments (beta, s1, s2) in S4^3
BG = EXTRA[0] if EXTRA else None             # kept for the P3NB code path (single extra grid)
RECT = (((0, 1), (0, 2), (1, 2)) if Q12K else ((0, 1), (0, 2))) + YR + EXTRA
BOFF = YOFF + 4 * len(YR)
EOFF = [BOFF + 4 * i for i in range(len(EXTRA))]
LABELS = tuple((2 * a + s, 2 * b + t) for a, b in RECT for s, t in product(range(2), repeat=2))
NK = len(LABELS)
SHARED = tuple(tuple(len(set(a) & set(b)) for b in LABELS) for a in LABELS)
LETTER_MASKS = tuple(sum(1 << i for i, q in enumerate(LABELS) if l in q) for l in range(14))
KNOWN_RECTS = set(RECT)
OUT_RECTS = [q for q in combinations(range(7), 2) if q not in KNOWN_RECTS]
OUTSIDE = tuple((2 * a + s, 2 * b + t) for a, b in OUT_RECTS for s, t in product(range(2), repeat=2))
P4 = tuple(permutations(range(4)))


def base(q, f):
    return 2 if q == f else (0 if set(q) & set(f) else 1)


@lru_cache(None)
def profiles(q):
    lines = {l // 2 for l in q}
    rect = tuple(sorted(lines))
    ncore = base(rect, (0, 1)) + base(rect, (0, 2))
    parts = []
    core_choices = list(combinations(range(8), ncore))
    q12 = [()] if (lines & {1, 2} or not Q12K) else [(v,) for v in range(8, 12)]
    ys = []
    for g, r in enumerate(YR):
        if not (lines & set(r)):
            ys.append([YOFF + 4 * g + c for c in range(4)])
    for i, F in enumerate(EXTRA):
        if not (lines & set(F)):
            ys.append([EOFF[i] + c for c in range(4)])
    out = []
    for cc in core_choices:
        for qq in q12:
            for yy in product(*ys):
                out.append(tuple(cc) + tuple(qq) + tuple(yy))
    return tuple(out)


def rainbow(allowed):
    return tuple(pi for pi, p in enumerate(P4) if all(allowed[p[j]] & (1 << j) for j in range(4)))


class Attachments:
    def __init__(self, core):
        _, factors = colourings(core)
        forbidden = []
        for j in range(4):
            forbidden.append(sum(1 << k for k, (u, v) in enumerate(PAIRS)
                                 if (u < 4) == (v < 4) and u % 2 == v % 2 and u % 2 == (j // 2 if u < 4 else j % 2)))
        self.factors = [fs for fs in factors if all(not (fs[j] & forbidden[j]) for j in range(4))]
        self.keys = [c['key'] for c in matching_catalogue(core)]
        self.index = {key: i for i, key in enumerate(self.keys)}

    def for_boundary(self, boundary):
        keys = tuple(tuple(sorted(boundary[4 * b:4 * b + 4])) for b in range(NG))
        corner = [tuple(boundary[4 * b:4 * b + 4].index(mask) for mask in keys[b]) for b in range(NG)]
        for fs in self.factors:
            opts = []
            for b in range(NG):
                ids = [PAIR_ID[tuple(v for v in range(8) if mask & (1 << v))] for mask in keys[b]]
                allowed = tuple(sum(1 << j for j in range(4) if fs[j] & (1 << k)) for k in ids)
                opts.append(rainbow(allowed))
            if any(not o for o in opts):
                continue
            for ids in product(*opts):
                choices = [tuple(keys[m][e] for e in P4[p]) for m, p in enumerate(ids)]
                if not all(len({choices[g][j] for g in range(NG)}) == NG for j in range(4)):
                    continue
                attached = tuple(tuple(corner[b][e] for e in P4[p]) for b, p in enumerate(ids))
                bad = False
                for a, b in combinations(range(NG), 2):
                    for j in range(4):
                        ia, ib = 12 + 4 * a + attached[a][j], 12 + 4 * b + attached[b][j]
                        if (boundary[4 * a + attached[a][j]] & boundary[4 * b + attached[b][j]]).bit_count() + SHARED[ia][ib] > 1:
                            bad = True; break
                    if bad:
                        break
                if not bad:
                    yield attached


def materialize(core, boundary, attached, sigma=None):
    rows = [0] * NK

    def edge(u, v):
        rows[u] |= 1 << v; rows[v] |= 1 << u
    for u, v in core['edges']:
        edge(u, v)
    for off in ([8] if Q12K else []) + [YOFF + 4 * g for g in range(NG)] + EOFF:
        for i, j in combinations(range(4), 2):
            if i ^ j != 3:
                edge(off + i, off + j)
    for k, mask in enumerate(boundary):
        for u in range(8):
            if mask & (1 << u):
                edge(u, YOFF + k)
    for b in range(NG if Q12K else 0):
        for j, k in enumerate(attached[b]):
            edge(8 + j, 12 + 4 * b + k)
    if sigma is not None:
        for c in range(4):
            edge(YOFF + c, YOFF + 4 + sigma[c])
    if FAMILY == "GEN":
        for (x0, y0), perm in zip(MATCH_BLOCKS, attached):
            for c in range(4):
                edge(x0 + c, y0 + perm[c])
    elif BG is not None:
        beta, s1, s2 = attached
        for c in range(4):
            edge(BOFF + c, 4 + beta[c]); edge(BOFF + c, YOFF + s1[c]); edge(BOFF + c, YOFF + 4 + s2[c])
    for u in range(NK):
        if FAMILY == "GEN":
            expect = EXPECT[u]
        elif BG is not None:
            expect = 4 if u < 4 else 5          # Q01: 2 core + 2 Y; Q02: + 1 B; Y: 2 + 2 core + 1 B; B: 2 + 1 core + 2 Y
        else:
            expect = ((2 + NG) if u < 12 else 5 + int(YY)) if Q12K else ((2 + NG) if u < 8 else 4 + int(YY))
        assert rows[u].bit_count() == expect, (u, rows[u].bit_count(), expect)
    return rows


def frontier(rows, propagate=True):
    deficits = [[7 if u == v else 2 - ((rows[u] >> v) & 1) - SHARED[u][v] - (rows[u] & rows[v]).bit_count()
                 for v in range(NK)] for u in range(NK)]
    if any(min(r) < 0 for r in deficits):
        return {'status': 'EXCLUDED_NEGATIVE_KNOWN_DEFICIT'}
    letter_def = [[2 - int(l in LABELS[u]) - int((l ^ 1) in LABELS[u]) - (rows[u] & LETTER_MASKS[l]).bit_count()
                   for l in range(14)] for u in range(NK)]
    if any(min(r) < 0 for r in letter_def):
        return {'status': 'EXCLUDED_NEGATIVE_LETTER_DEFICIT'}
    domains = []
    for qi, q in enumerate(OUTSIDE):
        good = []
        allowed = [all(letter_def[v][l] > 0 for l in q) for v in range(NK)]
        for prof in profiles(q):
            if any(not allowed[v] for v in prof):
                continue
            if any(not deficits[u][v] for u, v in combinations(prof, 2)):
                continue
            mask = sum(1 << v for v in prof)
            if any((rows[v] & mask).bit_count() > 2 - int(v in prof) - len(set(q) & set(LABELS[v])) for v in range(NK)):
                continue
            if any((mask & LETTER_MASKS[l]).bit_count() > 2 - int(l in q) - int((l ^ 1) in q) for l in range(14)):
                continue
            good.append(prof)
        if not good:
            return {'status': 'EXCLUDED_EMPTY_VERTEX_DOMAIN', 'outside_index': qi, 'outside_letters': q}
        domains.append(good)
    # pair capacity
    W = NK
    mn = Counter(); mx = Counter()
    for dom in domains:
        sets = [set((min(u, v), max(u, v)) for u, v in combinations(p, 2)) for p in dom]
        uni = set().union(*sets); inter = set.intersection(*sets) if sets else set()
        for k in uni:
            mx[k] += 1
        for k in inter:
            mn[k] += 1
    for u in range(W):
        for v in range(u + 1, W):
            if not (mn[(u, v)] <= deficits[u][v] <= mx[(u, v)]):
                return {'status': 'EXCLUDED_PROFILE_CAPACITY', 'known_vertices': [u, v], 'demand': deficits[u][v],
                        'minimum': mn[(u, v)], 'maximum': mx[(u, v)]}
    if not propagate:
        return {'status': 'PASSES_PAIR_CAPACITY', 'domain_sizes': [len(d) for d in domains]}
    # exact cardinality propagation (pairs and letters), as Codex's propagate_profiles
    demands = {}
    for u in range(W):
        for v in range(u + 1, W):
            demands[('p', u, v)] = deficits[u][v]
        for l in range(14):
            demands[('l', u, l)] = letter_def[u][l]
    feats = []
    for q, dom in zip(OUTSIDE, domains):
        fl = []
        for p in dom:
            f = set(('p', min(a, b), max(a, b)) for a, b in combinations(p, 2))
            f |= set(('l', u, l) for u in p for l in q)
            fl.append(frozenset(f))
        feats.append(fl)
    active = [list(range(len(d))) for d in domains]
    while True:
        lower = Counter(); upper = Counter(); bounds = []
        for vi, idx in enumerate(active):
            uni = set(); inter = None
            for i in idx:
                f = feats[vi][i]; uni |= f; inter = set(f) if inter is None else inter & f
            inter = inter or set()
            bounds.append((uni, inter))
            for k in uni:
                upper[k] += 1
            for k in inter:
                lower[k] += 1
        for k, tgt in demands.items():
            if not (lower[k] <= tgt <= upper[k]):
                return {'status': 'EXCLUDED_PROFILE_PROPAGATION', 'feature': list(k), 'demand': tgt,
                        'minimum': lower[k], 'maximum': upper[k]}
        tight_lo = {k for k, t in demands.items() if lower[k] == t}
        tight_up = {k for k, t in demands.items() if upper[k] == t}
        changed = False
        for vi, (uni, inter) in enumerate(bounds):
            optional = uni - inter
            forb = optional & tight_lo; req = optional & tight_up
            kept = [i for i in active[vi] if not (feats[vi][i] & forb) and req <= feats[vi][i]]
            if not kept:
                return {'status': 'EXCLUDED_PROFILE_PROPAGATION', 'outside_index': vi, 'reason': 'tight bounds'}
            if len(kept) < len(active[vi]):
                active[vi] = kept; changed = True
        if not changed and INCLUSION:
            r = inclusion_step(active, feats, demands)
            if r is not None and r.get('status', '').startswith('EXCLUDED'):
                return r
            if r is not None and r.get('changed'):
                changed = True
        if not changed and OUTSIDE_C2:
            # two outside labels a, b have at most 2 - |shared letters| common neighbours, hence at most that many
            # common KNOWN neighbours (Codex's outside C2 filter); arc consistency over all pairs
            masks = [[sum(1 << v for v in domains[vi][i]) for i in range(len(domains[vi]))] for vi in range(len(domains))]
            for a, b in combinations(range(len(OUTSIDE)), 2):
                cap = 2 - len(set(OUTSIDE[a]) & set(OUTSIDE[b]))
                for x, y in ((a, b), (b, a)):
                    kept = [i for i in active[x] if any((masks[x][i] & masks[y][j]).bit_count() <= cap for j in active[y])]
                    if not kept:
                        return {'status': 'EXCLUDED_OUTSIDE_PROFILE_C2', 'outside_vertices': [x, y]}
                    if len(kept) < len(active[x]):
                        active[x] = kept; changed = True
        if not changed:
            if DUMP is not None and len(DUMPED) < DUMP_MAX:
                DUMPED.append({'family': FAMILY, 'known_labels': [list(l) for l in LABELS], 'rows': rows,
                               'outside_labels': [list(q) for q in OUTSIDE],
                               'domains_after_propagation': [[list(domains[vi][i]) for i in active[vi]]
                                                             for vi in range(len(domains))],
                               'pair_deficits': deficits, 'letter_deficits': letter_def,
                               'note': 'pair_deficits[u][u] is a placeholder (7); outside degree = 12 - popcount(rows[u])'})
            if SAT:
                return profile_sat(domains, active, deficits, letter_def, rows)
            if GLOBAL:
                return global_selection(domains, active, feats, demands)
            return {'status': 'PASSES_PROFILE_PROPAGATION', 'domain_sizes': [len(a) for a in active]}


INCLUSION = "--inclusion" in sys.argv


def inclusion_step(active, feats, demands):
    """Inclusion propagation (Codex, main d29b018a): if every remaining option (over all outside labels) carrying the
    feature e also carries f, the exact totals satisfy t_e <= t_f; if t_e = t_f, every chosen option carrying f also
    carries e, so the options with f and without e are removed.  Exact; no search."""
    occ = {}
    pos = 0
    index = []
    for vi, idx in enumerate(active):
        for i in idx:
            for k in feats[vi][i]:
                occ[k] = occ.get(k, 0) | (1 << pos)
            index.append((vi, i)); pos += 1
    keys = [k for k in demands if k in occ]
    removed = set()
    for e in keys:
        oe = occ[e]
        for f in keys:
            if e == f:
                continue
            of = occ[f]
            if oe & ~of:
                continue                       # some option carries e without f
            if demands[e] > demands[f]:
                return {'status': 'EXCLUDED_INCLUSION', 'e': list(e), 'f': list(f), 't_e': demands[e], 't_f': demands[f]}
            if demands[e] == demands[f]:
                extra = of & ~oe
                while extra:
                    b = extra & -extra; extra ^= b
                    removed.add(index[b.bit_length() - 1])
    if not removed:
        return {'changed': False}
    for vi in range(len(active)):
        kept = [i for i in active[vi] if (vi, i) not in removed]
        if not kept:
            return {'status': 'EXCLUDED_INCLUSION', 'outside_index': vi, 'reason': 'all options removed'}
        active[vi] = kept
    return {'changed': True}


GLOBAL = "--global" in sys.argv


def global_selection(domains, active, feats, demands):
    """Exact profile selection: one profile per outside label, every known-pair and known-letter demand met exactly
    (they are exact counts).  CP-SAT on a small 0/1 model; INFEASIBLE excludes the partial configuration."""
    from ortools.sat.python import cp_model
    m = cp_model.CpModel()
    x = {}
    for vi, idx in enumerate(active):
        vs = [m.NewBoolVar("") for _ in idx]
        m.AddExactlyOne(vs)
        for i, v in zip(idx, vs):
            x[(vi, i)] = v
    occ = {}
    for (vi, i), v in x.items():
        for k in feats[vi][i]:
            occ.setdefault(k, []).append(v)
    for k, tgt in demands.items():
        m.Add(sum(occ.get(k, [])) == tgt)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 60; s.parameters.num_search_workers = 1
    st = s.StatusName(s.Solve(m))
    if st == 'INFEASIBLE':
        return {'status': 'EXCLUDED_GLOBAL_SELECTION'}
    return {'status': 'PASSES_GLOBAL_SELECTION' if st in ('FEASIBLE', 'OPTIMAL') else 'UNKNOWN_GLOBAL_SELECTION'}


SAT = "--sat" in sys.argv
VERBOSE = "--verbose" in sys.argv
DISSECT = "--dissect" in sys.argv
LEAN = "--lean" in sys.argv
ALLATT = "--all-attachments" in sys.argv
DUMP = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--dump=")), None)
DUMP_MAX = 12
DUMPED = []
SOLVER = next((a.split("=")[1] for a in sys.argv if a.startswith("--solver=")), "g3")
OUTSIDE_C2 = SAT or "--outside-c2" in sys.argv
PLANT = "--plant" in sys.argv          # positive control: demands recomputed from a planted selection


def rect_of(lab):
    return tuple(sorted((lab[0] // 2, lab[1] // 2)))


# Exact redundant region counts on the known rows.  Each is sum_{F in R} H_F = 0 with R made of outside rectangles
# only, so for a known label u: #(outside neighbours of u in R) = sum_{F in R} base(rect(u), F).
#   Z : H03+H04+H05+H06 = 0  (root 0 and H01 = -H02), both families;
#   N : K3: H34+H35+H36 = 0 ; P3: H34+H35+H36+H56 = 0  (root 3 minus the bipartition relation {0,1,2,3}|{4,5,6}:
#       H03+H13+H23 = H45+H46+H56, with H01+H02 = 0, H12 = 0 and the Y-grids zero).
REGIONS = {'Z': ((0, 3), (0, 4), (0, 5), (0, 6)),
           'N': {"K3": ((3, 4), (3, 5), (3, 6)), "P3": ((3, 4), (3, 5), (3, 6), (5, 6)), "P3N": ((3, 4), (3, 5), (3, 6), (5, 6)),
                 # K2 (only Q45 a Y-grid): bipartition gives H03+H13+H23 = H46+H56, root 3 gives H34+H35+H36+H46+H56 = 0
                 "K2": ((3, 4), (3, 5), (3, 6), (4, 6), (5, 6)),
                 # 2K2 (Q12, Q34, Q56 grids): bipartition gives H03+H13+H23 = H45+H46, root 3 (H34 = 0) gives
                 # H35+H36+H45+H46 = 0
                 "2K2": ((3, 5), (3, 6), (4, 5), (4, 6)), "2K2N": (), "P3NB": (), "GEN": ()}[FAMILY]}
if not Q12K:
    del REGIONS['N']          # no 0/1 region relation without H12 = 0          # P3N: H34+H35+H36+H56 = H12 (not a 0/1 region relation); Z still holds
for _R in REGIONS.values():
    assert all(F in OUT_RECTS for F in _R)


class Pool:
    def __init__(self):
        self.top = 0

    def new(self):
        self.top += 1
        return self.top


def exactly(lits, t, pool):
    """CNF for sum(lits) = t: unary sequential counter s[i][j] <=> 'at least j of lits[:i+1] are true' (j <= t+1),
    defined in BOTH directions (so the encoding is exact and every assignment of lits extends uniquely), then s[n-1][t]
    and not s[n-1][t+1].  About 4 n (t+1) clauses (pysat's seqcounter 'atleast' costs O(n (n-t)))."""
    n = len(lits)
    if t < 0 or t > n:
        return [[]]
    if t == 0:
        return [[-x] for x in lits]
    if t == n:
        return [[x] for x in lits]
    K = t + 1
    cl = []
    prev = {}                       # j -> literal of s[i-1][j]; j = 0 is TRUE (absent), j > i is FALSE (absent)
    for i, x in enumerate(lits):
        cur = {}
        for j in range(1, min(i + 1, K) + 1):
            v = pool.new(); cur[j] = v
            a = prev.get(j)                       # s[i-1][j] (None = false)
            b = prev.get(j - 1) if j > 1 else True  # s[i-1][j-1] (True for j = 1)
            # v <= a
            if a is not None:
                cl.append([-a, v])
            # v <= x & b
            if b is True:
                cl.append([-x, v])
            elif b is not None:
                cl.append([-x, -b, v])
            # v => a | x
            cl.append([-v, x] + ([a] if a is not None else []))
            # v => a | b
            if b is not True:
                cl.append([-v] + ([a] if a is not None else []) + ([b] if b is not None else []))
        prev = cur
    cl.append([prev[t]])
    if K in prev:
        cl.append([-prev[K]])
    return cl


def profile_sat(domains, active, deficits, letter_def, rows, conflicts=int(next((a.split("=")[1] for a in sys.argv if a.startswith("--conflicts=")), 200000))):
    """Exact joint selection (Codex's root_component_shared_k3_profile_sat model, written for both families): one
    profile per outside label; every known-pair count (u <= v, u = v being the outside degree) and every known-letter
    count exact; region counts Z, N exact; outside pairs: common known neighbours <= 2 - shared letters.
    No outside-outside adjacency variables: SAT means only that all known rows can be completed."""
    from pysat.formula import CNF, IDPool
    from pysat.card import CardEnc, EncType
    from pysat.solvers import Solver
    from root_component_shared_k3_profile_sat import check_rup, finished_proof
    try:
        from root_component_shared_k3_profile_sat import flush_native_proof
    except ImportError:                       # older Codex snapshot
        flush_native_proof = None
    t0 = time.process_time()
    doms = [[domains[vi][i] for i in active[vi]] for vi in range(len(domains))]
    vp = IDPool(); feat = {}; rows_v = []
    for qi, (q, dom) in enumerate(zip(OUTSIDE, doms)):
        row = []
        reg = [k for k, R in REGIONS.items() if rect_of(q) in R]
        for pi, p in enumerate(dom):
            x = vp.id(('x', qi, pi)); row.append(x)
            for i, u in enumerate(p):
                for v in p[i:]:
                    feat.setdefault(('p', u, v), []).append(x)
                for l in q:
                    feat.setdefault(('l', u, l), []).append(x)
                for k in reg:
                    feat.setdefault((k, u), []).append(x)
        rows_v.append(row)
    planted = None
    if PLANT:
        import random
        rnd = random.Random(12345)
        planted = [rnd.randrange(len(d)) for d in doms]
    targets = {}
    for u in range(NK):
        for v in range(u, NK):
            if u == v:
                targets[('p', u, u)] = 12 - rows[u].bit_count()          # outside degree (degree 14 = 2 letters + 12)
            else:
                targets[('p', u, v)] = deficits[u][v]
        for l in range(14):
            targets[('l', u, l)] = letter_def[u][l]
        for k, R in REGIONS.items():
            targets[(k, u)] = sum(base(rect_of(LABELS[u]), F) for F in R)
    if planted is not None:
        chosen = {rows_v[qi][pi] for qi, pi in enumerate(planted)}
        targets = {k: sum(1 for x in feat.get(k, []) if x in chosen) for k in targets}
    ENCNAME = next((a.split('=')[1] for a in sys.argv if a.startswith('--enc=')), 'own')
    ENC = {'seq': EncType.seqcounter, 'tot': EncType.totalizer, 'kmt': EncType.kmtotalizer,
           'sn': EncType.sortnetwrk, 'cn': EncType.cardnetwrk, 'own': None}[ENCNAME]
    groups = {}

    allcl = []
    pool = Pool(); pool.top = vp.top if hasattr(vp, 'top') else 0
    pool.top = max(x for row in rows_v for x in row) if rows_v else 0
    CUSTOM = ENCNAME == 'own'

    def add(g, clauses):
        if DISSECT:
            groups.setdefault(g, []).extend(clauses)
        allcl.extend(clauses)

    def card(lits, t):
        if CUSTOM:
            return exactly(lits, t, pool)
        if t < 0 or t > len(lits):
            return [[]]
        if t == 0:
            return [[-x] for x in lits]
        if t == len(lits):
            return [[x] for x in lits]
        vp.occupy(1, pool.top)
        c = CardEnc.equals(lits=lits, bound=t, vpool=vp, encoding=ENC).clauses
        pool.top = max(pool.top, vp.top)
        return c
    for qi, row in enumerate(rows_v):
        add(('one', qi), card(row, 1))
    for k, t in targets.items():
        lits = feat.get(k, [])
        if not lits and t == 0:
            continue
        if LEAN and (k[0] in REGIONS or (k[0] == 'p' and k[1] == k[2])):
            continue      # implied: degree = (1/2) sum of the letter counts; Z = two letter counts; N = (1/2)(L3+L4+L5+L6-L0-L1-L2)
        add(('T',) + k, card(lits, t))
    import numpy as np
    masks = [np.array([sum(1 << v for v in p) for p in d], dtype=np.uint32) for d in doms]
    nc2 = 0
    for a, b in combinations(range(len(OUTSIDE)), 2):
        cap = 2 - len(set(OUTSIDE[a]) & set(OUTSIDE[b]))
        bad = np.bitwise_count(masks[a][:, None] & masks[b][None, :]) > cap
        if not bad.any():
            continue
        ra, rb = rows_v[a], rows_v[b]
        cls = []
        for i, j in zip(*np.nonzero(bad)):
            if planted is not None and planted[a] == i and planted[b] == j:
                continue                              # keep the planted selection admissible
            cls.append([-ra[i], -rb[j]])
        add(('C2', a, b), cls); nc2 += len(cls)
    cnf = CNF(from_clauses=allcl) if DISSECT else None
    out = {'variables': pool.top, 'clauses': len(allcl), 'outside_c2_clauses': nc2}
    if DISSECT:
        out.update(dissect(groups, pool, targets, feat, doms))
        out['status'] = 'EXCLUDED_PROFILE_SELECTION_UNSAT' if out.get('mus') is not None else 'NOT_UNSAT'
        return out
    class _L:
        clauses = allcl
    with Solver(name=SOLVER, bootstrap_with=allcl, with_proof=not PLANT) as s:
        s.conf_budget(conflicts)
        ans = s.solve_limited()
        if flush_native_proof is not None and not PLANT:
            flush_native_proof()              # never let a pending proof buffer survive into a later solver
        out['conflicts'] = s.accum_stats().get('conflicts')
        if ans is None:
            out['status'] = 'UNKNOWN_PROFILE_SAT'
        elif ans:
            out['status'] = 'SAT_KNOWN_ROWS_COMPLETE'
            model = set(x for x in s.get_model() if x > 0)
            out['selected_profiles'] = [list(doms[qi][next(i for i, x in enumerate(row) if x in model)])
                                        for qi, row in enumerate(rows_v)]
        else:
            proof = [ln for ln in finished_proof(s) if not ln.startswith('d ')]
            out['status'] = 'EXCLUDED_PROFILE_SELECTION_UNSAT'
            out['proof_check'] = check_rup(_L, proof)
            out['proof_lines'] = len(proof)
    out['cpu_seconds'] = round(time.process_time() - t0, 3)
    return out


def dissect(groups, vp, targets, feat, doms):
    """Minimal unsatisfiable set of constraint GROUPS (deletion-based, selector literals; the 'one profile per label'
    rows are hard).  Reports each group in letters: T = exact count (pair u-v, degree u-u, letter, region), C2 = pair
    of outside labels."""
    from pysat.solvers import Solver
    names = [g for g in groups if g[0] != 'one']
    sel = {g: vp.new() for g in names}            # vp is the shared Pool here (selectors above all variables)
    with Solver(name='g3') as s:
        for g, cl in groups.items():
            for c in cl:
                s.add_clause(c if g[0] == 'one' else c + [-sel[g]])
        if s.solve(assumptions=[sel[g] for g in names]):
            return {'mus': None}
        core = set(s.get_core())
        cur = [g for g in names if sel[g] in core]
        i = 0
        while i < len(cur):
            trial = cur[:i] + cur[i + 1:]
            if not s.solve(assumptions=[sel[g] for g in trial]):
                kept = set(s.get_core())
                cur = [g for g in trial if sel[g] in kept]
            else:
                i += 1
    def lab(u):
        return list(LABELS[u])
    desc = []
    for g in cur:
        if g[0] == 'T':
            k = g[1:]
            d = {'type': {'p': 'pair', 'l': 'letter', 'Z': 'regionZ', 'N': 'regionN'}[k[0]], 'target': targets[k],
                 'options': len(feat.get(k, []))}
            if k[0] == 'p':
                d.update(u=k[1], v=k[2], u_letters=lab(k[1]), v_letters=lab(k[2]))
            elif k[0] == 'l':
                d.update(u=k[1], u_letters=lab(k[1]), letter=k[2])
            else:
                d.update(u=k[1], u_letters=lab(k[1]))
            desc.append(d)
        else:
            desc.append({'type': 'C2', 'a': list(OUTSIDE[g[1]]), 'b': list(OUTSIDE[g[2]])})
    return {'mus': desc, 'mus_size': len(desc)}


# GEN matching blocks: (first vertex of A, first vertex of B), A an extra grid, B = the core half it is matched with
# (Q02 = 4..7 for a grid through b = 1, Q01 = 0..3 for a grid through c = 2) or a known grid disjoint from A
MATCH_BLOCKS = []          # order: core-half blocks, then extra-Y blocks, then extra-extra blocks (most constrained first)
for _i, _F in enumerate(EXTRA):
    MATCH_BLOCKS.append((EOFF[_i], 4 if 1 in _F else 0))
for _i, _F in enumerate(EXTRA):
    for _g, _G in enumerate(YR):
        if not set(_F) & set(_G):
            MATCH_BLOCKS.append((EOFF[_i], YOFF + 4 * _g))
for _i, _F in enumerate(EXTRA):
    for _j in range(_i + 1, len(EXTRA)):
        if not set(_F) & set(EXTRA[_j]):
            MATCH_BLOCKS.append((EOFF[_i], EOFF[_j]))


def _expected_degrees():
    """forced known degree of every known label: 2 inside its own rectangle (core 2-regular, grid 4-cycle) plus the
    forced counts towards the other known rectangles (grids: base; the core: base(.,01) + base(.,02))"""
    out = []
    for u, lab in enumerate(LABELS):
        own = tuple(sorted((lab[0] // 2, lab[1] // 2)))
        d = 2
        for F in RECT:
            if F in ((0, 1), (0, 2)):
                continue
            if F != own:
                d += base(own, F)
        if own not in ((0, 1), (0, 2)):
            d += base(own, (0, 1)) + base(own, (0, 2))
        out.append(d)
    return out


EXPECT = _expected_degrees() if FAMILY == "GEN" else None
# lines whose letter flips act ONLY on the extra grids (not on the core lines 0..2 nor on the Y-grid lines): such a flip
# is a symmetry of the whole problem fixing the boundary, so attachments in the same orbit have isomorphic known graphs
_YL = {x for F in YR for x in F}
FLIP_LINES = [l for l in range(3, 7) if l not in _YL and any(l in F for F in EXTRA)]


def _corner_map(F, flips):
    # corner c = 2 s + t of grid F = (i, j), s on line i, t on line j
    m = list(range(4))
    if F[0] in flips:
        m = [x ^ 2 for x in m]
    if F[1] in flips:
        m = [x ^ 1 for x in m]
    return m


def _block_target_rect(y0):
    if y0 < 8:
        return None                               # core half (lines 0, 1/2): unaffected
    if y0 < BOFF:
        return YR[(y0 - YOFF) // 4]
    return EXTRA[(y0 - BOFF) // 4]


def attachment_canon(att):
    best = None
    for k in range(1 << len(FLIP_LINES)):
        fl = {FLIP_LINES[i] for i in range(len(FLIP_LINES)) if k >> i & 1}
        img = []
        for (x0, y0), perm in zip(MATCH_BLOCKS, att):
            fF = _corner_map(EXTRA[(x0 - BOFF) // 4], fl)
            T = _block_target_rect(y0)
            fG = _corner_map(T, fl) if T is not None else list(range(4))
            np_ = [0] * 4
            for c in range(4):
                np_[fF[c]] = fG[perm[c]]
            img.append(tuple(np_))
        img = tuple(img)
        best = img if best is None or img < best else best
    return best
LAYER = Counter()


def gen_attachments(core, boundary):
    """all permutations of the GEN matching blocks (S4 each), pruned block by block by partial_ok (valid upper bounds);
    the final known graph is re-checked exactly by materialize() and frontier()"""
    base_rows = [0] * NK

    def edge(r, u, v):
        r[u] |= 1 << v; r[v] |= 1 << u
    for u, v in core['edges']:
        edge(base_rows, u, v)
    for off in [YOFF + 4 * g for g in range(NG)] + EOFF:
        for i, j in combinations(range(4), 2):
            if i ^ j != 3:
                edge(base_rows, off + i, off + j)
    for k, mask in enumerate(boundary):
        for u in range(8):
            if mask & (1 << u):
                edge(base_rows, u, YOFF + k)

    def rec(i, rows, chosen):
        LAYER[i] += 1
        if i == len(MATCH_BLOCKS):
            yield tuple(chosen), None
            return
        x0, y0 = MATCH_BLOCKS[i]
        for p in P4:
            r = rows[:]; ne = [(x0 + c, y0 + p[c]) for c in range(4)]
            for x, y in ne:
                edge(r, x, y)
            if partial_ok(r, ne):
                yield from rec(i + 1, r, chosen + [p])
    yield from rec(0, base_rows, [])


def partial_ok(rows, new_edges):
    """C2 / letter / degree upper bounds for the vertices and pairs affected by new_edges (exact necessary conditions:
    common known neighbours <= 2 - adj - shared letters, known letter counts <= quota, degree <= 12)"""
    touched = set()
    for x, y in new_edges:
        touched.add(x); touched.add(y)
    for z in touched:
        rz = rows[z]
        if rz.bit_count() > 12:
            return False
        for l in range(14):
            if (rz & LETTER_MASKS[l]).bit_count() > 2 - int(l in LABELS[z]) - int((l ^ 1) in LABELS[z]):
                return False
    for x, y in new_edges:
        rx, ry = rows[x], rows[y]
        if (rx & ry).bit_count() > 1 - SHARED[x][y]:
            return False
        m = rx
        while m:
            w = (m & -m).bit_length() - 1; m &= m - 1
            if w != y and (ry & rows[w]).bit_count() > 2 - ((ry >> w) & 1) - SHARED[y][w]:
                return False
        m = ry
        while m:
            w = (m & -m).bit_length() - 1; m &= m - 1
            if w != x and (rx & rows[w]).bit_count() > 2 - ((rx >> w) & 1) - SHARED[x][w]:
                return False
    return True


def p3nb_attachments(core, boundary):
    """all (beta, s1, s2) in S4^3 whose partial known graph passes the C2 / letter / degree bounds after each layer
    (the final graph is re-checked exactly by frontier())"""
    base_rows = [0] * NK

    def edge(r, u, v):
        r[u] |= 1 << v; r[v] |= 1 << u
    for u, v in core['edges']:
        edge(base_rows, u, v)
    for off in [YOFF + 4 * g for g in range(NG)] + [BOFF]:
        for i, j in combinations(range(4), 2):
            if i ^ j != 3:
                edge(base_rows, off + i, off + j)
    for k, mask in enumerate(boundary):
        for u in range(8):
            if mask & (1 << u):
                edge(base_rows, u, YOFF + k)
    for beta in P4:
        r1 = base_rows[:]; e1 = [(BOFF + c, 4 + beta[c]) for c in range(4)]
        for x, y in e1:
            edge(r1, x, y)
        if not partial_ok(r1, e1):
            continue
        for s1 in P4:
            r2 = r1[:]; e2 = [(BOFF + c, YOFF + s1[c]) for c in range(4)]
            for x, y in e2:
                edge(r2, x, y)
            if not partial_ok(r2, e2):
                continue
            for s2 in P4:
                r3 = r2[:]; e3 = [(BOFF + c, YOFF + 4 + s2[c]) for c in range(4)]
                for x, y in e3:
                    edge(r3, x, y)
                if partial_ok(r3, e3):
                    yield (beta, s1, s2), None


def solve(core, boundary, att, propagate):
    cnt = Counter(); cnt['max_conflicts'] = 0
    opened = []
    open_keys = set()
    seen = set()
    seen_att = set(); open_att = set(); last_att = [None]       # known matrices already refuted: different colour factors can give the SAME attachment
    gen = (gen_attachments(core, boundary) if FAMILY == "GEN" else
           p3nb_attachments(core, boundary) if BG is not None else
           ((a, sg) for a in (att.for_boundary(boundary) if Q12K else [()]) for sg in (P4 if YY else [None])))
    for attached, sigma in gen:
        rows = materialize(core, boundary, attached, sigma); cnt['valid_partial'] += 1
        if FAMILY == "GEN" and FLIP_LINES:
            ck = attachment_canon(attached)
            if ck != tuple(attached) and ck in seen_att:
                if ck in open_att:
                    cnt['OPEN_SYMMETRIC_ATTACHMENT'] += 1
                else:
                    cnt['EXCLUDED_SYMMETRIC_ATTACHMENT'] += 1      # its orbit representative was refuted
                continue
            seen_att.add(tuple(attached)); last_att[0] = tuple(attached)
        key = tuple(rows)
        if key in seen:
            # identical known rows => identical frontier input and verdict.  Outside --all-attachments the first
            # occurrence was excluded (a non-excluded one returns at once below); with --all-attachments a duplicate of
            # an OPEN matrix is counted as open.
            if key in open_keys:
                cnt['OPEN_DUPLICATE_ROWS'] += 1
            else:
                cnt['EXCLUDED_DUPLICATE_ROWS'] += 1
            continue
        seen.add(key)
        cert = frontier(rows, propagate)
        if cert['status'] == 'EXCLUDED_PROFILE_SELECTION_UNSAT':
            pc = cert.get('proof_check') or {}
            assert pc.get('empty_clause_verified') is True, 'unverified UNSAT'
            cnt['sat_calls'] += 1; cnt['rup_checked_additions'] += pc.get('checked_additions', 0)
            cnt['max_conflicts'] = max(cnt['max_conflicts'], cert.get('conflicts') or 0)
        if VERBOSE:
            print(json.dumps({k: cert.get(k) for k in ('status', 'cpu_seconds', 'proof_lines', 'variables', 'clauses', 'mus_size', 'mus') if k in cert}),
                  file=sys.stderr, flush=True)
        if cert['status'].startswith('EXCLUDED'):
            cnt[cert['status']] += 1
            continue
        if ALLATT:              # residual mapping: keep going and list every non-excluded (attachment, sigma)
            open_keys.add(key)
            if last_att[0] is not None:
                open_att.add(last_att[0])
            cnt['OPEN_' + cert['status']] += 1
            opened.append({'attachment': attached, 'sigma': sigma, 'status': cert['status'],
                           'selected_profiles': cert.get('selected_profiles')})
            continue
        return {'status': 'FEASIBLE_PARTIAL_FRONTIER', 'counts': dict(cnt), 'witness_attachments': attached,
                'witness_sigma': sigma, 'frontier': cert}
    if ALLATT and opened:
        return {'status': 'FEASIBLE_PARTIAL_FRONTIER', 'counts': dict(cnt), 'open_attachments': opened}
    return {'status': 'EXCLUDED_BY_FACTOR_JOIN_AND_FRONTIER', 'counts': dict(cnt)}


OUT = next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--out=')), None)
raw = open(bpath, 'rb').read()
src = json.loads(gzip.decompress(raw))
core = src.get('core')
att = Attachments(core) if (core is not None and Q12K) else None
t0 = time.process_time(); stats = Counter(); feas = []; records = []
IDX = next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--indices=')), None)
IDX = set(json.load(open(IDX))) if IDX else None      # optional explicit boundary indices (within [START, START+COUNT))
if src.get('status') == 'COMPLETE_BOUNDARY_COVER':
    for bi, hx in enumerate(src['boundaries_hex']):
        if bi < START:
            continue
        if bi >= START + COUNT:
            break
        if IDX is not None and bi not in IDX:
            continue
        tb = time.process_time()
        r = solve(core, tuple(bytes.fromhex(hx)), att, PROPAGATE)
        stats[r['status']] += 1
        if not r['status'].startswith('EXCLUDED'):
            feas.append((bi, r))
        records.append({'boundary_index': bi, 'boundary_hex': hx, 'status': r['status'], 'counts': r['counts'],
                        'cpu_seconds': round(time.process_time() - tb, 3),
                        **({'witness': r} if not r['status'].startswith('EXCLUDED') else {})})
summary = {'family': FAMILY, 'core': src['core_index'], 'range': [START, START + COUNT], 'statuses': dict(stats),
           'gen_layer_nodes': dict(sorted(LAYER.items())) if FAMILY == 'GEN' else None,
           'first_feasible': feas[:2], 'cpu_seconds': round(time.process_time() - t0, 1)}
print(json.dumps(summary, default=str))
if DUMP is not None:
    from pathlib import Path as _P
    _P(DUMP).write_text(json.dumps({'source': bpath, 'start': START, 'count': COUNT, 'blocks': DUMPED}))
if OUT:
    import hashlib
    from pathlib import Path
    mods = {m: hashlib.sha256(Path(codex, m).read_bytes()).hexdigest() for m in
            ('root_component_shared_core_colors.py', 'root_component_shared_k3_boundary.py',
             'root_component_shared_k3_profile_sat.py')}
    doc = {'scope': 'P3/K3 shared-core frontier with exact profile SAT (LAB py_extend.py); EXCLUDED means every '
                    'attachment of the boundary is refuted (frontier or RUP-checked UNSAT)',
           'flags': [a for a in sys.argv[6:]], 'program_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'codex_modules_sha256': mods, 'source_path': bpath, 'source_sha256': hashlib.sha256(raw).hexdigest(),
           'core_index': src['core_index'], 'total_boundaries': src.get('boundary_count', 0),
           'summary': summary, 'cases': records}
    Path(OUT).parent.mkdir(parents=True, exist_ok=True)
    tmp = OUT + '.tmp'
    Path(tmp).write_bytes(gzip.compress(json.dumps(doc, default=str).encode(), mtime=0))
    Path(tmp).replace(OUT)
