"""Finite support search for orthogonal co-Heawoods through one vertex.

Labels 0, 1..14, 15..98 are the root, its seven paired neighbor lines,
and the unique second common neighbors of non-mate neighbor pairs.
Only necessary conditions are used: this is not an SRG construction.
"""
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import json


PAIRS = list(combinations(range(14), 2))
PAIRS = [p for p in PAIRS if p[0] // 2 != p[1] // 2]
Q = {p: 15 + k for k, p in enumerate(PAIRS)}
NMASK = (1 << 15) - 2


def mask(vertices):
    return sum(1 << x for x in vertices)


def matchings(vertices):
    if not vertices:
        yield ()
        return
    a = vertices[0]
    for b in vertices[1:]:
        if a // 2 != b // 2:
            for tail in matchings(tuple(x for x in vertices if x not in (a, b))):
                yield (tuple(sorted((a, b))),) + tail


def all_roots():
    roots = []
    for lines in combinations(range(7), 4):
        unused = tuple(x for x in range(14) if x // 2 not in lines)
        ms = list(matchings(unused))
        assert len(ms) == 8
        for bits in product(range(2), repeat=4):
            neg_n = tuple(2*l+b for l, b in zip(lines, bits))
            positive = 1 | mask(Q[p] for p in combinations(neg_n, 2))
            for matching in ms:
                negative = mask(x+1 for x in neg_n) | mask(Q[p] for p in matching)
                assert positive.bit_count() == negative.bit_count() == 7
                assert not positive & negative
                roots.append((positive, negative))
    assert len(set(roots)) == len(roots) == 4480
    return roots


def compatible(f, g):
    fp, fn = f
    gp, gn = g
    if fp & gp != 1:
        return False
    nn = fn & gn
    if nn.bit_count() > 1 or nn & ~NMASK:
        return False
    pn = (fp & gn).bit_count()
    np = (fn & gp).bit_count()
    return pn <= 1 and np <= 1 and pn + np == 1 + nn.bit_count()


def root_stabilizer(roots):
    """The 144 elements of the local wreath group fixing roots[0]."""
    index = {f: i for i, f in enumerate(roots)}
    group = []
    for first in permutations(range(4)):
        for last in permutations(range(4, 7)):
            for flips in product(range(2), repeat=3):
                perm = first + last
                flip = (0, 0, 0, 0) + flips
                nmap = [2*perm[x//2] + (x%2 ^ flip[x//2]) for x in range(14)]
                mapping = [0] + [x+1 for x in nmap]
                mapping += [Q[tuple(sorted((nmap[x], nmap[y])))] for x, y in PAIRS]
                def transform(bits):
                    result = 0
                    while bits:
                        b = bits & -bits
                        bits ^= b
                        result |= 1 << mapping[b.bit_length()-1]
                    return result
                if tuple(transform(bits) for bits in roots[0]) != roots[0]:
                    continue
                group.append([index[tuple(transform(bits) for bits in f)] for f in roots])
    assert len(group) == 144
    assert len({tuple(g) for g in group}) == 144
    return group


def vertices(bits):
    while bits:
        b = bits & -bits
        bits ^= b
        yield b.bit_length() - 1


def base_graph():
    ns = [0] * 99
    def edge(x, y):
        ns[x] |= 1 << y
        ns[y] |= 1 << x
    for x in range(1, 15):
        edge(0, x)
        edge(x, 1 + ((x-1) ^ 1))
    for (x, y), q in Q.items():
        edge(q, x+1)
        edge(q, y+1)
    assert all(ns[x].bit_count() == 14 for x in range(15))
    return ns


def root_graph_options(root):
    positive, negative = root
    neg_n = [x-1 for x in vertices(negative & NMASK)]
    neg_q = list(vertices(negative & ~NMASK))
    a, b, c, d = neg_n
    omitted = [((a,b),(c,d)), ((a,c),(b,d)), ((a,d),(b,c))]
    options = []
    for ordering in permutations(omitted):
        ns = [0] * 99
        fs = [0] * 99
        def edge(x, y):
            ns[x] |= 1 << y
            ns[y] |= 1 << x
        for x in neg_n:
            edge(0, x+1)
        for pair in combinations(neg_n, 2):
            for x in pair:
                edge(Q[pair], x+1)
        for x, missing in zip(neg_q, ordering):
            for pair in combinations(neg_n, 2):
                if pair not in missing:
                    edge(x, Q[pair])
        support = positive | negative
        for x in vertices(support):
            assert ns[x].bit_count() == 4
            fs[x] = support & ~(ns[x] | (1 << x))
        options.append((ns, fs))
    return options


def partial_reason(ns, fs, roots):
    for x in range(99):
        if ns[x] & fs[x]:
            return 'edge_nonedge_conflict'
        for positive, negative in roots:
            if not ((positive | negative) >> x & 1):
                if (ns[x] & positive).bit_count() > 1 or (ns[x] & negative).bit_count() > 1:
                    return 'outside_root_capacity'
    active = [x for x in range(99) if ns[x].bit_count() > 2]
    for x, y in combinations(active, 2):
        common = (ns[x] & ns[y]).bit_count()
        if common > (1 if ns[x] >> y & 1 else 2):
            return 'common_neighbor_capacity'
    return None


def check_internal_options(ids, roots):
    selected = [roots[i] for i in ids]
    count = len(selected)
    options = [root_graph_options(f) for f in selected]
    ns0 = base_graph()
    fs0 = [0]*99
    full = (1 << 99) - 1
    for x in range(15):
        fs0[x] = full & ~(ns0[x] | (1 << x))
        for y in vertices(fs0[x]):
            fs0[y] |= 1 << x
    histogram = Counter()
    survivors = []
    def walk(depth, ns, fs, choices):
        if depth == count:
            survivors.append(choices)
            return
        for j, (on, of) in enumerate(options[depth]):
            nn = [a | b for a, b in zip(ns, on)]
            ff = [a | b for a, b in zip(fs, of)]
            reason = partial_reason(nn, ff, selected)
            if reason:
                histogram[reason] += 6 ** (count-depth-1)
            else:
                walk(depth+1, nn, ff, choices + [j])
    walk(0, ns0, fs0, [])
    assert sum(histogram.values()) + len(survivors) == 6**count
    return dict(rejections=dict(histogram), survivors=survivors)


def support_orbits(supports, group, roots):
    unseen = {tuple(fs) for fs in supports}
    representatives = []
    while unseen:
        rep = min(unseen)
        orbit = {tuple(sorted(g[i] for i in rep)) for g in group}
        assert orbit <= unseen
        unseen -= orbit
        internal = check_internal_options(rep, roots)
        common_negative_neighbors = NMASK
        for i in rep:
            common_negative_neighbors &= roots[i][1]
        representatives.append(dict(roots=rep, orbit_size=len(orbit),
                                    common_negative_neighbors=list(vertices(common_negative_neighbors)),
                                    internal_options=internal))
    return representatives


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--labelled-audit', action='store_true',
                        help='also check every labelled pair/triple without the stabilizer quotient')
    args = parser.parse_args()
    roots = all_roots()
    f = roots[0]
    ids = [i for i, g in enumerate(roots) if compatible(f, g)]
    ns = [0] * len(ids)
    for i, j in combinations(range(len(ids)), 2):
        if compatible(roots[ids[i]], roots[ids[j]]):
            ns[i] |= 1 << j
            ns[j] |= 1 << i
    histogram = Counter()
    edge_count = 0
    triple_edge_rejected = 0
    three = []
    four = []
    for i in range(len(ids)):
        after = ns[i] & ~((1 << (i+1)) - 1)
        edge_count += after.bit_count()
        while after:
            bj = after & -after
            after ^= bj
            j = bj.bit_length() - 1
            three.append([0, ids[i], ids[j]])
            candidates = ns[i] & ns[j] & ~((1 << (j+1)) - 1)
            while candidates:
                bk = candidates & -candidates
                candidates ^= bk
                k = bk.bit_length() - 1
                fs = [f, roots[ids[i]], roots[ids[j]], roots[ids[k]]]
                if any(fs[a][1] & fs[b][1] & fs[c][1] & NMASK
                       for a, b, c in combinations(range(4), 3)):
                    triple_edge_rejected += 1
                b = sum(bool(fs[a][1] & fs[c][1] & NMASK)
                        for a, c in combinations(range(4), 2))
                histogram[b] += 1
                four.append([0, ids[i], ids[j], ids[k]])
    group = root_stabilizer(roots)
    representatives = support_orbits(four, group, roots)
    triple_reps = support_orbits(three, group, roots)
    pair_reps = support_orbits([[0, i] for i in ids], group, roots)
    assert all(not r['internal_options']['survivors'] or r['common_negative_neighbors']
               for r in pair_reps + triple_reps + representatives)
    assert sum(bool(r['internal_options']['survivors']) for r in pair_reps) == 2
    assert sum(bool(r['internal_options']['survivors']) for r in triple_reps) == 1
    assert sum(bool(r['internal_options']['survivors']) for r in representatives) == 1
    labelled_audit = None
    if args.labelled_audit:
        counts = Counter()
        for family in [[0, i] for i in ids] + three:
            common = NMASK
            for i in family:
                common &= roots[i][1]
            if common:
                continue
            outcome = check_internal_options(family, roots)
            assert not outcome['survivors'], family
            counts[len(family)] += 1
        labelled_audit = dict(families_checked=dict(sorted(counts.items())),
                              survivors=0, uses_orbit_quotient=False)
    report = dict(root_count=len(roots), fixed_first=0,
                  compatible_with_first=len(ids), neighbor_graph_edges=edge_count,
                  four_root_with_triple_edge=triple_edge_rejected,
                  four_root_shared_edge_histogram=dict(sorted(histogram.items())),
                  four_root_survivors=len(four), stabilizer_order=len(group),
                  orbit_count=len(representatives), representatives=representatives,
                  triple_orbit_count=len(triple_reps), triple_representatives=triple_reps,
                  pair_orbit_count=len(pair_reps), pair_representatives=pair_reps,
                  labelled_audit=labelled_audit,
                  consequence=dict(intersection_sizes=[0,4], max_roots_at_vertex=2,
                                   max_orthogonal_roots=12,
                                   depends_on_three_roots_common_edge_exclusion=True))
    out = Path(__file__).resolve().parents[3] / 'data' / 'codex_night_20261014'
    (out / 'orthogonal_root_stars.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if 'representatives' not in k}, sort_keys=True))
    print(json.dumps(dict(internal_survivors=[len(r['internal_options']['survivors'])
                                            for r in representatives])))
    print(json.dumps(dict(triple_survivors=[dict(roots=r['roots'], count=len(r['internal_options']['survivors']),
                                              common=r['common_negative_neighbors'])
                                           for r in triple_reps if r['internal_options']['survivors']])))


if __name__ == '__main__':
    main()
