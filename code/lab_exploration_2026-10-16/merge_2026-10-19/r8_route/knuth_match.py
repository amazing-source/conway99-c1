"""Knuth estimate of the 'matching tree' of R8 and sampled conquer (LAB 20/10/2026).

Tree: level 1 = the perfect matching M_0 of L_0 (each label of L_0 has exactly one neighbour in L_0: C1, letter 0),
level 2 = M_1 of L_1, level 3 = M_2, level 4 = M_3.  A node is kept iff unit propagation (pysat) of
F + (matchings fixed so far) finds no conflict.  Each level is enumerated completely by a DFS over partial matchings
with propagation at every step, so the number of children n_i of the visited node is exact.  The Knuth random walk
picks one child uniformly; prod(n_i) is an unbiased estimate of the number of nodes at that depth (leaves = 4-level
cubes).  With --conquer T, the leaf cube is given to cadical (binary, units appended to a copy of the CNF) with T
seconds; the verdict and time are recorded (TIMEOUT = censored).
Symmetry: level 1 can be restricted to the 52 G_0-orbit representatives (--m0reps): then n_1 = 52 orbit classes and
the walk picks a class with probability proportional to... uniform over classes, weight 52 (the estimate counts cubes
up to the G_0 action on M_0; every solution has a G_0-image whose M_0 is a representative).
usage: python knuth_match.py <cnf> <probes> <seed> <out jsonl> [--m0reps] [--levels 4] [--conquer T --cadical exe]
                             [--solver glucose4] [--budget seconds]"""
import itertools
import json
import os
import random
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
    cls = []
    with open(path) as fh:
        for line in fh:
            if not line or line[0] in "cp":
                continue
            lits = [int(t) for t in line.split()]
            if lits and lits[-1] == 0:
                lits.pop()
            cls.append(lits)
    return cls


class Tree:
    def __init__(self, M, sv):
        self.M, self.sv = M, sv
        self.L = {r: [i for i, l in enumerate(M.S) if r in l] for r in range(4)}
        self.calls = 0

    def prop(self, cube):
        self.calls += 1
        ok, imp = self.sv.propagate(assumptions=cube)
        return ok, imp

    def matchings(self, r, cube, limit=None):
        """All perfect matchings of L_r compatible with cube by unit propagation (list of literal lists)."""
        M = self.M
        Lr = self.L[r]
        out = []

        def dfs(unm, lits, cur):
            if limit is not None and len(out) >= limit:
                return
            if not unm:
                out.append(list(lits))
                return
            a = unm[0]
            for b in unm[1:]:
                v = M.var(a, b)
                if -v in cur:
                    continue
                ok, imp = self.prop(cube + lits + [v])
                if not ok:
                    continue
                dfs([u for u in unm if u not in (a, b)], lits + [v], set(imp))

        ok, imp = self.prop(cube)
        if not ok:
            return out
        dfs(list(Lr), [], set(imp))
        return out


def main():
    cnf, probes, seed, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    levels = int(opt("--levels", "4"))
    conquer = float(opt("--conquer", "0"))
    cad = opt("--cadical")
    budget = float(opt("--budget", "280"))
    t_start = time.time()
    M = r8lib.Model(14)
    cls = load_cnf(cnf)
    sv = Solver(name=opt("--solver", "glucose4"), bootstrap_with=cls)
    T = Tree(M, sv)
    rng = random.Random(seed)
    reps = m0_orbits(14) if "--m0reps" in sys.argv else None
    L0 = T.L[0]
    t_load = time.time() - t_start
    for pr in range(probes):
        if time.time() - t_start > budget:
            break
        t0 = time.time()
        cube = []
        ns = []
        path = []
        dead = False
        for lev in range(levels):
            r = lev
            if lev == 0 and reps is not None:
                k = rng.randrange(len(reps))
                rep, size = reps[k]
                pairs = set(frozenset(p) for p in rep)
                lits = []
                for a, b in itertools.combinations(L0, 2):
                    s, t = list(M.S[a] - {0})[0], list(M.S[b] - {0})[0]
                    if frozenset((s, t)) in pairs:
                        lits.append(M.var(a, b))
                ok, _ = T.prop(cube + lits)
                ns.append(len(reps))
                path.append({"m0case": k, "orbit": size, "ok": ok})
                if not ok:
                    dead = True
                    break
                cube = cube + lits
                continue
            opts = T.matchings(r, cube)
            ns.append(len(opts))
            if not opts:
                dead = True
                break
            ch = rng.choice(opts)
            path.append({"level": lev, "children": len(opts)})
            cube = cube + ch
        weight = 1
        for x in ns:
            weight *= x
        ok, imp = T.prop(cube)
        nfix = len([v for v in imp if abs(v) <= len(M.pairs)])
        rec = {"probe": pr, "seed": seed, "ns": ns, "dead": dead, "weight": weight, "fixed_edge_lits": nfix,
               "probe_s": round(time.time() - t0, 2), "prop_calls": T.calls}
        if not dead and conquer > 0 and time.time() - t_start + conquer + 10 < budget:
            # conquer: copy of the CNF + the propagated edge literals of the cube as units
            tmp = out + ".cube.cnf"
            units = [v for v in imp if abs(v) <= len(M.pairs)]
            with open(cnf) as fi, open(tmp, "w") as fo:
                head = None
                for line in fi:
                    if line.startswith("p cnf"):
                        p_, c_, nv, nc = line.split()
                        fo.write("p cnf %s %d\n" % (nv, int(nc) + len(units)))
                    else:
                        fo.write(line)
                for u in units:
                    fo.write("%d 0\n" % u)
            t1 = time.time()
            p = subprocess.Popen([cad, "-q", "-n", tmp], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            try:
                p.wait(timeout=conquer)
                st = {10: "SAT", 20: "UNSAT"}.get(p.returncode, "rc%d" % p.returncode)
            except subprocess.TimeoutExpired:
                p.kill()
                p.wait()
                st = "TIMEOUT"
            rec["conquer"] = st
            rec["conquer_s"] = round(time.time() - t1, 1)
            rec["cube"] = cube
            os.remove(tmp)
        rec["path"] = path
        print(json.dumps({k: v for k, v in rec.items() if k != "cube"}), flush=True)
        with open(out, "a") as fh:
            fh.write(json.dumps(rec) + "\n")
    print("load %.1f s, total %.1f s" % (t_load, time.time() - t_start), flush=True)


if __name__ == "__main__":
    main()
