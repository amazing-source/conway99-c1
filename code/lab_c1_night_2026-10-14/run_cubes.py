"""Target T1: for the representatives K0..K1-1 of cube_reps.txt, fix the five lines through [+1,+2] and call cadical.

usage: python run_cubes.py K0 K1 seconds_per_cube workdir
One process at a time (cadical is run sequentially; declared memory bound 2 GB). Results are appended to
cubes_log.txt:   K  orbit_size  verdict  seconds
The base formula (srg(99,14,1,2) seen from a vertex whose 14 matchings respect the blocks) is written once; each
cube adds at most 15 unit clauses (the five lines through the outer vertex [+1,+2]).
"""
import ast
import shutil
import subprocess
import sys
import time

import affine_cube as AC
import srg_sat as S

CADICAL = r"C:\Users\RESEARCHER\Desktop\Recherche_Conway\c1-codex\tools\win64\cadical.exe"

k0, k1, limit, workdir = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
reps = [ast.literal_eval(line) for line in open("cube_reps.txt")]
mate = {a: (a + 1 if a % 2 == 1 else a - 1) for a in range(1, 15)}
n, k, lam, mu, fixed, _, outer, idx = S.local_view(lambda a, b: mate[b])
enc, e = S.encode(n, k, lam, mu, fixed)
base_clauses = len(enc.clauses)
body = workdir + "/t1_body.cnf"
with open(body, "w") as f:
    for c in enc.clauses:
        f.write(" ".join(map(str, c)) + " 0\n")


def ov(p, q):
    a, b = AC.iv(*p), AC.iv(*q)
    return idx[(min(a, b), max(a, b))]


base = ov((1, 1), (2, 1))
for K in range(k0, min(k1, len(reps))):
    size, F = reps[K]
    del enc.clauses[base_clauses:]
    for tm in F:
        pts = [ov(*edge) for edge in tm]
        for u, v in ((base, pts[0]), (base, pts[1]), (pts[0], pts[1])):
            enc.assert_true(e[(min(u, v), max(u, v))])
    extra = enc.clauses[base_clauses:]
    cnf = workdir + "/cube.cnf"
    with open(cnf, "wb") as out:
        out.write(("p cnf %d %d\n" % (enc.nv, base_clauses + len(extra))).encode())
        with open(body, "rb") as b:
            shutil.copyfileobj(b, out, 1 << 24)
        for c in extra:
            out.write((" ".join(map(str, c)) + " 0\n").encode())
    t0 = time.time()
    try:
        # this build of cadical has no -t option: the time limit is the subprocess timeout (the child is killed)
        r = subprocess.run([CADICAL, "-q", cnf], capture_output=True, text=True, timeout=limit)
        res = r.stdout
    except subprocess.TimeoutExpired:
        res = ""
    dt = time.time() - t0
    verdict = "UNSAT" if "s UNSATISFIABLE" in res else ("SAT" if "s SATISFIABLE" in res else "UNKNOWN")
    line = "%d %d %s %.1f" % (K, size, verdict, dt)
    print(line, flush=True)
    with open("cubes_log.txt", "a") as f:
        f.write(line + "\n")
    if verdict == "SAT":
        with open("cube_%d_model.txt" % K, "w") as f:
            f.write(res)
