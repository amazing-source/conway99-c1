"""Lab session, 2026-10-12. Local problem at P = 0 with the block R0 = far[0] in a fixed type B state: exhaustive search
by dynamic cubes on the question "which blocks are of type B".

A cube = a list of decisions (block r is of type B / block r is not of type B). For a cube, cadical is called with a time
limit; UNSAT closes the cube, SAT gives a local solution with a type B block (printed and stored), no decision splits the
cube on the next undecided block (static order: blocks closest to R0 first).
The open cubes are kept in a JSON file, so that the search can be resumed (each run stays under five minutes).

python typeB_cubes.py <state file (json)> <tmp dir> <seconds per call> <seconds for this run> [state index 0..5]
Memory: a few megabytes (cadical on 1560 variables)."""
import sys, os, subprocess, time, json, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import local_cnf2 as L
statefile, tmp, tl, budget = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
which = int(sys.argv[5]) if len(sys.argv) > 5 else 0
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
R0 = L.far[0]; sB = [s for s in range(1, 11) if L.state_type(R0, L.MASKS[s]) == "B"][which]
m0 = L.MASKS[sB]; Cr = L.C[R0]; side = {z: (m0 >> i) & 1 for i, z in enumerate(Cr)}
nv, base, x, y = L.build([]); base = base + [[x[R0][sB]]]
Bst = {r: [s for s in range(1, 11) if L.state_type(r, L.MASKS[s]) == "B"] for r in L.far}
# static order of the other blocks: number of points shared with Oct(R0), then number of separated non-grid pairs shared
def score(r):
    common = [z for z in L.C[r] if z in Cr]
    sepng = sum(1 for a, b in itertools.combinations(common, 2) if side[a] != side[b] and L.partner[R0][a] != b)
    return (-len(common), -sepng, r)
order = sorted((r for r in L.far if r != R0), key=score)

def solve(cube, limit):
    extra = []
    for r, isB in cube:
        if isB: extra.append([x[r][s] for s in Bst[r]])
        else: extra += [[-x[r][s]] for s in Bst[r]]
    path = os.path.join(tmp, "tbc_%d.cnf" % os.getpid())
    with open(path, "w", newline="\n") as f:
        f.write("p cnf %d %d\n" % (nv, len(base) + len(extra)))
        for c in base + extra: f.write(" ".join(map(str, c)) + " 0\n")
    try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=limit).stdout
    except subprocess.TimeoutExpired: return "?", None
    if "s UNSATISFIABLE" in out: return "UNSAT", None
    if "s SATISFIABLE" in out:
        model = set(int(t) for line in out.split("\n") if line.startswith("v ") for t in line[2:].split() if int(t) > 0)
        return "SAT", {r: [s for s in range(11) if x[r][s] in model][0] for r in L.far}
    return "?", None

if os.path.exists(statefile): st = json.load(open(statefile))
else: st = {"open": [[]], "closed": 0, "calls": 0, "sat": [], "maxdepth": 0, "seconds": 0.0, "state": which}
assert st["state"] == which
t0 = time.time()
while st["open"] and time.time() - t0 < budget:
    cube = st["open"].pop()                                    # depth first
    res, sol = solve([(r, b) for r, b in cube], tl); st["calls"] += 1
    if res == "UNSAT": st["closed"] += 1
    elif res == "SAT":
        types = {}
        for r in L.far:
            t = L.state_type(r, L.MASKS[sol[r]]); types[t] = types.get(t, 0) + 1
        print("SAT: a local solution with a type B block; block types %s; %s" % (types, L.identify(sol)), flush=True)
        st["sat"].append({"cube": cube, "states": {str(r): sol[r] for r in L.far}})
        st["closed"] += 1                                      # the cube is not explored further (one solution recorded)
    else:
        decided = {r for r, b in cube}
        nxt = next((r for r in order if r not in decided), None)
        if nxt is None:
            print("UNDECIDED LEAF (all blocks decided, no decision in %.0f s): %s" % (tl, cube), flush=True)
            st.setdefault("hard", []).append(cube)
        else:
            st["open"].append(cube + [[nxt, False]]); st["open"].append(cube + [[nxt, True]])
            st["maxdepth"] = max(st["maxdepth"], len(cube) + 1)
st["seconds"] += time.time() - t0
json.dump(st, open(statefile, "w"))
print("type B state %d of R0 = %s: calls %d, closed cubes %d, open cubes %d, max depth %d, solutions found %d, hard leaves %d, total %.0f s%s"
      % (which, L.V[R0], st["calls"], st["closed"], len(st["open"]), st["maxdepth"], len(st["sat"]), len(st.get("hard", [])), st["seconds"],
         "" if st["open"] else "  -- SEARCH COMPLETE"), flush=True)
if st["open"]:
    depths = sorted(len(c) for c in st["open"]); print("depths of the open cubes: %s" % depths[:40], flush=True)
