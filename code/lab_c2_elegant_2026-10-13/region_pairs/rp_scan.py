"""Task 1 scan: classify every stored no-witness ('survivor') pair of one lattice and compute the Task 1 counts.

  <lab python> -B rp_scan.py <lid> [<lid> ...]          output: scan_<lid>.json in this folder

For every survivor pair (y1, y2) of hand_28/<lid>_pairs.npz (rows with stored minimum E >= 11) it recomputes, directly and in exact integers:
  * validity: (y1,y1) = (y2,y2) = 7, (y1,y2) = 0;
  * witness test: minimum of E(v) = 7(v,v) - (v,y1)^2 - (v,y2)^2 over ALL vectors of norm 2, 3, 4 of U (and E > 0 for all of them);
  * trap test: minimum of E(b) over ALL shadow vectors of norm 2 and 4 (4 E(b) = 7 q - p1^2 - p2^2, q = 4 (b,b), p_i = 2 (b,y_i));
  * the Task 1 counts (window recipe) and the same counts by an independent canonical-representative method.

Why norms <= 4 / products in [-3,3] suffice: (v + m y1 + n y2, y1) = (v,y1) + 7m, so every coset v + J has exactly ONE representative with both
products in [-3,3]; it has the smallest norm of its coset (norm changes by m(7m + 2a) >= 0 for |a| <= 3); E is constant on the coset and
N = (E + a^2 + b^2)/7 <= (E + 18)/7.  E <= 16 gives N <= 4.86, so N <= 4: the shells of norm 2, 3, 4 contain every coset with 0 < E <= 16.
Shadow: p_i = 2(b,y_i) odd, shift by y_i changes p_i by 14, unique representative with p_i in {-5,...,7}; |p_i| <= 7 gives
a^2 + b^2 <= 24.5 so E(b) >= 7 N - 24.5 >= 17.5 for N >= 6: shadow norms 2 and 4 contain every coset with E(b) <= 15.5.
(The shadow norm is even; 4E(b) = 28 k - p1^2 - p2^2 is == 6 mod 8, so E(b) in {..., 9.5, 11.5, 13.5, 15.5, 17.5, ...}.)
"""
import sys, os, json, time, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rp_lib
from rp_lib import Lattice, load_survivor_pairs, OUT

PRED = {  # user's predictions, as functions of (n11, s)
    "N2 = s - 12": lambda n11, s: s - 12,
    "I12 = 4 - n11 + s/2": lambda n11, s: 4 - n11 + s / 2,
    "I13 = 8 - n11 + 3s/2": lambda n11, s: 8 - n11 + 3 * s / 2,
    "I15 = 96 - n11 - s": lambda n11, s: 96 - n11 - s,
    "N3 = 688 + 2 n11 - s": lambda n11, s: 688 + 2 * n11 - s,
    "S13 = 48 - 2 n11 + s": lambda n11, s: 48 - 2 * n11 + s,
}


def mm(A, Y):
    """exact A @ Y for small integer matrices through float64 BLAS (all entries < 2^20, 24-term sums < 2^53)"""
    return np.rint(A @ Y).astype(np.int64)


