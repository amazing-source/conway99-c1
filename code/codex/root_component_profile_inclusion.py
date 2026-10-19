"""Exact propagation of inclusions between equal-sum profile features.

For every variable choose one of its bit-set options. Feature e has
prescribed total t_e. If every option containing e also contains f,
then t_e <= t_f. Equality forces every chosen f-option to contain e.
This is a necessary counting identity, independent of SRG parameters.
"""


def inclusion_filter(options, targets):
    offsets = []; flat = []; occurrences = {}
    target_mask = sum(1 << k for k in targets)
    for row in options:
        offsets.append(len(flat))
        for feature_set in row:
            index = len(flat); flat.append(feature_set & target_mask)
            mask = flat[-1]
            while mask:
                bit = mask & -mask; mask ^= bit; key = bit.bit_length() - 1
                occurrences[key] = occurrences.get(key, 0) | (1 << index)
    forbidden = 0; implications = []
    for e, support in occurrences.items():
        first = support & -support
        implied = flat[first.bit_length() - 1]
        rest = support ^ first
        while rest and implied != (1 << e):
            bit = rest & -rest; rest ^= bit
            implied &= flat[bit.bit_length() - 1]
        implied &= ~(1 << e)
        while implied:
            bit = implied & -implied; implied ^= bit; f = bit.bit_length() - 1
            if targets[e] > targets[f]:
                return {'status': 'EXCLUDED_PROFILE_INCLUSION', 'implies': [e, f],
                        'demands': [targets[e], targets[f]],
                        'reason': 'Contained feature has larger prescribed total'}, None
            if targets[e] != targets[f]:
                continue
            extra = occurrences[f] & ~support
            if extra:
                forbidden |= extra
                implications.append({'implies': [e, f], 'equal_demand': targets[e],
                                     'forbidden_options': extra.bit_count()})
    kept = [[j for j in range(len(row)) if not (forbidden & (1 << (offset + j)))]
            for offset, row in zip(offsets, options)]
    if any(not row for row in kept):
        return {'status': 'EXCLUDED_PROFILE_INCLUSION',
                'empty_variable': next(i for i, row in enumerate(kept) if not row),
                'inclusions': implications}, None
    return {'status': 'PROPAGATED_PROFILE_INCLUSIONS', 'inclusions': implications,
            'removed_options': forbidden.bit_count()}, kept
