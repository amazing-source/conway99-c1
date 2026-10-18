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
        identity = report['source_sha256'], report['template_index']
        assert identity not in identities, 'Supply one complete/current report per template.'
        identities.add(identity)
        branches = report['matching_branches']
        cover = set(range(len(report['matching_cover'])))
        processed = {b['matching_index'] for b in branches}
        assert len(processed) == len(branches) and processed <= cover
        counts = Counter(b['status'] for b in branches)
        closed = processed == cover and counts['INFEASIBLE'] == len(cover)
        assert (report['status'] == 'INFEASIBLE') == closed
        timing = sum(b['cpu_seconds'] for b in branches)
        build = sum(b['build_cpu_seconds'] for b in branches)
        row = {'report': path.as_posix(), 'sha256_lf': hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest(),
               'source_file': report['source_file'], 'template_index': report['template_index'],
               'grids': 21-len(report['template']['nongrid_edges']), 'root_line': report['root_line'],
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
