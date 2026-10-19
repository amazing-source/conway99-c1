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
import threading

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
    p.add_argument('--continuation-cuts', action='store_true')
    p.add_argument('--attachment', type=int, nargs=4, action='append',
                   help='Target one specified grid attachment, avoiding an already covered boundary scan.')
    p.add_argument('--sigma', type=int, nargs=4)
    p.add_argument('--proof-checker', choices=('auto','python','native'),default='auto')
    args = p.parse_args()
    assert not args.output.exists(), 'Use a new output name.'
    resources = limit_research_process(1)
    helper_hashes = {name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in
                     ('root_component_lab_profile_export.py','root_component_profile_row_cuts.py',
                      'root_component_profile_guard_cut.py','root_component_profile_row_extension.py',
                      'root_component_p3_neighbor_support.py','root_component_native_rup.py')}
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
                'resources': resources, 'helper_sha256': helper_hashes,
                'rows': rows, 'known_labels': labels, 'outside_labels': outside,
                'domains': domains, 'selected_indices': [ids[0] for ids in indices], 'profiles': selected}
        args.output.write_text(json.dumps(data, separators=(',', ':'))+'\n', encoding='utf-8')
        if 'extension' in learning:
            from root_component_profile_row_extension import materialize_extension
            extended = materialize_extension(rows, labels, outside, selected, learning['extension'], positive)
            extended['scope'] = 'More completed rows; still no full graph.'
            atomic_json_write(args.output.with_suffix('.extended.json'), extended)

    learning = {'scope': 'Necessary row-quota clauses added to this one boundary profile SAT.',
                'rounds': [], 'clauses_added': 0, 'helper_sha256': helper_hashes}
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
            done = threading.Event()
            def interrupt_on_budget():
                while not done.wait(.05):
                    if time.process_time()-start >= args.row_cut_cpu_seconds:
                        solver.interrupt(); return
            timer = threading.Thread(target=interrupt_on_budget, daemon=True); timer.start()
            try:
                answer = solver.solve_limited(expect_interrupt=True)
            finally:
                done.set(); timer.join(); solver.clear_interrupt()
            flush_native_proof()
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
            if not cuts and args.continuation_cuts:
                from root_component_profile_guard_cut import GuardOracle
                guard = GuardOracle(rows,labels,outside,domains,selected).minimize()
                if guard is not None:
                    assert oracle.check_cut(guard)
                    cuts = [guard]
            entry['selected_indices'] = selected; entry['violated_cuts'] = cuts
            if not cuts or ri == args.row_cut_rounds or time.process_time()-start >= args.row_cut_cpu_seconds:
                learning['terminal_status'] = 'NO_VIOLATED_ROW_INCLUSION' if not cuts else 'BUDGET_WITH_SAT_SELECTION'
                atomic_json_write(args.output.with_suffix('.row_cut_learning.json'), learning)
                return True
            for cut in cuts:
                assert oracle.check_cut(cut)
                guards = cut['guards'] if 'guards' in cut else [(cut['outside_index'], cut['profile_index'])]
                clause = [-literals[y][pi] for y, pi in guards]
                clause += [literals[y][pi] for y, pi in cut['support_options']]
                assert not any(l in positive if l > 0 else -l not in positive for l in clause)
                solver.add_clause(clause); allclauses.append(clause); learning['clauses_added'] += 1
            out['clauses'] = len(allclauses)
            atomic_json_write(args.output.with_suffix('.row_cut_learning.json'), learning)

    replacement = marker + '\n            export_selection_hook(rows, LABELS, OUTSIDE, doms, rows_v, s.get_model())'
    source = source.replace(marker, replacement)
    from root_component_native_rup import CHECKER, check_native_rup
    use_native = args.proof_checker=='native' or (args.proof_checker=='auto' and sys.platform=='win32' and CHECKER.exists())
    if use_native:
        check_call = "            out['proof_check'] = check_rup(_L, proof)"
        assert source.count(check_call)==1
        source=source.replace(check_call,"            out['proof_check'] = export_proof_check_hook(_L.clauses, proof)")
        proof_call = "            proof = [ln for ln in finished_proof(s) if not ln.startswith('d ')]"
        assert source.count(proof_call)==1
        source=source.replace(proof_call,"            proof = finished_proof(s)")
    if args.row_cut_rounds or args.extend_rows:
        call = '        ans = s.solve_limited()'
        assert source.count(call) == 1
        source = source.replace(call, '        ans = profile_cut_solve_hook(s, allcl, rows, doms, rows_v, LABELS, OUTSIDE, pool, exactly, out)')
    previous = sys.argv[:]
    sys.argv = [str(args.lab_source), str(Path(__file__).resolve().parent), args.family,
                str(args.boundary), str(args.index), '1', '--sat', '--lean',
                '--out='+str(args.output.with_suffix('.lab_result.json.gz'))]
    try:
        ns = {'__name__': '__main__', '__file__': str(args.lab_source), 'export_selection_hook': save_selection,
              'profile_cut_solve_hook': solve_with_cuts,
              'export_proof_check_hook':lambda clauses,proof:check_native_rup(clauses,proof,args.output)}
        if args.attachment:
            marker = '\nOUT = next('
            assert source.count(marker)==1, 'Inspect the changed LAB driver.'
            exec(compile(source.split(marker)[0],str(args.lab_source),'exec'),ns)
            assert len(args.attachment)==ns['NG'] and ns['Q12K']
            assert all(sorted(a)==list(range(4)) for a in args.attachment)
            assert (args.sigma is not None)==ns['YY']
            if args.sigma is not None:
                assert sorted(args.sigma)==list(range(4))
            boundary_raw=args.boundary.read_bytes(); boundary_data=json.loads(gzip.decompress(boundary_raw))
            assert boundary_data['status']=='COMPLETE_BOUNDARY_COVER'
            boundary=tuple(bytes.fromhex(boundary_data['boundaries_hex'][args.index]))
            rows=ns['materialize'](boundary_data['core'],boundary,args.attachment,args.sigma)
            result=ns['frontier'](rows,True)
            record={'scope':'One specified attachment only; not a boundary or family verdict.',
                    'boundary_index':args.index,'boundary_hex':boundary_data['boundaries_hex'][args.index],
                    'boundary_source_sha256':hashlib.sha256(boundary_raw).hexdigest(),
                    'attachments':args.attachment,'sigma':args.sigma,'frontier':result}
            args.output.with_suffix('.lab_result.json.gz').write_bytes(
                gzip.compress(json.dumps(record,separators=(',',':')).encode(),mtime=0))
            print(json.dumps({'target_attachment_status':result['status']}))
        else:
            exec(compile(source, str(args.lab_source), 'exec'), ns)
    finally:
        sys.argv = previous
    print(json.dumps({'witness_exported': args.output.exists(), 'output': str(args.output)}))


if __name__ == '__main__':
    main()
