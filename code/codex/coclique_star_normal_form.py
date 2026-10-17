"""Four constructive matching representatives for each complete H star.

Local labels: Y0,Y1,C0,C1,Z0,...,Z5.  These ten neighbours of H,
after removing its two already closed H-H-X triangles, form 5K2.
C0-C1 is forbidden.  Independent permutations of Y, C and Z give
exactly four orbits: YY, or zero/one/two Y-C matching edges.

This changes representatives, not the graph family.  In particular the
old unconditional C-pair and ZH signature orders must be removed.
"""
from itertools import combinations


def pairs(items):
    return frozenset(tuple(sorted(pair)) for pair in items)


PATTERNS = (
    pairs(((0, 1), (2, 4), (3, 5), (6, 7), (8, 9))),  # YY
    pairs(((0, 4), (1, 5), (2, 6), (3, 7), (8, 9))),  # YC0
    pairs(((0, 2), (1, 4), (3, 5), (6, 7), (8, 9))),  # YC1
    pairs(((0, 2), (1, 3), (4, 5), (6, 7), (8, 9))),  # YC2
)
NAMES = ('YY', 'YC0', 'YC1', 'YC2')


def star_vertices(i):
    return [29+2*i, 30+2*i, 2*i, 2*i+1] + list(range(39+6*i, 45+6*i))


def fixed_edges():
    """Values shared by all representatives, before product variables exist."""
    result = {}
    for i in range(4):
        vertices = star_vertices(i)
        for a, b in combinations(range(10), 2):
            values = {int((a, b) in pattern) for pattern in PATTERNS}
            if len(values) == 1:
                result[tuple(sorted((vertices[a], vertices[b])))] = values.pop()
    return result


def add_constraints(model, edge):
    selectors = []
    for i in range(4):
        vertices = star_vertices(i)
        choices = [model.NewBoolVar(f'v12_star{i}_{name}') for name in NAMES]
        selectors.append(choices)
        model.Add(sum(choices) == 1)
        for a, b in combinations(range(10), 2):
            x = edge(vertices[a], vertices[b])
            if not isinstance(x, int):
                model.Add(x == sum(choices[j] for j, pattern in enumerate(PATTERNS)
                                   if (a, b) in pattern))
        # Safe remaining Z permutations: independent flips of Z-Z matching
        # edges, and permutations of those edges, in the chosen pattern.
        def signature(v):
            return sum((1 << (s-21))*edge(v, s) for s in range(21, 39))
        for j, pattern in enumerate(PATTERNS):
            zz = sorted((a, b) for a, b in pattern if a >= 4)
            for a, b in zz:
                model.Add(signature(vertices[a]) <= signature(vertices[b])).OnlyEnforceIf(choices[j])
            for (a, _), (b, _) in zip(zz, zz[1:]):
                model.Add(signature(vertices[a]) <= signature(vertices[b])).OnlyEnforceIf(choices[j])
        # A zero-charge H-neighbour has as many L neighbours as negative
        # neighbours. Every Y-C or Y-Z matching edge consumes one such slot.
        for y in vertices[:2]:
            for v in vertices[2:]:
                model.Add(edge(y, v) <= edge(v, 37)+edge(v, 38))
    return selectors


def add_negative_budget(model, edge, selectors):
    """The four stars share the SAME negative-neighbour budget in C8."""
    yc = sum(choices[2]+2*choices[3] for choices in selectors)
    model.Add(yc <= sum(edge(c, e) for c in range(8) for e in (37, 38)))
