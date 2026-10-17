"""Read exact affine certificates; check the new reduction and its parity example."""
from pathlib import Path
from itertools import product
import json
import argparse
import sympy as sp


def verify(folder):
    reports = []
    for name in ('rook', 'petersen', 'paley13', 'paley17'):
        obj = json.loads((folder/(name+'.json')).read_text(encoding='utf-8'))
        B, D, base = (sp.Matrix(obj[key]) for key in ('B', 'D', 'base'))
        N = sp.Matrix(obj['kernel']) if obj['nullity'] else sp.zeros(D.cols, 0)
        basis = [sp.Matrix(T) for T in obj['basis']]
        chosen = [tuple(p) for p in obj['selected_pairs']]
        k, mu = obj['k'], obj['mu']; n, m = D.shape; h = N.cols
        F = mu*sp.ones(n, m)-(B+sp.eye(n))*D
        assert D*D.T == (k-mu)*sp.eye(n)+mu*sp.ones(n)-B-B*B
        assert any(sum(B.row(i)) == k for i in range(n))
        assert D*N == sp.zeros(n, h) and N.rank() == h and h == m-D.rank()
        pairs = [(a, b) for a in range(h) for b in range(a, h)]
        diagonal = sp.Matrix(m, len(pairs), lambda i, j:
            N[i, pairs[j][0]]*N[i, pairs[j][1]]*(1 if pairs[j][0] == pairs[j][1] else 2))
        delta = len(pairs)-diagonal.rank()
        assert delta == len(basis) == len(chosen) == obj['dimension']
        assert delta <= h*(h-1)//2
        assert base == base.T and D*base == F and all(base[i, i] == 0 for i in range(m))
        for a, T in enumerate(basis):
            assert T == T.T and D*T == sp.zeros(n, m) and all(T[i, i] == 0 for i in range(m))
            assert [T[u, v] for u, v in chosen] == [int(a == b) for b in range(delta)]
        exact_solutions = []
        truth = []
        assert delta <= 3
        for bits in product((0, 1), repeat=delta):
            E = base+sum((x*T for x, T in zip(bits, basis)), sp.zeros(m))
            binary = all(x in (0, 1) for x in E)
            if not binary: continue
            A = B.row_join(D).col_join(D.T.row_join(E))
            assert A*sp.ones(n+m, 1) == k*sp.ones(n+m, 1)
            residual = A*A+A-(k-mu)*sp.eye(n+m)-mu*sp.ones(n+m)
            L = residual[n:, n:]
            assert residual[:n, :] == sp.zeros(n, n+m)
            assert D*L == sp.zeros(n, m) and all(L[i, i] == 0 for i in range(m))
            selected_zero = all(L[u, v] == 0 for u, v in chosen)
            full_zero = residual == sp.zeros(n+m)
            assert selected_zero == full_zero
            if full_zero: exact_solutions.append(E)
            truth.append(dict(free=list(bits), complete_graph=full_zero,
                              selected_defects=[int(L[u, v]) for u, v in chosen]))
        claimed = [sp.Matrix(E) for E in obj['completions']]
        assert len(claimed) == len(exact_solutions) and all(E in claimed for E in exact_solutions)
        if name == 'petersen':
            assert len(truth) == 8
            for row in truth:
                x, y, z = row['free']
                assert row['selected_defects'] == [x-y-z+2*y*z, y-x-z+2*x*z, z-x-y+2*x*y]
                assert row['complete_graph'] == (sum(row['free']) % 2 == 0)
            (folder/'petersen_parity_certificate.json').write_text(json.dumps(dict(
                selected_pairs=chosen, identity='x + y + z = 0 (mod 2)',
                selected_integer_polynomials=['x-y-z+2*y*z', 'y-x-z+2*x*z', 'z-x-y+2*x*y'],
                truth_table=truth,
                scope='Illustrates exact coexistence extraction on a known graph; not a Conway exclusion'),
                indent=2)+'\n', encoding='utf-8')
        reports.append(dict(name=name, nullity=h, affine_dimension=delta,
                            boolean_linear_candidates=len(truth), full_completions=len(exact_solutions)))
    report = dict(status='PASS', controls=reports,
                  verified='Rational affine dimension, defect containment, exhaustive free-edge cases and all graph identities')
    (folder/'independent_check.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('folder', type=Path)
    verify(parser.parse_args().folder)
