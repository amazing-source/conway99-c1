"""Prove C4DO for flat incidence-zero kernel vectors of support at most12.

This is an analytic exclusion of their44-label extensions, not a solver
verdict. The three tiny integer budgets below certify the final inequality.
"""
import argparse
import json
from pathlib import Path


PROOF = [
    "Let Gamma be a binary44-label block satisfying the four central-star C1 equations and the C2 common-neighbour caps, and let T and U be PSD with the usual Conway geometry. Suppose q is a nonzero vector with entries0,+1,-1, Bq=0, Tq=0, support at most12, and w_C.q nonzero. Since Kq=0, Gamma*q=3*q. The six-vertex prism lemma forces six positive and six negative vertices, each inducing a prism, with no edges between the signs. Its proof and the covering core classification are in four_star_flat_kernel_prism_cores.py.",
    "A repeated root letter in a prism must close one of its three vertical edges: triangle edges already have their common neighbour, and nonadjacent prism pairs already have two. Thus a prism vertex cannot carry two repeated letters. The total central incidence is6+o, where o counts its overlap vertices. This forces o<=1. Bq=0 and w_C.q nonzero force exactly one overlap label of each sign, sharing the unique multiplicity-one central root. Normalize these labels to +02,-03. The root multiplicities of either sign are r=(1,2,2,2) on the centres, with five distinct exterior letters of multiplicity1 and all other exterior multiplicities0. All three vertical edges are closed by central roots1,2,3.",
    "Every vertex outside the two prisms meets either prism in at most one vertex. Meeting two triangle-adjacent or nonadjacent vertices exceeds the C2 capacity; meeting a vertical pair also exceeds it because that pair already has its common root neighbour. Let v be the positive prism indicator, and define k=Gamma*v-3v. Then k is binary, zero on both prisms, and Gamma*q=3q makes the two outside-prism neighbour counts equal.",
    "Let p be the number of mate pairs entirely contained in the five exterior letters. Then p is0,1,2. Put f=(3I+M)r. Its central entries are(5,7,8,8). Among the ten exterior entries there are2p fours,5-2p threes,5-2p ones and2p zeros. With T8=8T, w=T8*v=12*1-B^t*f-8k. Moreover d=v^t*T8*v=72-r^t(3I+M)r=6-2p.",
    "For either unused overlap label12 or13, w_x=-3-8k_x and (T8)_xx=20. PSD on the two vectors(v,e_x) gives w_x^2<=20d<=120. If k_x=1 the left side is121, impossible. Thus k vanishes on all four overlap labels. This strict one-unit inequality uses T PSD alone.",
    "Sum k over central star a. C1 gives sum_{x in L_a}(Gamma*v)_x=12-r_a-r_{a^1}. Subtracting3r_a yields sum_{x in L_a}k_x=12-4r_a-r_{a^1}, namely(6,3,2,2). Since k vanishes on the overlap, these are also the sums on the ten exterior labels of each star.",
    "Write b=12*1-B^t*f. Directly from the listed multiplicities, ||b||^2=480+48p, with overlap contribution20. On an exterior coordinate in central star a, changing k from0 to1 changes w_x^2 by64-16b_x. To lower-bound ||w||^2, relax the forced zeros on the support and choose the6,3,2,2 smallest such increments separately in the four stars. The resulting exact lower bounds are384,304,304 for p=0,1,2 respectively.",
    "On the other hand T+U=7Pi, where Pi=I-(11B^tB+B^tMB-2J)/120. Because B^t J_14 B=4J, the subtracted matrix equals B^t(11I+M-J_14/2)B/120. The inner matrix has eigenvalues5 on constants,12 on the nonconstant M-even space,10 on the M-odd space, so Pi<=I. With T,U PSD this gives0<=T8<=56I. Hence ||T8*v||^2<=56*v^t*T8*v=56d, namely336,224,112 in the three cases.",
    "The lower bounds384,304,304 strictly exceed336,224,112. This contradiction excludes every44-label extension containing such a q. Equivalently every incidence-zero kernel vector with coefficients0,+1,-1 and support at most12 satisfies C4DO. No assumption of h symmetry, modular rank, nullity14 or C1-prime is used beyond the stated C1/C2 caps. General coefficients, nonzero incidence, larger support, ODDCONST, N9-NG, NG5 and NG7 remain outside this theorem.",
    "Structural corollary: none of the832 labelled twelve-vertex cores can occur as an induced subgraph of an admissible44-label block. Indeed each core already has its sign vector in its principal T kernel. Full T PSD extends a principal kernel vector by zero, supplying the global kernel hypothesis automatically. No additional prescribed-kernel assumption is needed for this forbidden induced-core conclusion.",
]


def certificate():
    rows = []
    for pairs in range(3):
        exterior_f = [4]*(2*pairs)+[3]*(5-2*pairs)+[1]*(5-2*pairs)+[0]*(2*pairs)
        assert len(exterior_f) == 10
        assert sum(exterior_f) == 20
        assert sum(x*x for x in exterior_f) == 50+12*pairs
        central_f = [5, 7, 8, 8]
        counts = [6, 3, 2, 2]
        baseline = 20+sum((12-c-y)**2 for c in central_f for y in exterior_f)
        assert baseline == 480+48*pairs
        chosen = [sorted(64-16*(12-c-y) for y in exterior_f)[:n]
                  for c, n in zip(central_f, counts)]
        lower = baseline+sum(map(sum, chosen))
        energy = 6-2*pairs
        upper = 56*energy
        assert 121 > 20*energy
        assert lower > upper
        rows.append(dict(exterior_mate_pairs=pairs, prism_T8_energy=energy,
                         unused_overlap_nonzero_profile_square=121,
                         unused_overlap_PSD_upper=20*energy,
                         baseline_squared_norm=baseline,
                         minimum_star_corrections=list(map(sum, chosen)),
                         squared_norm_lower=lower, spectral_squared_norm_upper=upper,
                         contradiction_margin=lower-upper))
    assert [r['squared_norm_lower'] for r in rows] == [384, 304, 304]
    return dict(status='PROVED_FLAT_INCIDENCE_ZERO_C4DO_SUPPORT_AT_MOST_TWELVE',
                proof=PROOF, cases=rows,
                hypotheses=['binary Gamma', 'four complete central-star C1 equations',
                            'C2 capacities including root-label intersections', 'T PSD', 'U PSD',
                            'q in ker T', 'Bq=0', 'q entries in{0,+1,-1}', 'support(q)<=12'],
                conclusion='q(02)-q(03)-q(12)+q(13)=0',
                scope='All832 classified cores are forbidden as induced subgraphs of an admissible44-label block: PSD propagates their principal kernel relation. This does not prove general C4DO, N9-NG, NG5 or NG7, and does not exclude Conway.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = certificate()
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in ('proof', 'hypotheses')}, indent=2))
