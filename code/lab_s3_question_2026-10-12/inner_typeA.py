"""Lab session, 2026-10-12. Local problem at P = 0: can an INNER pair be of type A?
(In the trivial solution and in the ten line solutions no inner pair is of type A.)
The first inner pair p0 = {a, b} is prescribed to be split with separators: its grid block, the block v or w of its first
grid pair of blocks, the block v2 or w2 of the second one (four cases).
python inner_typeA.py <tmp dir> <seconds per case> [extra options of local_cnf2, e.g. noB]"""
import sys, os, subprocess, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import local_cnf2 as L
tmp, tl = sys.argv[1], float(sys.argv[2]); opts = sys.argv[3:]
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
nv, base, x, y = L.build(opts)
p0 = L.pairs[0]; g, v, w, v2, w2 = y[p0]
print("inner pair %s %s; options %s" % (L.V[p0[0]], L.V[p0[1]], opts))
for c1 in (0, 1):
    for c2 in (0, 1):
        extra = [[g], [v if c1 == 0 else -v], [w if c1 == 1 else -w], [v2 if c2 == 0 else -v2], [w2 if c2 == 1 else -w2]]
        path = os.path.join(tmp, "ita_%d.cnf" % os.getpid())
        with open(path, "w", newline="\n") as f:
            f.write("p cnf %d %d\n" % (nv, len(base) + len(extra)))
            for c in base + extra: f.write(" ".join(map(str, c)) + " 0\n")
        t0 = time.time()
        try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
        except subprocess.TimeoutExpired: out = ""
        res = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"
        print("  type A with separators (grid block, block %d of the first pair, block %d of the second): %s (%.1f s)" % (c1, c2, res, time.time() - t0), flush=True)
        if res == "SAT":
            model = set(int(t) for line in out.split("\n") if line.startswith("v ") for t in line[2:].split() if int(t) > 0)
            st = {r: [s for s in range(11) if x[r][s] in model][0] for r in L.far}
            types = {t: sum(1 for r in L.far if L.state_type(r, L.MASKS[st[r]]) == t) for t in ("flat", "A", "B")}
            print("    block types %s; states %s" % (types, [st[r] for r in L.far]), flush=True)
