import json, subprocess, sys, time
sys.path.insert(0, r"C:\Users\RESEARCHER\Downloads\conway_c2_researcher2_start_2026_09_30\conway_c2_researcher2_start_2026_09_30\work\exploration_2026-10-16\merge_2026-10-19")
from enum37_burnside import partitions, count_lambda
m = int(sys.argv[1]); exe = sys.argv[2]; budget = float(sys.argv[3]); out = sys.argv[4]; maxfull = float(sys.argv[5])
n = 2 * m
lams = sorted(((count_lambda(l, n)["N"], l) for l in partitions(n)))
rows = []; t0 = time.time(); ok = True
def run(arg, opts):
    r = subprocess.run([exe, arg] + opts, capture_output=True, text=True, timeout=max(5, budget - (time.time() - t0) + 5))
    return json.loads(r.stdout.strip().splitlines()[-1])
for b, lam in lams:
    if time.time() - t0 > budget: break
    arg = ",".join(map(str, lam))
    f = run(arg, ["--fastcount"]); fa = run(arg, ["--fastcount", "--adm"])
    row = {"lambda": arg, "z": f["z"], "burnside": b, "fast": f["classes"], "fast_adm": fa["classes"], "wall_fast": f["wall_s"], "wall_fast_adm": fa["wall_s"]}
    if b <= maxfull:
        c = run(arg, ["--count"]); ca = run(arg, ["--count", "--adm"])
        row["full"] = c["classes"]; row["full_adm"] = ca["classes"]
        if c["classes"] != f["classes"] or ca["classes"] != fa["classes"]: ok = False
    if f["classes"] != b: ok = False
    rows.append(row)
    print(json.dumps(row), flush=True)
json.dump({"n": n, "all_ok": ok, "rows": rows, "total_fast": sum(r["fast"] for r in rows), "total_fast_adm": sum(r["fast_adm"] for r in rows)}, open(out, "w"), indent=1)
print("n=%d: %d partitions, all_ok=%s, total=%d, total_adm=%d, wall %.1f" % (n, len(rows), ok, sum(r["fast"] for r in rows), sum(r["fast_adm"] for r in rows), time.time() - t0))
