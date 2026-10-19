"""LAB local driver for the remaining K3 production (manifest_k3prod_v4.tsv, Codex code 587f1fdd).
One job at a time (one process), Windows BELOW_NORMAL priority, at most 300 s per job, resume by existing output.
Memory bound declared: one job loads one boundary cover (core 0: about 255k boundaries), well under 1 GB."""
import subprocess
import sys
import time
from pathlib import Path

base = Path(__file__).resolve().parent
pkg = base / "pkg"
py = sys.executable
log = open(base / "local_run.log", "a", encoding="utf8")
jobs = [l.rstrip("\n").split("\t") for l in open(base / "manifest_k3prod_v4.tsv", encoding="utf8") if l.strip()]
flags = 0x00004000 if sys.platform == "win32" else 0          # BELOW_NORMAL_PRIORITY_CLASS
done = failed = 0
t0 = time.time()
for name, _cap, cmd, out in jobs:
    if (pkg / out).exists():
        done += 1
        continue
    args = cmd.split()
    assert args[0] == "python"
    args[0] = py
    t = time.time()
    try:
        r = subprocess.run(args, cwd=pkg, capture_output=True, text=True, timeout=300, creationflags=flags)
        ok = r.returncode == 0 and (pkg / out).exists()
        tail = (r.stdout.strip().splitlines() or [""])[-1][:200]
        err = r.stderr.strip()[-300:]
    except subprocess.TimeoutExpired:
        ok, tail, err = False, "", "TIMEOUT 300 s"
    done += ok; failed += (not ok)
    log.write(f"{time.strftime('%H:%M:%S')} {name} {'OK' if ok else 'FAIL'} {time.time() - t:.1f}s {tail} {'' if ok else err}\n")
    log.flush()
log.write(f"END done={done} failed={failed} wall={time.time() - t0:.0f}s\n")
log.close()
