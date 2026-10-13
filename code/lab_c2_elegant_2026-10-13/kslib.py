"""Shared helpers for the kill-statistics scripts (READ-ONLY on every record). Nothing here runs the original computation.

Sources (all on this machine):
  LAB   = C:\\Users\\RESEARCHER\\Desktop\\Recherche_Conway\\c2_experimental        (lab PC copy: data/, aws_repo/, logs/, c2_cloud_run*/)
  CODEX = C:\\Users\\RESEARCHER\\Desktop\\Recherche_Conway\\t20-codex              (second checkout of the compute repo: measures/, lemma/)
  git objects of LAB/aws_repo (remote-tracking branches origin/run/*), read with `git ls-tree` / `git cat-file --batch` only.
"""
import os, re, json, subprocess, collections

LAB = r"C:\Users\RESEARCHER\Desktop\Recherche_Conway\c2_experimental"
REPO = LAB + r"\aws_repo"
CODEX = r"C:\Users\RESEARCHER\Desktop\Recherche_Conway\t20-codex"
OUT = r"C:\Users\RESEARCHER\Downloads\conway_c2_researcher2_start_2026_09_30\conway_c2_researcher2_start_2026_09_30\work\c2_elegant_2026-10-13"
SCRATCH = r"C:\Users\RESEARCHER\AppData\Local\Temp\claude\C--Users-RESEARCHER-Downloads-conway-c2-researcher2-start-2026-09-30-conway-c2-researcher2-start-2026-09-30\cbac93e9-0e6a-4af7-8693-1962039bcf17\scratchpad"
INDEX = SCRATCH + r"\records_compact.jsonl"

# --------------------------------------------------------------------------------------------------------------------
# verdict names -> (class, kind).  kind: "a" short-vector rule, "b" no-frame rule, "dup" duplicate-of-another-orientation,
# "twin" twin-lattice bookkeeping, "inc" incomplete, "other".  The mapping is MY reading of AUDIT_ENGINE_RULES.md /
# the engine source (frame_dfs_next.py, hstage_stream_next.py, defer_consumer.py); uncertain entries are flagged in UNCERTAIN.
# --------------------------------------------------------------------------------------------------------------------
def classify(v):
    if v.startswith("SWAP-COVERED"): return ("swap", "dup")
    if v == "TWIN-DEFERRED": return ("twin_deferred", "twin")
    if v.startswith("TWIN-CANON"): return ("twin_canon", "twin")
    if v == "EXCLUDED (twin transfer)": return ("twin_transfer", "twin")
    if v == "EXCLUDED (char-vector trap)": return ("char_trap", "b")
    if v.startswith("EXCLUDED (dual min 9/7"): return ("dual_min_9_7_Y13_E8", "a")
    if v.startswith("DEFERRED (pending T18"): return ("deferred_T18_E9", "a")
    if v.startswith("DEFERRED (pending T20: root"): return ("deferred_T20_root_E10", "a")
    if v.startswith("DEFERRED (pending T20: norm-4"): return ("deferred_T20_norm4_E10", "a")
    if v.startswith("EXCLUDED (a y has |(y, beta)|") or v.startswith("EXCLUDED (both y hit the same new root"): return ("new_root_setup", "b")
    if v == "EXCLUDED (stage 1 empty: no 7 h)": return ("stage1_empty", "b")
    if v == "EXCLUDED (Lemma Z)": return ("lemmaZ", "b")
    if v == "EXCLUDED (no local star sums)": return ("no_local_star_sums", "b")
    if v == "EXCLUDED (no joint star sums)": return ("no_joint_star_sums", "b")
    if "but (F) fails" in v: return ("joint_F_fails", "b")
    if v == "EXCLUDED (pair budget)": return ("pair_budget", "b")
    if v.startswith("EXCLUDED (too few candidates"): return ("too_few_candidates", "b")
    if v.startswith("EXCLUDED (a root has Y > 6"): return ("root_Y_gt_6", "a")
    if v.startswith("INCOMPLETE"): return ("incomplete", "inc")
    if v.startswith("INVALID"): return ("invalid", "other")
    return ("other:" + v[:60], "other")

# verdicts whose kind is a judgement call (reported in the Limits section)
UNCERTAIN = {
    "char_trap": "listed by the requester under (b); proof uses only the frame identity at a norm-16 characteristic vector (no T16/T18/T20), but it is a short-ish vector argument (Y_z>66 means a vector of the shadow with large product with y1,y2)",
    "twin_transfer": "not a rule about the pair itself: the pair is moved to the twin lattice U+ (same frame) whose type is already excluded",
    "new_root_setup": "uses the shadow ('new') roots; rule of the pair set-up, before any search",
    "root_Y_gt_6": "a root with Y>6 has E<8 (R-vi); a short-vector rule, appears only in old h-stage code/producer",
}


def lid3(x): return "%03d" % int(x)


