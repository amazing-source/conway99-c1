"""Probe run c3p5 (LAB 19/10/2026): Codex's fixed-Gram probe (--eigen, layer 0, 30 s, same code as P4E) on the orbit
representatives (aut_orbits.py logic: permutations of the 7 root lines preserving J and every block partition) of the
complete Gram covers of the open c3 templates that no probe run has touched yet (covers produced after the P4E
manifest, mostly by c3ga2), restricted to covers of at most <maxg> Grams.
usage: py -3 gen_c3p5.py <out manifest> <maxg> <chunk> <seconds>"""
import glob, gzip, json, os, re, subprocess, sys
from collections import defaultdict
from itertools import permutations
out, maxg, CH, seconds = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
B = "conway99-c1-runs-733515672125"; L = "code/lab_exploration_2026-10-16"
cat = json.load(gzip.open("pkg_c3eig2/code/lab_exploration_2026-10-16/c3_root_cover/c3_open_templates_k3_12.json.gz"))["open"]
open_ = {int(l.split()[1]) for l in open("c3_ledger_open.tsv") if l.startswith("gz")}
p4e = set(int(re.search(r"--index (\d+)", l).group(1)) for l in open("manifest_c3p4e.tsv"))
tested = defaultdict(set)
for f in glob.glob("collect_*/files/out/*.json"):
    if not re.match(r"(eg|pe|l1|hd|or|l2)_gz_", os.path.basename(f)): continue
    try: r = json.load(open(f))
    except Exception: continue
    tested[int(r["template_index"])] |= {int(c["gram_selector"]) for c in r.get("cases", [])}
s3cov = {}
for line in open("s3_covers_list.txt"):
    run, name = line.split(); t = int(re.search(r"cv_s2_gz_(\d+)", name).group(1))
    if run == "c3ga2" or t not in s3cov or (run == "c3gb" and s3cov[t] == "c3ga"):
        s3cov[t] = run
count = {}
for run in ["c3ga", "c3gb", "c3ga2"]:
    for f in glob.glob("collect_%s/files/out/s2_gz_*.json" % run):
        try: r = json.load(open(f))
        except Exception: continue
        if run == s3cov.get(int(r["template_index"])) and r.get("gram_count") is not None:
            count[int(r["template_index"])] = r["gram_count"]
targets = sorted(t for t in open_ if t != 10006 and t not in p4e and not tested[t] and t in s3cov and count.get(t, 10**9) <= maxg)
os.makedirs("covers_p5", exist_ok=True)
rows, ngr, nrep = [], 0, 0
for t in targets:
    key = "runs/%s/files/out/cv_s2_gz_%05d.json.gz" % (s3cov[t], t)
    loc = "covers_p5/cv_s2_gz_%05d.json.gz" % t
    if not os.path.exists(loc):
        subprocess.run(["aws", "--profile", "frere", "--region", "eu-north-1", "s3", "cp", "s3://%s/%s" % (B, key), loc,
                        "--only-show-errors"], check=True, shell=False)
    tpl = cat[t]["template"]; E = [tuple(e) for e in tpl["nongrid_edges"]]; Es = set(E)
    parts = [{frozenset(p) for p in tpl["nontrivial_component_groups"][r]} for r in range(7)]
    aut = [p for p in permutations(range(7)) if {tuple(sorted((p[a], p[b]))) for a, b in E} == Es
           and all({frozenset(p[j] for j in P) for P in parts[r]} == parts[p[r]] for r in range(7))]
    cv = json.load(gzip.open(loc, "rt")); edges = [tuple(e) for e in cv["edges"]]
    assert sorted(edges) == sorted(E) and len(cv["grams"]) == count[t], (t, len(cv["grams"]), count[t])
    pos = {e: i for i, e in enumerate(edges)}
    qs = [[pos[tuple(sorted((p[a], p[b])))] for (a, b) in edges] for p in aut]
    m = len(edges); seen = set(); reps = []
    for gi, R in enumerate(cv["grams"]):
        k = min(tuple(R[q[i]][q[j]] for i in range(m) for j in range(m)) for q in qs)
        if k not in seen:
            seen.add(k); reps.append(gi)
    ngr += len(cv["grams"]); nrep += len(reps)
    for c in range(0, len(reps), CH):
        chunk = reps[c:c + CH]; jid = "p5_gz_%05d_%03d" % (t, c // CH)
        bundle = "data/covers/cv_s2_gz_%05d__%s.json.gz" % (t, jid)
        cmd = ("mkdir -p out data/covers && python -I %s/s3get.py %s %s %s && "
               "python -I code/codex/root_component_fixed_gram_probe.py --catalogue %s/c3_root_cover/c3_open_templates_k3_12.json.gz "
               "--index %d --bundle %s --grams %s --eigen --seconds %d --output out/%s.json ; rm -f %s"
               % (L, B, key, bundle, L, t, bundle, " ".join(map(str, chunk)), seconds, jid, bundle))
        rows.append((jid, str((seconds + 30) * len(chunk) + 600), cmd, "out/%s.json" % jid))
with open(out, "w", newline="\n") as f:
    for r in rows: f.write("\t".join(r) + "\n")
json.dump({"targets": targets}, open(out + ".targets.json", "w"))
print(len(targets), "templates,", ngr, "Grams,", nrep, "orbit representatives,", len(rows), "jobs")
