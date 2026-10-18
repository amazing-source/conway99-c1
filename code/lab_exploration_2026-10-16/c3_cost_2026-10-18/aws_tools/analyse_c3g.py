"""Summary of the second c3 pass with Gram covers (runs c3ga/c3gb, LAB 18/10/2026).
Per template: cover status (from the job record), verdict of gram_cover_branch --table full, cross-check verdict."""
import glob, json, os, sys
from collections import Counter
dirs = sys.argv[1:] or ["collect_c3ga"]
verd, xc, cpu, gram, fails = Counter(), Counter(), [], [], []
excluded, open_ = [], []
for d in dirs:
    for f in glob.glob(os.path.join(d, "done", "*.json")):
        rec = json.load(open(f)); n = rec["id"]
        out = os.path.join(d, "files", "out", n + ".json")
        xo = os.path.join(d, "files", "out", "xc_" + n + ".json")
        if os.path.exists(out):
            r = json.load(open(out)); verd[r.get("status")] += 1
            cpu.append(r.get("cpu_seconds") or 0); gram.append(r.get("gram_count") or 0)
            (excluded if r.get("status") == "INFEASIBLE" else open_).append((n, r.get("gram_count")))
        else:
            verd["NO_VERDICT"] += 1
            fails.append((n, (rec.get("stdout_tail") or "")[-200:].strip().splitlines()[-1:] if rec.get("stdout_tail") else (rec.get("stderr_tail") or "")[-200:]))
        if os.path.exists(xo):
            x = json.load(open(xo)); xc[x.get("verdict")] += 1
            if x.get("verdict") != "LAB_COVER_CONFIRMED":
                xc["detail:" + str(x.get("codex_status")) + "/unexplained=" + str(x.get("unexplained")) + "/only_lab=" + str(x.get("only_lab"))] += 1
        else:
            xc["NO_CROSSCHECK"] += 1
print("jobs done:", sum(verd.values()), dict(verd))
print("cross-checks:", dict(xc))
if cpu:
    s = sorted(cpu); print("branch cpu median %.0f, mean %.0f" % (s[len(s) // 2], sum(s) / len(s)))
    g = sorted(gram); print("gram counts median", g[len(g) // 2], "max", g[-1])
print("no verdict examples:", fails[:5])
with open("c3g_excluded.tsv", "w", newline="\n") as fh:
    for n, gcount in sorted(excluded):
        fh.write("%s\t%s\n" % (n, gcount))
with open("c3g_open.tsv", "w", newline="\n") as fh:
    for n, gcount in sorted(open_):
        fh.write("%s\t%s\n" % (n, gcount))
