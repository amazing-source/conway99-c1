"""Aggregate the per-part logs of the (4,8) sweep (LAP's sweep48.py run in 12000 parts through guarded_pool.py).
  python aggregate_48.py            -> sweep_48_all.log, counts, lists of TORSION balls and of lines that are not dead
A line is "dead" by the laptop session's own criterion in sweep48.py: it contains "solutions 0 timeout 0 |".
From 01:30 UTC on 09/10 the sweep is restricted to one ball per isomorphism class (reps48.txt, 97 896 balls; the parts
finished before that were swept in full). The report therefore gives the coverage of the representatives, which is
what the statement needs, and separately the other balls that happen to have been swept."""
import glob, collections, os
NL = chr(10)
lines = {}
for f in glob.glob("sweep_48_part*of12000.log"):
    for l in open(f):
        l = l.rstrip(NL)
        if l.startswith("48 "): lines[l.split("|")[0].strip()] = l
keys = sorted(lines, key=lambda k: (int(k.split()[1]), int(k.split()[2])))
reps = {"48 %s %s" % tuple(l.split()[:2]) for l in open("reps48.txt") if l.strip()} if os.path.exists("reps48.txt") else None
kind = collections.Counter(); rkind = collections.Counter(); tors = []; bad = []
for k in keys:
    l = lines[k]; v = "torsion" if "TORSION" in l else "dead" if "solutions 0 timeout 0 |" in l else "other"
    kind[v] += 1
    if reps is not None and k in reps: rkind[v] += 1
    if v == "torsion": tors.append(k)
    if v == "other": bad.append(l)
open("sweep_48_all.log", "w", newline=NL).write(NL.join(lines[k] for k in keys) + NL)
open("sweep_48_torsion.txt", "w", newline=NL).write(NL.join(tors) + NL)
open("sweep_48_not_dead.txt", "w", newline=NL).write(NL.join(bad) + (NL if bad else ""))
print("balls logged %d of 245877: dead %d, torsion %d, other %d" % (len(keys), kind["dead"], kind["torsion"], kind["other"]))
if reps is not None:
    got = sum(rkind.values()); missing = sorted(reps - set(keys), key=lambda k: (int(k.split()[1]), int(k.split()[2])))
    print("representatives (one ball per isomorphism class) logged %d of %d: dead %d, torsion %d, other %d; missing %d" % (got, len(reps), rkind["dead"], rkind["torsion"], rkind["other"], len(missing)))
    open("sweep_48_missing_reps.txt", "w", newline=NL).write(NL.join(missing) + (NL if missing else ""))
for l in bad[:10]: print("  OTHER:", l[:300])
