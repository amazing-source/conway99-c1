"""Controlled, short CP-SAT runs. Counts are diagnostics, never exclusions.

Separate processes keep resource peaks comparable. Exported model fingerprints
and source snapshots distinguish a parameter experiment from a model change.
Tightened edge domains are diagnostic only: presolve may select representatives.
"""
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import os
import platform
import threading
import time

import ortools
from ortools.sat.python import cp_model
from coclique_column_coexistence import build, observe
from coclique_solver_diagnostics import diagnose


def save(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parameters(solver, portfolio, seconds, workers, seed):
    p = solver.parameters
    p.max_time_in_seconds = seconds
    p.num_workers = workers
    p.random_seed = seed
    p.log_search_progress = True
    p.log_subsolver_statistics = True
    p.log_to_stdout = False
    p.fill_tightened_domains_in_response = True
    if portfolio == 'legacy':
        p.ignore_subsolvers.extend(['max_lp', 'probing_max_lp'])
    elif portfolio == 'balanced':
        # Prevent the automatic substitution max_lp -> max_lp_sym.
        p.ignore_subsolvers.append('*max_lp*')
    elif portfolio == 'boolean':
        p.linearization_level = 0
        p.num_full_subsolvers = workers-2
        p.ignore_subsolvers.extend(['*max_lp*', 'feasibility_pump', 'rins/rens'])
        p.subsolvers.extend(['no_lp', 'quick_restart_no_lp', 'probing_no_lp',
                             'portfolio_no_lp', 'auto_no_lp', 'quick_alt_no_lp'])
        auto = type(p)()
        auto.name = 'auto_no_lp'
        auto.linearization_level = 0
        p.subsolver_params.append(auto)
        quick = type(p)()
        quick.name = 'quick_alt_no_lp'
        quick.linearization_level = 0
        quick.search_branching = cp_model.PORTFOLIO_WITH_QUICK_RESTART_SEARCH
        quick.search_random_variable_pool_size = 5
        p.subsolver_params.append(quick)
    else:
        raise ValueError(portfolio)


def run(folder, portfolio, seconds=180, workers=8, seed=1, mixed='coclique', moments=False,
        presolve_only=False):
    folder.mkdir(parents=True, exist_ok=False)
    scope = 'All (0,2); no fixed positive core, cycles, or required four-X center'
    source_names = ['coclique_calibration.py', 'coclique_column_coexistence.py',
                    'coclique_global_boundary.py', 'coclique_solver_diagnostics.py',
                    'coclique_residual_moments.py']
    sources = folder/'sources'
    sources.mkdir()
    for name in source_names:
        (sources/name).write_bytes(Path(__file__).with_name(name).read_bytes())
    config = dict(start_utc=datetime.now(timezone.utc).isoformat(), pid=os.getpid(),
                  seconds=seconds, workers=workers, seed=seed, portfolio=portfolio,
                  mixed=mixed, moments=moments, presolve_only=presolve_only,
                  scope=scope, ortools=ortools.__version__,
                  python=platform.python_version(), platform=platform.platform(),
                  source_hashes={p.name: digest(p) for p in sources.iterdir()},
                  reuse_learned_clauses=False, tightened_domains_reused=False)
    save(folder/'config.json', config)
    stop = threading.Event()
    monitor = threading.Thread(target=observe, args=(folder, stop), daemon=True)
    monitor.start()
    try:
        start = time.monotonic()
        model, B, M, edge, meta = build(mixed=mixed, saturated=True, triangles=True,
                                      rook_cut=True, center_kind='conditional')
        if moments:
            from coclique_residual_moments import add_moments
            # The five or four C-neighbours leave at most nine or ten in M.
            meta.update(add_moments(model, M, edge,
                        degree_upper={u: 9 if u in (37, 38) else 10 for u in M}))
        meta.update(build_seconds=time.monotonic()-start, model_stats=model.model_stats(),
                    border=B, missing=M)
        assert not model.validate(), model.validate()
        # Byte-identical exports check that only the engine settings changed.
        exported = folder/'model.pb'
        assert model.export_to_file(str(exported))
        model_hash = digest(exported)
        cache = folder.parent/'models'
        cache.mkdir(exist_ok=True)
        frozen = cache/(model_hash+'.pb')
        if frozen.exists():
            assert digest(frozen) == model_hash
            exported.unlink()
        else:
            exported.replace(frozen)
        meta.update(model_sha256=model_hash, model_file=str(frozen.resolve()),
                    model_bytes=frozen.stat().st_size)
        edge_map = []
        for u, v in combinations(range(99), 2):
            x = edge(u, v)
            edge_map.append(dict(u=u, v=v, fixed=x) if isinstance(x, int)
                            else dict(u=u, v=v, variable=x.index))
        save(folder/'edge_map.json', edge_map)
        save(folder/'model.json', meta)
        solver = cp_model.CpSolver()
        parameters(solver, portfolio, seconds, workers, seed)
        solver.parameters.stop_after_presolve = presolve_only
        config['ignored_subsolvers'] = list(solver.parameters.ignore_subsolvers)
        config['model_sha256'] = model_hash
        save(folder/'config.json', config)
        (folder/'parameters.textproto').write_text(str(solver.parameters), encoding='utf-8')
        print(json.dumps(dict(event='SOLVE_START', folder=str(folder), portfolio=portfolio,
                              seed=seed, mixed=mixed, model_sha256=model_hash,
                              build_seconds=meta['build_seconds'])), flush=True)
        with (folder/'search.log').open('w', encoding='utf-8') as log:
            solver.log_callback = lambda line: (log.write(line+'\n'), log.flush())
            status = solver.solve(model)
        result = dict(status=solver.status_name(status), seconds=solver.wall_time,
                      response_stats=solver.response_stats(), scope=scope,
                      necessary_model=True, full_srg=False)
        tightened = solver.response_proto.tightened_variables
        diagnostic_edges = []
        if tightened:
            assert len(tightened) == len(model.proto.variables)
            for item in edge_map:
                if 'variable' not in item:
                    continue
                idx = item['variable']
                domain = list(tightened[idx].domain)
                if domain != list(model.proto.variables[idx].domain):
                    diagnostic_edges.append(dict(**item, domain=domain))
        save(folder/'edge_domain_diagnostics.json', dict(
            warning='Presolve may remove feasible representatives. These are NOT universal graph lemmas; do not combine across runs.',
            edges=diagnostic_edges))
        result['diagnostic_reduced_edge_domains'] = len(diagnostic_edges)
        if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            import sympy as sp
            from coclique_global_completion import encode
            from coclique_affine_completion import binary_completions
            def value(u, v):
                x = edge(u, v)
                return x if isinstance(x, int) else solver.value(x)
            A = sp.Matrix(99, 99, value)
            BB, DD, EE = A[B, B], A[B, M], A[M, M]
            defect = A*A+A-12*sp.eye(99)-2*sp.ones(99)
            save(folder/'boundary_candidate.json', dict(B=encode(BB), D=encode(DD),
                  residual_degree_graph=encode(EE), polynomial_defect=encode(defect)))
            completion = binary_completions(BB, DD, seconds=60)
            save(folder/'completion.json', completion)
            result.update(full_srg=bool(completion['completions']),
                          completion_verdict=completion.get('verdict', completion['status']))
        save(folder/'result.json', result)
    finally:
        stop.set()
        monitor.join(timeout=3)
    diagnostics = diagnose(folder)
    save(folder/'diagnostics.json', diagnostics)
    print(json.dumps(dict(event='SOLVE_END', folder=str(folder),
                          status=result['status'], seconds=result['seconds'],
                          conflicts=diagnostics['total_worker_conflicts'],
                          edge_domains=len(diagnostic_edges),
                          peak_bytes=diagnostics['peak_working_set'])), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=Path)
    parser.add_argument('--portfolio', choices=('legacy', 'balanced', 'boolean'), required=True)
    parser.add_argument('--seconds', type=float, default=180)
    parser.add_argument('--workers', type=int, default=8)
    parser.add_argument('--seed', type=int, default=1)
    parser.add_argument('--mixed', choices=('coclique', 'all'), default='coclique')
    parser.add_argument('--moments', action='store_true')
    parser.add_argument('--presolve-only', action='store_true')
    args = parser.parse_args()
    run(args.folder, args.portfolio, args.seconds, args.workers, args.seed, args.mixed,
        args.moments, args.presolve_only)
