"""Manifest of AWS run 'verif1' (LAB, 18/10/2026).
  V3 : c_min >= 3, every k = 0..21 and every graph of cle_templates.cpp: enumerate, then CP-SAT (cle3_gram) AND HiGHS
       (cle3_gram_milp_check) on every template, then the template-by-template comparison.
  E2 / E1 : exact c_min = 2 and exact c_min = 1, every k = 0..21: the union-find enumerator with --la AND the
       independent linear-algebra enumerator with --dedup (k <= 4 split by the option of the first root).
  P3 : 100 matching tasks drawn uniformly among Codex's 106 852 complete-star tasks of the 10 052 open c >= 3
       templates; code 8d45031f, --seconds 60 --residual-eigen 2, with and without --no-transport.
usage: py -3 gen_manifest_verif.py <work dir with cle3_templates.py> <codex complete_star_manifest10052.json> <out.tsv>"""
import json
import random
import sys
from itertools import combinations, permutations

work, cmanifest, out = sys.argv[1:4]
sys.path.insert(0, work)
import cle3_templates as CT                             # noqa: E402

EDGES = list(combinations(range(7), 2))
EIDX = {e: k for k, e in enumerate(EDGES)}
std_reps = CT.graph_reps()                               # same list and order as cle_templates.cpp
PERMS = list(permutations(range(7)))


def permute(mask, p):
    r = 0
    for k, (a, b) in enumerate(EDGES):
        if mask >> k & 1:
            x, y = p[a], p[b]
            r |= 1 << EIDX[(x, y) if x < y else (y, x)]
    return r


la_reps = sorted({min(permute(m, p) for p in PERMS) for m in std_reps})   # orbit minima, as cle_templates_la.cpp
assert len(la_reps) == len(std_reps) == 588


def maxdeg(mask):
    d = [0] * 7
    for k, (a, b) in enumerate(EDGES):
        if mask >> k & 1:
            d[a] += 1
            d[b] += 1
    return max(d)


BLOCKS = {0: [0], 2: [1], 3: [1], 4: [1, 2, 2, 2], 5: [1] + [2] * 10, 6: [1] + [2] * 25 + [3] * 15}  # #blocks per partition


def n0(deg, cmin):
    return sum(1 for b in BLOCKS[deg] if 6 - deg + b >= cmin)


jobs = []
# E1 / E2 first (the long ones), low k first
for cmin in (1, 2):
    for k in range(0, 22):
        for prog, reps in (("s", std_reps), ("l", la_reps)):
            graphs = [m for m in reps if bin(m).count("1") == 21 - k]
            for g, mask in enumerate(graphs):
                splits = range(n0(maxdeg(mask), cmin)) if k <= 4 and maxdeg(mask) > 0 else [None]
                for a in splits:
                    jid = "e%d%s_k%02d_g%03d" % (cmin, prog, k, g) + ("" if a is None else "_f%02d" % a)
                    if prog == "s":
                        fix = "" if a is None else " --fix %d" % a
                        cmd = ("mkdir -p out && ./bin/cle_templates %d 1 %d --la --graph %d%s --out out/%s.jsonl > out/%s.sum.json"
                               " && gzip -f out/%s.jsonl" % (cmin, k, g, fix, jid, jid, jid))
                        outs = ["out/%s.sum.json" % jid, "out/%s.jsonl.gz" % jid]
                    else:
                        fix = "" if a is None else " --fix0 %d" % a
                        cmd = ("mkdir -p out && ./bin/cle_templates_la %d 1 %d --dedup --graph %d%s --out out/%s.txt > out/%s.sum.json"
                               " && gzip -f out/%s.txt" % (cmin, k, g, fix, jid, jid, jid))
                        outs = ["out/%s.sum.json" % jid, "out/%s.txt.gz" % jid]
                    jobs.append((jid, 7200, cmd, outs))
# P3 pilot
cm = json.load(open(cmanifest))
tasks = [(r["source_file"], r["template_index"], j) for r in cm["records"] for j in range(r["matching_count"])]
assert len(tasks) == cm["matching_tasks"] == 106852
sample = random.Random(20261018).sample(tasks, 100)
for n, (src, idx, j) in enumerate(sample):
    for tag, extra in (("t", ""), ("n", " --no-transport")):
        jid = "p3%s_%03d" % (tag, n)
        cmd = ("mkdir -p out && python -I -u -X utf8 code/codex/root_component_complete_star.py %s --index %d --matching-indices %d"
               " --seconds 60 --residual-eigen 2%s --output out/%s.json" % (src, idx, j, extra, jid))
        jobs.append((jid, 1800, cmd, ["out/%s.json" % jid]))
# V3 last (many short jobs)
for k in range(0, 22):
    graphs = [m for m in std_reps if bin(m).count("1") == 21 - k]
    for g, mask in enumerate(graphs):
        jid = "v3_k%02d_g%03d" % (k, g)
        cmd = ("mkdir -p out && ./bin/cle_templates 3 0 %d --graph %d --out out/%s.jsonl > out/%s.sum.json"
               " && python -I code/lab/cle3_gram_jsonl.py 300 out/%s_cp.json out/%s.jsonl > out/%s_cp.log"
               " && python -I code/lab/cle3_gram_milp_check.py 300 out/%s_hi.json out/%s.jsonl > out/%s_hi.log"
               " && python -I code/lab/compare_gram_verdicts.py out/%s_cp.json out/%s_hi.json > out/%s_cmp.json"
               " && gzip -f out/%s.jsonl out/%s_cp.json out/%s_hi.json" % ((k, g) + (jid,) * 14))
        jobs.append((jid, 10800, cmd, ["out/%s.sum.json" % jid, "out/%s.jsonl.gz" % jid, "out/%s_cp.json.gz" % jid,
                                      "out/%s_hi.json.gz" % jid, "out/%s_cmp.json" % jid, "out/%s_cp.log" % jid,
                                      "out/%s_hi.log" % jid]))
with open(out, "w", encoding="utf-8", newline="\n") as f:
    for jid, to, cmd, outs in jobs:
        f.write("%s\t%d\t%s\t%s\n" % (jid, to, cmd, ",".join(outs)))
kinds = {}
for jid, *_ in jobs:
    kinds[jid[:3]] = kinds.get(jid[:3], 0) + 1
json.dump({"pilot_sample": sample}, open(out + ".pilot.json", "w"))
print(len(jobs), "jobs", kinds)
