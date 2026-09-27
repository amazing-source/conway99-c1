r"""Finish line (C), C1 27/09: FUSED y-pair enumeration + exact h-check, per W-dominant y1 (caches per y1).  PROVEN conditions:
pairs as in y_pairs.py / y2_engine.py (complete up to W); for each pair, 7 h with
  h _|_ y1, y2, pairwise orthogonal, |(h,beta)| <= 1 on new roots, Lemma Z (sum h in 2U),
  coverage w(beta) = sum_c (h_c,beta)^2: = 1 on hits(y1) u hits(y2); = 3 elsewhere if RIGID (no norm-3 vector hits at 3/2),
  in {1,3} elsewhere otherwise;  cells: norm-3 x _|_ y1, y2 with (x,h_c)(x,h_d) = +-1 (both signs) and (x,h_e) = 0 else.
A pair with no h-configuration is dead; a lattice all of whose pairs are dead is EXCLUDED.
Usage: python pairs_hcheck.py <envelope.json> <out.json> [--max-seconds S] [--pair-seconds P] [--y1 a:b]"""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from y_pairs import setup as ysetup, dominant_y1
from y2_engine import Y2Engine
from h_stage2 import short_vectors_fast


def bits(row):
    return int.from_bytes(np.packbits(np.asarray(row, dtype=np.uint8), bitorder='little').tobytes(), 'little')  # bit i = row[i]


