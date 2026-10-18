"""Necessary test of the letter-swap equivariance of Codex's complete-star model (LAB, 18/10/2026).
For a template, its star line r0 and a star matching M, build the model for M and for sigma(M), where sigma is the
label permutation induced by exchanging the two letters 2j <-> 2j+1 of a line j != r0.  If the model generator has
no labelling-dependent normalisation, the two models are isomorphic; a necessary condition, tested here, is that their
multisets of constraint signatures (type, sorted coefficients, domain, number of variables, enforcement count) and of
variable domains coincide.  A difference proves non-equivariance; equality is evidence, not a proof.
usage: python equivariance_test.py <package dir> <catalogue> <template index> <matching index> [--transport]"""
import json
import sys
from collections import Counter
from pathlib import Path

pkg, cat, ti, mi = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
transport = "--transport" in sys.argv
sys.path.insert(0, str(Path(pkg) / "code" / "codex"))
import root_component_complete_star as CS                # noqa: E402
from root_component_propagation import LABELS            # noqa: E402

template, _, _ = CS.load_template(Path(cat), ti)
root, parts, counts, cover = CS.matching_cover(template)
M = cover[mi]
lookup = {tuple(p): w for w, p in enumerate(LABELS)}


def signature(model):
    """Multisets, invariant under a renaming of the variables: variable domains, and for every constraint its kind,
    number of enforcement literals, sorted coefficients, domain, numbers of variables and of positive/negative
    literals (read from the text format, variable indices dropped)."""
    p = model.proto
    var_doms = Counter(tuple(list(v.domain)) for v in p.variables)
    cons = Counter()
    for c in p.constraints:
        lines = [l.strip() for l in str(c).splitlines() if l.strip()]
        kind = next((l.split()[0] for l in lines if l.endswith("{")), "?")
        enf = sum(1 for l in lines if l.startswith("enforcement_literal:"))
        coeffs = tuple(sorted(int(l.split()[1]) for l in lines if l.startswith("coeffs:")))
        dom = tuple(int(l.split()[1]) for l in lines if l.startswith("domain:"))
        nvars = sum(1 for l in lines if l.startswith("vars:"))
        lits = [int(l.split()[1]) for l in lines if l.startswith("literals:")]
        values = sum(1 for l in lines if l.startswith("values:"))
        cons[(kind, enf, coeffs, dom, nvars, sum(1 for x in lits if x >= 0), sum(1 for x in lits if x < 0), values,
              sum(1 for l in lines if l.endswith("{")))] += 1
    return var_doms, cons


base_model, _, base_info = CS.build_branch(template, root, M, 2, transport, False)
base = signature(base_model)
print(json.dumps({"template": ti, "root": root, "parts": [len(x) for x in parts], "matching": mi,
                  "variables": len(base_model.proto.variables), "constraints": len(base_model.proto.constraints)}))
for j in range(7):
    if j == root:
        continue
    def swap_letter(a):
        return a ^ 1 if a // 2 == j else a
    sigma = {w: lookup[tuple(sorted((swap_letter(a), swap_letter(b))))] for w, (a, b) in enumerate(LABELS)}
    Ms = tuple(sorted(tuple(sorted((sigma[u], sigma[v]))) for u, v in M))
    in_cover = Ms in set(cover)
    model, _, info = CS.build_branch(template, root, Ms, 2, transport, False)
    sig = signature(model)
    print(json.dumps({"swap_line": j, "image_in_cover": in_cover, "image_index": cover.index(Ms) if in_cover else None,
                      "same_variable_domains": sig[0] == base[0], "same_constraint_signatures": sig[1] == base[1],
                      "variables": len(model.proto.variables), "constraints": len(model.proto.constraints)}), flush=True)
