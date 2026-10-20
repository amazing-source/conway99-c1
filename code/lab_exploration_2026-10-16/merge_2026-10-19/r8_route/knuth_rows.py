"""Knuth estimate of the X-attachment tree of R8 ("rows first"), with sampled conquer of the base (LAB 20/10/2026).

A row is (x, r) with x in X = {{4,t}} and r a star: by (C1) N(x) n L_r is a 2-subset of L_r.  The walk fixes the 32
rows in a static order (x_6 rows r = 0..3, then x_7, ...).  At each row all 2-subsets {y, y'} of L_r whose two edge
variables are not already false are tested by unit propagation of F + cube + (x~y, x~y'); the consistent ones are the
children (n_i).  One is drawn uniformly; prod(n_i) estimates the number of labelled X-attachments that survive unit
propagation (divide by the group order 3072 for a count up to symmetry, exact when stabilisers are trivial).
After the 32 rows, the cube (all X-B adjacencies) is conquered by cadical for at most T s (base completion + X-X edges).
Option --m0case: start from the representative of an M_0 class (assumptions), drawn uniformly (weight 52).
usage: python knuth_rows.py <cnf> <probes> <seed> <out jsonl> [--conquer T --cadical exe] [--budget 280]
                            [--rows N (stop after N rows)] [--m0]"""
import itertools
import json
import os
import random
import sys
import time

from pysat.solvers import Solver

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r8lib  # noqa: E402
from build_cnf import m0_orbits  # noqa: E402
from knuth_la import cadical, load_cnf, write_cube_cnf  # noqa: E402


def opt(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def main():
    cnf, probes, seed, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    T = float(opt("--conquer", "0"))
    cad = opt("--cadical")
    budget = float(opt("--budget", "280"))
    nrows = int(opt("--rows", "32"))
    t_start = time.time()
    M = r8lib.Model(14)
    NE = len(M.pairs)
    cls, nv = load_cnf(cnf)
    sv = Solver(name="glucose4", bootstrap_with=cls)
    del cls
    rng = random.Random(seed)
    L = {r: [i for i, l in enumerate(M.S) if r in l] for r in range(4)}
    Xi = list(range(len(M.B), M.n))
    rows = [(x, r) for x in Xi for r in range(4)][:nrows]
    reps = m0_orbits(14)
    L0 = L[0]
    for pr in range(probes):
        if time.time() - t_start > budget - (T + 20 if T else 20):
            break
        t0 = time.time()
        cube, W, ns, dead = [], 1, [], False
        if "--m0" in sys.argv:
            k = rng.randrange(len(reps))
            pairs = set(frozenset(p) for p in reps[k][0])
            cube = [M.var(a, b) for a, b in itertools.combinations(L0, 2)
                    if frozenset((list(M.S[a] - {0})[0], list(M.S[b] - {0})[0])) in pairs]
            W = len(reps)
        for (x, r) in rows:
            ok, imp = sv.propagate(assumptions=cube)
            if not ok:
                dead = True
                ns.append(0)
                break
            fx = set(imp)
            cand = [y for y in L[r] if -M.var(x, y) not in fx]
            opts = []
            for y, z in itertools.combinations(cand, 2):
                a, b = M.var(x, y), M.var(x, z)
                ok2, _ = sv.propagate(assumptions=cube + [a, b])
                if ok2:
                    opts.append((a, b))
            ns.append(len(opts))
            if not opts:
                dead = True
                break
            a, b = rng.choice(opts)
            cube = cube + [a, b]
            W *= len(opts)
        rec = {"probe": pr, "seed": seed, "ns": ns, "dead": dead, "weight": W, "probe_s": round(time.time() - t0, 2)}
        if not dead:
            ok, imp = sv.propagate(assumptions=cube)
            units = [v for v in imp if abs(v) <= NE]
            rec["fixed"] = len(units)
            if T > 0 and ok:
                tmp = out + ".cube.cnf"
                write_cube_cnf(cnf, tmp, units)
                st, ts, conf = cadical(cad, tmp, T)
                os.remove(tmp)
                rec.update({"conquer": st, "conquer_s": ts, "conflicts": conf})
            rec["cube"] = cube
        print(json.dumps({k2: v for k2, v in rec.items() if k2 != "cube"}), flush=True)
        with open(out, "a") as fh:
            fh.write(json.dumps(rec) + "\n")
    print("total %.1f s" % (time.time() - t_start), flush=True)


if __name__ == "__main__":
    main()
