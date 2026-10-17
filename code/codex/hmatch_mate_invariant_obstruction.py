"""Extract an upper-Gram obstruction unchanged by every outer rematching.

This diagnoses a new obstruction for a supplied failed block; it does not
re-audit its T positivity, rank, automorphisms, or producer SAT search.
"""
import argparse
from functools import reduce
from math import gcd, lcm
import json
from pathlib import Path
import sys
import time

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hmatch_cycle_reflections import B, H, LABELS, ROOT_INTERSECTION, load_graph


def primitive(vector):
    scale = lcm(*(int(x.q) for x in vector))
    values = [int(x*scale) for x in vector]
    divisor = reduce(gcd, values)
    return sp.Matrix([x//abs(divisor) for x in values]) if divisor else sp.zeros(44, 1)


def run(source, output):
    start = time.monotonic()
    record = json.loads(Path(source).read_text(encoding='utf-8'))
    G = sp.Matrix(load_graph(record))
    incidence = sp.Matrix(B)
    mate = [r ^ 1 for r in range(14)]
    L15 = 4*incidence.T*incidence-incidence.T*incidence[mate, :]+2*sp.ones(44)
    U15 = 60*sp.eye(44)+15*G-L15
    representatives = [i for i in range(44) if i < H[i]]
    odd = sp.zeros(44, 22)
    for j, i in enumerate(representatives):
        odd[i, j], odd[H[i], j] = 1, -1
    # Use the compressed kernel to FIND a leakage relation, not to certify PSD.
    compressed = odd.T*U15*odd
    columns = compressed.nullspace()
    stars = [incidence[0, :].T-incidence[1, :].T,
             incidence[2, :].T-incidence[3, :].T]
    relations = []
    for column in columns:
        q = odd*column
        letters = incidence*q
        q -= stars[0]*letters[0]/12+stars[1]*letters[2]/12
        q = primitive(q)
        if not any(q):
            continue
        assert incidence*q == sp.zeros(14, 1)
        z = 4*q+G*q
        assert U15*q == 15*z
        assert (q.T*z)[0] == 0
        if not any(z):
            continue
        degree_bound = max(sum(G.row(i)) for i in range(44))
        upper = int(4+degree_bound)
        witness = upper*q-z
        norm_z = int(z.dot(z))
        source_energy15 = int((witness.T*U15*witness)[0])
        bound = -upper*norm_z
        assert source_energy15 <= 15*bound < 0
        relation = dict(kind='ZERO_ENERGY_LEAKAGE', q=list(map(int, q)), z=list(map(int, z)),
            negative_witness=list(map(int, witness)), q_support=sum(int(x != 0) for x in q),
            maximum_Gamma_degree=int(degree_bound), uniform_upper_for_U=upper,
            squared_norm_z=norm_z, uniform_witness_energy_upper=bound,
            source_witness_energy_times15=source_energy15)
        if incidence*z == sp.zeros(14, 1):
            z_energy = int((z.T*(4*sp.eye(44)+G)*z)[0])
            multiplier = max(1, z_energy//(2*norm_z)+1)
            smaller = multiplier*q-z
            smaller_energy = int((smaller.T*(4*sp.eye(44)+G)*smaller)[0])
            assert incidence*smaller == sp.zeros(14, 1)
            assert smaller_energy == z_energy-2*multiplier*norm_z < 0
            relation.update(incidence_free_witness=list(map(int, smaller)),
                incidence_free_energy=smaller_energy, incidence_free_multiplier=multiplier,
                z_energy=z_energy)
        relations.append(relation)
        break
    if not relations:
        # A negative vector in ker B has an M-independent energy directly.
        # Floating arithmetic proposes coefficients only; the saved verdict
        # is the exact integer value of q^t(4I+Gamma)q.
        basis = sp.Matrix.hstack(*[primitive(column) for column in incidence.nullspace()])
        compressed_free = basis.T*(4*sp.eye(44)+G)*basis
        values, vectors = np.linalg.eigh(np.array(compressed_free, dtype=float))
        if values[0] < -1e-9:
            direction = vectors[:, 0]/max(abs(vectors[:, 0]))
            for scale in (1, 2, 4, 8, 16, 32, 64, 128, 256, 1024, 4096, 16384):
                coefficients = sp.Matrix([int(round(scale*x)) for x in direction])
                q = primitive(basis*coefficients)
                energy = int((q.T*(4*sp.eye(44)+G)*q)[0])
                if energy < 0:
                    assert incidence*q == sp.zeros(14, 1)
                    assert int((q.T*U15*q)[0]) == 15*energy
                    relations.append(dict(kind='NEGATIVE_ENERGY_IN_KER_B',
                        negative_witness=list(map(int, q)),
                        q_support=sum(int(x != 0) for x in q),
                        uniform_witness_energy_upper=energy,
                        source_witness_energy_times15=15*energy))
                    break
    if not relations:
        # Even without Bq=0, U(M)<=4I+Gamma for every mate involution.
        values, vectors = np.linalg.eigh(np.array(4*sp.eye(44)+G, dtype=float))
        if values[0] < -1e-9:
            direction = vectors[:, 0]/max(abs(vectors[:, 0]))
            for scale in (1, 2, 4, 8, 16, 32, 64, 128, 256, 1024, 4096, 16384):
                q = primitive(sp.Matrix([int(round(scale*x)) for x in direction]))
                energy = int((q.T*(4*sp.eye(44)+G)*q)[0])
                if energy < 0:
                    source_energy15 = int((q.T*U15*q)[0])
                    assert source_energy15 <= 15*energy < 0
                    relations.append(dict(kind='ADJACENCY_BELOW_MINUS_FOUR',
                        negative_witness=list(map(int, q)),
                        q_support=sum(int(x != 0) for x in q),
                        uniform_witness_energy_upper=energy,
                        source_witness_energy_times15=source_energy15))
                    break
    proof = [
        'Adjacency case: L(M) is PSD for every involution M, so U(M)<=4I+Gamma. A saved negative integer value of q^t(4I+Gamma)q is therefore an upper bound on q^t U(M)q for every M, even if Bq is not zero.',
        'Negative-energy case: Bq=0 implies q^t U(M)q=q^t(4I+Gamma)q for EVERY M. A saved negative integer value excludes every mate assignment immediately.',
        'Zero-energy leakage case: the certificate gives Bq=0, z=(4I+Gamma)q nonzero and q^t z=0. Thus U(M)q=z and q^t U(M)q=0 for EVERY root-mate involution M, not merely the source assignment.',
        'Positive semidefiniteness would turn a zero-energy vector into a kernel vector, contradicting U(M)q=z nonzero. Hence no outer rematching of this fixed adjacency can make U PSD, independently of T or its nullity.',
        'Explicit uniform separator: L(M)=[B^t(4I-M)B+2J]/15 is PSD because4I-M is positive definite. If Gamma has maximum degree d, U(M)<=4I+Gamma<=(4+d)I. With t=4+d and w=t*q-z, w^t U(M)w=-2t||z||^2+z^t U(M)z<=-t||z||^2<0. The same integer w therefore rejects every mate assignment.',
        'If Bz also vanishes, a smaller saved witness w=t*q-z has the exactly M-independent energy z^t(4I+Gamma)z-2t||z||^2. The smallest positive integer t making this negative is used for the additional incidence_free_witness.',
    ]
    result = dict(status=('ALL_OUTER_MATE_ASSIGNMENTS_EXCLUDED_BY_ONE_EXACT_WITNESS'
                          if relations else 'NO_MATE_INVARIANT_WITNESS_FOUND'),
        source=str(source), labels=LABELS, relations=relations, proof=proof,
        seconds=time.monotonic()-start,
        scope='A proof about every outer rematching of this fixed adjacency. No universal H-MATCH proof and no new source PSD/rank audit.')
    Path(output).write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(status=result['status'], found=len(relations),
        uniform_energy_upper=relations[0]['uniform_witness_energy_upper'] if relations else None,
        seconds=result['seconds'])), flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    run(args.source, args.output)
