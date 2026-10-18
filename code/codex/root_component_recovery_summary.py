"""Merge corrected fixed-Gram exclusions without hiding unfinished branches.

Matching-group and full-code reports can be combined only when their
ordered component code cover, root, part and Gram values agree exactly.
This is a provenance ledger, not an independent UNSAT certificate checker.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_low_budget_transport import digest
from root_component_resources import atomic_json_write
from root_component_rotated_gram import unsafe_product_reports


def merge(gram_cover, template_index, reports, minimal_root=False):
    cover = next(r for r in json.loads(gram_cover.read_text())['records']
                 if r['template_index'] == template_index)
    assert cover['exhaustive'] and cover['usable_as_gram_cover']
    remaining = dict(zip(cover['source_gram_indices'], cover['gram_anchor_values']))
    cases = {}; sources = []; frontier_hashes = set(); profile_hashes = set()
    for path in reports:
        report = json.loads(path.read_text(encoding='utf-8-sig'))
        assert not list(unsafe_product_reports(report)), f'Withdrawn product encoding: {path}'
        options = report.get('options', {})
        assert minimal_root or not options.get('minimum_prism_root',False), (
            f'Minimum-root exclusion cannot enter an arbitrary-root ledger: {path}')
        for record in report.get('records', []):
            if record['template_index'] != template_index:
                continue
            for case in record.get('cases', []):
                gi = case['gram_index']
                if gi not in remaining:
                    continue
                assert case['gram_anchor_values'] == remaining[gi], path
                codes = case['component_codes']
                assert codes and len({tuple(c) for c in codes}) == len(codes)
                identity = (case['component_root'], case['component_part'], codes)
                if gi not in cases:
                    cases[gi] = {'identity': identity, 'exclusions': {}, 'attempts': Counter()}
                merged = cases[gi]
                assert merged['identity'] == identity, f'Incompatible component cover: {path}'
                frontier_hashes.add(options['low_budget_cover_sha256_lf'])
                profile_hashes.add(options['residual_gram_profiles_sha256_lf'])
                sources.append({'path': str(path), 'sha256_lf': digest(path)})
                for i, branch in enumerate(case.get('matching_branches', [])):
                    mi = branch['matching_index']
                    assert mi in case['matching_cover']
                    covered = [ci for ci, code in enumerate(codes) if code[1] == mi]
                    assert covered and len(covered) == branch['component_code_count']
                    merged['attempts'][branch['status']] += 1
                    if branch['status'] == 'INFEASIBLE':
                        for ci in covered:
                            merged['exclusions'].setdefault(ci, {'source': str(path),
                                'kind': 'matching_group', 'branch_index': i, 'matching_index': mi})
                for i, branch in enumerate(case.get('branches', [])):
                    ci = branch['component_index']
                    assert codes[ci] == branch['code']
                    merged['attempts'][branch['status']] += 1
                    if branch['status'] == 'INFEASIBLE':
                        merged['exclusions'].setdefault(ci, {'source': str(path),
                            'kind': 'full_component_code', 'branch_index': i})
    assert len(frontier_hashes) <= 1 and len(profile_hashes) <= 1
    records = []
    for gi, values in remaining.items():
        if gi not in cases:
            records.append({'gram_index': gi, 'status': 'NOT_RUN'})
            continue
        merged = cases[gi]; root, part, codes = merged['identity']
        excluded = merged['exclusions']; open_indices = sorted(set(range(len(codes)))-set(excluded))
        records.append({'gram_index': gi, 'gram_anchor_values': values,
            'status': 'OPEN' if open_indices else 'EXCLUDED',
            'component_root': root, 'component_part': part, 'component_codes': codes,
            'ordered_component_code_cover_sha256': hashlib.sha256(
                json.dumps(codes, separators=(',', ':')).encode()).hexdigest(),
            'code_count': len(codes), 'excluded_code_count': len(excluded),
            'open_code_indices': open_indices, 'exclusions': excluded,
            'solver_attempt_counts': dict(merged['attempts'])})
    return {'scope': __doc__, 'template_index': template_index,
        'global_minimum_components': 4, 'chosen_root_prism_budget': 51,
        'requires_globally_minimal_root': minimal_root,
        'usable_in_arbitrary_low_budget_root_frontier': not minimal_root,
        'gram_cover': str(gram_cover), 'gram_cover_sha256_lf': digest(gram_cover),
        'required_gram_count': len(remaining), 'records': records,
        'counts': dict(Counter(r['status'] for r in records)),
        'template_excluded': all(r['status'] == 'EXCLUDED' for r in records),
        'sources': sources, 'portable_unsat_proof': False,
        'global_conway_exclusion': False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--gram-cover', type=Path, required=True)
    p.add_argument('--index', type=int, required=True)
    p.add_argument('--reports', type=Path, nargs='+', required=True)
    p.add_argument('--minimal-root', action='store_true')
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    result = merge(args.gram_cover, args.index, args.reports, args.minimal_root)
    atomic_json_write(args.output, result)
    print(json.dumps({'counts': result['counts'], 'template_excluded': result['template_excluded'],
        'code_counts': [(r['gram_index'], r.get('excluded_code_count'), r.get('code_count'))
                        for r in result['records']]}))


if __name__ == '__main__':
    main()
