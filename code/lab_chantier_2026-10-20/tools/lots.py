"""Assign every inventory record to exactly one lot (first matching rule on its first location).
usage: python lots.py <notes_tagged.jsonl> <lots dir>"""
import collections
import json
import os
import re
import sys

RULES = [  # (lot, regex on "group|path|branch" of the first location)
    ("L04_C3", r"^git:conway99-c3(-experimental)?\||c3_review_2026-10-13|lab_c3_review"),
    ("L02_C2_aws", r"^git:conway99-c2-aws\|"),
    ("L03a_session_eeaf2d22", None),          # filled below (first half of the lab archive)
    ("L03b_session_eeaf2d22", None),
    ("L01_origines_C2", r"^git:conway99-involution\||^fs:Recherche_Conway/conway99-involution|^git:c2-compute\||"
                        r"^git:conway99-c2-(experimental|campaign|researcher2)\||^fs:Recherche_Conway/c2_experimental|"
                        r"^git:turbo-octo-waffle\||^git:conway-C7\||^git:conway_c2_researcher2_start|"
                        r"^fs:conway_c2_researcher2_start_2026_09_30/(?!work/)|"
                        r"^fs:conway_c2_researcher2_start_2026_09_30/work/(c2_|audit_v7|chatgpt_wagner|indep_wagner|t20_hand|twist|"
                        r"[A-Z_0-9-]+\.md$|AUDIT_156|CASCADE|ROUTE_C|FINAL_STATEMENT|HANDOVER|VERIF_CUBE)|"
                        r"code/lab_c2_|code/lab_audit_v7|code/r6/|code/code7_mots_binaires"),
    ("L05_Codex", r"^fs:Codex/|^fs:Recherche_Conway/(c1-main-codex|c1-codex|t20-codex)|^git:c1-codex\||"
                  r"\|origin/codex/"),
    ("L06_C1_arith_LAB", r"c1_theta_lp|lab_theta_lp|c1_index|coheawood|s3_question|spreadfree|c1_cost37|lab_cost37|"
                         r"c1_cores_sat|c1_lap_|c1_biplane|lab_biplane|c1_triangles|c1-norm16-export|\|papers/|lab/theta-lp|"
                         r"lab/biplane"),
    ("L07_C1_asym_local", r"asym_|lambda1_|lab_lambda1|c1_coclique|stars_rank|lab_stars_rank|c1_night|lab_c1_night|"
                          r"REVUE_GLOBALE|code/asym243|claude/v7-simultaneous|astra/bvls|c1-asymmetry-audit|"
                          r"lab_exchange_2026-10-14|c1-lambda1-env|c1-lap-girth5-audit|srg-research-audit|"
                          r"^git:strongly-regular-graphs-research\|"),
    ("L08_C1_exploration", r"exploration_2026-10-16|lab_exploration|lab/exploration|lab/aws-codex|c1-p3-export|"
                           r"c1-audit-deps|c1-imports|RECOVERY_2026-10-12"),
    ("L09_structures_astra_coord", r"^git:conway99-structures-lab\||^git:c1-structures-audit\||^git:conway99-rank17\||"
                                   r"CONWAY_ASTRA|^fs:review|^git:conway99-c1\|"),
    ("L10_sessions_memoires", r"scratchpad_LAB_2026-09-30|^fs:memory|.*"),
]


def main():
    recs = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8")]
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    lab = sorted((r for r in recs if r["group"] == "git:conway99-lab-archive"), key=lambda r: r["locations"][0]["path"])
    half = len(lab) // 2
    lab_lot = {r["blob"]: ("L03a_session_eeaf2d22" if i < half else "L03b_session_eeaf2d22") for i, r in enumerate(lab)}
    comp = [(lot, re.compile(rx)) for lot, rx in RULES if rx]
    lots = collections.defaultdict(list)
    for r in recs:
        if r["blob"] in lab_lot:
            lots[lab_lot[r["blob"]]].append(r)
            continue
        loc = r["locations"][0]
        key = "%s|%s|%s" % (r["group"], loc["path"].replace("\\", "/"), loc.get("branch", ""))
        for lot, rx in comp:
            if rx.search(key):
                lots[lot].append(r)
                break
    total = 0
    for lot in sorted(lots):
        rs = sorted(lots[lot], key=lambda r: (r.get("first_date") or "9999", r["locations"][0]["path"]))
        with open(os.path.join(out, lot + ".jsonl"), "w", encoding="utf-8") as f:
            for r in rs:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        prose = sum(1 for r in rs if r["kind_guess"] == "prose")
        total += len(rs)
        print("%-30s %5d notes (%5d prose)  %7.1f MB  %s .. %s" % (lot, len(rs), prose, sum(r["size"] for r in rs) / 1e6,
                                                               rs[0].get("first_date"), rs[-1].get("first_date")))
    print("total assigned", total, "of", len(recs))


if __name__ == "__main__":
    main()
