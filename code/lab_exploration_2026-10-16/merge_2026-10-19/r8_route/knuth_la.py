"""Knuth estimate of a lookahead cube tree for R8, with sampled conquer (LAB 20/10/2026).

Level 0: the M_0 orbit class (52 classes under G_0; drawn uniformly, weight 52), imposed as assumption literals (the
true edges of M_0; the other 60 pairs of L_0 follow by unit propagation).  The lex-leader clauses of the (usually
trivial) stabiliser are NOT used here: conservative (over-counts the few symmetric classes).
Below: binary tree.  At each node: unit propagation (pysat); failed-literal probing on 'ncand' candidate free edge
variables (random sample, refreshed at each node); a candidate failing in one polarity forces the other (node
re-processed), failing in both closes the node.  Branching variable = candidate maximising (n+ + 1)(n- + 1), n+- =
number of new edge literals implied by each polarity (march-like).  The walk picks one polarity at random (weight x 2).
At depth D the node is an open cube; with --conquer T it is solved by cadical (CNF copy + all propagated edge literals as
units) for at most T seconds; TIMEOUT is recorded as censored at T.
Unbiased estimates (mean over probes): number of open cubes at depth D = E[W 1(open)], conquer cost = E[W t].
usage: python knuth_la.py <cnf> <probes> <seed> <out jsonl> --depth D [--ncand 30] [--conquer T --cadical exe]
                          [--budget 280] [--solver glucose4] [--class k]"""
import itertools
import json
import os
import random
import re
import subprocess
import sys
import time

from pysat.solvers import Solver

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r8lib  # noqa: E402
from build_cnf import m0_orbits  # noqa: E402


def opt(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def load_cnf(path):
    cls, nv = [], 0
    with open(path) as fh:
        for line in fh:
            if not line or line[0] == "c":
                continue
            if line[0] == "p":
                nv = int(line.split()[2])
                continue
            lits = [int(t) for t in line.split()]
            if lits and lits[-1] == 0:
                lits.pop()
            cls.append(lits)
    return cls, nv


def write_cube_cnf(src, dst, units):
    with open(src) as fi, open(dst, "w") as fo:
        for line in fi:
            if line.startswith("p cnf"):
                _, _, nv, nc = line.split()
                fo.write("p cnf %s %d\n" % (nv, int(nc) + len(units)))
            else:
                fo.write(line)
        for u in units:
            fo.write("%d 0\n" % u)


def cadical(exe, cnf, T):
    t1 = time.time()
    p = subprocess.Popen([exe, cnf], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    try:
        outp, _ = p.communicate(timeout=T)
        st = {10: "SAT", 20: "UNSAT"}.get(p.returncode, "rc%d" % p.returncode)
    except subprocess.TimeoutExpired:
        p.kill()
        outp, _ = p.communicate()
        st = "TIMEOUT"
    m = re.search(r"^c conflicts:\s+(\d+)", outp or "", re.M)
    return st, round(time.time() - t1, 2), int(m.group(1)) if m else None


def main():
    cnf, probes, seed, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    D = int(opt("--depth", "20"))
    ncand = int(opt("--ncand", "30"))
    T = float(opt("--conquer", "0"))
    cad = opt("--cadical")
    budget = float(opt("--budget", "280"))
    t_start = time.time()
    M = r8lib.Model(14)
    NE = len(M.pairs)
    cls, nv = load_cnf(cnf)
    sv = Solver(name=opt("--solver", "glucose4"), bootstrap_with=cls)
    del cls
    reps = m0_orbits(14)
    L0 = [i for i, l in enumerate(M.S) if 0 in l]
    rng = random.Random(seed)
    calls = [0]

    def prop(c):
        calls[0] += 1
        return sv.propagate(assumptions=c)

    t_load = round(time.time() - t_start, 1)
    for pr in range(probes):
        if time.time() - t_start > budget - (T + 15 if T else 15):
            break
        t0 = time.time()
        k = int(opt("--class")) if opt("--class") else rng.randrange(len(reps))
        rep, size = reps[k]
        pairs = set(frozenset(p) for p in rep)
        cube = [M.var(a, b) for a, b in itertools.combinations(L0, 2)
                if frozenset((list(M.S[a] - {0})[0], list(M.S[b] - {0})[0])) in pairs]
        W = len(reps)
        depth, forced, status = 0, 0, None
        node_log = []
        while True:
            ok, imp = prop(cube)
            if not ok:
                status = "closed"
                break
            base = set(imp)
            fixed = sum(1 for v in imp if abs(v) <= NE)
            if depth >= D:
                status = "open"
                break
            free = [v for v in range(1, NE + 1) if v not in base and -v not in base]
            if not free:
                status = "open"          # complete assignment, no conflict: a solution of the cube formula
                break
            cand = rng.sample(free, min(ncand, len(free)))
            best, bests, restart = None, -1, False
            for v in cand:
                okp, ip = prop(cube + [v])
                okn, ineg = prop(cube + [-v])
                if not okp and not okn:
                    status = "closed"
                    break
                if not okp or not okn:
                    cube = cube + ([-v] if not okp else [v])
                    forced += 1
                    restart = True
                    break
                sp = sum(1 for x in ip if abs(x) <= NE) - fixed
                sn = sum(1 for x in ineg if abs(x) <= NE) - fixed
                sc = (sp + 1) * (sn + 1)
                if sc > bests:
                    best, bests = v, sc
            if status == "closed":
                break
            if restart:
                continue
            lit = best if rng.random() < 0.5 else -best
            node_log.append([fixed, bests])
            cube = cube + [lit]
            W *= 2
            depth += 1
        rec = {"probe": pr, "seed": seed, "class": k, "orbit": size, "depth": depth, "status": status,
               "weight": W, "forced": forced, "probe_s": round(time.time() - t0, 2), "calls": calls[0],
               "fixed_at_leaf": fixed if status == "open" else None, "nodes": node_log}
        if status == "open" and T > 0:
            ok, imp = prop(cube)
            units = [v for v in imp if abs(v) <= NE]
            tmp = out + ".cube.cnf"
            write_cube_cnf(cnf, tmp, units)
            st, ts, conf = cadical(cad, tmp, T)
            os.remove(tmp)
            rec.update({"conquer": st, "conquer_s": ts, "conflicts": conf, "cube": cube})
        print(json.dumps({x: y for x, y in rec.items() if x not in ("cube", "nodes")}), flush=True)
        with open(out, "a") as fh:
            fh.write(json.dumps(rec) + "\n")
    print("load %.1f s, total %.1f s" % (t_load, time.time() - t_start), flush=True)


if __name__ == "__main__":
    main()
