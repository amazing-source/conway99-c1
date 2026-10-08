"""C1, lab session, 2026-10-08. Sweep Codex's solver-free two-star propagation (code/codex/joint_star_propagation.py,
commit f87be43) over the common-apex branches of one ball, in one process, within a time budget.
  python sweep_two_star_propagation.py <codex code/codex dir> <ball json> <apex start> <seconds> <out json>
Each branch: setup + propagate + replay (Codex's own exact checker). Records which branches die by propagation alone
(and how), which survive it (to be sent to the pair LP). Nothing here is a uniform statement."""
import sys, json, time
sys.path.insert(0, sys.argv[1])
from joint_generic_stars import prepare
from joint_star_propagation import setup, propagate, replay
t0 = time.time(); ball = json.load(open(sys.argv[2]))["adjacency"]; start = int(sys.argv[3]); budget = float(sys.argv[4])
prepared = prepare(ball, 0, 12); n = len(prepared[6]); out = {"ball": sys.argv[2], "apex_candidates": n, "branches": {}}
i = start
while i < n and time.time() - t0 < budget:
    system = setup(prepared, 0, 12, i); res = propagate(system); replay(system, res)
    out["branches"][i] = {"contradiction": res["contradiction"], "deletions": res["deletion_counts"]}
    i += 1
out["next_start"] = i; out["seconds"] = round(time.time() - t0, 1)
dead = sum(1 for b in out["branches"].values() if b["contradiction"]); out["dead_by_propagation"] = dead; out["survivors"] = [k for k, b in out["branches"].items() if not b["contradiction"]]
json.dump(out, open(sys.argv[5], "w"), indent=1)
print("ball %s: %d apex candidates; branches %d..%d done in %.0f s: %d dead by propagation alone, survivors %s" % (sys.argv[2].split("/")[-1], n, start, i - 1, time.time() - t0, dead, out["survivors"]))
