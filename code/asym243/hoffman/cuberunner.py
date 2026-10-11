"""Resumable cube-and-conquer for the Conway-99 sub-case alpha = 22 (note 171 sec. 5).

Nothing is lost when a solver or the container dies: every cube's verdict is appended to a ledger (JSONL) as soon as
it is known, and the runner restarts from the ledger.  A cube that times out is SPLIT (one more block through point 0
is fixed, all sound children are added), so the work already done is never redone at the same granularity.

Model: alpha99.cnf = srg(99,14,1,2) with coclique 0..21, N(0) = 22..35 with mate pairs (22,23),(24,25),...,
blocks 22 = {0,1,2,3}, 23 = {0,4,5,6} fixed (alpha_cnf.py + alpha99.units).  A cube fixes the point sets ("triples"
besides 0) of further blocks 24, 25, ... .  Children of a cube: all triples for the next block that respect
  - every point lies in exactly 2 blocks through 0 (so at most 2 so far),
  - mates are disjoint, two blocks through 0 share at most one point besides 0,
  - symmetry: points with the same signature (set of fixed blocks containing them) are interchangeable, so within a
    signature class only the smallest unused points are taken.  This is exact: swapping two such points preserves
    every fixed unit.
Roots: case A (24 = {0,1,4,7}) and case B (24 = {0,1,7,8}), exhaustive (note 171).

  python3 cuberunner.py DIR init                # create ledger with the two roots
  python3 cuberunner.py DIR work TIMEOUT        # one worker (run several in parallel)
  python3 cuberunner.py DIR status              # summary
"""
import sys, os, json, time, fcntl, pickle, subprocess, itertools, socket, ctypes, signal


def _die_with_parent():
    """kissat is killed if its worker dies (no orphan solvers after a crash)."""
    ctypes.CDLL("libc.so.6").prctl(1, signal.SIGKILL)  # PR_SET_PDEATHSIG

KISSAT = "/tmp/solvers/kissat/build/kissat"
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "alpha99.cnf")
FIXED0 = {22: (1, 2, 3), 23: (4, 5, 6)}
ROOTS = {"A": {24: (1, 4, 7)}, "B": {24: (1, 7, 8)}}
NPTS = 22  # points 0..21, triples on 1..21


def boot_id():
    try: return open("/proc/sys/kernel/random/boot_id").read().strip()
    except OSError: return "?"


def mate(b): return b + 1 if (b - 22) % 2 == 0 else b - 1


class Ledger:
    def __init__(self, d):
        self.d = d; self.path = os.path.join(d, "ledger.jsonl"); self.lock = os.path.join(d, ".lock")

    def append(self, rec):
        rec["t"] = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.lock, "a") as lk:
            fcntl.flock(lk, fcntl.LOCK_EX)
            with open(self.path, "a") as f:
                f.write(json.dumps(rec, sort_keys=True) + "\n"); f.flush(); os.fsync(f.fileno())
            fcntl.flock(lk, fcntl.LOCK_UN)

    def state(self):
        st = {}
        if os.path.exists(self.path):
            for line in open(self.path):
                if line.strip():
                    r = json.loads(line); st.setdefault(r["id"], {}).update(r)
        return st


def children(fixed):
    blocks = dict(FIXED0); blocks.update({int(k): tuple(v) for k, v in fixed.items()})
    nxt = next((b for b in range(24, 36) if b not in blocks), None)
    if nxt is None: return None
    use = {p: sum(p in t for t in blocks.values()) for p in range(1, NPTS)}
    sig = {p: tuple(sorted(b for b, t in blocks.items() if p in t)) for p in range(1, NPTS)}
    m = blocks.get(mate(nxt))
    out = []
    for tri in itertools.combinations(range(1, NPTS), 3):
        if any(use[p] >= 2 for p in tri): continue
        if m is not None and set(tri) & set(m): continue
        if any(len(set(tri) & set(t)) > 1 for t in blocks.values()): continue
        # symmetry: within each signature class, the chosen points are the smallest ones of the class
        ok = True
        for p in tri:
            cls = [q for q in range(1, NPTS) if sig[q] == sig[p]]
            k = sum(1 for q in tri if sig[q] == sig[p])
            if sorted(q for q in tri if sig[q] == sig[p]) != cls[:k]: ok = False; break
        if ok: out.append((nxt, tri))
    return out


def cube_units(fixed, X):
    lits = []
    for b, tri in fixed.items():
        b = int(b)
        for s in range(NPTS):
            v = X[(min(s, b), max(s, b))]
            lits.append(v if (s == 0 or s in tri) else -v)
    return lits


def write_cube_cnf(path, lits):
    with open(BASE) as f:
        header = f.readline().split()
        nv, nc = int(header[2]), int(header[3])
        with open(path, "w") as g:
            g.write(f"p cnf {nv} {nc + len(lits)}\n")
            for line in f: g.write(line)
            for l in lits: g.write(f"{l} 0\n")


