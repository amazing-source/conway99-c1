"""Aggregate the per-part logs of the (4,8) sweep (LAP's sweep48.py run in 12000 parts through guarded_pool.py).
  python aggregate_48.py            -> sweep_48_all.log, counts, lists of TORSION balls and of lines that are not dead
A line is "dead" by the laptop session's own criterion in sweep48.py: it contains "solutions 0 timeout 0 |"."""
import glob, collections
NL = chr(10)
lines = {}
for f in glob.glob("sweep_48_part*of12000.log"):
    for l in open(f):
        l = l.rstrip(NL)
        if l.startswith("48 "): lines[l.split("|")[0].strip()] = l
keys = sorted(lines, key=lambda k: (int(k.split()[1]), int(k.split()[2])))
kind = collections.Counter(); tors = []; bad = []
for k in keys:
    l = lines[k]
    if "TORSION" in l: kind["torsion"] += 1; tors.append(k)
    elif "solutions 0 timeout 0 |" in l: kind["dead"] += 1
    else: kind["other"] += 1; bad.append(l)
open("sweep_48_all.log", "w", newline=NL).write(NL.join(lines[k] for k in keys) + NL)
open("sweep_48_torsion.txt", "w", newline=NL).write(NL.join(tors) + NL)
open("sweep_48_not_dead.txt", "w", newline=NL).write(NL.join(bad) + (NL if bad else ""))
print("balls logged %d of 245877: dead %d, torsion %d, other %d" % (len(keys), kind["dead"], kind["torsion"], kind["other"]))
for l in bad[:10]: print("  OTHER:", l[:300])