def main():
    rec_ = json.load(open(sys.argv[1]))
    outp = sys.argv[2]
    ms = float(sys.argv[sys.argv.index('--max-seconds') + 1]) if '--max-seconds' in sys.argv else 3600
    ps = float(sys.argv[sys.argv.index('--pair-seconds') + 1]) if '--pair-seconds' in sys.argv else 60
    t0 = time.time()
    B, Gi, Bf, R, X3, Snew = ysetup(rec_['gens'])
    Y, Yf, info = dominant_y1(B, Gi, Bf, R, X3, Snew)
    lo, hi = 0, len(Y)
    if '--y1' in sys.argv:
        a, b = sys.argv[sys.argv.index('--y1') + 1].split(':')
        lo, hi = int(a), min(int(b), len(Y))
    eng = Y2Engine(B, Gi, Bf, R, X3, Snew)
    # new roots up to sign, norm-4 candidates with |(h,beta)| <= 1
    keep, seen = [], set()
    for k, s in enumerate(Snew):
        key = tuple(np.round(s * 4).astype(int))
        if tuple(-v for v in key) in seen:
            continue
        seen.add(key); keep.append(k)
    S = Snew[keep]
    X, nrm = short_vectors_fast(Gi, 4)
    X4c = X[nrm == 4]; X4 = X4c.astype(float) @ Bf
    HS = np.rint(X4 @ S.T).astype(np.int64)
    okh = np.abs(HS).max(axis=1) <= 1
    Hall, Hcall, COV = X4[okh], X4c[okh], (HS[okh] != 0)
    PAR = np.array([int(''.join(str(int(b) & 1) for b in row[::-1]), 2) for row in Hcall], dtype=object)
    rigid = bool((np.abs(np.abs(X3 @ S.T) - 1.5) < 1e-6).sum(axis=1).max() == 0)
    NI = len(S)
    stats = {'id': rec_['id'], 'roots': rec_['roots'], 'rigid': rigid, 'dominant_y1': len(Y), 'y1_range': [lo, hi],
             'h_cands': int(len(Hall)), 'pairs': 0, 'dead': 0, 'alive': 0, 'timeout': 0, 'y1_done': 0}
    alive = []
    print(json.dumps({k: stats[k] for k in ('id', 'rigid', 'dominant_y1', 'h_cands')}), flush=True)
    for k in range(lo, hi):
        if time.time() - t0 > ms:
            stats['stopped_at_y1'] = k
            break
        y1 = Yf[k]
        Y2, st = eng.pairs_for(y1, t0=time.time(), max_seconds=ms)
        if st.get('truncated'):
            stats['truncated_y2_at'] = k
        Y2f = Y2.astype(float) @ Bf if len(Y2) else np.zeros((0, 24))
        # caches for y1
        i1 = np.nonzero(np.abs(Hall @ y1) < 1e-9)[0]
        H1, C1, P1 = Hall[i1], COV[i1], PAR[i1]
        M1 = len(i1)
        orth = []
        for a in range(0, M1, 2000):
            G = np.abs(H1[a:a + 2000] @ H1.T) < 1e-9
            orth += [bits(r) for r in G]
        item_c = [bits(C1[:, b]) for b in range(NI)]
        parm = {}
        for i, p in enumerate(P1):
            parm[p] = parm.get(p, 0) | (1 << i)
        x1 = np.abs(X3 @ y1) < 1e-9
        X3p = X3[x1]
        IP3 = np.rint(X3p @ H1.T).astype(np.int8)
        hit1 = np.abs(np.abs(S @ y1) - 1.5) < 1e-6
        for y2 in Y2f:
            stats['pairs'] += 1
            tp = time.time()
            m2 = np.abs(H1 @ y2) < 1e-9
            allowed0 = bits(m2)
            rows = np.abs(X3p @ y2) < 1e-9
            IP = IP3[rows]
            yh = hit1 | (np.abs(np.abs(S @ y2) - 1.5) < 1e-6)
            found = []
            timed = [False]

            def cells_ok(ch):
                cols = IP[:, ch].astype(np.int16); nz = cols != 0; cnt = nz.sum(axis=1)
                for a in range(len(ch)):
                    for b in range(a + 1, len(ch)):
                        sel = (cnt == 2) & nz[:, a] & nz[:, b] & (np.abs(cols[:, a]) == 1) & (np.abs(cols[:, b]) == 1)
                        if not sel.any():
                            return False
                        pr = cols[sel, a] * cols[sel, b]
                        if not (pr > 0).any() or not (pr < 0).any():
                            return False
                return True

            def rec(ch, allowed, w, parity):
                if found or timed[0]:
                    return
                if time.time() - tp > ps:
                    timed[0] = True
                    return
                kk = len(ch)
                if kk == 7:
                    good = np.all(w[yh] == 1) and (np.all(w[~yh] == 3) if rigid else np.all((w[~yh] == 1) | (w[~yh] == 3)))
                    if good and parity == 0:
                        found.append(list(ch))
                    return
                best, bc = None, None
                for b in range(NI):
                    wb = w[b]
                    if yh[b]:
                        if wb >= 1:
                            continue
                        need = 1
                    elif rigid:
                        if wb >= 3:
                            continue
                        need = 3 - wb
                    else:
                        if wb in (1, 3):
                            continue
                        need = 1
                    if need > 7 - kk:
                        return
                    cnt = (allowed & item_c[b]).bit_count()
                    if cnt < need:
                        return
                    if best is None or cnt < bc:
                        best, bc = b, cnt
                if best is None:
                    if rigid:
                        return
                    cand = allowed
                else:
                    cand = allowed & item_c[best]
                if kk == 6:
                    cand &= parm.get(parity, 0)
                rest = allowed
                while cand:
                    low = cand & -cand; i = low.bit_length() - 1; cand ^= low
                    nw = w + C1[i]
                    if (nw[yh] > 1).any() or (nw > 3).any():
                        rest &= ~low; continue
                    chn = ch + [i]
                    if len(chn) >= 2 and not cells_ok(chn):
                        rest &= ~low; continue
                    na = rest & orth[i] & ~low
                    closed = (yh & (nw >= 1)) | (nw >= 3)
                    for b in np.nonzero(closed)[0]:
                        na &= ~item_c[b]
                    rec(chn, na, nw, parity ^ P1[i])
                    rest &= ~low
                    if found or timed[0]:
                        return
            rec([], allowed0, np.zeros(NI, dtype=np.int64), 0)
            if found:
                stats['alive'] += 1
                alive.append({'y1': k, 'y2': [int(v) for v in np.rint(y2 @ np.linalg.inv(Bf)).astype(np.int64)],
                              'h': [int(i1[i]) for i in found[0]]})
            elif timed[0]:
                stats['timeout'] += 1
                alive.append({'y1': k, 'y2': [int(v) for v in np.rint(y2 @ np.linalg.inv(Bf)).astype(np.int64)], 'timeout': True})
            else:
                stats['dead'] += 1
        stats['y1_done'] += 1
        stats['seconds'] = round(time.time() - t0, 1)
        print(json.dumps({'y1': k, 'pairs_so_far': stats['pairs'], 'dead': stats['dead'], 'alive': stats['alive'],
                          'timeout': stats['timeout'], 's': stats['seconds']}), flush=True)
        json.dump({'stats': stats, 'alive_or_timeout': alive}, open(outp, 'w'))
    stats['complete'] = stats['y1_done'] == (hi - lo) and 'truncated_y2_at' not in stats
    stats['verdict'] = ('ALL PAIRS DEAD in this y1 range' if stats['complete'] and stats['alive'] == 0 and stats['timeout'] == 0
                        else 'open')
    json.dump({'stats': stats, 'alive_or_timeout': alive}, open(outp, 'w'))
    print(json.dumps(stats), flush=True)


if __name__ == '__main__':
    main()
