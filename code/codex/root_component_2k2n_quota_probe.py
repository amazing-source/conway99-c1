"""Measure solver-free continuation pruning on exact 2K2N block classes."""

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write, limit_research_process
from root_component_quota_domain_propagation import QuotaDomains, check_certificate, controls


def load_lab_frontier(source, family):
    marker = '\nOUT = next('
    text = source.decode('utf-8-sig')
    assert text.count(marker) == 1
    old = sys.argv[:]
    sys.argv = ['saved_lab_source.py', str(Path(__file__).resolve().parent), family, 'unused', '0', '0', '--sat']
    ns = {'__name__': 'lab_frontier_for_new_continuation', '__file__': 'saved_lab_source.py'}
    try:
        exec(compile(text.split(marker)[0], 'saved_lab_source.py', 'exec'), ns)
    finally:
        sys.argv = old
    # Preserve SAT's preceding profile propagation, but never call its solver.
    ns['SAT'] = False; ns['DUMP'] = 'memory'; ns['DUMP_MAX'] = 1
    return ns


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory', type=Path)
    p.add_argument('--limit', type=int)
    p.add_argument('--stratified', action='store_true', help='First representative of each core only.')
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args(); resources = limit_research_process(1)
    assert not a.output.exists()
    data = json.loads((a.directory/'cases.json').read_text())
    groups = json.loads((a.directory/'isomorphisms.json').read_text())['classes']
    assert data['family'] == '2K2N'
    source = gzip.decompress((a.directory/'lab_source.py.gz').read_bytes())
    assert hashlib.sha256(source).hexdigest() == data['source_sha256']
    ns = load_lab_frontier(source, data['family'])
    report = {'family': '2K2N', 'scope': 'New continuation conditions only; not a repeat or replacement of the LAB census.',
              'resources': resources, 'controls': controls(), 'class_count': len(groups),
              'catalogue_cases': len(data['cases']), 'source_sha256': data['source_sha256'], 'cases': []}
    chosen = []; seen = set()
    for group in groups:
        case = data['cases'][group['representative']]
        if a.stratified and case['core_index'] in seen:
            continue
        seen.add(case['core_index']); chosen.append(group)
    if a.limit is not None:
        chosen = chosen[:a.limit]
    atomic_json_write(a.output, report)
    for group in chosen:
        index = group['representative']; case = data['cases'][index]
        started = time.process_time(); ns['DUMPED'] = []
        frontier = ns['frontier'](case['rows'])
        assert frontier['status'] == 'PASSES_PROFILE_PROPAGATION', frontier
        assert len(ns['DUMPED']) == 1
        inp = ns['DUMPED'][0]; domains = inp['domains_after_propagation']
        assert inp['known_labels'] == case['known_labels'] and inp['outside_labels'] == case['outside_labels']
        engine = QuotaDomains(case['rows'], case['known_labels'], case['outside_labels'], domains)
        result = engine.run()
        assert check_certificate(case['rows'], case['known_labels'], case['outside_labels'], domains, result)
        record = {'case_index': index, 'core_index': case['core_index'], 'boundary_index': case['boundary_index'],
                  'sigma': case['sigma'], 'class_size': len(group['members']),
                  'initial_profile_count': sum(map(len, domains)), 'domain_sizes': list(map(len, domains)),
                  'cpu_seconds': time.process_time()-started, **result}
        if result['removed_count']:
            input_file = a.output.with_name(a.output.stem+'.case%04d.input.json.gz'%index)
            raw = json.dumps({'rows': case['rows'], 'known_labels': case['known_labels'],
                              'outside_labels': case['outside_labels'], 'domains': domains}, separators=(',', ':')).encode()
            input_file.write_bytes(gzip.compress(raw, mtime=0))
            record['input_file'] = str(input_file)
            record['input_sha256'] = hashlib.sha256(input_file.read_bytes()).hexdigest()
        record.pop('kept_indices', None)
        report['cases'].append(record)
        report['status_counts'] = dict(Counter(r['status'] for r in report['cases']))
        report['covered_attachment_count'] = sum(r['class_size'] for r in report['cases'])
        atomic_json_write(a.output, report)
        print(json.dumps({k: v for k, v in record.items() if k not in ('trail', 'domain_sizes')}), flush=True)
        engine.oracle.support.cache_clear(); engine.oracle.targets.cache_clear()
    report['completed_requested_classes'] = True
    report['excluded_attachment_count'] = sum(r['class_size'] for r in report['cases'] if r['status'].startswith('EXCLUDED_'))
    atomic_json_write(a.output, report)
    print(json.dumps({'statuses': report.get('status_counts', {}),
                      'excluded_attachments': report['excluded_attachment_count']}), flush=True)


if __name__ == '__main__':
    main()
