import sys, os, json, itertools, collections, time
sys.path.insert(0, r"C:\Users\RESEARCHER\Downloads\conway_c2_researcher2_start_2026_09_30\conway_c2_researcher2_start_2026_09_30\work\c2_elegant_2026-10-13\region_pairs")
import numpy as np
from rp_lib import Lattice, OUT
import rp_search as RS
lid = sys.argv[1]; idx = int(sys.argv[2])
lat = Lattice(lid); G = lat.G
scan = json.load(open(os.path.join(OUT, "scan_%s.json" % lid)))
p = [q for q in scan["pairs"] if q["region"]][idx]
inst = RS.build_instance(lat, np.array(p["y1"]), np.array(p["y2"]), p)
adm = inst["adm"]
Q = (np.abs(inst["P11"][adm]) == 1).astype(np.uint8)       # n x s hit matrix
n, s = Q.shape
def gf2_rank_and_span(M, target):
    # gaussian elimination over GF(2) on rows (as python ints)
    rows = [int("".join(map(str, r[::-1])), 2) for r in M]
    basis = {}
    for r in rows:
        while r:
            hb = r.bit_length() - 1
            if hb in basis: r ^= basis[hb]
            else: basis[hb] = r; break
    t = int("".join(map(str, target[::-1])), 2)
    while t:
        hb = t.bit_length() - 1
        if hb in basis: t ^= basis[hb]
        else: return len(basis), False
    return len(basis), True
r, inspan = gf2_rank_and_span(Q, np.ones(s, np.uint8))
print("pair row", p["row"], "s", s, "adm", n, "| GF(2) rank of admissible hit vectors:", r, "| all-ones in the span:", inspan)
# integer rank
print("real rank of hit matrix:", np.linalg.matrix_rank(Q.astype(float)))
# distinct hit vectors
U = np.unique(Q, axis=0)
print("distinct hit sets:", len(U), "sizes:", dict(sorted(collections.Counter(U.sum(axis=1).tolist()).items())))
# column weights: are some classes always hit together (twins)?
cols = collections.Counter(map(bytes, (Q.T).tolist()))
print("number of classes with identical hit patterns across all admissible h (twin classes): distinct column patterns =", len(cols), "of", s)
