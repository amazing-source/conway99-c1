"""Merge all fiches/*.jsonl into one index; report status counts, malformed lines, and likely cross-lot duplicates.
usage: python merge_fiches.py <fiches dir> <out dir>"""
import collections
import json
import os
import re
import sys
import unicodedata

FIELDS = ["id", "titre", "enonce", "statut", "relu_par", "sources", "date", "auteur", "depend_de", "implique",
          "remplace_par", "remarques"]
STOP = set("le la les de des du un une et ou en au aux a à par pour sur dans est sont que qui ne pas plus avec sans "
           "ce cette ces son sa ses leur leurs tout toute tous toutes on il elle the of and to in is for".split())


def toks(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return {w for w in re.findall(r"[a-z0-9]+", s) if w not in STOP and len(w) > 1}


def main():
    d, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    recs, bad = [], []
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".jsonl") or fn.endswith("_recomb.jsonl"):  # *_recomb.jsonl = materials, not results
            continue
        lot = fn[:-6]
        for i, line in enumerate(open(os.path.join(d, fn), encoding="utf-8"), 1):
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except Exception as e:
                bad.append((fn, i, str(e)[:80]))
                continue
            r["_lot"], r["_line"] = lot, i
            recs.append(r)
    st = collections.Counter((r["_lot"], str(r.get("statut", "?"))[:1]) for r in recs)
    lots = sorted({r["_lot"] for r in recs})
    with open(os.path.join(out, "INDEX_RESULTATS.tsv"), "w", encoding="utf-8") as f:
        f.write("id\tlot\tstatut\tdate\tauteur\ttitre\tsource1\n")
        for r in recs:
            src = r.get("sources") or [""]
            src = src[0] if isinstance(src, list) and src else str(src)
            f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (r.get("id"), r["_lot"], r.get("statut"), r.get("date"),
                                                   r.get("auteur"), str(r.get("titre", "")).replace("\t", " "),
                                                   src.replace("\t", " ")))
    # duplicates across lots: Jaccard on title+statement tokens
    T = [toks(str(r.get("titre", "")) + " " + str(r.get("enonce", ""))[:400]) for r in recs]
    inv = collections.defaultdict(set)
    for i, t in enumerate(T):
        for w in t:
            inv[w].add(i)
    df = {w: len(s) for w, s in inv.items()}
    pairs = []
    for i, t in enumerate(T):
        cand = collections.Counter()
        for w in t:
            if df[w] <= 60:
                for j in inv[w]:
                    if j > i and recs[j]["_lot"] != recs[i]["_lot"]:
                        cand[j] += 1
        for j, c in cand.items():
            if c >= 4:
                jac = len(t & T[j]) / max(1, len(t | T[j]))
                if jac >= 0.30:
                    pairs.append((jac, i, j))
    pairs.sort(reverse=True)
    with open(os.path.join(out, "DOUBLONS_PROBABLES.tsv"), "w", encoding="utf-8") as f:
        f.write("jaccard\tid1\tstatut1\tid2\tstatut2\ttitre1\ttitre2\n")
        for jac, i, j in pairs:
            a, b = recs[i], recs[j]
            f.write("%.2f\t%s\t%s\t%s\t%s\t%s\t%s\n" % (jac, a.get("id"), a.get("statut"), b.get("id"), b.get("statut"),
                                                     str(a.get("titre", ""))[:120], str(b.get("titre", ""))[:120]))
    disc = [(jac, i, j) for jac, i, j in pairs if str(recs[i].get("statut"))[:1] != str(recs[j].get("statut"))[:1]]
    print("records", len(recs), "malformed", len(bad))
    for b in bad[:20]:
        print("  malformed", b)
    print("%-28s %s" % ("lot", " ".join("%4s" % s for s in "PCESHORX?")))
    for lot in lots:
        print("%-28s %s" % (lot, " ".join("%4d" % st[(lot, s)] for s in "PCESHORX?")))
    print("likely duplicates across lots:", len(pairs), "| with different status letter:", len(disc))


if __name__ == "__main__":
    main()
