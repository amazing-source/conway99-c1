import pickle, sys
from sympy.combinatorics import Permutation
sys.argv = [sys.argv[0]]
import importlib.util
spec = importlib.util.spec_from_file_location("pca", "parity_cms_aut.py")
src = open("parity_cms_aut.py").read().split("for key, h in reps.items():")[0]
src = src.replace("random.seed(1); reps = {}", "reps = {}\nif False:").replace("for _ in range(4000):", "  for _ in range(0):")
exec(compile(src, "pca", "exec"))
cl = pickle.load(open("oddclasses.pkl", "rb"))
for i, a in enumerate(cl["3"]):
    sat, dt = solve(Permutation(a))
    fp = sum(1 for x in range(81) if a[x] == x)
    print(f"order-3 class {i} (fixed points {fp}): {'SAT' if sat else 'UNSAT'} ({dt:.1f}s)", flush=True)
sat, dt = solve(Permutation(cl["5"])); print(f"order-5 class: {'SAT' if sat else 'UNSAT'} ({dt:.1f}s)", flush=True)
