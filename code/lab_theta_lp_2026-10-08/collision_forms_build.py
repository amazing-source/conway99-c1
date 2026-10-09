"""C1, lab session, 2026-10-09. Codex's collision bounds for the sub-collection "sums 0, +3, -3" (its note 226 and its
message of 00:07 UTC), written as affine forms of my 549 census parameters, for the coupled LP of lp_family.py.
  python collision_forms_build.py <census2 order-10 json> <codex mass-9 json> <out json>
All bounds are conditional on P = 0 and count unordered pairs of representatives with the same projection:
  C7 <= 5402 H,  H = number of induced copies of D (order 7, 11 edges, degrees 4333333; Codex's note 181);
  C8 <= 872, 816, 2840 per cubic support of order 8 and 2836, 3312, 4448 per support with 13 edges ("new", uses the
        lemma that a class of equal projection contains at most one weighted windmill; no constant), and the earlier form
        1872, 1840, 3088, 3512, 3616, 4448 plus the constant 2592 x 3465 ("old");
  C9 <= sum of integer_coefficient x number of induced copies over the types of the mass-9 file.
Codex's code of a graph on n vertices: adjacency read row by row above the diagonal, first pair in the least significant
bit. The translation is exact (rational); nothing is solved here."""
import sys, json, os, importlib.util
from fractions import Fraction as Fr
spec = importlib.util.spec_from_file_location("census2", os.path.join(os.path.dirname(os.path.abspath(__file__)), "census2.py")); c2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
C = json.load(open(sys.argv[1])); B = json.load(open(sys.argv[2])); tmap = {n: {t[0]: t for t in C["types"][str(n)]} for n in range(6, 11)}
def decode(code, n):
    rows = [0] * n; k = 0
    for i in range(n):
        for j in range(i + 1, n):
            if (code >> k) & 1: rows[i] |= 1 << j; rows[j] |= 1 << i
            k += 1
    assert code >> k == 0, "code too long for this order"
    return rows
def copies(n, code):
    rows = decode(code, n); t = tmap[n][c2.canon(n, rows)[0]]; aut = t[2] if t[2] is not None else c2.aut_order(n, t[1])
    return {p: Fr(v) / aut for p, v in t[3].items()}, sum(bin(r).count("1") for r in rows) // 2, sorted(bin(r).count("1") for r in rows)
def lin(terms):
    out = {}
    for n, code, w in terms:
        f, e, deg = copies(n, code)
        for p, v in f.items(): out[p] = out.get(p, Fr(0)) + Fr(w) * v
    return out
isD = [t for t in C["types"]["7"] if sorted(bin(r).count("1") for r in t[1]) == [3, 3, 3, 3, 3, 3, 4]]; assert len(isD) == 1   # D of Codex's note 181: the only admissible type of order 7 with minimum degree 3
autD = isD[0][2] if isD[0][2] is not None else c2.aut_order(7, isD[0][1]); fD = {p: Fr(v) / autD for p, v in isD[0][3].items()}; print("H = number of copies of D:", {p: str(v) for p, v in fD.items()})
NEW = {2022000: 872, 5683824: 816, 5691760: 2840, 127305925: 2836, 128354469: 3312, 245715219: 4448}
OLD = {2022000: 1872, 5683824: 1840, 5691760: 3088, 127305925: 3512, 128354469: 3616, 245715219: 4448}
for code in NEW:
    f, e, deg = copies(8, code); print("order-8 type %d: %d edges, degrees %s" % (code, e, "".join(map(str, deg)))); assert min(deg) >= 3 and e in (12, 13)
C7 = {p: 5402 * v for p, v in fD.items()}; C8n = lin([(8, c, w) for c, w in NEW.items()]); C8o = lin([(8, c, w) for c, w in OLD.items()]); C8o["0"] = C8o.get("0", Fr(0)) + 2592 * 3465
C9 = lin([(9, c["code"], c["integer_coefficient"]) for c in B["coefficients"]])
def tot(*fs):
    out = {}
    for f in fs:
        for p, v in f.items(): out[p] = out.get(p, Fr(0)) + v
    return out
S = lambda f: {"form": {p: str(v) for p, v in f.items() if v}}
counts = {"H": S(fD)}
for code in NEW: counts["n8_%d" % code] = S(copies(8, code)[0])
for e_ in (14, 15, 16): counts["C9_e%d" % e_] = S(lin([(9, c["code"], c["integer_coefficient"]) for c in B["coefficients"] if c["edges"] == e_]))
json.dump({"what": "Codex's collision bounds at P = 0 in the census parameters of census2.py (key '0' = constant)",
           "C7": S(C7), "C8new": S(C8n), "C8old": S(C8o), "C9": S(C9), "C7+C8new": S(tot(C7, C8n)), "C7+C8new+C9": S(tot(C7, C8n, C9)), "C7+C8old+C9": S(tot(C7, C8o, C9)), **counts}, open(sys.argv[3], "w"))
print("mass-9 types translated: %d; forms written: C7, C8new, C8old, C9, C7+C8new, C7+C8new+C9, C7+C8old+C9" % len(B["coefficients"]))
