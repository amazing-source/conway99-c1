"""Driver (LAB 15/10/2026): complete SAT enumeration (kernel_sat_enum.py) of the structures sharing each distinct
kernel of the 331 rank-30 objects (kernel_classes_331.json), one process at a time, 300 s cap per kernel.
usage: python ksat_all_kernels.py <log>"""
import json
import os
import subprocess
import sys

log = sys.argv[1]
d = json.load(open("rank30_psd_objects_2026-10-15.json"))
cls = json.load(open("kernel_classes_331.json"))
os.makedirs("ksat_kernels", exist_ok=True)
with open(log, "a", encoding="utf-8") as fh:
    for ci, members in enumerate(cls["classes"]):
        k = members[0]
        f = os.path.join("ksat_kernels", "obj%d.json" % k)
        json.dump({"labels": d["labels"], "edges": d["structures"][k]["edges"]}, open(f, "w"))
        r = subprocess.run([sys.executable, "kernel_sat_enum.py", f, "100000000", "300"], capture_output=True, text=True)
        out = [l.strip() for l in r.stdout.splitlines() if not l.startswith("progress")]
        fh.write("class %d (objects %s): %s%s\n" % (ci, members, " | ".join(out[1:]),
                                                     (" | ERR " + r.stderr.strip().splitlines()[-1]) if r.returncode else ""))
        fh.flush()
