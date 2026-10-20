"""resumable: fastcount (plain and --adm) for every lambda |- 12, appended to a jsonl; stops before the time budget"""
import json, os, subprocess, sys, time
sys.path.insert(0, r"C:\Users\RESEARCHER\Downloads\conway_c2_researcher2_start_2026_09_30\conway_c2_researcher2_start_2026_09_30\work\exploration_2026-10-16\merge_2026-10-19")
from enum37_burnside import partitions, count_lambda
exe, budget, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
susp = os.path.join(os.path.dirname(out), "..", "suspended.json")
done = set()
if os.path.exists(out):
    for l in open(out):
        j = json.loads(l); done.add((j["lambda"], j["adm"]))
lams = sorted(((count_lambda(l, 12)["N"], l) for l in partitions(12)))
t0 = time.time()
est = {}   # expected seconds ~ classes / rate
for b, lam in lams:
    arg = ",".join(map(str, lam))
    for adm in (False, True):
        if (arg, adm) in done: continue
        if os.path.exists(susp): print("suspended"); sys.exit(0)
        need = b / 1.6e8 + 2           # (12) took 83 s for 1.56e10
        if time.time() - t0 + need > budget: print("budget stop before", arg, adm); sys.exit(0)
        opts = ["--fastcount"] + (["--adm"] if adm else [])
        r = subprocess.run([exe, arg] + opts, capture_output=True, text=True, timeout=budget - (time.time() - t0) + 10)
        j = json.loads(r.stdout.strip().splitlines()[-1])
        rec = {"lambda": arg, "adm": adm, "burnside": b, "classes": j["classes"], "z": j["z"], "wall_s": j["wall_s"],
               "candidates": j["candidates"], "ties": j["tie_checks"], "fast_pairs": j["fast_pairs"], "pairs": j["pairs"]}
        if not adm: rec["match"] = j["classes"] == b
        open(out, "a").write(json.dumps(rec) + "\n")
        print(arg, adm, j["classes"], b, j["wall_s"], flush=True)
print("all done")
