"""Export an omitted SAT witness from one LAB py_extend boundary.

The LAB source is read and instrumented in memory, never edited. This
is for studying continuation, not for repeating a peer's verification.
The exact unmodified source is archived alongside the exported input.
"""

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import limit_research_process, atomic_json_write


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('lab_source', type=Path); p.add_argument('boundary', type=Path)
    p.add_argument('--index', type=int, required=True)
    p.add_argument('--family', choices=('P3N', '2K2N', 'P3', '2K2'), default='P3N')
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--row-cut-rounds', type=int, default=0)
    p.add_argument('--row-cut-cpu-seconds', type=float, default=60)
    p.add_argument('--extend-rows', type=int, nargs='*', default=[])
    args = p.parse_args()
    assert not args.output.exists(), 'Use a new output name.'
    resources = limit_research_process(1)
    raw = args.lab_source.read_bytes(); source = raw.decode('utf-8-sig')
    marker = "            out['status'] = 'SAT_KNOWN_ROWS_COMPLETE'"
    assert source.count(marker) == 1, 'LAB source changed; inspect its SAT branch before updating the hook.'
    archive = args.output.with_suffix('.lab_source.py.gz')
    archive.write_bytes(gzip.compress(raw, mtime=0))

    def save_selection(rows, labels, outside, domains, literals, model):
        positive = {v for v in model if v > 0}
        indices = [[i for i, literal in enumerate(row) if literal in positive] for row in literals]
        assert all(len(ids) == 1 for ids in indices)
        selected = [domain[ids[0]] for domain, ids in zip(domains, indices)]
        data = {'scope': 'A SAT selection completing the known rows only; outside edges remain unknown.',
                'family': args.family, 'boundary_file': str(args.boundary), 'boundary_index': args.index,
                'lab_source_sha256': hashlib.sha256(raw).hexdigest(), 'source_archive': str(archive),
                'resources': resources, 'rows': rows, 'known_labels': labels, 'outside_labels': outside,
                'domains': domains, 'selected_indices': [ids[0] for ids in indices], 'profiles': selected}
        args.output.write_text(json.dumps(data, separators=(',', ':'))+'\n', encoding='utf-8')
        if 'extension' in learning:
            from root_component_profile_row_extension import materialize_extension
            extended = materialize_extension(rows, labels, outside, selected, learning['extension'], positive)
            extended['scope'] = 'More completed rows; still no full graph.'
            atomic_json_write(args.output.with_suffix('.extended.json'), extended)

    learning = {'scope': 'Necessary row-quota clauses added to this one boundary profile SAT.',
                'rounds': [], 'clauses_added': 0}
    def solve_with_cuts(solver, allclauses, rows, domains, literals, labels, outside, pool, exactly, out):
        from root_component_profile_row_cuts import RowCutOracle
        from root_component_shared_k3_profile_sat import flush_native_proof, finished_proof
        oracle = RowCutOracle(rows, labels, outside, domains)
        initial = {'rows': rows, 'known_labels': labels, 'outside_labels': outside, 'domains': domains,
                   'profile_literals': literals, 'lab_source_sha256': hashlib.sha256(raw).hexdigest()}
        atomic_json_write(args.output.with_suffix('.row_cut_input.json'), initial)
        if args.extend_rows:
            from root_component_profile_row_extension import extend_rows, controls
            learning['extension_controls'] = controls()
            extra, extension = extend_rows(rows, labels, outside, domains, literals, args.extend_rows, pool, exactly)
            solver.append_formula(extra); allclauses.extend(extra)
            learning['extension'] = extension
            out['variables'] = pool.top; out['clauses'] = len(allclauses)
            out['additional_completed_rows'] = len(extension['hubs'])
        start = time.process_time()
        for ri in range(args.row_cut_rounds+1):
            solver.conf_budget(200000)
            answer = solver.solve_limited(); flush_native_proof()
            entry = {'round': ri, 'answer': answer, 'cpu_seconds': time.process_time()-start,
                     'solver_stats': solver.accum_stats()}
            learning['rounds'].append(entry)
            if answer is not True:
                learning['terminal_status'] = 'UNSAT_WITH_NECESSARY_ROW_CUTS' if answer is False else 'UNKNOWN'
                if answer is False:
                    proof = finished_proof(solver)
                    args.output.with_suffix('.row_cut_proof.rup.gz').write_bytes(
                        gzip.compress(('\n'.join(proof)+'\n').encode(), mtime=0))
                    args.output.with_suffix('.row_cut_cnf.json.gz').write_bytes(
                        gzip.compress(json.dumps(allclauses, separators=(',', ':')).encode(), mtime=0))
                atomic_json_write(args.output.with_suffix('.row_cut_learning.json'), learning)
                return answer
            positive = {v for v in solver.get_model() if v > 0}
            chosen = [[i for i, literal in enumerate(row) if literal in positive] for row in literals]
            assert all(len(ids) == 1 for ids in chosen)
            selected = [ids[0] for ids in chosen]
            cuts = oracle.separate(selected)
            entry['selected_indices'] = selected; entry['violated_cuts'] = cuts
            if not cuts or ri == args.row_cut_rounds or time.process_time()-start >= args.row_cut_cpu_seconds:
                learning['terminal_status'] = 'NO_VIOLATED_ROW_INCLUSION' if not cuts else 'BUDGET_WITH_SAT_SELECTION'
                atomic_json_write(args.output.with_suffix('.row_cut_learning.json'), learning)
                return True
            for cut in cuts:
                assert oracle.check_cut(cut)
                clause = [-literals[cut['outside_index']][cut['profile_index']]]
                clause += [literals[y][pi] for y, pi in cut['support_options']]
                assert not any(l in positive if l > 0 else -l not in positive for l in clause)
                solver.add_clause(clause); allclauses.append(clause); learning['clauses_added'] += 1
            atomic_json_write(args.output.with_suffix('.row_cut_learning.json'), learning)

    replacement = marker + '\n            export_selection_hook(rows, LABELS, OUTSIDE, doms, rows_v, s.get_model())'
    source = source.replace(marker, replacement)
    if args.row_cut_rounds or args.extend_rows:
        call = '        ans = s.solve_limited()'
        assert source.count(call) == 1
        source = source.replace(call, '        ans = profile_cut_solve_hook(s, allcl, rows, doms, rows_v, LABELS, OUTSIDE, pool, exactly, out)')
    previous = sys.argv[:]
    sys.argv = [str(args.lab_source), str(Path(__file__).resolve().parent), args.family,
                str(args.boundary), str(args.index), '1', '--sat', '--lean',
                '--out='+str(args.output.with_suffix('.lab_result.json.gz'))]
    try:
        exec(compile(source, str(args.lab_source), 'exec'),
             {'__name__': '__main__', '__file__': str(args.lab_source), 'export_selection_hook': save_selection,
              'profile_cut_solve_hook': solve_with_cuts})
    finally:
        sys.argv = previous
    print(json.dumps({'witness_exported': args.output.exists(), 'output': str(args.output)}))


if __name__ == '__main__':
    main()
