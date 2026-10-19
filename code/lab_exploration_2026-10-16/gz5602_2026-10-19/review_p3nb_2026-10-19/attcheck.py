# Independent attachment check for P3NB.  My own label model: core (0..7), Q45 (8..11), Q46 (12..15), Q13 (16..19).
# Known graph = core edges + letter 4-cycles in Q45, Q46, Q13 + boundary Y-core edges + three perfect matchings
# Q13-Q02, Q13-Q45, Q13-Q46 (all 24^3).  Valid = lambda/mu on known pairs (with shared letters), letter quotas, degree<=12.
# Compares with py_extend's p3nb_attachments (yield set) and materialize rows; for yielded-but-invalid ones checks that
# frontier() reports a NEGATIVE deficit.  Loads py_extend via runpy with an empty range (no output files).
import gzip, json, runpy, sys
from itertools import permutations, product, combinations
pyext, codex, covdir, ci, bis = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]
cov = "%s/core_%03d.json.gz" % (covdir, ci)
sys.argv = [pyext, codex, "P3NB", cov, "0", "0", "--sat", "--lean", "--enc=seq"]
ns = runpy.run_path(pyext, run_name="__notmain__")
rec = json.loads(gzip.decompress(open(cov, "rb").read())); core = rec["core"]
L = [(s, 2 + t) for s in range(2) for t in range(2)] + [(s, 4 + t) for s in range(2) for t in range(2)] \
    + [(8 + s, 10 + t) for s in range(2) for t in range(2)] + [(8 + s, 12 + t) for s in range(2) for t in range(2)] \
    + [(2 + s, 6 + t) for s in range(2) for t in range(2)]
assert [tuple(q) for q in ns["LABELS"]] == L, ns["LABELS"]
SH = [[len(set(a) & set(b)) for b in L] for a in L]
def quota(u, l): return 2 - (l in L[u]) - ((l ^ 1) in L[u])
def base_adj(bd):
    A = [0] * 20
    def e(u, v): A[u] |= 1 << v; A[v] |= 1 << u
    for u, v in core["edges"]: e(u, v)
    for off in (8, 12, 16):
        for i in range(4):
            for j in range(i + 1, 4):
                if SH[off + i][off + j] == 1: e(off + i, off + j)   # letter-sharing cycle (my criterion, not i^j)
    for k in range(8):
        for v in range(8):
            if bd[k] >> v & 1: e(v, 8 + k)
    return A, e
LM = [sum(1 << v for v in range(20) if l in L[v]) for l in range(14)]
QU = [[quota(u, l) for l in range(14)] for u in range(20)]
PAIRS = [(u, v, SH[u][v]) for u, v in combinations(range(20), 2)]
def valid(A):
    for u in range(20):
        a = A[u]
        if a.bit_count() > 12: return False
        q = QU[u]
        for l in range(14):
            if (a & LM[l]).bit_count() > q[l]: return False
    for u, v, sh in PAIRS:
        if (A[u] & A[v]).bit_count() + sh > 2 - (A[u] >> v & 1): return False
    return True
P4 = list(permutations(range(4)))
recs = rec["boundaries_hex"]
import random
if bis == "all": sel = range(len(recs))
elif bis.startswith("rand"): sel = sorted(random.Random(ci * 7919 + 1).sample(range(len(recs)), min(int(bis[4:]), len(recs))))
else: sel = [int(x) for x in bis.split(",")]
tot = {"boundaries": 0, "my_valid": 0, "yielded": 0, "pruned_but_valid": 0, "yield_invalid_not_negdef": 0, "rows_mismatch": 0}
for bi in sel:
    bd = tuple(bytes.fromhex(recs[bi])); tot["boundaries"] += 1
    A0, _ = base_adj(bd)
    mv = set()
    # layered for speed: only full checks at the end, all 24^3
    for beta in P4:
        for s1 in P4:
            for s2 in P4:
                A = A0[:]
                for c in range(4):
                    for (u, v) in ((16 + c, 4 + beta[c]), (16 + c, 8 + s1[c]), (16 + c, 12 + s2[c])):
                        A[u] |= 1 << v; A[v] |= 1 << u
                if valid(A): mv.add((beta, s1, s2))
    theirs = [a for a, _ in ns["p3nb_attachments"](core, bd)]
    ts = set(theirs)
    tot["my_valid"] += len(mv); tot["yielded"] += len(ts)
    tot["pruned_but_valid"] += len(mv - ts)
    for a in ts:
        rows = ns["materialize"](core, bd, a)
        A = A0[:]
        beta, s1, s2 = a
        for c in range(4):
            for (u, v) in ((16 + c, 4 + beta[c]), (16 + c, 8 + s1[c]), (16 + c, 12 + s2[c])):
                A[u] |= 1 << v; A[v] |= 1 << u
        if list(rows) != A: tot["rows_mismatch"] += 1
        if a not in mv:
            st = ns["frontier"](rows, True)["status"]
            if not st.startswith("EXCLUDED_NEGATIVE"): tot["yield_invalid_not_negdef"] += 1
print(json.dumps({"core": ci, **tot}))
