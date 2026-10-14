"""Cubic multigraphs Psi on 12 points given as an ordered union of three perfect matchings (colours 0, 1, 2), up to
isomorphism and permutation of the colours. (NOTE_NIGHT 9.4: Psi = beta_a u beta_b u beta_c for a line with 12 prisms.)

Colour 0 is fixed to beta = {(0,1),(2,3),...,(10,11)}. The second matching runs over one representative of each
cycle type of beta u beta_b (partitions of 6), the third over all 10395 perfect matchings. Canonical form: for each
of the 6 colour permutations, each component is coded by the smallest traversal code over its start vertices; the
form is the smallest sorted tuple of component codes. Writes psi_reps.txt: one line per class,
(count, beta_b, beta_c) with the matchings as tuples of pairs.
"""
import itertools

N = 12
BETA = tuple((2 * i, 2 * i + 1) for i in range(6))


def all_matchings(points):
    if not points:
        yield ()
        return
    a = points[0]
    for i in range(1, len(points)):
        b = points[i]
        rest = points[1:i] + points[i + 1:]
        for m in all_matchings(rest):
            yield ((a, b),) + m


def to_map(m):
    d = {}
    for a, b in m:
        d[a] = b
        d[b] = a
    return d


def second_matchings():
    """One beta_b for each partition of 6: blocks arranged in alternating cycles of the given lengths."""
    reps = []
    for part in ([6], [5, 1], [4, 2], [4, 1, 1], [3, 3], [3, 2, 1], [3, 1, 1, 1], [2, 2, 2], [2, 2, 1, 1],
                 [2, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]):
        m = []
        blk = 0
        for k in part:
            blocks = list(range(blk, blk + k))
            blk += k
            if k == 1:
                m.append((2 * blocks[0], 2 * blocks[0] + 1))
            else:
                for i in range(k):
                    m.append(tuple(sorted((2 * blocks[i] + 1, 2 * blocks[(i + 1) % k]))))
        reps.append(tuple(sorted(m)))
    return reps


def canon(maps):
    """maps: three dicts (colour -> involution). Canonical form up to isomorphism and colour permutation."""
    best = None
    for perm in itertools.permutations(range(3)):
        mp = [maps[perm[0]], maps[perm[1]], maps[perm[2]]]
        seen_global = set()
        comps = []
        for s0 in range(N):
            if s0 in seen_global:
                continue
            # component of s0
            comp = {s0}
            stack = [s0]
            while stack:
                v = stack.pop()
                for c in range(3):
                    w = mp[c][v]
                    if w not in comp:
                        comp.add(w)
                        stack.append(w)
            seen_global |= comp
            bestc = None
            for s in comp:
                label = {s: 0}
                order = [s]
                i = 0
                code = []
                while i < len(order):
                    v = order[i]
                    i += 1
                    for c in range(3):
                        w = mp[c][v]
                        if w not in label:
                            label[w] = len(order)
                            order.append(w)
                        code.append(label[w])
                code = tuple(code)
                if bestc is None or code < bestc:
                    bestc = code
            comps.append(bestc)
        form = tuple(sorted(comps))
        if best is None or form < best:
            best = form
    return best


if __name__ == "__main__":
    ms = list(all_matchings(tuple(range(N))))
    assert len(ms) == 10395
    b0 = to_map(BETA)
    classes = {}
    for mb in second_matchings():
        b1 = to_map(mb)
        for mc in ms:
            f = canon([b0, b1, to_map(mc)])
            if f not in classes:
                classes[f] = [0, mb, mc]
            classes[f][0] += 1
    reps = sorted(classes.values(), key=lambda t: (-t[0], t[1], t[2]))
    with open("psi_reps.txt", "w") as out:
        for cnt, mb, mc in reps:
            out.write(repr((cnt, mb, tuple(sorted(mc)))) + "\n")
    print("classes of 3-edge-coloured cubic multigraphs on 12 points:", len(reps))
