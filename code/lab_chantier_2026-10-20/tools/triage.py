"""Triage of the inventory: prose notes vs run logs, grouped by origin (first location).  usage: python triage.py <notes.jsonl> <out.json>"""
import collections
import json
import os
import re
import sys

LOG = re.compile(r"(^|/)(logs?|runs?|out|outputs?|results?|prod|raw|data|tasks|aws_c1|stdout|stderr)(/|$)"
                 r"|\.log$|_log\.txt$|\.out$|stdout|stderr", re.I)


def group(loc):
    path = loc["path"].replace("\\", "/")
    if loc["kind"] == "git":
        return "git:" + loc["repo"]
    root = os.path.basename(loc["repo"].replace("\\", "/").rstrip("/"))
    parts = path.split("/")
    first = "/".join(parts[:2]) if (root.startswith("conway_c2_researcher2") and parts[0] == "work") else parts[0]
    return "fs:%s/%s" % (root, first)


def main():
    recs = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8")]
    prose, logs, psize = collections.Counter(), collections.Counter(), collections.Counter()
    tagged = []
    for r in recs:
        loc = r["locations"][0]
        g = group(loc)
        title = r.get("title") or ""
        is_log = r["ext"] == ".txt" and (bool(LOG.search(loc["path"].replace("\\", "/"))) or title.startswith(("{", "[", "+", "|")))
        r["group"], r["kind_guess"] = g, "log" if is_log else "prose"
        tagged.append(r)
        if is_log:
            logs[g] += 1
        else:
            prose[g] += 1
            psize[g] += r["size"]
    print("prose-like notes:", sum(prose.values()), "| log-like txt:", sum(logs.values()))
    print("%-72s %6s %6s %8s" % ("group (first location)", "prose", "logs", "prose MB"))
    for g, n in sorted(prose.items(), key=lambda kv: -kv[1])[:70]:
        print("%-72s %6d %6d %8.1f" % (g[:72], n, logs.get(g, 0), psize[g] / 1e6))
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        for r in tagged:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
