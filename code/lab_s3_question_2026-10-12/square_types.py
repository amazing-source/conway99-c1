"""Lab session, 2026-10-12. Local problem at P = 0: an odd grid square through P has a diagonal {P, R} (a block R that
separates one of its grid pairs {a, a'}) and the diagonal {a, a'} (an inner pair separated by its grid block R).
Four cases for the types (block, inner pair): (A, A), (A, B), (B, A), (B, B); each is tested with the state of the block
fixed and the type of the inner pair imposed.
python square_types.py <tmp dir> <seconds per case>"""
import sys, os, subprocess, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import local_cnf2 as L
tmp, tl = sys.argv[1], float(sys.argv[2])
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
nv, base, x, y = L.build([])
R0 = L.far[0]; Cr = L.C[R0]
def run(extra):
    path = os.path.join(tmp, "sqt_%d.cnf" % os.getpid())
    with open(path, "w", newline="\n") as f:
        f.write("p cnf %d %d\n" % (nv, len(base) + len(extra)))
        for c in base + extra: f.write(" ".join(map(str, c)) + " 0\n")
    t0 = time.time()
    try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
    except subprocess.TimeoutExpired: out = ""
    return ("UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"), time.time() - t0
for btype in ("A", "B"):
    s0 = [s for s in range(1, 11) if L.state_type(R0, L.MASKS[s]) == btype][0]; m = L.MASKS[s0]
    side = {z: (m >> i) & 1 for i, z in enumerate(Cr)}
    a = next(z for z in Cr if side[z] != side[L.partner[R0][z]]); ap = L.partner[R0][a]        # a separated grid pair of R0
    p = (a, ap) if (a, ap) in y else (ap, a); g, v, w, v2, w2 = y[p]; assert L.pblocks[p][0] == R0
    for ptype, extra in (("A", [[v, w], [-v, -w], [v2, w2], [-v2, -w2]]), ("B", [[-u1, -u2] for u1 in (v, w) for u2 in (v2, w2)])):
        res, t = run([[x[R0][s0]]] + extra)
        print("odd grid square through P: block of type %s, inner pair of type %s: %s (%.1f s)" % (btype, ptype, res, t), flush=True)
