"""Complete a line neighbourhood using two prism components as a frame.

Let L be a triangle, C the cubic graph on its 36 neighbours, coloured by
their unique neighbour in L, and D its incidence to the remaining 60
vertices.  Every outside vertex meets each six-vertex component once.
Two prism components P,Q therefore label the 60 outside vertices by
(p,q,copy): one copy when p,q have the same colour, two copies otherwise.
This follows from (DD^t)[p,q]=2-[same colour]. It is a relabelling of every
completion, not a choice of a boundary seed.

All completions satisfy
 DD^t=12I-C-C^2+2J-Z,  D(H+I)=2J-CD,
 H^2+H+D^tD=12I+2J,
where H is symmetric binary with degree 8, and each column of D has two
entries in each colour. Stage 0 imposes DD^t, stage 1 also the twelve
fixed rows of D(H+I), stage 2 all of D(H+I), stage 3 all three identities.
Only stage 3 can produce a full SRG; weaker SATs are boundary witnesses.

For the remaining root templates: template 7 has a six-prism line, while
9 and 19 have a line with components 12+12+6+6. The first case has one
neighbourhood type; the second is covered by 14*32=448 types. Normalize
colours on the first 12-component only; retain colour-preserving types
on the second. A repeated isomorphism is harmless; omitting relative
colour orientations would not be sound. No time bound is asserted.
"""

import argparse
from collections import Counter
from itertools import combinations,permutations
import hashlib
import json
from pathlib import Path
import sys
import threading
import time

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write,limit_research_process
from ortools.sat.python import cp_model


