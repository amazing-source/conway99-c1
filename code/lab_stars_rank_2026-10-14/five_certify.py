"""Certification of UNSAT five-star cases (LAB 16/10/2026), one case at a time to respect the free disk space.
For each case: write the CNF (same construction as five_split_par.py), run cadical with a binary DRAT proof, verify it
with drat-trim, record the verdict and the SHA-256 of the CNF, delete the proof.  Only cases already found UNSAT
should be passed.  usage: python five_certify.py <work dir> <cadical exe> <drat-trim exe> <case list, e.g. 0,3,7>"""
import hashlib
import json
import os
import subprocess
import sys
import time

import five_split_par_core as core  # noqa: E402  (module written from five_split_par.py, same orbit order)

wd, cad, dt = sys.argv[1], sys.argv[2], sys.argv[3]
cases = [int(t) for t in sys.argv[4].split(",")]
os.makedirs(wd, exist_ok=True)
log = os.path.join(wd, "certificates.jsonl")
for k in cases:
    cnf = os.path.join(wd, "case%03d.cnf" % k)
    core.write_case(k, cnf)
    sha = hashlib.sha256(open(cnf, "rb").read()).hexdigest()
    proof = os.path.join(wd, "case%03d.drat" % k)
    t0 = time.time()
    r = subprocess.run([cad, "-q", "--binary=true", cnf, proof], capture_output=True, text=True)
    t1 = time.time()
    if r.returncode != 20:
        row = {"case": k, "status": "NOT_UNSAT(%d)" % r.returncode, "sha256": sha}
    else:
        size = os.path.getsize(proof)
        v = subprocess.run([dt, cnf, proof], capture_output=True, text=True)
        ok = "s VERIFIED" in v.stdout
        row = {"case": k, "status": "UNSAT", "drat_verified": ok, "proof_bytes": size, "solve_s": round(t1 - t0, 1),
               "verify_s": round(time.time() - t1, 1), "sha256": sha, "drat_trim_tail": v.stdout[-300:]}
    with open(log, "a") as fh:
        fh.write(json.dumps(row) + "\n")
    print(json.dumps({x: row[x] for x in row if x != "drat_trim_tail"}), flush=True)
    for f in (proof, cnf):
        if os.path.exists(f):
            os.remove(f)
