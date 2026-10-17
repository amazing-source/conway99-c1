"""Apply the omitted-pair lemma of note255 to the old eligible D edges.

These counts are labelled necessary edge positions, not SRG counts.
"""
from collections import Counter
import json
from norm16_schur_data import ROOT, source_data


def refined_sources():
    sources = json.loads((ROOT/'data/codex_norm16_D_edge_reduction.json').read_text())
    attachments = source_data()[1]
    counts = Counter()
    cases = []
    for case in sources['cases']:
        ci = case['case']
        orbits = []
        for orbit in case['orbits']:
            oi = orbit['orbit']
            shadows = [set(r[:2]) | {8+q for q in r[2:]} for r in attachments[ci]['orbits'][oi]['representative']]
            c = [[len(s & t) for t in shadows] for s in shadows]
            keep = []
            for d, e in orbit['eligible_edges']:
                profile = sorted(c[d][j]+c[e][j] for j in range(8) if j not in (d, e))
                if profile != [1, 1, 1, 1, 2, 2]:
                    counts['wrong_intersection_profile'] += 1
                    continue
                pair = [j for j in range(8) if j not in (d, e) and c[d][j]+c[e][j] == 2]
                if c[pair[0]][pair[1]]:
                    counts['opposite_pair_has_core_common_neighbour'] += 1
                    continue
                rest = [j for j in range(8) if j not in [d, e]+pair]
                if any(c[j][k] > 1 for j in pair for k in rest):
                    counts['opposite_pair_meets_a_core_shadow_twice'] += 1
                    continue
                keep.append([d, e])
            orbits.append({'orbit': oi, 'eligible_edges': keep})
        cases.append({'case': ci, 'before': case['after_note253'], 'after': sum(len(o['eligible_edges']) for o in orbits), 'orbits': orbits})
    return {'scope': __doc__, 'counts_removed': dict(counts), 'cases': cases}


if __name__ == '__main__':
    data = refined_sources()
    (ROOT/'data/codex_norm16_edge_omitted_pair.json').write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps({'before': sum(c['before'] for c in data['cases']), 'after': sum(c['after'] for c in data['cases']), 'by_case': [c['after'] for c in data['cases']], 'removed': data['counts_removed']}))
