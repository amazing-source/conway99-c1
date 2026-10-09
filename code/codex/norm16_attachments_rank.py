"""Exhaust the first attachment stage of all five norm-16 support cores.

Classifies attachments of the eight t=2 vertices, not graph completions.
Two complete enumeration methods are compared. All rank computations use F7.
An unrestricted symmetric completion witnesses sharpness of the block bound.
"""
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
PAIRS = list(combinations(range(8), 2))


def rref(a):
    a = [[x % 7 for x in row] for row in a]
    pivots = []
    for j in range(len(a[0])):
        r = len(pivots)
        pick = next((i for i in range(r, len(a)) if a[i][j]), None)
        if pick is None:
            continue
        a[r], a[pick] = a[pick], a[r]
        factor = pow(a[r][j], -1, 7)
        a[r] = [x*factor % 7 for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][j]:
                factor = a[i][j]
                a[i] = [(x-factor*y) % 7 for x, y in zip(a[i], a[r])]
        pivots.append(j)
        if len(pivots) == len(a):
            break
    return a, pivots


def rank(a):
    return len(rref(a)[1])


def kernel(a):
    reduced, pivots = rref(a)
    result = []
    for j in range(len(a[0])):
        if j in pivots:
            continue
        v = [0]*len(a[0])
        v[j] = 1
        for i, p in enumerate(pivots):
            v[p] = -reduced[i][j] % 7
        assert all(sum(x*y for x, y in zip(row, v)) % 7 == 0 for row in a)
        result.append(v)
    return result


def defects(b):
    m = [[0 if i == j else 2-sum(b[i][c]*b[j][c] for c in range(8))
          for j in range(8)] for i in range(8)]
    n = [[0 if i == j else 2-sum(b[c][i]*b[c][j] for c in range(8))
          for j in range(8)] for i in range(8)]
    return m, n


def edges_with_multiplicity(m):
    return [pair for pair in PAIRS for _ in range(m[pair[0]][pair[1]])]


def enumerate_backtracking(b, pe, qe):
    remaining = Counter(qe)
    capacity = [[2-b[i][j] for j in range(8)] for i in range(8)]
    chosen, masks, answers = [], [], set()
    states = 0

    def visit(d):
        nonlocal states
        states += 1
        if d == 8:
            answers.add(tuple(sorted(p+q for p, q in zip(pe, chosen))))
            return
        p = pe[d]
        for q in remaining:
            if not remaining[q]:
                continue
            if d and p == pe[d-1] and q < chosen[-1]:
                continue
            if any(sum(b[i][j] for j in q) > 1 for i in p):
                continue
            if any(sum(b[i][j] for i in p) > 1 for j in q):
                continue
            if any(capacity[i][j] == 0 for i in p for j in q):
                continue
            mask = sum(1 << i for i in p)+sum(1 << (8+j) for j in q)
            if any((mask & old).bit_count() > 2 for old in masks):
                continue
            remaining[q] -= 1
            for i in p:
                for j in q:
                    capacity[i][j] -= 1
            chosen.append(q)
            masks.append(mask)
            visit(d+1)
            masks.pop()
            chosen.pop()
            for i in p:
                for j in q:
                    capacity[i][j] += 1
            remaining[q] += 1

    visit(0)
    return answers, states


def enumerate_permutations(b, pe, qe):
    """Separate complete enumeration: 8! bijections, then whole-object checks."""
    answers = set()
    for order in permutations(qe):
        quadruples = tuple(p+q for p, q in zip(pe, order))
        # Every induced neighbourhood on these four vertices is a matching.
        if any(b[p][q]+b[p][s] > 1 or b[r][q]+b[r][s] > 1 or
               b[p][q]+b[r][q] > 1 or b[p][s]+b[r][s] > 1
               for p, r, q, s in quadruples):
            continue
        cells = Counter((p, q) for ps in quadruples for p in ps[:2] for q in ps[2:])
        if any(count > 2-b[p][q] for (p, q), count in cells.items()):
            continue
        neighborhoods = [set(ps[:2]) | {8+q for q in ps[2:]} for ps in quadruples]
        if any(len(x & y) > 2 for x, y in combinations(neighborhoods, 2)):
            continue
        answers.add(tuple(sorted(quadruples)))
    return answers


def automorphisms(b):
    columns = [tuple(i for i in range(8) if b[i][j]) for j in range(8)]
    lookup = {c: j for j, c in enumerate(columns)}
    answers = []
    for p in permutations(range(8)):
        images = [tuple(sorted(p[i] for i in column)) for column in columns]
        if not all(column in lookup for column in images):
            continue
        q = tuple(lookup[column] for column in images)
        assert all(b[i][j] == b[p[i]][q[j]] for i in range(8) for j in range(8))
        answers.append((p, q))
    return answers


def image(attachment, p, q):
    return tuple(sorted(tuple(sorted((p[i], p[j])))+tuple(sorted((q[k], q[l])))
                        for i, j, k, l in attachment))


