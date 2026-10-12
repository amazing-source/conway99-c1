"""Lab session, 2026-10-12. Direct isomorphism tests of the new graph against other graphs, with positive controls.
python -I iso_check.py <directory of aut_tools.py> <new graph> <other edge files ...>"""
import sys, time
sys.path.insert(0, sys.argv[1])
import aut_tools as T
new = T.load(sys.argv[2])
for p in sys.argv[3:]:
    t0 = time.time(); f = T.find_iso(new, T.load(p)); print("new graph isomorphic to %s: %s (%.1f s)" % (p.split("/")[-1], f is not None, time.time() - t0), flush=True)
t0 = time.time(); f = T.find_iso(new, new); print("control, new graph isomorphic to itself: %s" % (f is not None))
import random, numpy as np
perm = list(range(243)); random.Random(5).shuffle(perm); B = new[np.ix_(perm, perm)]
f = T.find_iso(new, B); print("control, new graph isomorphic to a random relabelling of itself: %s" % (f is not None))
