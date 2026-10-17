"""Use the complementary projector 7 Pi - T to filter integer signatures.

Pi projects onto ker(B), and P is the 84 by 21 rectangle incidence.
Pi P = P E, where E_{qr}=delta(q,r)-|q intersect r|/5+1/15.
Thus P^t (7Pi-T) P = 28 E-R and (7Pi-T)_{ww}=10/3.

For a row w in rectangle q, put u=7 E e_q-h_w. On im(E), for u
orthogonal to ker(28I-R),
    28 u^t(28E-R)^+u = ||u||^2 + u^t R(28I-R)^+u.
Here ||u||^2=98/3-14 h_w[q]+||h_w||^2. All computations are rational.
This is a necessary upper-projector Schur condition, not a construction.
"""

from math import lcm
import sympy as sp


def data_for(edges, matrix):
    m=len(edges)
    kernel_matrix=28*sp.eye(m)-matrix
    null=kernel_matrix.nullspace()
    if null:
        z=sp.Matrix.hstack(*null)
        projection=z*(z.T*z).inv()*z.T
        inverse=(kernel_matrix+projection).inv(method='DM')-projection
    else:
        inverse=kernel_matrix.inv(method='DM')
    correction=matrix*inverse
    denominator=lcm(*(x.q for x in correction))
    return {'edges':edges,'denominator':denominator,
            'correction':[[int(x*denominator) for x in row] for row in correction.tolist()],
            'null':[[int(x*lcm(*(a.q for a in column))) for x in column] for column in null]}


def signature_passes(rectangle, h, data):
    edges=data['edges'];den=data['denominator'];corr=data['correction']
    # v=15u on the nongrid coordinates, avoiding rational inner products.
    v=[7*(15*int(rectangle==e)-3*len(set(rectangle)&set(e))+1)-15*x for e,x in zip(edges,h)]
    if any(sum(x*y for x,y in zip(v,row)) for row in data['null']): return False
    own=h[edges.index(rectangle)] if rectangle in edges else 0
    correction=sum(v[i]*corr[i][j]*v[j] for i in range(len(v)) for j in range(len(v)))
    return 3*(sum(x*x for x in h)-14*own)*225*den + 3*correction <= 182*225*den


def filter_domains(edges,matrix,domains,data=None):
    data=data_for(edges,matrix) if data is None else data
    before=sum(len(d['signatures']) for d in domains.values())
    for rectangle,item in domains.items():
        item['signatures']=[h for h in item['signatures'] if signature_passes(rectangle,h,data)]
    return {'before':before,'after':sum(len(d['signatures']) for d in domains.values()),
            'eigenvalue_28_kernel':len(data['null'])}


def corner_filter(table, domains, data):
    """Exact complementary Schur PSD on the four corners of one rectangle."""
    from root_component_gram_enumeration import integer_psd
    from root_rectangle_domains import RECTANGLE_LABELS
    rectangle=table['rectangle'];hs=domains[rectangle]['signatures'];edges=data['edges']
    scale=225*data['denominator'];den=28*scale;corr=data['correction']
    own_index=edges.index(rectangle) if rectangle in edges else None
    own=[h[own_index] if own_index is not None else 0 for h in hs]
    vs=[[7*(15*int(rectangle==e)-3*len(set(rectangle)&set(e))+1)-15*x for e,x in zip(edges,h)] for h in hs]
    cvs=[[sum(x*y for x,y in zip(row,v)) for row in corr] for v in vs]
    ips=[[(98*scale)//3-7*(own[i]+own[j])*scale+sum(x*y for x,y in zip(a,b))*scale+
          sum(x*y for x,y in zip(vs[i],cvs[j])) for j,b in enumerate(hs)] for i,a in enumerate(hs)]
    pairs=[(i,j) for i in range(4) for j in range(i+1,4)]
    common={(i,j):len(set(RECTANGLE_LABELS[i])&set(RECTANGLE_LABELS[j])) for i,j in pairs}
    kept=[]
    for row in table['rows']:
        residual=[[0]*4 for _ in range(4)]
        for i in range(4):residual[i][i]=10*den-3*ips[row[i]][row[i]]
        for edge,(i,j) in zip(row[4:],pairs):
            residual[i][j]=residual[j][i]=(3*edge-common[i,j])*den-3*ips[row[i]][row[j]]
        if integer_psd(residual):kept.append(row)
    before=len(table['rows']);table['rows']=kept
    return {'before':before,'after':len(kept)}


