"""Exact necessary projection of twelve missing vertices onto three Y grids.

Q03,Q13,Q23 each contribute one neighbour to each of Q45,Q46,Q56.
Their twelve triples are distinct (otherwise two vertices have three
common neighbours), avoid the twelve known K/Q12 triples, and realize
all three residual pair-margin matrices. Two triples sharing two
coordinates must carry opposite root-3 letters; their overlap graph
is consequently bipartite. No unknown rectangle is assumed a grid.
"""

from functools import lru_cache
from itertools import combinations, permutations, product


@lru_cache(maxsize=4096)
def row_options(row_margin, column_margin):
    """All binary 4x4 tables with prescribed margins (total three)."""
    result = []
    def visit(b, remaining, mask):
        if b == 4:
            if not any(remaining):
                result.append(mask)
            return
        for choice in combinations([c for c in range(4) if remaining[c]], row_margin[b]):
            new = list(remaining)
            for c in choice:
                new[c] -= 1
            visit(b + 1, tuple(new), mask | sum(1 << (4*b+c) for c in choice))
    visit(0, column_margin, 0)
    return tuple(result)


def code(mask):
    return sum(1 << (2*i) for i in range(16) if mask & (1 << i))


def bipartite_overlap(triples):
    vertices = [(t//16, t//4 % 4, t % 4) for t in range(64) if triples & (1 << t)]
    adjacency = [set() for _ in vertices]
    for i, j in combinations(range(len(vertices)), 2):
        if sum(a == b for a, b in zip(vertices[i], vertices[j])) == 2:
            adjacency[i].add(j); adjacency[j].add(i)
    colour = {}
    for start in range(len(vertices)):
        if start in colour:
            continue
        colour[start] = 0; pending = [start]
        while pending:
            u = pending.pop()
            for v in adjacency[u]:
                if v in colour:
                    if colour[v] == colour[u]:
                        return False
                else:
                    colour[v] = 1-colour[u]; pending.append(v)
    return True


def complete_triplets(margins, allowed=(1 << 64)-1, require_bipartite=True):
    """Exhaustive four-row join, at most six options per row."""
    ab, ac, bc = [tuple(tuple(r) for r in matrix) for matrix in margins]
    assert all(all(0 <= x <= 2 for x in row) for m in (ab, ac, bc) for row in m)
    assert all(all(sum(row) == 3 for row in m) and
               all(sum(m[a][b] for a in range(4)) == 3 for b in range(4)) for m in (ab, ac, bc))
    support = sum(1 << (4*b+c) for b in range(4) for c in range(4) if bc[b][c])
    choices = [tuple(mask for mask in row_options(ab[a], ac[a])
                     if not mask & ~(support & (allowed >> (16*a)))) for a in range(4)]
    if any(not row for row in choices):
        return {'status': 'EXCLUDED_Y_TRIPLET_MARGINS', 'row_domain_sizes': list(map(len, choices)),
                'margin_solutions': 0, 'bipartite_solutions': 0}, ()
    target = sum(bc[b][c] << (2*(4*b+c)) for b in range(4) for c in range(4))
    right = {}
    for c, d in product(choices[2], choices[3]):
        right.setdefault(code(c) + code(d), []).append((c, d))
    survivors = []; total = 0
    for a, b in product(choices[0], choices[1]):
        left = code(a) + code(b)
        if any(((left >> (2*i)) & 3) > ((target >> (2*i)) & 3) for i in range(16)):
            continue
        for c, d in right.get(target-left, ()):
            mask = a | (b << 16) | (c << 32) | (d << 48); total += 1
            if not require_bipartite or bipartite_overlap(mask):
                survivors.append(mask)
    status = 'PASSES_Y_TRIPLET_PROJECTION' if survivors else (
        'EXCLUDED_Y_TRIPLET_OVERLAP' if total else 'EXCLUDED_Y_TRIPLET_MARGINS')
    return {'status': status, 'row_domain_sizes': list(map(len, choices)),
            'margin_solutions': total, 'bipartite_solutions': len(survivors)}, tuple(survivors)


@lru_cache(maxsize=1)
def universal_designs():
    """All X24-to-Y12 incidence sets before choosing the shared core.

    X consists of all six rectangles on the other four roots. Its
    vertices have distinct triples, and margins 2 minus shared letters.
    Four binary slices have margins (1,1,2,2) in the appropriate orders;
    each has 34 options. The exhaustive join gives 816 labelled sets.
    """
    ab=tuple(tuple(2-int(a//2==b//2) for b in range(4)) for a in range(4))
    ac=tuple(tuple(2-int(a%2==c//2) for c in range(4)) for a in range(4))
    bc=tuple(tuple(2-int(b%2==c%2) for c in range(4)) for b in range(4))
    choices=[row_options(ab[a],ac[a]) for a in range(4)]
    right={}
    for c,d in product(choices[2],choices[3]):
        right.setdefault(code(c)+code(d),[]).append((c,d))
    target=sum(bc[b][c]<<(2*(4*b+c)) for b in range(4) for c in range(4))
    result=[]
    for a,b in product(choices[0],choices[1]):
        left=code(a)+code(b)
        if any(((left>>(2*i))&3)>((target>>(2*i))&3) for i in range(16)):
            continue
        for c,d in right.get(target-left,()):
            result.append(a|(b<<16)|(c<<32)|(d<<48))
    return tuple(sorted(result))


@lru_cache(maxsize=1)
def incidence_index():
    return tuple(sum(1<<i for i,m in enumerate(universal_designs()) if m&(1<<t)) for t in range(64))


@lru_cache(maxsize=65536)
def extend_known_triplets(known):
    designs=universal_designs();index=incidence_index();candidates=(1<<len(designs))-1
    remaining=known
    while remaining and candidates:
        bit=remaining&-remaining;remaining^=bit
        candidates&=index[bit.bit_length()-1]
    count=candidates.bit_count();survivors=[]
    while candidates:
        bit=candidates&-candidates;candidates^=bit
        missing=designs[bit.bit_length()-1]^known
        if bipartite_overlap(missing):survivors.append(missing)
    status='PASSES_Y_TRIPLET_PROJECTION' if survivors else (
        'EXCLUDED_Y_TRIPLET_OVERLAP' if count else 'EXCLUDED_Y_TRIPLET_MARGINS')
    return {'status':status,'universal_designs':len(designs),'margin_solutions':count,
            'bipartite_solutions':len(survivors)},tuple(survivors)


def from_block(rows, shared):
    margins = [[[2-shared[12+4*i+a][12+4*j+b]-
                 (rows[12+4*i+a] & rows[12+4*j+b]).bit_count()
                 for b in range(4)] for a in range(4)] for i, j in ((0,1),(0,2),(1,2))]
    known = 0
    for v in range(12):
        triple = [next(j for j in range(4) if rows[v] & (1 << (12+4*i+j))) for i in range(3)]
        known |= 1 << (16*triple[0]+4*triple[1]+triple[2])
    assert known.bit_count() == 12
    report, solutions = extend_known_triplets(known)
    return {**report, 'known_triplets_mask': hex(known), 'pair_margins': margins}, solutions


def design_orbits():
    rectangles=((0,1),(0,2),(1,2));maps=[]
    for permutation in permutations(range(3)):
        for flips in product(range(2),repeat=3):
            mapping=[]
            for t in range(64):
                corners=(t//16,t//4%4,t%4);out=[None]*3
                for (a,b),corner in zip(rectangles,corners):
                    letters=sorted(((permutation[a],(corner//2)^flips[permutation[a]]),
                                    (permutation[b],(corner%2)^flips[permutation[b]])))
                    target=rectangles.index((letters[0][0],letters[1][0]))
                    out[target]=2*letters[0][1]+letters[1][1]
                mapping.append(16*out[0]+4*out[1]+out[2])
            maps.append(mapping)
    designs=set(universal_designs());unseen=set(designs);orbits=[]
    while unseen:
        rep=min(unseen);support=[t for t in range(64) if rep&(1<<t)]
        orbit={sum(1<<mapping[t] for t in support) for mapping in maps}
        assert orbit<=designs
        unseen-=orbit
        orbits.append({'representative':f'{rep:016x}','size':len(orbit),
                       'stabilizer_in_root_relabellings':48//len(orbit),
                       'members':[f'{x:016x}' for x in sorted(orbit)]})
    return orbits


if __name__=='__main__':
    import argparse,json,sys,time
    from pathlib import Path
    from collections import Counter
    sys.path.insert(0,str(Path(__file__).resolve().parent))
    from root_component_resources import limit_research_process,atomic_json_write
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();assert not args.output.exists();limit_research_process(1)
    start=time.process_time();designs=universal_designs();orbits=design_orbits()
    out={'scope':'X24-to-Y12 incidences only; no full SRG construction',
         'number_of_designs':len(designs),'number_of_orbits':len(orbits),
         'design_masks_hex':[f'{x:016x}' for x in designs],
         'orbits':orbits,'orbit_sizes':dict(Counter(o['size'] for o in orbits)),
         'cpu_seconds':time.process_time()-start}
    atomic_json_write(args.output,out)
    print(json.dumps({k:v for k,v in out.items() if k not in ('design_masks_hex','orbits')}))
