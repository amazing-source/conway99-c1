"""Driver (LAB 15/10/2026): kernel_milp.py on every object of a bundle, sequentially, one process at a time.
usage: python kernel_milp_all.py <bundle json> <log> [mode match|hfull] [first] [last]"""
import json
import os
import subprocess
import sys

bundle, log = sys.argv[1], sys.argv[2]
mode = sys.argv[3] if len(sys.argv) > 3 else "match"
d = json.load(open(bundle))
nobj = len(d["structures"]) if "structures" in d else 1
first = int(sys.argv[4]) if len(sys.argv) > 4 else 0
last = int(sys.argv[5]) if len(sys.argv) > 5 else nobj - 1
env = dict(os.environ, MODE=mode)
with open(log, "a", encoding="utf-8") as fh:
    for k in range(first, last + 1):
        r = subprocess.run([sys.executable, "kernel_milp.py", bundle, str(k), "300"], capture_output=True, text=True, env=env)
        out = [l for l in r.stdout.splitlines() if l.startswith("OPTIMUM") or l.startswith("MILP") or l.startswith("saved")
               or l.startswith("time limit")]
        fh.write("%d %s | %s%s\n" % (k, mode, " | ".join(out), (" | ERR " + r.stderr.strip().splitlines()[-1]) if r.returncode else ""))
        fh.flush()
