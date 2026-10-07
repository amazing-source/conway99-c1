import sys, time
from srg_moments import Hierarchy
from exact6 import nullspace_affine
n, k, lam, mu, t = map(int, sys.argv[1:6]); t0 = time.time()
H = Hierarchy(n, k, lam, mu, t, exact=True); A = H.equalities()
x0, basis = nullspace_affine(A.tolist(), len(H.top))
print(f"srg({n},{k},{lam},{mu}) order {t}: {len(H.top)} classes, {len(basis)} free parameters ({time.time() - t0:.0f}s)")
