"""Check the NEW global completion certificates without the constructor.

This does not rerun old C1, BvLS or border-catalogue audits. It checks
the saved rational identities of the new elimination criterion.
"""
from pathlib import Path
import argparse
import json
import sympy as sp


def check(path):
    data=json.loads(path.read_text())
    B,D,E0,P,Q,E=[sp.Matrix(data[key]).applyfunc(sp.Rational) for key in ('B','D','E0','P','Q','E')]
    n,m=D.shape;k=data['k'];mu=data['mu'];r=sp.Rational(data['r']);s=sp.Rational(data['s'])
    assert D*sp.ones(m,1)==k*sp.ones(n,1)-B*sp.ones(n,1)
    assert D*D.T==(k-mu)*sp.eye(n)+mu*sp.ones(n)-B-B*B
    assert any(sum(B.row(i))==k for i in range(n))
    assert D*E0==mu*sp.ones(n,m)-(B+sp.eye(n))*D
    assert E0==E0.T and E0*P==sp.zeros(m)
    assert P==P.T and P*P==P and D*P==sp.zeros(n,m)
    assert P*sp.ones(m,1)==sp.zeros(m,1)
    assert P.trace()==data['nullity']
    assert Q==Q.T and Q*Q==Q and P*Q==Q
    assert E==E0+r*P+(s-r)*Q
    assert E0*E0+E0+D.T*D==(k-mu)*(sp.eye(m)-P)+mu*sp.ones(m)
    assert E*sp.ones(m,1)==k*sp.ones(m,1)-D.T*sp.ones(n,1)
    assert E*E+E+D.T*D==(k-mu)*sp.eye(m)+mu*sp.ones(m)
    assert all(x.is_Integer for x in E)
    for i in range(m):
        terms=[E[i,i]**2]+[E[i,j]*(E[i,j]-1) for j in range(m) if j!=i]
        assert all(x>=0 for x in terms) and sum(terms)==0
    if 'other_projector_zero_matrix' in data:
        alternative=sp.Matrix(data['other_projector_zero_matrix']).applyfunc(sp.Rational)
        assert alternative==E0+r*P
        assert alternative*alternative+alternative+D.T*D==(k-mu)*sp.eye(m)+mu*sp.ones(m)
        assert alternative*sp.ones(m,1)==k*sp.ones(m,1)-D.T*sp.ones(n,1)
        assert not all(x.is_Integer for x in alternative)
    return dict(name=data['name'],nullity=data['nullity'],status='PASS')


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('folder',type=Path);args=ap.parse_args()
    cases=[check(args.folder/(name+'.json')) for name in ('rook_singular','rook_injective','bvls_missing39')]
    report=dict(status='PASS',cases=cases,scope='New exact closure identities only; no C1 exclusion')
    (args.folder/'independent_check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report),flush=True)
