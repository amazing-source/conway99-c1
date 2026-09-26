"""Export anchored motif survivors to C2's ptype format for orbit_colmodel_U:
[{"tag": ..., "ptype": {"a,b": ["sib"] | ["anch", c]}}] with 0-based blocks (C2's convention 0..6), a < b.
An orientation (motiflib.survivors_full order) is listed if some D-graph choice passing the tail rule and T+ is feasible
in the sib pair model (ad/sib_model.py).  Usage: python export_ptype.py <motif> <idx,idx,...|all> <out.json>"""
import sys, json, itertools
sys.path.insert(0, r"C:/home/researcher/Desktop/c99_structures_lab/ad")
from motiflib import MOTIFS, B, survivors_full

name = sys.argv[1]
sig = MOTIFS[name]
Sset = set(frozenset(p) for p in sig)
res = survivors_full(name, sig)
idx = range(len(res)) if sys.argv[2] == 'all' else [int(t) for t in sys.argv[2].split(',')]
out = []
for n in idx:
    arc, indeg, o, In = res[n]
    pt = {}
    for a, b in itertools.combinations(B, 2):
        key = '%d,%d' % (a - 1, b - 1)
        if frozenset((a, b)) in Sset:
            pt[key] = ['sib']
        else:
            head = b if (a, b) in arc else a          # arc tail -> head : pair anchored at head
            assert (a, b) in arc or (b, a) in arc
            pt[key] = ['anch', head - 1]
    out.append({'tag': 'C1_anch_%s_or%d' % (name, n), 'motif_0based': [[a - 1, b - 1] for a, b in sig],
                'In_0based': {str(k - 1): sorted(m - 1 for m in v) for k, v in In.items()}, 'ptype': pt})
json.dump(out, open(sys.argv[3], 'w'), indent=None)
print(name, len(out), 'orientations written to', sys.argv[3])
