"""Map single-line odd permutation moments into the accepted census.

No census is regenerated. New marked patterns are enumerated and mapped
to the supplied affine count rows, with exact automorphism multiplicity.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys

import sympy as sp


def vector_text(vector, names):
    return {name:str(value) for name,value in zip(['1']+names,vector) if value}


def investigate(source, point_file=None):
    source = Path(source)
    sys.path.insert(0, str(source/'code/codex'))
    from seven_vertex_census import canonical_orders, decode
    from higher_vertex_census import ir_orders
    files = {7:'codex_seven_vertex_census.json',8:'codex_order8_census.json',9:'codex_order9_census.json'}
    census, hashes = {}, {}
    for n, name in files.items():
        raw = (source/'data'/name).read_bytes()
        census[n] = json.loads(raw)
        hashes[name] = sha256(raw).hexdigest()
    names = census[9]['parameters']
    indexes = {n:{r['code']:r for r in d['counts']} for n,d in census.items()}
    def lift(n, row):
        result = [F(0)]*(1+len(names))
        result[0] = F(row['affine'][0])
        for name, value in zip(census[n]['parameters'],row['affine'][1:]):
            result[1+names.index(name)] = F(value)
        return result
    def canonical(adj):
        return (ir_orders if len(adj)==9 else canonical_orders)(tuple(adj))
    def pattern(name, far_labels, gamma_edges):
        # Ordered root flags(v,a,abar), distinct ordered exterior letters(x,y).
        # First five vertices have root-letter names0=v,1=a,2=abar,3=x,4=y.
        n = 5+len(far_labels)
        positions = {p:5+i for i,p in enumerate(far_labels)}
        required = {(0,1),(0,2),(1,2),(0,3),(0,4)}
        for pair, index in positions.items():
            required.update(tuple(sorted((letter,index))) for letter in pair)
        required.update(tuple(sorted((positions[p],positions[q]))) for p,q in gamma_edges)
        free = [(3,4)]+[pair for pair in combinations(range(5,n),2) if pair not in required]
        by_code = Counter()
        automorphisms = {}
        admissible = 0
        for bits in product((0,1), repeat=len(free)):
            edges = required | {pair for pair,bit in zip(free,bits) if bit}
            adj = [0]*n
            for i,j in edges:
                adj[i] |= 1<<j
                adj[j] |= 1<<i
            if any((adj[i]&adj[j]).bit_count() > (1 if adj[i]>>j&1 else 2)
                   for i,j in combinations(range(n),2)):
                continue
            code, orders = canonical(adj)
            if code not in indexes[n]:
                raise ValueError(f'Allowed new pattern absent from supplied census:{n},{code}')
            by_code[code] += 1
            automorphisms[code] = len(orders)
            admissible += 1
        value = [F(0)]*(1+len(names))
        terms = []
        for code,multiplicity in sorted(by_code.items()):
            coefficient = multiplicity*automorphisms[code]
            row = lift(n,indexes[n][code])
            value = [a+coefficient*b for a,b in zip(value,row)]
            terms.append(dict(code=code,labelled_completions=multiplicity,
                              automorphisms=automorphisms[code],induced_count_coefficient=coefficient))
        return dict(name=name,vertices=n,required_edges=sorted(required),free_pairs=free,
            unspecified_pairs_are_nonedges=True,raw_completions=2**len(free),
            admissible_completions=admissible,terms=terms,ordered_flag_affine=vector_text(value,names)), value
    all_four = [(1,3),(1,4),(2,3),(2,4)]
    record_a, vec_a = pattern('tr(tau_a*tau_abar)', all_four,
        [((1,3),(1,4)),((2,3),(2,4))])
    record_b2, vec_b2 = pattern('nonfixed contribution to tr(sigma^2)', all_four,
        [((1,3),(2,4)),((1,4),(2,3))])
    record_c, vec_c = pattern('tr(tau_a*sigma)', [(1,3),(1,4),(2,4)],
        [((1,3),(1,4)),((1,3),(2,4))])
    # a,b are invariant under swapping a and abar. The c pattern then becomes d.
    global_a = [x/2 for x in vec_a]
    global_b2 = [x/2 for x in vec_b2]
    global_cd = vec_c
    global_f = [F(0)]*(1+len(names))
    global_f[1+names.index('P')] = 6
    global_b = [x+y for x,y in zip(global_b2,global_f)]
    global_q2 = [2*a+2*b-4*cd for a,b,cd in zip(global_a,global_b,global_cd)]
    global_q2[0] += 693*48
    trace_product = [4*f-q for f,q in zip(global_f,global_q2)]
    trace_product[0] += 693*528
    # Z2 has a unique degree-four root, so its induced count is sum_v d_v.
    z_edges = [(0,1),(0,2),(0,3),(0,4),(1,2),(3,4),(1,5),(3,5),(2,6),(4,6),(5,6)]
    z_adj = [0]*7
    for i,j in z_edges:
        z_adj[i] |= 1<<j
        z_adj[j] |= 1<<i
    z_code,_ = canonical(z_adj)
    z_row = indexes[7][z_code]
    assert global_cd == [4*x for x in lift(7,z_row)]
    # Check our new trace expansion on our own permutation fixture, not a graph.
    tau_a = sp.Matrix(12,12,lambda i,j:int(j == (i ^ 1)))
    tau_b_perm = [0]*12
    for i in range(0,12,2):
        u,v = (i+1)%12,(i+2)%12
        tau_b_perm[u],tau_b_perm[v] = v,u
    tau_b = sp.Matrix(12,12,lambda i,j:int(j == tau_b_perm[i]))
    sigma_perm = [1,2,0,4,3,5,7,8,9,10,11,6]
    sigma = sp.Matrix(12,12,lambda i,j:int(j == sigma_perm[i]))
    Q = tau_a+tau_b-sigma-sigma.T
    f,aa,bb,cc,dd = [sp.trace(matrix) for matrix in (sigma,tau_a*tau_b,sigma*sigma,tau_a*sigma,tau_b*sigma)]
    T = 6*sp.eye(12)-sp.ones(12)/2-Q
    U = 8*sp.eye(12)-sp.Rational(2,3)*sp.ones(12)+Q
    assert sp.trace(Q) == -2*f
    assert sp.trace(Q*Q) == 48+2*aa+2*bb-4*cc-4*dd
    assert sp.trace(T*U) == 528+4*f-sp.trace(Q*Q)
    assert 4*sp.eye(12)-Q == (sp.eye(12)-tau_a)**2/2+(sp.eye(12)-tau_b)**2/2+(sp.eye(12)+sigma)*(sp.eye(12)+sigma.T)
    point_values = None
    if point_file:
        point = {k:F(v) for k,v in json.loads(Path(point_file).read_text())['point'].items()}
        point['1'] = F(1)
        point_values = {name:str(sum(v*point[k] for k,v in zip(['1']+names,vector)))
            for name,vector in [('sum_f',global_f),('sum_a',global_a),('sum_b',global_b),
                                ('sum_c_plus_d',global_cd),('sum_Q_squared_norm',global_q2),('sum_trace_TU',trace_product)]}
    # Parameter meanings are graphs, not names of individual rooted variables.
    catalogue = []
    for name in names:
        if name == 'P':
            catalogue.append(dict(parameter=name,vertices=6,description='Induced triangular prism count.'))
            continue
        ns, cs = name[1:].split('_')
        n, code = int(ns),int(cs)
        adj = decode(n,code)
        catalogue.append(dict(parameter=name,vertices=n,code=code,
            edges=[(i,j) for i,j in combinations(range(n),2) if adj[i]>>j&1]))
    return dict(status='EXACT_SINGLE_LINE_ODD_MOMENT_CENSUS_MAP',source=str(source),
        source_sha256=hashes,parameters=names,parameter_catalogue=catalogue,
        counts_per_order={str(n):dict(types=len(d['counts']),parameters=len(d['parameters'])) for n,d in census.items()},
        accepted_single_line_form='Q=tau_a+tau_abar-sigma-sigma^T; T_odd=6I-J/2-Q; U_odd=8I-2J/3+Q.',
        new_uniform_spectral_lemma=dict(domain='The eleven-dimensional subspace perpendicular to all-ones.',
            Q_spectrum_bounds=[-4,4],T_spectrum_bounds=[2,10],U_spectrum_bounds=[4,12],
            proof='All four summands are orthogonal permutation matrices; Q is symmetric, Q1=0, and its operator norm is at most4 by the triangle inequality. Hence both single-line forms are automatically positive definite on1-perp, with exactly the forced all-ones kernel.',
            consequence='Any violation in the combined two-line odd space is a cross-line coupling obstruction, not failure of either diagonal block.'),
        local_moment_identities=dict(f='tr(sigma): prism degree of the root triangle line',
            a='tr(tau_a*tau_abar)',b='tr(sigma^2)',c='tr(tau_a*sigma)',d='tr(tau_abar*sigma)',
            Q_trace='-2f',Q_squared_norm='48+2a+2b-4c-4d',
            trace_TU='528+4f-||Q||_F^2',
            automatic_lower_bound='tr(T_odd*U_odd)>=432+4f, since ||Q||_F^2<=96.'),
        odd_schur_reduction=dict(coordinates='Project each12-letter block to its all-ones perpendicular subspace using any orthonormal basis.',
            T_condition='D_T-C^T*A_T^(-1)*C is PSD.',
            U_condition='D_U-(7*Omega+C)^T*A_U^(-1)*(7*Omega+C) is PSD.',
            validity='Both diagonal blocks A_T and A_U are automatically positive definite with the proved windows. These are exact equivalences for the combined odd compression, not for the full44x44 forms.'),
        marked_pattern_enumerations=[record_a,record_b2,record_c],
        compact_induced_count_formulas=dict(H='H_n_code denotes the induced unlabelled type count, whether free or affine.',
            sum_a='6H9_10984541408+36H9_13262907120+2H9_13912920516+2H9_15781745092+2H9_40207239904+2H9_61757303448',
            sum_b='6P+12H9_13904794052+6H9_61505645208',
            sum_c_plus_d='2H8_225487536=4Z2',
            sum_Q_squared_norm='33264+2sum_a+2sum_b-16Z2'),
        global_affine=dict(sum_f=vector_text(global_f,names),sum_a=vector_text(global_a,names),
            sum_b=vector_text(global_b,names),sum_c_plus_d=vector_text(global_cd,names),
            sum_Q_squared_norm=vector_text(global_q2,names),sum_trace_TU=vector_text(trace_product,names)),
        global_indexing='Sum over the99 roots and their7 unordered triangle lines. Oriented flags(a,abar) are divided by2 for a and b; summing the c pattern over both orientations gives c+d.',
        Z2_mapping=dict(vertices=7,code=z_code,count=z_row['count'],affine=vector_text(lift(7,z_row),names)),
        values_at_supplied_own_census_point=point_values,
        own_validation='Exact new trace expansion and sum-of-squares window on an own permutation fixture; new marked completions with canonical automorphism factors; new affine identity sum(c+d)=4Z2. No peer graph audited or census regenerated.',
        raw_support_limits=dict(single_B_entry='With the root, all four central letters, two exterior letters and two far vertices: at most9 vertices.',
            generic_two_line_B_product='With the same anchors and four distinct far vertices:11 vertices. No automatic conversion to order9 is asserted.',
            single_line_quadratic_moments='Two root-line letters, the root, two exterior letters and up to four far vertices: at most9; exact maps supplied above.',
            long_permutation_words='Count distinct root letters and far labels in each word. Above9, targeted extra counts or additional identities are required for a direct census representation; algebraic reductions might still exist.'),
        limitations='The census is consumed as supplied. These maps count marked configurations exactly; they do not prove realizability, PSD of the two-line coupling, or exclusion of Conway.')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--point')
    a = p.parse_args()
    report = investigate(a.source,a.point)
    out = Path(a.output)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({key:report[key] for key in ('status','counts_per_order','global_affine','Z2_mapping','limitations')}))
