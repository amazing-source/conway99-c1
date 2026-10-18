"""Compare compressed pair formulas with full exact projector matrices."""
import argparse
from itertools import combinations
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import sympy as sp
from root_component_resources import atomic_json_write, limit_research_process
from root_component_propagation import LABELS, PAIRS, RECTANGLES
from root_component_signature_moments import gram_matrix
from root_component_upper_signatures import data_for


def pseudoinverse(matrix):
    kernel = matrix.nullspace()
    if not kernel:
        return matrix.inv()
    z = sp.Matrix.hstack(*kernel)
    p = z*(z.T*z).inv()*z.T
    return (matrix+p).inv()-p


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory',type=Path)
    p.add_argument('--cover',type=Path,required=True)
    p.add_argument('--index',type=int,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args(); resources=limit_research_process(1)
    assert not a.output.exists()
    b=sp.Matrix(14,84,lambda i,j:int(i in LABELS[j]))
    mate=sp.Matrix(14,14,lambda i,j:int(j==(i^1)))
    inverse=(b*b.T).inv()
    pi=sp.eye(84)-b.T*inverse*b
    # These constants follow solely from B Gamma=2J-(M+I)B.
    t0=3*sp.eye(84)-(b.T*(mate+4*sp.eye(14))-2*sp.ones(84,14))*inverse*b
    upper0=7*pi-t0
    assert all(t0[i,i]==sp.Rational(5,2) and upper0[i,i]==sp.Rational(10,3) for i in range(84))
    for u,v in PAIRS:
        c=len(set(LABELS[u])&set(LABELS[v])); m=sum((x^1) in LABELS[v] for x in LABELS[u])
        assert t0[u,v]==sp.Rational(2-3*c-m,8)
        assert upper0[u,v]==sp.Rational(-4*c+m-2,15)
    template=json.loads((a.directory/'root_component_templates.json').read_text())['survivors'][a.index]
    cover=next(r for r in json.loads(a.cover.read_text())['records'] if r['template_index']==a.index)
    edges=[tuple(e) for e in template['nongrid_edges']]; all_edges=list(RECTANGLES)
    positions={q:i for i,q in enumerate(edges)}; full_positions=[all_edges.index(e) for e in edges]
    e=sp.Matrix(21,21,lambda i,j:int(i==j)-sp.Rational(len(set(all_edges[i])&set(all_edges[j])),5)+sp.Rational(1,15))
    lift=sp.Matrix([[sp.Rational(*x) for x in row] for row in cover['lift_matrix']])
    tables={tuple(t['rectangle']):t for t in cover['corner_signature_tables']}
    sampled=sorted({0,cover['gram_count']//2,cover['gram_count']-1}); checked=0
    for gi in sampled:
        matrix=gram_matrix(cover,cover['gram_anchor_values'][gi]); full=sp.zeros(21)
        for i,p0 in enumerate(full_positions):
            for j,q0 in enumerate(full_positions):full[p0,q0]=matrix[i,j]
        lower_inv=pseudoinverse(full); upper_inv=pseudoinverse(28*e-full)
        upper=data_for(edges,matrix); scale=225*upper['denominator']; den=28*scale
        anchors=list(matrix.rref()[1]); small_inv=matrix.extract(anchors,anchors).inv()
        states=[]
        for q,table in tables.items():
            row=next(row for row in table['rows'] if row[0]==gi)
            for si in sorted(set(row[1:5]))[:2]:
                h=lift*sp.Matrix(table['catalog'][si]); hh=sp.zeros(21,1)
                for i,p0 in enumerate(full_positions):hh[p0]=h[i]
                u=7*e[:,all_edges.index(q)]-hh
                v=sp.Matrix([7*(15*int(q==f)-3*len(set(q)&set(f))+1)-15*x for f,x in zip(edges,h)])
                states.append((q,h,hh,u,v))
        for ai in range(0,len(states),max(1,len(states)//8)):
            q,ha,hha,ua,va=states[ai]
            for bi in (ai,(ai+1)%len(states),len(states)-1):
                r,hb,hhb,ub,vb=states[bi]
                lower=(ha.extract(anchors,[0]).T*small_inv*hb.extract(anchors,[0]))[0]
                assert lower==(hha.T*lower_inv*hhb)[0]
                cross=(ha[positions[r]] if r in positions else 0)+(hb[positions[q]] if q in positions else 0)
                ip=49*(15*int(q==r)-3*len(set(q)&set(r))+1)*(scale//15)-7*cross*scale+(ha.T*hb)[0]*scale+(va.T*sp.Matrix(upper['correction'])*vb)[0]
                assert sp.Rational(ip,den)==(ua.T*upper_inv*ub)[0]
                checked+=1
    result={'status':'PASSED','scope':__doc__,'resources':resources,
            'full_84_projector_entry_pairs':len(PAIRS),'full_21_schur_pair_checks':checked,
            'tested_gram_selectors':sampled,'template_index':a.index}
    atomic_json_write(a.output,result);print(json.dumps(result),flush=True)


if __name__=='__main__':main()
