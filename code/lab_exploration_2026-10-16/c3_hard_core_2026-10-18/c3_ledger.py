"""Ledger of the c3 branch (budget root, all 7 root lines with c >= 3), LAB 18/10/2026.
For each of the 10 052 templates left open by the integer Gram test, the list of the methods that exclude it:
  P1   first pass, complete star at 60 s per letter-flip orbit representative (c3oa, c3ob);
  P2   second pass, complete Gram cover + table on every entry in the exact model (c3ga, c3gb), with the cover
       cross-checked by Codex's enumerator (flag xc = confirmed / not confirmed);
  GC   Gram-cover tests on the hard core (gc1a anchors/full, gc2a 'all' ablation);
  P3   Gram-by-Gram split with the moment filters (gc3b; every slice SLICE_ALL_INFEASIBLE);
  MOM  moment certificates on every Gram of the cover (Codex 63e87d62/80556dc3; LAB moment_bounds 5128, 4192);
  GFM  Gram-free moment model (gfm1);
  ZC   Codex's count design (root_component_z_pipeline, afa3706e; no Gram cover, no budget), run zscan1:
       EXCLUDED_BY_INTEGER_CERTIFICATE (exact Farkas certificate, re-checked in integers by Codex's code);
  ZCP  same run, DESIGN_CP_INFEASIBLE or JOINT_CP_INFEASIBLE (CP-SAT verdicts on the multiplicities).
usage: py -3 c3_ledger.py   (run in the aws_c1 scratch directory; reads the collect_* directories)"""
import glob
import json
import os
from collections import Counter, defaultdict

TAG = {"code/lab_exploration_2026-10-16/c3_root_cover/c3_open_templates_k3_12.json.gz": "gz",
       "data/codex_c3_pilot_20261018/inputs/cle3_c3_g1_open.json": "g1",
       "data/codex_c3_pilot_20261018/inputs/cle3_c3_g2_open.json": "g2"}
recs = json.load(open("pkg_c3star/data/codex_c3_pilot_20261018/complete_star_manifest10052.json"))["records"]
universe = {(TAG[r["source_file"]], r["template_index"]) for r in recs}
methods = defaultdict(set)
notes = defaultdict(list)
for line in open("c3o_excluded.tsv"):
    src, ti = line.split()[:2]
    methods[(TAG[src], int(ti))].add("P1")


def load(path):
    try:
        return json.load(open(path))
    except Exception:
        return None


for d in ("collect_c3ga", "collect_c3gb", "collect_c3ga2"):
    for f in glob.glob(os.path.join(d, "files", "out", "s2_*.json")):
        n = os.path.basename(f)[:-5]
        r = load(f)
        if r and r.get("status") == "INFEASIBLE":
            _, tag, ti = n.split("_")
            key = (tag, int(ti))
            methods[key].add("P2")
            x = load(os.path.join(d, "files", "out", "xc_" + n + ".json"))
            if not x or x.get("verdict") != "LAB_COVER_CONFIRMED":
                notes[key].append("P2 cover not confirmed by Codex's enumerator")
for f in glob.glob(os.path.join("collect_gc1a", "files", "out", "gc[af]_*.json")):
    r = load(f)
    if r and r.get("status") == "INFEASIBLE":
        methods[("gz", int(os.path.basename(f)[:-5].split("_")[1]))].add("GC")
for f in glob.glob(os.path.join("collect_gc2a", "files", "out", "ab_*_all.json")):
    r = load(f)
    if r and r.get("status") == "INFEASIBLE":
        methods[("gz", int(os.path.basename(f).split("_")[1]))].add("GC")
slices = defaultdict(dict)
for f in glob.glob(os.path.join("collect_gc3b", "files", "out", "gm_*.json")):
    if f.endswith(".codex_moments.json"):
        continue
    _, t, i, n = os.path.basename(f)[:-5].split("_")
    r = load(f)
    slices[int(t)][int(i)] = (int(n), r.get("status") if r else None)
for f in glob.glob(os.path.join("collect_c3gs", "files", "out", "sp_*.json")):
    _, tag, t, i, n = os.path.basename(f)[:-5].split("_")
    r = load(f)
    slices3 = slices.setdefault(("c3gs", tag, int(t)), {})
    slices3[int(i)] = (int(n), r.get("status") if r else None)
for key in [k for k in slices if isinstance(k, tuple)]:
    _, tag, t = key
    sl = slices.pop(key)
    n = next(iter(sl.values()))[0]
    if len(sl) == n and all(s == "SLICE_ALL_INFEASIBLE" for _, s in sl.values()):
        methods[(tag, t)].add("P3")
for t, sl in slices.items():
    n = next(iter(sl.values()))[0]
    if len(sl) == n and all(s == "SLICE_ALL_INFEASIBLE" for _, s in sl.values()):
        methods[("gz", t)].add("P3")
