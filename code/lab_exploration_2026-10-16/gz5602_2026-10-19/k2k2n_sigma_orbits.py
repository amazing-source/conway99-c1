"""Exact reduction of the 2K2N residual (sigma) attachments by boundary stabilisers (LAB 19/10/2026).
The 2K2N model is invariant under G = (core stabiliser, order <= 16) x (relabellings of lines 3..6 preserving
{{3,4},{5,6}} with letter flips, order 128), the group used by py_boundary.py for the canonical covers.  Two residual
attachments (B, sigma) and (B, sigma') of the SAME canonical boundary B are equivalent when some g in Stab_G(B) maps
the known graph of (B, sigma) onto that of (B, sigma'); then one certificate covers both (the image of a refutation is
a refutation).  sigma maps corner c of the first Y-grid (Q34) to corner sigma[c] of the second (Q56).  The induced
action is checked by rebuilding both known graphs with py_extend.materialize and comparing the relabelled adjacency.
usage: python k2k2n_sigma_orbits.py <codex dir> <residual json> <cover dir> <out json>"""
import gzip
import json
import sys
from collections import defaultdict
from itertools import permutations, product

codex, resid_path, cover_dir, out_path = sys.argv[1:5]
sys.argv = ['py_extend.py', codex, '2K2N', 'x', '0', '0']
src = open('py_extend.py', encoding='utf8').read()
exec(compile(src[:src.index("OUT = next((a.split('=', 1)[1]")], 'py_extend.py', 'exec'))
sys.path.insert(0, codex)
from root_component_shared_k3_boundary import core_stabilizers          # noqa: E402

GR = ((0, 1), (2, 3))                                  # local Y roots 0..3 = lines 3..6


def y_group():
    out = []
    for p in permutations(range(4)):
        img = [tuple(sorted((p[a], p[b]))) for a, b in GR]
        if sorted(img) != sorted(GR):
            continue
        for f in product((0, 1), repeat=4):
            m = {}
            for g, (a, b) in enumerate(GR):
                ng = GR.index(tuple(sorted((p[a], p[b]))))
                na, nb = GR[ng]
                for corner in range(4):
                    s, t = divmod(corner, 2)
                    vals = {p[a]: s ^ f[a], p[b]: t ^ f[b]}
                    m[(g, corner)] = (ng, 2 * vals[na] + vals[nb])
            out.append(m)
    return out


YG = y_group()
res = json.load(open(resid_path))
by_b = defaultdict(list)
for r in res:
    by_b[(r['core_index'], r['boundary_index'])].append(r)
covers = {}
classes = []
for (ci, bi), lst in sorted(by_b.items()):
    if ci not in covers:
        covers[ci] = json.load(gzip.open('%s/core_%03d.json.gz' % (cover_dir, ci)))
    cov = covers[ci]
    core = cov['core']
    b = tuple(bytes.fromhex(cov['boundaries_hex'][bi]))
    assert cov['boundaries_hex'][bi] == lst[0]['boundary_hex']
    trs = core_stabilizers(core)
    # core-label permutations: tr maps masks; recover the vertex permutation from singletons
    stab = []
    for tr in trs:
        perm = [tr[1 << v].bit_length() - 1 for v in range(8)]
        for m in YG:
            img = [0] * 8
            for g in range(2):
                for c in range(4):
                    ng, nc = m[(g, c)]
                    img[4 * ng + nc] = tr[b[4 * g + c]]
            if tuple(img) == b:
                stab.append((perm, m))
    sig = [tuple(r['sigma']) for r in lst]
    rows_of = {s: materialize(core, b, (), s) for s in sig}
    parent = {s: s for s in sig}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for perm, m in stab:
        # vertex map on the 16 known labels: core 0..7 by perm, Y corners by m (YOFF = 8)
        vmap = perm + [0] * 8
        for g in range(2):
            for c in range(4):
                ng, nc = m[(g, c)]
                vmap[8 + 4 * g + c] = 8 + 4 * ng + nc
        for s in sig:
            # image of sigma: edge (grid0 c) - (grid1 s[c]) goes to (vmap...) ; rebuild as a sigma on grid0 -> grid1
            img = [None] * 4
            for c in range(4):
                u, v = vmap[8 + c], vmap[12 + s[c]]
                if u > v:
                    u, v = v, u
                img[u - 8] = v - 12
            ts = tuple(img)
            if ts in rows_of:
                # exact check: relabelled known graph of (B, s) equals the known graph of (B, ts)
                ra, rb = rows_of[s], rows_of[ts]
                ok = all(sum(1 << vmap[w] for w in range(16) if (ra[x] >> w) & 1) == rb[vmap[x]] for x in range(16))
                assert ok, (ci, bi, s, ts)
                parent[find(s)] = find(ts)
    groups = defaultdict(list)
    for s in sig:
        groups[find(s)].append(list(s))
    for rep, members in groups.items():
        classes.append({'core_index': ci, 'boundary_index': bi, 'boundary_hex': cov['boundaries_hex'][bi],
                        'stabiliser_order': len(stab), 'representative_sigma': list(rep), 'members': members})
json.dump({'residual_attachments': len(res), 'classes': len(classes), 'items': classes}, open(out_path, 'w'), indent=1)
print(json.dumps({'residual_attachments': len(res), 'boundaries': len(by_b), 'classes': len(classes)}))
