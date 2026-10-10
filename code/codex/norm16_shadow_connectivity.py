"""Apply the union bound of note257 to all norm16 core attachments.

Only the archived shadows are read. No SRG search or floating point is used.
The certificates are subsets U of D with a lower bound >11 for |N_Z(U)|.
Equality subsets also forbid D edges meeting U and multiple B incidences in U.
"""
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def components(c):
    remaining = set(range(len(c)))
    answer = []
    while remaining:
        comp, queue = set(), [min(remaining)]
        while queue:
            i = queue.pop()
            if i in comp:
                continue
            comp.add(i)
            queue.extend(j for j in remaining if c[i][j] and j not in comp)
        remaining -= comp
        answer.append(sorted(comp))
    return answer


def catalogue():
    source = json.loads((ROOT/'data/codex_norm16_attachments_rank.json').read_text())
    # The source is a list of the five nonempty core cases.
    cases = source['cases'] if isinstance(source, dict) else source
    old_edges = json.loads((ROOT/'data/codex_norm16_edge_omitted_pair.json').read_text())
    edges = {(c['case'], o['orbit']): o['eligible_edges']
             for c in old_edges['cases'] for o in c['orbits']}
    old_closed = {(2, i) for i in (44, 46, 81, 82, 84, 85)} | {(3, 26), (4, 0), (4, 3), (0, 52)}
    records, removed_edges = [], []
    for ci, case in enumerate(cases):
        for oi, orbit in enumerate(case['orbits']):
            shadows = [set(r[:2]) | {8+q for q in r[2:]} for r in orbit['representative']]
            c = [[len(s & t) if i != j else 0 for j,t in enumerate(shadows)] for i,s in enumerate(shadows)]
            assert all(sum(row) == 4 for row in c)
            assert all(0 <= v <= 2 for row in c for v in row)
            excluded, tight = [], []
            for k in range(2, 9):
                for u in combinations(range(8), k):
                    lower = 4*k-sum(2-c[d][e] for d,e in combinations(u,2))
                    if lower > 11:
                        excluded.append({'U': list(u), 'union_lower_bound': lower})
                    elif lower == 11:
                        tight.append(list(u))
            comp = components(c)
            assert bool(excluded) == (len(comp) > 1)
            forbidden = set(range(8)) if excluded else set().union(*map(set, tight)) if tight else set()
            removed = [edge for edge in edges[ci, oi] if set(edge) & forbidden]
            if removed:
                removed_edges.append({'case': ci, 'orbit': oi, 'edges': removed})
            if excluded or tight:
                records.append({'case': ci, 'orbit': oi, 'C': c, 'components': comp,
                                'exclusion_certificates': excluded, 'tight_subsets': tight,
                                'already_closed_in_note256': (ci,oi) in old_closed,
                                'D_vertices_forbidden_in_D_edges': sorted(forbidden),
                                'remaining_D_edge_positions': [edge for edge in edges[ci,oi] if edge not in removed]})
    newly_closed = [[r['case'],r['orbit']] for r in records if r['exclusion_certificates'] and not r['already_closed_in_note256']]
    all_closed = old_closed | {(r['case'],r['orbit']) for r in records if r['exclusion_certificates']}
    total = sum(len(c['orbits']) for c in cases)
    return {'scope': __doc__, 'summary': {'attachments': total,
            'disconnected_attachments': sum(bool(r['exclusion_certificates']) for r in records),
            'newly_closed_after_note256': newly_closed,
            'closed_by_notes256_257': len(all_closed), 'not_closed_by_notes256_257': total-len(all_closed),
            'connected_attachments_with_tight_subsets': sum(not r['exclusion_certificates'] for r in records),
            'D_edge_positions_before': sum(map(len, edges.values())),
            'D_edge_positions_removed': sum(len(r['edges']) for r in removed_edges)},
            'records': records, 'removed_D_edge_positions': removed_edges}


if __name__ == '__main__':
    result = catalogue()
    (ROOT/'data/codex_norm16_shadow_connectivity.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result['summary']))
