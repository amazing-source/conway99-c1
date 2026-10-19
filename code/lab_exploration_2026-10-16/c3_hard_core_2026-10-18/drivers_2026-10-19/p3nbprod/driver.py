"""P3NB local production driver: every STEP-th job of jobs.tsv (offset OFF), one process at a time, BELOW_NORMAL,
<= 3600 s per job, frozen program p3nbprod/py_extend.py.  usage: python driver.py STEP OFF"""
import subprocess, sys, time
from pathlib import Path
P = Path(__file__).resolve().parent; S = P.parent
STEP, OFF = int(sys.argv[1]), int(sys.argv[2])
jobs = [l.rstrip("\n").split("\t") for l in open(P / "jobs.tsv", encoding="utf8") if l.strip()]
log = open(P / ("driver_%d_%d.log" % (STEP, OFF)), "a", encoding="utf8")
for k, (name, ci, s, n, total, out) in enumerate(jobs):
    if k % STEP != OFF or Path(out).exists():
        continue
    t = time.time()
    try:
        r = subprocess.run([sys.executable, "-X", "utf8", str(P / "py_extend.py"), str(S / "k3prod_v4/pkg/code/codex"), "P3NB",
                            str(S / "pybd_p3nb_all" / ("core_%03d.json.gz" % int(ci))), s, n, "--sat", "--lean", "--enc=seq",
                            "--out=" + out], cwd=str(P), capture_output=True, text=True, timeout=3600, creationflags=0x00004000)
        tail = (r.stdout.strip().splitlines() or [""])[-1][:240]
        ok = Path(out).exists()
        log.write("%s %s %s %.0fs %s %s\n" % (time.strftime("%H:%M:%S"), name, "OK" if ok else "FAIL", time.time() - t, tail,
                                             "" if ok else r.stderr.strip()[-300:]))
    except subprocess.TimeoutExpired:
        log.write("%s %s TIMEOUT\n" % (time.strftime("%H:%M:%S"), name))
    log.flush()
log.write("END\n"); log.close()
