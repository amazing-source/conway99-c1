r"""X19s -- export a pair x block certificate (x19q pickle) in the verification format agreed with 'structures':
<base>.npz (data, indices, indptr, shape, b, y_int, D) and <base>.json (tau, sigma, specials, rows, cols,
farkas_scaled, D).  Columns: x|<z>|<i>|<type>, s|<z>|<i>|<R>|<y1>+<y2>...; rows: conv, cons, labdeg, bal, lab, P2,
pairblk, pairpair (names carry every index)."""
import sys, json, pickle
import numpy as np
sys.path.insert(0, 'scripts')
import x19n_pairblock as PB
fmt = lambda l: f'{l[0]}.{l[1]}'
pn = lambda z: '-'.join(fmt(l) for l in sorted(z))
for pkl in sys.argv[1:]:
    C = pickle.load(open(pkl, 'rb'))
    A, b, nv, rn, cn, spec = PB.build(C['tau'], C['sigma'], track=True)
    Ai = A.tocsr().astype(np.int64); bi = np.rint(b).astype(np.int64); yi = np.asarray(C['y_int'], dtype=np.int64)
    colv = Ai.T @ yi
    val = int(bi @ yi) - int(colv[colv > 0].sum())
    assert val > 0 and val == C['value_scaled'], (val, C['value_scaled'])
    base = pkl.replace('.pkl', '_pb')
    np.savez_compressed(base + '.npz', data=Ai.data, indices=Ai.indices, indptr=Ai.indptr, shape=np.array(Ai.shape),
                        b=bi, y_int=yi, D=np.array([C['D']]))
    json.dump(dict(tau={fmt(u): [[fmt(v), fmt(w)] for v, w in C['tau'][u].items() if v < w] for u in C['tau']},
                   sigma={str(c): [[fmt(v), fmt(w)] for v, w in C['sigma'][c].items()] for c in C['sigma']},
                   specials={pn(z): [pn(w) for w in spec[z]] for z in spec},
                   rows=rn, cols=cn, farkas_scaled=val, D=C['D']), open(base + '.json', 'w'))
    print(f'{pkl} -> {base}.npz/.json  ({len(rn)} rows, {len(cn)} cols, Farkas {val} re-checked)', flush=True)
