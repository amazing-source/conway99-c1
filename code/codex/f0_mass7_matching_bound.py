"""Exact integer mass-seven losses, over every matching of the seven apices.

No numerical optimisation: for each matching and each possible apex edge
count, allocate edges to the largest collision increments in each degree class.
"""
from collections import Counter, defaultdict
from itertools import combinations_with_replacement, permutations
import gzip
import json
import time
import sys

from higher_census_minima import ROOT


def run():
    suffix = "_tf" if "--triangle-free" in sys.argv else ""
    if "--positive-type" in sys.argv:
        assert suffix
        suffix += "_"+sys.argv[sys.argv.index("--positive-type")+1]
    start = time.monotonic()
    with gzip.open(ROOT/f'data/codex_f0_mass7_p6{suffix}_patterns.json.gz', 'rt', encoding='utf-8') as stream:
        data = json.load(stream)
    profiles = data['profiles']; core = data['core_adjacency']
    masks = [mask for mask, _ in profiles]; index = {mask: i for i, mask in enumerate(masks)}
    doubles = sorted({mask & 127 for mask in masks if (mask & 127).bit_count() == 2})
    assert len(doubles) == 7
    pattern = {(tuple(row['profiles']), row['edges']): row['counts'] for row in data['patterns']}
    names = ['F0']
    with gzip.open(ROOT/f'data/codex_f0_mass7_p5{suffix}_patterns.json.gz', 'rt') as stream:
        cross_data = json.load(stream)
    cross_counts = {row['profiles'][0]: row['counts']['F0'] for row in cross_data['patterns']}
    with gzip.open(ROOT/f'data/codex_f0_mass7_p4{suffix}_patterns.json.gz','rt') as stream:
        small_data = json.load(stream)
    assert len(small_data['patterns']) == 1 and small_data['patterns'][0]['profiles'] == []
    cross_four = small_data['patterns'][0]['counts']['F0']
    cross_max = 0
    edge_counts = {(0, 0): (14, 1), (0, 1): (182, -4), (0, 2): (28, 2),
                   (1, 1): (254, 4), (1, 2): (42, -4), (2, 2): (0, 1)}
    records = []; maxima = Counter(); rejected = Counter()
    for sigma in permutations(range(7)):
        apex_masks = [a | (doubles[sigma[i]] << 7) for i, a in enumerate(doubles)]
        if any(mask not in index for mask in apex_masks):
            rejected['impossible_apex_profile'] += 1; continue
        volumes = {index[0]: 17}
        volumes.update({index[mask]: 1 for mask in apex_masks})
        feasible = True
        for u in range(7):
            for v in range(7, 14):
                count = (1 if core[u] >> v & 1 else 2)-(core[u] & core[v]).bit_count()
                count -= sum(bool(mask >> u & 1) and bool(mask >> v & 1) for mask in apex_masks)
                mask = (1 << u) | (1 << v)
                if count < 0 or (count and mask not in index):
                    feasible = False; break
                if count:
                    volumes[index[mask]] = count
            if not feasible: break
        if not feasible:
            rejected['negative_single_profile'] += 1; continue
        assert sum(volumes.values()) == 85
        assert sum(n for i, n in volumes.items() if (masks[i] & 127).bit_count() == 1) == 61
        base = Counter(); forced = Counter(); histograms = {name: defaultdict(Counter) for name in names}
        for i, j in combinations_with_replacement(sorted(volumes), 2):
            total = volumes[i]*volumes[j] if i != j else volumes[i]*(volumes[i]-1)//2
            if not total: continue
            group = tuple(sorted(((masks[i] & 127).bit_count(), (masks[j] & 127).bit_count())))
            zero, one = pattern.get(((i, j), 0)), pattern.get(((i, j), 1))
            if zero is None and one is None:
                feasible = False; break
            if zero is None:
                forced[group] += total
                for name in names: base[name] += total*one[name]
            else:
                for name in names:
                    base[name] += total*zero[name]
                    if one is not None:
                        histograms[name][group][one[name]-zero[name]] += total
        if not feasible:
            rejected['impossible_pair_profile'] += 1; continue
        best = {name: -1 for name in names}; best_t = {}
        for t in range(11):
            targets = {g: c+a*t-forced[g] for g, (c, a) in edge_counts.items()}
            if any(number < 0 or number > sum(histograms[names[0]][g].values()) for g, number in targets.items()):
                continue
            for name in names:
                value = base[name]
                for group, number in targets.items():
                    remaining = number
                    for increment, capacity in sorted(histograms[name][group].items(), reverse=True):
                        used = min(remaining, capacity)
                        value += used*increment; remaining -= used
                    assert not remaining
                if value > best[name]:
                    best[name] = value; best_t[name] = t
        if best[names[0]] < 0:
            rejected['group_edge_counts_impossible'] += 1; continue
        for name in names: maxima[name] = max(maxima[name], best[name])
        cross_value = sum(n*cross_counts[i] for i,n in volumes.items())
        cross_max = max(cross_max,cross_value)
        records.append({'matching': sigma, 'upper_bounds': best, 'maximising_t': best_t, 'F0_vs_5_2': cross_value})
    report = {'matchings_examined': 5040, 'matchings_retained': len(records), 'exact_rejection_counts': dict(rejected),
              'uniform_collision_pair_bounds': dict(maxima), 'matching_records': records,
              'F0_vs_5_2_bound':cross_max,'F0_vs_4_1_exact':cross_four,
              'joint_bound':max(r['upper_bounds']['F0']+r['F0_vs_5_2']+cross_four for r in records),
              'scope': 'Both signs; mass-seven collisions. Integer finite maxima, no claim of attainable ambient graph.'}
    path = ROOT/f'data/codex_f0_mass7{suffix}_matching_bound.json.gz'
    if '--verify-only' in sys.argv:
        with gzip.open(path,'rt') as stream:
            assert json.load(stream) == json.loads(json.dumps(report))
    else:
        with gzip.GzipFile(filename=path,mode='wb',mtime=0) as stream:
            stream.write(json.dumps(report).encode())
    print('Retained matchings:', len(records), 'of 5040; internal F0 bounds:', dict(maxima), 'F0_vs_5_2:',cross_max,
          '; seconds:', round(time.monotonic()-start, 1), flush=True)


if __name__ == '__main__':
    run()
