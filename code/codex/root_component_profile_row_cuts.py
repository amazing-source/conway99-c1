"""Separate necessary profile clauses from a missing row's two quotas.

Fix a profile p of x. Future neighbours have features: known vertices
they meet, upper letters they carry, and degree. Their exact feature
totals are t_f. If t_f>t_g, at least t_f-t_g DISTINCT future neighbours
carry f but not g. For any fixed set W of fewer than t_f-t_g vertices,
at least one such neighbour lies outside W and must choose a compatible
profile. Consequently (the original inclusion cut is the case W empty)

  not choose(x,p) OR any choose(y,q), y outside W, with xy possible and f without g.

These clauses concern ONLY the original profile choices. Their validity
does not require fixing the other profiles. They can be learned from a
SAT selection whose possible future edges violate a quota inclusion.
"""

from functools import lru_cache

from root_component_p3_neighbor_support import prepare_profile, edge_failure

if not __debug__:
    raise RuntimeError('Row-cut certificates require assertions; do not use python -O.')


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
        assert cut.get('kind', 'row_quota') in ('row_quota', 'forced_edge_quota', 'continuation_guard')
        if cut.get('kind') == 'continuation_guard':
            from root_component_profile_guard_cut import check_guard_cut
            return check_guard_cut(self.rows,self.known,self.outside,self.domains,cut,self.roots)
        if cut.get('kind') == 'forced_edge_quota':
            assert len(cut['guards']) == 2
            x, pi = cut['guards'][0]; v, pj = cut['guards'][1]
            assert x != v
            fx, f, g = cut['source_feature'], cut['feature'], cut['excluded_feature']
            assert self.targets(x, pi)[fx] == 1
            target = self.targets(v, pj)
            assert target[g] == 1 and target[f] >= 2
            assert self.features[x][pi] & (1 << g) and not self.features[x][pi] & (1 << f)
            assert self.features[v][pj] & (1 << fx)
            assert edge_failure(self.prepared[x][pi], self.prepared[v][pj]) is None
            exceptions = set(cut['exempt_partner_vertices'])
            assert len(exceptions) <= target[f]-1
            alternatives = {(y, qi) for y, qi in self.support(x, pi, fx, 0) if y != v}
            alternatives.update((y, qi) for y, qi in self.support(v, pj, f, g) if y not in exceptions)
            assert tuple(map(tuple, cut['support_options'])) == tuple(sorted(alternatives))
            return True
        x, pi, f, g = (cut[k] for k in ('outside_index', 'profile_index', 'feature', 'excluded_feature'))
        targets = self.targets(x, pi)
        assert targets[f] > targets[g]
        exceptions = set(cut.get('exempt_partner_vertices', []))
        assert len(exceptions) < targets[f]-targets[g]
        assert tuple(map(tuple, cut['support_options'])) == tuple((y,qi) for y,qi in self.support(x,pi,f,g) if y not in exceptions)
        assert cut['demands'] == [targets[f], targets[g]]
        return True

    def separate(self, selected, max_cuts=64):
        assert len(selected) == len(self.domains)
        cuts = []; seen = set(); selected_occurrences = []
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
            selected_occurrences.append(occurrence)
            for f in range(len(targets)):
                for g in range(len(targets)):
                    remaining = occurrence[f] & ~occurrence[g]
                    if targets[f] <= targets[g] or remaining.bit_count() >= targets[f]-targets[g]:
                        continue
                    exceptions = [y for y in range(len(selected)) if remaining & (1 << y)]
                    support = tuple((y,qi) for y,qi in self.support(x,pi,f,g) if y not in exceptions)
                    key = (x, pi, support)
                    if key in seen:
                        continue
                    seen.add(key)
                    assert not any(selected[y] == qi for y, qi in support)
                    cut = {'outside_index': x, 'outside_label': self.outside[x], 'profile_index': pi,
                           'feature': f, 'excluded_feature': g,
                           'feature_name': self.names[f], 'excluded_feature_name': self.names[g],
                           'demands': [targets[f], targets[g]], 'support_options': support,
                           'exempt_partner_vertices': exceptions,
                           'currently_possible_feature_vertices': [y for y in range(len(selected)) if occurrence[f] & (1 << y)],
                           'currently_possible_excluded_feature_vertices': [y for y in range(len(selected)) if occurrence[g] & (1 << y)]}
                    assert self.check_cut(cut)
                    cuts.append(cut)
                    if len(cuts) >= max_cuts:
                        return cuts
        # A singleton quota forces xv. If x consumes v's entire g quota
        # without contributing to f, v must find t_f neighbours in f\g.
        # At most t_f-1 can come from any fixed exception set. The
        # alternatives to xv or to that exception set form a profile clause.
        for x, pi in enumerate(selected):
            for fx, demand in enumerate(self.targets(x, pi)):
                neighbourhood = selected_occurrences[x][fx]
                if demand != 1 or neighbourhood.bit_count() != 1:
                    continue
                v = neighbourhood.bit_length()-1; pj = selected[v]
                targets = self.targets(v, pj); source_features = self.features[x][pi]
                for g, tg in enumerate(targets):
                    if tg != 1 or not source_features & (1 << g):
                        continue
                    for f, tf in enumerate(targets):
                        if tf < 2 or source_features & (1 << f):
                            continue
                        remaining = selected_occurrences[v][f] & ~selected_occurrences[v][g]
                        if remaining.bit_count() >= tf:
                            continue
                        exceptions = [y for y in range(len(selected)) if remaining & (1 << y)]
                        alternatives = {(y, qi) for y, qi in self.support(x, pi, fx, 0) if y != v}
                        alternatives.update((y, qi) for y, qi in self.support(v, pj, f, g) if y not in exceptions)
                        support = tuple(sorted(alternatives)); guards = ((x, pi), (v, pj))
                        key = (tuple(sorted(guards)), support)
                        if key in seen:
                            continue
                        seen.add(key)
                        cut = {'kind': 'forced_edge_quota', 'guards': guards, 'source_feature': fx,
                               'source_feature_name': self.names[fx], 'feature': f, 'excluded_feature': g,
                               'feature_name': self.names[f], 'excluded_feature_name': self.names[g],
                               'target_demands': [tf, tg], 'exempt_partner_vertices': exceptions,
                               'support_options': support}
                        assert self.check_cut(cut)
                        assert not any(selected[y] == qi for y, qi in support)
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
