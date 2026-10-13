"""Step 1: build a compact index of every pair-level result record found on this machine (READ-ONLY on the sources).

Sources read:
  (1) git blobs results/<lid>_<k>_<n>.jsonl of the 255 local remote-tracking branches origin/run/*  of LAB/aws_repo (git ls-tree + git cat-file);
  (2) the working-tree copies aws_repo/resultats_q/*/results, aws_repo/resultats/*/results, aws_repo/resultats_ci/*/results;
  (3) the lab PC folders data/finishC/stream/<lid>/chunks.jsonl, data/finishC/golay/<lid>/chunks.jsonl, data/finishC/sweep/extra/*/ *.jsonl.
Records are de-duplicated on (lid, kind, chunk, range, sha256|pair_files_sha256, t, machine, verdict counts).
Output: records_compact.jsonl in the session scratchpad (an intermediate; regenerate with this script).
Usage: python -I index_records.py"""
import sys, os, re, json, glob, time, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kslib as K

t0 = time.time()
seen = {}; recs = []; stat = collections.Counter(); bad = []

def add(d, src, fname=None, oid=None, srctype=""):
    if "verdicts" not in d or d.get("kind") == "resolve": stat["skipped_no_verdicts:" + srctype] += 1; return
    c = K.compact(d, src, fname, oid)
    key = json.dumps([c["lid"], c["kind"], c["chunk"], c["range"], c["sha256"] or c["pfs"], c["t"], c["machine"], c["verdicts"]], sort_keys=True)
    if key in seen:
        seen[key]["dup_srcs"].append(src); stat["dup:" + srctype] += 1; return
    c["dup_srcs"] = []; c["srctype"] = srctype
    seen[key] = c; recs.append(c); stat["new:" + srctype] += 1

# (1) git blobs
blobs = [(b, p, o) for (b, p, o) in K.branch_result_blobs() if re.match(r"^results/\d{3}_\d+_\d+\.jsonl$", p)]
print("branch result blobs (name matches lid_k_n):", len(blobs), "distinct oids:", len({o for _, _, o in blobs}), "t=%.0fs" % (time.time() - t0), flush=True)
oid2meta = collections.defaultdict(list)
for b, p, o in blobs: oid2meta[o].append((b, p))
oids = sorted(oid2meta)
n = 0
nmiss = 0
for oid, data in K.read_blobs(oids):
    b, p = oid2meta[oid][0]
    if data is None: nmiss += 1; bad.append(("missing blob", b, p)); continue
    for line in data.decode("utf-8", errors="replace").splitlines():
        if '"verdicts"' not in line: continue
        try: d = json.loads(line)
        except ValueError: bad.append(("json", b, p)); continue
        add(d, "git:%s:%s" % (b.replace("origin/", ""), p), os.path.basename(p), oid, "git")
    n += 1
print("blobs read:", n, "records so far:", len(recs), "t=%.0fs" % (time.time() - t0), flush=True)

# (2) working tree
for pat, tag in ((K.REPO + r"\resultats_q\*\results\*.jsonl", "wt_q"), (K.REPO + r"\resultats\*\results\*.jsonl", "wt_res"), (K.REPO + r"\resultats_ci\*\results\*.jsonl", "wt_ci")):
    for f in glob.glob(pat):
        bn = os.path.basename(f)
        if not re.match(r"^\d{3}_\d+_\d+\.jsonl$", bn): continue
        for line in open(f, encoding="utf-8", errors="replace"):
            if '"verdicts"' not in line: continue
            try: d = json.loads(line)
            except ValueError: bad.append(("json", f)); continue
            add(d, "wt:" + f.replace(K.REPO, "").lstrip("\\"), bn, None, tag)
print("after working tree:", len(recs), "t=%.0fs" % (time.time() - t0), flush=True)

# (3) lab folders
for f in sorted(glob.glob(K.LAB + r"\data\finishC\stream\*\chunks.jsonl")) + sorted(glob.glob(K.LAB + r"\data\finishC\golay\*\chunks.jsonl")):
    lid = os.path.basename(os.path.dirname(f))
    for i, line in enumerate(open(f, encoding="utf-8", errors="replace")):
        if not line.strip(): continue
        try: d = json.loads(line)
        except ValueError: bad.append(("json", f, i)); continue
        add(d, "lab:%s#%d" % (f.replace(K.LAB, "").lstrip("\\"), i), None, None, "lab_chunks")
for f in sorted(glob.glob(K.LAB + r"\data\finishC\sweep\extra\*\*.jsonl")):
    for i, line in enumerate(open(f, encoding="utf-8", errors="replace")):
        if not line.strip(): continue
        d = json.loads(line)
        add(d, "lab:%s#%d" % (f.replace(K.LAB, "").lstrip("\\"), i), os.path.basename(f), None, "lab_extra")
print("total compact records:", len(recs), dict(stat), "bad lines:", len(bad), "t=%.0fs" % (time.time() - t0), flush=True)

with open(K.INDEX, "w", encoding="utf-8") as w:
    for c in recs: w.write(json.dumps(c) + "\n")
print("wrote", K.INDEX, os.path.getsize(K.INDEX), "bytes")
per = collections.Counter((c["lid"], c["kind"]) for c in recs)
print("lattices with records:", len({c["lid"] for c in recs}))
