"""Smallest set of prescribed pairs that cadical still refutes, with a checked proof.

Local view at a vertex x of srg(99,14,1,2), nothing assumed (generic body), plus unit clauses "M_a pairs b with c".
Loop: cadical with a DRAT proof -> drat-trim checks the proof and returns the clauses it used -> keep only the
units that occur in that core -> repeat until the set of units is stable. Then try to delete the remaining units
one at a time (a deletion is kept only if cadical still answers UNSAT within the limit; the final set is checked
once more by drat-trim). The result is a machine-checked forbidden local pattern; it need not be minimum.

usage: python core_units.py workdir limit name units
       units = a:b-c,d-e;a2:b-c ...   or a family name of family.py followed by ;extra units, e.g.
               kk5;11:1-3,2-5,4-7,6-9,8-13,10-14
appends to core_log.txt. One process at a time, 2 GB bound.
"""
import os
import shutil
import subprocess
import sys
import time

import family as FAM
import h12_instance as H
import srg_sat as S

TOOLS = r"C:\Users\RESEARCHER\Desktop\Recherche_Conway\c1-codex\tools\win64"
CADICAL = TOOLS + r"\cadical.exe"
DRAT = TOOLS + r"\drat-trim.exe"


def parse_units(arg):
    units = []
    for part in arg.split(";"):
        if not part:
            continue
        if ":" not in part:
            for a, pairs in FAM.prescriptions(part).items():
                units += [(a, b, c) for b, c in pairs]
            continue
        a, _, pairs = part.partition(":")
        for p in pairs.split(","):
            b, c = (int(t) for t in p.split("-"))
            units.append((int(a), min(b, c), max(b, c)))
    return sorted(set(units))


class Body:
    def __init__(self, workdir):
        n, k, lam, mu, fixed, mate, outer, idx = H.build(lambda a, b, b2: None)
        self.enc, self.e = S.encode(n, k, lam, mu, fixed)
        self.idx = idx
        self.workdir = workdir
        self.path = workdir + "/core_body.cnf"
        with open(self.path, "w") as f:
            for c in self.enc.clauses:
                f.write(" ".join(map(str, c)) + " 0\n")
        self.base = len(self.enc.clauses)

    def var(self, a, b, b2):
        u, v = self.idx[(min(a, b), max(a, b))], self.idx[(min(a, b2), max(a, b2))]
        return self.e[(min(u, v), max(u, v))]

    def write(self, units, cnf):
        with open(cnf, "wb") as out:
            out.write(("p cnf %d %d\n" % (self.enc.nv, self.base + len(units))).encode())
            with open(self.path, "rb") as b:
                shutil.copyfileobj(b, out, 1 << 24)
            for a, b1, b2 in units:
                out.write(("%d 0\n" % self.var(a, b1, b2)).encode())

    def solve(self, units, limit, proof=None):
        cnf = self.workdir + "/core_case.cnf"
        self.write(units, cnf)
        cmd = [CADICAL, "-q", cnf] + ([proof] if proof else [])
        t0 = time.time()
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=limit)
            res = r.stdout
        except subprocess.TimeoutExpired:
            res = ""
        v = "UNSAT" if "s UNSATISFIABLE" in res else ("SAT" if "s SATISFIABLE" in res else "UNKNOWN")
        return v, time.time() - t0, cnf

    def core(self, units, limit):
        """Return (verdict, used units) with verdict in VERIFIED / NOT VERIFIED / the cadical verdict."""
        proof = self.workdir + "/core_case.drat"
        v, dt, cnf = self.solve(units, limit, proof)
        if v != "UNSAT":
            return v, units
        corefile = self.workdir + "/core_case.core"
        if os.path.exists(corefile):
            os.remove(corefile)
        r = subprocess.run([DRAT, cnf, proof, "-c", corefile, "-w"], capture_output=True, text=True)
        if "s VERIFIED" not in r.stdout:
            return "NOT VERIFIED", units
        lit = {self.var(*u): u for u in units}
        used = set()
        with open(corefile) as f:
            for line in f:
                t = line.split()
                if len(t) == 2 and t[1] == "0" and t[0].lstrip("-").isdigit() and int(t[0]) in lit:
                    used.add(lit[int(t[0])])
        return "VERIFIED", sorted(used)


def fmt(units):
    by = {}
    for a, b, c in units:
        by.setdefault(a, []).append("%d-%d" % (b, c))
    return ";".join("%d:%s" % (a, ",".join(v)) for a, v in sorted(by.items()))


if __name__ == "__main__":
    workdir, limit, name = sys.argv[1], float(sys.argv[2]), sys.argv[3]
    units = parse_units(sys.argv[4])
    body = Body(workdir)
    log = open("core_log.txt", "a")

    def say(s):
        print(s, flush=True)
        log.write(s + "\n")
        log.flush()

    say("%s start: %d units" % (name, len(units)))
    while True:
        v, used = body.core(units, limit)
        say("%s core pass: %s, %d -> %d units" % (name, v, len(units), len(used)))
        if v != "VERIFIED" or len(used) == len(units):
            break
        units = used
    if v == "VERIFIED":
        i = 0
        while i < len(units):
            trial = units[:i] + units[i + 1:]
            v2, dt, _ = body.solve(trial, limit)
            if v2 == "UNSAT":
                units = trial
            else:
                i += 1
        v, used = body.core(units, limit)
        say("%s after deletion: %s, %d units (core uses %d)" % (name, v, len(units), len(used)))
        say("%s pattern: %s" % (name, fmt(units)))
