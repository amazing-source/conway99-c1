"""Separate necessary profile clauses from a missing row's two quotas.

Fix a profile p of x. Future neighbours have features: known vertices
they meet, upper letters they carry, and degree. Their exact feature
totals are t_f. If t_f>t_g, at least one future neighbour carries f but
not g. It must select a profile allowing adjacency to x. Consequently

  not choose(x,p) OR any choose(y,q) with xy locally possible and f without g.

These clauses concern ONLY the original profile choices. Their validity
does not require fixing the other profiles. They can be learned from a
SAT selection whose possible future edges violate a quota inclusion.
"""

from functools import lru_cache

from root_component_p3_neighbor_support import prepare_profile, edge_failure


class RowCutOracle:
    def __init__(self, rows, known_labels, outside_labels, domains, root_count=7):
        self.rows = rows; self.known = known_labels; self.outside = outside_labels
        self.domains = domains; self.roots = root_count; self.nk = len(rows)
        self.names = [('zero', None), ('degree', None)] + [('known', v) for v in range(self.nk)]
        self.names += [('letter', l) for l in range(2*root_count)]
        self.prepared = [[prepare_profile(rows, known_labels, q, p, root_count) for p in domain]
                         for q, domain in zip(outside_labels, domains)]
        self.features = [[2 | (a['mask'] << 2) | (a['letters'] << (2+self.nk)) for a in domain]
                         for domain in self.prepared]

    @lru_cache(None)
    def targets(self, x, pi):
        q = self.outside[x]; p = self.domains[x][pi]; a = self.prepared[x][pi]
        roots = {l // 2 for l in q}
        values = [0, 2*self.roots-2-len(p)]
        values += [2-int(v in p)-len(set(q) & set(self.known[v]))-(a['mask'] & row).bit_count()
                   for v, row in enumerate(self.rows)]
        values += [(1 if l // 2 in roots else 2)-sum(l in self.known[v] for v in p)
                   for l in range(2*self.roots)]
        return tuple(values)

    @lru_cache(None)
    def support(self, x, pi, f, g):
        a = self.prepared[x][pi]; answer = []
        for y, domain in enumerate(self.prepared):
            if x == y:
                continue
            for qi, b in enumerate(domain):
                features = self.features[y][qi]
                if features & (1 << f) and not features & (1 << g) and edge_failure(a, b) is None:
                    answer.append((y, qi))
        return tuple(answer)

    def check_cut(self, cut):
        x, pi, f, g = (cut[k] for k in ('outside_index', 'profile_index', 'feature', 'excluded_feature'))
        targets = self.targets(x, pi)
        assert targets[f] > targets[g]
        assert tuple(map(tuple, cut['support_options'])) == self.support(x, pi, f, g)
        assert cut['demands'] == [targets[f], targets[g]]
        return True

    def separate(self, selected, max_cuts=64):
        assert len(selected) == len(self.domains)
        cuts = []; seen = set()
        for x, pi in enumerate(selected):
            a = self.prepared[x][pi]; occurrence = [0] * len(self.names)
            for y, qi in enumerate(selected):
                if y == x or edge_failure(a, self.prepared[y][qi]) is not None:
                    continue
                features = self.features[y][qi]
                while features:
                    bit = features & -features; features ^= bit
                    occurrence[bit.bit_length()-1] |= 1 << y
            targets = self.targets(x, pi)
            for f in range(len(targets)):
                for g in range(len(targets)):
                    if targets[f] <= targets[g] or occurrence[f] & ~occurrence[g]:
                        continue
                    support = self.support(x, pi, f, g)
                    key = (x, pi, support)
                    if key in seen:
                        continue
                    seen.add(key)
                    assert not any(selected[y] == qi for y, qi in support)
                    cut = {'outside_index': x, 'outside_label': self.outside[x], 'profile_index': pi,
                           'feature': f, 'excluded_feature': g,
                           'feature_name': self.names[f], 'excluded_feature_name': self.names[g],
                           'demands': [targets[f], targets[g]], 'support_options': support,
                           'currently_possible_feature_vertices': [y for y in range(len(selected)) if occurrence[f] & (1 << y)],
                           'currently_possible_excluded_feature_vertices': [y for y in range(len(selected)) if occurrence[g] & (1 << y)]}
                    assert self.check_cut(cut)
                    cuts.append(cut)
                    if len(cuts) >= max_cuts:
                        return cuts
        return cuts


def controls():
    oracle = RowCutOracle([0], [(0, 2)], [(0, 3), (1, 2), (1, 3)],
                          [[[0]], [[0]], [[], [0]]], root_count=2)
    assert not oracle.separate([0, 0, 0]), 'The actual rooted 3x3 rook graph must pass.'
    cuts = oracle.separate([0, 0, 1])
    assert cuts and all(oracle.check_cut(c) for c in cuts)
    return {'actual_rook_completion_passes': True, 'impossible_selection_cuts': cuts}
