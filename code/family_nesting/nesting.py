# Fixed subgraphs of automorphisms of odd prime order in the family srg(v_t, k_t, 1, 2), t in {1,3,4,10,31}.
# Fix(g) has lambda=1, mu=2 exactly  =>  Fix in {empty, K1, K3} or a smaller family member (or the whole graph).
# Necessary conditions: |Fix|(k-k') <= v-|Fix| (a non-fixed vertex has at most one fixed neighbour), p | (k-k')/2 (non-fixed triangles through a fixed vertex are permuted in p-cycles;
# for Fix = empty: p | v), v = v' (mod p), and the character
#   chi_r(g) = (a1 + (t+1) v' - (k+t+1)) / (2t+1)  in Z,  chi_r = f (mod p),  |chi_r| <= f,
# for some a1 = #{x : x ~ g(x)} with a1 = 0 (mod p), 0 <= a1 <= v - v'.
from sympy import primefactors
fam = {}
for t in (1, 3, 4, 10, 31):
    k = t * t + t + 2; v = 1 + k + k * (k - 2) // 2; r, s = t, -(t + 1)
    f = (-(k) - s * (v - 1)) // (r - s); g = v - 1 - f
    assert k + f * r + g * s == 0
    fam[t] = dict(v=v, k=k, f=f, g=g)
fixopts = lambda t: [('empty', 0, 0), ('K1', 1, 0), ('K3', 3, 2)] + [(f'srg({fam[u]["v"]})', fam[u]['v'], fam[u]['k']) for u in fam if u < t]
for t in (3, 4, 10, 31):
    F = fam[t]; v, k, f = F['v'], F['k'], F['f']
    print(f"== srg({v},{k},1,2)  t={t}  f={f} g={F['g']}")
    for name, vp, kp in fixopts(t):
        cand = primefactors(v) if vp == 0 else primefactors((k - kp) // 2) if k > kp else []
        for p in cand:
            if p == 2 or (v - vp) % p: continue
            if vp * (k - kp) > v - vp:
                print(f"   p={p:<4} Fix={name:<12} EXCLUDED by |Fix|(k-k') <= v-|Fix|  ({vp*(k-kp)} > {v-vp})"); continue
            sols = []
            for a1 in range(0, v - vp + 1, p):
                num = a1 + (t + 1) * vp - (k + t + 1)
                if num % (2 * t + 1): continue
                chi = num // (2 * t + 1)
                if (chi - f) % p == 0 and abs(chi) <= f: sols.append((a1, chi))
            if sols:
                a1s = [a for a, _ in sols]
                print(f"   p={p:<4} Fix={name:<12} feasible; a1 = {a1s[0]} (mod {a1s[1]-a1s[0] if len(a1s)>1 else '-'}), e.g. a1={a1s[0]} chi_r={sols[0][1]}")
            else:
                print(f"   p={p:<4} Fix={name:<12} EXCLUDED by the character")

print()
print("Hoffman point c: other coclique points (= edges of Gamma_c, t-regular on k vertices) vs pairs of triangles through c")
for t in (1, 3, 4, 10, 31):
    F = fam[t]; v, k = F['v'], F['k']; a = v * (t + 1) // (k + t + 1)
    assert a * (k + t + 1) == v * (t + 1)
    print(f"  t={t:<3} v={v:<7} alpha_H={a:<6} points-1={a-1:<6} pairs={(k//2)*(k//2-1)//2:<7} 2t vs k/2-1: {2*t} vs {k//2-1}")
