"""Watch AWS runs in any region (LAB 18/10/2026): every 3 minutes, read runs/<run>/status.json from S3 and the state of
the instance tagged with the given Name in the given region; print one line per change (progress, failures, timeouts,
machine gone before all_done = Spot reclaim).  Stops when every run is all_done.
usage: py -3 -u watch_any.py <run>:<region>:<Name tag> [...]"""
import json
import subprocess
import sys
import time

B = "conway99-c1-runs-733515672125"


def aws(region, args):
    r = subprocess.run(["aws", "--profile", "frere", "--region", region] + args, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


specs = [a.split(":") for a in sys.argv[1:]]
last = {}
while True:
    alldone = True
    for run, region, tag in specs:
        rc, out, err = aws(region, ["ec2", "describe-instances", "--filters", "Name=tag:Name,Values=" + tag,
                                    "Name=instance-state-name,Values=pending,running",
                                    "--query", "Reservations[].Instances[].InstanceId", "--output", "text"])
        if rc != 0 and "expired" in err.lower():
            print("AWS SESSION EXPIRED: re-login needed", flush=True)
            sys.exit(0)
        machine = out.strip() or "none"
        rc, out, err = aws("eu-north-1", ["s3", "cp", "s3://%s/runs/%s/status.json" % (B, run), "-"])
        st = json.loads(out) if rc == 0 and out.strip() else None
        if st is None:
            line = "%s: no status yet | machine %s" % (run, machine)
            alldone = False
        else:
            line = ("%s: finished %s/%s running %s pending %s failed %s timeouts %s | machine %s"
                    % (run, st["finished"], st["total"], st["running"], st["pending"], st["failed"], st["timeouts"], machine))
            if st.get("all_done"):
                line += " ALL_DONE"
            else:
                alldone = False
                if machine == "none":
                    line += "  <<< MACHINE GONE BEFORE THE END (Spot reclaim or hard cap)"
        # report progress coarsely (every 100 finished) and every change of failures/timeouts/machine
        coarse = (line.split(" finished ")[0], st and st["finished"] // 100, st and st["failed"], st and st["timeouts"],
                  machine, st and st.get("all_done"))
        if last.get(run) != coarse:
            print(time.strftime("%H:%M:%S"), line, flush=True)
            last[run] = coarse
    if alldone:
        print("ALL RUNS DONE", flush=True)
        break
    time.sleep(180)
