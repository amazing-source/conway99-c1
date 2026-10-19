"""K2BC cost/strength sample: 2 boundaries (start and middle) of each of the 28 core types; one process, BELOW_NORMAL."""
import gzip, json, subprocess, sys, time
from pathlib import Path
S = Path(__file__).resolve().parent
W = Path(r"C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/exploration_2026-10-16/gz5602_2026-10-19")
out = open(S / "sample_k2bc.txt", "a", encoding="utf8")
for ci in json.load(open(S / "pybd_k2bc_all" / "core_reps_flips.json"))["representatives"]:
    bf = S / "pybd_k2bc_all" / ("core_%03d.json.gz" % ci)
    n = json.load(gzip.open(bf))["boundary_count"]
    for st in sorted({0, n // 2}):
        t = time.time()
        try:
            r = subprocess.run([sys.executable, "-X", "utf8", str(W / "py_extend_gen.py"), str(S / "k3prod_v4/pkg/code/codex"), "GEN",
                                str(bf), str(st), "1", "--sat", "--lean", "--enc=seq", "--yr=45", "--extra=13,26"],
                               capture_output=True, text=True, timeout=900, creationflags=0x00004000)
            last = (r.stdout.strip().splitlines() or [""])[-1]
            d = json.loads(last) if last.startswith("{") else {}
            out.write("%03d n=%d b=%d %s cpu=%s wall=%.0f\n" % (ci, n, st, d.get("statuses"), d.get("cpu_seconds"), time.time() - t))
        except subprocess.TimeoutExpired:
            out.write("%03d n=%d b=%d TIMEOUT\n" % (ci, n, st))
        out.flush()
out.write("END\n"); out.close()
