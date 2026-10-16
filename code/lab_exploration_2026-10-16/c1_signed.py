"""c = 1: ODD-PURE as a top-eigenvalue multiplicity of a signed graph (exploration, LAB 16/10/2026 night).
Odd profiles eta = (g, -g) on Y (eta_{2s} = g_s, eta_{3s} = -g_s).  With h = sqrt2 g, the odd block of F is
    D(h) = h^T [(3I - A_sig/2) - (Bo/sqrt2)^T L^+ (Bo/sqrt2)] h ,
A_sig = signed graph on the 10 outer letters (+M_2, +M_3, -sigma_m, diagonal -2 for {2s}~{3s}),
Bo = 36 x 10 odd injection (hub 2: +1, hub 3: -1, letters: 0, label u: C_us = [u~2s] - [u~3s]).
Hence with the signed graph  SG = [[A_G, Bo/sqrt2], [Bo^T/sqrt2, A_sig/2]] (46 vertices):
    F >= 0 on odd vectors  <=>  lambda_max(SG) <= 3,  and  ODD-PURE  <=>  mult of 3 in SG = 2
((1_G, 0) and the constant odd profile).  Interlacing: lambda_3(SG) <= lambda_max(SG - {u, w}), so a pair (u, w) with
lambda_max(SG - {u, w}) < 3 certifies ODD-PURE.  We test u, w = the two hubs, and the best pair.
usage: python c1_signed.py <distinct cache.jsonl> <cle3_sides.jsonl>"""
import itertools, json, sys
import numpy as np
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from c1_network import build


def signed_graph(Gv, Y, AG, B, AY):
    outer = sorted({min(y - {2, 3}) for y in Y})
    iy = {y: i for i, y in enumerate(Y)}
    n2 = lambda s: iy[frozenset((2, s))]
    n3 = lambda s: iy[frozenset((3, s))]
    Bo = np.zeros((36, 10))
    for j, s in enumerate(outer):
        Bo[:, j] = B[:, n2(s)] - B[:, n3(s)]
    Asig = np.zeros((10, 10))
    for j, s in enumerate(outer):
        for k, t in enumerate(outer):
            # eta^T A_YY eta = g^T Asig g  with eta_2s = g_s, eta_3s = -g_s
            Asig[j, k] = AY[n2(s), n2(t)] + AY[n3(s), n3(t)] - AY[n2(s), n3(t)] - AY[n3(s), n2(t)]
    SG = np.block([[AG, Bo / np.sqrt(2)], [Bo.T / np.sqrt(2), Asig / 2]])
    return SG, Bo, Asig, outer


if __name__ == "__main__":
    want = {json.loads(x)["src"] for x in open(sys.argv[2]) if json.loads(x)["c"] == 1}
    rows = []
    for line in open(sys.argv[1]):
        d = json.loads(line)
        if d["src"] not in want:
            continue
        L = [frozenset(x) for x in d["labels"]]
        E = set(frozenset((frozenset(a), frozenset(b))) for a, b in d["edges"])
        S, Gv, Y, AG, B, AY = build(L, E)
        if np.sum(np.linalg.eigvalsh(3 * np.eye(36) - AG) < 1e-9) != 1:
            continue
        SG, Bo, Asig, outer = signed_graph(Gv, Y, AG, B, AY)
        ev = np.linalg.eigvalsh(SG)
        lmax = ev[-1]
        mult3 = int(np.sum(np.abs(ev - 3) < 1e-7))
        hubs = [Gv.index(("L", 2)), Gv.index(("L", 3))]
        keep = [i for i in range(46) if i not in hubs]
        lh = np.linalg.eigvalsh(SG[np.ix_(keep, keep)])[-1]
        best = 99
        for u, w in itertools.combinations(range(46), 2):
            kk = [i for i in range(46) if i not in (u, w)]
            best = min(best, np.linalg.eigvalsh(SG[np.ix_(kk, kk)])[-1])
            if best < 2.9:
                break
        rows.append((lmax, mult3, ev[-3], lh, best, d["src"]))
    print("c = 1 sides:", len(rows))
    print("max lambda_max(SG) = %.9f ; mult of 3 in SG: %s" % (max(r[0] for r in rows), sorted({r[1] for r in rows})))
    print("lambda_3(SG): max %.6f" % max(r[2] for r in rows))
    print("lambda_max(SG - hubs): min %.4f  max %.4f   (< 3 certifies ODD-PURE)" % (min(r[3] for r in rows), max(r[3] for r in rows)))
    print("best pair (first found < 2.9 or overall min): max over sides %.4f" % max(r[4] for r in rows))
    rows.sort(key=lambda r: -r[2])
    for r in rows[:6]:
        print("  lambda_3 %.6f  lambda_max(SG-hubs) %.4f  best pair %.4f  %s" % (r[2], r[3], r[4], r[5]))
