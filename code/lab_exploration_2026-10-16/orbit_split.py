"""Orbit-reduced splitting of a template census (LAB, 18/10/2026).

For a graph J (one of a program's representatives) let r0, r1 be the first two roots of the program's DFS order.
Every template is Aut(J)-equivalent to one whose option at r0 is the smallest-index representative of its orbit under
H0 = Stab_Aut(J)(r0); and, the option a at r0 being fixed, to one whose option at r1 is a representative of its orbit
under K = {h in H0 : h(option a) = option a, h(r1) = r1}.  Proof: an automorphism of J maps templates to templates and
preserves every filter (all are defined from J and the partitions), and h in H0 (resp. K) keeps r0 (resp. r0, the
option a and r1) in place.  Since the census is only needed up to Aut(J), it suffices to run the pairs (a, b) of
representatives; the comparator deduplicates up to S7.
usage: python orbit_split.py <program: std|la> <c_min> <k> <exe> -> prints one line "g a b" per sub-job"""
import json
import subprocess
import sys
from itertools import combinations, permutations

prog, cmin, k, exe = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
exact = sys.argv[5] if len(sys.argv) > 5 else "1"
EDGES = list(combinations(range(7), 2))
args = [exe, str(cmin), exact, str(k), "--print-opts"]
out = subprocess.run(args, capture_output=True, text=True, timeout=600).stdout
for line in out.splitlines():
    if not line.startswith("{"):
        continue
    d = json.loads(line)
    if "mask" not in d:
        continue
    mask, order = d["mask"], d["order"]
    adj = {e for kk, e in enumerate(EDGES) if mask >> kk & 1}
    auts = [p for p in permutations(range(7)) if all(tuple(sorted((p[a], p[b]))) in adj for a, b in adj)]
    r0, r1 = order[0], order[1]
    opts0 = [frozenset(frozenset(B) for B in o) for o in d["opts0"]]
    opts1 = [frozenset(frozenset(B) for B in o) for o in d["opts1"]]
    idx0 = {o: i for i, o in enumerate(opts0)}
    idx1 = {o: i for i, o in enumerate(opts1)}
    assert len(idx0) == len(opts0) and len(idx1) == len(opts1)

    def img(h, o):
        return frozenset(frozenset(h[j] for j in B) for B in o)
    H0 = [h for h in auts if h[r0] == r0]
    reps0 = sorted({min(idx0[img(h, o)] for h in H0) for o in opts0})
    for a in reps0:
        K = [h for h in H0 if img(h, opts0[a]) == opts0[a] and h[r1] == r1]
        reps1 = sorted({min(idx1[img(h, o)] for h in K) for o in opts1})
        for b in reps1:
            print(d["graph"], a, b)
