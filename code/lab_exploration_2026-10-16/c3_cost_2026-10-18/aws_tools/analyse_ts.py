"""Summarise the two-star test (run verif4b): per hard pilot task, how many opposite matchings M' are INFEASIBLE
(the task is excluded iff all are), with CPU."""
import glob, json, os, re
from collections import defaultdict
per = defaultdict(dict)
for f in glob.glob(os.path.join("collect_verif4b", "files", "out", "ts_*.json")):
    m = re.match(r"ts_(\d+)_o(\d+)\.json", os.path.basename(f))
    d = json.load(open(f))
    r = d["results"][0] if d.get("results") else {}
    per[int(m.group(1))][int(m.group(2))] = (r.get("status"), r.get("cpu_seconds", 0) or 0)
closed = 0
for n in sorted(per):
    st = [s for s, _ in per[n].values()]
    full = all(s == "INFEASIBLE" for s in st)
    closed += full
    cpu = sum(c for _, c in per[n].values())
    print("task %3d: %2d opposite matchings, INFEASIBLE %2d, UNKNOWN %2d, total CPU %6.0f s %s"
          % (n, len(st), st.count("INFEASIBLE"), st.count("UNKNOWN"), cpu, "-> TASK EXCLUDED" if full else ""))
print("hard tasks excluded by the two-star split at 60 s per sub-branch:", closed, "/", len(per))
