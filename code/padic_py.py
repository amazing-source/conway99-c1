"""Thin Python wrapper around padic.exe (exact local linear algebra over Z_q mod q^E, see padic.c)."""
import os, subprocess, math
import numpy as np

EXE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'padic.exe')


def exponent(q, bits=50):
    return int(bits // math.log2(q))


def _run(mode, q, M, E=None):
    E = E or exponent(q)
    M = np.asarray(M, dtype=object)
    m, n = M.shape
    data = f'{m} {n}\n' + '\n'.join(' '.join(str(int(x)) for x in row) for row in M) + '\n'
    out = subprocess.run([EXE, mode, str(q), str(E)], input=data, capture_output=True, text=True, check=True).stdout
    return out.split('\n'), E


def smith_vals(M, q, E=None):
    lines, E = _run('smith', q, M, E)
    return [int(x) for x in lines[1].split()], E


def kernel(M, q, E=None):
    lines, E = _run('kernel', q, M, E)
    k, n = map(int, lines[0].split())
    return [list(map(int, lines[1 + i].split())) for i in range(k)], E


def gram_vals(B, q, E=None):
    if len(B) == 0:
        return [], E or exponent(q)
    lines, E = _run('gram', q, B, E)
    return [int(x) for x in lines[1].split()], E


def summary(vals, E):
    """{valuation: multiplicity} for 0 < v < E; key 'inf' counts entries >= E (zero mod q^E)."""
    out = {}
    for v in vals:
        if v == 0:
            continue
        key = 'inf' if v >= E else v
        out[key] = out.get(key, 0) + 1
    return dict(sorted(out.items(), key=lambda kv: (kv[0] == 'inf', kv[0] if kv[0] != 'inf' else 0)))
