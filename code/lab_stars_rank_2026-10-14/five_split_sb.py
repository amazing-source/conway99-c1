"""Parallel run of the 34 five-star cases WITH lex-leader symmetry breaking (five_symbreak.py), LAB 16/10/2026.
usage: python five_split_sb.py <out dir> <cadical exe> <workers> <seconds per case> <case list e.g. 1-33 or 4,7,9>"""
import concurrent.futures as cf
import json
import os
import subprocess
import sys
import threading
import time

out, cad, workers, limit, sel = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
os.makedirs(out, exist_ok=True)
if "-" in sel:
    lo, hi = (int(t) for t in sel.split("-"))
    cases = list(range(lo, hi + 1))
else:
    cases = [int(t) for t in sel.split(",")]
lock = threading.Lock()
here = os.path.dirname(os.path.abspath(__file__))


def run(k):
    cnf = os.path.join(out, "case%03d_sb.cnf" % k)
    subprocess.run([sys.executable, os.path.join(here, "five_symbreak.py"), str(k), cnf, "200"], capture_output=True)
    t0 = time.time()
    p = subprocess.Popen([cad, "-q", cnf], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        so, se = p.communicate(timeout=limit)
        st = {10: "SAT", 20: "UNSAT"}.get(p.returncode, "UNKNOWN(%d)" % p.returncode)
    except subprocess.TimeoutExpired:
        p.kill()
        so, se = p.communicate()
        st = "TIMEOUT"
    row = {"case": k, "status": st, "seconds": round(time.time() - t0, 1), "symmetry_breaking": "lex-leader, 200 elements"}
    with lock:
        with open(os.path.join(out, "results_sb.jsonl"), "a") as fh:
            fh.write(json.dumps(row) + "\n")
        if st == "SAT":
            open(os.path.join(out, "case%03d_sb.model" % k), "w").write(so)
    os.remove(cnf)
    return row


with cf.ThreadPoolExecutor(max_workers=workers) as ex:
    list(ex.map(run, cases))
print("all done", flush=True)
