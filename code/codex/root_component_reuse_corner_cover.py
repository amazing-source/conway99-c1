"""Restrict existing exact corner tables to an unchanged subset of Gram values.

No Gram is excluded here. The anchor frame, lift, template and root budget
must agree exactly. Table selectors are remapped by their complete anchor
value tuple; catalog state indices are retained unchanged.
"""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write, limit_research_process
from root_component_low_budget_transport import digest


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cover', type=Path, required=True)
    p.add_argument('--prepared', type=Path, required=True)
    p.add_argument('--index', type=int, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args(); limit_research_process(1)
    assert not a.output.exists()
    source = json.loads(a.cover.read_text(encoding='utf-8-sig'))
    result = deepcopy(source)
    current = next(r for r in result['records'] if r['template_index'] == a.index)
    old = json.loads(a.prepared.read_text(encoding='utf-8-sig'))['cover']
    for key in ('template_index','anchors','anchor_pairs','lift_matrix','root_prism_budget'):
        assert current[key] == old[key], f'Different frame: {key}'
    assert current['exhaustive'] and current['usable_as_gram_cover']
    previous = {tuple(values): i for i, values in enumerate(old['gram_anchor_values'])}
    assert len(previous) == old['gram_count']
    old_to_new = {previous[tuple(values)]: i for i, values in enumerate(current['gram_anchor_values'])}
    assert len(old_to_new) == current['gram_count']
    for field in ('row_signature_tables','corner_signature_tables'):
        tables = deepcopy(old[field]); assert len(tables) == 21
        for table in tables:
            table['rows'] = [[old_to_new[row[0]], *row[1:]] for row in table['rows'] if row[0] in old_to_new]
            assert {row[0] for row in table['rows']} == set(range(current['gram_count']))
        current[field] = tables
    result['corner_table_reuse'] = {'scope': __doc__, 'template_index': a.index,
        'input_cover': str(a.cover), 'input_cover_sha256_lf': digest(a.cover),
        'prepared_source': str(a.prepared), 'prepared_source_sha256_lf': digest(a.prepared),
        'source_gram_count': old['gram_count'], 'retained_gram_count': current['gram_count'],
        'old_to_new_gram_indices': old_to_new, 'newly_excluded_grams': 0}
    atomic_json_write(a.output, result)
    print(json.dumps({'template_index': a.index, 'gram_count': current['gram_count'],
                     'individual_rows': sum(len(t['rows']) for t in current['row_signature_tables']),
                     'corner_rows': sum(len(t['rows']) for t in current['corner_signature_tables'])}))


if __name__ == '__main__':
    main()
