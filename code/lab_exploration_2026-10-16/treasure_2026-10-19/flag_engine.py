"""Flag blocks as sparse AMALGAM INCIDENCES (LAB 19/10/2026), for the cutting-plane solver flag_cut_loop.py.

For a labelled admissible type sigma (k vertices) and its flags of order m (flag_sdp.flags_of), the block
    M_sigma[F1,F2] = sum over amalgam patterns of x_H        (x_H = number of induced embeddings of the type H)
is stored as the list of (pair index, census type id, multiplicity), pair index = i*nf + j for i <= j.  The census
gives x_H = F[H] . (1, x) (affine in the parameters x), so M_sigma(x) and the cuts u^T M_sigma(x) u >= 0 are cheap.
Census type ids: position in the list of all (order, key) of the census JSON, orders ascending, keys in file order.

usage: python flag_engine.py build <census json> <k> <m> <sigma start> <sigma count> <out dir> [--workers=W]
       python flag_engine.py forms <census json> <out npz>        (sparse form matrix F, type ids, P index)"""
import json
import os
import sys
import time
from fractions import Fraction as Fr

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "census2_code"))
import census2 as C2  # noqa: E402
from flag_sdp import admissible, amalgams, flags_of  # noqa: E402


def load_types(path):
    d = json.load(open(path))
    tid, forms = {}, []
    for n in sorted(d["types"], key=int):
        for key, rows, aut, form in d["types"][n]:
            tid[(int(n), key)] = len(forms)
            forms.append(form)
    return d, tid, forms


def build_block(d, tid, sigma, k, m, cache):
    fl = flags_of(sigma, k, m)
    nf = len(fl)
    pairs, tids, mult = [], [], []
    for i in range(nf):
        for j in range(i, nf):
            acc = {}
            for n, rows in amalgams(fl[i], fl[j], k, m):
                key = (n, tuple(rows))
                t = cache.get(key, -2)
                if t == -2:
                    if not admissible(n, rows):
                        t = -1
                    else:
                        code, _ = C2.canon(n, list(rows))
                        t = tid.get((n, code), -1)
                    cache[key] = t
                if t >= 0:
                    acc[t] = acc.get(t, 0) + 1
            for t, c in acc.items():
                pairs.append(i * nf + j)
                tids.append(t)
                mult.append(c)
    return nf, np.array(pairs, dtype=np.int64), np.array(tids, dtype=np.int32), np.array(mult, dtype=np.int32)


def _job(args):
    path, k, m, si, out = args
    fn = os.path.join(out, "T_k%d_m%d_s%d.npz" % (k, m, si))
    if os.path.exists(fn):
        return si, "exists"
    tid = _G["tid"]
    sig = _G["sig"][k][si]
    t0 = time.time()
    nf, pairs, tids, mult = build_block(None, tid, sig, k, m, {})
    np.savez_compressed(fn + ".tmp.npz", nf=nf, pairs=pairs, tids=tids, mult=mult, k=k, m=m, sigma=si)
    os.replace(fn + ".tmp.npz", fn)
    return si, "nf %d, entries %d, %.0f s" % (nf, len(pairs), time.time() - t0)


_G = {}


def main():
    what = sys.argv[1]
    if what == "forms":
        d, tid, forms = load_types(sys.argv[2])
        NP = len(d["params"])
        rows, cols, vals = [], [], []
        for t, form in enumerate(forms):
            for p, v in form.items():
                rows.append(t)
                cols.append(int(p))
                vals.append(float(Fr(v)))
        np.savez_compressed(sys.argv[3], rows=np.array(rows, dtype=np.int32), cols=np.array(cols, dtype=np.int32),
                            vals=np.array(vals), ntypes=len(forms), NP=NP)
        print("forms: %d types, %d parameters, %d nonzeros" % (len(forms), NP, len(vals)))
        return
    path, k, m, start, count, out = sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), \
        int(sys.argv[6]), sys.argv[7]
    opts = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
    W = int(opts.get("workers", 1))
    os.makedirs(out, exist_ok=True)
    d, tid, forms = load_types(path)
    sig = {int(n): [rows for key, rows, aut, form in lst] for n, lst in d["types"].items()}
    del d, forms                                     # workers only need the type ids and the sigma rows
    _G.update(tid=tid, sig=sig)
    nsig = len(sig[k])
    jobs = [(path, k, m, si, out) for si in range(start, min(start + count, nsig))]
    t0 = time.time()
    if W <= 1:
        for j in jobs:
            print(_job(j), "[%.0f s]" % (time.time() - t0), flush=True)
    else:
        import multiprocessing as mp
        ctx = mp.get_context("fork")
        with ctx.Pool(W) as pool:
            for r in pool.imap_unordered(_job, jobs):
                print(r, "[%.0f s]" % (time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
