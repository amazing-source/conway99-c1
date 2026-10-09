"""Small exact identities used in the proof of note 237; no graph sweep."""
import json
from pathlib import Path

import sympy as s


ROOT = Path(__file__).resolve().parents[2]


def main():
    c, t, m = s.symbols("c t m")
    p = s.expand((10*c-5)**2*(1-c*c)-(3-2*c)**2)
    polynomial = s.Poly(p.subs(c, s.Rational(3, 4)+t/6), t)
    bernstein = [s.factor(sum(polynomial.nth(k)*s.binomial(j, k)/s.binomial(4, k)
                              for k in range(j+1))) for j in range(5)]
    assert bernstein == [s.Rational(n, 5184) for n in (2511, 6507, 9507, 10311, 7319)]
    assert all(x > 0 for x in bernstein)
    assert s.expand(sum(bernstein[j]*s.binomial(4, j)*t**j*(1-t)**(4-j)
                        for j in range(5))-polynomial.as_expr()) == 0
    moment_defect = s.factor(((20*m)**2-(99-3*m)*4*m*(2*m-1))/(4*m))
    assert moment_defect == 6*m*m-101*m+99
    assert moment_defect.subs(m, 16) == 19
    upper_cos = s.Rational(11, 12)
    chebyshev_gap = s.factor(16*upper_cos**5-20*upper_cos**3+5*upper_cos+s.Rational(1, 2))
    assert chebyshev_gap == s.Rational(527, 15552)
    out = {
        "scope": "closed transport ribbons with distinct roles and extra edges only between centres",
        "conclusion": "length <= 8",
        "proof": "notes/237_CODEX_RUBANS_REPARES_PAR_CENTRES.md",
        "moment_polynomial": str(moment_defect),
        "moment_polynomial_at_16": 19,
        "spectral_polynomial": str(p),
        "interval": ["3/4", "11/12"],
        "positive_bernstein_coefficients": [str(x) for x in bernstein],
        "upper_cosine_bound_chebyshev_gap": str(chebyshev_gap),
        "solver_used": False,
        "all_transport_cycles_bounded": False,
    }
    (ROOT / "data/codex_center_repaired_ribbons.json").write_text(
        json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
