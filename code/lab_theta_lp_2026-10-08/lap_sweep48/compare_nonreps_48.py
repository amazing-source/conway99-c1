"""(4,8) sweep, lab PC: the balls swept before the switch to one ball per isomorphism class include many balls that are
not representatives. For each of them whose representative is logged too, compare the two verdicts (dead / torsion /
other). They must agree if the reduction is right (an isomorphism of balls preserves both).
  python compare_nonreps_48.py <folder with act22_c.txt, act48.txt, types_m2.txt>
Reads sweep_48_part*of12000.log in the current folder. One process, a few seconds."""
import sys, os, glob, collections
NL = chr(10); folder = sys.argv[1]
load = lambda p: [list(map(int, l.split())) for l in open(os.path.join(folder, p)) if l.strip()]
a2 = load("act22_c.txt"); a4 = load("act48.txt"); small_all = load("types_m2.txt"); p0 = [i for i, v in enumerate(small_all) if v[12] == 0]
REPS = [0, 1, 3]; stab = {s: [g for g in range(6) if a2[p0[s]][g] == p0[s]] for s in REPS}
verdict = {}
for f in glob.glob("sweep_48_part*of12000.log"):
    for l in open(f):
        l = l.rstrip(NL)
        if not l.startswith("48 "): continue
        k = l.split("|")[0].split(); s, b = int(k[1]), int(k[2])
        verdict[(s, b)] = "torsion" if "TORSION" in l else "dead" if "solutions 0 timeout 0 |" in l else "other"
same = collections.Counter(); diff = []; norep = 0; nonrep = 0
for (s, b), v in verdict.items():
    r = min(a4[b][g] for g in stab[s])
    if r == b: continue
    nonrep += 1
    if (s, r) not in verdict: norep += 1; continue
    if verdict[(s, r)] == v: same[v] += 1
    else: diff.append((s, b, v, r, verdict[(s, r)]))
print("balls logged %d, of which non-representatives %d" % (len(verdict), nonrep))
print("non-representatives whose representative is logged: %d; same verdict %d (dead %d, torsion %d, other %d); different %d; representative not logged %d"
      % (sum(same.values()) + len(diff), sum(same.values()), same["dead"], same["torsion"], same["other"], len(diff), norep))
for d in diff[:10]: print("  DIFFERENT: ball (%d, %d) %s, representative (%d, %d) %s" % (d[0], d[1], d[2], d[0], d[3], d[4]))
