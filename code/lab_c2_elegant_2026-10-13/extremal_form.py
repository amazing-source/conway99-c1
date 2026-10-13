"""Lab session, 2026-10-13. Mission "C2 without computation": the extremal form, in exact rational arithmetic.

For a threshold T: the forms of the 61-dimensional space (coarse model) whose integral coefficients with 1 <= E <= T
and whose shadow coefficients with E < 11.5 all vanish form a space of dimension d(T) (forcing_exact.py: 7, 3, 1 for
T = 10, 11, 12). For T = 12 the space is a line. This script computes it exactly (fractions), normalises the
constant term to 1 when it is not zero, and prints its coefficients, the negative ones first.
A theta series has non-negative coefficients and constant term 1; so if the line has a negative coefficient (or
constant term 0), no (U; y1, y2) satisfying the shadow condition has all its vectors outside J at E >= 13.
python extremal_form.py <EMAX> <T>        pure rationals, seconds."""
import sys, pickle
from fractions import Fraction

EMAX, T = int(sys.argv[1]), int(sys.argv[2])
desc, tabs = pickle.load(open("gen_tables_%d.pkl" % EMAX, "rb"))
keys = sorted(k for k in set().union(*[set(t) for t in tabs]) if any(t.get(k, 0) for t in tabs))
P = (1 << 61) - 1


def independent_rows(Mat):
    A = [[int(x) % P for x in row] for row in Mat]
    rows = len(A)
    order = list(range(rows))
    r = 0
    for c in range(len(A[0])):
        pr = next((i for i in range(r, rows) if A[i][c]), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        order[r], order[pr] = order[pr], order[r]
        inv = pow(A[r][c], P - 2, P)
        A[r] = [(x * inv) % P for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(x - f * y) % P for x, y in zip(A[i], A[r])]
        r += 1
        if r == rows:
            break
    return order[:r]


full = [[t.get(k, 0) for k in keys] for t in tabs]
basis = independent_rows(full)
assert len(basis) == 61
B = [full[i] for i in basis]
cond = [j for j, k in enumerate(keys) if (k[0] == "I" and 0 < k[2] <= 4 * T) or (k[0] == "S" and k[2] < 46)]
# unknown lambda in Q^61 with sum_i lambda_i B[i][j] = 0 for j in cond: null space of the matrix C (len(cond) x 61)
C = [[Fraction(B[i][j]) for i in range(61)] for j in cond]
piv = []
r = 0
for c in range(61):
    pr = next((i for i in range(r, len(C)) if C[i][c] != 0), None)
    if pr is None:
        continue
    C[r], C[pr] = C[pr], C[r]
    inv = 1 / C[r][c]
    C[r] = [x * inv for x in C[r]]
    for i in range(len(C)):
        if i != r and C[i][c] != 0:
            f = C[i][c]
            C[i] = [x - f * y for x, y in zip(C[i], C[r])]
    piv.append(c)
    r += 1
free = [c for c in range(61) if c not in piv]
print("threshold %d: %d conditions, rank %d, solution space of dimension %d" % (T, len(cond), r, len(free)))
if len(free) != 1:
    sys.exit()
lam = [Fraction(0)] * 61
lam[free[0]] = Fraction(1)
for row, c in zip(C, piv):
    lam[c] = -row[free[0]]
tab = {k: sum(lam[i] * B[i][j] for i in range(61)) for j, k in enumerate(keys)}
c0 = tab[("I", (0, 0), 0)]
print("constant term of the generator of the line: %s" % c0)
if c0 != 0:
    tab = {k: v / c0 for k, v in tab.items()}
assert all(tab[keys[j]] == 0 for j in cond)
neg = sorted((float(v), k) for k, v in tab.items() if v < 0)
print("negative coefficients (window E <= %d): %d" % (EMAX, len(neg)))
for v, k in neg[:12]:
    print("   %s, class %s, E = %g: %s = %.4f" % ("integral" if k[0] == "I" else "shadow", k[1], k[2] / 4, tab[k], v))
print("first non-zero coefficients:")
for k in sorted(keys, key=lambda k: (k[2], k[0], k[1])):
    if tab[k] != 0 and k[2] <= 4 * 15:
        print("   %s, class %s, E = %g: %s" % ("integral" if k[0] == "I" else "shadow", k[1], k[2] / 4, tab[k]))
