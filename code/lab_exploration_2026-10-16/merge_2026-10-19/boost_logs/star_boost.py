"""Boost driver (LAB 20/10/2026): complete star of one near vertex for one line graph, with the residual form allowed
by the rule (delta = 1 if (tau|7) = +1, delta = 3 if (tau|7) = -1), at rank 39 (rho = 2) or 37 (rho = 0).
Tries x = 0, 1, ..., 11 until x is not in a transversal triangle, preps with star39_prep.py, runs star39.exe.
usage: python star_boost.py <seed> <rho 0|2> <outdir> <limit_s> [--tau any|-1|+1] [--x X]
prints one JSON line (prep info + engine result + wall times)."""
import json
import os
import subprocess
import sys
import time

MERGE = ("C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/"
         "work/exploration_2026-10-16/merge_2026-10-19")
PY = sys.executable
seed, rho, outdir, limit = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
tau = sys.argv[sys.argv.index("--tau") + 1] if "--tau" in sys.argv else "any"
xs = [int(sys.argv[sys.argv.index("--x") + 1])] if "--x" in sys.argv else list(range(12))
env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1")


def prep(x, delta, b):
    t = time.time()
    r = subprocess.run([PY, os.path.join(MERGE, "star39_prep.py"), str(seed), str(x), str(rho), str(delta), b,
                        "--tau", tau], capture_output=True, text=True, env=env, creationflags=0x40)
    if r.returncode != 0:
        return None, time.time() - t
    return json.loads(r.stdout.strip().splitlines()[-1]), time.time() - t


for x in xs:
    tag = "star%d_s%d_x%d" % (37 if rho == 0 else 39, seed, x)
    b = os.path.join(outdir, tag + ".bin")
    info, tp = prep(x, 3 if rho == 2 else 0, b)
    if info is None:
        continue
    if rho == 2 and info["delta_allowed_by_rule"] != 3:
        info, tp2 = prep(x, 1, b)
        tp += tp2
    t = time.time()
    with open(os.path.join(outdir, tag + ".out"), "w") as fo, open(os.path.join(outdir, tag + ".err"), "w") as fe:
        subprocess.run([os.path.join(MERGE, "star39.exe"), b, limit], stdout=fo, stderr=fe)
    te = time.time() - t
    res = open(os.path.join(outdir, tag + ".out")).read().strip()
    try:
        res = json.loads(res)
    except Exception:
        pass
    print(json.dumps({"tag": tag, "prep": info, "prep_s": round(tp, 2), "engine_s": round(te, 2), "result": res}),
          flush=True)
    break
