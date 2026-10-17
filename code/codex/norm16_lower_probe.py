"""Bounded exploration of the unused lower spectral bound on saved bases.

Numerical results are a probe only; no exclusion is certified here.
"""
import json
from pathlib import Path
import numpy as np
import sympy as sp
from norm16_schur_data import ROOT, source_data


def lower_data(case, orbit):
    cores, cases, _ = source_data()
    b = sp.Matrix(cores[case]['representatives'][0])
    ac = sp.zeros(16)
    ac[:8, 8:] = b
    ac[8:, :8] = b.T
    f = sp.Matrix([1]*8+[-1]*8)
    proj = f*f.T/16
    m = 4*sp.eye(16)+ac-2*sp.ones(16)/11
    inverse = (m+proj).inv()-proj
    v = sp.zeros(16, 8)
    for d, r in enumerate(cases[case]['orbits'][orbit]['representative']):
        for i in r[:2]+[8+q for q in r[2:]]:
            v[i, d] = 1
    cd = v-2*sp.ones(16, 8)/11
    h = 4*sp.eye(8)-2*sp.ones(8)/11-cd.T*inverse*cd
    return h


if __name__ == '__main__':
    h = np.array(lower_data(4, 1), float)
    qinv = {f['id']: np.linalg.inv(4*np.eye(11)+np.array(f['adjacency_Z'])-2*np.ones((11, 11))/7)/49 for f in source_data()[2]}
    counts = {}
    for line in (ROOT/'data/codex_norm16_even_core_full/supports.jsonl').read_text().splitlines():
        item = json.loads(line)
        fid = item['forest']
        x = np.array([[(m >> j) & 1 for j in range(11)] for m in item['D_Z_row_masks']])
        k = 7*x-1
        eigen = np.linalg.eigvalsh(h-k@qinv[fid]@k.T)[0]
        row = counts.setdefault(fid, {'negative_below_minus_1e_8': 0, 'other': 0, 'min': 0.0})
        row['negative_below_minus_1e_8' if eigen < -1e-8 else 'other'] += 1
        row['min'] = min(row['min'], float(eigen))
    print(json.dumps(counts))
