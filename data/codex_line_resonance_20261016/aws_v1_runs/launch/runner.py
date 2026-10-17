"""Parallel job runner for the AWS instance (LAB 18/10/2026).  Manifest: one job per line,
    job_id <TAB> timeout_seconds <TAB> shell command [<TAB> comma-separated output paths, relative to the repo]
Each job runs in the repo directory under `taskset -c <its own cpu>` (Codex's limit_research_process pins a process to
the first CPUs of its affinity set, so a distinct single-CPU affinity per job is required).  Results go to S3 at once:
runs/<run>/done/<job_id>.json (exit code, wall time, tails of stdout/stderr) and runs/<run>/files/<path> for outputs.
A job whose done file already exists in S3 is skipped (restart after a Spot interruption).  status.json every 60 s."""
import argparse
import json
import os
import shlex
import subprocess
import threading
import time
from pathlib import Path

import boto3

ap = argparse.ArgumentParser()
ap.add_argument("--bucket", required=True)
ap.add_argument("--run", required=True)
ap.add_argument("--manifest", required=True)
ap.add_argument("--repo", default="/work/repo")
ap.add_argument("--workers", type=int, default=os.cpu_count())
args = ap.parse_args()
s3 = boto3.client("s3", region_name="eu-north-1")
prefix = "runs/%s/" % args.run
t0 = time.time()


def put_json(key, value):
    s3.put_object(Bucket=args.bucket, Key=prefix + key, Body=json.dumps(value, indent=1).encode())


def done_keys():
    keys = set()
    pag = s3.get_paginator("list_objects_v2")
    for page in pag.paginate(Bucket=args.bucket, Prefix=prefix + "done/"):
        for o in page.get("Contents", []):
            keys.add(o["Key"][len(prefix + "done/"):-len(".json")])
    return keys


jobs = []
for line in open(args.manifest, encoding="utf-8"):
    line = line.rstrip("\n")
    if not line.strip() or line.startswith("#"):
        continue
    parts = line.split("\t")
    jobs.append(dict(id=parts[0], timeout=float(parts[1]), cmd=parts[2],
                     outputs=[p for p in (parts[3].split(",") if len(parts) > 3 else []) if p]))
already = done_keys()
todo = [j for j in jobs if j["id"] not in already]
state = dict(total=len(jobs), skipped=len(already & {j["id"] for j in jobs}), finished=0, running=0, failed=0,
             timeouts=0, started=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), workers=args.workers)
lock = threading.Lock()
queue = list(todo)


THREADS1 = "export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1; "
MIN_FREE_GIB = 4.0


def mem_available_gib():
    for line in open("/proc/meminfo"):
        if line.startswith("MemAvailable:"):
            return int(line.split()[1]) / 1048576.0
    return 1e9


def run_one(cpu, job):
    t = time.time()
    cmd = "taskset -c %d /usr/bin/time -f 'MAXRSS_KB=%%M' bash -c %s" % (cpu, shlex.quote(THREADS1 + job["cmd"]))
    try:
        p = subprocess.run(cmd, shell=True, cwd=args.repo, capture_output=True, text=True, timeout=job["timeout"] + 60,
                           start_new_session=True)
        code, out, err, to = p.returncode, p.stdout, p.stderr, False
    except subprocess.TimeoutExpired as e:
        code, out, err, to = None, (e.stdout or b"").decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or ""), \
            (e.stderr or b"").decode(errors="replace") if isinstance(e.stderr, bytes) else (e.stderr or ""), True
    rss = [l for l in err.splitlines() if l.startswith("MAXRSS_KB=")]
    rec = dict(id=job["id"], cmd=job["cmd"], exit=code, hard_timeout=to, wall=round(time.time() - t, 2), cpu=cpu,
               maxrss_kb=int(rss[-1].split("=")[1]) if rss else None,
               stdout_tail=out[-20000:], stderr_tail=err[-5000:], outputs={})
    for rel in job["outputs"]:
        f = Path(args.repo) / rel
        if f.exists():
            s3.upload_file(str(f), args.bucket, prefix + "files/" + rel)
            rec["outputs"][rel] = f.stat().st_size
        else:
            rec["outputs"][rel] = None
    put_json("done/%s.json" % job["id"], rec)
    with lock:
        state["finished"] += 1
        state["failed"] += code not in (0,)
        state["timeouts"] += to


def worker(cpu):
    while True:
        while mem_available_gib() < MIN_FREE_GIB:
            with lock:
                state["memory_waits"] = state.get("memory_waits", 0) + 1
            time.sleep(5)
        with lock:
            if not queue:
                return
            job = queue.pop(0)
            state["running"] += 1
        try:
            run_one(cpu, job)
        finally:
            with lock:
                state["running"] -= 1


threads = [threading.Thread(target=worker, args=(c,), daemon=True) for c in range(args.workers)]
for th in threads:
    th.start()
while any(th.is_alive() for th in threads):
    with lock:
        snap = dict(state, elapsed_s=round(time.time() - t0), pending=len(queue))
    put_json("status.json", snap)
    time.sleep(60)
with lock:
    put_json("status.json", dict(state, elapsed_s=round(time.time() - t0), pending=0, all_done=True))
