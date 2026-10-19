"""Inventory of the 10 052 c = 3 root templates (LAB 19/10/2026): status, excluding methods and known structure.
Read-only: it runs the rules of the ledger c3_ledger_2026-10-19.py on the collected run directories (no new verdict)
and recomputes, in exact rational arithmetic, the structural properties used by the families of 18-19/10:
  * grids, kernel dimension, components and blocks per root line (from the catalogues);
  * two-term column relations forced by the block and grid relations (H_A = -H_B sharing a line = 'shared pair',
    H_A = -H_B disjoint, H_A = H_B disjoint), as in gz5602_2026-10-19/two_term_relations.py;
  * the smallest non-empty signed S|T core (sum over S-internal H = sum over T-internal H, |S| = 3);
  * the best block core: a non-grid block P at a root line a gives a 2-regular core on 4|P| labels; Y-grids (inside the
    free lines) cut it into |P|-sets, grids inside P match it;
  * family memberships (gz only): K3U, P3U, 2K2, 2K2N, P3NB, K2BC, 45+14+26, from the members files of the night.
usage: python c3_inventaire_2026-10-19.py <ledger run dir (scratchpad aws_c1)> <gz catalogue.json.gz> <members dir> <out stem>"""
import csv
import gzip
import json
import os
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path

RUN, CAT, MEM, OUT = sys.argv[1], sys.argv[2], Path(sys.argv[3]), sys.argv[4]
here = os.getcwd()
os.chdir(RUN)
src = open("c3_ledger.py", encoding="utf-8").read()
cut = "excluded = {k for k in universe if methods[k]}"
assert src.count(cut) == 1
ns = {"__name__": "ledger"}
exec(compile(src.split(cut)[0], "c3_ledger.py", "exec"), ns)
universe, methods, notes = ns["universe"], ns["methods"], ns["notes"]
recs = json.load(open("pkg_c3star/data/codex_c3_pilot_20261018/complete_star_manifest10052.json"))["records"]
g1 = json.load(open("pkg_c3star/data/codex_c3_pilot_20261018/inputs/cle3_c3_g1_open.json"))["templates"]
g2 = json.load(open("pkg_c3star/data/codex_c3_pilot_20261018/inputs/cle3_c3_g2_open.json"))["templates"]
os.chdir(here)
gzc = json.load(gzip.open(CAT))["open"]
TPL = {}
for (tag, i) in universe:
    if tag == "gz":
        TPL[tag, i] = (gzc[i]["template"], gzc[i].get("gram", {}).get("status"))
    else:
        TPL[tag, i] = ((g1 if tag == "g1" else g2)[i], None)
assert len(TPL) == 10052


def members(name, key=None):
    p = MEM / name
    d = json.load(open(p))
    d = d[key] if key else d
    return set(map(int, d))


FAM = {"K3U": members("k3universal_members.json", "k3"), "P3U": members("k3universal_members.json", "p3"),
       "2K2": members("k2k2_members.json", "2k2"), "2K2N": members("k2k2_members.json", "2k2n"),
       "P3NB": members("p3nb_members.json", "p3nb"), "K2BC": members("k2bc_members.json", "members")}
if (MEM / "fam_45_14_26.json").exists():
    FAM["45+14+26"] = members("fam_45_14_26.json", "members")
RECT = list(combinations(range(7), 2))
ridx = {q: i for i, q in enumerate(RECT)}


def basis(t):
    ng = {tuple(e) for e in t["nongrid_edges"]}
    rows = []
    for q in RECT:
        if q not in ng:
            v = [0] * 21; v[ridx[q]] = 1; rows.append(v)
    for a, groups in enumerate(t["nontrivial_component_groups"]):
        for P in groups:
            v = [0] * 21
            for j in P:
                v[ridx[tuple(sorted((a, j)))]] = 1
            rows.append(v)
    rows = [[Fraction(x) for x in r] for r in rows]
    piv, r = [], 0
    for c in range(21):
        p = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        rows[r] = [x / rows[r][c] for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c]; rows[i] = [x - f * y for x, y in zip(rows[i], rows[r])]
        piv.append(c); r += 1
    assert 21 - r == t["kernel_dimension"], ("kernel dimension", 21 - r, t["kernel_dimension"])
    return rows[:r], piv


def in_span(B, piv, v):
    v = [Fraction(x) for x in v]
    for row, c in zip(B, piv):
        if v[c] != 0:
            f = v[c]; v = [a - f * b for a, b in zip(v, row)]
    return all(x == 0 for x in v)


def rel(t):
    B, piv = basis(t)
    E = sorted(tuple(e) for e in t["nongrid_edges"])
    sh, dj, eq = [], [], []
    for A, C in combinations(E, 2):
        v = [0] * 21; v[ridx[A]] = 1; v[ridx[C]] = 1
        if in_span(B, piv, v):
            (sh if set(A) & set(C) else dj).append("%d%d/%d%d" % (A + C))
        v[ridx[C]] = -1
        if in_span(B, piv, v):
            eq.append("%d%d=%d%d" % (A + C))
    return sh, dj, eq


