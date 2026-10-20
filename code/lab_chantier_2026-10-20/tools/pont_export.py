"""Readable export of the LAB<->Codex bridge log (copy in pont_codex/brut), plus draft coverage and a secret scan.
usage: python pont_export.py <pont_codex dir>
writes: par_jour/AAAA-MM-JJ.md, index.tsv, brouillons_hors_journal.tsv, scan_secrets.txt (counts only), lots_pont.json"""
import collections
import json
import os
import re
import sys

SECRET = {  # pattern name -> regex; only counts are written, never the matched text
    "aws_key_id": r"AKIA[0-9A-Z]{16}",
    "aws_secret_kw": r"aws_secret_access_key",
    "github_token": r"gh[pousr]_[A-Za-z0-9]{30,}",
    "openai_like_key": r"\bsk-[A-Za-z0-9_-]{20,}",
    "bearer": r"[Bb]earer\s+[A-Za-z0-9._-]{20,}",
    "password_kw": r"(?i)\b(password|mot de passe|mdp)\s*[:=]",
    "token_kw": r"(?i)\btoken\s*[:=]\s*\S{12,}",
    "private_key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "mdp_txt": r"(?i)mdp\.txt",
    "auth_json": r"(?i)auth\.json",
    "runtime_json": r"(?i)runtime\.json",
    "email": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}",
}


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def main():
    base = sys.argv[1]
    brut = os.path.join(base, "brut")
    recs = [json.loads(l) for l in open(os.path.join(brut, "state", "messages.jsonl"), encoding="utf-8") if l.strip()]
    recs.sort(key=lambda r: r["sequence"])
    who = {"claude": "LAB (Claude Code) -> Codex", "codex": "Codex -> LAB"}
    days = collections.defaultdict(list)
    for r in recs:
        days[r["timestamp"][:10]].append(r)
    out = os.path.join(base, "par_jour")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(base, "index.tsv"), "w", encoding="utf-8") as idx:
        idx.write("sequence\ttimestamp_utc\tdirection\treplyTo\tchars\tpremiere_ligne\n")
        for r in recs:
            first = norm(r["text"].splitlines()[0] if r["text"].strip() else "")[:140]
            idx.write("%d\t%s\t%s\t%s\t%d\t%s\n" % (r["sequence"], r["timestamp"], r["direction"], r.get("replyTo", ""),
                                                   len(r["text"]), first.replace("\t", " ")))
    stats = {}
    for d, rs in sorted(days.items()):
        with open(os.path.join(out, d + ".md"), "w", encoding="utf-8") as f:
            f.write("# Pont LAB <-> Codex, %s (UTC), messages %d a %d\n\n" % (d, rs[0]["sequence"], rs[-1]["sequence"]))
            f.write("Source : pont_codex/brut/state/messages.jsonl (copie du 20/10/2026). direction 'claude' = envoye par "
                    "LAB (session Claude Code), 'codex' = envoye par Codex.\n\n")
            for r in rs:
                rt = (" | en reponse a %s" % r["replyTo"]) if r.get("replyTo") else ""
                f.write("---\n\n## #%d | %s | %s%s\n\n" % (r["sequence"], r["timestamp"], who.get(r["direction"], r["direction"]), rt))
                f.write(r["text"].rstrip() + "\n\n")
        stats[d] = {"n": len(rs), "chars": sum(len(r["text"]) for r in rs), "seq": [rs[0]["sequence"], rs[-1]["sequence"]],
                    "codex": sum(r["direction"] == "codex" for r in rs), "claude": sum(r["direction"] == "claude" for r in rs)}
    # drafts (.txt) not found in the log
    corpus = norm("\n".join(r["text"] for r in recs))
    rows = []
    for sub in ("state", "messages", "racine"):
        d = os.path.join(brut, sub)
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".txt"):
                continue
            t = norm(open(os.path.join(d, fn), encoding="utf-8", errors="replace").read())
            probe = t[:300]
            found = bool(probe) and probe in corpus
            if not found and len(t) > 120:  # tolerate small edits: try a middle chunk
                mid = t[len(t) // 2: len(t) // 2 + 120]
                found = mid in corpus
            rows.append((sub, fn, len(t), found))
    with open(os.path.join(base, "brouillons_hors_journal.tsv"), "w", encoding="utf-8") as f:
        f.write("dossier\tfichier\tchars\tpresent_dans_le_journal\n")
        for row in rows:
            f.write("%s\t%s\t%d\t%s\n" % row)
    # secret scan, counts only
    hits = collections.Counter()
    files = [os.path.join(dp, fn) for dp, _, fns in os.walk(brut) for fn in fns]
    per_file = collections.defaultdict(collections.Counter)
    for p in files:
        t = open(p, encoding="utf-8", errors="replace").read()
        for k, rx in SECRET.items():
            n = len(re.findall(rx, t))
            if n:
                hits[k] += n
                per_file[os.path.relpath(p, brut)][k] += n
    with open(os.path.join(base, "scan_secrets.txt"), "w", encoding="utf-8") as f:
        f.write("Scan par motifs (comptes seulement, aucune valeur recopiee)\n")
        for k in SECRET:
            f.write("%-16s %d\n" % (k, hits[k]))
        f.write("\nfichiers touches:\n")
        for p, c in sorted(per_file.items()):
            f.write("%s\t%s\n" % (p, dict(c)))
    # balanced agent lots by characters, cut at day boundaries when possible
    seqs = [(r["sequence"], r["timestamp"], len(r["text"])) for r in recs]
    total = sum(c for _, _, c in seqs)
    k = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    target = total / k
    lots, cur, acc = [], [], 0
    for s in seqs:
        cur.append(s)
        acc += s[2]
        if acc >= target and len(lots) < k - 1:
            lots.append(cur)
            cur, acc = [], 0
    if cur:
        lots.append(cur)
    desc = [{"lot": "L11%s_pont" % chr(ord('a') + i), "seq_debut": l[0][0], "seq_fin": l[-1][0], "ts_debut": l[0][1],
             "ts_fin": l[-1][1], "messages": len(l), "chars": sum(c for _, _, c in l)} for i, l in enumerate(lots)]
    json.dump({"jours": stats, "lots": desc, "total_chars": total, "messages": len(recs)},
              open(os.path.join(base, "lots_pont.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps(desc, indent=1))
    print("drafts:", len(rows), "absent from log:", sum(1 for r in rows if not r[3]))
    print("secret scan:", dict(hits))


if __name__ == "__main__":
    main()
