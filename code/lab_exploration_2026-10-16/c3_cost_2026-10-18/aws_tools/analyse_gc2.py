"""Summary of run gc2a (LAB 18/10/2026): ablations of the Gram-cover model and Gram-by-Gram deaths."""
import glob, json, os
from collections import defaultdict
ab, pg = defaultdict(dict), defaultdict(dict)
for f in sorted(glob.glob("collect_gc2a/files/out/*.json")):
    d = json.load(open(f)); n = os.path.basename(f)[:-5]
    if n.startswith("ab_"):
        _, t, v = n.split("_", 2); ab[int(t)][v] = (d.get("status"), round(d.get("cpu_seconds") or 0))
    else:
        _, t, k = n.split("_"); pg[int(t)][int(k)] = (d.get("status"), round(d.get("cpu_seconds") or 0, 1))
for t in sorted(ab):
    print("ablation", t, " ".join("%s=%s/%ss" % (v, s[0][:5], s[1]) for v, s in sorted(ab[t].items())))
for t in sorted(pg):
    st = [v[0] for v in pg[t].values()]; cpu = sorted(v[1] for v in pg[t].values())
    print("per-Gram", t, "done", len(st), "INFEASIBLE", st.count("INFEASIBLE"), "UNKNOWN", st.count("UNKNOWN"),
          "cpu min/median/max", cpu[0], cpu[len(cpu) // 2], cpu[-1], "unknown grams", [k for k, v in sorted(pg[t].items()) if v[0] != "INFEASIBLE"][:20])
