"""Census type ids forced to N_H = 0 by the E3 lemma (LAB 19/10/2026; lemma: archive, Codex; used in p852_recheck.py).
E3 configuration: a vertex v, its lines {v,a,a'}, {v,b,b'}, the four common neighbours w_xy (x in {a,a'}, y in {b,b'},
w_xy != v) with EXACTLY three edges among the w_xy: impossible in a srg(99,14,1,2).  Every admissible 9-vertex graph of
that shape is an E3 type; a type of order 10 with an induced 9-subset of E3 type also has N_H = 0.
usage: python e3_zero_ids.py <census json> <out txt>     (ids in flag_engine.load_types order)"""
import sys, os
from itertools import combinations
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "census2_code"))
import census2 as C2  # noqa: E402
from flag_engine import load_types  # noqa: E402
from flag_sdp import admissible  # noqa: E402
d, tid, forms = load_types(sys.argv[1])
V, A, AS, B, BS = 0, 1, 2, 3, 4
Wm = {(A, B): 5, (A, BS): 6, (AS, B): 7, (AS, BS): 8}
base = [(V, A), (V, AS), (V, B), (V, BS), (A, AS), (B, BS)]
for (x, y), w in Wm.items():
    base += [(x, w), (y, w)]
labels = list(Wm.values())
e3 = set()
for three in combinations(list(combinations(labels, 2)), 3):
    rows = [0] * 9
    for i, j in base + list(three):
        rows[i] |= 1 << j; rows[j] |= 1 << i
    if admissible(9, rows):
        e3.add(C2.canon(9, rows)[0])
zero = [tid[(9, k)] for k in e3 if (9, k) in tid]
maxn = max(int(n) for n in d["types"])
if maxn >= 10:
    for key, rows, aut, form in d["types"]["10"]:
        for drop in range(10):
            keep = [i for i in range(10) if i != drop]
            pos = {v: p for p, v in enumerate(keep)}
            sub = []
            for i in keep:
                r = 0
                for j in keep:
                    if rows[i] >> j & 1:
                        r |= 1 << pos[j]
                sub.append(r)
            if C2.canon(9, sub)[0] in e3:
                zero.append(tid[(10, key)]); break
open(sys.argv[2], "w").write("\n".join(map(str, sorted(set(zero)))) + "\n")
print("E3 types of order 9: %d; ids forced to zero: %d" % (len(e3), len(set(zero))))
