"""AWS runner of the flag-algebra campaign (LAB 19/10/2026).  On the instance: build the form matrix and E3 zeros of
the order-10 census, all flag blocks (k,m) in {(5,7), (7,8), (8,9)} with the order-10 type ids, then cutting-plane
runs (min and max P) for five constraint sets, in parallel.  Everything is uploaded to
s3://conway99-c1-runs-733515672125/runs/flags/ as it is produced; status.json every minute."""
import glob, json, os, subprocess, sys, threading, time
import boto3
B = "conway99-c1-runs-733515672125"; PRE = "runs/flags/"
s3 = boto3.client("s3", region_name="eu-north-1")
W = os.cpu_count() - 2
R = "/work/repo"; J10 = R + "/census10.json"
os.chdir(R)
state = {"started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "phase": "init", "workers": W}
def put(key, val):
    s3.put_object(Bucket=B, Key=PRE + key, Body=json.dumps(val, indent=1).encode())
def up(path, key):
    try:
        s3.upload_file(path, B, PRE + key)
    except Exception as e:
        state.setdefault("upload_errors", []).append(str(e)[:200])
def heartbeat():
    while True:
        try:
            put("status.json", dict(state, t=time.strftime("%H:%M:%S", time.gmtime())))
        except Exception:
            pass
        time.sleep(60)
threading.Thread(target=heartbeat, daemon=True).start()
env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1")
py = sys.executable
def run(cmd, log):
    with open(log, "w") as f:
        return subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, env=env).returncode
state["phase"] = "forms"
run([py, "flag_engine.py", "forms", J10, "forms10.npz"], "forms10.log"); up("forms10.log", "forms10.log")
run([py, "e3_zero_ids.py", J10, "e3_zero10.txt"], "e3.log"); up("e3.log", "e3.log"); up("e3_zero10.txt", "e3_zero10.txt")
state["phase"] = "build"
t0 = time.time()
procs = []
# one pool process per config, the (5,7) one first (heaviest per sigma)
for k, m, n, w in ((5, 7, 21, 21), (7, 8, 208, max(8, W // 6)), (8, 9, 916, max(8, W - 21 - W // 6))):
    p = subprocess.Popen([py, "flag_engine.py", "build", J10, str(k), str(m), "0", str(n), "T10",
                          "--workers=%d" % w], stdout=open("build_%d_%d.log" % (k, m), "w"), stderr=subprocess.STDOUT, env=env)
    procs.append((k, m, p))
while any(p.poll() is None for _, _, p in procs):
    state["built"] = len(glob.glob("T10/T_*.npz")); state["build_s"] = round(time.time() - t0)
    time.sleep(30)
state["built"] = len(glob.glob("T10/T_*.npz")); state["build_s"] = round(time.time() - t0)
for k, m, p in procs:
    up("build_%d_%d.log" % (k, m), "build_%d_%d.log" % (k, m))
subprocess.run("tar czf T10.tar.gz T10", shell=True); up("T10.tar.gz", "T10.tar.gz")
state["phase"] = "cuts"
os.makedirs("sets", exist_ok=True)
def mk(name, pats):
    d = "sets/" + name; os.makedirs(d, exist_ok=True)
    for pat in pats:
        for f in glob.glob("T10/" + pat):
            dst = os.path.join(d, os.path.basename(f))
            if not os.path.exists(dst):
                os.symlink(os.path.abspath(f), dst)
    return d
sets = {"lp": None, "lp_e3": None, "e3_57": mk("e3_57", ["T_k5_m7_*"]), "e3_7889": mk("e3_7889", ["T_k7_m8_*", "T_k8_m9_*"]),
        "e3_all": mk("e3_all", ["T_k*"])}
cuts = []
for name, d in sets.items():
    for sense in ("max", "min"):
        per = "3" if name in ("e3_57",) else "1"
        cmd = [py, "flag_cut_loop.py", "forms10.npz"] + ([d] if d else []) + ["--obj=" + sense, "--maxit=400", "--per=" + per,
               "--log=cut_%s_%s.log" % (name, sense), "--out=cut_%s_%s.json" % (name, sense)]
        if name != "lp":
            cmd.append("--zero=e3_zero10.txt")
        cuts.append((name, sense, subprocess.Popen(cmd, stdout=open("cutrun_%s_%s.out" % (name, sense), "w"),
                                                  stderr=subprocess.STDOUT, env=env)))
deadline = time.time() + 150 * 60
while any(p.poll() is None for _, _, p in cuts) and time.time() < deadline:
    for name, sense, p in cuts:
        for f in ("cut_%s_%s.log" % (name, sense), "cutrun_%s_%s.out" % (name, sense)):
            if os.path.exists(f):
                up(f, f)
    state["cuts_running"] = sum(p.poll() is None for _, _, p in cuts)
    time.sleep(120)
for name, sense, p in cuts:
    if p.poll() is None:
        p.terminate()
    for f in ("cut_%s_%s.log" % (name, sense), "cutrun_%s_%s.out" % (name, sense), "cut_%s_%s.json" % (name, sense)):
        if os.path.exists(f):
            up(f, f)
state["phase"] = "done"
put("status.json", state)
