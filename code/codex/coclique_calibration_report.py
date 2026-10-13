"""Summarize matched experiments without inventing a progress percentage."""
from datetime import datetime, timezone
from pathlib import Path
import json
import re
import sys


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def domain_set(folder):
    return {(e['u'],e['v'],tuple(e['domain']))
            for e in read(folder/'edge_domain_diagnostics.json')['edges']}


def report(root):
    rows = []
    presolves = {}
    for folder in sorted(root.iterdir()):
        if not (folder/'result.json').exists():
            continue
        c = read(folder/'config.json')
        if c.get('presolve_only'):
            presolves[(c['model_sha256'],c['seed'])] = (folder.name,domain_set(folder))
    for folder in sorted(root.iterdir()):
        if not (folder/'diagnostics.json').exists():
            continue
        c, r, d = [read(folder/name) for name in ['config.json','result.json','diagnostics.json']]
        peak = d['peak_working_set']/(1024**3)
        domains = domain_set(folder)
        reference = presolves.get((c['model_sha256'],c['seed']))
        reference_name, presolve_domains = reference if reference else (None,None)
        added = domains-presolve_domains if presolve_domains is not None else None
        log = (folder/'search.log').read_text(encoding='utf-8')
        events = [dict(seconds=float(t),variables_left=int(v),variables_total=int(n),
                       constraints_left=int(k),constraints_total=int(total))
                  for t,v,n,k,total in re.findall(
                      r'#Model\s+([\d.]+)s var:(\d+)/(\d+) constraints:(\d+)/(\d+)',log)]
        trajectory = []
        for second in range(30,int(r['seconds'])+1,30):
            previous = [event for event in events if event['seconds']<=second]
            trajectory.append(dict(at_seconds=second,
                                   last_model_event=previous[-1] if previous else None))
        row = dict(name=folder.name, portfolio=c['portfolio'], seed=c['seed'],
                   model_sha256=c['model_sha256'], moments=c.get('moments',False),
                   mixed=c['mixed'], presolve_only=c.get('presolve_only',False),
                   status=r['status'], seconds=r['seconds'],
                   presolve_seconds=d['search_start_seconds'], peak_gib=round(peak,3),
                   conflicts=d['total_worker_conflicts'],
                   exported_clause_counts=sum(v['#Exported'] for v in d['clauses_shared'].values()),
                   reduced_edge_domains=len(domains),
                   domain_reference=reference_name,
                   additional_edge_domains_vs_presolve=len(added) if added is not None else None,
                   trajectory_30s=trajectory,
                   last_model_update=d['last_model_update'], actual_portfolio=d['actual_portfolio'])
        rows.append(row)
    result = dict(captured_utc=datetime.now(timezone.utc).isoformat(), runs=rows,
                  meaning='A bounded exploratory calibration; no optimality claim for the configuration',
                  warnings=['UNKNOWN provides no C1 exclusion',
                            'Conflict/export counts are activity, not unique excluded cases or time-to-proof',
                            'Tightened domains may depend on presolve representatives; do not transfer or combine',
                            'Same seed does not make an eight-worker run deterministic',
                            'Compare portfolios within the same model hash; model strengthening is a separate experiment'])
    (root/'report.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps([{k:r[k] for k in ('name','status','seconds','presolve_seconds','peak_gib',
                     'conflicts','reduced_edge_domains','additional_edge_domains_vs_presolve')} for r in rows]))


if __name__ == '__main__':
    report(Path(sys.argv[1]))
