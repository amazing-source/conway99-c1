"""Summarise the second c3 pilot (run verif2b): 600 s on the 42 tasks unresolved at 60 s, and --grid-corner-tables
at 60 s on the 100 pilot tasks, compared with the first pilot (verif1b)."""
import json
from collections import Counter
from pathlib import Path
root = Path("collect_verif2b")
first = {}
for r in json.load(open("collect_verif1b/p3_summary.json")):
    first.setdefault(r["task"], {})[r["variant"]] = r["status"]
def status(jid):
    f = root / "files" / "out" / (jid + ".json")
    if not f.exists():
        return None, None
    d = json.load(open(f))
    b = (d.get("matching_branches") or [{}])[0]
    return b.get("status"), b.get("cpu_seconds")
rows = {}
for n in range(100):
    rows[n] = {"t60": first[n]["t"], "n60": first[n]["n"]}
    for tag in ("q2n600", "q2g600", "q2g60"):
        s, cpu = status("%s_%03d" % (tag, n))
        if s is not None:
            rows[n][tag] = s
            rows[n][tag + "_cpu"] = cpu
print("g60 vs n60 on 100 tasks:", dict(Counter((r["n60"], r.get("q2g60")) for r in rows.values())))
unk = [n for n, r in rows.items() if r["t60"] == "UNKNOWN" and r["n60"] == "UNKNOWN"]
print("on the 42 unresolved: n600", dict(Counter(rows[n].get("q2n600") for n in unk)), "| g600", dict(Counter(rows[n].get("q2g600") for n in unk)))
closed = [n for n in range(100) if "INFEASIBLE" in (rows[n]["t60"], rows[n]["n60"], rows[n].get("q2n600"), rows[n].get("q2g600"), rows[n].get("q2g60"))]
print("excluded by at least one valid model:", len(closed), "/ 100")
cpus = [rows[n]["q2n600_cpu"] for n in unk if rows[n].get("q2n600") == "INFEASIBLE"]
print("n600 CPU of the newly closed:", sorted(round(c) for c in cpus))
cpus = [rows[n]["q2g600_cpu"] for n in unk if rows[n].get("q2g600") == "INFEASIBLE"]
print("g600 CPU of the newly closed:", sorted(round(c) for c in cpus))
json.dump(rows, open(root / "q2_summary.json", "w"), indent=1)
