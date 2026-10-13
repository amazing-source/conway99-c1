"""Step 2: select, for every lattice that has pair-level records, the record set the lab's own tooling selects, and add up the RAW verdict
names. READ-ONLY on every source; reads the compact index built by index_records.py. Validates against the lab's published numbers.

Selection rules (re-implemented from q/tools/lab_2026-10-07/import_sweep.py and stream_recount.py, which I read; I did not run them):
  DEFERRAL   (001,002,003,005-009,011-015): records accepted by the basic checks and from a lab-package engine; 'done' records first,
             then 'deferred' ones, each only if it covers a y1 representative not yet covered (stream); Golay: tiling of the pair range.
  STREAM     (91 lattices of STREAM_RECOUNT): records of data/finishC/stream/<lid>/chunks.jsonl, tiers P (package engine), L (engine hash
             not a package), N (no code version), selected in this order, each only if it covers a representative not yet covered.
  RERUN28    v10 whole-lattice re-run of the 28 old pair-list lattices (chunks k/8 of measures/rerun_28/plan_<lid>.json).
  RERUN713   v10 re-run of the representatives without code version (25 lattices): whole lattice in 16 chunks, or one job per representative.
  EXTRA105   v10 re-run of lattice 105 (chunks k/8).
  GOLAY_OLD  004, 010: Golay pair blocks of 02/10 (package v4).
Usage: python -I select_sets.py     (writes sets.json to the scratchpad)"""
import sys, os, json, collections, re, glob, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kslib as K

t0 = time.time()
R = K.load_index()
ST, GO = K.engines()
V10 = json.dumps({"frame_dfs_next.py": "1591aeeac9c0be5c", "hstage_stream_next.py": "f48520f7ebac4bf8", "twin_transfer.py": "77a446c7cb8b3922"}, sort_keys=True)
TR = json.load(open(K.LAB + r"\data\finishC\finishC_tracker.json"))["lattices"]
TRK = {"%03d" % v["id"]: v for v in TR}

# ---- import_sweep.cls : 8 coarse classes, used only for validation against the published numbers
def cls8(v):
    if "but (F) fails" in v: return "other"
    if v.startswith("DEFERRED (pending T18"): return "defer_T18"
    if v.startswith("DEFERRED (pending T20"): return "defer_T20"
    if "INCOMPLETE" in v: return "incomplete"
    if v.startswith("SWAP-COVERED"): return "swap"
    if v.startswith("TWIN") or "twin transfer" in v: return "twin"
    if "stage 1" in v or "star" in v or "Lemma Z" in v: return "excl_search"
    if v.startswith("EXCLUDED"): return "excl_at_once"
    return "other"

def tier_of(r):
    cs = json.dumps(r["code_sha"] or {}, sort_keys=True)
    pk = GO if r["kind"] == "golay_pairs" else ST
    if cs in pk: return "P"
    return "L" if r["code_sha"] else "N"

def basic_faults(r):
    """subset of import_sweep.check without the engine and wrapper-hash tests"""
    bad = []
    if not r["chunk_ok"]: return ["not chunk_ok"]
    if r["fname"]:
        m = re.match(r"^(\d{3})_(\d+)_(\d+)\.jsonl$", r["fname"])
        if m and (m.group(1) != r["lid"] or list(r["chunk"]) != [int(m.group(2)), int(m.group(3))]): bad.append("id/chunk differ from file name")
    if sum(r["verdicts"].values()) != r["n_pairs"]: bad.append("verdict counts do not add up")
    c = collections.Counter()
    for v, n in r["verdicts"].items(): c[cls8(v)] += n
    if r["kind"] == "stream":
        p = r["producer"]
        if p is not None and not (p.get("complete") is True and p.get("sha256") == r["sha256"] and p.get("pairs") == r["n_pairs"]): bad.append("producer end line")
        dn = r["deferred_n"]
        if (c["defer_T18"], c["defer_T20"]) != (dn.get("T18", 0), dn.get("T20", 0) + dn.get("T20_norm4", 0)):
            if c["defer_T18"] or c["defer_T20"] or dn: bad.append("DEFERRED counts differ from index lists")
    else:
        ne = r["ne"]; e18 = sum(1 for i, v in ne if cls8(str(v)) == "defer_T18"); e20 = sum(1 for i, v in ne if cls8(str(v)) == "defer_T20")
        if (c["defer_T18"], c["defer_T20"]) != (e18, e20): bad.append("DEFERRED counts differ from not_excluded")
        a, b = r["range"]
        if b - a != r["n_pairs"]: bad.append("range inconsistent")
    if r["merged"] and r["merged"].get("bad"): bad.append("merged record with bad shards")
    if any(cls8(v) == "other" for v in r["verdicts"]): bad.append("unknown verdict")
    return bad

