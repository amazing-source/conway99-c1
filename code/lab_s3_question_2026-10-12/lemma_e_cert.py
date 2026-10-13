"""Lab session, 2026-10-13. Certificate for lemma (e) of full_ultimate.py (C5): in the local problem at P = 0 with the
block R0 in its first type B state, type B cannot be confined to the 25 blocks of Omega(R0). Same instance as
explore_typeB4.py; here the CNF is kept as lemma_e.cnf, cadical writes its DRAT proof lemma_e.drat, and drat-trim
checks it.   python lemma_e_cert.py <tmp dir> <seconds>"""
import sys, os, subprocess, time, itertools, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import local_cnf2 as L
tmp, tl = sys.argv[1], float(sys.argv[2])
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
DRATTRIM = os.environ.get("DRATTRIM", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/drat-trim.exe")
R0 = L.far[0]; sB = [s for s in range(1, 11) if L.state_type(R0, L.MASKS[s]) == "B"][0]
m = L.MASKS[sB]; Cr = L.C[R0]; side = {z: (m >> i) & 1 for i, z in enumerate(Cr)}
nv, base, x, y = L.build([]); base = base + [[x[R0][sB]]]
omega = {r for r in L.far if len(set(L.C[r]) & set(Cr)) >= 3}
for a, b in itertools.combinations(Cr, 2):
    if side[a] != side[b] and L.partner[R0][a] != b: omega |= {r for r in L.far if a in L.C[r] and b in L.C[r]}
assert len(omega) == 25
extra = [[-x[r][s]] for r in L.far if r not in omega for s in range(1, 11) if L.state_type(r, L.MASKS[s]) == "B"]
path = os.path.join(tmp, "lemma_e.cnf"); proof = os.path.join(tmp, "lemma_e.drat")
with open(path, "w", newline="\n") as f:
    f.write("p cnf %d %d\n" % (nv, len(base) + len(extra)))
    for c in base + extra: f.write(" ".join(map(str, c)) + " 0\n")
t0 = time.time()
try: out = subprocess.run([CAD, "-q", path, proof], capture_output=True, text=True, timeout=tl).stdout
except subprocess.TimeoutExpired: out = ""
res = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"
print("lemma (e): type B confined to the 25 blocks of Omega(R0): %s (%.1f s)" % (res, time.time() - t0), flush=True)
if res == "UNSAT":
    t1 = time.time()
    try: chk = subprocess.run([DRATTRIM, path, proof], capture_output=True, text=True, timeout=10 * tl + 600).stdout
    except subprocess.TimeoutExpired: chk = "checker timeout"
    verdict = "VERIFIED" if "s VERIFIED" in chk else "NOT VERIFIED: " + chk[-300:]
    print("   certificate: lemma_e.drat (%d bytes), drat-trim: %s (%.1f s); sha256 of the CNF %s" % (os.path.getsize(proof), verdict, time.time() - t1, hashlib.sha256(open(path, "rb").read()).hexdigest()[:16]), flush=True)
