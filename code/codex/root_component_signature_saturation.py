"""Exact domain propagation for four signatures with a prescribed sum.

If each entry of coordinate j lies in [l,u], the sum lies in [4l,4u].
Equality at an endpoint forces every one of the four entries to that
endpoint. Iterating this implication cannot remove a feasible quadruple.
The trace consists entirely of integer bounds and forced equalities.
"""


def saturate(signatures, target):
    signatures = [tuple(h) for h in signatures]
    assert all(len(h) == len(target) for h in signatures)
    active = list(range(len(signatures)))
    steps = []
    while active:
        changed = False
        for j, required in enumerate(target):
            lo = min(signatures[i][j] for i in active)
            hi = max(signatures[i][j] for i in active)
            if not 4 * lo <= required <= 4 * hi:
                return {'signatures': [], 'retained_indices': [], 'steps': steps,
                        'contradiction': {'coordinate': j, 'required_sum': required,
                                          'lower_sum': 4 * lo, 'upper_sum': 4 * hi,
                                          'remaining_indices': active}}
            if lo == hi:
                continue
            value = lo if required == 4 * lo else hi if required == 4 * hi else None
            if value is None:
                continue
            after = [i for i in active if signatures[i][j] == value]
            steps.append({'coordinate': j, 'required_sum': required,
                          'minimum': lo, 'maximum': hi, 'forced_value': value,
                          'before': len(active), 'after': len(after)})
            assert after and len(after) < len(active)
            active = after
            changed = True
        if not changed:
            break
    return {'signatures': [signatures[i] for i in active], 'retained_indices': active,
            'steps': steps, 'contradiction': None}
