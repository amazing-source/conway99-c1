"""Exercise the continuation cuts on actual rooted SRG(243,22,1,2) graphs.

The genuine completion is kept explicitly. Extra profile alternatives and
deliberately wrong selections exercise learned clauses; every generated
clause must still be true on the genuine completion. These are controls of
Codex's own necessary conditions, not a repeat of LAB's family enumeration.
No SAT search and no large RUP check is performed here.
"""

import argparse
from collections import Counter
import gzip
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import random
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write, limit_research_process
from root_component_p3_neighbor_support import prepare_profile, edge_failure
from root_component_profile_row_cuts import RowCutOracle, controls as small_row_controls
from root_component_profile_guard_cut import GuardOracle, controls as small_guard_controls

if not __debug__:
    raise RuntimeError('Positive controls require assertions; do not use python -O.')

ROOT = Path(__file__).resolve().parents[2]


def load_graph(path):
    edges = [tuple(map(int, line.split())) for line in path.read_text().splitlines() if line.strip()]
    n = max(max(e) for e in edges) + 1
    neighbours = [set() for _ in range(n)]
    for u, v in edges:
        assert u != v and v not in neighbours[u]
        neighbours[u].add(v); neighbours[v].add(u)
    assert n == 243 and all(len(a) == 22 for a in neighbours)
    for u, v in combinations(range(n), 2):
        assert len(neighbours[u] & neighbours[v]) == (1 if v in neighbours[u] else 2)
    return neighbours


