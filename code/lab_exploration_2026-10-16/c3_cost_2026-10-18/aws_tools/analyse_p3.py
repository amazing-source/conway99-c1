"""Summarise the c3 complete-star pilot of run verif1b (LAB 18/10/2026).
For every task (template, matching) and both variants (t = default transport, n = --no-transport): final status,
solver CPU, build CPU, peak memory, product-domain encoding tag; then the kill rate and the cost extrapolated to the
106 852 tasks (and to the 40 297 mate-swap orbit representatives, if that reduction is confirmed).
usage: py -3 analyse_p3.py <dir with done/*.json and files/out/p3*.json> <manifest_verif1.tsv.pilot.json>"""
import json
import sys
from collections import Counter
from pathlib import Path

root, pilot = Path(sys.argv[1]), json.load(open(sys.argv[2]))["pilot_sample"]
rows = []
for n, (src, idx, j) in enumerate(pilot):
    for tag in "tn":
        jid = "p3%s_%03d" % (tag, n)
        done = root / "done" / (jid + ".json")
        rep = root / "files" / "out" / (jid + ".json")
        d = json.load(open(done)) if done.exists() else None
        r = json.load(open(rep)) if rep.exists() else None
        branches = (r or {}).get("matching_branches") or []
        b = branches[0] if branches else {}
        text = json.dumps(r) if r else ""
        rows.append(dict(task=n, variant=tag, template=idx, source=src.split("/")[-1], matching=j,
                         exit=(d or {}).get("exit"), wall=(d or {}).get("wall"), rss_kb=(d or {}).get("maxrss_kb"),
                         status=b.get("status") or (r or {}).get("status"), branch_keys=sorted(b)[:40],
                         encoding_v2="python_list_endpoints_v2" in text))
by = {t: Counter(r["status"] for r in rows if r["variant"] == t) for t in "tn"}
print("status by variant:", {t: dict(c) for t, c in by.items()})
for t in "tn":
    sel = [r for r in rows if r["variant"] == t and r["wall"] is not None]
    if sel:
        walls = sorted(r["wall"] for r in sel)
        mean = sum(walls) / len(walls)
        print("variant %s: %d done, wall mean %.1f s, median %.1f s, max %.1f s; encoding v2 tag on %d; peak RSS max %.2f GiB"
              % (t, len(sel), mean, walls[len(walls) // 2], walls[-1], sum(r["encoding_v2"] for r in sel),
                 max((r["rss_kb"] or 0) for r in sel) / 1048576))
        print("   extrapolation: 106852 tasks x %.1f s = %.0f core-hours; 40297 orbit tasks = %.0f core-hours"
              % (mean, 106852 * mean / 3600, 40297 * mean / 3600))
json.dump(rows, open(root / "p3_summary.json", "w"), indent=1)
print("example branch keys:", rows[0]["branch_keys"] if rows else None)
