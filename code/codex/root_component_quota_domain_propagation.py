"""Delete impossible profiles by exact future-neighbour quota deficits.

For fixed (x,p), at least t_F-t_G distinct neighbours carry F without G.
If all currently compatible profiles provide fewer vertices, delete p.
The certificate is a sequence of the already proved row-quota clauses:
every positive support outside the small exception set was deleted earlier.
No selection, SAT solver, LP tolerance, or graph symmetry is used here.
"""

from itertools import combinations

from root_component_profile_row_cuts import RowCutOracle
from root_component_p3_neighbor_support import edge_failure

if not __debug__:
    raise RuntimeError('Quota propagation requires assertions; do not use python -O.')


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length()-1
        mask ^= bit


class QuotaDomains:
    def __init__(self, rows, known, outside, domains, root_count=7):
        self.oracle = RowCutOracle(rows, known, outside, domains, root_count)
        self.entries = [(x, pi) for x, d in enumerate(domains) for pi in range(len(d))]
        self.vertex = [x for x, _ in self.entries]
        self.vertex_masks = [0]*len(domains)
        self.feature_masks = [0]*len(self.oracle.names)
        nk = len(rows); zero = [0]*nk; upper_zero = [0]*(2*root_count)
        valid = 0
        for i, (x, pi) in enumerate(self.entries):
            bit = 1 << i; a = self.oracle.prepared[x][pi]
            self.vertex_masks[x] |= bit
            for f in bits(self.oracle.features[x][pi]):
                self.feature_masks[f] |= bit
            for u in bits(a['zero']):
                zero[u] |= bit
            for l in bits(a['upper_zero']):
                upper_zero[l] |= bit
            assert a['valid'], 'The initial profile domains must already have nonnegative quotas.'
            if a['degree_remaining'] > 0:
                valid |= bit
        assert all(self.vertex_masks), 'An initially empty domain must be handled before this propagator.'
        known_masks = self.feature_masks[2:2+nk]
        letter_masks = self.feature_masks[2+nk:]
        self.compatible = []
        for x, pi in self.entries:
            a = self.oracle.prepared[x][pi]
            if not a['degree_remaining']:
                self.compatible.append(0)
                continue
            allowed = valid & ~self.vertex_masks[x]
            own_known = list(bits(a['mask'])); own_letters = list(bits(a['letters']))
            assert len(own_letters) == 2
            # Known common neighbours >=2, or a shared letter plus >=1 known.
            shares_known = 0
            for u in own_known:
                shares_known |= known_masks[u]
            shares_letter = letter_masks[own_letters[0]] | letter_masks[own_letters[1]]
            allowed &= ~(shares_known & shares_letter)
            allowed &= ~(letter_masks[own_letters[0]] & letter_masks[own_letters[1]])
            for u, v in combinations(own_known, 2):
                allowed &= ~(known_masks[u] & known_masks[v])
            for u in own_known:
                allowed &= ~zero[u]
            for u in bits(a['zero']):
                allowed &= ~known_masks[u]
            for l in own_letters:
                allowed &= ~upper_zero[l]
            for l in bits(a['upper_zero']):
                allowed &= ~letter_masks[l]
            self.compatible.append(allowed)
        self.demands = []
        for x, pi in self.entries:
            t = self.oracle.targets(x, pi)
            self.demands.append([(f, g, tf-tg) for f, tf in enumerate(t)
                                 for g, tg in enumerate(t) if tf > tg])

    def check_compatibility_kernel(self):
        count = 0
        for i, (x, pi) in enumerate(self.entries):
            for j, (y, qi) in enumerate(self.entries):
                expected = x != y and edge_failure(self.oracle.prepared[x][pi], self.oracle.prepared[y][qi]) is None
                assert bool(self.compatible[i] & (1 << j)) == expected
                count += 1
        return count

    def small_cover(self, options, threshold):
        """Return its distinct vertices if fewer than threshold; else None."""
        cover = []
        while options:
            i = (options & -options).bit_length()-1
            x = self.vertex[i]; cover.append(x)
            if len(cover) >= threshold:
                return None
            options &= ~self.vertex_masks[x]
        return cover

    def run(self):
        active = (1 << len(self.entries))-1
        trail = []; iterations = 0
        while True:
            iterations += 1; changed = False
            for i, (x, pi) in enumerate(self.entries):
                if not active & (1 << i):
                    continue
                allowed = self.compatible[i] & active
                for f, g, difference in self.demands[i]:
                    options = allowed & self.feature_masks[f] & ~self.feature_masks[g]
                    if difference == 1 and options:
                        continue
                    exceptions = self.small_cover(options, difference)
                    if exceptions is None:
                        continue
                    target = self.oracle.targets(x, pi)
                    trail.append({'outside_index': x, 'profile_index': pi, 'feature': f, 'excluded_feature': g,
                                  'demands': [target[f], target[g]], 'exempt_partner_vertices': sorted(exceptions)})
                    active ^= 1 << i; changed = True
                    if not active & self.vertex_masks[x]:
                        return {'status': 'EXCLUDED_BY_QUOTA_DOMAIN_PROPAGATION', 'empty_domain': x,
                                'removed_count': len(trail), 'iterations': iterations, 'trail': trail}
                    break
            if not changed:
                return {'status': 'PASSES_QUOTA_DOMAIN_PROPAGATION', 'removed_count': len(trail),
                        'iterations': iterations, 'trail': trail,
                        'kept_indices': [[pi for i, (y, pi) in enumerate(self.entries) if y == x and active & (1 << i)]
                                         for x in range(len(self.vertex_masks))]}


