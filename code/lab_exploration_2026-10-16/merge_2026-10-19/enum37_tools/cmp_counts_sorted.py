import json, subprocess, sys, time
sys.path.insert(0, r"C:\Users\RESEARCHER\Downloads\conway_c2_researcher2_start_2026_09_30\conway_c2_researcher2_start_2026_09_30\work\exploration_2026-10-16\merge_2026-10-19")
from enum37_burnside import partitions, count_lambda
m = int(sys.argv[1]); exe = sys.argv[2]; budget = float(sys.argv[3]); out = sys.argv[4]; rate = float(sys.argv[5]) if len(sys.argv) > 5 else 1.5e7
extra = sys.argv[6:]          # e.g. --adm
n = 2 * m
lams = sorted(((count_lambda(l, n)["N"], l) for l in partitions(n)))
rows = []; t0 = time.time(); ok = True
for b, lam in lams:
    left = budget - (time.time() - t0)
    if b / rate > left:
        continue
    arg = ",".join(map(str, lam))
    r = subprocess.run([exe, arg, "--count"] + extra, capture_output=True, text=True, timeout=left + 5)
    j = json.loads(r.stdout.strip().splitlines()[-1])
    rows.append({"lambda": arg, "burnside": b, "enum": j["classes"], "wall_s": j["wall_s"], "candidates": j["candidates"],
                 "ties": j["tie_checks"], "tie_rejects": j["tie_rejects"], "node2_tables_max": j["node2_tables_max"]})
    if not extra and b != j["classes"]:
        ok = False
    print(arg, b, j["classes"], ("OK" if b == j["classes"] else "MISMATCH") if not extra else "", j["wall_s"], flush=True)
json.dump({"n": n, "extra": extra, "all_ok": ok, "rows": rows}, open(out, "w"), indent=1)
print("n=%d checked %d partitions, all_ok=%s, wall %.1f" % (n, len(rows), ok, time.time() - t0))
