"""Size of a complete search for srg(99,14,1,2) by "local matchings first, SAT oracle at every node".

Local view at a vertex x: the graph is determined by the 14 matchings M_a (which pairs of outer vertices sharing
the inner vertex a are adjacent) and by the adjacencies of disjoint outer pairs. Search tree: the matchings are
filled one pair at a time (inner vertices in the order 1..14, smallest unmatched point first, all possible
partners as children). A node is dead when cadical refutes "base formula + the pairs chosen so far" within TAU
seconds; otherwise it is kept and expanded. No symmetry is used.

This script does not run the search. It estimates its size by Knuth's method: random descents, at each level all
children are tested, one surviving child is chosen uniformly, the estimate of the number of nodes at level d is the
product of the numbers of surviving children above. Output: one line per probe and per level in knuth_log.txt
  probe level inner_vertex children tested_alive weight_so_far seconds
One process, cadical calls in sequence, 2 GB bound.

usage: python knuth_probe.py workdir n_probes tau_seconds wall_budget_seconds seed
"""
import random
import shutil
import subprocess
import sys
import time

import h12_instance as H
import srg_sat as S

CADICAL = r"C:\Users\RESEARCHER\Desktop\Recherche_Conway\c1-codex\tools\win64\cadical.exe"
workdir, n_probes, tau, budget, seed = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5])
rng = random.Random(seed)
t_start = time.time()

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
    """pairs: list of (a, b, b2). Returns 'UNSAT', 'SAT' or 'UNKNOWN'."""
    cnf = workdir + "/probe.cnf"
    with open(cnf, "wb") as out:
        out.write(("p cnf %d %d\n" % (enc.nv, base + len(pairs))).encode())
        with open(body, "rb") as b:
            shutil.copyfileobj(b, out, 1 << 24)
        for a, b1, b2 in pairs:
            out.write(("%d 0\n" % var(a, b1, b2)).encode())
    try:
        r = subprocess.run([CADICAL, "-q", cnf], capture_output=True, text=True, timeout=tau)
        res = r.stdout
    except subprocess.TimeoutExpired:
        return "UNKNOWN"
    if "s UNSATISFIABLE" in res:
        return "UNSAT"
    if "s SATISFIABLE" in res:
        with open("knuth_SAT_model.txt", "w") as f:
            f.write(repr(pairs) + "\n" + res)
        return "SAT"
    return "UNKNOWN"


def next_choice(pairs):
    """First inner vertex with an incomplete matching and its smallest unmatched point; None if all complete."""
    matched = {a: set() for a in range(1, 15)}
    for a, b1, b2 in pairs:
        matched[a].add(b1)
        matched[a].add(b2)
    for a in range(1, 15):
        pts = [b for b in range(1, 15) if b != a and b != mate[a] and b not in matched[a]]
        if pts:
            return a, pts[0], pts[1:]
    return None


for probe in range(n_probes):
    pairs = []
    weight = 1.0
    level = 0
    while True:
        if time.time() - t_start > budget:
            print("wall budget reached", flush=True)
            sys.exit(0)
        ch = next_choice(pairs)
        if ch is None:
            line = "%d %d - complete_local_type_alive weight=%.3e" % (probe, level, weight)
            print(line, flush=True)
            open("knuth_log.txt", "a").write(line + "\n")
            break
        a, b, partners = ch
        t0 = time.time()
        alive = []
        for b2 in partners:
            v = oracle(pairs + [(a, b, b2)])
            if v == "SAT":
                print("SAT FOUND", flush=True)
                sys.exit(0)
            if v == "UNKNOWN":
                alive.append(b2)
        dt = time.time() - t0
        line = "%d %d %d %d %d %.3e %.1f" % (probe, level, a, len(partners), len(alive), weight, dt)
        print(line, flush=True)
        open("knuth_log.txt", "a").write(line + "\n")
        if not alive:
            break
        weight *= len(alive)
        pairs.append((a, b, rng.choice(alive)))
        level += 1
