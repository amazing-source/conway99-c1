"""Statuses of the zscan1 run (Codex's root_component_z_pipeline, no Gram cover, no budget) by family."""
import glob, json, os, re, sys
from collections import Counter, defaultdict
d = sys.argv[1]
by = defaultdict(Counter); rows = {}
for f in glob.glob(os.path.join(d, "done", "*.json")):
    r = json.load(open(f))
    lines = [l for l in r.get("stdout_tail", "").splitlines() if l.startswith("{")]
    st = json.loads(lines[-1]) if lines else {}
    fam = re.sub(r"_\d+$", "", r["id"])
    s = st.get("status", "NO_STATUS") if r.get("exit") == 0 else "EXIT_%s" % r.get("exit")
    if st.get("uses_Gram_cover") or st.get("uses_prism_budget"):
        s += "+GRAM/BUDGET"
    by[fam][s] += 1
    rows[r["id"]] = {"status": s, "wall": r.get("wall"), "free_dimension": st.get("free_dimension"),
                     "row_state_count": st.get("row_state_count"), "checked": st.get("integer_certificate_checked")}
for fam in sorted(by):
    print(fam, sum(by[fam].values()), dict(by[fam].most_common()))
json.dump(rows, open(os.path.join(d, "zscan1_status.json"), "w"), indent=0)