def check_certificate(rows, known, outside, domains, result, root_count=7):
    """Replay using the original edge predicate and full-support row oracle."""
    oracle = RowCutOracle(rows, known, outside, domains, root_count)
    active = [set(range(len(d))) for d in domains]
    for step in result['trail']:
        x, pi = step['outside_index'], step['profile_index']
        assert pi in active[x]
        exceptions = set(step['exempt_partner_vertices'])
        support = [(y, qi) for y, qi in oracle.support(x, pi, step['feature'], step['excluded_feature'])
                   if y not in exceptions]
        assert oracle.check_cut({**step, 'support_options': support})
        assert all(qi not in active[y] for y, qi in support)
        active[x].remove(pi)
    assert len(result['trail']) == result['removed_count']
    if result['status'] == 'EXCLUDED_BY_QUOTA_DOMAIN_PROPAGATION':
        assert not active[result['empty_domain']]
    else:
        assert result['status'] == 'PASSES_QUOTA_DOMAIN_PROPAGATION'
        if 'kept_indices' in result:
            assert result['kept_indices'] == [sorted(d) for d in active]
        assert all(active)
    oracle.support.cache_clear(); oracle.targets.cache_clear()
    return True


def controls():
    from pathlib import Path
    from root_component_row_cut_positive_controls import load_graph, rooted_block
    root = Path(__file__).resolve().parents[2]
    graph = load_graph(root/'data/srg243/bvls243.edges')
    rows, known, outside, domains, _, _, _ = rooted_block(graph, 1, 180, 191020)
    engine = QuotaDomains(rows, known, outside, domains, 11)
    pairs = engine.check_compatibility_kernel()
    positive = engine.run()
    assert positive['status'] == 'PASSES_QUOTA_DOMAIN_PROPAGATION'
    assert all(0 in d for d in positive['kept_indices'])
    assert check_certificate(rows, known, outside, domains, positive, 11)
    rows = [0]; known = [(0, 2)]; outside = [(0, 3), (1, 2), (1, 3)]
    domains = [[[0]], [[0]], [[0]]]
    engine = QuotaDomains(rows, known, outside, domains, 2)
    pairs += engine.check_compatibility_kernel()
    negative = engine.run()
    assert negative['status'] == 'EXCLUDED_BY_QUOTA_DOMAIN_PROPAGATION'
    assert check_certificate(rows, known, outside, domains, negative, 2)
    try:
        check_certificate(rows, known, outside, domains, {**negative, 'trail': []}, 2)
    except AssertionError:
        pass
    else:
        raise AssertionError('A damaged deletion certificate was accepted.')
    return {'actual_srg243_preserved': True, 'positive_removed_alternatives': positive['removed_count'],
            'compatibility_pairs_compared': pairs, 'impossible_rook_profile_refuted': negative,
            'damaged_certificate_rejected': True}