# third pass completed Gram by Gram: c3gs slices (all Grams processed) plus per-Gram reruns of its UNKNOWN Grams,
# c3hard1 (same exact model, 3600 s) and c3eig1 (Codex's fixed_gram_probe --eigen, ce1c814f, rank <= 6).
rerun_inf = defaultdict(set)
rerun_kind = defaultdict(set)
for f in glob.glob(os.path.join("collect_c3hard1", "files", "out", "hd_*.json")):
    r = load(f)
    _, tag, t, g = os.path.basename(f)[:-5].split("_")
    if r and r.get("grams") and r["grams"][0].get("status") == "INFEASIBLE":
        rerun_inf[(tag, int(t))].add(int(g[1:]))
        rerun_kind[(tag, int(t))].add("H")
for f in glob.glob(os.path.join("collect_c3eig1", "files", "out", "eg_*.json")):
    r = load(f)
    _, tag, t, c = os.path.basename(f)[:-5].split("_")
    for case in (r or {}).get("cases", []):
        if case.get("status") == "INFEASIBLE":
            rerun_inf[(tag, int(t))].add(int(case["gram_selector"]))
            rerun_kind[(tag, int(t))].add("E")
slice_info = defaultdict(dict)
for f in glob.glob(os.path.join("collect_c3gs", "files", "out", "sp_*.json")):
    _, tag, t, i, n = os.path.basename(f)[:-5].split("_")
    r = load(f)
    if not r:
        continue
    gs = r.get("grams") or []
    slice_info[(tag, int(t))][int(i)] = (int(n), len(gs) == len(r.get("slice_grams") or []),
                                        {x["gram"] for x in gs if x["status"] != "INFEASIBLE"})
for key, sl in slice_info.items():
    n = next(iter(sl.values()))[0]
    if len(sl) != n or not all(c for _, c, _ in sl.values()):
        continue
    hard = set().union(*(u for _, _, u in sl.values()))
    if hard and hard <= rerun_inf[key]:
        methods[key].add("P3" + "".join(sorted(rerun_kind[key])))
# fourth pass: Codex's fixed_gram_probe --eigen (ce1c814f, rank <= 6) on EVERY Gram of the complete cover (c3p4e);
# the template is excluded when the INFEASIBLE Grams cover all gram_count Grams of its 2nd-pass cover.
gram_count = {}
for d in ("collect_c3ga", "collect_c3gb", "collect_c3ga2"):
    for f in glob.glob(os.path.join(d, "files", "out", "s2_*.json")):
        r = load(f)
        if r and r.get("gram_count"):
            _, tag, ti = os.path.basename(f)[:-5].split("_")
            gram_count[(tag, int(ti))] = r["gram_count"]
p4 = defaultdict(set)
for f in glob.glob(os.path.join("collect_c3p4e", "files", "out", "pe_*.json")) + glob.glob(os.path.join("collect_c3p4eb", "files", "out", "pe_*.json")):
    r = load(f)
    _, tag, t, c = os.path.basename(f)[:-5].split("_")
    for case in (r or {}).get("cases", []):
        if case.get("status") == "INFEASIBLE":
            p4[(tag, int(t))].add(int(case["gram_selector"]))
for key, gs in p4.items():
    if key in gram_count and len(gs) == gram_count[key] and gs == set(range(gram_count[key])):
        methods[key].add("P4E")
for t in (5128, 4192):
    methods[("gz", t)].add("MOM")
for f in glob.glob(os.path.join("collect_gfm1", "files", "out", "gfm_*.json")):
    r = load(f)
    if r and r.get("status") == "INFEASIBLE":
        _, tag, ti = os.path.basename(f)[:-5].split("_")
        methods[(tag, int(ti))].add("GFM")
for f in glob.glob(os.path.join("collect_zscan1", "done", "*.json")):
    r = load(f)
    if not r or r.get("exit") != 0 or not r["id"].startswith(("zgz_", "zg1_", "zg2_")):
        continue
    lines = [l for l in r.get("stdout_tail", "").splitlines() if l.startswith("{")]
    st = json.loads(lines[-1]).get("status") if lines else None
    tag, ti = r["id"][1:].split("_")
    if st == "EXCLUDED_BY_INTEGER_CERTIFICATE":
        methods[(tag, int(ti))].add("ZC")
    elif st in ("DESIGN_CP_INFEASIBLE", "JOINT_CP_INFEASIBLE"):
        methods[(tag, int(ti))].add("ZCP")
excluded = {k for k in universe if methods[k]}
by_count = Counter(len(methods[k]) for k in universe)
combos = Counter("+".join(sorted(methods[k])) or "NONE" for k in universe)
print(json.dumps({"templates": len(universe), "excluded_by_at_least_one_method": len(excluded),
                  "not_excluded": len(universe) - len(excluded),
                  "number_of_methods_per_template": dict(sorted(by_count.items())),
                  "method_combinations": dict(combos.most_common(20)),
                  "notes": {"%s_%05d" % k: v for k, v in notes.items()}}, indent=1))
with open("c3_ledger_open.tsv", "w", newline="\n") as f:
    for k in sorted(universe - excluded):
        f.write("%s\t%d\n" % k)
