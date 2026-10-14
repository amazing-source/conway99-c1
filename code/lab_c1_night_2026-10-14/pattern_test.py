"""Decide by cadical a small local pattern at a vertex x of srg(99,14,1,2).

A pattern = prescribed pairs "M_a pairs b with c" and forbidden pairs "M_a does not pair b with c"
(M_a = the matching induced on the 12 inner vertices outside the block of a; blocks {1,2}, ..., {13,14}).
Everything else is free. Used to see which short local statements the solver finds by itself.

usage: python pattern_test.py workdir limit name pos neg [tiles]
       pos, neg = a:b-c,d-e;a2:b-c      (empty string = none)
       tiles = "tiles" adds the 84 clauses of the tile lemma at x (three pairings of a grid force the fourth)
appends to pattern_log.txt: name verdict seconds
One process, one cadical call, 2 GB bound.
"""
import subprocess
import sys
import time

import h12_instance as H
import srg_sat as S

CADICAL = r"C:\Users\RESEARCHER\Desktop\Recherche_Conway\c1-codex\tools\win64\cadical.exe"


def parse(arg):
    out = []
    for part in arg.split(";"):
        if not part:
            continue
        a, _, pairs = part.partition(":")
        for p in pairs.split(","):
            b, c = (int(t) for t in p.split("-"))
            out.append((int(a), b, c))
    return out


def make_share(pos, neg):
    partner = {}
    for a, b, c in pos:
        assert partner.get((a, b), c) == c and partner.get((a, c), b) == b
        partner[(a, b)] = c
        partner[(a, c)] = b
    forbidden = {(a, min(b, c), max(b, c)) for a, b, c in neg}

    def share(a, b, b2):
        pb, pb2 = partner.get((a, b)), partner.get((a, b2))
        if pb is not None or pb2 is not None:
            return pb == b2
        if (a, min(b, b2), max(b, b2)) in forbidden:
            return False
        return None

    return share


def pair_lit(e, idx, a, b, b2):
    u, v = idx[(min(a, b), max(a, b))], idx[(min(a, b2), max(a, b2))]
    return e[(min(u, v), max(u, v))]


def add_tiles(enc, e, idx):
    """For blocks i != j with members (a, a2), (b, b2): the four literals M_a{b,b2}, M_a2{b,b2}, M_b{a,a2},
    M_b2{a,a2} are never exactly three true. Returns the number of clauses added."""
    count = 0
    for i in range(1, 8):
        for j in range(i + 1, 8):
            a, a2 = 2 * i - 1, 2 * i
            b, b2 = 2 * j - 1, 2 * j
            lits = [pair_lit(e, idx, a, b, b2), pair_lit(e, idx, a2, b, b2),
                    pair_lit(e, idx, b, a, a2), pair_lit(e, idx, b2, a, a2)]
            for s in range(4):
                head = lits[s]
                body = [lits[t] for t in range(4) if t != s]
                if head == S.T or any(t == S.F for t in body):
                    continue
                clause = [-t for t in body if t != S.T]
                if head != S.F:
                    clause.append(head)
                enc.add(*clause)
                count += 1
    return count


if __name__ == "__main__":
    workdir, limit, name = sys.argv[1], float(sys.argv[2]), sys.argv[3]
    pos, neg = parse(sys.argv[4]), parse(sys.argv[5])
    tiles = len(sys.argv) > 6 and sys.argv[6] == "tiles"
    n, k, lam, mu, fixed, mate, outer, idx = H.build(make_share(pos, neg))
    enc, e = S.encode(n, k, lam, mu, fixed)
    extra = add_tiles(enc, e, idx) if tiles else 0
    cnf = workdir + "/pattern.cnf"
    S.write_dimacs(enc, cnf)
    t0 = time.time()
    try:
        r = subprocess.run([CADICAL, "-q", cnf], capture_output=True, text=True, timeout=limit)
        res = r.stdout
    except subprocess.TimeoutExpired:
        res = ""
    dt = time.time() - t0
    verdict = "UNSAT" if "s UNSATISFIABLE" in res else ("SAT" if "s SATISFIABLE" in res else "UNKNOWN")
    line = "%s %s %.1f pos=%s neg=%s tiles=%d" % (name, verdict, dt, sys.argv[4], sys.argv[5], extra)
    print(line, flush=True)
    open("pattern_log.txt", "a").write(line + "\n")
