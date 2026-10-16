"""Case split of the plain five-star admissibility problem by the matching M_4, up to symmetry (LAB 16/10/2026).

Stars 0,1,2,3,4 (lines l = {0,1}, m = {2,3}, letter 4 of n = {4,5}).  The symmetry group of the model fixes 4 and 5,
acts on {0,1,2,3} by the dihedral group of order 8 preserving the lines, and on the outer letters 6..13 by the
hyperoctahedral group of order 384 (permute the four outer lines, swap mates inside them): order 3072.
M_4 is a perfect matching of the 12 letters {0,1,2,3,6,...,13} (the label {4,y} is matched to {4,z}).
We list one representative per orbit, write the CNF of stars_rank.build with M_4 fixed by unit clauses, and run cadical
on each case (conflict limit).  The plain problem is UNSAT iff every case is UNSAT.
usage: python five_split.py <out dir> <cadical exe> <conflict limit> [first case] [last case]"""
import itertools
import json
import os
import random
import subprocess
import sys
import time

from stars_rank import build

out, cad, climit = sys.argv[1], sys.argv[2], sys.argv[3]
first = int(sys.argv[4]) if len(sys.argv) > 4 else 0
last = int(sys.argv[5]) if len(sys.argv) > 5 else 10 ** 9
os.makedirs(out, exist_ok=True)
pts = [0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13]


def matchings(p):
    if not p:
        yield []
        return
    a = p[0]
    for i in range(1, len(p)):
        b = p[i]
        rest = p[1:i] + p[i + 1:]
        for m in matchings(rest):
            yield [(a, b)] + m


# group elements as letter maps
star_maps = []
for sl in (False, True):            # swap the two star lines
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
assert len(group) == 3072


def canon(m):
    best = None
    for g in group:
        key = tuple(sorted(tuple(sorted((g[a], g[b]))) for a, b in m))
        if best is None or key < best:
            best = key
    return best


reps = {}
for m in matchings(pts):
    c = canon(m)
    reps.setdefault(c, 0)
    reps[c] += 1
reps = sorted(reps.items(), key=lambda kv: kv[0])
print("perfect matchings: %d, orbits under the group of order 3072: %d" % (sum(v for _, v in reps), len(reps)),
      flush=True)
S, idx, e, F = build([0, 1, 2, 3, 4], random.Random(1))
base = "\n".join(" ".join(map(str, c)) + " 0" for c in F.clauses)
L4 = [l for l in S if 4 in l]
summary = []
for k, (rep, size) in enumerate(reps):
    if k < first or k > last:
        continue
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
    r = subprocess.run([cad, "-q", "-c", climit, path], capture_output=True, text=True)
    st = {10: "SAT", 20: "UNSAT"}.get(r.returncode, "UNKNOWN(%d)" % r.returncode)
    row = {"case": k, "M4": [list(p) for p in rep], "orbit_size": size, "status": st, "seconds": time.time() - t0}
    summary.append(row)
    print(json.dumps(row), flush=True)
    if st == "SAT":
        with open(os.path.join(out, "case%03d.model" % k), "w") as fh:
            fh.write(r.stdout)
    os.remove(path)
json.dump(summary, open(os.path.join(out, "summary_%d_%d.json" % (first, min(last, len(reps) - 1))), "w"), indent=1)