def rooted_block(neighbours, root, known_count, seed):
    upper = neighbours[root]
    pairs = sorted(tuple(sorted((v, next(iter(neighbours[v] & upper))))) for v in upper)
    pairs = sorted(set(pairs))
    assert len(pairs) == 11 and len({v for p in pairs for v in p}) == 22
    letter = {v: 2*i+j for i, pair in enumerate(pairs) for j, v in enumerate(pair)}
    gamma = sorted(set(range(len(neighbours))) - upper - {root})
    labels = {v: tuple(sorted(letter[u] for u in neighbours[v] & upper)) for v in gamma}
    assert len(gamma) == 220 and len(set(labels.values())) == 220
    assert all(len(q) == 2 and q[0]//2 != q[1]//2 for q in labels.values())
    random.Random(seed).shuffle(gamma)
    known, outside = gamma[:known_count], gamma[known_count:]
    rows = [sum(1 << i for i, u in enumerate(known) if u in neighbours[v]) for v in known]
    known_labels = [labels[v] for v in known]
    outside_labels = [labels[v] for v in outside]
    actual = [sorted(i for i, u in enumerate(known) if u in neighbours[v]) for v in outside]
    domains = []
    for q, profile in zip(outside_labels, actual):
        candidates = [profile]
        for i in range(known_count):
            alternative = sorted(set(profile) ^ {i})
            if prepare_profile(rows, known_labels, q, alternative, 11)['valid']:
                candidates.append(alternative)
        # A replacement preserves degree while changing the known-pair quotas.
        for i in profile:
            for j in range(known_count):
                if j in profile:
                    continue
                alternative = sorted(set(profile) - {i} | {j})
                if prepare_profile(rows, known_labels, q, alternative, 11)['valid']:
                    candidates.append(alternative)
            if len(candidates) >= 12:
                break
        unique = list(dict.fromkeys(tuple(p) for p in candidates))
        domains.append([list(p) for p in unique[:12]])
    future = [set(j for j, u in enumerate(outside) if u in neighbours[v]) for v in outside]
    return rows, known_labels, outside_labels, domains, future, known, outside


def clause_true(cut, selected):
    guards = cut.get('guards', [(cut.get('outside_index'), cut.get('profile_index'))])
    return (any(selected[x] != pi for x, pi in guards)
            or any(selected[x] == pi for x, pi in cut['support_options']))


def exercise(path, root, known_count, seed):
    start = time.process_time()
    graph = load_graph(path)
    rows, known, outside, domains, future, known_ids, outside_ids = rooted_block(graph, root, known_count, seed)
    oracle = RowCutOracle(rows, known, outside, domains, root_count=11)
    actual = [0]*len(outside)
    quota_checks = 0; edge_checks = 0
    for x in range(len(outside)):
        for f, target in enumerate(oracle.targets(x, 0)):
            assert target == sum(bool(oracle.features[y][0] & (1 << f)) for y in future[x])
            quota_checks += 1
        for y in future[x]:
            assert edge_failure(oracle.prepared[x][0], oracle.prepared[y][0]) is None
            edge_checks += 1
    # This scans every feature pair, then every forced-edge opportunity.
    assert not oracle.separate(actual, max_cuts=10000)
    counts = Counter(); direct = Counter(); nonempty_exceptions = 0
    for x in range(len(outside)):
        t = oracle.targets(x, 0)
        for f in range(len(t)):
            for g in range(len(t)):
                d = t[f]-t[g]
                if d <= 0 or direct['row_quota'] >= 128:
                    continue
                available = sorted(y for y in future[x]
                                   if oracle.features[y][0] & (1 << f)
                                   and not oracle.features[y][0] & (1 << g))
                exceptions = available[:d-1]
                cut = {'outside_index': x, 'profile_index': 0, 'feature': f, 'excluded_feature': g,
                       'demands': [t[f], t[g]], 'exempt_partner_vertices': exceptions,
                       'support_options': [(y, pi) for y, pi in oracle.support(x, 0, f, g) if y not in exceptions]}
                assert oracle.check_cut(cut) and clause_true(cut, actual)
                direct['row_quota'] += 1; nonempty_exceptions += bool(exceptions)
    # Instantiate two-row clauses on real edges, including the saturated G quota.
    for x in range(len(outside)):
        for v in sorted(future[x]):
            if direct['forced_edge_quota'] >= 128:
                break
            source = oracle.features[x][0]; target = oracle.targets(v, 0)
            for h, th in enumerate(oracle.targets(x, 0)):
                if th != 1 or not oracle.features[v][0] & (1 << h):
                    continue
                for g, tg in enumerate(target):
                    if tg != 1 or not source & (1 << g):
                        continue
                    for f, tf in enumerate(target):
                        if tf < 2 or source & (1 << f) or direct['forced_edge_quota'] >= 128:
                            continue
                        exceptions = sorted(y for y in future[v] if oracle.features[y][0] & (1 << f))[:tf-1]
                        options = {(y, pi) for y, pi in oracle.support(x, 0, h, 0) if y != v}
                        options.update((y, pi) for y, pi in oracle.support(v, 0, f, g) if y not in exceptions)
                        cut = {'kind': 'forced_edge_quota', 'guards': [(x, 0), (v, 0)],
                               'source_feature': h, 'feature': f, 'excluded_feature': g,
                               'target_demands': [tf, tg], 'exempt_partner_vertices': exceptions,
                               'support_options': sorted(options)}
                        assert oracle.check_cut(cut) and clause_true(cut, actual)
                        direct['forced_edge_quota'] += 1; nonempty_exceptions += bool(exceptions)
    rng = random.Random(seed+1000)
    mutable = [x for x, d in enumerate(domains) if len(d) > 1]
    bad_selections = []
    for trial in range(8):
        selected = actual.copy()
        for x in rng.sample(mutable, min(1+trial, len(mutable))):
            selected[x] = rng.randrange(1, len(domains[x]))
        cuts = oracle.separate(selected, max_cuts=512)
        for cut in cuts:
            assert oracle.check_cut(cut)
            assert not clause_true(cut, selected)
            assert clause_true(cut, actual)
            counts[cut.get('kind', 'row_quota')] += 1
        bad_selections.append({'changed_profiles': sum(pi != 0 for pi in selected), 'cuts': len(cuts)})
    # The guard relaxation must contain the actual edge assignment, including
    # when only a proper subset of the profiles is fixed.
    guard = GuardOracle(rows, known, outside, domains, actual, root_count=11)
    guard_checks = 0
    for fixed in ([], list(range(min(3, len(outside)))), list(range(0, len(outside), 2)), list(range(len(outside)))):
        edges, bounds = guard.system(fixed)
        truth = [int(y in future[x]) for x, y in edges]
        for c in bounds:
            value = sum(truth[e] for e in c['edges'])
            assert c['lower'] <= value <= c['upper']
            guard_checks += 1
        assert guard.refute(fixed) is None
    result = {'graph': str(path.relative_to(ROOT)), 'graph_sha256': sha256(path.read_bytes()).hexdigest(),
              'parameters': [243, 22, 1, 2], 'root': root, 'known_vertices': known_ids, 'outside_vertices': outside_ids,
              'seed': seed, 'root_count': 11, 'gamma_degree': 20,
              'domain_sizes': [len(d) for d in domains], 'genuine_selection': actual,
              'quota_equalities_checked': quota_checks, 'actual_directed_edges_allowed': edge_checks,
              'positive_selection_yields_no_cuts': True, 'direct_clauses_preserving_completion': dict(direct),
              'direct_clauses_with_nonempty_exception_set': nonempty_exceptions,
              'generated_clauses_preserving_completion': dict(counts), 'perturbed_selections': bad_selections,
              'guard_bounds_satisfied_by_actual_edges': guard_checks,
              'cpu_seconds': time.process_time()-start}
    print(json.dumps({k: v for k, v in result.items() if k not in ('known_vertices', 'outside_vertices', 'domain_sizes', 'genuine_selection')}), flush=True)
    # lru_cache is shared by all instances; don't retain this graph's supports.
    oracle.support.cache_clear(); oracle.targets.cache_clear()
    return result


def inventory_2k2():
    """Replay the 172 mathematical clauses, without repeating SAT or RUP."""
    base = ROOT/'data/codex_short_columns_20261018'
    directory = base/'shared_2k2_residuals_20261019'
    sources = [('6/547', base/'shared_2k2_core006_b547_continuation'),
               ('51/476', directory/'case002'), ('51/702', directory/'case003'),
               ('75/355', directory/'case004_retry1'), ('88/618', directory/'case005')]
    reports = []; totals = Counter(); malformed_checks = 0
    for name, prefix in sources:
        ip = prefix.with_suffix('.row_cut_input.json')
        lp = prefix.with_suffix('.row_cut_learning.json')
        cp = prefix.with_suffix('.row_cut_cnf.json.gz')
        inp = json.loads(ip.read_text(encoding='utf-8'))
        learning = json.loads(lp.read_text(encoding='utf-8'))
        oracle = RowCutOracle(inp['rows'], inp['known_labels'], inp['outside_labels'], inp['domains'])
        literals = inp['profile_literals']; clauses = []; kinds = Counter()
        for record in learning['rounds']:
            for cut in record.get('violated_cuts', []):
                assert oracle.check_cut(cut)
                kind = cut.get('kind', 'row_quota'); kinds[kind] += 1
                guards = cut.get('guards', [(cut.get('outside_index'), cut.get('profile_index'))])
                clauses.append([-literals[x][pi] for x, pi in guards]
                               + [literals[x][pi] for x, pi in cut['support_options']])
                if malformed_checks == 0:
                    try:
                        oracle.check_cut({**cut, 'kind': 'unproved_unknown_kind'})
                    except AssertionError:
                        malformed_checks += 1
                    else:
                        raise AssertionError('An unknown mathematical rule was accepted.')
        assert set(kinds) <= {'row_quota', 'forced_edge_quota'}
        assert len(clauses) == learning['clauses_added']
        cnf = json.loads(gzip.decompress(cp.read_bytes()))
        assert not clauses or cnf[-len(clauses):] == clauses
        reports.append({'case': name, 'prefix': str(prefix.relative_to(ROOT)), 'kinds': dict(kinds),
                        'mathematical_clauses_replayed': len(clauses), 'exact_cnf_suffix': True,
                        'input_sha256': sha256(ip.read_bytes()).hexdigest(),
                        'learning_sha256': sha256(lp.read_bytes()).hexdigest(),
                        'cnf_archive_sha256': sha256(cp.read_bytes()).hexdigest()})
        totals.update(kinds)
        oracle.support.cache_clear(); oracle.targets.cache_clear()
    assert totals == Counter(row_quota=99, forced_edge_quota=73)
    optimized_rejections = []
    for module in ('root_component_profile_row_cuts', 'root_component_profile_guard_cut'):
        code = 'import sys; sys.path.insert(0, ' + repr(str(Path(__file__).resolve().parent)) + '); import ' + module
        run = subprocess.run([sys.executable, '-I', '-O', '-c', code], capture_output=True, text=True)
        assert run.returncode != 0 and 'do not use python -O' in run.stderr
        optimized_rejections.append(module)
    return {'scope': 'Replay of the mathematical clause instances only; existing RUP certificates were not rerun.',
            'cases': reports, 'total_kinds': dict(totals), 'continuation_guard_used': False,
            'unknown_kind_rejected': malformed_checks == 1, 'optimized_python_rejected': optimized_rejections}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--inventory-only', action='store_true', help='Replay existing 2K2 clauses; do not rerun graph controls.')
    a = p.parse_args(); resources = limit_research_process(1)
    if a.inventory_only:
        report = {'resources': resources, **inventory_2k2()}
        atomic_json_write(a.output, report, indent=2)
        print(json.dumps({'total_kinds': report['total_kinds'], 'all_exact_suffixes': True,
                          'optimized_python_rejected': report['optimized_python_rejected']}), flush=True)
        return
    results = []
    for filename in ('bvls243.edges', 'twin243_switched.edges'):
        for root, size, seed in ((0, 20, 191019), (1, 180, 191020)):
            results.append(exercise(ROOT/'data/srg243'/filename, root, size, seed))
    assert sum(r['direct_clauses_preserving_completion'].get('forced_edge_quota', 0) for r in results) > 0
    assert sum(sum(r['generated_clauses_preserving_completion'].values()) for r in results) > 0
    report = {'scope': 'Positive controls of necessary continuation cuts; not a family census or a Conway construction.',
              'resources': resources, 'rook_row_control': small_row_controls(), 'rook_guard_control': small_guard_controls(),
              'cases': results, 'all_actual_completions_preserved': True}
    atomic_json_write(a.output, report, indent=2)


if __name__ == '__main__':
    main()