def coupling_rows(b, attachment):
    """The 83 outside rows in order D(8), S(64), Z(11)."""
    rows = []
    cover = Counter()
    for i, j, k, l in attachment:
        row = [0]*16
        for point in (i, j, 8+k, 8+l):
            row[point] = 1
        rows.append(row)
        cover.update((p, q) for p in (i, j) for q in (k, l))
    singles = []
    for i in range(8):
        for j in range(8):
            count = 2-b[i][j]-cover[i, j]
            assert count >= 0
            row = [int(p == i or p == 8+j) for p in range(16)]
            singles.extend([row]*count)
    assert len(singles) == 64
    rows.extend(singles)
    rows.extend([[0]*16 for _ in range(11)])
    assert len(rows) == 83
    assert all(sum(row[:8]) == sum(row[8:]) for row in rows)
    assert all(sum(row[i] for row in rows) == 10 for i in range(16))
    return rows


def sharp_completion(f, outside):
    """A symmetric F7 matrix, not a 0/1 adjacency matrix or SRG."""
    pivots = rref(f)[1]
    rr = len(pivots)
    principal = [[f[i][j] for j in pivots] for i in pivots]
    reduced, ps = rref([row+[int(i == j) for j in range(rr)] for i, row in enumerate(principal)])
    assert ps[:rr] == list(range(rr))
    inv = [row[rr:] for row in reduced]
    cross = [[row[i] for i in pivots] for row in outside]
    left = [[sum(row[t]*inv[t][j] for t in range(rr)) % 7 for j in range(rr)] for row in cross]
    h = [[sum(x*y for x, y in zip(row, col)) % 7 for col in cross] for row in left]
    completed = [f[i]+[row[i] for row in outside] for i in range(16)]
    completed.extend([outside[i]+h[i] for i in range(83)])
    assert all(completed[i][j] % 7 == completed[j][i] % 7 for i in range(99) for j in range(99))
    return rank(completed)


def main():
    source = ROOT/'data/codex_norm16_cores.json'
    report = []
    for case in json.loads(source.read_text())['cases']:
        if not case['representatives']:
            continue
        b = case['representatives'][0]
        m, n = defects(b)
        pe, qe = edges_with_multiplicity(m), edges_with_multiplicity(n)
        assert len(pe) == len(qe) == 8
        attachments, states = enumerate_backtracking(b, pe, qe)
        second = enumerate_permutations(b, pe, qe)
        assert attachments == second
        f = [[-3*int(i == j) for j in range(16)] for i in range(16)]
        for i in range(8):
            for j in range(8):
                f[i][8+j] = f[8+j][i] = b[i][j]
        ker = kernel(f)
        fr = rank(f)
        assert fr+len(ker) == 16
        coupling_ranks = Counter()
        for attachment in attachments:
            rows = coupling_rows(b, attachment)
            k = [[sum(x*y for x, y in zip(row, vector)) % 7 for vector in ker] for row in rows]
            kr = rank(k)
            assert kr == len(ker)-1
            coupling_ranks[kr] += 1
        autos = automorphisms(b)
        unseen = set(attachments)
        orbits = []
        while unseen:
            representative = min(unseen)
            orbit = {image(representative, p, q) for p, q in autos}
            assert orbit <= unseen
            unseen -= orbit
            orbits.append({'representative': representative, 'size': len(orbit)})
        assert sum(o['size'] for o in orbits) == len(attachments)
        bound = fr+2*(len(ker)-1)
        exact_completion_rank = sharp_completion(f, coupling_rows(b, min(attachments)))
        assert exact_completion_rank == bound
        # Independent rank implementation on the fixed support blocks.
        import sympy as sp
        from norm14_audit import rank7
        assert rank7(sp.Matrix(f)) == fr
        entry = {'defect_cycle_lengths': case['defect_cycle_lengths'],
                 'support_rank7': fr, 'support_nullity7': len(ker),
                 'attachment_count_fixed_B_unlabelled_D': len(attachments),
                 'backtracking_states': states, 'permutation_crosscheck_identical': True,
                 'side_preserving_automorphism_order': len(autos),
                 'side_preserving_attachment_orbits': len(orbits),
                 'kernel_coupling_rank_distribution': dict(coupling_ranks),
                 'block_rank_lower_bound': bound,
                 'unrestricted_symmetric_completion_rank': exact_completion_rank,
                 'sorted_attachments_sha256': hashlib.sha256(json.dumps(sorted(attachments), separators=(',', ':')).encode()).hexdigest(),
                 'orbits': orbits}
        report.append(entry)
        print(json.dumps({k: v for k, v in entry.items() if k != 'orbits'}), flush=True)
    output = {'scope': 'First D attachments and support-block ranks only; no 99-vertex completion or exclusion.',
              'source_normalized_lf_sha256': hashlib.sha256(source.read_bytes().replace(b'\r\n', b'\n')).hexdigest(),
              'cases': report}
    (ROOT/'data/codex_norm16_attachments_rank.json').write_text(json.dumps(output, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
