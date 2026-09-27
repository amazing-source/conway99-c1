r"""Independent check (C1 27/09) of the y-pair enumeration (y_pairs.py / y2_engine.py) by BRUTE FORCE, for small cases.
1. Stream ALL norm-7 vectors of U (Fincke-Pohst, exact integer norms), keep those passing the single-y filters
   (|(a,y)| <= 2 on roots, |(b,y)| <= 3/2 on new roots, |(v,y)| <= 3 on norm-3 vectors); memory: survivors only.
2. Map each survivor to its W(R)-dominant representative by simple reflections (no label/DP/orbit machinery), and compare the set
   of dominant ones with dominant_y1.
3. For each dominant y1: all survivors orthogonal to y1 with the pair filters, reduced to W(R cap y1-perp)-dominance by reflections
   in the simple roots of the parabolic subsystem (simple roots at the zero labels of y1), up to sign; compare with Y2Engine.
Usage: python brute_ypairs.py <envelope.json> [--max-seconds S]"""
import json, math, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from y_pairs import setup, dominant_y1, root_system
from y2_engine import Y2Engine


def stream_norm(Gi, bound, cb, chunk=10000):
    n = len(Gi)
    L = np.linalg.cholesky(np.array(Gi, dtype=float))
    d = [float(L[i, i] ** 2) for i in range(n)]
    Q = [[float(L[j, i] / L[i, i]) if j > i else 0.0 for j in range(n)] for i in range(n)]
    buf, x, eps = [], [0] * n, 1e-7

    def rec(k, rem):
        s = 0.0
        Qk = Q[k]
        for j in range(k + 1, n):
            if x[j]:
                s += Qk[j] * x[j]
        c = -s
        sp = math.sqrt(max(rem, 0.0) / d[k]) + eps
        for xi in range(math.ceil(c - sp), math.floor(c + sp) + 1):
            t = xi - c
            r2 = rem - d[k] * t * t
            if r2 < -eps:
                continue
            x[k] = xi
            if k == 0:
                buf.append(tuple(x))
                if len(buf) >= chunk:
                    cb(np.array(buf, dtype=np.int64)); buf.clear()
            else:
                rec(k - 1, r2)
        x[k] = 0
    rec(n - 1, float(bound) + eps)
    if buf:
        cb(np.array(buf, dtype=np.int64))


def to_dominant(v, simple, max_iter=100000):
    v = v.copy()
    for _ in range(max_iter):
        ips = simple @ v
        k = int(np.argmin(ips))
        if ips[k] >= -1e-9:
            return v
        v = v - ips[k] * simple[k]
    raise RuntimeError('no convergence')


def main():
    rec_ = json.load(open(sys.argv[1]))
    ms = float(sys.argv[sys.argv.index('--max-seconds') + 1]) if '--max-seconds' in sys.argv else 3000
    t0 = time.time()
    B, Gi, Bf, R, X3, Snew = setup(rec_['gens'])
    Gz = np.array(Gi, dtype=np.int64)
    Binv = np.linalg.inv(Bf)
    surv = []

    def cb(A):
        A = A[np.any(A != 0, axis=1)]
        nr = np.einsum('ij,jk,ik->i', A, Gz, A)
        A = A[nr == 7]
        if not len(A):
            return
        V = A.astype(float) @ Bf
        ok = np.abs(V @ Snew.T).max(axis=1) <= 1.5 + 1e-9
        ok &= np.abs(V @ X3.T).max(axis=1) <= 3 + 1e-9
        if len(R):
            ok &= np.abs(V @ R.T).max(axis=1) <= 2 + 1e-9
        surv.extend(V[ok])
    stream_norm(Gi, 7, cb)
    S_all = np.array(surv)
    print(json.dumps({'id': rec_['id'], 'survivors_single_y': len(S_all), 's': round(time.time() - t0, 1)}), flush=True)
    Ssimp, comp, marks, A, P = root_system(R)
    # 2. dominant representatives (up to nothing) of all survivors
    domset = set()
    for v in S_all:
        dvec = to_dominant(v, Ssimp)
        domset.add(tuple(np.rint(dvec @ Binv).astype(np.int64)))
    Y, Yf, info = dominant_y1(B, Gi, Bf, R, X3, Snew)
    mine = {tuple(int(a) for a in row) for row in Y}
    print(json.dumps({'dominant_bruteforce': len(domset), 'dominant_y1': len(mine), 'equal': domset == mine,
                      'only_brute': len(domset - mine), 'only_mine': len(mine - domset)}), flush=True)
    # 3. per dominant y1: y2 sets
    eng = Y2Engine(B, Gi, Bf, R, X3, Snew)
    Rall = R
    mism = 0
    for k in range(len(Y)):
        if time.time() - t0 > ms:
            print('TIMEOUT at y1', k); break
        y1 = Yf[k]
        labs = np.rint(Ssimp @ y1).astype(np.int64)
        par = Ssimp[labs == 0]
        cand = S_all[np.abs(S_all @ y1) < 1e-6]
        if len(cand):
            ok = np.ones(len(cand), bool)
            P1 = np.abs(Snew @ y1); P2 = np.abs(cand @ Snew.T)
            ok &= ~((P2 > 1.4) & (P1[None, :] > 1.4)).any(axis=1)
            Q1 = np.abs(X3 @ y1); Q2 = np.abs(cand @ X3.T)
            ok &= ~((Q2 > 2.9) & (Q1[None, :] > 2.9)).any(axis=1)
            if len(Rall):
                A1 = Rall @ y1; A2 = cand @ Rall.T
                ok &= ((A1[None, :] ** 2 + A2 ** 2) <= 6 + 1e-9).all(axis=1)
            cand = cand[ok]
        bset = set()
        for v in cand:
            dv = to_dominant(v, par) if len(par) else v
            key = tuple(np.rint(dv @ Binv).astype(np.int64))
            neg = tuple(-a for a in key)
            bset.add(min(key, neg))
        Y2, st = eng.pairs_for(y1, t0=time.time(), max_seconds=ms)
        mset = set()
        for row in Y2:
            key = tuple(int(a) for a in row); neg = tuple(-a for a in key)
            mset.add(min(key, neg))
        if bset != mset:
            mism += 1
            print(json.dumps({'y1': k, 'brute': len(bset), 'mine': len(mset), 'only_brute': len(bset - mset), 'only_mine': len(mset - bset)}), flush=True)
    print(json.dumps({'y1_checked': len(Y), 'y2_mismatches': mism, 'seconds': round(time.time() - t0, 1)}), flush=True)


if __name__ == '__main__':
    main()
