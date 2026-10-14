"""Family kk6: six of the seven lines through x pairwise span grids (15 grids through x on blocks 1..6).

Then every M_a, a <= 12, respects all seven blocks (the last pair is forced), and the only freedom is the pair of
matchings (M_13, M_14) on the points 1..12, up to the group of block permutations and sign changes of blocks 1..6
and the exchange of 13 and 14. This script
  1. lists the classes of pairs (M_13, M_14): canonical form of the 3-edge-coloured multigraph
     (blocks, M_13, M_14) with colour 0 fixed and colours 1, 2 exchangeable (psi_orbits.canon restricted);
  2. encodes kk6 once with M_13, M_14 free, and for each class adds the 132 unit clauses and calls cadical.
One process, cadical calls in sequence, 2 GB bound. Log kk6_all_log.txt:  K count verdict seconds
The class with M_13 = M_14 = blocks is target T1 (decided separately by 588 sub-cases).

usage: python kk6_all.py limit_seconds workdir
"""
import shutil
import subprocess
import sys
import time

import family as FAM
import h12_instance as H
import psi_orbits as PO
import srg_sat as S

CADICAL = r"C:\Users\RESEARCHER\Desktop\Recherche_Conway\c1-codex\tools\win64\cadical.exe"


def canon_fixed(maps):
    """Canonical form with colour 0 fixed and colours 1, 2 exchangeable."""
    best = None
    for perm in ((0, 1, 2), (0, 2, 1)):
        mp = [maps[perm[0]], maps[perm[1]], maps[perm[2]]]
        seen = set()
        comps = []
        for s0 in range(PO.N):
            if s0 in seen:
                continue
            comp = {s0}
            stack = [s0]
            while stack:
                v = stack.pop()
                for c in range(3):
                    w = mp[c][v]
                    if w not in comp:
                        comp.add(w)
                        stack.append(w)
            seen |= comp
            bestc = None
            for s in comp:
                label = {s: 0}
                order = [s]
                i = 0
                code = []
                while i < len(order):
                    v = order[i]
                    i += 1
                    for c in range(3):
                        w = mp[c][v]
                        if w not in label:
                            label[w] = len(order)
                            order.append(w)
                        code.append(label[w])
                code = tuple(code)
                if bestc is None or code < bestc:
                    bestc = code
            comps.append(bestc)
        form = tuple(sorted(comps))
        if best is None or form < best:
            best = form
    return best


if __name__ == "__main__":
    limit, workdir = int(sys.argv[1]), sys.argv[2]
    ms = list(PO.all_matchings(tuple(range(PO.N))))
    b0 = PO.to_map(PO.BETA)
    classes = {}
    for mb in PO.second_matchings():
        b1 = PO.to_map(mb)
        for mc in ms:
            f = canon_fixed([b0, b1, PO.to_map(mc)])
            if f not in classes:
                classes[f] = [0, mb, tuple(sorted(mc))]
            classes[f][0] += 1
    reps = sorted(classes.values(), key=lambda t: (-t[0], t[1], t[2]))
    with open("kk6_classes.txt", "w") as out:
        for r in reps:
            out.write(repr(tuple(r)) + "\n")
    print("classes of pairs (M_13, M_14):", len(reps), flush=True)

    n, k, lam, mu, fixed, mate, outer, idx = H.build(FAM.share_from(FAM.prescriptions("kk6")))
    enc, e = S.encode(n, k, lam, mu, fixed)
    base = len(enc.clauses)
    body = workdir + "/kk6_body.cnf"
    with open(body, "w") as f:
        for c in enc.clauses:
            f.write(" ".join(map(str, c)) + " 0\n")

    def var(a, b, b2):
        u, v = idx[(min(a, b), max(a, b))], idx[(min(a, b2), max(a, b2))]
        return e[(min(u, v), max(u, v))]

    for K, (cnt, mb, mc) in enumerate(reps):
        del enc.clauses[base:]
        for a, m in ((13, mb), (14, mc)):
            pairs = {frozenset((p + 1, q + 1)) for p, q in m}
            for b in range(1, 13):
                for b2 in range(b + 1, 13):
                    lit = var(a, b, b2)
                    if frozenset((b, b2)) in pairs:
                        enc.assert_true(lit)
                    else:
                        enc.assert_false(lit)
        extra = enc.clauses[base:]
        cnf = workdir + "/kk6_case.cnf"
        with open(cnf, "wb") as out:
            out.write(("p cnf %d %d\n" % (enc.nv, base + len(extra))).encode())
            with open(body, "rb") as b:
                shutil.copyfileobj(b, out, 1 << 24)
            for c in extra:
                out.write((" ".join(map(str, c)) + " 0\n").encode())
        t0 = time.time()
        try:
            r = subprocess.run([CADICAL, "-q", cnf], capture_output=True, text=True, timeout=limit)
            res = r.stdout
        except subprocess.TimeoutExpired:
            res = ""
        dt = time.time() - t0
        verdict = "UNSAT" if "s UNSATISFIABLE" in res else ("SAT" if "s SATISFIABLE" in res else "UNKNOWN")
        line = "%d %d %s %.1f" % (K, cnt, verdict, dt)
        print(line, flush=True)
        with open("kk6_all_log.txt", "a") as f:
            f.write(line + "\n")
