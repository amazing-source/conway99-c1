"""Third-line extension test, combinatorics only (LAB 16/10/2026).

For a four-star structure S (stars 0..3, lines l = {0,1}, m = {2,3}) and each outer line n = {2k, 2k+1}: relabel the
letters by the transposition (4 2k)(5 2k+1) so that n becomes {4,5}, fix the adjacency of S, and ask CP-SAT for an
admissible six-star structure on the 60 labels meeting {0,...,5} (C1 exact for the six star letters, C1' upper bounds
for the other letters, C2 caps).  In a Conway graph the block of S together with any third line through v is such a
structure, so INFEASIBLE for one n means S is not the (l,m)-block of a Conway graph in which n is a line at v ...
and every outer line of S is a line at v.  So INFEASIBLE for ONE n already excludes S.
usage: python ext3line.py <seconds per line> <out json> <germ json> [...]"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
secs = sys.argv[1]
out = sys.argv[2]
files = sys.argv[3:]
res = []
for f in files:
    d = json.load(open(f))
    if len(d.get("labels", [])) != 44 or "edges" not in d:
        continue
    row = {"file": f, "lines": {}}
    for k in range(2, 7):
        a, b = 2 * k, 2 * k + 1
        perm = {i: i for i in range(14)}
        perm[4], perm[a], perm[5], perm[b] = a, 4, b, 5
        rl = [sorted(perm[y] for y in l) for l in d["labels"]]
        tmp = os.path.join(tempfile.gettempdir(), "ext3line_base.json")
        json.dump({"labels": rl, "edges": d["edges"]}, open(tmp, "w"))
        env = dict(os.environ, BASE=tmp, HREL="")
        o = os.path.join(tempfile.gettempdir(), "ext3line_out.json")
        r = subprocess.run([sys.executable, os.path.join(HERE, "cp6.py"), "0,1,2,3,4,5", secs, o], env=env,
                           capture_output=True, text=True)
        st = json.load(open(o))["status"] if os.path.exists(o) else "ERROR " + r.stderr[-300:]
        row["lines"]["%d,%d" % (a, b)] = st
        if os.path.exists(o):
            os.remove(o)
    res.append(row)
    print(os.path.basename(f), row["lines"], flush=True)
json.dump(res, open(out, "w"), indent=1)
