"""Small exact F2 reduction for a vertex contained in all 21 local grids.

No old files, external solver, random choices or floating point arithmetic.
"""
from itertools import combinations, product, permutations
from pathlib import Path
import json


def span(basis):
    out = [0]
    for x in basis:
        out += [y ^ x for y in out]
    return out


def independent(vectors):
    pivots = {}
    out = []
    for v in vectors:
        x = v
        while x:
            p = x.bit_length()-1
            if p in pivots:
                x ^= pivots[p]
            else:
                pivots[p] = x
                out.append(v)
                break
    return out


def kernel(rows,n):
    rows = list(rows)
    pivots = []
    rank = 0
    for col in range(n):
        pivot = next((j for j in range(rank,len(rows)) if (rows[j]>>col)&1),None)
        if pivot is None:
            continue
        rows[rank],rows[pivot] = rows[pivot],rows[rank]
        for j in range(len(rows)):
            if j != rank and (rows[j]>>col)&1:
                rows[j] ^= rows[rank]
        pivots.append(col)
        rank += 1
    out = []
    for col in range(n):
        if col in pivots:
            continue
        v = 1<<col
        for j,p in enumerate(pivots):
            if (rows[j]>>col)&1:
                v |= 1<<p
        assert all((v&r).bit_count()%2==0 for r in rows)
        out.append(v)
    return out


def dot(x,y):
    return (x&y).bit_count()%2


def sym_coeff(x,y,n):
    out = 0
    for k,(i,j) in enumerate(combinations_with_diagonal(n)):
        v = ((x>>i)&1)*((y>>j)&1)
        if i != j:
            v ^= ((x>>j)&1)*((y>>i)&1)
        out |= v<<k
    return out


def combinations_with_diagonal(n):
    return [(i,j) for i in range(n) for j in range(i,n)]


def symp(x,y):
    return dot(x&63,y>>6)^dot(x>>6,y&63)


def gram_nondegenerate(p,q):
    a,b = [sum(symp(x,y)<<j for j,y in enumerate(q)) for x in p]
    return a != 0 and b != 0 and a != b


def check_square_character_representation():
    chars = [[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]]
    seen = set()
    for perm in permutations(range(4)):
        matrix = [[sum(chars[i][x]*chars[j][perm[x]] for x in range(4))//4
                   for j in range(3)] for i in range(3)]
        assert all(sum(abs(x) for x in row)==1 for row in matrix)
        assert all(sum(abs(matrix[i][j]) for i in range(3))==1 for j in range(3))
        nonzero = [x for row in matrix for x in row if x]
        assert nonzero[0]*nonzero[1]*nonzero[2]==1
        seen.add(tuple(map(tuple,matrix)))
    assert len(seen)==24
    return len(seen)


def xor_conflict_certificate(equations):
    pivots = {}
    for k,(mask,rhs) in enumerate(equations):
        provenance = 1<<k
        while mask:
            p = mask.bit_length()-1
            if p not in pivots:
                pivots[p] = (mask,int(rhs),provenance)
                break
            old,oldrhs,oldp = pivots[p]
            mask ^= old
            rhs ^= oldrhs
            provenance ^= oldp
        if not mask and rhs:
            ids = [j for j in range(len(equations)) if (provenance>>j)&1]
            lhs,total = 0,0
            for j in ids:
                lhs ^= equations[j][0]
                total ^= int(equations[j][1])
            assert lhs==0 and total==1
            return ids
    return None


def opposition_components(equations):
    adj = [[] for _ in range(315)]
    for mask,rhs in equations:
        assert rhs==1
        ends = [3*h+((mask>>(2*h))&3)-1 for h in range(105) if (mask>>(2*h))&3]
        assert len(ends)==2
        a,b = ends
        adj[a].append(b)
        adj[b].append(a)
    colors = {}
    odd = 0
    components = []
    for root in range(315):
        if root in colors:
            continue
        stack = [root]
        colors[root] = 0
        size = 0
        bad = False
        while stack:
            v = stack.pop()
            size += 1
            for w in adj[v]:
                if w in colors:
                    bad |= colors[w]==colors[v]
                else:
                    colors[w] = colors[v]^1
                    stack.append(w)
        odd += bad
        components.append(size)
    return dict(odd_components=odd,component_sizes=sorted(components),max_degree=max(map(len,adj)))


