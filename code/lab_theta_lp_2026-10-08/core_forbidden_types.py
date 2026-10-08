"""C1, lab session, 2026-10-09. Crossing the rank-free cores with the census: which small induced types become impossible?
  python core_forbidden_types.py <twisted_core_check.json> <codex_unresolved_174_bits.json> <census2 order-10 json> <out json>
Fact used (Codex's notes 221, 222, certified there; my re-derivation of the 310): in every srg(99,14,1,2) every motif S
(two disjoint triangles joined by exactly two edges) has its 14-vertex core H(S) among 174 types.
Consequence: let X be a graph of order 6 + j <= 10 made of S and j vertices each adjacent to exactly two points of S (so
"doubles" of S). An induced copy of X in the graph is a sub-configuration of a core, hence X is induced, on S and j of its
doubles, in one of the 174 surviving cores. If it is in none, the number of induced copies of X is ZERO.
This script lists the abstract types X (canonical keys of census2.py) of the form "S + j doubles", j <= 4, that are
admissible (the census knows them) but occur in none of the 174 cores, and looks each one up in the census file to get
its count as an affine form of the 549 census parameters. Exact; no solver."""
import sys, json, os, importlib.util
from itertools import combinations
spec = importlib.util.spec_from_file_location("census2", os.path.join(os.path.dirname(os.path.abspath(__file__)), "census2.py")); c2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
D = json.load(open(sys.argv[1])); keep = set(json.load(open(sys.argv[2]))); C = json.load(open(sys.argv[3]))
SUP = {6: (0, 3), 7: (1, 4), 8: (2, 3), 9: (2, 4), 10: (0, 5), 11: (1, 5), 12: (2, 5), 13: (2, 5)}
BASE = [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5), (0, 3), (1, 4)] + [(d, s) for d, sp in SUP.items() for s in sp]
def key_of(vertices, edges):
    pos = {v: i for i, v in enumerate(vertices)}; rows = [0] * len(vertices)
    for u, v in edges:
        if u in pos and v in pos: rows[pos[u]] |= 1 << pos[v]; rows[pos[v]] |= 1 << pos[u]
    return c2.canon(len(vertices), rows)[0]
def patterns(cores):
    out = {j: set() for j in range(0, 5)}
    for c in cores:
        edges = BASE + [tuple(e) for e in c["edges_among_doubles"]]
        for j in range(0, 5):
            for sub in combinations(range(6, 14), j): out[j].add(key_of(list(range(6)) + list(sub), edges))
    return out
surv = [c for c in D["cores"] if c["bits"] in keep]; assert len(surv) == 174
allc = D["cores"]                                                       # the 373 locally consistent cores (reference set of admissible patterns)
Ps = patterns(surv); Pa = patterns(allc); Pp = patterns([c for c in D["cores"] if not c["excluded"]])
census = {n: {t[0]: t for t in C["types"][str(n)]} for n in range(6, 11)}
out = {"what": "types 'S + j doubles' admissible in the census but absent from the 174 surviving cores: their counts are zero", "forbidden": []}
for j in range(0, 5):
    n = 6 + j; miss = sorted(Pa[j] - Ps[j]); inc = [k for k in miss if k in census[n]]
    print("j = %d (order %d): patterns in the 373 cores %d, in the 310 %d, in the 174 %d; absent from the 174: %d, of which known to the census: %d" % (j, n, len(Pa[j]), len(Pp[j]), len(Ps[j]), len(miss), len(inc)))
    for k in inc:
        t = census[n][k]; out["forbidden"].append({"order": n, "key": k, "rows": t[1], "aut": t[2], "form": t[3], "edges": sum(bin(r).count("1") for r in t[1]) // 2})
json.dump(out, open(sys.argv[4], "w"))
print("forbidden types written: %d (orders %s)" % (len(out["forbidden"]), sorted(set(f["order"] for f in out["forbidden"]))))
for f in out["forbidden"][:12]: print("   order %d, %d edges, key %d, form with %d terms, constant %s" % (f["order"], f["edges"], f["key"], len(f["form"]), f["form"].get("0", "0")))
