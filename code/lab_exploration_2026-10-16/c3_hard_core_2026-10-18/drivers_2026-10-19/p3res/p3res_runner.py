"""P3 residual runner for AWS (LAB 19/10/2026).  The production p3prod leaves some borders not excluded (UNKNOWN at its
200k-conflict budget).  This runner watches the p3prod shards in S3 and re-runs every such border exactly as the local
second_pass.py does: py_extend.py (LAB 3d31ec7d) P3 --sat --lean --enc=seq --all-attachments --conflicts=3000000
--indices=[border], one border per job, 3 h timeout (the whole process group is killed on timeout).  Outputs:
runs/p3res/files/p3_residual/coreXXX_bBBBBBB.json.gz and runs/p3res/done/coreXXX_bBBBBBB.json; status.json every scan.
Static list p3res_static.json: borders already known non-excluded ('todo') and borders done or running on the lab PC
('skip').  Ends when p3prod reports all_done, a full scan started after that has been made, and every queued border
has finished.
usage: python p3res_runner.py --workers N [--repo /work/repo]"""
import argparse
import gzip
import json
import os
import shlex
import signal
import subprocess
import threading
import time
from pathlib import Path

import boto3

ap = argparse.ArgumentParser()
ap.add_argument("--workers", type=int, default=os.cpu_count())
ap.add_argument("--repo", default="/work/repo")
args = ap.parse_args()
B = "conway99-c1-runs-733515672125"
s3 = boto3.client("s3", region_name="eu-north-1")
PRE = "runs/p3res/"
SHARDS = "runs/p3prod/files/data/p3_shards/"
repo = Path(args.repo)
for d in ("idx", "out", "shards"):
    (repo / d).mkdir(exist_ok=True)
static = json.load(open(repo / "p3res_static.json"))
skip = {tuple(x) for x in static["skip"]}
lock = threading.Lock()
queue, submitted, open_list = [], set(), []
state = dict(started=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), workers=args.workers, submitted=0, finished=0,
             running=0, failed=0, timeouts=0, excluded=0, not_excluded=0, scans=0, shards_seen=0)
t0 = time.time()
STOP = threading.Event()
THREADS1 = "export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1; "


def put_json(key, value):
    s3.put_object(Bucket=B, Key=PRE + key, Body=json.dumps(value, indent=1).encode())


def add(ci, n, bi):
    with lock:
        if (ci, bi) in skip or (ci, bi) in submitted:
            return
        submitted.add((ci, bi))
        queue.append((ci, n, bi))
        state["submitted"] = len(submitted)


for ci, n, bi in static["todo"]:
    add(ci, n, bi)
seen = {}


def scan():
    pag = s3.get_paginator("list_objects_v2")
    for page in pag.paginate(Bucket=B, Prefix=SHARDS):
        for o in page.get("Contents", []):
            k = o["Key"]
            if not k.endswith(".json.gz") or seen.get(k) == o["ETag"]:
                continue
            dst = repo / "shards" / os.path.basename(k)
            s3.download_file(B, k, str(dst))
            d = json.load(gzip.open(dst))
            seen[k] = o["ETag"]
            for c in d["cases"]:
                if not c["status"].startswith("EXCLUDED"):
                    add(d["core_index"], d["total_boundaries"], c["boundary_index"])
    with lock:
        state["scans"] += 1
        state["shards_seen"] = len(seen)


def p3prod_done():
    try:
        st = json.loads(s3.get_object(Bucket=B, Key="runs/p3prod/status.json")["Body"].read())
        return bool(st.get("all_done"))
    except Exception:
        return False


def run_one(cpu, ci, n, bi):
    name = "core%03d_b%06d" % (ci, bi)
    (repo / "idx" / ("idx_%s.json" % name)).write_text(json.dumps([bi]))
    out = "out/%s.json.gz" % name
    cmd = ("python -I -u -X utf8 code/lab/py_extend.py code/codex P3 data/p3_boundaries/core_%03d.json.gz 0 %d --sat --lean "
           "--enc=seq --all-attachments --conflicts=3000000 --indices=idx/idx_%s.json --out=%s") % (ci, n, name, out)
    full = "taskset -c %d /usr/bin/time -f 'MAXRSS_KB=%%M' bash -c %s" % (cpu, shlex.quote(THREADS1 + cmd))
    t = time.time()
    p = subprocess.Popen(full, shell=True, cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                         start_new_session=True)
    try:
        so, se = p.communicate(timeout=10800)
        code, to = p.returncode, False
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        so, se = p.communicate()
        code, to = None, True
    rss = [l for l in se.splitlines() if l.startswith("MAXRSS_KB=")]
    rec = dict(id=name, core=ci, border=bi, cmd=cmd, exit=code, hard_timeout=to, wall=round(time.time() - t, 2), cpu=cpu,
               maxrss_kb=int(rss[-1].split("=")[1]) if rss else None, stdout_tail=so[-20000:], stderr_tail=se[-5000:])
    f = repo / out
    status = None
    if f.exists():
        s3.upload_file(str(f), B, PRE + "files/p3_residual/%s.json.gz" % name)
        try:
            status = json.load(gzip.open(f))["cases"][0]["status"]
        except Exception:
            status = "UNREADABLE"
    rec["case_status"] = status
    put_json("done/%s.json" % name, rec)
    with lock:
        state["finished"] += 1
        state["failed"] += code != 0
        state["timeouts"] += to
        if status and status.startswith("EXCLUDED"):
            state["excluded"] += 1
        else:
            state["not_excluded"] += 1
            open_list.append([ci, bi, status, code])


def worker(cpu):
    while True:
        with lock:
            job = queue.pop(0) if queue else None
            if job:
                state["running"] += 1
        if job is None:
            if STOP.is_set():
                return
            time.sleep(10)
            continue
        try:
            run_one(cpu, *job)
        finally:
            with lock:
                state["running"] -= 1


threads = [threading.Thread(target=worker, args=(c,), daemon=True) for c in range(args.workers)]
for th in threads:
    th.start()
while True:
    done_flag = p3prod_done()          # observed BEFORE the scan: if true, every p3prod shard is already in S3
    try:
        scan()
        scanned = True
    except Exception as e:
        scanned = False
        with lock:
            state["scan_error"] = repr(e)[:300]
    with lock:
        idle = not queue and state["running"] == 0
        snap = dict(state, elapsed_s=round(time.time() - t0), pending=len(queue), p3prod_all_done=done_flag,
                    open_list=list(open_list))
    put_json("status.json", snap)
    if done_flag and scanned and idle:
        break
    time.sleep(120)
STOP.set()
for th in threads:
    th.join()
with lock:
    put_json("status.json", dict(state, elapsed_s=round(time.time() - t0), pending=0, all_done=True,
                                 open_list=list(open_list)))