def open_state(r):
    c = collections.Counter()
    for v, n in r["verdicts"].items(): c[cls8(v)] += n
    if c["incomplete"] or c["other"]: return "open"
    if c["defer_T18"] or c["defer_T20"]: return "deferred"
    return "done" if r["chunk_done"] else "open"

def in_lab_chunks(r):
    return any(s.startswith("lab:data\\finishC\\stream\\") or s.startswith("lab:data\\finishC\\golay\\") for s in [r["src"]] + r["dup_srcs"])

def plan_nr(lid):
    return len(json.load(open(K.LAB + r"\data\finishC\stream\%s\plan.json" % lid))["y1_reps"])

def tile(recs, N):
    """exact tiling of [0,N) by non-overlapping records (range), minimising first the number of DEFERRED pairs, then the number of records.
    Needed because Golay pair records come in several overlapping chunkings (n=17, 170, 1700, ...)."""
    edges = collections.defaultdict(list)
    for r in recs:
        a_, b_ = r["range"]
        dn = sum(n for v, n in r["verdicts"].items() if cls8(v) in ("defer_T18", "defer_T20", "incomplete", "other"))
        edges[a_].append((dn, b_, r))
    best = {0: (0, 0, None, None)}
    for p in sorted({0} | set(edges)):
        if p not in best: continue
        d, c, _, _ = best[p]
        for dn, b_, r in edges[p]:
            cand = (d + dn, c + 1, p, r)
            if b_ not in best or cand[:2] < best[b_][:2]: best[b_] = cand
    if N not in best: return {"ok": False, "records": [], "deferred": None}
    path = []; p = N
    while p != 0:
        d, c, prev, r = best[p]; path.append(r); p = prev
    return {"ok": True, "records": path[::-1], "deferred": best[N][0]}


def agg(recs):
    """add up the raw verdict names, telemetry and bookkeeping of a list of records"""
    v = collections.Counter(); pairs = 0; tel = {"E_pair_trap": collections.Counter(), "E_pair_search": collections.Counter(), "search_K": collections.Counter(), "trap_Yz": collections.Counter()}
    eng = collections.Counter(); tw = collections.Counter(); nd = 0
    for r in recs:
        v.update(r["verdicts"]); pairs += r["n_pairs"]
        for k in tel: tel[k].update(r["tel"].get(k, {}))
        cs = r["code_sha"] or {}
        eng[(cs.get("frame_dfs_next.py") or cs.get("frame_dfs.py") or "none")[:8]] += 1
        tw.update(r["twin_def_types"] if r["twin_def_types"] else {})
    return {"records": len(recs), "pairs": pairs, "verdicts": dict(v), "telemetry": {k: dict(x) for k, x in tel.items()}, "engines_frame_dfs": dict(eng),
            "twin_deferred_types": dict(tw)}

def cls_sum(recs):
    c = collections.Counter()
    for r in recs:
        for v, n in r["verdicts"].items(): c[cls8(v)] += n
    return dict(c)

OUT = {}; REPORT = []
by_lid = collections.defaultdict(list)
for r in R: by_lid[r["lid"]].append(r)

