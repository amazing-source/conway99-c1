"""Exact Boolean adders for a weighted upper bound, without repeated literals."""
from collections import defaultdict
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))


def xor(enc, a, b):
    if type(a) is bool:
        return enc.neg(b) if a else b
    if type(b) is bool:
        return enc.neg(a) if b else a
    if a == b:
        return False
    if a == -b:
        return True
    q = enc.var()
    enc.clause(-a, -b, -q); enc.clause(a, b, -q)
    enc.clause(a, -b, q); enc.clause(-a, b, q)
    return q


def majority(enc, a, b, c):
    terms = [a, b, c]
    ones = sum(x is True for x in terms)
    variables = [x for x in terms if type(x) is not bool]
    if ones >= 2:
        return True
    if len(variables)+ones < 2:
        return False
    if len(variables) == 1:
        return variables[0]
    q = enc.var()
    if len(variables) == 2:
        a, b = variables
        if ones:
            enc.clause(enc.neg(a), q); enc.clause(enc.neg(b), q)
            enc.clause(-q, a, b)
        else:
            enc.clause(-q, a); enc.clause(-q, b)
            enc.clause(q, enc.neg(a), enc.neg(b))
    else:
        for x, y in ((a, b), (a, c), (b, c)):
            enc.clause(enc.neg(x), enc.neg(y), q)
            enc.clause(x, y, -q)
    return q


def weighted_atmost(enc, terms, bound):
    """Encode sum(weight*truth(literal)) <= bound; constants are permitted."""
    weights = defaultdict(int)
    for literal, weight in terms:
        assert isinstance(weight, int) and weight >= 0
        if literal is True:
            bound -= weight
        elif literal is not False:
            weights[literal] += weight
    # Cancel opposing literals before constructing any adder.
    for variable in {abs(x) for x in weights}:
        common = min(weights[variable], weights[-variable])
        weights[variable] -= common; weights[-variable] -= common; bound -= common
    weights = {literal: weight for literal, weight in weights.items() if weight}
    maximum = sum(weights.values())
    if bound < 0:
        enc.clause()
        return {'maximum_sum': maximum, 'bound_after_constants': bound, 'adder_bits': 0}
    if bound >= maximum:
        return {'maximum_sum': maximum, 'bound_after_constants': bound, 'adder_bits': 0}
    width = maximum.bit_length()
    accumulator = [False]*width
    for literal, weight in sorted(weights.items()):
        carry = False; result = []
        for i, a in enumerate(accumulator):
            b = literal if (weight >> i) & 1 else False
            result.append(xor(enc, xor(enc, a, b), carry))
            carry = majority(enc, a, b, carry)
        enc.clause(enc.neg(carry))
        accumulator = result
    for i in range(width):
        if not ((bound >> i) & 1):
            # Forbid a lexicographically larger bit with equal higher bits.
            enc.clause(enc.neg(accumulator[i]),
                       *(enc.neg(accumulator[j]) if (bound >> j) & 1 else accumulator[j]
                         for j in range(i+1, width)))
    return {'maximum_sum': maximum, 'bound_after_constants': bound,
            'adder_bits': width, 'weighted_literals_after_cancellation': len(weights)}


def check_small_truth_tables():
    from itertools import product
    from pysat.solvers import Solver
    from root_component_boundary_sat import Encoder
    terms = [(1, 9), (-2, 8), (3, 2), (3, 7), (-3, 3), (True, 3), (False, 50)]
    checks = 0
    for bound in range(-1, 40):
        enc = Encoder(3); weighted_atmost(enc, terms, bound)
        with Solver(name='glucose4', bootstrap_with=enc.clauses) as solver:
            for bits in product((0, 1), repeat=3):
                actual = sum(w*(int(lit) if type(lit) is bool else bits[abs(lit)-1]
                                if lit > 0 else 1-bits[abs(lit)-1]) for lit, w in terms)
                result = solver.solve(assumptions=[i+1 if b else -(i+1) for i, b in enumerate(bits)])
                assert result == (actual <= bound), (bound, bits, actual, result)
                checks += 1
    return {'truth_table_checks': checks, 'passed': True,
            'covers': ['signed literals', 'constants', 'duplicate/opposite literals',
                       'carry propagation', 'impossible/vacuous bounds', 'weights 8 and 9']}


if __name__ == '__main__':
    import argparse
    import json
    from pathlib import Path
    from root_component_resources import atomic_json_write, limit_research_process
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-output', type=Path, required=True)
    args = parser.parse_args(); limit_research_process(1)
    assert not args.check_output.exists()
    result = check_small_truth_tables()
    atomic_json_write(args.check_output, result)
    print(json.dumps(result))
