"""Lab session, 2026-10-13. Mission "C2 without computation": exact ranks behind the forcing statement.

For a threshold T, consider the forms F of the 61-dimensional space of weil_dimension.py (coarse model) such that
   (I)  every integral coefficient with 1 <= E <= T vanishes, and
   (S)  every shadow coefficient with E < 11.5 vanishes.
This script checks that the generators of gen_tables_<EMAX>.pkl (integers) have rank 61, so that they span the space,
and prints the rank of the conditions (I) + (S) for T = 8..12, hence the dimension of the space of such forms:
15, 11, 7, 3, 1. For T = 12 it is a line; extremal_form.py computes it and finds negative coefficients, which is the
contradiction. (A first version of this docstring said "only the zero form" for T = 12; that was a floating-point
reading and is wrong: the exact rank is 60.)
Ranks are computed modulo two primes; a rank modulo a prime is a lower bound for the rational rank.
python forcing_exact.py <EMAX>        pure integers, seconds."""
import sys, pickle

EMAX = int(sys.argv[1])
desc, tabs = pickle.load(open("gen_tables_%d.pkl" % EMAX, "rb"))
keys = sorted(k for k in set().union(*[set(t) for t in tabs]) if any(t.get(k, 0) for t in tabs))


def rank_mod(Mat, p):
    A = [[int(x) % p for x in row] for row in Mat]
    rows = len(A)
    cols = len(A[0]) if rows else 0
    r = 0
    for c in range(cols):
        pr = next((i for i in range(r, rows) if A[i][c]), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [(x * inv) % p for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        r += 1
        if r == rows:
            break
    return r


P1, P2 = (1 << 61) - 1, (1 << 89) - 1
full = [[t.get(k, 0) for k in keys] for t in tabs]
print("generators: %d ; rank of their tables (E <= %d): %d and %d modulo two primes" % (len(tabs), EMAX, rank_mod(full, P1), rank_mod(full, P2)))
for T in range(8, 13):
    cond = [k for k in keys if (k[0] == "I" and 0 < k[2] <= 4 * T) or (k[0] == "S" and k[2] < 46)]
    sub = [[t.get(k, 0) for k in cond] for t in tabs]
    r1, r2 = rank_mod(sub, P1), rank_mod(sub, P2)
    print("threshold %2d: %d positions (integral 1 <= E <= %d: %d, shadow E < 11.5: %d); rank %d and %d  ->  %s" % (
        T, len(cond), T, sum(1 for k in cond if k[0] == "I"), sum(1 for k in cond if k[0] == "S"), r1, r2,
        "only the zero form" if r1 == 61 else "a space of dimension %d survives" % (61 - r1)))