def git(*a):
    env = dict(os.environ); env["GIT_NO_LAZY_FETCH"] = "1"
    return subprocess.run(["git", "-C", REPO] + list(a), capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, timeout=120).stdout


def branch_result_blobs():
    """[(branch, path, oid)] for every file results/*.jsonl in every origin/run/* branch (read-only `git ls-tree`)"""
    brs = [b.strip() for b in git("branch", "-r").splitlines() if "origin/run/" in b]
    out = []
    for b in brs:
        for line in git("ls-tree", "-r", b, "results/").splitlines():
            meta, path = line.split("\t", 1)
            mode, typ, oid = meta.split()
            if typ == "blob" and path.endswith(".jsonl"): out.append((b, path, oid))
    return out


def read_blobs(oids, batch=400):
    """yield (oid, bytes) with `git cat-file --batch`, one short process per batch (read-only).
    GIT_NO_LAZY_FETCH=1: the repository is a partial clone (promisor remote = GitHub); this forbids any network fetch.
    A blob that is not local is reported as missing (bytes = None) instead of being fetched."""
    env = dict(os.environ); env["GIT_NO_LAZY_FETCH"] = "1"
    for i in range(0, len(oids), batch):
        chunk = oids[i:i + batch]
        r = subprocess.run(["git", "-C", REPO, "cat-file", "--batch"], input=("\n".join(chunk) + "\n").encode(), capture_output=True, env=env, timeout=120)
        buf = r.stdout; pos = 0
        for oid in chunk:
            nl = buf.index(b"\n", pos); hdr = buf[pos:nl].split(); pos = nl + 1
            if len(hdr) < 3 or hdr[1] == b"missing":
                yield oid, None; continue
            size = int(hdr[2]); data = buf[pos:pos + size]; pos += size + 1
            yield oid, data


def compact(d, src, fname_lkn=None, oid=None):
    """reduce a record to the fields used by the scripts"""
    kind = d.get("kind", "stream")
    de = d.get("deferred") or {}
    ne = d.get("not_excluded") or []
    tel = d.get("telemetry") or {}
    mg = d.get("merged") or {}
    dl = d.get("deferral") or {}
    prod = d.get("producer")
    return {
        "src": src, "oid": oid, "fname": fname_lkn, "lid": lid3(d.get("id", -1)), "kind": kind, "chunk": d.get("chunk"), "range": d.get("range"),
        "n_pairs": d.get("n_pairs"), "pairs_total": d.get("pairs_total"), "sha256": d.get("sha256"), "pfs": d.get("pair_files_sha256"),
        "producer": None if prod is None else {"complete": prod.get("complete"), "sha256": prod.get("sha256"), "pairs": prod.get("pairs")},
        "code_sha": d.get("code_sha"), "chunk_ok": d.get("chunk_ok"), "chunk_done": d.get("chunk_done"), "verdicts": d.get("verdicts"),
        "deferred_n": {k: len(v) for k, v in de.items() if isinstance(v, list)},
        "ne": [[e.get("index"), e.get("verdict")] for e in ne] if kind == "golay_pairs" else [e.get("verdict") for e in ne],
        "merged": {"bad": bool(mg.get("bad")), "defer": mg.get("defer"), "par": mg.get("par_consumer_sha256"), "dc": mg.get("defer_consumer_sha256"),
                   "pmo": mg.get("producer_max_out")} if mg else None,
        "deferral_dc": dl.get("defer_consumer_sha256"),
        "machine": d.get("machine"), "t": d.get("t"), "wall": d.get("wall_secs"), "node_limit": d.get("node_limit"),
        "tel": {k: tel.get(k) for k in ("E_pair_trap", "E_pair_search", "search_K", "trap_Yz") if tel.get(k) is not None},
        "twin_def_n": sum((d.get("twin_deferred") or {}).values()) if d.get("twin_deferred") else 0,
        "twin_def_types": d.get("twin_deferred") or {},
        "gamma": ((d.get("producer_info") or [{}])[0] or {}).get("gamma") if d.get("producer_info") else None,
        "y1_orbits": ((d.get("producer_info") or [{}])[0] or {}).get("y1_orbits") if d.get("producer_info") else None,
    }


def load_index():
    recs = []
    with open(INDEX, encoding="utf-8") as f:
        for l in f:
            if l.strip(): recs.append(json.loads(l))
    return recs


def engines():
    """code_sha dicts of the lab packages c2_cloud_run*/MANIFEST.json: ({json: package}, {json: package}) for stream / golay"""
    import glob
    st, go = {}, {}
    for f in sorted(glob.glob(LAB + r"\c2_cloud_run*\MANIFEST.json")):
        m = json.load(open(f)); name = os.path.basename(os.path.dirname(f))
        if "engine_code_sha" in m: st.setdefault(json.dumps(m["engine_code_sha"], sort_keys=True), name)
        if "engine_code_sha_golay" in m: go.setdefault(json.dumps(m["engine_code_sha_golay"], sort_keys=True), name)
    return st, go
