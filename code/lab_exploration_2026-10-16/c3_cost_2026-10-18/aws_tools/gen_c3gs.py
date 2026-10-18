"""Third c3 pass (LAB 18/10/2026): Gram-by-Gram split (gram_cover_split.py, C R = 0 added) for the templates that the
second pass (table of all their Grams, 600 s) left UNKNOWN.  Their complete covers are the ones the second pass
computed and uploaded (runs/<run>/files/out/cv_<job>.json.gz); they are fetched here and shipped in the package.
Each Gram first goes through the two moment tests (moment_bounds.py, LAB from scratch, and Codex's
root_component_corner_moment_bounds at 63e87d62, ranks <= 5), then the corner filter, then the exact model with R
fixed, vertex signature tables and C R = 0.  Covers above <slice size> Grams are cut into slices (verdict per slice;
the template is excluded iff all its slices are SLICE_ALL_INFEASIBLE).
usage: py -3 gen_c3gs.py <c3g_open.tsv> <run name of pass 2> <slice size> <per-gram s> <budget per slice s> <out manifest> <pkg dir>"""
import os
import shutil
import subprocess
import sys

open_path, run, slice_size, per_gram, cap, out_manifest, pkg = (sys.argv[1], sys.argv[2], int(sys.argv[3]),
                                                               float(sys.argv[4]), float(sys.argv[5]), sys.argv[6], sys.argv[7])
cat = {"gz": "code/lab_exploration_2026-10-16/c3_root_cover/c3_open_templates_k3_12.json.gz",
       "g1": "data/codex_c3_pilot_20261018/inputs/cle3_c3_g1_open.json",
       "g2": "data/codex_c3_pilot_20261018/inputs/cle3_c3_g2_open.json"}
os.makedirs(os.path.join(pkg, "data", "covers"), exist_ok=True)
A = ["aws", "--profile", "frere", "--region", "eu-north-1"]
B = "conway99-c1-runs-733515672125"
rows, skipped = [], []
import math
for line in open(open_path):
    n, g = line.split()[:2]
    g = int(g)
    _, tag, ti = n.split("_")
    dst = os.path.join(pkg, "data", "covers", "cv_%s.json.gz" % n)
    if not os.path.exists(dst):
        r = subprocess.run(A + ["s3", "cp", "s3://%s/runs/%s/files/out/cv_%s.json.gz" % (B, run, n), dst, "--only-show-errors"])
        if r.returncode:
            skipped.append((n, g, "no cover file"))
            continue
    parts = max(1, math.ceil(g / slice_size))
    for i in range(parts):
        job = "sp_%s_%03d_%03d" % (n[3:], i, parts)
        cmd = ("mkdir -p out && python -I -u -X utf8 code/lab_exploration_2026-10-16/gram_cover_split.py code/codex %s "
               "--index %d --cover data/covers/cv_%s.json.gz --per-gram %g --budget %g --slice %d/%d --moment-filter "
               "--codex-moment code/codex_63e87d62 --corner-filter --signature-tables --keep-going --output out/%s.json"
               % (cat[tag], int(ti), n, per_gram, cap, i, parts, job))
        rows.append((job, int(cap + 3600), cmd, "out/%s.json" % job))
rows.sort(key=lambda r: -r[1])                      # longest first
with open(out_manifest, "w", newline="\n") as f:
    for r in rows:
        f.write("%s\t%d\t%s\t%s\n" % r)
print(len(rows), "jobs;", len(skipped), "templates skipped:", skipped[:20])
