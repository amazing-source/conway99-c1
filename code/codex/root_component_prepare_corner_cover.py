"""Prepare exact coupled corner tables, retaining the source root-choice scope."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys
import time
sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write, limit_research_process
from root_component_low_budget_transport import digest


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory', type=Path)
    p.add_argument('--cover', type=Path, required=True)
    p.add_argument('--index', type=int, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args(); resources = limit_research_process(1)
    progress_file = a.output.with_suffix('.progress.json')
    assert not a.output.exists() and not progress_file.exists()
    source = json.loads(a.cover.read_text(encoding='utf-8-sig'))
    templates = a.directory/'root_component_templates.json'
    template = json.loads(templates.read_text(encoding='utf-8-sig'))['survivors'][a.index]
    record = next(r for r in source['records'] if r['template_index'] == a.index)
    assert record['exhaustive'] and record['usable_as_gram_cover']
    state = {'scope': __doc__, 'template_index': a.index, 'resources': resources,
             'source_cover': str(a.cover), 'source_cover_sha256_lf': digest(a.cover),
             'templates_sha256_lf': digest(templates), 'gram_count': record['gram_count'],
             'source_root_order': source.get('root_order'), 'status': 'RUNNING',
             'processed': 0, 'empty_corner_gram_indices': []}
    atomic_json_write(progress_file, state)
    start = time.process_time()
    def progress(index, empty):
        state['processed'] = index+1
        if empty:
            state['empty_corner_gram_indices'].append(record['source_gram_indices'][index])
        state['cpu_seconds'] = time.process_time()-start
        atomic_json_write(progress_file, state)
        if index == 0 or (index+1) % 10 == 0 or empty:
            print(json.dumps({'processed': index+1, 'total': record['gram_count'],
                              'empty': len(state['empty_corner_gram_indices']),
                              'cpu_seconds': state['cpu_seconds']}), flush=True)
    from root_component_coupled_cover import prepare
    prepared = prepare(template, record, progress)
    result = deepcopy(source)
    result['records'] = [prepared if r['template_index'] == a.index else r for r in result['records']]
    state.update(status='COMPLETE', cpu_seconds=time.process_time()-start,
                 individual_rows=sum(len(t['rows']) for t in prepared['row_signature_tables']),
                 corner_rows=sum(len(t['rows']) for t in prepared['corner_signature_tables']))
    result['coupled_corner_preparation'] = state
    atomic_json_write(a.output, result)
    atomic_json_write(progress_file, state)
    print(json.dumps(state), flush=True)


if __name__ == '__main__':
    main()
