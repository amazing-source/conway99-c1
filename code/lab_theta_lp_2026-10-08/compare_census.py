"""C1, lab session, 2026-10-08. Compare my independent census (census2.py, JSON output) with Codex's packet (note 184).
  python -I compare_census.py <census2 json> <codex packet json>
Both give, for every admissible type, the number of induced copies as an affine form in the numbers of copies of the
types of minimum degree >= 3. Types and parameters are matched by my canonical form of the adjacency rows given in the
packet (read as data). Every coefficient is compared exactly."""
import sys, json
from fractions import Fraction as Fr
sys.path.insert(0, __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0])
import census2 as C2
mine = json.load(open(sys.argv[1])); cod = json.load(open(sys.argv[2]))
assert cod["srg_parameters"][:2] == [mine["v"], mine["k"]]
pid = {(n, key): i + 1 for i, (n, key, rows) in enumerate(mine["params"])}
tab = {}
for n, lst in mine["types"].items():
    for key, rows, aut, form in lst: tab[(int(n), key)] = {int(p): Fr(val) / aut for p, val in form.items()}
tot = bad = 0; pmap = {}
for st in cod["stages"]:
    for g in st["new_parameter_graphs"]:
        rows = g["adjacency_bits"]; key, _ = C2.canon(len(rows), rows); assert (len(rows), key) in pid, ("a Codex parameter is not a minimum-degree-3 type of mine", g["name"]); pmap[g["name"]] = pid[(len(rows), key)]
for st in cod["stages"]:
    n = st["order"]; names = st["parameters"]; seen = set()
    for c in st["counts"]:
        rows = c["adjacency_bits"]; key, _ = C2.canon(n, rows); assert (n, key) in tab, ("type of the packet unknown to my census", n, c["code"]); assert key not in seen; seen.add(key)
        theirs = {0: Fr(c["affine"][0])}
        for nm, val in zip(names, c["affine"][1:]):
            if Fr(val): theirs[pmap[nm]] = Fr(val)
        theirs = {p: x for p, x in theirs.items() if x}; ours = {p: x for p, x in tab[(n, key)].items() if x}; tot += 1
        if theirs != ours:
            bad += 1
            if bad <= 5: print("MISMATCH order %d code %s: codex %s / mine %s" % (n, c["code"], theirs, ours))
    assert len(seen) == len(mine["types"][str(n)]) == st["graph_types"], (n, len(seen), len(mine["types"][str(n)]))
    print("order %d: %d types, all matched one to one" % (n, len(seen)), flush=True)
print("parameters matched: %d (of %d in my census)" % (len(pmap), len(pid)))
print("formulas compared: %d; mismatches: %d" % (tot, bad))
