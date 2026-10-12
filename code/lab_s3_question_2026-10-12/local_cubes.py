"""Lab session, 2026-10-12. Local problem at P = 0 (local_vertex.py), cube by cube: the far vertex far[r0] is split with a
given partition (one of the ten masks on its labels); all solutions in the cube are enumerated with cadical and blocking
clauses, each call with a time limit.
python local_cubes.py <tmp dir> <r0> <seconds per call> [first mask index] [last mask index]"""
import sys, os, subprocess, itertools, time, importlib.util
tmp, r0, tl = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
lo = int(sys.argv[4]) if len(sys.argv) > 4 else 0; hi = int(sys.argv[5]) if len(sys.argv) > 5 else 9
spec = importlib.util.spec_from_file_location("lv", os.path.join(os.path.dirname(os.path.abspath(__file__)), "local_vertex.py"))
lv = importlib.util.module_from_spec(spec); keep = sys.argv; sys.argv = ["x"]; spec.loader.exec_module(lv); sys.argv = keep
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
Bf = lambda x, y: (2 * x[0] * y[0] + 2 * x[1] * y[1] + x[2] * y[3] + x[3] * y[2]) % 3
iso = []
for z in lv.NP:
    if lv.I[tuple((-c) % 3 for c in lv.V[z])] not in iso: iso.append(z)
base = lv.build("free"); R = lv.far[r0]; labs = lv.C[R][1:]
masks = [c for c in itertools.combinations(range(5), 3)]
path = os.path.join(tmp, "cube_%d.cnf" % r0)
for mi in range(lo, hi + 1):
    cl = list(base) + [[lv.var[(labs[i], R)] if i in masks[mi] else -lv.var[(labs[i], R)]] for i in range(5)]
    nsol = 0; kinds = []; t0 = time.time(); status = "complete"
    while True:
        with open(path, "w", newline="\n") as f:
            f.write("p cnf %d %d\n" % (lv.nv, len(cl)))
            for c in cl: f.write(" ".join(map(str, c)) + " 0\n")
        try:
            out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
        except subprocess.TimeoutExpired:
            status = "TIMEOUT (no decision)"; break
        if "s UNSATISFIABLE" in out: break
        assert "s SATISFIABLE" in out
        model = set(int(t) for line in out.split("\n") if line.startswith("v ") for t in line[2:].split() if int(t) > 0)
        nsol += 1
        split = [r for r in lv.far if any(lv.var[(z, r)] in model for z in lv.C[r][1:])]
        kind = "OTHER (%d split)" % len(split)
        for d in iso:
            if sorted(split) == sorted(r for r in lv.far if Bf(lv.V[r], lv.V[d]) == 0):
                ok = all(len({(Bf(lv.V[z], lv.V[d]) + (lv.var.get((z, r), 0) in model)) % 2 for z in lv.C[r]}) == 1 for r in split)
                kind = "line %s%s" % (lv.V[d], "" if ok else " BUT other partitions")
        kinds.append(kind)
        cl.append([(-v if (v in model) else v) for v in range(1, 301)])
    print("far vertex %s, partition %s: %d solution(s) %s; %s; %.1f s" % (lv.V[R], masks[mi], nsol, kinds, status, time.time() - t0), flush=True)
