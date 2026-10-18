"""Summarize matching-level pilot reports, preserving all open branches."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import statistics
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write
from root_component_rotated_gram import unsafe_product_reports
from root_component_complete_star import mate_flip_orbits
from root_component_root_order import root_choice_requirements


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('reports', type=Path, nargs='+')
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    rows = []; timings = []; builds = []; identities = set()
    for path in args.reports:
        raw = path.read_bytes(); report = json.loads(raw)
        if any(unsafe_product_reports(report)):
            raise ValueError(f'{path}: withdrawn product-domain encoding; recompute before aggregation.')
        identity = report['source_sha256'], report['template_index']
        assert identity not in identities, 'Supply one complete/current report per template.'
        identities.add(identity)
        branches = report['matching_branches']
        cover = set(range(len(report['matching_cover'])))
        partition = report.get('matching_partition', 'labelled')
        expected = {i: [i] for i in cover}
        if partition == 'mate_flip_orbits':
            orbits = mate_flip_orbits(report['root_line'], report['matching_cover'])
            assert orbits == report['mate_flip_orbit_cover']
            expected = {o['representative']: o['members'] for o in orbits['orbits']}
        elif partition == 'all_in_one':
            assert report['options']['all_matchings_variable'] and not report['options']['transport']
            expected = {None: sorted(cover)}
        else:
            assert partition == 'labelled'
        keys = {b['matching_index'] for b in branches}
        assert len(keys) == len(branches) and keys <= set(expected)
        for branch in branches:
            assert branch.get('covered_matching_indices', [branch['matching_index']]) == expected[branch['matching_index']]
        processed = {i for key in keys for i in expected[key]}
        counts = Counter(b['status'] for b in branches)
        excluded = {i for b in branches if b['status']=='INFEASIBLE' for i in expected[b['matching_index']]}
        closed = excluded == cover
        assert (report['status'] == 'INFEASIBLE') == closed
        timing = sum(b['cpu_seconds'] for b in branches)
        build = sum(b['build_cpu_seconds'] for b in branches)
        row = {'report': path.as_posix(), 'sha256_lf': hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest(),
               'source_file': report['source_file'], 'template_index': report['template_index'],
               'grids': 21-len(report['template']['nongrid_edges']), 'root_line': report['root_line'],
               'matching_partition': partition, 'solver_branch_count': len(branches),
               'excluded_labelled_matchings': len(excluded),
               'root_choice_requirements': sorted(root_choice_requirements(report)),
               'global_minimum_components': report.get('global_minimum_components'),
               'usable_in_arbitrary_low_budget_root_frontier': not root_choice_requirements(report) and report.get('global_minimum_components') is None,
               'matching_count': len(cover), 'processed': len(processed), 'unprocessed': len(cover-processed),
               'verdict_counts': dict(counts), 'status': 'INFEASIBLE' if closed else report['status'],
               'build_cpu_seconds': build, 'solve_cpu_seconds': timing,
               'total_cpu_seconds': build+timing, 'peak_rss_bytes': report.get('process_peak_rss_bytes',0)}
        rows.append(row)
        timings.extend(b['cpu_seconds'] for b in branches)
        builds.extend(b['build_cpu_seconds'] for b in branches)
        print(json.dumps(row), flush=True)
    output = {'scope': __doc__, 'templates': len(rows),
              'excluded_templates': sum(r['status']=='INFEASIBLE' for r in rows),
              'matching_count': sum(r['matching_count'] for r in rows),
              'matching_verdict_counts': dict(sum((Counter(r['verdict_counts']) for r in rows), Counter())),
              'unprocessed_matchings': sum(r['unprocessed'] for r in rows),
              'build_cpu_seconds': sum(builds), 'solve_cpu_seconds': sum(timings),
              'solve_cpu_min_median_max': [min(timings), statistics.median(timings), max(timings)] if timings else [],
              'build_cpu_min_median_max': [min(builds), statistics.median(builds), max(builds)] if builds else [],
              'maximum_peak_rss_bytes': max(r['peak_rss_bytes'] for r in rows),
              'portable_unsat_proof': False, 'global_cmin3_exclusion': False, 'records': rows}
    atomic_json_write(args.output, output)
    print(json.dumps({k:v for k,v in output.items() if k not in ('records','scope')}), flush=True)


if __name__ == '__main__':
    main()
