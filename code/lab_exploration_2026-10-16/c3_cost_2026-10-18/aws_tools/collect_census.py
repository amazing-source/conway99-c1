"""Collect and cross-check the exact c_min = 2 and c_min = 1 censuses of runs verif1a (k = 0..21, split by the first
root's option) and verif3a (k = 0 only, orbit-reduced split) (LAB, 18/10/2026).
For every (c_min, k): union of the union-find enumerator's files vs union of the linear-algebra enumerator's files,
compared up to S7 by compare_enumerators.key (own canonical form).  Writes census_c12.json with the counts and, per
(c_min, k), a deduplicated jsonl.gz of the surviving templates (std format) for the Gram phase.
usage: py -3 collect_census.py <collect dir of verif1a> <collect dir of verif3a> <work dir with compare_enumerators.py> <out dir>"""
import glob
import gzip
import json
import os
import re
import sys
from collections import defaultdict

c1, c3, work, outdir = sys.argv[1:5]
sys.argv = [sys.argv[0], "--std", "--la"]               # compare_enumerators parses argv at import; neutralise it
sys.path.insert(0, work)
import importlib.util                                    # noqa: E402
spec = importlib.util.spec_from_file_location("CE", os.path.join(work, "compare_enumerators.py"))
CE = importlib.util.module_from_spec(spec)
spec.loader.exec_module(CE)
os.makedirs(outdir, exist_ok=True)
files = defaultdict(lambda: {"s": [], "l": []})
for d in (c1, c3):
    for f in glob.glob(os.path.join(d, "files", "out", "*")):
        m = re.match(r"([eo])([12])([sl])_k(\d\d)_", os.path.basename(f))
        if not m or not (f.endswith(".jsonl.gz") or f.endswith(".txt.gz")):
            continue
        files[(int(m.group(2)), int(m.group(4)), m.group(1))][m.group(3)].append(f)
report = {}
for (cmin, k, src) in sorted(files):
    fs = files[(cmin, k, src)]
    std, la = {}, set()
    for f in fs["s"]:
        for line in gzip.open(f, "rt"):
            t = json.loads(line)
            key = CE.key(t["graph_mask"], [[tuple(B) for B in blocks] for blocks in t["nontrivial_component_groups"]])
            std.setdefault(key, t)
    for f in fs["l"]:
        for line in gzip.open(f, "rt"):
            fields = line.strip().split("|")
            parts = [[tuple(int(ch) for ch in b) for b in fld.split(".")] if fld else [] for fld in fields[1:]]
            la.add(CE.key(int(fields[0]), parts))
    sk = set(std)
    rep = {"std_files": len(fs["s"]), "la_files": len(fs["l"]), "std_up_to_S7": len(sk), "la_up_to_S7": len(la),
           "only_std": len(sk - la), "only_la": len(la - sk), "identical": sk == la}
    report["c%d_k%02d_%s" % (cmin, k, src)] = rep
    print(cmin, k, src, json.dumps(rep), flush=True)
    with gzip.open(os.path.join(outdir, "census_c%d_k%02d_%s.jsonl.gz" % (cmin, k, src)), "wt") as g:
        for key in sorted(std):
            g.write(json.dumps(std[key]) + "\n")
json.dump(report, open(os.path.join(outdir, "census_c12.json"), "w"), indent=1)
