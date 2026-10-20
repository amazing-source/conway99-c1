"""Boost batch (LAB 20/10/2026): complete-star test at a given global rank r for several line kinds, through
star_prep_gen.py (general 7-adic formalism) and star39.exe (STAR_NORANK=1 when c >= 2, where rank <= 7 + c is automatic).
For each (spec, seed): first x not in a transversal triangle; every variant in the list:
  "1", "3"  balanced residue with form type delta (the type is not fixed by a proved rule for these kinds, so the line
            dies only if every variant dies);
  "u"       unbalanced 7-torsion (r(T) = 1); if the star candidates span several torsion directions, one run per
            direction F_7 g (labels u0, u1, ...).
usage: python gen_batch.py <outdir> <r> <limit_s> <seeds a-b> <variants 1,3,u> <spec> [<spec> ...]   (JSON lines)"""
import json
import os
import re
import subprocess
import sys
import time

MERGE = ("C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/"
         "work/exploration_2026-10-16/merge_2026-10-19")
PY = sys.executable
outdir, r, limit = sys.argv[1], int(sys.argv[2]), sys.argv[3]
a, b = (int(v) for v in sys.argv[4].split("-"))
variants = sys.argv[5].split(",")
specs = sys.argv[6:]
env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1")


def prep(spec, seed, x, delta, bpath, extra):
    t = time.time()
    p = subprocess.run([PY, os.path.join(MERGE, "star_prep_gen.py"), spec, str(seed), "0", str(x), str(r), delta,
                        bpath] + extra, capture_output=True, text=True, env=env, creationflags=0x40)
    return p, time.time() - t


def engine(info, bpath):
    e2 = dict(env)
    if info["c"] >= 2:
        e2["STAR_NORANK"] = "1"
    t = time.time()
    q = subprocess.run([os.path.join(MERGE, "star39.exe"), bpath, limit], capture_output=True, text=True, env=e2)
    te = time.time() - t
    try:
        out = json.loads(q.stdout.strip())
    except Exception:
        out = q.stdout.strip()[-300:]
    os.remove(bpath)
    return out, te


for spec in specs:
    for seed in range(a, b + 1):
        for x in range(12):
            res, info, status = [], None, "ok"
            for var in variants:
                tag = "g%d_%s_s%d_x%d_v%s" % (r, spec.replace(":", "").replace(",", "-"), seed, x, var)
                bpath = os.path.join(outdir, tag + ".bin")
                extra = ["--unbal"] if var == "u" else []
                p, tp = prep(spec, seed, x, "0" if var == "u" else var, bpath, extra)
                msg = p.stdout + p.stderr
                if p.returncode != 0 and "transversal" in msg:
                    status = "next_x"
                    break
                if p.returncode != 0 and var == "u" and "possible directions" in msg:
                    nk = int(re.search(r"(\d+) possible directions", msg).group(1))
                    for k in range(nk):
                        bk = bpath.replace(".bin", "_k%d.bin" % k)
                        pk, tk = prep(spec, seed, x, "0", bk, extra + ["--kappa", str(k)])
                        if pk.returncode != 0:
                            res.append({"variant": "u%d" % k, "prep_error": (pk.stdout + pk.stderr)[-300:]})
                            continue
                        info = json.loads(pk.stdout.strip().splitlines()[-1])
                        out, te = engine(info, bk)
                        res.append({"variant": "u%d" % k, "prep_s": round(tk, 2), "engine_s": round(te, 2),
                                    "result": out})
                    continue
                if p.returncode != 0:
                    res.append({"variant": var, "prep_error": msg[-300:]})
                    continue
                info = json.loads(p.stdout.strip().splitlines()[-1])
                out, te = engine(info, bpath)
                res.append({"variant": var, "prep_s": round(tp, 2), "engine_s": round(te, 2), "result": out})
                if info["rho"] == 0 and var != "u":
                    break
            if status == "next_x":
                continue
            rec = {"spec": spec, "seed": seed, "x": x, "runs": res}
            if info:
                rec.update({"c": info["c"], "d": info["d"], "rho": info["rho"]})
            print(json.dumps(rec), flush=True)
            break
