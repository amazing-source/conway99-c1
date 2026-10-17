"""Finite certificates for local transport-window obstructions (note 238).

Six-centre windows: only two centre graphs survive local counts and PSD;
one is excluded by exterior moments. Seven-centre windows with one extra
lateral edge: six necessary types remain. Overlap excludes eight-centre
windows with at most one lateral edge. --check uses only integer arithmetic
and exhaustive, small finite lists; no eigensolver or LP is called.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path

import networkx as nx
import numpy as np

from twisted_prism_extension import projectors, certify_infeasible, verify_certificate


ROOT = Path(__file__).resolve().parents[2]
A6 = [(1, 5), (2, 4), (2, 6), (3, 5)]
B6 = [(1, 4), (1, 6), (2, 5), (3, 6)]
P7 = [(1, 4), (1, 6), (2, 5), (2, 7), (3, 6), (4, 7)]
C8 = P7 + [(3, 8), (5, 8)]


def base_window(m):
    n = 3*m+2
    a = np.zeros((n, n), dtype=np.int64)
    for i in range(m):
        for off in (0, m+1):
            for u, v in combinations((off+i, off+i+1, 2*(m+1)+i), 2):
                a[u, v] = a[v, u] = 1
    return a


def centre_pairs(m):
    start = 2*(m+1)
    return [(start+i, start+j) for i, j in combinations(range(m), 2) if j-i >= 2]


def centre_bits(m, edges):
    return sum(1 << centre_pairs(m).index((2*m+1+i, 2*m+1+j)) for i, j in edges)


def matrix(m, bits=0, lateral=None):
    a = base_window(m)
    for k, (u, v) in enumerate(centre_pairs(m)):
        if bits >> k & 1:
            a[u, v] = a[v, u] = 1
    if lateral is not None:
        u, v = lateral
        a[u, v] = a[v, u] = 1
    return a


def local_ok(a):
    return not np.any((a@a+a)[~np.eye(len(a), dtype=bool)] > 2)


def negative_witness(a):
    for k, (gram, *_) in enumerate(projectors(a, 14)):
        values, vectors = np.linalg.eigh(gram.astype(float))
        if values[0] >= -1e-8:
            continue
        for scale in (10, 100, 1000, 10000, 1000000):
            w = np.rint(scale*vectors[:, 0]).astype(np.int64)
            q = int(w@gram@w)
            if q < 0:
                return {"projector": k, "vector": w.tolist(), "quadratic_value": q}
        raise RuntimeError("Numerical negative eigenvalue without integer witness")
    return None


def check_negative(a, witness):
    gram = projectors(a, 14)[witness["projector"]][0]
    w = np.array(witness["vector"], dtype=np.int64)
    q = int(w@gram@w)
    assert q < 0
    if "quadratic_value" in witness:
        assert q == witness["quadratic_value"]


class WitnessPool:
    """Reuse integer separating vectors; each form is affine in the edges."""
    def __init__(self, m, records):
        self.m, self.records = m, records
        self.base = base_window(m)
        self.pairs = centre_pairs(m)
        self._refresh()

    def _refresh(self):
        n = len(self.base)
        self.w = np.array([r["vector"] for r in self.records], dtype=np.int64).reshape(-1, n)
        self.factor = np.array([-18 if r["projector"] == 0 else 22 for r in self.records], dtype=np.int64)
        self.value = np.array([int(w@projectors(self.base, 14)[r["projector"]][0]@w)
                               for w, r in zip(self.w, self.records)], dtype=np.int64)
        self.weights = np.array([self.factor*self.w[:, u]*self.w[:, v]
                                 for u, v in self.pairs], dtype=np.int64)

    def find(self, a, bits, lateral=None):
        q = self.value.copy()
        for k in range(len(self.pairs)):
            if bits >> k & 1:
                q += self.weights[k]
        if lateral is not None:
            q += self.factor*self.w[:, lateral[0]]*self.w[:, lateral[1]]
        negative = np.flatnonzero(q < 0)
        if len(negative):
            return int(negative[0])
        new = negative_witness(a)
        if new is None:
            return None
        new.pop("quadratic_value")
        self.records.append(new)
        self._refresh()
        return len(self.records)-1


def exterior_model(a):
    n = len(a)
    deficit = 2-a-a@a
    compatible = nx.Graph()
    compatible.add_nodes_from(range(n))
    compatible.add_edges_from((i, j) for i, j in combinations(range(n), 2) if deficit[i, j] > 0)
    bs = [np.zeros(n, dtype=np.int64)]
    for clique in nx.enumerate_all_cliques(compatible):
        b = np.zeros(n, dtype=np.int64)
        b[clique] = 1
        if len(clique) <= 14 and np.all(b@a <= 2-b):
            bs.append(b)
    bs = np.array(bs)
    pairs = list(combinations(range(n), 2))
    rows = ([np.ones(len(bs), dtype=np.int64)] + [bs[:, i] for i in range(n)]
            + [bs[:, i]*bs[:, j] for i, j in pairs])
    rhs = np.r_[99-n, 14-a.sum(axis=1), [deficit[i, j] for i, j in pairs]].astype(np.int64)
    return np.array(rows), rhs, np.full(len(bs), 99-n, dtype=np.int64)


def lateral_orbits(m):
    a = base_window(m)
    def swap(u):
        return u+m+1 if u < m+1 else u-m-1 if u < 2*(m+1) else u
    def reverse(u):
        return m-u if u < m+1 else 3*m+2-u if u < 2*(m+1) else 5*m+3-u
    actions = (lambda u: u, swap, reverse, lambda u: swap(reverse(u)))
    reps = {}
    for u, v in combinations(range(len(a)), 2):
        if u >= 2*(m+1) or a[u, v]:
            continue
        rep = min(tuple(sorted((f(u), f(v)))) for f in actions)
        reps[rep] = reps.get(rep, 0)+1
    return reps


def build_or_check(report, check):
    six = report.setdefault("six_centre_psd", {})
    pools = report.setdefault("witness_pools", {"6": [], "7": []})
    six_pool = WitnessPool(6, pools["6"])
    six_left = []
    for bits in range(1 << len(centre_pairs(6))):
        a = matrix(6, bits)
        if not local_ok(a):
            continue
        if check:
            index = six.get(str(bits))
        else:
            index = six_pool.find(a, bits)
            if index is not None:
                six[str(bits)] = index
        if index is not None:
            check_negative(a, pools["6"][index])
        else:
            six_left.append(bits)
    assert set(six_left) == {centre_bits(6, A6), centre_bits(6, B6)}
    m, rhs, upper = exterior_model(matrix(6, centre_bits(6, A6)))
    if not check:
        report["six_A_exterior"] = certify_infeasible(m, rhs, upper)
    assert report["six_A_exterior"]
    verify_certificate(m, rhs, upper, report["six_A_exterior"])

    # No lateral edge on a seven-centre window: overlapping B6 windows.
    seven = matrix(7, centre_bits(7, P7))
    seven_extra = seven.copy()
    seven_extra[16, 22] = seven_extra[22, 16] = 1
    assert not local_ok(seven_extra)
    if not check:
        report["seven_no_lateral"] = negative_witness(seven)
    check_negative(seven, report["seven_no_lateral"])

    # Exactly one lateral edge, up to reversal and global rail exchange.
    seven_psd = report.setdefault("seven_one_lateral_psd", {})
    seven_pool = WitnessPool(7, pools["7"])
    candidates = [(bits, matrix(7, bits)) for bits in range(1 << len(centre_pairs(7)))]
    candidates = [(bits, a) for bits, a in candidates if local_ok(a)]
    assert len(candidates) == 1089
    before_exterior = []
    for edge in sorted(lateral_orbits(7)):
        for bits, base in candidates:
            a = base.copy()
            a[edge[0], edge[1]] = a[edge[1], edge[0]] = 1
            if not local_ok(a):
                continue
            key = f"{edge[0]},{edge[1]}:{bits}"
            index = seven_psd.get(key) if check else seven_pool.find(a, bits, edge)
            if index is not None:
                check_negative(a, pools["7"][index])
                if not check:
                    seven_psd[key] = index
            else:
                before_exterior.append((key, edge, bits, a))
    assert len(before_exterior) == 14
    if not check:
        pilot = json.loads((ROOT/"data/codex_ribbon7_one_lateral_extensions.json").read_text())
        report["seven_exterior"] = {
            f"{x['lateral_edge'][0]},{x['lateral_edge'][1]}:{x['center_bits']}": x["certificate"]
            for x in pilot["records"] if x.get("certificate")
        }
    left = []
    for key, edge, bits, a in before_exterior:
        cert = report["seven_exterior"].get(key)
        if cert:
            m, rhs, upper = exterior_model(a)
            verify_certificate(m, rhs, upper, cert)
        else:
            left.append((edge, bits))
    expected = [((u, v), centre_bits(7, P7))
                for u, v in ((1, 5), (1, 6), (1, 13), (1, 14), (2, 5), (2, 13))]
    assert sorted(left) == sorted(expected)

    # In two overlapping seven-centre windows the only common lateral
    # column pair is (3,7); the centre graph is C8, optionally with (1,8).
    positions = {(2, 6), (3, 7), (2, 7), (3, 6)}
    assert positions & {(i+1, j+1) for i, j in positions} == {(3, 7)}
    eight = report.setdefault("eight_one_lateral", {})
    for cross in (0, 1):
        for outer in (0, 1):
            edges = C8 + ([(1, 8)] if outer else [])
            a = matrix(8, centre_bits(8, edges), (2, 6+9*cross))
            key = f"{cross},{outer}"
            if not check:
                eight[key] = negative_witness(a)
            check_negative(a, eight[key])
    report["summary"] = {
        "six_centre_subsets": 1024,
        "six_spectral_exclusions": len(six),
        "six_remaining_after_exterior": "B6 only",
        "seven_lateral_position_orbits": len(lateral_orbits(7)),
        "seven_combinatorial_centre_graphs": len(candidates),
        "seven_spectral_exclusions": len(seven_psd),
        "integer_vector_pool_sizes": {key: len(value) for key, value in pools.items()},
        "seven_before_exterior": 14,
        "seven_exterior_exclusions": len(report["seven_exterior"]),
        "seven_remaining_necessary_types": 6,
        "eight_final_spectral_exclusions": 4,
        "conclusion": "Every eight-centre window has a role identification or at least two extra lateral edges",
    }
    return report


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--out", type=Path, default=ROOT/"data/codex_ribbon_window_obstructions.json")
    args = ap.parse_args()
    report = json.loads(args.out.read_text(encoding="utf-8")) if args.check else {
        "scope": "local transport windows with arbitrary centre edges; not a proof of C1",
    }
    report = build_or_check(report, args.check)
    if not args.check:
        args.out.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))
    print("All exclusions checked using integer witnesses.")


if __name__ == "__main__":
    main()
