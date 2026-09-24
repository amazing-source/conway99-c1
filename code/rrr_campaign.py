"""Construction campaign for srg(99,14,1,2) by RRR (sequential runs, time-limited, near-misses saved).
Any hit is verified exactly and saved to data/FOUND_*.json immediately."""
import sys, time, json
import numpy as np
from rrr_srg import RRR
from rrr_rooted import RootedRRR
from near_miss import analyse

def verify(a, n, k, lam, mu):
    A = np.asarray(a, dtype=np.int64)
    return (A == A.T).all() and not A.diagonal().any() and (A.sum(1) == k).all() and \
        (A @ A + (mu - lam) * A + (mu - k) * np.eye(n, dtype=np.int64) == mu).all()

def run_one(tag, solver, n, k, lam, mu, seconds, report_every=20000):
    t0 = time.time(); it = 0; best = None; best_pa = None
    while time.time() - t0 < seconds:
        it += 1
        pb = solver.PB(solver.x)
        pa = solver.PA(2 * pb - solver.x)
        solver.x = solver.x + solver.beta * (pa - pb)
        err = float(np.abs(pa - pb).sum())
        if best is None or err < best:
            best, best_pa = err, pa.copy()
        if it % 50 == 0 or err < 1e-6:
            A = pa.astype(np.int64)
            if not (A.sum(1) == k).all():
                A = solver.PA(pb).astype(np.int64)
            if (A.sum(1) == k).all() and verify(A, n, k, lam, mu):
                fn = f'../data/FOUND_srg{n}_{tag}.json'
                json.dump(A.tolist(), open(fn, 'w'))
                print(f'*** {tag}: FOUND a verified srg({n},{k},{lam},{mu}) at iteration {it} -> {fn}', flush=True)
                return True
        if it % report_every == 0:
            print(f'   {tag}: it {it}, err {err:.1f}, best {best:.1f} ({time.time()-t0:.0f}s)', flush=True)
    json.dump(best_pa.astype(int).tolist(), open(f'../data/nearmiss_{tag}.json', 'w'))
    st = analyse(best_pa) if n == 99 else {}
    print(f'{tag}: not found in {it} its ({time.time()-t0:.0f}s); best err {best:.1f}; near-miss: '
          f"lambda viol {st.get('lambda violations (pairs)')}, mu viol {st.get('mu violations (pairs)')}, "
          f"degrees {st.get('degree hist')}, triangles {st.get('triangles')}, P {st.get('prisms P')}", flush=True)
    return False

if __name__ == '__main__':
    plan = sys.argv[1] if len(sys.argv) > 1 else 'main'
    secs = float(sys.argv[2]) if len(sys.argv) > 2 else 1800
    if plan == 'control81':
        run_one('ctrl81_b02', RRR(81, 20, 1, 6, beta=0.02, seed=0), 81, 20, 1, 6, secs)
    elif plan == 'main':
        runs = [('gen_b02_s0', lambda: RRR(99, 14, 1, 2, beta=0.02, seed=0)),
                ('root_b02_s0', lambda: RootedRRR(6, beta=0.02, seed=0)),
                ('root_noprism_b02_s0', lambda: RootedRRR(6, beta=0.02, seed=0, noprism=True)),
                ('gen_b05_s1', lambda: RRR(99, 14, 1, 2, beta=0.05, seed=1)),
                ('root_b05_s1', lambda: RootedRRR(6, beta=0.05, seed=1)),
                ('root_noprism_b05_s1', lambda: RootedRRR(6, beta=0.05, seed=1, noprism=True))]
        for tag, make in runs:
            if run_one(tag, make(), 99, 14, 1, 2, secs):
                break
