"""Layer-2 rerun (Codex's fixed-Gram probe, --eigen --layer 2) of every Gram still UNKNOWN in some probe output
(eg_, pe_, l1_, hd_) of a template that is open in the ledger, minus every Gram INFEASIBLE in any probe output
(LAB 18/10/2026; pilot: gz 984 Grams 136, 290, 665 UNKNOWN at layer 1 / 120 s, INFEASIBLE at layer 2 in 26-68 s).
gz 10006 is left out (layer 2 and layer 4 UNKNOWN at 200 s on its Gram 2).
usage: py -3 gen_c3l2.py <out manifest> <seconds> <chunk>"""
import glob, json, os, re, sys
from collections import defaultdict
out, seconds, CH = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
B = "conway99-c1-runs-733515672125"; L = "code/lab_exploration_2026-10-16"
open_ = {int(l.split()[1]) for l in open("c3_ledger_open.tsv") if l.startswith("gz")}
cover = {}
for man in glob.glob("manifest_*.tsv"):
    for line in open(man):
        m = re.search(r"s3get\.py \S+ (runs/\S+/cv_s2_gz_(\d+)\.json\.gz)", line)
        if m:
            cover.setdefault(int(m.group(2)), m.group(1))
unk, inf = defaultdict(set), defaultdict(set)
for f in glob.glob("collect_*/files/out/*.json"):
    b = os.path.basename(f)
    if not re.match(r"(eg|pe|l1|hd|or)_gz_", b):
        continue
    try:
        r = json.load(open(f))
    except Exception:
        continue
    t = int(r["template_index"])
    for c in r.get("cases", []):
        (inf if c.get("status") == "INFEASIBLE" else unk if c.get("status") == "UNKNOWN" else defaultdict(set))[t].add(int(c["gram_selector"]))
rows, ngr, missing = [], 0, []
for t in sorted(open_):
    if t == 10006:
        continue
    gs = sorted(unk[t] - inf[t])
    if not gs:
        continue
    if t not in cover:
        missing.append(t); continue
    ngr += len(gs)
    for c in range(0, len(gs), CH):
        chunk = gs[c:c + CH]
        jid = "l2_gz_%05d_%03d" % (t, c // CH)
        cv = "data/covers/cv_s2_gz_%05d__%s.json.gz" % (t, jid)
        cmd = ("mkdir -p out data/covers && python -I %s/s3get.py %s %s %s && "
               "python -I code/codex/root_component_fixed_gram_probe.py --catalogue %s/c3_root_cover/c3_open_templates_k3_12.json.gz "
               "--index %d --bundle %s --grams %s --eigen --layer 2 --seconds %d --output out/%s.json ; rm -f %s"
               % (L, B, cover[t], cv, L, t, cv, " ".join(map(str, chunk)), seconds, jid, cv))
        rows.append((jid, str((seconds + 40) * len(chunk) + 600), cmd, "out/%s.json" % jid))
with open(out, "w", newline="\n") as f:
    for r in rows:
        f.write("\t".join(r) + "\n")
tmpl = len({r[0][6:11] for r in rows})
print(len(rows), "jobs,", ngr, "Grams over", tmpl, "open templates; open templates with no UNKNOWN Gram on record:",
      sum(1 for t in open_ if t != 10006 and not (unk[t] - inf[t])), "; missing cover key:", missing[:10])
