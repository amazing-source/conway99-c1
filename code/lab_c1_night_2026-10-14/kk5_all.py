"""Family kk5: five of the seven lines through x pairwise span grids (10 grids through x on blocks 1..5).

Hypothesis in the local view: for a in blocks 1..5 the matching M_a pairs the two vertices of each other block
among 1..5 (its last four points 11, 12, 13, 14 are matched in one of three ways, left to the solver). The
matchings M_11, M_12, M_13, M_14 are free. Probes (kkN_probe_log.txt) show that prescribing M_11 alone lets
cadical refute the instance in about 20 to 30 s. Any graph of the family has some M_11, so it is enough to refute
one representative of each class of M_11 under the symmetries that keep the hypothesis and fix the vertex 11:
permutations and sign changes of blocks 1..5, and the exchange of 13 and 14.

M_11 is a perfect matching of the 12 points {1..10, 13, 14}; these carry six blocks, one of them ({13,14}) marked.
Classes = union with the block matching, up to isomorphism keeping the marked block: 19 classes expected
(partitions of 6 with one marked part).

usage: python kk5_all.py limit_seconds workdir       -> kk5_classes.txt, kk5_all_log.txt: K count verdict seconds
One process, cadical calls in sequence, 2 GB bound.
"""
import subprocess
import sys
import time

import family as FAM
import h12_instance as H
import psi_orbits as PO
import srg_sat as S

CADICAL = r"C:\Users\RESEARCHER\Desktop\Recherche_Conway\c1-codex\tools\win64\cadical.exe"
# points 0..9 = inner vertices 1..10 ; points 10, 11 = inner vertices 13, 14
POINT_TO_INNER = {i: i + 1 for i in range(10)}
POINT_TO_INNER[10] = 13
POINT_TO_INNER[11] = 14
MARKED = {10, 11}


def canon_marked(b0, m):
    comps = []
    seen = set()
    for s0 in range(12):
        if s0 in seen:
            continue
        comp = {s0}
        stack = [s0]
        while stack:
            v = stack.pop()
            for mp in (b0, m):
                w = mp[v]
                if w not in comp:
                    comp.add(w)
                    stack.append(w)
        seen |= comp
        best = None
        for s in comp:
            label = {s: 0}
            order = [s]
            i = 0
            code = []
            while i < len(order):
                v = order[i]
                i += 1
                for mp in (b0, m):
                    w = mp[v]
                    if w not in label:
                        label[w] = len(order)
                        order.append(w)
                    code.append(label[w])
                code.append(1 if v in MARKED else 0)
            code = tuple(code)
            if best is None or code < best:
                best = code
        comps.append(best)
    return tuple(sorted(comps))


if __name__ == "__main__":
    limit, workdir = float(sys.argv[1]), sys.argv[2]
    b0 = PO.to_map(PO.BETA)
    classes = {}
    for m in PO.all_matchings(tuple(range(12))):
        f = canon_marked(b0, PO.to_map(m))
        if f not in classes:
            classes[f] = [0, tuple(sorted(m))]
        classes[f][0] += 1
    reps = sorted(classes.values(), key=lambda t: (-t[0], t[1]))
    with open("kk5_classes.txt", "w") as out:
        for r in reps:
            out.write(repr(tuple(r)) + "\n")
    print("classes of M_11:", len(reps), " total", sum(r[0] for r in reps), flush=True)
    for K, (cnt, m) in enumerate(reps):
        pres = FAM.prescriptions("kk5")
        pres[11] = [(POINT_TO_INNER[p], POINT_TO_INNER[q]) for p, q in m]
        n, k, lam, mu, fixed, mate, outer, idx = H.build(FAM.share_from(pres))
        enc, e = S.encode(n, k, lam, mu, fixed)
        cnf = workdir + "/kk5_case.cnf"
        S.write_dimacs(enc, cnf)
        t0 = time.time()
        try:
            r = subprocess.run([CADICAL, "-q", cnf], capture_output=True, text=True, timeout=limit)
            res = r.stdout
        except subprocess.TimeoutExpired:
            res = ""
        dt = time.time() - t0
        verdict = "UNSAT" if "s UNSATISFIABLE" in res else ("SAT" if "s SATISFIABLE" in res else "UNKNOWN")
        line = "%d %d %s %.1f %s" % (K, cnt, verdict, dt, pres[11])
        print(line, flush=True)
        with open("kk5_all_log.txt", "a") as f:
            f.write(line + "\n")
