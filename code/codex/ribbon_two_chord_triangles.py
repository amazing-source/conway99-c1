"""Pilot: jointly realize the forced triangles of two disjoint ribbon chords.

This adds a two-outside-vertex condition to the known one-vertex relaxation.
No full SRG completion or exhaustive two-chord claim is made by this pilot.
"""
import json
from itertools import combinations
from pathlib import Path

import numpy as np
import sympy as sp

from ribbon_six_star import ribbon
from ribbon_window_obstructions import exterior_model, local_ok
from twisted_prism_extension import spectral_masks, projectors


def schur_pair_data(a, masks):
    data = []
    for gram, diagonal, constant, coefficient in projectors(a, 14):
        g = sp.Matrix(gram.tolist())
        pivots = list(g.rref()[1])
        inv = g.extract(pivots, pivots).inv()
        den = int(sp.ilcm(*[x.q for x in inv]))
        num = np.array((den*inv).tolist(), dtype=object)
        cross = (constant+coefficient*masks[:, pivots]).astype(object)
        inner = cross@num@cross.T
        slack = diagonal*den-np.diag(inner)
        data.append((den, constant, coefficient, inner, slack))
    return data


def pair_passes(data, i, j, edge):
    return all((den*(const+coeff*edge)-inner[i, j])**2 <= slack[i]*slack[j]
               for den, const, coeff, inner, slack in data)


def run(twist, chords):
    a = np.array(ribbon(twist), dtype=np.int64)
    for u, v in chords:
        a[u, v] = a[v, u] = 1
    assert local_ok(a)
    rows, _, _ = exterior_model(a)
    masks = rows[1:19].T
    before = len(masks)
    masks = spectral_masks(a, masks, 14)
    options = [np.flatnonzero(masks[:, u]*masks[:, v]).tolist() for u, v in chords]
    relevant = sorted(set(options[0]+options[1]))
    selected = masks[relevant]
    lookup = {old: new for new, old in enumerate(relevant)}
    data = schur_pair_data(a, selected)
    same = sorted(set(options[0]) & set(options[1]))
    joint = []
    counts = {"different_local": 0, "different_spectral": 0}
    for i in options[0]:
        for j in options[1]:
            # Each chord has exactly one third vertex. If either mask contains
            # the other chord, the two third vertices must be the same vertex.
            if i in same or j in same:
                continue
            for e in (0, 1):
                b = np.zeros((20, 20), dtype=np.int64)
                b[:18, :18] = a
                b[18, :18] = b[:18, 18] = masks[i]
                b[19, :18] = b[:18, 19] = masks[j]
                b[18, 19] = b[19, 18] = e
                if not local_ok(b):
                    continue
                counts["different_local"] += 1
                if not pair_passes(data, lookup[i], lookup[j], e):
                    continue
                counts["different_spectral"] += 1
                joint.append({"first_mask": masks[i].tolist(),
                              "second_mask": masks[j].tolist(), "edge": e})
    return {"twist": twist, "chords": chords, "combinatorial_masks": before,
            "spectral_masks": len(masks), "third_vertex_choices": list(map(len, options)),
            "same_third_masks": [masks[i].tolist() for i in same],
            "counts": counts, "different_third_pairs": joint}


def main():
    cases = [[(12, 15), (13, 16)], [(12, 14), (13, 16)],
             [(0, 9), (1, 10)], [(0, 14), (1, 16)]]
    out = Path(__file__).resolve().parents[2]/"data/codex_ribbon_two_chord_triangles_pilot.json"
    reports = []
    for chords in cases:
        row = run(0, chords)
        reports.append(row)
        print({k: v for k, v in row.items() if k not in ("different_third_pairs", "same_third_masks")}
              | {"same_third_choices": len(row["same_third_masks"])}, flush=True)
        out.write_text(json.dumps(reports, indent=2)+"\n", encoding="utf-8")


if __name__ == "__main__":
    main()
