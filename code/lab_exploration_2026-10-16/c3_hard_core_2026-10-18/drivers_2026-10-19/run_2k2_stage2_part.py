"""Stage 2 of the 2K2 family: for every core representative with Q12 colour factors, the boundaries NOT excluded by
the 2K2N run (Q12 unknown) are run in full 2K2 mode (Q12 grid, rainbow attachments, Y-Y matching sigma).
Valid because every 2K2 configuration restricts to a 2K2N configuration with the same boundary and sigma (the 2K2N
constraints are a subset of the 2K2 ones).  Cores 20 and 23 need no stage 2 (no colour factor: EXCLUDED_Q12_COLOUR_FACTORS).
Waits for each 2K2N shard.  One process at a time, BELOW_NORMAL, <= 3600 s per call, memory < 500 MB."""
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
bd = S / "pybd_2k2n_all"
sh1 = S / "shards_2k2n"
sh2 = S / "shards_2k2_stage2"
sh2.mkdir(exist_ok=True)
log = open(S / ("run_2k2_stage2_part_%s.log" % sys.argv[1].split(",")[0]), "a", encoding="utf8")
reps = [int(x) for x in sys.argv[1].split(",")]
F = 0x00004000
for ci in reps:
    s1 = sh1 / ("core%03d_all.json.gz" % ci)
    while not s1.exists():
        time.sleep(20)
    d = json.load(gzip.open(s1))
    surv = [c['boundary_index'] for c in d['cases'] if not c['status'].startswith('EXCLUDED')]
    out = sh2 / ("core%03d_stage2.json.gz" % ci)
    if out.exists():
        continue
    if not surv:
        log.write("%s core %d: no 2K2N survivor (%d boundaries)\n" % (time.strftime("%H:%M:%S"), ci, len(d['cases'])))
        log.flush(); continue
    idxf = S / ("surv_2k2n_core%03d.json" % ci)
    idxf.write_text(json.dumps(surv))
    n = d['total_boundaries']
    t = time.time()
    try:
        r = subprocess.run([py, "-X", "utf8", str(W / "py_extend.py"), str(codex), "2K2", str(bd / ("core_%03d.json.gz" % ci)),
                            "0", str(n), "--sat", "--lean", "--enc=seq", "--indices=" + str(idxf), "--out=" + str(out)],
                           capture_output=True, text=True, timeout=3600, creationflags=F)
        last = (r.stdout.strip().splitlines() or [""])[-1][:300]
        log.write("%s core %d survivors=%d: %s (%.0fs) %s\n" % (time.strftime("%H:%M:%S"), ci, len(surv), last, time.time() - t,
                                                              r.stderr.strip()[-300:]))
    except subprocess.TimeoutExpired:
        log.write("%s core %d survivors=%d: TIMEOUT 3600 s\n" % (time.strftime("%H:%M:%S"), ci, len(surv)))
    log.flush()
log.write("END\n"); log.close()