# --------------------------------------------------------------------------- DEFERRAL (stream) -----------
SWEEP = json.load(open(K.CODEX + r"\measures\SWEEP_LAB_2026-10-07.json"))["lattices"]
for lid in ("003", "005", "006", "007", "008", "009", "011", "012", "013", "014", "015"):
    NR = plan_nr(lid)
    acc = []; refused = collections.Counter()
    for r in by_lid[lid]:
        if r["kind"] != "stream": continue
        b = basic_faults(r)
        if not r["chunk_ok"]: continue
        if tier_of(r) != "P": b = b + ["engine not of a lab package"]
        if b: refused[";".join(b)[:60]] += 1; continue
        acc.append(r)
    cov = [0] * NR; sel = []
    key = lambda d: (tuple(d["chunk"]), d["sha256"])
    for want in ("done", "deferred"):
        seen = set()
        for d in sorted((d for d in acc if open_state(d) == want), key=lambda d: (d["chunk"][1], d["chunk"][0], d.get("t") or "")):
            if key(d) in seen: continue
            k, n = d["chunk"]; mine = range(k, NR, n)
            if all(cov[i] for i in mine): continue
            seen.add(key(d)); sel.append(d)
            for i in mine: cov[i] += 1
    miss = [i for i, x in enumerate(cov) if x == 0]
    a = agg(sel); a["reps_missing_in_records"] = miss; a["y1_reps"] = NR; a["covered_twice"] = sum(1 for x in cov if x > 1)
    a["classes8"] = cls_sum(sel); a["refused"] = dict(refused); a["accepted_records"] = len(acc)
    S = SWEEP[lid]
    a["validation"] = {"pairs_equal": a["pairs"] == S["pairs"], "classes_equal": all(a["classes8"].get(x, 0) == S[x] for x in ("excl_at_once", "excl_search", "twin", "swap", "defer_T18", "defer_T20")),
                       "selected_equal": len(sel) == S["selected"], "published_pairs": S["pairs"], "my_pairs": a["pairs"], "published_selected": S["selected"], "my_selected": len(sel)}
    OUT.setdefault(lid, {})["DEFERRAL"] = a
    REPORT.append(("DEFERRAL", lid, a["validation"]))

# --------------------------------------------------------------------------- DEFERRAL (golay 001, 002) ---------
for lid in ("001", "002"):
    acc = []
    for r in by_lid[lid]:
        if r["kind"] != "golay_pairs": continue
        b = basic_faults(r)
        if tier_of(r) != "P": b = b + ["engine"]
        if b: continue
        acc.append(r)
    N = acc[0]["pairs_total"]
    # pair-by-pair best state, as in import_sweep: 4 excluded > 3 deferred T18 > 2 deferred T20 > 1 other > 0 uncovered; remember which record gave the best
    state = bytearray(N); owner = [None] * N
    for ri, r in enumerate(acc):
        a_, b_ = r["range"]; opn = {}
        for i, v in r["ne"]:
            x = cls8(str(v)); opn[i] = 3 if x == "defer_T18" else 2 if x == "defer_T20" else 1
        for i in range(a_, b_):
            s = opn.get(i, 4)
            if s > state[i]: state[i] = s; owner[i] = ri
    h = collections.Counter(state)
    # verdict names for the pairs: take, record by record, the pairs it owns.  Records excluding a pair carry only aggregate counts, so
    # when ranges overlap the aggregate cannot be split; we check that no record is partly owned.
    tl = tile(acc, N)
    a = agg(tl["records"]) if tl["ok"] else {"records": 0, "pairs": 0, "verdicts": {}, "telemetry": {}, "engines_frame_dfs": {}, "twin_deferred_types": {}}
    a["pairs_total"] = N; a["accepted_records"] = len(acc); a["states"] = {"excluded": h[4], "defer_T18": h[3], "defer_T20": h[2], "incomplete_or_other": h[1], "uncovered": h[0]}
    a["tiling"] = {"ok": tl["ok"], "records": len(tl["records"]), "deferred_pairs_in_tiling": tl["deferred"]}
    a["classes8"] = cls_sum(tl["records"]) if tl["ok"] else {}
    S = SWEEP[lid]
    a["validation"] = {"pairs_equal": N == S["pairs"], "excluded_equal": h[4] == S["excluded"], "T18_equal": h[3] == S["defer_T18"], "T20_equal": h[2] == S["defer_T20"],
                       "tiling_T18_equal": a["classes8"].get("defer_T18", -1) == S["defer_T18"], "tiling_T20_equal": a["classes8"].get("defer_T20", -1) == S["defer_T20"],
                       "tiling_pairs_equal": a["pairs"] == N,
                       "my_accepted": len(acc), "published_accepted": S["records_accepted"], "note_accepted_count_differs": len(acc) != S["records_accepted"]}
    OUT.setdefault(lid, {})["DEFERRAL"] = a
    REPORT.append(("DEFERRAL-golay", lid, a["validation"]))