def component(record=None,code=None):
    if record is None:
        n=2;perm=[0,1];matchings=[[(0,1)]]*3
    else:
        p,a,b=code;perm=record['cross_permutations'][p];n=len(perm)
        matchings=[[(i,i+1) for i in range(0,n,2)],
                   record['internal_matchings'][a],record['internal_matchings'][b]]
    c=[[0]*(3*n) for _ in range(3*n)]
    def edge(u,v):c[u][v]=c[v][u]=1
    for colour,matching in enumerate(matchings):
        for a,b in matching:edge(colour*n+a,colour*n+b)
    for i in range(n):
        edge(i,n+i);edge(i,2*n+i);edge(n+i,2*n+perm[i])
    assert all(sum(row)==3 for row in c)
    return c,[i//n for i in range(3*n)]


def neighbourhood(library,orbits,family,first,second):
    cs=[component(),component()]
    descriptors=[{'vertices':6},{'vertices':6}]
    if family=='six-prisms':
        assert first==second==0
        cs += [component() for _ in range(4)]
        descriptors += [{'vertices':6} for _ in range(4)]
    else:
        record=next(r for r in library['records'] if r['vertices']==12)
        for index,colours in ((first,True),(second,False)):
            cover=next(r for r in orbits['records'] if r['vertices']==12 and r['allow_colour_permutations']==colours)
            assert cover['all_generator_images_in_source'] and cover['all_codes_covered_disjointly']
            code=cover['orbits'][index]['representative']
            cs.append(component(record,code))
            descriptors.append({'vertices':12,'orbit_index':index,'allow_colour_permutations':colours,'code':code})
    c=[[0]*36 for _ in range(36)];colours=[];groups=[];offset=0
    for (block,colour),description in zip(cs,descriptors):
        group=list(range(offset,offset+len(block)));groups.append(group)
        for i,row in enumerate(block):
            for j,value in enumerate(row):c[offset+i][offset+j]=value
        colours.extend(colour);description['vertices_in_neighbourhood']=group
        offset+=len(block)
    assert offset==36 and Counter(colours)=={0:12,1:12,2:12}
    return c,colours,groups,descriptors


def add_prism_normalization(model,d,cells,groups,template_seven=False):
    """Choose a lexicographically minimal free D block under relabellings.

This is compatible with sorting each two-copy cell: all inequalities hold
at a minimum of the same row-major D[12:36] word over the finite group.
Component flips/permutations, frame flips/interchange, and global colour
permutations relabel an arbitrary completion; no automorphism is assumed.
    """
    assert all(len(group)==6 for group in groups)
    comparisons=0
    def lex(a,b):
        nonlocal comparisons
        tag=f'prism_canonical_{comparisons}';comparisons+=1;prefix=1
        for i,(u,v) in enumerate(zip(a,b)):
            model.add(u<=v).only_enforce_if(prefix)
            equal=model.new_bool_var(f'{tag}_equal_{i}')
            model.add(u==v).only_enforce_if(equal)
            model.add(u!=v).only_enforce_if(equal.Not())
            if isinstance(prefix,int):prefix=equal
            else:
                both=model.new_bool_var(f'{tag}_prefix_{i}')
                model.add(both<=prefix);model.add(both<=equal);model.add(both>=prefix+equal-1)
                prefix=both
    for group in groups[2:]:lex(d[group[0]],d[group[1]])
    interchangeable=groups[3:] if template_seven else groups[2:]
    for left,right in zip(interchangeable,interchangeable[1:]):lex(d[left[0]],d[right[0]])
    index={cell:i for i,cell in enumerate(cells)}
    transforms=[lambda p,q,t:(p^1,q,t),lambda p,q,t:(p,q^1,t),lambda p,q,t:(q-6,p+6,t)]
    for transform in transforms:
        image=[index[transform(*cell)] for cell in cells]
        lex(d[12],[d[12][j] for j in image])
    for permutation in permutations(range(3)):
        if permutation==(0,1,2):continue
        if template_seven and permutation[0]!=0:continue
        image=[index[(2*permutation[p//2]+p%2,6+2*permutation[(q-6)//2]+q%2,t)] for p,q,t in cells]
        row=12+2*permutation[0]
        lex(d[12],[d[row][j] for j in image])
    return {'lex_comparisons':comparisons,'template_seven_root_and_parts_preserved':template_seven,
            'scope':'A common row-major minimum under prism and cell relabellings.'}


def add_prism_cut_partitions(model,h,cells,count,d=None,product=None):
    """Apply global c>=4 at the four known triangles in the two frame prisms.

For such a triangle T, the original line and the other triangle of its
prism form one isolated prism in N(T). The other thirty neighbours are
exactly the core vertices selecting a vertex of T. Their induced cubic
graph must therefore have at least three components. Merge these into
three nonempty balanced bins (sizes18+6+6 or12+12+6), without cross edges.
When D and a product builder are supplied, a bin of size6s also has exactly
s neighbours at every vertex outside T union N(T). Indeed sum d=60s and
sum d^2=60s^2 for a union of components, so its exterior variance is zero.
    """
    assert 0<=count<=4
    records=[]
    for ci,(prism,bit) in enumerate([(0,0),(0,1),(1,0),(1,1)][:count]):
        values=[cell[0] if prism==0 else cell[1]-6 for cell in cells]
        vertices=[x for x,v in enumerate(values) if v%2==bit]
        colours=[[x for x in vertices if values[x]//2==colour] for colour in range(3)]
        assert len(vertices)==30 and all(len(row)==10 for row in colours)
        bins={x:model.new_int_var(1,3,f'prism_cut_{ci}_bin_{x}') for x in vertices}
        flags={x:[model.new_bool_var(f'prism_cut_{ci}_{x}_{j}') for j in range(3)] for x in vertices}
        for x in vertices:
            model.add_map_domain(bins[x],flags[x],offset=1)
            model.add(sum(h[x][y] for y in vertices)==3)
        model.add(bins[colours[0][0]]==1);previous=1
        for i,x in enumerate(colours[0][1:]):
            model.add(bins[x]<=previous+1)
            maximum=model.new_int_var(1,3,f'prism_cut_{ci}_max_{i}')
            model.add_max_equality(maximum,[previous,bins[x]]);previous=maximum
        balance_equations=0
        for j in range(3):
            half=model.new_int_var(1,3,f'prism_cut_{ci}_half_{j}')
            for row in colours:model.add(sum(flags[x][j] for x in row)==2*half)
            if d is not None:
                assert product is not None
                for u in range(36):
                    if u//6==prism:continue
                    model.add(sum(product(d[u][x],flags[x][j]) for x in vertices)==half)
                    balance_equations+=1
                for y in range(60):
                    if y in bins:continue
                    model.add(sum(product(h[y][x],flags[x][j]) for x in vertices)==half)
                    balance_equations+=1
        for x,y in combinations(vertices,2):
            edge=h[x][y]
            if isinstance(edge,int):
                if edge:model.add(bins[x]==bins[y])
            else:model.add(bins[x]==bins[y]).only_enforce_if(edge)
        records.append({'prism':prism,'triangle_bit':bit,'core_vertices':vertices,
                        'minimum_components_inside_cut':3,'known_separate_prism_component':True,
                        'exterior_component_balance_equations':balance_equations})
    return {'global_minimum_components':4,'cuts':records,'scope':add_prism_cut_partitions.__doc__}


def build(c,colours,groups,stage,minc_lines=0,rotated_rectangles=0,core_triangles=False,normalize_prisms=False,template_seven=False,prism_matchings=False,prism_cut_partitions=0,grid_perfect_codes=False,prism_cut_balance=False):
    assert not template_seven or (stage>=1 and all(len(g)==6 for g in groups))
    assert not prism_matchings or (stage>=1 and core_triangles and all(len(g)==6 for g in groups))
    cells=[(p,q,copy) for p in range(6) for q in range(6,12)
           for copy in range(2-int(colours[p]==colours[q]))]
    assert len(cells)==60
    m=cp_model.CpModel()
    d=[[int(u==p or u==q) if u<12 else m.new_bool_var(f'd_{u}_{x}')
        for x,(p,q,_) in enumerate(cells)] for u in range(36)]
    cn=[[sum(c[u][z]*c[v][z] for z in range(36)) for v in range(36)] for u in range(36)]
    targets=[[12*int(u==v)-c[u][v]-cn[u][v]+2-int(colours[u]==colours[v])
              for v in range(36)] for u in range(36)]
    assert all(targets[u][u]==10 for u in range(36))
    assert min(map(min,targets))>=0
    products={}
    def product(a,b):
        if isinstance(a,int):return b if a else 0
        if isinstance(b,int):return a if b else 0
        if a.index==b.index:return a
        key=tuple(sorted((a.index,b.index)))
        if key not in products:
            v=m.new_bool_var(f'product_{len(products)}')
            m.add(v<=a);m.add(v<=b);m.add(v>=a+b-1);products[key]=v
        return products[key]
    for u in range(36):m.add(sum(d[u])==10)
    for x in range(60):
        for colour in range(3):m.add(sum(d[u][x] for u in range(36) if colours[u]==colour)==2)
        for group in groups:m.add(sum(d[u][x] for u in group)==len(group)//6)
        for u in range(36):
            # The neighbours of an outside vertex induce a matching.
            terms=[d[v][x] for v in range(36) if c[u][v]]
            m.add(sum(terms)<=1+3*(1-d[u][x]))
    for u,v in combinations(range(36),2):
        target=targets[u][v]
        if target==0:
            for x in range(60):m.add(d[u][x]+d[v][x]<=1)
        else:m.add(sum(product(d[u][x],d[v][x]) for x in range(60))==target)
    from root_component_rotated_boundary import fixed_forbidden_triples
    forbidden=fixed_forbidden_triples(c,colours)
    for triple in forbidden:
        for x in range(60):m.add(sum(d[u][x] for u in triple)<=2)
    # The two copies of a cell have interchangeable outside names. Ordering
    # their D columns is a valid simultaneous row/column relabelling of H.
    for x in range(59):
        if cells[x][:2]!=cells[x+1][:2]:continue
        prefix=1
        for u in range(12,36):
            a,b=d[u][x],d[u][x+1]
            m.add(a<=b).only_enforce_if(prefix)
            equal=m.new_bool_var(f'equal_{x}_{u}')
            m.add(a==b).only_enforce_if(equal)
            m.add(a!=b).only_enforce_if(equal.Not())
            if isinstance(prefix,int):prefix=equal
            else:
                both=m.new_bool_var(f'prefix_{x}_{u}')
                m.add(both<=prefix);m.add(both<=equal);m.add(both>=prefix+equal-1)
                prefix=both
    h=None;dh_count=0;core_count=0;dh_rows=[];saturated_pairs=0
    prism_normalization=add_prism_normalization(m,d,cells,groups,template_seven=template_seven) if normalize_prisms else None
    if stage:
        h=[[0]*60 for _ in range(60)]
        for x,y in combinations(range(60),2):
            # Same cell already means two shared neighbours in P union Q.
            h[x][y]=h[y][x]=0 if cells[x][:2]==cells[y][:2] else m.new_bool_var(f'h_{x}_{y}')
        for x in range(60):m.add(sum(h[x])==8)
        # The two vertices of a double cell already have their two common
        # neighbours p,q. No further common neighbour is possible in C or H.
        for x,y in combinations(range(60),2):
            if cells[x][:2]!=cells[y][:2]:continue
            saturated_pairs+=1
            for u in range(12,36):m.add(d[u][x]+d[u][y]<=1)
            for z in range(60):m.add(h[x][z]+h[y][z]<=1)
        # In template7 colour0 is the original low-prism root. Its complete
        # mixed equations recover C1 at all fourteen original neighbours.
        dh_rows=[u for u in range(36) if stage>=2 or u<12 or (template_seven and colours[u]==0)]
        for u in dh_rows:
            for x in range(60):
                m.add(sum(product(d[u][y],h[y][x]) for y in range(60))
                      +d[u][x]+sum(d[v][x] for v in range(36) if c[u][v])==2)
                dh_count+=1
        if stage>=3:
            for x,y in combinations(range(60),2):
                m.add(h[x][y]+sum(product(h[x][z],h[y][z]) for z in range(60))
                      +sum(product(d[u][x],d[u][y]) for u in range(36))==2)
                core_count+=1
    partition_info=None
    rotation_info=None;triangle_info=None;matching_info=None;cut_info=None
    template_info=None
    if minc_lines or rotated_rectangles or template_seven:
        assert h is not None
        full=full_graph(c,colours,d,h)
    if minc_lines:
        lines=[(colour,3+u,3+v) for colour in range(3)
               for u,v in combinations(range(36),2)
               if colours[u]==colours[v]==colour and c[u][v]][:minc_lines]
        from root_component_minimum_partition import add_partitions_for_lines
        partition_info=add_partitions_for_lines(m,full,lines)
    if rotated_rectangles or template_seven:
        from root_component_rotated_rectangles import add_fixed_star_rectangles
        stars=[(colour,[3+u for u in range(36) if colours[u]==colour],list(range(39,99))) for colour in range(3)]
        budget=[];prescribed=[]
        def prescribe(root_colour,first,second,es):
            if root_colour!=0:return
            i,j=(first[0]-3)//6,(second[0]-3)//6
            same_part=(i<3)==(j<3)
            if same_part:
                for ei,edge in enumerate(es):m.add(edge==int(ei in (0,1,4,5)))
            else:
                m.add(sum(es)<=2)
                budget.extend(es[ei] for ei in (0,1,4,5))
            prescribed.append({'components':[i,j],'grid':same_part})
            return same_part
        rotation_info=add_fixed_star_rectangles(m,full,stars,rotated_rectangles,
            required_roots=(0,) if template_seven else (),rectangle_constraints=prescribe if template_seven else None,
            grid_dominance_roots=(0,) if grid_perfect_codes else ())
        if template_seven:
            assert len(prescribed)==15 and sum(not r['grid'] for r in prescribed)==9 and len(budget)==36
            # Six base-line grids and six same-part grids already contribute48.
            m.add(sum(budget)<=3)
            template_info={'template_index':7,'original_root_colour':0,
                'component_parts':[[0,1,2],[3,4,5]],'frame_prisms_chosen_in_same_part':True,
                'rectangles':prescribed,'fixed_grid_prism_budget':48,'remaining_prism_budget':3,
                'coverage':'Every template7 completion can choose two reference prisms in one of its three-element parts.'}
    if core_triangles:
        assert h is not None
        incident=[[] for _ in range(60)];flags=[];forbidden_triangles=0
        edge_triangle_flags={pair:[] for pair in combinations(range(60),2)}
        known=[[u for u in range(36) if isinstance(d[u][x],int) and d[u][x]==1] for x in range(60)]
        for tri in combinations(range(60),3):
            es=[h[x][y] for x,y in combinations(tri,2)]
            if any(isinstance(e,int) and e==0 for e in es):continue
            if any(set(known[x])&set(known[y]) for x,y in combinations(tri,2)):
                # An adjacent pair with a known boundary common neighbour
                # cannot have a second common neighbour inside H.
                m.add_bool_or([e.Not() for e in es if not isinstance(e,int)])
                forbidden_triangles+=1;continue
            flag=m.new_bool_var('core_actual_triangle_'+'_'.join(map(str,tri)))
            for edge in es:m.add(flag<=edge)
            m.add(flag>=sum(es)-2)
            flags.append(flag)
            for x in tri:incident[x].append(flag)
            for pair in combinations(tri,2):edge_triangle_flags[pair].append(flag)
        local_triangles=sum(all(c[u][v] for u,v in combinations(tri,2)) for tri in combinations(range(36),3))
        m.add(sum(flags)==32-local_triangles)
        for x in range(60):
            boundary_edges=sum(product(d[u][x],d[v][x]) for u,v in combinations(range(36),2)
                               if c[u][v] and targets[u][v]>0)
            m.add(sum(incident[x])==1+boundary_edges)
        triangle_info={'actual_triangle_indicators':len(flags),'forbidden_by_known_boundary':forbidden_triangles,
                       'total_triangles':32-local_triangles,'per_vertex_balance':'t_H(x)=1+e(C[N_C(x)])'}
    if prism_matchings:
        # Each D column selects exactly one of the six vertices in each prism.
        # A selected row u has (CD)_{u,x}=0, hence (DH)_{u,x}=1. Therefore
        # its class induces a matching in H, once for each of the six prisms.
        # lambda=1 makes these six matchings disjoint, with the twenty core
        # triangles supplying the other two incident edges at every vertex.
        choices=[]
        for i,group in enumerate(groups):
            if i<2:
                choices.append([p if i==0 else q-6 for p,q,_ in cells]);continue
            row=[]
            for x in range(60):
                value=m.new_int_var(0,5,f'prism_choice_{i}_{x}')
                m.add_map_domain(value,[d[u][x] for u in group])
                row.append(value)
            choices.append(row)
        degrees=[[[] for _ in range(60)] for _ in groups]
        shared_flags=0;products_before=len(products)
        for x,y in combinations(range(60),2):
            shared=[];matching=[]
            for i in range(6):
                if i<2:same=int(choices[i][x]==choices[i][y])
                else:
                    same=m.new_bool_var(f'common_prism_{i}_{x}_{y}')
                    m.add(choices[i][x]==choices[i][y]).only_enforce_if(same)
                    m.add(choices[i][x]!=choices[i][y]).only_enforce_if(same.Not())
                    shared_flags+=1
                shared.append(same)
                edge=product(h[x][y],same)
                matching.append(edge);degrees[i][x].append(edge);degrees[i][y].append(edge)
            m.add(sum(shared)+h[x][y]<=2)
            m.add(sum(matching)+sum(edge_triangle_flags[x,y])==h[x][y])
        for row in degrees:
            for edges in row:m.add(sum(edges)==1)
        matching_info={'prism_matchings':6,'vertices_per_matching':60,
            'shared_component_indicators':shared_flags,'matching_edge_products':len(products)-products_before,
            'common_boundary_inequalities':1770,'triangle_matching_edge_partition_equations':1770,
            'matching_degree_equations':360,
            'scope':'H is the disjoint union of twenty triangles and six perfect matchings, one within each prism incidence partition.'}
    if prism_cut_partitions:
        assert h is not None
        cut_info=add_prism_cut_partitions(m,h,cells,prism_cut_partitions,
            d=d if prism_cut_balance else None,product=product if prism_cut_balance else None)
    return m,d,h,{'stage':stage,'full_SRG_equations':stage==3,'cells':[list(t) for t in cells],
                  'DDt_pair_equations':630,'DH_equations':dh_count,'core_pair_equations':core_count,
                  'DH_rows':dh_rows,
                  'products':len(products),'minimum_components':partition_info,
                  'rotated_rectangles':rotation_info,'core_triangles':triangle_info,
                  'prism_normalization':prism_normalization,
                  'template_seven':template_info,
                  'prism_matchings':matching_info,
                  'prism_cut_partitions':cut_info,
                  'saturated_double_cell_pairs':saturated_pairs,
                  'rotated_forbidden_triples':[list(t) for t in forbidden],
                  'variables':len(m.proto.variables),'constraints':len(m.proto.constraints)}


def full_graph(c,colours,d,h):
    graph=[[0]*99 for _ in range(99)]
    for a,b in combinations(range(3),2):graph[a][b]=graph[b][a]=1
    for u in range(36):
        graph[colours[u]][3+u]=graph[3+u][colours[u]]=1
        for v in range(36):graph[3+u][3+v]=c[u][v]
        for x in range(60):graph[3+u][39+x]=graph[39+x][3+u]=d[u][x]
    for x in range(60):
        for y in range(60):graph[39+x][39+y]=h[x][y]
    return graph


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory',type=Path)
    p.add_argument('--family',choices=['six-prisms','double12'],required=True)
    p.add_argument('--first',type=int,default=0);p.add_argument('--second',type=int,default=0)
    p.add_argument('--stage',type=int,choices=range(4),default=1)
    p.add_argument('--minc-lines',type=int,default=0)
    p.add_argument('--rotated-rectangles',type=int,default=0)
    p.add_argument('--core-triangles',action='store_true')
    p.add_argument('--build-only',action='store_true')
    p.add_argument('--normalize-prisms',action='store_true')
    p.add_argument('--template-seven',action='store_true')
    p.add_argument('--prism-matchings',action='store_true')
    p.add_argument('--prism-cut-partitions',type=int,default=0,choices=range(5))
    p.add_argument('--grid-perfect-codes',action='store_true')
    p.add_argument('--prism-cut-balance',action='store_true')
    p.add_argument('--seconds',type=float,default=60)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();resources=limit_research_process(1)
    if args.template_seven and args.family!='six-prisms':p.error('--template-seven requires --family six-prisms')
    tables_path=args.directory/'line_component_pattern_tables_rotated.json'
    orbit_path=args.directory/'line_component_colored_orbits.json'
    raw=tables_path.read_bytes();library=json.loads(raw);orbits=json.loads(orbit_path.read_bytes())
    assert orbits['source_sha256']==hashlib.sha256(raw).hexdigest()
    c,colours,groups,descriptors=neighbourhood(library,orbits,args.family,args.first,args.second)
    if args.prism_cut_balance and not args.prism_cut_partitions:p.error('--prism-cut-balance requires --prism-cut-partitions')
    started=time.process_time();m,d,h,info=build(c,colours,groups,args.stage,args.minc_lines,args.rotated_rectangles,args.core_triangles,args.normalize_prisms,args.template_seven,args.prism_matchings,args.prism_cut_partitions,args.grid_perfect_codes,args.prism_cut_balance)
    assert not m.validate(),m.validate()
    info.update(status='MODEL_BUILT',scope=__doc__,family=args.family,first=args.first,second=args.second,
                components=descriptors,resources=resources,build_cpu_seconds=time.process_time()-started,
                source_sha256=hashlib.sha256(raw).hexdigest())
    atomic_json_write(args.output,info)
    print({k:v for k,v in info.items() if k not in ('scope','cells','components')},flush=True)
    if args.build_only:return
    solver=cp_model.CpSolver();solver.parameters.num_search_workers=1
    solver.parameters.max_time_in_seconds=max(600,100*args.seconds)
    solver.parameters.symmetry_level=0;solver.parameters.cp_model_probing_level=0
    solver.parameters.linearization_level=0
    started=time.process_time();done=threading.Event()
    def interrupt():
        while not done.wait(.05):
            if time.process_time()-started>=args.seconds:solver.stop_search();return
    timer=threading.Thread(target=interrupt,daemon=True);timer.start()
    try:status=solver.solve(m)
    finally:done.set();timer.join()
    info.update(status=solver.status_name(status),solver_cpu_seconds=time.process_time()-started,
                branches=solver.num_branches,conflicts=solver.num_conflicts)
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        dd=[[solver.value(v) for v in row] for row in d]
        info['D_columns']=[[u for u in range(36) if dd[u][x]] for x in range(60)]
        if h is not None:
            hh=[[solver.value(v) for v in row] for row in h]
            info['H_edges']=[[x,y] for x,y in combinations(range(60),2) if hh[x][y]]
            graph=full_graph(c,colours,dd,hh)
            errors=[(u,v) for u,v in combinations(range(99),2)
                    if sum(graph[u][z]*graph[v][z] for z in range(99))!=2-graph[u][v]]
            info['missing_SRG_pair_equations']=len(errors)
            info['full_SRG_verified']=not errors and all(sum(row)==14 for row in graph)
            if args.stage==3:assert info['full_SRG_verified']
    atomic_json_write(args.output,info)
    print({k:v for k,v in info.items() if k not in ('scope','cells','components','D_columns','H_edges')},flush=True)


if __name__=='__main__':main()
