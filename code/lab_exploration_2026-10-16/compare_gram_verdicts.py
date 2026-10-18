"""Template-by-template comparison of cle3_gram (CP-SAT) and cle3_gram_milp_check (HiGHS) verdicts (LAB, 18/10/2026).
usage: python compare_gram_verdicts.py <gram.json> <milp.json> [...pairs]"""
import json
import sys

MAP = {"QUOTIENT_FEASIBLE": "FEASIBLE", "QUOTIENT_INFEASIBLE": "INFEASIBLE"}
total, bad, unk = 0, [], 0
for a_path, b_path in zip(sys.argv[1::2], sys.argv[2::2]):
    a = {(r["file"], r["line"]): MAP.get(r["status"], r["status"]) for r in json.load(open(a_path))["records"]}
    b = {(r["file"], r["line"]): r["status"] for r in json.load(open(b_path))["records"]}
    assert set(a) == set(b), (a_path, b_path)
    for key in a:
        total += 1
        if "UNKNOWN" in (a[key], b[key]):
            unk += 1
        elif a[key] != b[key]:
            bad.append((key, a[key], b[key]))
print(json.dumps({"templates": total, "disagreements": len(bad), "unknown": unk, "first": bad[:5]}))
