r"""Finish line (C), C1 27/09: triage of the envelopes by the size of the y-pair enumeration (y_pairs.py).
For each id: number of W-dominant y1 (fast); if <= Y1MAX, the y2 counts per y1 within a time budget, extrapolated.
One process, sequential, results appended to a JSONL (resumable).  Usage: python y_triage.py <envdir> <out.jsonl> [ids...]"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from y_pairs import setup, dominant_y1

Y1MAX = 400
BUDGET = 40.0          # seconds of y2 enumeration per lattice


def main():
    envdir, outp = sys.argv[1], sys.argv[2]
    want = [int(a) for a in sys.argv[3:]]
    done = set()
    if os.path.exists(outp):
        for line in open(outp):
            try:
                done.add(json.loads(line)['id'])
            except Exception:
                pass
    excluded = {94, 117, 128, 129, 133, 134, 136, 142, 144, 145, 146, 147, 148, 150, 151, 152, 153, 154, 155}
    ids = want or [i for i in range(1, 156) if i not in excluded]
    for i in ids:
        if i in done:
            continue
        rec = json.load(open(os.path.join(envdir, '%03d.json' % i)))
        t0 = time.time()
        row = {'id': i, 'roots': rec['roots']}
        try:
            B, Gi, Bf, R, X3, Snew = setup(rec['gens'])
            Y, Yf, info = dominant_y1(B, Gi, Bf, R, X3, Snew)
            row.update(info)
            row['y1_s'] = round(time.time() - t0, 1)
            if 0 < len(Y) <= Y1MAX:
                from y2_engine import Y2Engine
                eng = Y2Engine(B, Gi, Bf, R, X3, Snew)
                t1 = time.time()
                npairs, done_y1 = 0, 0
                for k in range(len(Y)):
                    if time.time() - t1 > BUDGET:
                        break
                    Y2, st = eng.pairs_for(Yf[k], t0=t1, max_seconds=BUDGET)
                    if st.get('truncated'):
                        break
                    npairs += len(Y2)
                    done_y1 += 1
                row['y2_done_y1'] = done_y1
                row['pairs_partial'] = npairs
                row['pairs_extrapolated'] = int(npairs * len(Y) / max(done_y1, 1)) if done_y1 else None
                row['complete'] = done_y1 == len(Y)
        except Exception as ex:
            row['error'] = repr(ex)[:200]
        row['seconds'] = round(time.time() - t0, 1)
        with open(outp, 'a') as f:
            f.write(json.dumps(row) + '\n')
        print(json.dumps(row), flush=True)


if __name__ == '__main__':
    main()
