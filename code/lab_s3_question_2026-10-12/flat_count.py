"""Lab session, 2026-10-12. Complete parity skeleton problem (hybrid encoding + the 720 parity chains) with the extra
assumption "at least k of the 60 pairs through P = 0 are flat" and "some pair is split".
UNSAT for k means: in a non-trivial skeleton every vertex has at most k - 1 flat pairs, hence at most 81 (k - 1) / 2 flat
pairs in all.
python flat_count.py <tmp dir> <seconds> <k> [<k> ...]"""
import sys, os, subprocess, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from local_lib import *
import full_hybrid, parity_hybrid
tmp, tl = sys.argv[1], float(sys.argv[2]); ks = [int(a) for a in sys.argv[3:]]
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
nv0, base, ev, xs = full_hybrid.build([])
nvv = [nv0]
def new(): nvv[0] += 1; return nvv[0]
base.append([-vs[0] for vs in xs.values()])
for W in parity_hybrid.families():
    acc = xs[W[0]][0]
    for p in W[1:]:
        t = new(); a, b = acc, xs[p][0]
        base += [[-a, -b, -t], [a, b, -t], [a, -b, t], [-a, b, t]]
        acc = t
    base.append([acc])
P = 0; flats = [xs[k][0] for k in sorted(xs) if P in k]; assert len(flats) == 60
nbase = nvv[0]
for k in ks:
    nvv[0] = nbase; cl = list(base)
    # sequential counter: s[i][j] = at least j flats among the first i+1
    prev = None
    for i, l in enumerate(flats):
        cur = [None] + [new() for _ in range(k)]
        for j in range(1, k + 1):
            pj = prev[j] if prev else None; pj1 = (prev[j - 1] if j > 1 else "T") if prev else ("T" if j == 1 else None)
            c = [-cur[j]] + ([pj] if pj is not None else [])
            cl.append(c + [l])                                   # cur_j -> prev_j or l
            if pj1 != "T": cl.append(c + ([pj1] if pj1 is not None else []))   # cur_j -> prev_j or prev_{j-1}
        prev = cur
    cl.append([prev[k]])
    path = os.path.join(tmp, "fc_%d.cnf" % os.getpid())
    with open(path, "w", newline="\n") as f:
        f.write("p cnf %d %d\n" % (nvv[0], len(cl)))
        for c in cl: f.write(" ".join(map(str, c)) + " 0\n")
    t0 = time.time()
    try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
    except subprocess.TimeoutExpired: out = ""
    res = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"
    print("at least %d flat pairs at P, some pair split: %s (%.1f s)" % (k, res, time.time() - t0), flush=True)
    try: os.remove(path)
    except OSError: pass
