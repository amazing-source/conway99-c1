"""Watch run verif1 (LAB 18/10/2026): every 3 minutes, read runs/verif1{a,b}/status.json from S3 and the state of the
instances tagged c1-verif1-*; print one line per change.  Flags: a Spot reclaim (instance gone while the run is not
all_done), failures, timeouts, a silent status (no update for 10 minutes).  Stops when both runs are all_done.
usage: py -3 watch_verif1.py   (needs the AWS CLI profile frere)"""
import json
import subprocess
import sys
import time

B = "conway99-c1-runs-733515672125"
A = ["aws", "--profile", "frere", "--region", "eu-north-1"]


def aws(args):
    r = subprocess.run(A + args, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


RUNS = sys.argv[1:]
last = {}
while True:
    rc, out, err = aws(["ec2", "describe-instances", "--filters", "Name=tag:Name,Values=c1-verif*",
                        "--query", "Reservations[].Instances[].[Tags[?Key=='Name']|[0].Value,InstanceId,State.Name]",
                        "--output", "json"])
    inst = json.loads(out) if rc == 0 and out.strip() else []
    if rc != 0 and "expired" in err.lower():
        print("AWS SESSION EXPIRED: re-login needed", flush=True)
        break
    alive = {n: s for n, i, s in inst if s in ("pending", "running")}
    alldone = True
    for m in RUNS:
        rc, out, err = aws(["s3", "cp", "s3://%s/runs/%s/status.json" % (B, m), "-"])
        st = json.loads(out) if rc == 0 and out.strip() else None
        line = "%s: %s" % (m, "no status yet" if st is None else
                                 "finished %(finished)s/%(total)s running %(running)s pending %(pending)s failed %(failed)s timeouts %(timeouts)s elapsed %(elapsed_s)ss" % st
                                 + (" ALL_DONE" if st.get("all_done") else ""))
        machine = alive.get("c1-" + m[:-1] + "-" + m[-1])
        line += " | machine: %s" % (machine or "none")
        if st is None or not st.get("all_done"):
            alldone = False
            if machine is None and st is not None:
                line += "  <<< MACHINE GONE BEFORE THE END (Spot reclaim?): relaunch with launch script of %s" % m
        if last.get(m) != line:
            print(time.strftime("%H:%M:%S"), line, flush=True)
            last[m] = line
    if alldone:
        print("BOTH RUNS ALL_DONE", flush=True)
        break
    time.sleep(180)
