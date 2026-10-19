"""Build the AWS package for the remaining 2K2 stage-2 work (LAB 19/10/2026): every core representative with Q12
colour factors whose stage-2 shard is missing locally; its 2K2N survivors are split in chunks of CHUNK boundaries.
Writes k2k2s2/{code_k2k2s2.tar.gz, manifest_k2k2s2.tsv, userdata_k2k2s2.sh}.  Run it only at launch time."""
import gzip
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

S = Path(__file__).resolve().parent
W = Path(r"C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/exploration_2026-10-16/gz5602_2026-10-19")
CHUNK = int(sys.argv[1]) if len(sys.argv) > 1 else 3
out = S / "k2k2s2"; pkg = out / "pkg"
if out.exists():
    shutil.rmtree(out)
(pkg / "code/lab").mkdir(parents=True); (pkg / "data/2k2n_boundaries").mkdir(parents=True); (pkg / "data/2k2_surv").mkdir(parents=True)
shutil.copytree(S / "k3prod_v4/pkg/code/codex", pkg / "code/codex")
shutil.copy(W / "py_extend.py", pkg / "code/lab/py_extend.py")
reps = [0, 1, 6, 7, 8, 9, 10, 21, 22, 25, 26, 27, 30, 45, 47, 50, 51, 52, 75, 76, 88]
lines = []; tot = 0
for ci in reps:
    bf = S / "pybd_2k2n_all" / ("core_%03d.json.gz" % ci)
    shutil.copy(bf, pkg / "data/2k2n_boundaries" / bf.name)
    if (S / "shards_2k2_stage2" / ("core%03d_stage2.json.gz" % ci)).exists():
        continue
    d = json.load(gzip.open(S / "shards_2k2n" / ("core%03d_all.json.gz" % ci)))
    surv = [c["boundary_index"] for c in d["cases"] if not c["status"].startswith("EXCLUDED")]
    n = d["total_boundaries"]
    for k in range(0, len(surv), CHUNK):
        part = surv[k:k + CHUNK]
        idx = "data/2k2_surv/core%03d_p%03d.json" % (ci, k // CHUNK)
        (pkg / idx).write_text(json.dumps(part))
        o = "data/2k2_stage2_shards/core%03d_stage2_p%03d.json.gz" % (ci, k // CHUNK)
        cmd = ("python -I -u -X utf8 code/lab/py_extend.py code/codex 2K2 data/2k2n_boundaries/core_%03d.json.gz 0 %d "
               "--sat --lean --enc=seq --indices=%s --out=%s" % (ci, n, idx, o))
        lines.append("k2s2_%03d_p%03d\t7200\t%s\t%s" % (ci, k // CHUNK, cmd, o)); tot += len(part)
(out / "manifest_k2k2s2.tsv").write_text("\n".join(lines) + "\n")
(pkg / "build.sh").write_text('#!/bin/bash\necho "no build step (LAB py_extend.py 2K2 + Codex 587f1fdd helpers)"\n')
files = sorted(str(p.relative_to(pkg)).replace("\\", "/") for p in pkg.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
(out / "filelist.txt").write_text("\n".join(files) + "\n")
import tarfile
with tarfile.open(out / "code_k2k2s2.tar.gz", "w:gz") as tf:
    for f in files:
        tf.add(pkg / f, arcname=f)
ud = (S / "p3prod/userdata_p3prod.sh").read_text().replace("p3prod", "k2k2s2")
(out / "userdata_k2k2s2.sh").write_text(ud)
h = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
print(json.dumps({"jobs": len(lines), "survivor_boundaries": tot, "tar_sha256": h(out / "code_k2k2s2.tar.gz"),
                  "manifest_sha256": h(out / "manifest_k2k2s2.tsv")}))