def check_full_projector_identity(edges,matrix):
    """Compare the compressed formula with the full 21 by 21 rational inverse."""
    from itertools import combinations
    all_edges=list(combinations(range(7),2));positions=[all_edges.index(q) for q in edges]
    e=sp.Matrix(21,21,lambda i,j:int(i==j)-sp.Rational(len(set(all_edges[i])&set(all_edges[j])),5)+sp.Rational(1,15))
    full=sp.zeros(21)
    for i,p in enumerate(positions):
        for j,q in enumerate(positions):full[p,q]=matrix[i,j]
    assert e*e==e and e*full==full and full*e==full
    s=28*e-full
    z=sp.Matrix.hstack(*s.nullspace());projection=z*(z.T*z).inv()*z.T
    inverse=(s+projection).inv(method='DM')-projection
    data=data_for(edges,matrix)
    correction=sp.Matrix(data['correction'])/data['denominator']
    checked=0
    for q in (0,10,20):
        for h in (sp.zeros(matrix.rows,1),matrix[:,0],-matrix[:,0]):
            hh=sp.zeros(21,1)
            for i,p in enumerate(positions):hh[p]=h[i]
            u=7*e[:,q]-hh;reduced=u.extract(positions,[0])
            if any((sp.Matrix(row).T*reduced)[0] for row in data['null']):continue
            actual=(u.T*inverse*u)[0]
            formula=((u.T*u)[0]+(reduced.T*correction*reduced)[0])/28
            assert actual==formula
            assert signature_passes(all_edges[q],list(h),data)==(actual<=sp.Rational(10,3))
            checked+=1
    assert checked
    return {'full_21_by_21_exact_comparisons':checked,'rank_upper_gram':s.rank()}


if __name__=='__main__':
    import argparse,json,sys
    from pathlib import Path
    sys.path.insert(0,str(Path(__file__).resolve().parent))
    from root_component_resources import limit_research_process,atomic_json_write
    from root_component_signature_moments import gram_matrix
    from root_rectangle_domains import signature_domains
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory',type=Path)
    p.add_argument('--grams',type=Path,required=True)
    p.add_argument('--limit',type=int,default=3)
    p.add_argument('--controls',action='store_true')
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();resources=limit_research_process(2)
    templates=json.loads((a.directory/'root_component_templates.json').read_text())['survivors']
    covers=json.loads(a.grams.read_text())['records'];records=[]
    for cover in covers:
        if cover['template_index'] not in (7,9,19):continue
        edges=[tuple(e) for e in templates[cover['template_index']]['nongrid_edges']]
        for i,values in enumerate(cover['gram_anchor_values'][:a.limit]):
            matrix=gram_matrix(cover,values)
            if a.controls:
                checks=check_full_projector_identity(edges,matrix)
                atomic_json_write(a.output,checks);print(checks,flush=True);sys.exit(0)
            domains={tuple(d['rectangle']):d for d in signature_domains(edges,matrix.tolist())}
            info=filter_domains(edges,matrix,domains)
            info.update(template_index=cover['template_index'],gram_index=cover['source_gram_indices'][i],
                        empty_rectangles=[list(q) for q,d in domains.items() if not d['signatures']])
            records.append(info);print(info,flush=True)
            atomic_json_write(a.output,{'scope':__doc__,'resources':resources,'records':records})
