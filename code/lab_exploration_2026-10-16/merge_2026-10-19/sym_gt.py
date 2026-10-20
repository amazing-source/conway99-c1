"""The most symmetric line graphs: G_T on which a group H of order 12 acts regularly on each class (LAB 20/10/2026).

H must contain a central involution z (the partner of (c, h) is (c, h z)).  Groups of order 12 with a central
involution: Z12, Z6 x Z2 (three choices of z), D12 (dihedral, z = r^3), Dic3 (dicyclic, z = a^3).  Cross edges
(0,h)-(1,ha), (1,h)-(2,hb), (2,h)-(0,hc).  Relabelling classes 1 and 2 by right multiplication gives s01 = s12 = id and
s20 = right multiplication by t = abc, so the graph depends only on t, up to automorphisms of H fixing z (P, short
computation in the note).  For each H and t: c(G_T), d, K >= 0, (tau | 7); connected generic lines with (tau|7) = -1
(possible at rank 37 by L23) are run through oblr2 at rank 37; c = 2 lines (d = 2) through the rank-1 residual.
Runs at IDLE priority.  usage: python sym_gt.py <engine seconds> <out.jsonl>"""
import ctypes
import itertools
import json
import os
import subprocess
import sys
import tempfile

import numpy as np

if sys.platform == "win32":
    ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x40)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from oblr_prep import P7, build  # noqa: E402
from ll_test import components, gt_matrix, k_matrix  # noqa: E402
from rank7_line import rank_mod  # noqa: E402
from adversarial import det_mod  # noqa: E402


def groups():
    """(name, elements, mul, z) for the groups of order 12 with a central involution"""
    out = []
    Z12 = list(range(12))
    out.append(("Z12", Z12, lambda x, y: (x + y) % 12, 6))
    Z62 = [(a, b) for a in range(6) for b in range(2)]
    for zz in ((3, 0), (0, 1), (3, 1)):
        out.append(("Z6xZ2 z=%s" % (zz,), Z62, lambda x, y: ((x[0] + y[0]) % 6, (x[1] + y[1]) % 2), zz))
    # dihedral D12 = <r, s | r^6 = s^2 = 1, s r s = r^-1>, elements (k, e) = r^k s^e
    D = [(k, e) for k in range(6) for e in range(2)]

    def dmul(x, y):
        k1, e1 = x
        k2, e2 = y
        return ((k1 + (k2 if e1 == 0 else -k2)) % 6, (e1 + e2) % 2)
    out.append(("D12", D, dmul, (3, 0)))
    # dicyclic Dic3 = <a, x | a^6 = 1, x^2 = a^3, x a x^-1 = a^-1>, elements (k, e) = a^k x^e
    Q = [(k, e) for k in range(6) for e in range(2)]

    def qmul(x, y):
        k1, e1 = x
        k2, e2 = y
        if e1 == 0:
            return ((k1 + k2) % 6, e2)
        # a^k1 x a^k2 x^e2 = a^(k1 - k2) x^(1 + e2), and x^2 = a^3
        k = (k1 - k2) % 6
        if e2 == 0:
            return (k, 1)
        return ((k + 3) % 6, 0)
    out.append(("Dic3", Q, qmul, (3, 0)))
    return out


def line_graph(H, mul, z, t):
    """s01 = s12 = id, s20 = right multiplication by t, in the index convention partner(i) = i ^ 1"""
    reps, seen = [], set()
    for h in H:
        if h not in seen:
            reps.append(h)
            seen.add(h)
            seen.add(mul(h, z))
    idx = {}
    for j, r in enumerate(reps):
        idx[r] = 2 * j
        idx[mul(r, z)] = 2 * j + 1
    elem = {v: k for k, v in idx.items()}
    ident = list(range(12))
    s20 = [idx[mul(elem[i], t)] for i in range(12)]
    return ident, ident[:], s20


def main():
    sec, out = sys.argv[1], sys.argv[2]
    tmp = tempfile.mkdtemp(prefix="sym_")
    for name, H, mul, z in groups():
        assert all(mul(z, h) == mul(h, z) for h in H) and mul(z, z) == H[0]
        for t in H:
            s01, s12, s20 = line_graph(H, mul, z, t)
            G = gt_matrix(12, s01, s12, s20)
            rec = {"group": name, "t": t}
            if (k_matrix(12, G) < 0).any():
                rec["skip"] = "K < 0"
            else:
                nc, comp = components(G)
                L = (3 * np.eye(36, dtype=np.int64) - G) % P7
                d = 36 - rank_mod(L, P7)
                rec.update(c=nc, d=d)
                if nc == 1 and d == 1:
                    tm = det_mod(L[1:, 1:], P7)
                    rec["tau_legendre"] = 1 if pow(tm, 3, P7) == 1 else -1
                    if rec["tau_legendre"] == -1:
                        f = os.path.join(tmp, "s.bin")
                        build("c1", s01, s12, s20, G, nc, comp, d, 0, 1, f)
                        r = subprocess.run([os.path.join(HERE, "oblr2.exe"), f, sec], capture_output=True, text=True)
                        rec["rank37"] = json.loads(r.stdout.strip().splitlines()[-1])
                    else:
                        rec["rank37"] = "excluded by L23"
                elif nc == 2 and d == 2:
                    sizes = sorted(np.bincount(comp).tolist())
                    rec["sizes"] = sizes
                    for delta in (1, 3):
                        f = os.path.join(tmp, "s.bin")
                        build("blocks:x", s01, s12, s20, G, nc, comp, d, 1, delta, f)
                        r = subprocess.run([os.path.join(HERE, "oblr2.exe"), f, sec], capture_output=True, text=True)
                        rec["rank37_delta%d" % delta] = json.loads(r.stdout.strip().splitlines()[-1])
                else:
                    rec["note"] = "not tested (c >= 3 goes to the c3 ledger, or extra 7-torsion)"
            with open(out, "a") as g:
                g.write(json.dumps(rec, default=str) + "\n")
            print(json.dumps(rec, default=str)[:300], flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
