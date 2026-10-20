import json, sys
a = [json.loads(l) for l in open(sys.argv[1])]
b = [json.loads(l) for l in open(sys.argv[2])]
assert len(a) == len(b), (len(a), len(b))
bad = 0
from collections import Counter
st = Counter()
for x, y in zip(a, b):
    st[x["status"]] += 1
    for k in ("line", "status", "x", "candidates", "nodes"):
        if x[k] != y[k]:
            bad += 1
            if bad < 20: print("DIFF line", x["line"], k, x[k], y[k])
print("lines", len(a), "field diffs", bad, dict(st))
T = [i for i, x in enumerate(a) if x["status"] in ("UNSAT", "SAT", "TIMEOUT")]
if T:
    for nm, L in (("ref", a), ("fast", b)):
        s = sorted(L[i]["build_ms"] + L[i]["prep_ms"] + L[i]["search_ms"] for i in T)
        print(nm, "tested", len(T), "mean total ms %.4f" % (sum(s) / len(s)), "median %.4f" % s[len(s) // 2],
              "mean prep %.4f" % (sum(L[i]["prep_ms"] for i in T) / len(T)), "mean search %.4f" % (sum(L[i]["search_ms"] for i in T) / len(T)),
              "nodes sum", sum(L[i]["nodes"] for i in T))