# --------------------------------------------------------------------------- STREAM (91) ----------------------
REC = json.load(open(K.CODEX + r"\measures\STREAM_RECOUNT_2026-10-07.json"))
for lid in sorted(REC):
    NR = plan_nr(lid); res_f = K.LAB + r"\data\finishC\stream\%s\incomplete_resolved.jsonl" % lid
    has_res = os.path.exists(res_f)
    recs = []
    for r in by_lid[lid]:
        if r["kind"] != "stream" or not in_lab_chunks(r) or not r["chunk_ok"]: continue
        b = basic_faults(r)
        if b: continue
        t = tier_of(r)
        ne = r["ne"]
        done = bool(r["chunk_done"]) or (bool(ne) and has_res and all(str(v) == "INCOMPLETE" for v in ne))
        if done: recs.append((t, r))
    cov = [None] * NR; sel = []; twice = 0; pt = collections.Counter()
    for t, d in sorted(recs, key=lambda x: ("PLN".index(x[0]), x[1]["chunk"][1], x[1]["chunk"][0], str(x[1].get("t") or ""))):
        k, n = d["chunk"]; mine = range(k, NR, n)
        if all(cov[i] is not None for i in mine): continue
        for i in mine:
            if cov[i] is None: cov[i] = t
            else: twice += 1
        sel.append((t, d)); pt[t] += d["n_pairs"]
    a = agg([d for t, d in sel]); a["y1_reps"] = NR; a["covered_twice"] = twice; a["pairs_by_tier"] = {t: pt.get(t, 0) for t in "PLN"}
    a["reps_by_tier"] = dict(collections.Counter(x for x in cov if x is not None)); a["reps_missing"] = sum(1 for x in cov if x is None)
    a["classes8"] = cls_sum([d for t, d in sel])
    S = REC[lid]
    a["validation"] = {"pairs_equal": a["pairs"] == S["pairs"], "classes_equal": all(a["classes8"].get(x, 0) == S[x] for x in ("excl_at_once", "excl_search", "twin", "swap", "incomplete")),
                       "tiers_equal": a["pairs_by_tier"] == S["pairs_by_tier"], "published_pairs": S["pairs"], "my_pairs": a["pairs"]}
    OUT.setdefault(lid, {})["STREAM"] = a
    REPORT.append(("STREAM", lid, a["validation"]))
print("t=%.0fs after DEFERRAL/STREAM" % (time.time() - t0), flush=True)

# --------------------------------------------------------------------------- RERUN28 / RERUN713 / EXTRA105 -----
def dedupe_records(recs):
    seen = {}; dup_diff = 0
    for r in recs:
        key = (r["lid"], tuple(r["chunk"]), r["sha256"])
        if key in seen:
            if seen[key]["verdicts"] != r["verdicts"]: dup_diff += 1
            seen[key].setdefault("copies", 1); seen[key]["copies"] += 1; continue
        r = dict(r); r["copies"] = 1; seen[key] = r
    return list(seen.values()), dup_diff

M28 = json.load(open(K.REPO + r"\measures\RERUN_28_MANIFEST_2026-10-07.json"))
C28 = json.load(open(K.REPO + r"\measures\RERUN_28_CHECK_2026-10-07.json"))
M713 = json.load(open(K.REPO + r"\measures\RERUN_713_MANIFEST_LAB_2026-10-07.json"))
C713 = json.load(open(K.REPO + r"\measures\RERUN_713_CHECK_2026-10-07.json"))
nset = collections.defaultdict(set)
for j in M713["jobs"]: nset[j["lid"]].add(j["n"])
for lid, ck in sorted(C28.items()):
    cand = [r for r in by_lid[lid] if r["kind"] == "stream" and r["chunk_ok"] and json.dumps(r["code_sha"] or {}, sort_keys=True) == V10 and r["chunk"][1] == 8 and not basic_faults(r)]
    sel, dd = dedupe_records(cand)
    a = agg(sel); a["classes8"] = cls_sum(sel); a["copies_total"] = sum(r["copies"] for r in sel); a["copies_with_different_verdicts"] = dd
    a["pairs_with_double_copies_counted_once"] = True
    ck_classes = ck.get("verdict_classes") or {}
    a["validation"] = {"pairs_equal": a["pairs"] == ck["pairs"], "published_pairs": ck["pairs"], "my_pairs": a["pairs"], "published_ok": ck["ok"],
                       "classes_equal": all(a["classes8"].get(x, 0) == ck_classes.get(x, 0) for x in ("excl_at_once", "excl_search", "twin", "swap"))}
    OUT.setdefault(lid, {})["RERUN28"] = a; REPORT.append(("RERUN28", lid, a["validation"]))
