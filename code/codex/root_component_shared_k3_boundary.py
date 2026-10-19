"""Direct finite cover of a shared eight-core and grids Q45,Q46,Q56.

Uses the LAB's 114 cores and 23 root-letter orbits. No CP solver.
Three grid matchings are sorted using the six permutations of roots 4,5,6.
The eight letter flips on these roots then fix the smallest first-grid
pair at corner 0 and the second-grid pair at corner 0 below corner 1.
Finally core stabilizers are quotiented explicitly, with the same
normalization after every image. These are relabellings, not graph
automorphisms assumed of a completion. Other template equations are
not imposed, so the universal configuration is invariant under them.
"""

import argparse
from collections import Counter
from itertools import combinations, combinations_with_replacement, permutations, product
import gzip
import hashlib
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write, limit_research_process
from root_component_shared_core_colors import PAIRS, PAIR_ID, deficit, colourings

P4 = tuple(permutations(range(4)))
GRID_ROOTS = ((0,1),(0,2),(1,2))
GRID_LABELS = tuple((2*a+s,2*b+t) for a,b in GRID_ROOTS for s,t in product(range(2),repeat=2))
CORE_LABELS = tuple((s,2*r+t) for r in (1,2) for s,t in product(range(2),repeat=2))


def matchings(vertices):
    if not vertices:
        yield ()
        return
    a, *rest = vertices
    for b in rest:
        for tail in matchings([v for v in rest if v != b]):
            yield ((a,b),)+tail


