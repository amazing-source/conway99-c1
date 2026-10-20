"""Solve saved cubes (from knuth_la.py records) on one or more CNFs of the R8 family with cadical (LAB 20/10/2026).
The cube literals are edge literals (variables 1..1326, the same numbering in every encoder used here), appended as
units.  usage: python cube_solve.py <records jsonl> <record indices e.g. 0,3> <seconds> <cadical exe> <out jsonl>
                                     <cnf1> [<cnf2> ...]   (sequential: one solver process at a time)"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from knuth_la import cadical, write_cube_cnf  # noqa: E402


def main():
    recs, which, T, exe, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4], sys.argv[5]
    cnfs = sys.argv[6:]
    rows = [json.loads(l) for l in open(recs) if l.strip()]
    rows = [r for r in rows if "cube" in r]
    for k in [int(t) for t in which.split(",")]:
        r = rows[k]
        for cnf in cnfs:
            tmp = out + ".tmp.cnf"
            write_cube_cnf(cnf, tmp, r["cube"])
            st, ts, conf = cadical(exe, tmp, T)
            os.remove(tmp)
            rec = {"record": k, "probe": r["probe"], "seed": r["seed"], "depth": r["depth"], "cnf": os.path.basename(cnf),
                   "status": st, "seconds": ts, "conflicts": conf}
            print(json.dumps(rec), flush=True)
            with open(out, "a") as fh:
                fh.write(json.dumps(rec) + "\n")


if __name__ == "__main__":
    main()