def analyse(lat, y1, y2):
    G = lat.G
    r = {}
    assert int(y1 @ G @ y1) == 7 and int(y2 @ G @ y2) == 7 and int(y1 @ G @ y2) == 0, "pair is not (7,7,0)"
    Y = np.stack([y1, y2], axis=1).astype(np.float64)
    # ---- U shells
    minE = 10 ** 9; cnt = {}; raw = {}; canon = {}
    N_orth = {}
    for k in (2, 3, 4):
        P = mm(lat.XGf[k], Y); a, b = P[:, 0], P[:, 1]
        E = 7 * k - a * a - b * b
        assert (E > 0).all(), "a vector of norm %d outside J with E <= 0" % k
        minE = min(minE, int(E.min()))
        win = (np.abs(a) <= 3) & (np.abs(b) <= 3)
        raw[k] = {int(e): int(((E == e) & win).sum()) for e in range(1, 21)}
        N_orth[k] = int(((a == 0) & (b == 0)).sum())
        # independent check by canonical representatives: every vector with E in 11..16, moved to its window representative
        for e in range(11, 17):
            sel = np.flatnonzero(E == e)
            if len(sel) == 0: continue
            m = (a[sel] + 3) // 7; n = (b[sel] + 3) // 7                   # floor division: exact integer
            rep = lat.X[k][sel] - m[:, None] * y1[None, :] - n[:, None] * y2[None, :]
            canon.setdefault(e, []).append(rep)
    cosets = {}
    for e in range(11, 17):
        # total over shells of window counts
        tot = sum(raw[k].get(e, 0) for k in (2, 3, 4))
        reps = np.concatenate(canon[e]) if e in canon else np.zeros((0, 24), np.int64)
        nuniq = len(np.unique(reps, axis=0)) if len(reps) else 0
        assert nuniq == tot, ("canonical-representative count differs from the window count", e, nuniq, tot)
        assert tot % 2 == 0
        cosets[e] = tot            # number of cosets (v and -v counted separately)
    r["minE_U"] = minE
    r["cosets_E_both_signs"] = {str(e): cosets[e] for e in cosets}
    r["raw_window_by_norm"] = {str(k): {str(e): raw[k][e] for e in range(1, 21) if raw[k][e]} for k in raw}
    r["N2"] = N_orth[2]; r["N3"] = N_orth[3]; r["N4_orth_both_signs"] = N_orth[4]
    r["n11"] = cosets[11] // 2
    for e in (12, 13, 14, 15, 16): r["I%d" % e] = cosets[e] // 2
    r["I14_check_N2_over_2"] = (r["I14"] == N_orth[2] // 2)
    # ---- shadow
    minE4 = 10 ** 9; sh_counts = collections.Counter(); sh_raw = {}
    sfeat = {}
    for k in (2, 4):
        P = mm(lat.SGf[k], Y); p1, p2 = P[:, 0], P[:, 1]
        assert (p1 % 2 != 0).all() and (p2 % 2 != 0).all(), "shadow products must be half-odd"
        f = 28 * k - p1 * p1 - p2 * p2                                     # 4 E(b)
        assert (f > 0).all()
        minE4 = min(minE4, int(f.min()))
        win = (p1 >= -5) & (p1 <= 7) & (p2 >= -5) & (p2 <= 7)
        for val in np.unique(f[win]):
            sh_counts[int(val)] += int(((f == val) & win).sum())
        sh_raw[k] = {int(v): int((f == v).sum()) for v in np.unique(f)}
        sfeat[k] = (p1, p2, f, win)
    r["min_4E_shadow"] = minE4
    r["shadow_cosets_by_4E_both_signs"] = {str(v): c for v, c in sorted(sh_counts.items())}
    r["shadow_all_vectors_by_4E"] = {str(k): {str(v): c for v, c in sorted(sh_raw[k].items())} for k in sh_raw}
    for v, c in sh_counts.items(): assert c % 2 == 0, ("odd shadow coset count", v, c)
    # s : norm-2 shadow vectors with {|p1|,|p2|} = {1,3}
    p1, p2, f, win = sfeat[2]
    sel = (np.minimum(np.abs(p1), np.abs(p2)) == 1) & (np.maximum(np.abs(p1), np.abs(p2)) == 3)
    r["s_vectors"] = int(sel.sum()); assert r["s_vectors"] % 2 == 0
    r["s"] = r["s_vectors"] // 2
    assert int((sel & (f == 46)).sum()) == r["s_vectors"]
    # 4E = 46 can only come from norm 2 (66 is not a sum of two odd squares): check
    p1b, p2b, fb, winb = sfeat[4]
    assert int(((fb == 46)).sum()) == 0
    r["S13"] = sh_counts.get(54, 0) // 2
    r["S15"] = sh_counts.get(62, 0) // 2
    r["S11"] = sh_counts.get(46, 0) // 2
    assert r["S11"] == r["s"], (r["S11"], r["s"])
    r["witness"] = bool(minE <= 10)
    r["trap_violation"] = bool(minE4 < 46)
    r["region"] = (not r["witness"]) and (not r["trap_violation"])
    # predictions
    pr = {}
    for name, fn in PRED.items():
        lhs = name.split("=")[0].strip()
        val = r[lhs] if lhs in r else None
        pred = fn(r["n11"], r["s"])
        pr[name] = {"observed": val, "predicted": pred, "holds": (val == pred)}
    r["identities"] = pr
    return r


def main():
    lids = sys.argv[1:]
    for lid in lids:
        t0 = time.time()
        lat = Lattice(lid)
        lat.XGf = {k: lat.XG[k].astype(np.float64) for k in lat.XG}
        lat.SGf = {k: lat.SG[k].astype(np.float64) for k in lat.SG}
        assert max(int(np.abs(lat.XG[k]).max()) for k in lat.XG) < 2 ** 20 and max(int(np.abs(lat.SG[k]).max()) for k in lat.SG) < 2 ** 20
        pairs, total = load_survivor_pairs(lid)
        out = {"lid": lid, "stored_pairs": total, "survivors": len(pairs), "N2_lattice": lat.shell_counts[2],
               "shell_counts": lat.shell_counts, "shadow_counts": {str(k): len(lat.S[k]) for k in lat.S}, "pairs": []}
        nreg = ntrap = nwit = 0
        for (row, o, y1, y2) in pairs:
            r = analyse(lat, y1, y2)
            r.update(row=row, o=o, y1=[int(x) for x in y1], y2=[int(x) for x in y2])
            out["pairs"].append(r)
            nreg += r["region"]; ntrap += (r["trap_violation"] and not r["witness"]); nwit += r["witness"]
        out["n_region"] = nreg; out["n_trap_violation_no_witness"] = ntrap; out["n_witness_found_by_recheck"] = nwit
        out["seconds"] = round(time.time() - t0, 1)
        json.dump(out, open(os.path.join(OUT, "scan_%s.json" % lid), "w"))
        print("lid %s: stored pairs %d, survivors %d, recheck: with witness %d, trap violation (no witness) %d, REGION %d | %.1fs"
              % (lid, total, len(pairs), nwit, ntrap, nreg, out["seconds"]), flush=True)


if __name__ == "__main__":
    main()
