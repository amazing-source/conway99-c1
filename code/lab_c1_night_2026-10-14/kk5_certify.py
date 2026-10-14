"""Checked proofs for the first pass of kk5 (NOTE_NIGHT section 16).

For every class of M_11 marked UNSAT in kk5_all_log.txt: rebuild the instance exactly as kk5_all.py does, let
cadical write a DRAT proof, and have drat-trim check it. Log kk5_certify_log.txt: K count cadical drat seconds.
What is certified: the CNF written by srg_sat.encode is unsatisfiable. The encoder itself is not certified here
(its controls: control_local9.py, control_243.py).

usage: python kk5_certify.py workdir limit        One process, calls in sequence, 2 GB bound.
"""
import ast
import subprocess
import sys
import time

import family as FAM
import h12_instance as H
import srg_sat as S

TOOLS = r"C:\Users\RESEARCHER\Desktop\Recherche_Conway\c1-codex\tools\win64"
workdir, limit = sys.argv[1], float(sys.argv[2])
cases = []
for line in open("kk5_all_log.txt"):
    t = line.split(None, 4)
    if len(t) == 5 and t[2] == "UNSAT":
        cases.append((int(t[0]), int(t[1]), ast.literal_eval(t[4])))
print("classes to certify:", len(cases), flush=True)
for K, cnt, m11 in cases:
    pres = FAM.prescriptions("kk5")
    pres[11] = list(m11)
    n, k, lam, mu, fixed, mate, outer, idx = H.build(FAM.share_from(pres))
    enc, e = S.encode(n, k, lam, mu, fixed)
    cnf, proof = workdir + "/kk5_cert.cnf", workdir + "/kk5_cert.drat"
    S.write_dimacs(enc, cnf)
    t0 = time.time()
    try:
        r = subprocess.run([TOOLS + r"\cadical.exe", "-q", cnf, proof], capture_output=True, text=True, timeout=limit)
        v = "UNSAT" if "s UNSATISFIABLE" in r.stdout else "OTHER"
    except subprocess.TimeoutExpired:
        v = "UNKNOWN"
    d = "-"
    if v == "UNSAT":
        r = subprocess.run([TOOLS + r"\drat-trim.exe", cnf, proof, "-w"], capture_output=True, text=True)
        d = "VERIFIED" if "s VERIFIED" in r.stdout else "NOT_VERIFIED"
    line = "%d %d %s %s %.1f" % (K, cnt, v, d, time.time() - t0)
    print(line, flush=True)
    open("kk5_certify_log.txt", "a").write(line + "\n")
