"""Parallel version of five_split.py (LAB 16/10/2026): the 34 orbit cases of M_4 for the plain five-star problem,
each solved by cadical with a wall-clock limit, on a pool of worker threads (one cadical process per worker).
A SAT case writes its model; results are appended to results.jsonl as they arrive.
usage: python five_split_par.py <out dir> <cadical exe> <workers> <seconds per case> [case list, e.g. 2-33]"""
import concurrent.futures as cf
import itertools
import json
import os
import random
import subprocess
import sys
import threading
import time

sys.argv_saved = list(sys.argv)
out, cad, workers, limit = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4])
sel = sys.argv[5] if len(sys.argv) > 5 else "0-33"
os.makedirs(out, exist_ok=True)

from stars_rank import build

pts = [0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13]


def matchings(p):
    if not p:
        yield []
        return
    a = p[0]
    for i in range(1, len(p)):
        rest = p[1:i] + p[i + 1:]
        for m in matchings(rest):
            yield [(a, p[i])] + m


star_maps = []
for sl in (False, True):
    for s0 in (False, True):
        for s1 in (False, True):
            g = {0: 0, 1: 1, 2: 2, 3: 3}
            if s0:
                g[0], g[1] = 1, 0
            if s1:
                g[2], g[3] = 3, 2
            if sl:
                g = {k: {0: 2, 1: 3, 2: 0, 3: 1}[v] for k, v in g.items()}
            star_maps.append(g)
outer_lines = [(6, 7), (8, 9), (10, 11), (12, 13)]
outer_maps = []
for perm in itertools.permutations(range(4)):
    for flips in itertools.product((0, 1), repeat=4):
        g = {}
        for i, (a, b) in enumerate(outer_lines):
            c, d = outer_lines[perm[i]]
            if flips[i]:
                c, d = d, c
            g[a], g[b] = c, d
        outer_maps.append(g)
group = [dict(list(s.items()) + list(o.items())) for s in star_maps for o in outer_maps]


def canon(m):
    return min(tuple(sorted(tuple(sorted((g[a], g[b]))) for a, b in m)) for g in group)


reps = {}
for m in matchings(pts):
    c = canon(m)
    reps[c] = reps.get(c, 0) + 1
reps = sorted(reps.items(), key=lambda kv: kv[0])
assert len(reps) == 34
lo, hi = (int(t) for t in sel.split("-"))
S, idx, e, F = build([0, 1, 2, 3, 4], random.Random(1))
base = "\n".join(" ".join(map(str, c)) + " 0" for c in F.clauses)
L4 = [l for l in S if 4 in l]
lock = threading.Lock()


def run_case(k):
    rep, size = reps[k]
    pairs = set(frozenset(p) for p in rep)
    units = []
    for x, y in itertools.combinations(L4, 2):
        a = list(x - {4})[0]
        b = list(y - {4})[0]
        v = e[(idx[x], idx[y])]
        units.append(v if frozenset((a, b)) in pairs else -v)
    path = os.path.join(out, "case%03d.cnf" % k)
    with open(path, "w") as fh:
        fh.write("p cnf %d %d\n" % (F.n, len(F.clauses) + len(units)))
        fh.write(base + "\n")
        for u in units:
            fh.write("%d 0\n" % u)
    t0 = time.time()
    p = subprocess.Popen([cad, "-q", path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        so, se = p.communicate(timeout=limit)
        st = {10: "SAT", 20: "UNSAT"}.get(p.returncode, "UNKNOWN(%d)" % p.returncode)
    except subprocess.TimeoutExpired:
        p.kill()
        so, se = p.communicate()
        st = "TIMEOUT"
    row = {"case": k, "M4": [list(q) for q in rep], "orbit_size": size, "status": st, "seconds": round(time.time() - t0, 1)}
    with lock:
        with open(os.path.join(out, "results.jsonl"), "a") as fh:
            fh.write(json.dumps(row) + "\n")
        if st == "SAT":
            with open(os.path.join(out, "case%03d.model" % k), "w") as fh:
                fh.write(so)
    os.remove(path)
    return row


with cf.ThreadPoolExecutor(max_workers=workers) as ex:
    for r in ex.map(run_case, range(lo, hi + 1)):
        pass
print("all done", flush=True)
