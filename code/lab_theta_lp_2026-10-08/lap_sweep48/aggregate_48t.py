"""Aggregate the per-part logs of the torsion follow-up of the (4,8) sweep (the laptop session's sweep48t.py run through
guarded_pool.py: rank 1 in 2000 parts, rank 2 in 400, rank 3 in 144).
  python aggregate_48t.py      -> sweep_48t_all.log, sweep_48t_not_dead.txt, counts by torsion rank and verdict
Verdicts are the laptop session's: DEAD (every sub-case dead), COMB-ALIVE, ALIVE, ERROR."""
import glob, collections, json, re
NL = chr(10)
lines = {}
for f in glob.glob("sweep_48t_part*of*.log"):
    for l in open(f):
        l = l.rstrip(NL)
        if l.startswith("48t "): lines[l.split("|")[0].strip()] = l
keys = sorted(lines, key=lambda k: (int(k.split()[1]), int(k.split()[2])))
rank = dict((b, t) for b, t in json.load(open("tors_m4.json"))); expected = collections.Counter(rank.values())
kind = collections.Counter(); bad = []
for k in keys:
    l = lines[k]; t = rank[int(k.split()[2])]; m = re.search(r" (DEAD|COMB-ALIVE|ALIVE) ", l)
    v = m.group(1) if m else "ERROR"; kind[(t, v)] += 1
    if v != "DEAD": bad.append(l)
open("sweep_48t_all.log", "w", newline=NL).write(NL.join(lines[k] for k in keys) + NL)
open("sweep_48t_not_dead.txt", "w", newline=NL).write(NL.join(bad) + (NL if bad else ""))
for t in sorted(expected):
    got = {v: c for (t2, v), c in kind.items() if t2 == t}
    print("torsion rank %d: %d balls expected (3 x %d types), logged %d: %s" % (t, 3 * expected[t], expected[t], sum(got.values()), dict(sorted(got.items())) or "-"))
print("balls logged %d; not DEAD %d" % (len(keys), len(bad)))
for l in bad[:10]: print("  NOT DEAD:", l[:300])
