"""Families of local hypotheses at a vertex x of srg(99,14,1,2), as CNF (encoder srg_sat.py, local view of
h12_instance.build). Blocks are numbered 1..7; block k = {2k-1, 2k} (inner vertices 1..14).

A hypothesis is a set of prescribed pairs of the local matchings: "M_a pairs b with b2". When M_a has a prescribed
partner for b, every other pair of M_a through b is false; pairs not touched by a prescription stay free.

  kkN    (N = 2..7): the blocks 1..N are pairwise "grids" at x: for a in block i <= N and j <= N, j != i,
         M_a pairs the two vertices of block j. kk2 = one 3 x 3 grid through x; kk7 = target T1.
  h12    the line {x, 13, 14} has 12 prisms: every M_a, a outside block 7, pairs 13 with 14.
  g6     the line {x, 13, 14} lies in six grids: h12 and M_13, M_14 respect all blocks.

usage: python family.py NAME out.cnf
"""
import sys

import h12_instance as H
import srg_sat as S


def block(a):
    return (a + 1) // 2


def members(k):
    return (2 * k - 1, 2 * k)


def prescriptions(name):
    """Return dict a -> list of prescribed pairs (b, b2) of M_a."""
    pres = {a: [] for a in range(1, 15)}
    if name.startswith("kk"):
        n = int(name[2:])
        for a in range(1, 15):
            if block(a) <= n:
                for j in range(1, n + 1):
                    if j != block(a):
                        pres[a].append(members(j))
    elif name in ("h12", "g6"):
        for a in range(1, 13):
            pres[a].append((13, 14))
        if name == "g6":
            for a in (13, 14):
                for j in range(1, 7):
                    pres[a].append(members(j))
    else:
        raise SystemExit("unknown family")
    return pres


def share_from(pres):
    partner = {}
    for a, pairs in pres.items():
        for b, b2 in pairs:
            partner[(a, b)] = b2
            partner[(a, b2)] = b

    def share(a, b, b2):
        pb, pb2 = partner.get((a, b)), partner.get((a, b2))
        if pb is None and pb2 is None:
            return None
        return pb == b2

    return share


if __name__ == "__main__":
    name, out = sys.argv[1], sys.argv[2]
    n, k, lam, mu, fixed, mate, outer, idx = H.build(share_from(prescriptions(name)))
    enc, e = S.encode(n, k, lam, mu, fixed)
    S.write_dimacs(enc, out)
    free = sum(1 for x in e.values() if x not in (S.T, S.F))
    print("%s: free pairs=%d, variables=%d, clauses=%d" % (name, free, enc.nv, len(enc.clauses)))
