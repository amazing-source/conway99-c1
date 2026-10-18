"""Manifest of the second c3 pass with Gram covers (runs c3ga / c3gb, LAB 18/10/2026).
For every c3 template whose first pass is finished and left it open (it has a representative in c3o_open_pairs.tsv,
written by analyse_c3o.py), and not already submitted (optional list of submitted (src, index)), one chained job:
  1. gram_cover_enum2.py: complete list of the integer Grams allowed (900 s at most; else no verdict);
  2. gram_cover_branch.py --table full: Codex's exact all-in-one complete-star model + the table, 600 s CPU;
  3. gram_cover_crosscheck.py: Codex's own Gram enumerator on the same template, every difference explained (300 s).
Outputs: out/<job>.json (verdict), out/xc_<job>.json (cross-check), out/cv_<job>.json.gz (the cover itself).
usage: py -3 gen_c3gc.py <c3o_open_pairs.tsv> <c3o_excluded.tsv> <out manifest prefix> <parts> [submitted.tsv]"""
import random
import sys

reps_path, excl_path, prefix, parts = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
submitted = set()
if len(sys.argv) > 5:
    for line in open(sys.argv[5]):
        src, ti = line.split()[:2]
        submitted.add((src, int(ti)))
tag = {"code/lab_exploration_2026-10-16/c3_root_cover/c3_open_templates_k3_12.json.gz": "gz",
       "data/codex_c3_pilot_20261018/inputs/cle3_c3_g1_open.json": "g1",
       "data/codex_c3_pilot_20261018/inputs/cle3_c3_g2_open.json": "g2"}
templates = list(dict.fromkeys((line.split("\t")[0], int(line.split("\t")[1])) for line in open(reps_path)))
excluded = set()
for line in open(excl_path):
    src, ti = line.split()[:2]
    excluded.add((src, int(ti)))
todo = [k for k in templates if k not in excluded and k not in submitted]
random.Random(20261018).shuffle(todo)
L = "code/lab_exploration_2026-10-16/"
rows = []
for src, ti in todo:
    n = "s2_%s_%05d" % (tag[src], ti)
    cmd = ("mkdir -p out && python -I -u -X utf8 {L}gram_cover_enum2.py {src} {ti} 900 out/cv_{n}.json 10 && "
           "python -I -u -X utf8 {L}gram_cover_branch.py code/codex {src} --index {ti} --cover out/cv_{n}.json "
           "--seconds 600 --table full --output out/{n}.json ; "
           "python -I -u -X utf8 {L}gram_cover_crosscheck.py code/codex {src} {ti} out/cv_{n}.json 300 out/xc_{n}.json ; "
           "gzip -f out/cv_{n}.json").format(L=L, src=src, ti=ti, n=n)
    rows.append((n, 2400, cmd, "out/%s.json,out/xc_%s.json,out/cv_%s.json.gz" % (n, n, n)))
for p in range(parts):
    with open("%s_%s.tsv" % (prefix, "abcdefgh"[p]), "w", newline="\n") as f:
        for r in rows[p::parts]:
            f.write("%s\t%d\t%s\t%s\n" % r)
with open("%s_submitted.tsv" % prefix, "a", newline="\n") as f:
    for src, ti in todo:
        f.write("%s\t%d\n" % (src, ti))
print(len(templates), "open templates after pass 1;", len(excluded), "excluded by pass 1;", len(submitted), "already submitted;",
      len(todo), "jobs in", parts, "part(s)")