def cmd_init(d):
    os.makedirs(os.path.join(d, "logs"), exist_ok=True)
    L = Ledger(d)
    if L.state(): print("ledger exists, nothing to do"); return
    for name, fx in ROOTS.items():   # roots are split immediately (exact cover by their children)
        fixed = {str(k): list(v) for k, v in fx.items()}
        L.append({"id": name, "fixed": fixed, "status": "PENDING"})
        ch = children(fixed)
        for i, (b, tri) in enumerate(ch):
            f2 = dict(fixed); f2[str(b)] = list(tri)
            L.append({"id": f"{name}.{i}", "fixed": f2, "status": "PENDING"})
        L.append({"id": name, "status": "SPLIT", "secs": 0, "children": len(ch)})
    print("initialised", list(ROOTS))


def pick(L, me):
    """claim one pending cube (or one RUNNING cube whose worker is dead), atomically."""
    with open(L.lock, "a") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        st = L.state(); chosen = None
        for cid, r in sorted(st.items(), key=lambda kv: (len(kv[0]), kv[0])):
            s = r["status"]
            if s == "PENDING": chosen = cid; break
            if s == "RUNNING":
                alive = r.get("boot") == boot_id() and os.path.exists(f"/proc/{r.get('pid')}")
                if not alive: chosen = cid; break
        if chosen:
            with open(L.path, "a") as f:
                f.write(json.dumps({"id": chosen, "status": "RUNNING", "pid": os.getpid(), "boot": boot_id(),
                                    "host": socket.gethostname(), "t": time.strftime("%Y-%m-%d %H:%M:%S")},
                                   sort_keys=True) + "\n"); f.flush(); os.fsync(f.fileno())
        fcntl.flock(lk, fcntl.LOCK_UN)
        return chosen, (st[chosen] if chosen else None)


def cmd_work(d, timeout):
    L = Ledger(d); X = pickle.load(open(BASE + ".map", "rb"))
    while True:
        cid, rec = pick(L, os.getpid())
        if cid is None:
            busy = [r for r in L.state().values() if r["status"] == "RUNNING"]
            if not busy: print("no pending cube, nothing running: done"); return
            time.sleep(60); continue
        fixed = rec["fixed"]
        cnf = os.path.join(d, f"cube_{cid}.cnf"); log = os.path.join(d, "logs", f"{cid}.log")
        write_cube_cnf(cnf, cube_units(fixed, X))
        t0 = time.time()
        with open(log, "a") as lf:
            lf.write(f"=== cube {cid} fixed={fixed} start {time.ctime()} pid {os.getpid()}\n"); lf.flush()
            p = subprocess.Popen([KISSAT, "--verbose=1", cnf], stdout=lf, stderr=subprocess.STDOUT, preexec_fn=_die_with_parent)
            try: rc = p.wait(timeout=timeout)
            except subprocess.TimeoutExpired: p.kill(); p.wait(); rc = None
        dt = round(time.time() - t0, 1)
        os.remove(cnf)
        if rc == 20:
            L.append({"id": cid, "status": "UNSAT", "secs": dt})
        elif rc == 10:
            model = os.path.join(d, f"SAT_{cid}.log"); os.replace(log, model)
            L.append({"id": cid, "status": "SAT", "secs": dt, "model": os.path.basename(model)})
            print("!!! SAT on cube", cid, "model in", model)
        elif rc is None:
            ch = children(fixed)
            if not ch:
                L.append({"id": cid, "status": "TIMEOUT_LEAF", "secs": dt})
            else:
                for i, (b, tri) in enumerate(ch):
                    f2 = dict(fixed); f2[str(b)] = list(tri)
                    L.append({"id": f"{cid}.{i}", "fixed": f2, "status": "PENDING"})
                L.append({"id": cid, "status": "SPLIT", "secs": dt, "children": len(ch)})
        else:
            L.append({"id": cid, "status": "ERROR", "rc": rc, "secs": dt})


def cmd_status(d):
    st = Ledger(d).state(); from collections import Counter
    c = Counter(r["status"] for r in st.values())
    done = sum(r.get("secs", 0) for r in st.values() if r["status"] in ("UNSAT", "SPLIT", "SAT"))
    print(dict(c), f"solver-hours banked: {done / 3600:.2f}")
    for cid, r in sorted(st.items()):
        if r["status"] in ("SAT", "ERROR", "RUNNING"): print(" ", cid, r["status"], r.get("t"))


if __name__ == "__main__":
    d, cmd = sys.argv[1], sys.argv[2]
    if cmd == "init": cmd_init(d)
    elif cmd == "work": cmd_work(d, float(sys.argv[3]))
    elif cmd == "status": cmd_status(d)
