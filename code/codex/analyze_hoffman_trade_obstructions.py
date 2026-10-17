"""Compress new global exclusions and give an intrinsic asymmetry witness."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'data/codex_hoffman_trades'


def bits(mask):
    return [i for i in range(77) if mask >> i & 1]


def canon_colors(signatures):
    distinct = {value: i for i, value in enumerate(sorted(set(signatures)))}
    return [distinct[v] for v in signatures]


def cover_with_four(kill_masks, full):
    choices = [(j,m) for j,m in enumerate(kill_masks) if m]
    choices = [(j,m) for j,m in choices if not any((m | n) == n and (m != n or k < j) for k,n in choices)]
    union = 0
    for j,m in choices:
        union |= m
    if union != full:
        return None
    failed = set()
    def search(remaining, budget):
        if not remaining:
            return []
        if budget == 0 or (remaining,budget) in failed:
            return None
        useful = [(j,m&remaining) for j,m in choices if m&remaining]
        if remaining.bit_count() > budget*max(m.bit_count() for j,m in useful):
            return None
        points = [bit for bit in range(full.bit_length()) if remaining >> bit & 1]
        point = min(points,key=lambda bit:sum(m >> bit & 1 for j,m in useful))
        for j,m in sorted(useful,key=lambda jm:-jm[1].bit_count()):
            if not (m >> point & 1):
                continue
            rest = search(remaining & ~m,budget-1)
            if rest is not None:
                return [j]+rest
        failed.add((remaining,budget))
        return None
    return search(full,4)


def color_certificate(blocks):
    nb = [set() for _ in range(99)]
    for i, b in enumerate(blocks):
        for x in b:
            nb[x].add(22+i)
            nb[22+i].add(x)
    two = [set(j for j,c in enumerate(blocks) if i != j and len(set(b)&set(c)) == 2)
           for i,b in enumerate(blocks)]
    triangle_counts = [sum(v in two[u] for u,v in combinations(ns,2)) for ns in two]
    four_counts = [sum(len(two[u]&two[v])-1 for u,v in combinations(ns,2)) for ns in two]
    colors = canon_colors([(0,0,0)]*22 + [(1,t,q) for t,q in zip(triangle_counts,four_counts)])
    history = [dict(all=len(set(colors)), points=len(set(colors[:22])), blocks=len(set(colors[22:])))]
    rounds = [colors]
    while True:
        new = canon_colors([(colors[x], tuple(sorted(colors[y] for y in nb[x]))) for x in range(99)])
        if len(set(new)) == len(set(colors)):
            break
        colors = new
        rounds.append(colors)
        history.append(dict(all=len(set(colors)), points=len(set(colors[:22])), blocks=len(set(colors[22:]))))
    return dict(triangles_in_intersection_two_graph=triangle_counts,
                quadrangles_in_intersection_two_graph=four_counts,
                color_history=history, color_rounds=rounds,
                proves_trivial_design_automorphism_group=len(set(colors[:22])) == 22)


def main():
    designs = json.loads((OUT/'two_point_trades.json').read_text())['new_designs']
    summaries = []
    proof_bundle = []
    for d in designs:
        folder = OUT/('design_'+d['key'][:12])
        result = json.loads((folder/'result.json').read_text())
        assert result['status'] == 'UNSAT_FIXED_DESIGN'
        blocks = d['blocks']
        dom = [[sum(1 << int(j) for j in line.split())
                for line in (folder/f'row_{i}.rows').read_text().splitlines()] for i in range(77)]
        assert all(s[3] == 'EXHAUSTED' for s in result['row_statistics'])
        # Validate the actual rows used in every new certificate; do not repeat domain enumeration.
        for i, rows in enumerate(dom):
            for mask in rows:
                neighbours = bits(mask)
                assert len(neighbours) == 10 and i not in neighbours
                assert all(sum(x in blocks[j] for j in neighbours) == 2-int(x in blocks[i]) for x in range(22))
                assert all(len(set(blocks[i])&set(blocks[j])) <= 1 for j in neighbours)
                assert all(len(set(blocks[j])&set(blocks[k])) <= 1 for j,k in combinations(neighbours,2))
        # Replay the new contradiction sequence directly, without the searcher's support tables.
        alive = [set(range(len(row))) for row in dom]
        for i, ix, j in result['deletions']:
            assert ix in alive[i]
            x = dom[i][ix]
            z = len(set(blocks[i])&set(blocks[j]))
            edge = (x >> j)&1
            assert all(edge != ((dom[j][iy] >> i)&1) or
                       (x&dom[j][iy]).bit_count()+z != 2-edge for iy in alive[j])
            alive[i].remove(ix)
        assert not alive[result['empty_row']]
        best = None
        forced = [(1 << 77)-1 for _ in range(77)]
        for i in range(77):
            for mask in dom[i]:
                forced[i] &= mask
        contradictions = []
        no_support = [[0]*77 for _ in range(77)]
        for i,j in combinations(range(77),2):
            z = len(set(blocks[i])&set(blocks[j]))
            overlap_lower = (forced[i]&forced[j]).bit_count()
            edge_lower = int(bool(forced[i] >> j & 1 or forced[j] >> i & 1))
            if overlap_lower + z > 2-edge_lower:
                contradictions.append(dict(rows=[i,j], common_core_points=sorted(set(blocks[i])&set(blocks[j])),
                                           forced_common_neighbours=bits(forced[i]&forced[j]), forced_edge=edge_lower))
            supported_i = supported_j = 0
            for ix,x in enumerate(dom[i]):
                for iy,y in enumerate(dom[j]):
                    if ((x >> j)&1) == ((y >> i)&1) and (x&y).bit_count()+z == 2-((x >> j)&1):
                        supported_i |= 1 << ix
                        supported_j |= 1 << iy
            no_support[i][j] = ((1 << len(dom[i]))-1) ^ supported_i
            no_support[j][i] = ((1 << len(dom[j]))-1) ^ supported_j
            compatible = bool(supported_i)
            if not compatible:
                score = len(dom[i])+len(dom[j])
                if best is None or score < best['total_candidates']:
                    best = dict(rows=[i,j], blocks=[blocks[i],blocks[j]], core_overlap=z,
                                total_candidates=score,
                                domains=[[bits(x) for x in dom[i]], [bits(y) for y in dom[j]]])
        star = None
        for i in range(77):
            full = (1 << len(dom[i]))-1
            killers = [j for j in range(77) if no_support[i][j]]
            for count in (1,2,3):
                if star and count >= len(star['other_rows']):
                    break
                for js in combinations(killers,count):
                    covered = 0
                    for j in js:
                        covered |= no_support[i][j]
                    if covered == full:
                        star = dict(root_row=i, other_rows=list(js), root_candidates=len(dom[i]),
                                    unsupported_candidates={j: [x for x in range(len(dom[i])) if no_support[i][j] >> x & 1] for j in js})
                        break
                if star and len(star['other_rows']) == count:
                    break
        if star is None:
            for i in sorted(range(77),key=lambda i:len(dom[i])):
                js = cover_with_four(no_support[i],(1 << len(dom[i]))-1)
                if js is not None:
                    star = dict(root_row=i,other_rows=js,root_candidates=len(dom[i]),
                                unsupported_candidates={j:[x for x in range(len(dom[i])) if no_support[i][j] >> x & 1] for j in js})
                    break
        cert = dict(design_key=d['key'], automorphism_order=d['aut'],
                    direct_forced_common_neighbour_obstructions=contradictions,
                    smallest_incompatible_pair=best,
                    small_star_obstruction=star,
                    intrinsic_asymmetry=color_certificate(blocks))
        (folder/'compact_certificate.json').write_text(json.dumps(cert,indent=2))
        summaries.append(dict(design_key=d['key'],aut=d['aut'], direct_obstructions=len(contradictions),
                              pair=best['rows'] if best else None,
                              pair_candidates=best['total_candidates'] if best else None,
                              star_rows=1+len(star['other_rows']) if star else None,
                              asymmetry_colors=cert['intrinsic_asymmetry']['color_history']))
        proof_bundle.append(dict(design=d, domains=[[str(x) for x in row] for row in dom],
                                 row_statistics=result['row_statistics'], deletions=result['deletions'],
                                 empty_row=result['empty_row'], compact_certificate=cert))
    (OUT/'compact_obstructions.json').write_text(json.dumps(summaries,indent=2))
    (OUT/'proof_bundle.json').write_text(json.dumps(dict(scope='36 fixed designs only; every row enumeration exhausted; direct replay passed',
                                                       items=proof_bundle),separators=(',',':')))
    print('Designs',len(summaries),'direct forced-neighbour obstruction',sum(x['direct_obstructions'] > 0 for x in summaries),
          'incompatible pair',sum(x['pair'] is not None for x in summaries))
    print('First design:',json.dumps(summaries[0]))
    print('Pair candidate histogram:',dict(Counter(x['pair_candidates'] for x in summaries)))
    print('Star row histogram:',dict(Counter(x['star_rows'] for x in summaries)))
    print('Asymmetric designs with intrinsic certificate:',sum(x['aut']==1 and x['asymmetry_colors'][-1]['points']==22 for x in summaries))


if __name__ == '__main__':
    main()
