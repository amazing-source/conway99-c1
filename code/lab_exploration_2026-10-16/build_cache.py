"""Distinct four-star structures under a root, cached as JSONL (canonical labels/edges), in resumable chunks.
usage: python build_cache.py <root> <cache.jsonl> <start index> <count>   (files in sorted walk order)"""
import json, os, sys, time
root, cache, start, count = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
t0 = time.time()
files = []
for dp, dn, fn in os.walk(root):
    dn.sort()
    for f in sorted(fn):
        if f.endswith(".json"):
            files.append(os.path.join(dp, f))
seen = set()
if os.path.exists(cache):
    for line in open(cache):
        d = json.loads(line)
        seen.add(tuple(tuple(map(tuple, e)) for e in d["edges"]))
new = 0
with open(cache, "a") as out:
    for p in files[start:start + count]:
        try:
            d = json.load(open(p))
            L = [tuple(sorted(x)) for x in d["labels"]]
            E = sorted(tuple(sorted((L[i], L[j]))) for i, j in d["edges"])
        except Exception:
            continue
        key = tuple(E)
        if key in seen:
            continue
        seen.add(key)
        labs = sorted(set(L))
        out.write(json.dumps({"src": os.path.relpath(p, root), "labels": labs, "edges": [list(map(list, e)) for e in E]}) + "\n")
        new += 1
print("files total %d, processed %d..%d, new distinct %d, cache size %d, %.0f s" % (len(files), start, min(len(files), start + count), new, len(seen), time.time() - t0))