def signed_core(t):
    E = {tuple(e) for e in t["nongrid_edges"]}
    best = None
    for S in combinations(range(7), 3):
        T = [x for x in range(7) if x not in S]
        n = sum(q in E for q in combinations(S, 2)) + sum(q in E for q in combinations(T, 2))
        if n and (best is None or 4 * n < best[0]):
            best = (4 * n, "".join(map(str, S)))
    return best


def block_core(t):
    E = {tuple(e) for e in t["nongrid_edges"]}
    isg = lambda x, y: tuple(sorted((x, y))) not in E
    cands = []
    for a, groups in enumerate(t["nontrivial_component_groups"]):
        for P in groups:
            X = [x for x in range(7) if x != a and x not in P]
            Y = ["%d%d" % q for q in combinations(X, 2) if isg(*q)]
            JK = ["%d%d" % q for q in combinations(P, 2) if isg(*q)]
            cands.append((4 * len(P), -(3 * len(Y) + 2 * len(JK)), a, tuple(P), Y, JK))
    if not cands:
        return ""
    s, _, a, P, Y, JK = min(cands)
    return "%d@%d{%s} Y=%s P=%s" % (s, a, "".join(map(str, P)), ",".join(Y) or "-", ",".join(JK) or "-")


rows = []
for key in sorted(universe):
    tag, i = key
    t, gram = TPL[key]
    E = {tuple(e) for e in t["nongrid_edges"]}
    grids = ["%d%d" % q for q in RECT if q not in E]
    sh, dj, eq = rel(t)
    sc = signed_core(t)
    fams = [f for f, m in FAM.items() if tag == "gz" and i in m]
    st = "EXCLU" if methods[key] else "OUVERT"
    etat = ""
    if st == "OUVERT":
        if "P3U" in fams:
            etat = "P3 en production (AWS, regle P3U inactive tant que p3u_closed.json manque)"
        elif "2K2N" in fams:
            etat = "2K2N en production (local, marques B/C)"
        elif not sh:
            etat = "sans paire partagee forcee: aucun outil ferme"
        else:
            etat = "paire partagee mais grilles insuffisantes pour les familles: aucun outil ferme"
    rows.append({"gabarit": "%s%05d" % (tag, i), "source": tag, "indice": i, "statut": st,
                 "methodes": "+".join(sorted(methods[key])), "nb_methodes": len(methods[key]),
                 "notes": " | ".join(notes.get(key, [])), "dim_noyau": t["kernel_dimension"],
                 "nb_grilles": len(grids), "grilles": " ".join(grids),
                 "composantes_par_droite": "".join(map(str, t["component_count_by_root_line"])),
                 "blocs": " ".join("%d:%s" % (a, "|".join("".join(map(str, P)) for P in g)) for a, g in
                                   enumerate(t["nontrivial_component_groups"]) if g),
                 "paires_partagees": " ".join(sh), "paires_opposees_disjointes": " ".join(dj),
                 "paires_egales": " ".join(eq), "sans_paire": "oui" if not sh else "non",
                 "coeur_signe_min": "%d (S=%s)" % sc if sc else "", "meilleur_coeur_bloc": block_core(t),
                 "familles": "+".join(fams), "gram_catalogue": gram or "", "etat_si_ouvert": etat})
cols = list(rows[0].keys())
with open(OUT + ".csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=cols, delimiter=";")
    w.writeheader(); w.writerows(rows)
json.dump(rows, open(OUT + ".json", "w"), indent=0)
summ = {"total": len(rows), "statut": Counter(r["statut"] for r in rows),
        "par_source": {s: Counter(r["statut"] for r in rows if r["source"] == s) for s in ("gz", "g1", "g2")},
        "nb_methodes": Counter(r["nb_methodes"] for r in rows),
        "methode_presente": Counter(m for r in rows for m in r["methodes"].split("+") if m),
        "seule_methode": Counter(r["methodes"] for r in rows if r["nb_methodes"] == 1),
        "dim_par_statut": {d: Counter(r["statut"] for r in rows if r["dim_noyau"] == d) for d in sorted({r["dim_noyau"] for r in rows})},
        "grilles_par_statut": {g: Counter(r["statut"] for r in rows if r["nb_grilles"] == g) for g in sorted({r["nb_grilles"] for r in rows})},
        "sans_paire": {"%s / sans paire %s" % k: v for k, v in Counter((r["statut"], r["sans_paire"]) for r in rows).items()},
        "ouverts": [{k: r[k] for k in ("gabarit", "dim_noyau", "nb_grilles", "grilles", "paires_partagees",
                                       "paires_egales", "coeur_signe_min", "meilleur_coeur_bloc", "familles", "etat_si_ouvert")}
                    for r in rows if r["statut"] == "OUVERT"]}
json.dump(summ, open(OUT + "_resume.json", "w"), indent=1, default=str)
print(json.dumps({k: summ[k] for k in ("total", "statut", "par_source", "nb_methodes")}, default=str))
print("methods present:", dict(summ["methode_presente"]))
print("sole method:", dict(summ["seule_methode"]))
