"""Lab session, 2026-10-13. Mission "C2 without computation": exact identities forced by modular forms.

Assume Theorem R and "no integral vector with 1 <= E <= T" (T = 10 with the lemmas T16, T18, T20), and the shadow
condition (no shadow vector with E < 11.5). The coefficient table then lies in an affine space (constant term 1).
This script computes, in exact rationals, the TOTAL number of vectors for each (kind, E) (sum over the classes) as an
affine function of a few free totals, i.e. the exact linear identities between these numbers.
Notation of the output: I(E) = number of integral vectors v of U, counted once per class representative, with that E;
S(E) = number of shadow vectors; I0(E) = class 0 only (E = 14: roots of N; E = 21: norm-3 vectors of N; E = 28: norm 4).
python exact_identities.py <EMAX> <T>        pure rationals, seconds."""
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


def rref(C, ncols):
    C = [row[:] for row in C]
    piv = []
    r = 0
    for c in range(ncols):
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
    return C[:r], piv


full = [[t.get(k, 0) for k in keys] for t in tabs]
basis = independent_rows(full)
assert len(basis) == 61
B = [full[i] for i in basis]
cond = [j for j, k in enumerate(keys) if (k[0] == "I" and 0 < k[2] <= 4 * T) or (k[0] == "S" and k[2] < 46)]
C, piv = rref([[Fraction(B[i][j]) for i in range(61)] for j in cond], 61)
free = [c for c in range(61) if c not in piv]
null = []
for f in free:
    lam = [Fraction(0)] * 61
    lam[f] = Fraction(1)
    for row, c in zip(C, piv):
        lam[c] = -row[f]
    null.append(lam)
print("threshold %d: solution space of dimension %d" % (T, len(null)))
# functionals: totals per (kind, E), and class 0 alone
funcs = {}
for j, k in enumerate(keys):
    funcs.setdefault(("%s(%g)" % (k[0], k[2] / 4)), []).append(j)
    if k[0] == "I" and k[1] == (0, 0):
        funcs.setdefault("I0(%g)" % (k[2] / 4), []).append(j)
names = sorted(funcs, key=lambda s: (float(s[s.index("(") + 1:-1]), s))
names = [nm for nm in names if float(nm[nm.index("(") + 1:-1]) <= 21 and not (nm.startswith("I(") and ("I0" + nm[1:]) in funcs and len(funcs[nm]) == 1)]
vals = {nm: [sum(sum(lam[i] * B[i][j] for i in range(61)) for j in funcs[nm]) for lam in null] for nm in names}
# express everything through the constant term and the first independent totals
rows = [vals[nm] for nm in names]
R, pv = rref([[row[t] for row in rows] for t in range(len(null))], len(names))     # transpose: columns = functionals
params = [names[c] for c in pv]
print("free quantities: %s" % ", ".join(params))
for ci, nm in enumerate(names):
    if ci in pv:
        continue
    coef = [R[t][ci] for t in range(len(pv))]
    terms = " + ".join("(%s) %s" % (cf, params[t]) for t, cf in enumerate(coef) if cf != 0)
    print("   %-9s = %s" % (nm, terms if terms else "0"))
