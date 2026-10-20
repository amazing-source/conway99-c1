import json, sys, collections
c = collections.Counter(); t = collections.defaultdict(float); tested = []; nodes = []
for path in sys.argv[1:]:
    for l in open(path):
        j = json.loads(l); s = j["status"]; c[s] += 1
        ms = j["build_ms"] + j["prep_ms"] + j["search_ms"]; t[s] += ms
        if s in ("UNSAT", "SAT", "TIMEOUT"): tested.append(ms); nodes.append(j["nodes"])
tot = sum(c.values())
out = {"lines": tot, "status": dict(c), "ms_total": round(sum(t.values()), 1)}
if tested:
    tested.sort()
    out.update({"tested": len(tested), "tested_ms_mean": round(sum(tested) / len(tested), 3), "tested_ms_median": round(tested[len(tested) // 2], 3),
                "tested_ms_p99": round(tested[int(len(tested) * 0.99)], 3), "tested_ms_max": round(tested[-1], 3), "nodes_max": max(nodes)})
print(json.dumps(out))
