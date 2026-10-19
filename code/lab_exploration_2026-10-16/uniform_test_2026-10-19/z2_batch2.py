"""Run a z2 probe script on a list of gz templates (worker k of N), with a per-template cap; one JSONL line each.
usage: python z2_batch2.py <list.json> <k> <N> <out.jsonl> <script> <cap seconds> [extra args...]"""
import json, subprocess, sys, os
lst, k, N, out, script, cap, extra = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5], int(sys.argv[6]), sys.argv[7:]
here = os.path.dirname(os.path.abspath(__file__))
CX = "C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/code/codex"
CAT = "C:/home/researcher/Desktop/Recherche_Conway/c1-main-codex/code/lab_exploration_2026-10-16/c3_root_cover/c3_open_templates_k3_12.json.gz"
items = json.load(open(lst))
done = set()
if os.path.exists(out):
    done = {json.loads(l)["index"] for l in open(out) if l.strip()}
for i, it in enumerate(items):
    if i % N != k or it["index"] in done:
        continue
    try:
        r = subprocess.run([sys.executable, "-X", "utf8", os.path.join(here, script), CX, CAT, str(it["index"])] + extra,
                           capture_output=True, text=True, timeout=cap, creationflags=0x00004000)
        line = (r.stdout.strip().splitlines() or ["{}"])[-1]
        rec = json.loads(line) if line.startswith("{") else {"error": r.stderr[-300:]}
    except subprocess.TimeoutExpired:
        rec = {"lp_status": "TIMEOUT_%ds" % cap}
    rec.update(index=it["index"], group=it["group"])
    with open(out, "a") as f:
        f.write(json.dumps(rec) + "\n")
