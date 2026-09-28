"""All-dis family (B) = seven free stars: full orbit model (orbit_sat.build) + D(U) in a disjoint cell for EVERY U.
WLOG D(U0) = (3,4,0) (Stab(U0) is transitive on the 20 orbits of cells disjoint from {1,2}). Probe with a time cap."""
import sys, time, threading
sys.path.insert(0, 'C:/home/researcher/Desktop/conway99-involution/code/z2')
from orbit_sat import build, lift
from pysat.solvers import Solver
T = float(sys.argv[1]) if len(sys.argv) > 1 else 300
t0 = time.time()
cnf, pool, outer, rep, trep, A, B = build(7, "dis")
N = len(outer); extra = 0
for U in range(N):
    for V in range(U + 1, N):
        cu = {outer[U][0], outer[U][1]}; cv = {outer[V][0], outer[V][1]}
        if cu & cv:                                   # not disjoint: never a double edge
            cnf.append([-A[U, V], -B[U, V]]); extra += 1
print('vars', pool.top, 'clauses', len(cnf.clauses), 'all-dis clauses', extra, 'build %.1fs' % (time.time() - t0), flush=True)
with Solver(name='cadical195', bootstrap_with=cnf.clauses) as s:
    timer = threading.Timer(T, s.interrupt); timer.start()
    r = s.solve_limited(expect_interrupt=True); timer.cancel()
    print('RESULT', r, 'solve %.1fs' % (time.time() - t0), s.accum_stats(), flush=True)
    if r:
        M, ok = lift(7, outer, rep, trep, A, B, s.get_model()); print('LIFT srg identity:', ok, flush=True)
        import numpy as np; np.savetxt('alldis_solution.txt', M, fmt='%d')