for lid, ck in sorted(C713.items()):
    ns = nset[lid]
    cand = [r for r in by_lid[lid] if r["kind"] == "stream" and r["chunk_ok"] and json.dumps(r["code_sha"] or {}, sort_keys=True) == V10 and r["chunk"][1] in ns and not basic_faults(r)]
    sel, dd = dedupe_records(cand)
    a = agg(sel); a["classes8"] = cls_sum(sel); a["copies_total"] = sum(r["copies"] for r in sel); a["copies_with_different_verdicts"] = dd
    a["mode"] = "whole lattice" if ns == {16} else "per representative"
    ck_classes = ck.get("verdict_classes") or {}
    a["validation"] = {"pairs_equal": a["pairs"] == ck["pairs"], "published_pairs": ck["pairs"], "my_pairs": a["pairs"], "published_ok": ck["ok"],
                       "classes_equal": all(a["classes8"].get(x, 0) == ck_classes.get(x, 0) for x in ("excl_at_once", "excl_search", "twin", "swap")),
                       "published_classes": ck_classes, "my_classes": a["classes8"]}
    OUT.setdefault(lid, {})["RERUN713"] = a; REPORT.append(("RERUN713", lid, a["validation"]))
# 105 extra
cand = [r for r in by_lid["105"] if r["kind"] == "stream" and r["chunk_ok"] and json.dumps(r["code_sha"] or {}, sort_keys=True) == V10 and r["chunk"][1] == 8]
sel, dd = dedupe_records(cand); a = agg(sel); a["classes8"] = cls_sum(sel); a["copies_total"] = sum(r["copies"] for r in sel)
a["validation"] = {"published_pairs": 56544, "my_pairs": a["pairs"], "pairs_equal": a["pairs"] == 56544}
OUT.setdefault("105", {})["EXTRA105"] = a; REPORT.append(("EXTRA105", "105", a["validation"]))
print("t=%.0fs after reruns" % (time.time() - t0), flush=True)

# --------------------------------------------------------------------------- GOLAY OLD (004, 010) and the rest ----
for lid in ("004", "010"):
    cand = [r for r in by_lid[lid] if r["kind"] == "golay_pairs" and r["chunk_ok"]]
    N = cand[0]["pairs_total"]
    tl = tile(cand, N); ok = tl["ok"]; sel = tl["records"]
    a = agg(sel); a["classes8"] = cls_sum(sel); a["pairs_total"] = N; a["ranges_tile_exactly"] = ok; a["all_chunk_done"] = all(r["chunk_done"] for r in sel)
    a["tiling_records"] = len(sel); a["candidate_records"] = len(cand)
    a["validation"] = {"published_pairs": 416383 if lid == "004" else 3962, "my_pairs": a["pairs"], "pairs_equal": a["pairs"] == (416383 if lid == "004" else 3962)}
    OUT.setdefault(lid, {})["GOLAY_OLD"] = a; REPORT.append(("GOLAY_OLD", lid, a["validation"]))

other_lids = sorted(set(by_lid) - set(OUT))
print("lattices with records but no set selected:", other_lids, {l: collections.Counter((r["kind"], r["srctype"]) for r in by_lid[l]) for l in other_lids})

json.dump(OUT, open(K.SCRATCH + r"\sets.json", "w"))
bad = [(k, l, v) for k, l, v in REPORT if not all(x for kk, x in v.items() if kk.endswith("_equal"))]
print("sets computed:", len(REPORT), "validation failures:", len(bad))
for k, l, v in bad: print("  FAIL", k, l, v)
print("t=%.0fs" % (time.time() - t0))
