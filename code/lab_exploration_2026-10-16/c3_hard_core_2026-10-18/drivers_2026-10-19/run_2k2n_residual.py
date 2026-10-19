"""2K2 residual mapping: for every stage-2 shard, its non-excluded boundaries are re-run with --all-attachments, which
lists EVERY non-excluded (attachment, sigma) with its status (SAT_KNOWN_ROWS_COMPLETE or UNKNOWN_PROFILE_SAT), the
excluded ones being refuted as usual (frontier or RUP-checked UNSAT).  Writes residual shards and a summary JSON
k2k2_residual_attachments.json (core_index, boundary_index, boundary_hex, attachment, sigma, status).
One process at a time, BELOW_NORMAL, <= 3600 s per call."""
import gzip
import json
import subprocess
import sys
import time
from pathlib import Path

S = Path(__file__).resolve().parent
W = Path(r"C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/exploration_2026-10-16/gz5602_2026-10-19")
py = sys.executable
codex = S / "k3prod_v4/pkg/code/codex"
sh2 = S / "shards_2k2n"; shr = S / "shards_2k2n_residual"; shr.mkdir(exist_ok=True)
log = open(S / "run_2k2n_residual.log", "a", encoding="utf8")
summary = []
for f in sorted(sh2.glob("core*_all.json.gz")):
    d = json.load(gzip.open(f))
    ci = d["core_index"]
    res = [c["boundary_index"] for c in d["cases"] if not c["status"].startswith("EXCLUDED")]
    if not res:
        continue
    idxf = S / ("resid_2k2n_core%03d.json" % ci); idxf.write_text(json.dumps(res))
    out = shr / ("core%03d_residual.json.gz" % ci)
    if not out.exists():
        t = time.time()
        r = subprocess.run([py, "-X", "utf8", str(W / "py_extend.py"), str(codex), "2K2N",
                            str(S / "pybd_2k2n_all" / ("core_%03d.json.gz" % ci)), "0", str(d["total_boundaries"]),
                            "--sat", "--lean", "--enc=seq", "--all-attachments", "--indices=" + str(idxf), "--out=" + str(out)],
                           capture_output=True, text=True, timeout=7200, creationflags=0x00004000)
        log.write("%s core %d residual boundaries %s: %s (%.0fs) %s\n" % (time.strftime("%H:%M:%S"), ci, res,
                  (r.stdout.strip().splitlines() or [""])[-1][:200], time.time() - t, r.stderr.strip()[-300:])); log.flush()
    dd = json.load(gzip.open(out))
    for c in dd["cases"]:
        for a in c.get("witness", {}).get("open_attachments", []):
            summary.append({"core_index": ci, "boundary_index": c["boundary_index"], "boundary_hex": c["boundary_hex"],
                            "attachment": a["attachment"], "sigma": a["sigma"], "status": a["status"]})
(W / "k2k2n_residual_attachments.json").write_text(json.dumps(summary, indent=1))
log.write("END residual attachments: %d\n" % len(summary)); log.close()
print(len(summary))
