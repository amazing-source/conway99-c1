"""Local spread sample of the P3 production (every STEP-th job of manifest_p3prod.tsv, offset OFF), BELOW_NORMAL,
one process per driver, <= 3600 s per job; outputs land in pkg/data/p3_shards with the AWS names (reusable).
usage: python local_sample_driver.py STEP OFF"""
import subprocess
import sys
import time
from pathlib import Path

base = Path(__file__).resolve().parent
pkg = base / "pkg"
STEP, OFF = int(sys.argv[1]), int(sys.argv[2])
jobs = [l.rstrip("\n").split("\t") for l in open(base / "manifest_p3prod.tsv", encoding="utf8") if l.strip()]
log = open(base / ("local_sample_%d_%d.log" % (STEP, OFF)), "a", encoding="utf8")
for k, (name, _cap, cmd, out) in enumerate(jobs):
    if k % STEP != OFF or (pkg / out).exists():
        continue
    args = cmd.split(); args[0] = sys.executable
    t = time.time()
    try:
        r = subprocess.run(args, cwd=pkg, capture_output=True, text=True, timeout=3600, creationflags=0x00004000)
        tail = (r.stdout.strip().splitlines() or [""])[-1][:240]
        ok = (pkg / out).exists()
        log.write("%s %s %s %.0fs %s %s\n" % (time.strftime("%H:%M:%S"), name, "OK" if ok else "FAIL", time.time() - t, tail,
                                             "" if ok else r.stderr.strip()[-300:]))
    except subprocess.TimeoutExpired:
        log.write("%s %s TIMEOUT\n" % (time.strftime("%H:%M:%S"), name))
    log.flush()
log.write("END\n"); log.close()
