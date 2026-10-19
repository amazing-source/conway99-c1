"""Exact necessary projection of twelve missing vertices onto three Y grids.

Q03,Q13,Q23 each contribute one neighbour to each of Q45,Q46,Q56.
Their twelve triples are distinct (otherwise two vertices have three
common neighbours), avoid the twelve known K/Q12 triples, and realize
all three residual pair-margin matrices. Two triples sharing two
coordinates must carry opposite root-3 letters; their overlap graph
is consequently bipartite. No unknown rectangle is assumed a grid.
"""

from functools import lru_cache
from itertools import combinations, product


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


def from_block(rows, shared):
    margins = [[[2-shared[12+4*i+a][12+4*j+b]-
                 (rows[12+4*i+a] & rows[12+4*j+b]).bit_count()
                 for b in range(4)] for a in range(4)] for i, j in ((0,1),(0,2),(1,2))]
    known = 0
    for v in range(12):
        triple = [next(j for j in range(4) if rows[v] & (1 << (12+4*i+j))) for i in range(3)]
        known |= 1 << (16*triple[0]+4*triple[1]+triple[2])
    assert known.bit_count() == 12
    report, solutions = complete_triplets(margins, ((1 << 64)-1) ^ known)
    return {**report, 'known_triplets_mask': hex(known), 'pair_margins': margins}, solutions
