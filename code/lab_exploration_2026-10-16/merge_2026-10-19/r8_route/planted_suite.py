"""Planted-solution suite for the CNF encodings (LAB 20/10/2026).  One process; children run sequentially.

For each planted K = 22 structure (control243.py): build my CNF with the real adjacency as units (implied L4B, XPAIR
and five-star exactness included) and run cadical: must be SAT.  Then the same with ONE edge flipped (3 random flips
per graph): must be UNSAT (a single flip always breaks an exact C1 count, see note).  Then the archive encoder
(stars_rank_2026-10-14/five_cnf.py, five stars, --base) on the unflipped structure: must be SAT.
usage: python planted_suite.py <dir with planted_*.json> <cadical exe> <archive five_cnf.py> <out jsonl> [names]"""
import glob
import json
import os
import random
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable


def cad(exe, cnf, limit=120):
    t0 = time.time()
    p = subprocess.run([exe, "-q", "-n", cnf], capture_output=True, text=True, timeout=limit)
    return {10: "SAT", 20: "UNSAT"}.get(p.returncode, "rc%d" % p.returncode), round(time.time() - t0, 1)


def main():
    d, exe, arch, out = sys.argv[1:5]
    rng = random.Random(7)
    tmp = os.path.join(d, "_suite.cnf")
    names = sys.argv[5:]
    for f in sorted(glob.glob(os.path.join(d, "planted_*.json"))):
        if names and not any(nm in f for nm in names):
            continue
        P = json.load(open(f))
        rec = {"planted": os.path.basename(f)}
        subprocess.run([PY, os.path.join(HERE, "build_cnf.py"), tmp, "--K", "22", "--implied", "L4B,XPAIR", "--five",
                        "--units", f], check=True, capture_output=True)
        rec["mine"] = cad(exe, tmp)
        flips = []
        n = len(P["labels"])
        E = set(tuple(e) for e in P["edges"])
        for _ in range(3):
            i, j = sorted(rng.sample(range(n), 2))
            Q = dict(P)
            Q["edges"] = [list(e) for e in sorted(E ^ {(i, j)})]
            fq = os.path.join(d, "_flip.json")
            json.dump(Q, open(fq, "w"))
            subprocess.run([PY, os.path.join(HERE, "build_cnf.py"), tmp, "--K", "22", "--implied", "L4B,XPAIR",
                            "--five", "--units", fq], check=True, capture_output=True)
            flips.append([P["labels"][i], P["labels"][j], (i, j) in E, cad(exe, tmp)])
        rec["mine_flipped"] = flips
        subprocess.run([PY, arch, "22", "0,1,2,3,4", tmp, "--reify", "--base", f], check=True, capture_output=True)
        rec["archive_five_cnf"] = cad(exe, tmp)
        print(json.dumps(rec), flush=True)
        with open(out, "a") as fh:
            fh.write(json.dumps(rec) + "\n")
    os.remove(tmp)


if __name__ == "__main__":
    main()
