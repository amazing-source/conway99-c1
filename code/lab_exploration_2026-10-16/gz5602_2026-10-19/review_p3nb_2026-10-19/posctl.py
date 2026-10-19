import json, sys
sys.path.insert(0, sys.argv[2])
from indep_model import setup, constraints_on_witness, solve
d = json.load(open(sys.argv[1]))
GR = [(1, 2), (3, 4), (5, 6)]
K, O = setup(GR)
assert [list(q) for q in K] == d["known_labels"], "known order"
A = d["rows"]
X = {}
for q, prof in zip(d["outside_labels"], d["selected_profiles"]):
    for u in prof: X[tuple(q), u] = 1
assert sorted(tuple(q) for q in d["outside_labels"]) == sorted(O)
bad = constraints_on_witness(GR, A, X)
print("witness violations of my exact constraints:", len(bad), bad[:10])
r, ncl, model = solve(GR, A)
print("my SAT model on 2K2 positive control:", r, "clauses", ncl)
if model:
    X2 = {k: v for k, v in model.items() if v}
    print("my model's own solution re-checked:", len(constraints_on_witness(GR, A, X2)))
