"""Finish a saved continuation certificate without repeating its SAT search.

The learned clauses are reconstructed from their mathematical certificates
on unrestricted profile domains, then matched to the saved CNF suffix. The
native RUP checker verifies the saved refutation of that augmented CNF.
"""

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import limit_research_process, atomic_json_write
from root_component_profile_row_cuts import RowCutOracle
from root_component_native_rup import check_native_rup


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def check_saved(prefix, output, native_timeout=600):
    resources = limit_research_process(1)
    paths = {name: prefix.with_suffix(suffix) for name, suffix in (
        ('input', '.row_cut_input.json'), ('learning', '.row_cut_learning.json'),
        ('cnf', '.row_cut_cnf.json.gz'), ('proof', '.row_cut_proof.rup.gz'))}
    inp = json.loads(paths['input'].read_text(encoding='utf-8'))
    learning = json.loads(paths['learning'].read_text(encoding='utf-8'))
    cnf = json.loads(gzip.decompress(paths['cnf'].read_bytes()))
    assert learning['terminal_status'] == 'UNSAT_WITH_NECESSARY_ROW_CUTS'
    assert learning['rounds'][-1]['answer'] is False
    oracle = RowCutOracle(inp['rows'], inp['known_labels'], inp['outside_labels'], inp['domains'])
    literals = inp['profile_literals']; appended = []; kinds = Counter()
    for record in learning['rounds']:
        for cut in record.get('violated_cuts', []):
            assert oracle.check_cut(cut)
            guards = cut.get('guards', [(cut.get('outside_index'), cut.get('profile_index'))])
            clause = [-literals[y][pi] for y, pi in guards]
            clause += [literals[y][pi] for y, pi in cut['support_options']]
            appended.append(clause); kinds[cut.get('kind', 'row_quota')] += 1
    assert len(appended) == learning['clauses_added']
    assert not appended or cnf[-len(appended):] == appended
    print(json.dumps({'necessary_clauses_checked': len(appended), 'kinds': kinds}), flush=True)
    with gzip.open(paths['proof'], 'rt', encoding='ascii') as proof:
        checked = check_native_rup(cnf, proof, output, native_timeout)
    report = {
        'scope': 'Only this saved block/attachment; no census or family completeness assertion.',
        'status': 'EXCLUDED_ATTACHMENT_BY_NECESSARY_CONTINUATION_CUTS',
        'empty_clause_verified': True, 'proof_check': checked, 'resources': resources,
        'clauses_added': len(appended), 'kinds': dict(kinds),
        'sat_selections_refuted': sum(r['answer'] is True for r in learning['rounds']),
        'solve_learning_cpu_seconds': learning['rounds'][-1]['cpu_seconds'],
        'learned_clauses_checked_against_full_domains': True,
        'exact_appended_clauses_match': True,
        'files': {str(p): sha256(p) for p in paths.values()},
    }
    atomic_json_write(output, report)
    print(json.dumps({'status': report['status'], 'output': str(output), 'proof_check': checked}), flush=True)
    return report


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('prefix', type=Path)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--native-timeout', type=float, default=600)
    a = p.parse_args()
    assert not a.output.exists(), 'Use a new certificate filename.'
    check_saved(a.prefix, a.output, a.native_timeout)
