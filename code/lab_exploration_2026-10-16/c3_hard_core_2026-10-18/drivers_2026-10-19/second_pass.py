"""P3 second pass (LAB 19/10/2026): every non-excluded boundary found in pkg/data/p3_shards (UNKNOWN at the 200k-conflict
budget, or SAT) is re-run with --all-attachments and a 3M-conflict budget; output p3_residual/coreXXX_bBBBBB.json.gz.
Loops until no new non-excluded boundary appears and LOOP is off.  One process, BELOW_NORMAL, <= 3 h per boundary.
usage: python second_pass.py [--loop]"""
import gzip
import json
import subprocess
import sys
import time
from pathlib import Path

base = Path(__file__).resolve().parent
S = base.parent
W = Path(r"C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/exploration_2026-10-16/gz5602_2026-10-19")
out = S / "p3_residual"; out.mkdir(exist_ok=True)
log = open(out / "second_pass.log", "a", encoding="utf8")
LOOP = "--loop" in sys.argv
while True:
    todo = []
    for f in sorted((base / "pkg/data/p3_shards").glob("*.json.gz")):
        try:
            d = json.load(gzip.open(f))
        except Exception:
            continue
        for c in d["cases"]:
            if not c["status"].startswith("EXCLUDED"):
                o = out / ("core%03d_b%06d.json.gz" % (d["core_index"], c["boundary_index"]))
                if not o.exists():
                    todo.append((d["core_index"], d["total_boundaries"], c["boundary_index"], o))
    for ci, n, bi, o in todo:
        idx = out / ("idx_core%03d_b%06d.json" % (ci, bi)); idx.write_text(json.dumps([bi]))
        t = time.time()
        r = subprocess.run([sys.executable, "-X", "utf8", str(W / "py_extend.py"), str(S / "k3prod_v4/pkg/code/codex"), "P3",
                            str(base / "pkg/data/p3_boundaries" / ("core_%03d.json.gz" % ci)), "0", str(n), "--sat", "--lean",
                            "--enc=seq", "--all-attachments", "--conflicts=3000000", "--indices=" + str(idx), "--out=" + str(o)],
                           capture_output=True, text=True, timeout=10800, creationflags=0x00004000)
        log.write("%s core %d b%d: %s (%.0fs) %s\n" % (time.strftime("%H:%M:%S"), ci, bi,
                  (r.stdout.strip().splitlines() or [""])[-1][:160], time.time() - t, r.stderr.strip()[-200:])); log.flush()
    if not LOOP:
        break
    time.sleep(120)
log.write("END\n"); log.close()
