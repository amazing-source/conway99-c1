"""Cost sample of the P3N exact profile SAT (one process at a time, BELOW_NORMAL, <= 90 s per call).
For each core representative: 4 boundaries at the middle of its cover.  Memory: one small process (< 400 MB)."""
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
fam = sys.argv[1] if len(sys.argv) > 1 else "P3N"
out = open(S / ("sample_%s.txt" % fam.lower()), "a", encoding="utf8")
for ci in [0, 1, 6, 7, 8, 9, 10, 21, 22, 25, 26, 27, 30, 45, 47, 50, 51, 52, 75, 76, 88]:
    bf = S / "pybd_p3_all" / ("core_%03d.json.gz" % ci)
    n = json.load(gzip.open(bf))["boundary_count"]
    st = n // 2
    t = time.time()
    try:
        r = subprocess.run([py, "-X", "utf8", str(W / "py_extend.py"), str(codex), fam, str(bf), str(st), "4",
                            "--sat", "--lean", "--enc=seq"], capture_output=True, text=True, timeout=90,
                           creationflags=0x00004000)
        last = (r.stdout.strip().splitlines() or [""])[-1]
        d = json.loads(last) if last.startswith("{") else {}
        line = "%03d n=%d start=%d statuses=%s cpu=%s wall=%.1f" % (ci, n, st, d.get("statuses"), d.get("cpu_seconds"),
                                                                    time.time() - t)
    except subprocess.TimeoutExpired:
        line = "%03d n=%d start=%d TIMEOUT>90s" % (ci, n, st)
    out.write(line + "\n"); out.flush()
out.write("END\n"); out.close()
