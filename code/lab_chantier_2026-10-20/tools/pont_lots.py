"""Write one readable file per bridge lot (ranges from lots_pont.json). usage: python pont_lots.py <pont_codex dir>"""
import json, os, sys
base = sys.argv[1]
recs = sorted((json.loads(l) for l in open(os.path.join(base, "brut", "state", "messages.jsonl"), encoding="utf-8") if l.strip()),
              key=lambda r: r["sequence"])
who = {"claude": "LAB (Claude Code) -> Codex", "codex": "Codex -> LAB"}
os.makedirs(os.path.join(base, "lots"), exist_ok=True)
for lot in json.load(open(os.path.join(base, "lots_pont.json"), encoding="utf-8"))["lots"]:
    rs = [r for r in recs if lot["seq_debut"] <= r["sequence"] <= lot["seq_fin"]]
    with open(os.path.join(base, "lots", lot["lot"] + ".md"), "w", encoding="utf-8") as f:
        f.write("# %s : messages %d a %d (%s .. %s UTC)\n\n" % (lot["lot"], lot["seq_debut"], lot["seq_fin"], lot["ts_debut"], lot["ts_fin"]))
        f.write("Source : pont_codex/brut/state/messages.jsonl. Citer un message par son numero : pont:#N.\n\n")
        for r in rs:
            rt = (" | en reponse a %s" % r["replyTo"]) if r.get("replyTo") else ""
            f.write("---\n\n## #%d | %s | %s%s\n\n%s\n\n" % (r["sequence"], r["timestamp"], who[r["direction"]], rt, r["text"].rstrip()))
    print(lot["lot"], len(rs), os.path.getsize(os.path.join(base, "lots", lot["lot"] + ".md")))
