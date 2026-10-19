"""Run z2_probe.py on a list of gz templates (worker k of N), 300 s cap per template, one JSONL line each."""
import json, subprocess, sys, os
lst, k, N, out, extra = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5:]
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
        r = subprocess.run([sys.executable, "-X", "utf8", os.path.join(here, "z2_probe.py"), CX, CAT, str(it["index"])] + extra,
                           capture_output=True, text=True, timeout=300, creationflags=0x00004000)
        line = (r.stdout.strip().splitlines() or ["{}"])[-1]
        rec = json.loads(line) if line.startswith("{") else {"error": r.stderr[-300:]}
    except subprocess.TimeoutExpired:
        rec = {"lp_status": "TIMEOUT_300s"}
    rec.update(index=it["index"], group=it["group"], methods=it["methods"], dim=it["dim"])
    with open(out, "a") as f:
        f.write(json.dumps(rec) + "\n")