def derive():
    assert check_square_character_representation()==24
    # R=[[0,1],[1,1]], the nontrivial cube root of 1 in GL(2,2).
    planes = [[1,2],[4,8],[16,32],[1|4|16,2|8|32],
              [1|8|16|32,2|4|8|16], [1|4|8|32,2|4|16|32]]
    assert all(len(independent(sum((planes[i] for i in ids),[])))==6
               for ids in combinations(range(6),3))
    annihilators = [kernel(p,6) for p in planes]
    coordinates = [{v:k for k,v in enumerate(span(b))} for b in annihilators]
    equations = []
    for i,j in combinations(range(6),2):
        common = kernel(planes[i]+planes[j],6)
        assert len(common)==2
        for a,b in combinations_with_diagonal(2):
            x,y = common[a],common[b]
            equations.append((sym_coeff(coordinates[i][x],coordinates[i][y],4)<<(10*i))^
                             (sym_coeff(coordinates[j][x],coordinates[j][y],4)<<(10*j)))
    compatible = kernel(equations,60)
    shears = []
    for g in range(21):
        restriction = 0
        for i,basis in enumerate(annihilators):
            for k,(a,b) in enumerate(combinations_with_diagonal(4)):
                restriction |= ((sym_coeff(basis[a],basis[b],6)>>g)&1)<<(10*i+k)
        shears.append(restriction)
    shear_basis = independent(shears)
    assert all(all(dot(v,e)==0 for e in equations) for v in shears)
    joint = list(shear_basis)
    quotient = []
    for v in compatible:
        if len(independent(joint+[v]))>len(joint):
            joint.append(v)
            quotient.append(v)
    assert len(joint)==len(compatible)
    counts = {'compatible_dimension':len(compatible),'shear_dimension':len(shear_basis),
              'quotient_dimension':len(quotient),'quotient_cases':1<<len(quotient),
              'full_disjoint_pairings':0,'idempotent_frames':0}
    survivors = []
    frames = []
    for case,forms in enumerate(span(quotient)):
        lagrangians = [[1<<i for i in range(6)]]
        for i,S in enumerate(annihilators):
            form = (forms>>(10*i))&1023
            vectors = []
            for y in span(S):
                yc = coordinates[i][y]
                for x in range(64):
                    if all(dot(x,z)==dot(form,sym_coeff(yc,1<<j,4)) for j,z in enumerate(S)):
                        vectors.append(x|(y<<6))
            W = independent(vectors)
            assert len(W)==6 and all(symp(x,y)==0 for x in W for y in W)
            lagrangians.append(W)
        spaces = [set(span(W)) for W in lagrangians]
        pairs = list(combinations(range(7),2))
        edges = {e:independent(spaces[e[0]]&spaces[e[1]]) for e in pairs}
        assert all(len(p)==2 for p in edges.values())
        if not all(gram_nondegenerate(edges[e],edges[f]) for e,f in combinations(pairs,2)
                   if set(e).isdisjoint(f)):
            continue
        counts['full_disjoint_pairings'] += 1
        # B_ef = J2 * (R_e^t J12 R_f) is the induced GL(2,2) transport.
        vectors = sum((edges[e] for e in pairs),[])
        B = [sum(symp(vectors[i^1],vectors[j])<<j for j in range(42)) for i in range(42)]
        B2 = [0]*42
        for i,row in enumerate(B):
            for j in range(42):
                if (row>>j)&1:
                    B2[i] ^= B[j]
        if B2==B:
            counts['idempotent_frames'] += 1
            survivors.append(case)
            stars = []
            for i in range(7):
                incident = [e for e in pairs if i in e]
                choices = []
                for picked in product(*(span(edges[e])[1:] for e in incident)):
                    total = 0
                    for v in picked:
                        total ^= v
                    if total==0:
                        choices.append(dict(zip(incident,picked)))
                stars.append(choices)
            links = [(e,f) for e,f in combinations(pairs,2) if set(e).isdisjoint(f)]
            link_id = {link:k for k,link in enumerate(links)}
            edge_coordinates = {e:{v:k for k,v in enumerate(span(edges[e]))} for e in pairs}
            rules = []
            for i in range(7):
                node_rules = []
                for c in stars[i]:
                    equations2, fours = [],[]
                    for e in pairs:
                        if i in e:
                            continue
                        groups = {}
                        for f,v in c.items():
                            if not set(e).isdisjoint(f):
                                continue
                            a,b = edges[e]
                            transported = symp(b,v) | (symp(a,v)<<1)
                            assert transported
                            h = link_id[tuple(sorted((e,f)))]
                            coefficient = transported if e<f else edge_coordinates[f][v]
                            groups.setdefault(transported,[]).append(coefficient<<(2*h))
                        for masks in groups.values():
                            assert len(masks) in (2,4)
                            equation = 0
                            for mask in masks:
                                equation ^= mask
                            equations2.append((equation,len(masks)==2))
                            if len(masks)==4:
                                fours.append(masks)
                    node_rules.append((equations2,fours))
                rules.append(node_rules)
            assignments = []
            visited = 0
            inconsistent = 0
            conflict_depths = {}
            first_conflict = None
            consistent = []
            def extend(picked, pivots):
                nonlocal visited,inconsistent,first_conflict
                visited += 1
                i = len(picked)
                if i==7:
                    assignments.append(list(picked))
                    consistent.append((list(picked),len(pivots)))
                    return
                for state,c in enumerate(stars[i]):
                    if all(c[(j,i)] != stars[j][picked[j]][(j,i)] for j in range(i)):
                        newp = dict(pivots)
                        ok = True
                        for mask,rhs in rules[i][state][0]:
                            while mask:
                                p = mask.bit_length()-1
                                if p not in newp:
                                    newp[p] = (mask,int(rhs))
                                    break
                                old,oldrhs = newp[p]
                                mask ^= old
                                rhs ^= oldrhs
                            if not mask and rhs:
                                ok = False
                                inconsistent += 1
                                conflict_depths[i+1] = conflict_depths.get(i+1,0)+1
                                if first_conflict is None:
                                    full_choice = picked+[state]
                                    all_equations = sum((rules[j][s][0] for j,s in enumerate(full_choice)),[])
                                    certificate = xor_conflict_certificate(all_equations)
                                    assert certificate is not None
                                    first_conflict = dict(endpoint_states=full_choice,
                                                          equation_indices=certificate,
                                                          opposition_components=opposition_components(all_equations),
                                                          equations=[[str(all_equations[k][0]),int(all_equations[k][1])] for k in certificate])
                                break
                        if ok:
                            extend(picked+[state],newp)
            extend([],{})
            frames.append(dict(case=case,edge_planes={str(e):edges[e] for e in pairs},
                               zero_sum_star_choices=list(map(len,stars)),
                               linear_consistent_endpoint_assignment_count=len(assignments),
                               endpoint_search_nodes=visited,
                               inconsistent_prefixes=inconsistent,
                               conflict_depths=conflict_depths,
                               first_conflict_certificate=first_conflict,
                               four_term_rule_counts=sorted(set(len(r[1]) for rr in rules for r in rr)),
                               linear_ranks=sorted(set(rank for _,rank in consistent)),
                               endpoint_assignments=assignments[:10]))
    return dict(counts=counts, survivors=survivors,
                planes=planes, quotient_basis=quotient,frames=frames,
                statement='Every grid-star solution yields one of these symplectic configurations; surviving configurations still require endpoint assignments and signs.')


if __name__=='__main__':
    report = derive()
    out = Path('data/codex_night_20261014/grid_star_f2.json')
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(report['counts'])
    print('surviving cases:',report['survivors'])
    for frame in report['frames']:
        print('zero-sum choices per star:',frame['zero_sum_star_choices'])
        print('linear consistent endpoint assignments:',frame['linear_consistent_endpoint_assignment_count'],
              'search nodes:',frame['endpoint_search_nodes'])
        print('four-term rules per vertex:',frame['four_term_rule_counts'],
              'linear ranks:',frame['linear_ranks'])
        print('conflict counts by depth:',frame['conflict_depths'])
