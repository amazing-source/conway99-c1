"""Package + manifest of run gc1a (LAB 18/10/2026): Gram covers in Codex's exact all-in-one complete-star model.
For each hard c3 template (the 17 left UNKNOWN by --all-matchings-variable at 600 s in run verif6b, plus 4378 as a
control, closed there in 521 s): two variants (--table anchors / --table full), 600 s CPU each; plus Codex's own
Gram enumerator on the same template (cross-check of the cover, gram_cover_crosscheck.py, 900 s).
usage: py -3 gen_gc1.py <cover dir> <template>..."""
import json
import shutil
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
cover_dir = Path(sys.argv[1])
temps = [int(x) for x in sys.argv[2:]]
W = Path(r"C:\Users\RESEARCHER\Downloads\conway_c2_researcher2_start_2026_09_30\conway_c2_researcher2_start_2026_09_30\work\exploration_2026-10-16")
src, pkg = here / "pkg_verif6", here / "pkg_gc1"
if pkg.exists():
    shutil.rmtree(pkg)
shutil.copytree(src, pkg)
lab = pkg / "code" / "lab_exploration_2026-10-16"
for name in ("gram_cover_branch.py", "gram_cover_crosscheck.py", "cle3_gram.py"):
    shutil.copy2(W / name, lab / name)
shutil.copy2(pkg / "code" / "codex" / "three_star_ambient_upper.py", lab / "three_star_ambient_upper.py")
(pkg / "data" / "gramcover").mkdir(parents=True, exist_ok=True)
cat = "code/lab_exploration_2026-10-16/c3_root_cover/c3_open_templates_k3_12.json.gz"
rows = []
for t in temps:
    best = None
    for name in ("lab2_%d.json" % t, "lab_%d.json" % t):
        p = cover_dir / name
        if p.exists() and json.load(open(p))["status"] == "COMPLETE":
            best = p
            break
    assert best is not None, "no complete cover for %d" % t
    shutil.copy2(best, pkg / "data" / "gramcover" / ("cover_%d.json" % t))
    cov = "data/gramcover/cover_%d.json" % t
    for table in ("anchors", "full"):
        name = "gc%s_%05d" % (table[0], t)
        rows.append((name, 1500, "mkdir -p out && python -I -u -X utf8 code/lab_exploration_2026-10-16/gram_cover_branch.py "
                     "code/codex %s --index %d --cover %s --seconds 600 --table %s --output out/%s.json" % (cat, t, cov, table, name),
                     "out/%s.json" % name))
    name = "xc_%05d" % t
    rows.append((name, 1500, "mkdir -p out && python -I -u -X utf8 code/lab_exploration_2026-10-16/gram_cover_crosscheck.py "
                 "code/codex %s %d %s 900 out/%s.json" % (cat, t, cov, name), "out/%s.json" % name))
with open(here / "manifest_gc1a.tsv", "w", newline="\n") as f:
    for r in rows:
        f.write("%s\t%d\t%s\t%s\n" % r)
print(len(rows), "tasks;", len(temps), "templates")
