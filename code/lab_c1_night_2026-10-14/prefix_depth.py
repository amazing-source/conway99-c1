"""How many of the 14 local matchings, chosen at random, does cadical need before it refutes the completion?

Generic local view of srg(99,14,1,2) at x (nothing assumed). For each seed: 14 uniformly random perfect matchings
M_1, ..., M_14 (M_a on the 12 inner vertices outside the block of a). For j = 1, 2, ...: call cadical on
"base + all pairs of M_1..M_j" with a time limit TAU; stop at the first UNSAT. Log prefix_log.txt:
  seed j verdict seconds
A random prefix is refuted earlier than a path kept alive by a search, so j is a LOWER indication of the depth
at which a "matchings first" search can prune. One process, cadical calls in sequence, 2 GB bound.

usage: python prefix_depth.py workdir n_seeds tau_seconds first_seed [order]
       order = "pairs" (default: 1,2,3,...: both ends of a block consecutively) or "spread" (1,3,5,...,13,2,4,...)
"""
import random
import shutil
import subprocess
import sys
import time

import h12_instance as H
import srg_sat as S

CADICAL = r"C:\Users\RESEARCHER\Desktop\Recherche_Conway\c1-codex\tools\win64\cadical.exe"
workdir, n_seeds, tau, first = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])
order = sys.argv[5] if len(sys.argv) > 5 else "pairs"
seq = list(range(1, 15)) if order == "pairs" else list(range(1, 15, 2)) + list(range(2, 15, 2))

n, k, lam, mu, fixed, mate, outer, idx = H.build(lambda a, b, b2: None)
enc, e = S.encode(n, k, lam, mu, fixed)
base = len(enc.clauses)
body = workdir + "/generic_body.cnf"
with open(body, "w") as f:
    for c in enc.clauses:
        f.write(" ".join(map(str, c)) + " 0\n")
print("generic local view: variables %d, clauses %d" % (enc.nv, base), flush=True)


def var(a, b, b2):
    u, v = idx[(min(a, b), max(a, b))], idx[(min(a, b2), max(a, b2))]
    return e[(min(u, v), max(u, v))]


def oracle(pairs):
    cnf = workdir + "/prefix.cnf"
    with open(cnf, "wb") as out:
        out.write(("p cnf %d %d\n" % (enc.nv, base + len(pairs))).encode())
        with open(body, "rb") as b:
            shutil.copyfileobj(b, out, 1 << 24)
        for a, b1, b2 in pairs:
            out.write(("%d 0\n" % var(a, b1, b2)).encode())
    t0 = time.time()
    try:
        r = subprocess.run([CADICAL, "-q", cnf], capture_output=True, text=True, timeout=tau)
        res = r.stdout
    except subprocess.TimeoutExpired:
        return "UNKNOWN", time.time() - t0
    v = "UNSAT" if "s UNSATISFIABLE" in res else ("SAT" if "s SATISFIABLE" in res else "UNKNOWN")
    return v, time.time() - t0


for seed in range(first, first + n_seeds):
    rng = random.Random(seed)
    pairs = []
    for j, a in enumerate(seq, 1):
        pts = [b for b in range(1, 15) if b != a and b != mate[a]]
        rng.shuffle(pts)
        pairs += [(a, pts[2 * i], pts[2 * i + 1]) for i in range(6)]
        v, dt = oracle(pairs)
        line = "%d %d %s %.1f %s" % (seed, j, v, dt, order)
        print(line, flush=True)
        open("prefix_log.txt", "a").write(line + "\n")
        if v != "UNKNOWN":
            break
