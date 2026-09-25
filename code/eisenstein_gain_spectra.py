"""notes/113 R3 — the Eisenstein line-orientation gain H = (-A + i*sqrt3*T)/2 (T = cyclic orientation of the 231 lines)
has H ≡ A (mod pi), H1 = -7*1, 7I + H PSD, so chi_H ≡ x^54 (x+1)^45 (mod 3), tr H = 0, tr H^2 = tr H^3 = 1386.
Exhaustive search: no integer spectrum with <= 3 distinct eigenvalues (C2's hand proof: (a-2)(b-2) = -12, notes/113)."""
import itertools

sols = []
for k in (1, 2, 3):
    for ev in itertools.combinations(range(-7, 15), k):
        if -7 not in ev:
            continue
        for mult in itertools.product(range(1, 100), repeat=k - 1):
            m = list(mult) + [99 - sum(mult)]
            if m[-1] < 1:
                continue
            if sum(mi for x, mi in zip(ev, m) if x % 3 == 0) != 54 or sum(mi for x, mi in zip(ev, m) if x % 3 == 2) != 45:
                continue
            if [sum(x ** t * mi for x, mi in zip(ev, m)) for t in (1, 2, 3)] == [0, 1386, 1386]:
                sols.append((ev, m))
print("integer spectra with <= 3 eigenvalues:", sols)
assert not sols
