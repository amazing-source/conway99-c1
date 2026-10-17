"""Exact cubic inputs for the class-separated theta route (note 241).

Uses only integers and fractions. Produces the A8 coset theta series
weighted by 81*sum(y_i**3), through q^32, and the small-profile weights
for 3*sum(x_v**3) on the -1/3 coordinate class in V_-4.
Does not solve a modular feasibility programme or exclude a rank.
"""
from collections import defaultdict
from fractions import Fraction as F
from math import comb, isqrt
from pathlib import Path
import json


def a8_odd(qmax=32):
    # y=m-k/9*1, sum(m)=k. Then norm(y)=sum(m_i^2)-k^2/9.
    max_square = 2*qmax+64//9
    values = range(-isqrt(max_square), isqrt(max_square)+1)
    dp = {(0, 0): (1, 0)}
    for _ in range(9):
        nxt = defaultdict(lambda: [0, 0])
        for (s, square), (count, cube_sum) in dp.items():
            for v in values:
                sq = square+v*v
                if sq > max_square:
                    continue
                row = nxt[s+v, sq]
                row[0] += count
                row[1] += cube_sum+v*v*v*count
        dp = nxt
    series = []
    for k in range(9):
        rows = []
        for square in range(max_square+1):
            exponent = F(9*square-k*k, 18)
            if exponent < 0 or exponent > qmax:
                continue
            count, cube_sum = dp.get((k, square), (0, 0))
            if not count:
                continue
            weight81 = 81*cube_sum-27*k*square*count+2*k**3*count
            rows.append({"exponent": str(exponent), "count": count,
                         "weighted_coefficient_81": weight81})
        if k:
            first = rows[0]
            assert first["exponent"] == str(F(k*(9-k), 18))
            assert first["count"] == comb(9, k)
            assert first["weighted_coefficient_81"] == comb(9, k)*k*(9-k)*(9-2*k)
        series.append({"class": k, "terms": rows})
    assert all(row["weighted_coefficient_81"] == 0 for row in series[0]["terms"])
    for k in range(1, 5):
        a = {r["exponent"]: r for r in series[k]["terms"]}
        b = {r["exponent"]: r for r in series[9-k]["terms"]}
        assert a.keys() == b.keys()
        assert all(a[q]["count"] == b[q]["count"] and
                   a[q]["weighted_coefficient_81"] == -b[q]["weighted_coefficient_81"]
                   for q in a)
    return series


def profiles():
    rows = []
    for norm, name, hist, expected in [
        (22, "norm22", {1: 33, 0: 66}, 22),
        (24, "norm24", {1: 34, -1: 1, 0: 64}, 16),
        (26, "norm26", {1: 35, -1: 2, 0: 62}, 10),
        (28, "A", {1: 36, -1: 3, 0: 60}, 4),
        (28, "B", {1: 33, 2: 1, -1: 2, 0: 63}, 22),
        (28, "C", {1: 35, -2: 1, 0: 63}, -14),
    ]:
        assert sum(hist.values()) == 99
        assert sum(n*(F(v)-F(1, 3)) for v, n in hist.items()) == 0
        assert sum(n*(F(v)-F(1, 3))**2 for v, n in hist.items()) == norm
        p3 = sum(n*(F(v)-F(1, 3))**3 for v, n in hist.items())
        assert 3*p3 == expected
        rows.append({"profile": name, "norm": norm, "histogram_phi": hist,
                     "P3": str(p3), "three_P3": expected})
    return rows


def main():
    report = {"scope": __doc__, "qmax": 32, "V_minus4_profiles": profiles(),
              "A8_odd_cosets": a8_odd(),
              "norm28_identity": "D14 = 4*N14 + 18*N_B - 396*C22",
              "norm28_bounds": ["4*N14 - 396*C22 <= D14",
                                "D14 <= 22*N14 - 4158 - 756*k - 792*C22"],
              "root_triangle_reflection": "profile A; negative triple = edge plus isolated vertex",
              "normalizations": {"V_minus4_weight": "3*P3", "A8_weight": "81*P3"}}
    path = Path(__file__).resolve().parents[2]/"data/codex_odd_theta_inputs.json"
    path.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print("Exact profile weights:", [r["three_P3"] for r in report["V_minus4_profiles"]])
    print("A8 odd cosets generated through q^32; opposite classes cancel exactly.")
    print("No modular LP run and no rank excluded.")


if __name__ == "__main__":
    main()
