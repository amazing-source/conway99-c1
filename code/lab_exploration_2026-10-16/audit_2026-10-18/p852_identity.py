"""Independent check of the identity behind P <= 852 (Codex, codex_order9_prism_cap.json): the certificate weights w_g >= 0
times the census count expressions N_g(params) must sum to exactly 11088/13 - P.  Pure Fraction arithmetic, own parser.
This checks the certificate against the census; it does NOT check the census derivation itself."""
import json, re, sys
from fractions import Fraction
cap = json.load(open(sys.argv[1]))
cen = json.load(open(sys.argv[2]))
by_code = {}
for c in cen["counts"]:
    by_code.setdefault(int(c["code"]), []).append(c)
term = re.compile(r"\s*([+-])?\s*(\d+)?\s*\*?\s*([A-Za-z_][A-Za-z0-9_]*)?\s*(?:/\s*(\d+))?")
def parse(expr):
    out, s = {}, expr.replace(" ", "")
    for m in re.finditer(r"([+-]?)([^+-]+)", s):
        sign, body = m.group(1), m.group(2)
        num, den, var = Fraction(1), 1, "1"
        parts = body.split("/")
        assert len(parts) <= 2, body
        if len(parts) == 2:
            den = int(parts[1])
        mul = parts[0].split("*")
        for f in mul:
            if re.fullmatch(r"\d+", f):
                num *= int(f)
            else:
                assert var == "1", body
                var = f
        val = num / den * (-1 if sign == "-" else 1)
        out[var] = out.get(var, 0) + val
    return out
total, neg = {}, 0
for code, w in cap["certificate"]:
    w = Fraction(w)
    neg += w < 0
    rows = by_code[int(code)]
    assert len(rows) == 1, (code, len(rows))
    for var, val in parse(rows[0]["count"]).items():
        total[var] = total.get(var, 0) + w * val
total = {k: v for k, v in total.items() if v != 0}
print("certificate terms:", len(cap["certificate"]), "negative weights:", neg)
print("sum of w_g * N_g =", {k: str(v) for k, v in sorted(total.items())})
ok = set(total) <= {"1", "P"} and total.get("P") == -1 and total.get("1") == Fraction(11088, 13)
print("IDENTITY 11088/13 - P:", ok, "| floor(11088/13) =", 11088 // 13)
