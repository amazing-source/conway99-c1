"""All 64 corners of harm4_exact.py for one rank and truncation.   python run_corners_exact.py <rank> <nmax>"""
import subprocess, sys, os, time, collections
r, nmax = sys.argv[1], sys.argv[2]; t0 = time.time(); res = {}
for i in range(64):
    c = format(i, "06b")
    out = subprocess.run([sys.executable, "harm4_exact.py", r, nmax, "VT"], capture_output=True, text=True, env=dict(os.environ, CORNER=c)).stdout.strip().split("\n")[-1]
    res[c] = "feasible" if out.startswith("EXACT: feasible") else out
cnt = collections.Counter("feasible" if v == "feasible" else "other" for v in res.values())
print("rank %s, nmax %s: %s  [%.0f s]" % (r, nmax, dict(cnt), time.time() - t0))
for c, v in res.items():
    if v != "feasible": print("  corner %s: %s" % (c, v[:260]))
