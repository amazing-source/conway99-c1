"""POSITIVE CONTROL of the flag campaign on srg(243,22,1,2) (LAB 19/10/2026).  Real graphs exist there (BvLS has
P = 8910 prisms, the twin 2430), so every valid upper bound on P must stay >= 8910 and every valid lower bound <= 2430.
Same pipeline as the Conway run: census2 order 10 for (v,k) = (243,22), forms, flag blocks (7,8) and (8,9), then
(a) the AWS-style loop flag_cut_loop.py (diagonal normalisation without floor) and (b) flag_cut_exact.py (floored
normalisation, integer cuts, warm-started HiGHS), max and min P.  Uploads to runs/flagctl/."""
import glob, json, os, subprocess, sys, threading, time
import boto3
B = "conway99-c1-runs-733515672125"; PRE = "runs/flagctl/"
s3 = boto3.client("s3", region_name="eu-north-1")
W = os.cpu_count() - 2
R = "/work/repo"; os.chdir(R)
state = {"started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "phase": "census"}
def put(key, val):
    s3.put_object(Bucket=B, Key=PRE + key, Body=json.dumps(val, indent=1).encode())
def up(path, key=None):
    try:
        s3.upload_file(path, B, PRE + (key or os.path.basename(path)))
    except Exception as e:
        state.setdefault("upload_errors", []).append(str(e)[:200])
def hb():
    while True:
        try:
            put("status.json", dict(state, t=time.strftime("%H:%M:%S", time.gmtime())))
        except Exception:
            pass
        time.sleep(60)
threading.Thread(target=hb, daemon=True).start()
env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1")
py = sys.executable
def run(cmd, log, cwd=R):
    with open(log, "w") as f:
        return subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, env=env, cwd=cwd).returncode
rc = run([py, "census2.py", "census", "10", "243", "22", R + "/census243_10.json", "nocheck"], R + "/census.log",
         cwd=R + "/census2_code")
up("census.log"); state["census_rc"] = rc
state["phase"] = "forms"
run([py, "flag_engine.py", "forms", "census243_10.json", "forms243.npz"], "forms.log"); up("forms.log")
state["phase"] = "build"
procs = []
for k, m, n, w in ((7, 8, 208, 16), (8, 9, 916, W - 16)):
    procs.append(subprocess.Popen([py, "flag_engine.py", "build", "census243_10.json", str(k), str(m), "0", str(n),
                                   "T243", "--workers=%d" % w], stdout=open("build_%d.log" % k, "w"),
                                  stderr=subprocess.STDOUT, env=env))
while any(p.poll() is None for p in procs):
    state["built"] = len(glob.glob("T243/T_*.npz")); time.sleep(30)
state["built"] = len(glob.glob("T243/T_*.npz"))
for k in (7, 8):
    up("build_%d.log" % k)
state["phase"] = "cuts"
runs = []
for tool in ("loop", "exact"):
    for sense in ("max", "min"):
        script = "flag_cut_loop.py" if tool == "loop" else "flag_cut_exact.py"
        cmd = [py, script, "forms243.npz", "T243", "--obj=" + sense, "--maxit=200", "--per=1",
               "--log=ctl_%s_%s.log" % (tool, sense)]
        runs.append(("%s_%s" % (tool, sense), subprocess.Popen(cmd, stdout=open("ctl_%s_%s.out" % (tool, sense), "w"),
                                                              stderr=subprocess.STDOUT, env=env)))
lp = [py, "flag_cut_loop.py", "forms243.npz", "--obj=max", "--maxit=1", "--log=ctl_lp_max.log"]
runs.append(("lp_max", subprocess.Popen(lp, stdout=open("ctl_lp_max.out", "w"), stderr=subprocess.STDOUT, env=env)))
deadline = time.time() + 100 * 60
while any(p.poll() is None for _, p in runs) and time.time() < deadline:
    for name, p in runs:
        for f in glob.glob("ctl_*"):
            up(f)
    state["running"] = sum(p.poll() is None for _, p in runs)
    time.sleep(90)
for name, p in runs:
    if p.poll() is None:
        p.terminate()
for f in glob.glob("ctl_*"):
    up(f)
state["phase"] = "done"; put("status.json", state)
