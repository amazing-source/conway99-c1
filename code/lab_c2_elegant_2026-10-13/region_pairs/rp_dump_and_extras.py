"""(1) dump the raw data of the chosen pairs (H4, shadow classes, product matrices) to npz; (2) test whether the norm-2 shadow vectors form a
spherical 2-design of R^24 (sum_v (v,x)^2 proportional to (x,x)) for each lattice; (3) linear fits of extra counts on all region pairs.
<lab python> -B rp_dump_and_extras.py"""
import sys, os, json, glob, fractions
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rp_lib import Lattice, OUT
import rp_search as RS

CHOSEN = [("044", 0), ("044", 1), ("044", 3), ("072", 0), ("072", 18), ("106", 0), ("106", 2), ("106", 3), ("111", 0), ("131", 0)]
design = {}
for lid in sorted(set(c[0] for c in CHOSEN)):
    lat = Lattice(lid); G = lat.G
    scan = json.load(open(os.path.join(OUT, "scan_%s.json" % lid)))
    regs = [q for q in scan["pairs"] if q["region"]]
    for (l2, idx) in CHOSEN:
        if l2 != lid: continue
        p = regs[idx]
        y1 = np.array(p["y1"], dtype=np.int64); y2 = np.array(p["y2"], dtype=np.int64)
        inst = RS.build_instance(lat, y1, y2, p)
        np.savez_compressed(os.path.join(OUT, "pair_data_%s_row%d.npz" % (lid, p["row"])), y1=y1.astype(np.int16), y2=y2.astype(np.int16), G=G.astype(np.int16),
                            H4=inst["H"].astype(np.int16), E11_classes_2b=inst["V11"].astype(np.int16), E13_classes_2b=inst["V13"].astype(np.int16),
                            P11=inst["P11"].astype(np.int8), P13=inst["P13"].astype(np.int8), admissible=inst["adm"])
        print("dumped", lid, idx, "row", p["row"], flush=True)
    # 2-design test of the norm-2 shadow vectors v = 2b : sum_v (v G x)^2 = lambda (x G x) for all x  <=>  G Q G = lambda G, Q = sum v v^T
    V = lat.S[2].astype(object)
    Q = np.zeros((24, 24), dtype=object)
    Vi = lat.S[2]
    Q = (Vi.T @ Vi).astype(object)
    M = (G.astype(object) @ Q @ G.astype(object))
    M0 = G.astype(object)
    # is M proportional to G ?
    lam = fractions.Fraction(int(M[0, 0]), int(M0[0, 0])) if M0[0, 0] != 0 else None
    prop = all(fractions.Fraction(int(M[i, j])) == (lam * int(M0[i, j])) for i in range(24) for j in range(24)) if lam is not None else False
    design[lid] = {"S2_vectors": int(Vi.shape[0]), "gram_proportional": bool(prop), "lambda": (str(lam) if prop else None), "expected_lambda_if_design": str(fractions.Fraction(int(Vi.shape[0]), 3))}
    print("lattice", lid, "norm-2 shadow vectors form a spherical 2-design:", prop, design[lid], flush=True)
json.dump(design, open(os.path.join(OUT, "design_test.json"), "w"), indent=1)

# (3) extra linear relations over all region pairs
rows = []
for f in sorted(glob.glob(os.path.join(OUT, "scan_*.json"))):
    d = json.load(open(f))
    for p in d["pairs"]:
        if p["region"]: rows.append(p)
print("region pairs:", len(rows))
keys = ["I14", "I16", "S15"]
A = np.array([[1, p["n11"], p["s"]] for p in rows], dtype=float)
fits = {}
for k in keys:
    y = np.array([p[k] for p in rows], dtype=float)
    c, res, rk, sv = np.linalg.lstsq(A, y, rcond=None)
    err = np.abs(A @ c - y).max()
    fits[k] = {"coef_[1,n11,s]": [round(float(x), 6) for x in c], "max_abs_residual": float(err), "exact": bool(err < 1e-9)}
    print(k, fits[k])
json.dump(fits, open(os.path.join(OUT, "extra_fits.json"), "w"), indent=1)
