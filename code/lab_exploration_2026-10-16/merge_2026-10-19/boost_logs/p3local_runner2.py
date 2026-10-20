"""Second P3 runner (LAB 20/10/2026, boost while the PC is free): runs ONLY the sub-slices still queued in the first
runner (p3local/p3local_runner.py, which keeps its 3 running jobs).  Identical command and flags; separate output
and index names (suffix __r2) so the two runners never touch the same file; results in p3local2/p3local_done.jsonl.
Duplicates started later by the first runner are killed by boost/watchdog.py before they write anything
(py_extend.py writes its output only at the very end, via a .tmp file).
usage: python p3local_runner2.py <pkg dir> <timeout seconds> <job name> [<job name> ...]"""
import gzip
import json
import os
import re
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

PKG, TO, NAMES = sys.argv[1], float(sys.argv[2]), sys.argv[3:]
HERE = os.path.dirname(os.path.abspath(__file__))
DONE = os.path.join(HERE, "p3local_done.jsonl")
PY = sys.executable
lock = threading.Lock()
env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", NUMEXPR_NUM_THREADS="1")


def run(name):
    ci, bi, j = (int(v) for v in re.fullmatch(r"core(\d+)_b(\d+)_s(\d+)_n256", name).groups())
    total = json.load(gzip.open(os.path.join(PKG, "data/p3_boundaries/core_%03d.json.gz" % ci)))["boundary_count"]
    idx = os.path.join(PKG, "idx", "idx_%s__r2.json" % name)
    with open(idx, "w") as f:
        json.dump([bi], f)
    out = "out/%s__r2.json.gz" % name
    cmd = [PY, "-I", "-u", "-X", "utf8", "code/lab3/py_extend.py", "code/codex", "P3",
           "data/p3_boundaries/core_%03d.json.gz" % ci, "0", str(total), "--sat", "--lean", "--enc=seq",
           "--all-attachments", "--conflicts=3000000", "--att-slice=%d/256" % j, "--indices=idx/idx_%s__r2.json" % name,
           "--out=%s" % out]
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=PKG, env=env, capture_output=True, text=True, timeout=TO, creationflags=0x40)
        code, to = p.returncode, False
    except subprocess.TimeoutExpired:
        code, to = None, True
    wall = round(time.time() - t0, 1)
    status, case = None, {}
    f = os.path.join(PKG, out)
    if not to and os.path.exists(f):
        try:
            c = json.load(gzip.open(f))["cases"][0]
            status = c["status"]
            case = {k: c.get(k) for k in ("slice", "enumerated_total", "enumeration_sha256", "counts", "cpu_seconds")}
        except Exception:
            status = "UNREADABLE"
    rec = dict(id=name, core=ci, border=bi, sub=j, exit=code, timeout=to, wall=wall, status=status, runner=2,
               out=out, **case)
    with lock:
        with open(DONE, "a") as g:
            g.write(json.dumps(rec) + "\n")
        print("%s %s %s %.1fs" % (time.strftime("%H:%M:%S"), name, status if not to else "TIMEOUT", wall), flush=True)


with ThreadPoolExecutor(max_workers=len(NAMES)) as ex:
    list(ex.map(run, NAMES))
print("ALL JOBS VISITED", flush=True)
