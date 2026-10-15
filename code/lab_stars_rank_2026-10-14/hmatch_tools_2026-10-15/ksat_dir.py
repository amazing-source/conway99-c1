"""Driver: complete SAT enumeration (kernel_sat_enum.py) of every class representative in a directory, sequentially.
usage: python ksat_dir.py <dir> <log> [seconds per class]"""
import glob, os, subprocess, sys
d, log = sys.argv[1], sys.argv[2]
cap = sys.argv[3] if len(sys.argv) > 3 else "300"
with open(log, "a", encoding="utf-8") as fh:
    for f in sorted(glob.glob(os.path.join(d, "newk_*.json")), key=lambda p: int(p.split("_")[-1].split(".")[0])):
        r = subprocess.run([sys.executable, "kernel_sat_enum.py", f, "100000000", cap], capture_output=True, text=True)
        out = [l.strip() for l in r.stdout.splitlines() if not l.startswith("progress")]
        fh.write("%s: %s%s\n" % (f, " | ".join(out[1:]), (" | ERR " + r.stderr.strip().splitlines()[-1]) if r.returncode else ""))
        fh.flush()