def grid_permutations():
    lookup = {q:i for i,q in enumerate(GRID_LABELS)}
    result = []
    for p in permutations(range(3)):
        image = [lookup[tuple(sorted(2*p[l//2]+l%2 for l in q))] for q in GRID_LABELS]
        result.append(tuple(image.index(i) for i in range(12)))
    return tuple(result)


Y_PERMUTATIONS = grid_permutations()


def normalize_y(state):
    images = set()
    for inverse in Y_PERMUTATIONS:
        s = tuple(state[i] for i in inverse)
        keys = [tuple(sorted(s[4*b:4*b+4])) for b in range(3)]
        if keys != sorted(keys):
            continue
        first = s[:4].index(min(s[:4]))
        f4, f5 = divmod(first, 2)
        f6 = int(s[4+2*f4] > s[5+2*f4])
        flips = (first, 2*f4+f6, 2*f5+f6)
        images.add(bytes(s[4*b+(j^flips[b])] for b in range(3) for j in range(4)))
    assert images
    return images


def core_stabilizers(core):
    edges = {tuple(sorted(p)) for p in core['edges']}
    lookup = {q:i for i,q in enumerate(CORE_LABELS)}
    result = []
    for swap in (False,True):
        roots = (0,2,1) if swap else (0,1,2)
        for flips in product(range(2),repeat=3):
            p = [lookup[tuple(sorted(2*roots[l//2]+((l%2)^flips[l//2]) for l in q))]
                 for q in CORE_LABELS]
            if {tuple(sorted((p[u],p[v]))) for u,v in edges} != edges:
                continue
            result.append(tuple(sum(1<<p[v] for v in range(8) if mask&(1<<v)) for mask in range(256)))
    assert result
    return result


def matching_catalogue(core):
    T = deficit(core)
    nb = [set() for _ in range(8)]
    for u,v in core['edges']:
        nb[u].add(v);nb[v].add(u)
    result = []
    for matching in matchings(list(range(8))):
        ids = tuple(PAIR_ID[p] for p in matching)
        if any(not T[k] for k in ids):
            continue
        forced = [(i,j) for i,j in combinations(range(4),2)
                  if any(set(matching[j])<=nb[v] for v in matching[i])
                  or any(set(matching[i])<=nb[v] for v in matching[j])]
        layouts = tuple(tuple(sum(1<<v for v in matching[e]) for e in p) for p in P4
                        if all(p.index(i)^p.index(j)==3 for i,j in forced))
        if layouts:
            result.append({'ids':ids,'layouts':layouts,'key':tuple(sorted(layouts[0]))})
    result.sort(key=lambda r:r['key'])
    return result


def compatible(a,b,shift_a,shift_b):
    # Distinct grid labels with a common upper letter cannot see
    # the same pair in the core.
    return all(((i>>shift_a)&1)!=((j>>shift_b)&1)
               for i,x in enumerate(a) for j,y in enumerate(b) if x==y)


def enumerate_boundary(core):
    start = time.process_time()
    T = deficit(core)
    catalogue = matching_catalogue(core)
    states = set(); counts = Counter()
    for ia,ib,ic in combinations_with_replacement(range(len(catalogue)),3):
        a,b,c = (catalogue[i] for i in (ia,ib,ic))
        used = Counter(a['ids']+b['ids']+c['ids'])
        if any(n>T[k] for k,n in used.items()):
            continue
        counts['matching_triples'] += 1
        aa = [p for p in a['layouts'] if p[0]==min(p)]
        bb = [p for p in b['layouts'] if p[0]<p[1]]
        cc = c['layouts']
        counts['normalized_layout_triples_before_C2'] += len(aa)*len(bb)*len(cc)
        ac = {p:tuple(q for q in cc if compatible(p,q,0,1)) for p in aa}
        bc = {p:set(q for q in cc if compatible(p,q,0,0)) for p in bb}
        for p,q in product(aa,bb):
            if not compatible(p,q,1,1):
                continue
            for r in ac[p]:
                if r in bc[q]:
                    states.add(bytes(p+q+r))
    counts['normalized_states_before_core_quotient'] = len(states)
    transforms = core_stabilizers(core)
    cases = []; covered = 0
    for state in sorted(states):
        if state not in states:
            continue
        images = set()
        for transform in transforms:
            images.update(normalize_y(tuple(transform[b] for b in state)))
        present = states & images
        assert state in present
        covered += len(present)
        states.difference_update(images)
        cases.append(min(images).hex())
    assert not states and covered==counts['normalized_states_before_core_quotient']
    assert len(set(cases))==len(cases)
    return {'status':'COMPLETE_20_VERTEX_COVER','core':core,
            'core_labels':CORE_LABELS,'grid_labels':GRID_LABELS,
            'grid_root_offset':4,'boundary_encoding':'12 bytes in hex; each byte is the eight-core neighbour mask of one grid label',
            'core_stabilizer_order':len(transforms),'counts':dict(counts),
            'boundaries_hex':sorted(cases),'boundary_count':len(cases),
            'residual_cover_tested':False,'Q12_added':False,
            'cpu_seconds':time.process_time()-start}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pair-cores',type=Path,required=True)
    parser.add_argument('--core-orbits',type=Path,required=True)
    parser.add_argument('--output-directory',type=Path,required=True)
    parser.add_argument('--cores',help='comma-separated representatives; default all')
    args = parser.parse_args()
    resources = limit_research_process(1)
    cores = json.loads(args.pair_cores.read_text(encoding='utf8'))
    orbit_data = json.loads(args.core_orbits.read_text(encoding='utf8'))
    selected = list(map(int,args.cores.split(','))) if args.cores else orbit_data['representatives']
    assert set(selected)<=set(orbit_data['representatives'])
    args.output_directory.mkdir(parents=True,exist_ok=True)
    sources = {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (args.pair_cores,args.core_orbits)}
    for ci in selected:
        path = args.output_directory/f'core_{ci:03d}.json.gz'
        if path.exists():
            old = json.loads(gzip.decompress(path.read_bytes()))
            assert old['sources']==sources and old['core_index']==ci
            print(json.dumps({'core':ci,'resume':'completed_file','status':old['status']}),flush=True)
            continue
        _, colors = colourings(cores[ci])
        if colors:
            result = enumerate_boundary(cores[ci])
        else:
            result = {'status':'EXCLUDED_Q12_COLOUR_FACTORS','boundary_count':0,
                      'certificate':'shared_core_Q12_colour_factors.json'}
        result.update(scope=__doc__,core_index=ci,sources=sources,resources=resources,
                      whole_family_excluded=False)
        path.write_bytes(gzip.compress((json.dumps(result,separators=(',',':'))+'\n').encode('utf8'),mtime=0))
        print(json.dumps({k:v for k,v in result.items() if k in
                          ('core_index','status','boundary_count','counts','cpu_seconds')}),flush=True)


if __name__=='__main__':
    main()
