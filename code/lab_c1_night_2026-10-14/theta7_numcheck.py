"""Independent numerical check of the W_7 matrix of theta7_lp.py on the whole 15-dimensional space: for every basis
form F_i and several points t of the upper half plane,
    (sqrt7 t)^(-22) F_i(-1/(7t))  ==  sum_j Wm[j][i] F_j(t)
evaluated from the q-expansions (q = exp(2 pi i t), 60 terms; points chosen so that both t and -1/(7t) have
imaginary part >= 0.25, truncation error < 1e-30 relative to the terms kept)."""
import cmath
import theta7_lp as T

pts = [0.05 + 0.45j, -0.11 + 0.5j, 0.2 + 0.42j, 1j / 7 ** 0.5]


def val(coeffs, t):
    q = cmath.exp(2j * cmath.pi * t)
    s = 0
    qn = 1
    for a in coeffs:
        s += a * qn
        qn *= q
    return s


worst = 0.0
for t in pts:
    t2 = -1 / (7 * t)
    assert t.imag > 0.24 and t2.imag > 0.24, (t, t2)
    F = [val(T.bvecs[i], t) for i in range(15)]
    F2 = [val(T.bvecs[i], t2) for i in range(15)]
    for i in range(15):
        lhs = (7 ** 0.5 * t) ** (-22) * F2[i]
        rhs = sum(float(T.Wm[j][i]) * F[j] for j in range(15))
        rel = abs(lhs - rhs) / max(abs(lhs), abs(rhs), 1e-300)
        worst = max(worst, rel)
print("largest relative discrepancy over 15 basis forms and %d points: %.2e" % (len(pts), worst))

# high-precision version on the imaginary axis (q real), exact rational W entries, 80 digits
from decimal import Decimal, getcontext
getcontext().prec = 80
PI = Decimal("3.14159265358979323846264338327950288419716939937510582097494459230781640628620899863")
SQ7 = Decimal(7).sqrt()
worst = Decimal(0)
for y in (Decimal("0.5"), Decimal("0.42"), Decimal("0.61")):
    y2 = 1 / (7 * y)
    q, q2 = (-2 * PI * y).exp(), (-2 * PI * y2).exp()
    F = [sum(Decimal(a) * q ** n for n, a in enumerate(T.bvecs[i])) for i in range(15)]
    F2 = [sum(Decimal(a) * q2 ** n for n, a in enumerate(T.bvecs[i])) for i in range(15)]
    for i in range(15):
        lhs = -(SQ7 * y) ** (-22) * F2[i]
        rhs = sum(Decimal(T.Wm[j][i].numerator) / Decimal(T.Wm[j][i].denominator) * F[j] for j in range(15))
        rel = abs(lhs - rhs) / max(abs(lhs), abs(rhs))
        worst = max(worst, rel)
print("high precision (80 digits, imaginary axis, 3 points): largest relative discrepancy %.3e" % float(worst))
