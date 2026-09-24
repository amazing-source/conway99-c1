"""Enumerate class-level twist patterns with exactly k twisting labels (rules R0, L12, L13a) up to the symmetry
S7 x (sign flips), for general k, by orbit-canonical generation over the multiset of classes of the twisting labels.
Canonical form: brute force over the stabiliser (permutations of classes, sign flips of classes containing 2
twisting labels are trivial at W-level). Output: data/k{k}_patterns.txt (spec format for rooted_family.py).
Usage: python wpatterns_k.py k
"""
import itertools, sys
import wpatterns_direct as wd

C7 = list(range(7))


def shapes(k):
    """class-occupation shapes: tuples (n_classes_with_2_labels, n_classes_with_1_label) with 2*a + b = k."""
    return [(a, k - 2 * a) for a in range(k // 2 + 1) if a + (k - 2 * a) <= 7]


def canon(pat):
    best = None
    for perm in itertools.permutations(C7):
        img = []
        for a, Cs in pat.items():
            img.append(((perm[a[0]], a[1]), tuple(sorted(perm[j] for j in Cs))))
        # sign normalisation per class: within a class, the twisting labels' signs are relabelled so that
        # a single twisting label has sign 0 (sign flips of that class) ; two labels -> {0,1}
        by_class = {}
        for (c, s), Cs in img:
            by_class.setdefault(c, []).append((s, Cs))
        norm = []
        for c, lst in by_class.items():
            if len(lst) == 1:
                norm.append(((c, 0), lst[0][1]))
            else:
                lst = sorted(lst, key=lambda z: z[1])
                norm += [((c, 0), lst[0][1]), ((c, 1), lst[1][1])]
        key = tuple(sorted(norm))
        if best is None or key < best:
            best = key
    return best


def enumerate_k(k):
    reps = {}
    for a2, b1 in shapes(k):
        labs = [(c, s) for c in range(a2) for s in (0, 1)] + [(a2 + i, 0) for i in range(b1)]
        options = {}
        for a in labs:
            others = [c for c in C7 if c != a[0]]
            options[a] = [frozenset(S) for r in range(2, 7) for S in itertools.combinations(others, r)]
        # backtracking with partial pruning on R0 only (full rules at leaves)
        def rec(i, pat):
            if i == len(labs):
                if wd.rules_ok(pat):
                    c = canon(pat)
                    reps.setdefault(c, dict(pat))
                return
            for S in options[labs[i]]:
                pat[labs[i]] = S
                rec(i + 1, pat)
            del pat[labs[i]]
        rec(0, {})
    return reps


if __name__ == '__main__':
    k = int(sys.argv[1])
    reps = enumerate_k(k)
    specs = [','.join(f'{a[0]}{a[1]}:' + ''.join(str(j) for j in sorted(Cs)) for a, Cs in sorted(p.items()))
             for p in reps.values()]
    open(f'../data/k{k}_patterns.txt', 'w', newline='\n').write('\n'.join(specs) + '\n')
    print(f'k = {k}: {len(specs)} patterns up to symmetry -> data/k{k}_patterns.txt')
