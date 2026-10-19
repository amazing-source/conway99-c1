"""2K2N (and 2K2) full run: boundaries for all 23 core representatives, then the frontier + exact profile SAT on every
boundary.  One process at a time, Windows BELOW_NORMAL, <= 1200 s per call; memory < 500 MB per process."""
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
fam = sys.argv[1]
bd = S / ("pybd_%s_all" % fam.lower())
sh = S / ("shards_%s" % fam.lower())
sh.mkdir(exist_ok=True)
log = open(S / ("run_%s_part.log" % fam.lower()), "a", encoding="utf8")
reps = [int(x) for x in sys.argv[2].split(",")]
F = 0x00004000
for ci in reps:
    bf = bd / ("core_%03d.json.gz" % ci)
    if not bf.exists():
        t = time.time()
        r = subprocess.run([py, "-X", "utf8", str(W / "py_boundary.py"), str(codex), str(W / "paircores8.json"),
                            str(W / "paircore_orbits16.json"), fam, str(bd), str(ci)], capture_output=True, text=True,
                           timeout=1200, creationflags=F)
        log.write("%s boundary core %d: %s (%.0fs)\n" % (time.strftime("%H:%M:%S"), ci, r.stdout.strip()[-200:], time.time() - t))
        log.flush()
    d = json.load(gzip.open(bf))
    n = d.get("boundary_count", 0)
    out = sh / ("core%03d_all.json.gz" % ci)
    if d["status"] != "COMPLETE_BOUNDARY_COVER" or out.exists():
        log.write("core %d: %s, n=%d, shard exists=%s\n" % (ci, d["status"], n, out.exists())); log.flush()
        continue
    t = time.time()
    try:
        r = subprocess.run([py, "-X", "utf8", str(W / "py_extend.py"), str(codex), fam, str(bf), "0", str(n),
                            "--sat", "--lean", "--enc=seq", "--out=" + str(out)], capture_output=True, text=True,
                           timeout=1200, creationflags=F)
        last = (r.stdout.strip().splitlines() or [""])[-1][:300]
        log.write("%s extend core %d n=%d: %s (%.0fs) %s\n" % (time.strftime("%H:%M:%S"), ci, n, last, time.time() - t,
                                                             r.stderr.strip()[-300:]))
    except subprocess.TimeoutExpired:
        log.write("%s extend core %d n=%d: TIMEOUT 1200 s\n" % (time.strftime("%H:%M:%S"), ci, n))
    log.flush()
log.write("END\n"); log.close()
