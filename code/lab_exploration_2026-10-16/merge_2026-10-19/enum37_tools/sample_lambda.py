"""per-lambda sampling: enum37 --random k -> line37 file; status distribution and ms per line for each lambda (resumable)"""
import json, os, subprocess, sys, time, collections
sys.path.insert(0, r"C:\Users\RESEARCHER\Downloads\conway_c2_researcher2_start_2026_09_30\conway_c2_researcher2_start_2026_09_30\work\exploration_2026-10-16\merge_2026-10-19")
from enum37_burnside import partitions, count_lambda
enum, l37, k, budget, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
d = os.path.dirname(out)
done = set()
if os.path.exists(out):
    for l in open(out): done.add(json.loads(l)["lambda"])
t0 = time.time()
lams = sorted(((count_lambda(l, 12)["N"], l) for l in partitions(12)), reverse=True)
for b, lam in lams:
    arg = ",".join(map(str, lam))
    if arg in done: continue
    if os.path.exists(os.path.join(d, "..", "suspended.json")): print("suspended"); break
    if time.time() - t0 > budget: print("budget stop"); break
    seed = 1000 + len(done)
    tmp = os.path.join(d, "samp_tmp.txt")
    with open(tmp, "w") as fh:
        subprocess.run([enum, arg, "--random", str(k), str(7700 + hash(arg) % 1000)], stdout=fh, stderr=subprocess.DEVNULL, check=True)
    r = subprocess.run([l37, "file", tmp, "60"], capture_output=True, text=True)
    c = collections.Counter(); ms = 0.0; tested_ms = []
    for line in r.stdout.strip().splitlines():
        j = json.loads(line); c[j["status"]] += 1
        t = j["build_ms"] + j["prep_ms"] + j["search_ms"]; ms += t
        if j["status"] in ("UNSAT", "SAT", "TIMEOUT"): tested_ms.append(t)
    rec = {"lambda": arg, "N": b, "samples": sum(c.values()), "status": dict(c), "ms_per_line": ms / max(1, sum(c.values())),
           "tested_ms_mean": sum(tested_ms) / len(tested_ms) if tested_ms else None, "tested_ms_max": max(tested_ms) if tested_ms else None}
    open(out, "a").write(json.dumps(rec) + "\n"); done.add(arg)
    print(arg, dict(c), round(rec["ms_per_line"], 2), flush=True)
print("wall %.1f" % (time.time() - t0))
