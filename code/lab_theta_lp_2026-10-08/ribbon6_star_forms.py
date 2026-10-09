"""C1, lab session, 2026-10-09. The two residual star forms of Codex's note 239 for an injective closed ribbon of
length 6 (all chords through the centre c0): {c0-a4, c0-b3} and {c0-c2, c0-c4} (0-based), and their images under the
strand exchange where it changes the form, tested with the one-vertex multiplicity system (support_masks.verdict),
exact certificate when infeasible (certify_supports.certify).      python ribbon6_star_forms.py"""
import json
import support_masks as S
import certify_supports as C
m = 6; out = {}
for MO in (False, True):
    names = ["a%d" % i for i in range(m)] + ["b%d" % i for i in range(m)] + ["c%d" % i for i in range(m)]; ix = {s: i for i, s in enumerate(names)}; E0 = []
    for i in range(m):
        if i < m - 1 or not MO: an, bn = "a%d" % ((i + 1) % m), "b%d" % ((i + 1) % m)
        else: an, bn = "b0", "a0"
        for x, y in (("c%d" % i, "a%d" % i), ("c%d" % i, an), ("a%d" % i, an), ("c%d" % i, "b%d" % i), ("c%d" % i, bn), ("b%d" % i, bn)): E0.append((ix[x], ix[y]))
    tag = "moebius" if MO else "cylinder"
    for form in ((("c0", "a4"), ("c0", "b3")), (("c0", "a3"), ("c0", "b4")), (("c0", "c2"), ("c0", "c4"))):
        E = E0 + [(ix[u], ix[v]) for u, v in form]
        r = S.verdict(len(names), E); st = r["status"]; cert = None
        if st.startswith("INFEASIBLE"): st, cert = C.certify(len(names), E)
        lab = "%s %s" % (tag, ", ".join("%s-%s" % e for e in form)); out[lab] = {"status": st, "certificate": cert}
        print("%-34s : %s%s" % (lab, st, (" (masks %d, ranks %d %d)" % (r["masks"], r["rank_minus"], r["rank_plus"])) if "masks" in r else ""), flush=True)
json.dump(out, open("ribbon6_star_forms.json", "w"))
