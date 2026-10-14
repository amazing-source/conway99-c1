"""Which GQ orders (s,t) can carry a 3-ovoid inducing a strongly regular graph (lambda = 1)? mu = 4(t+1)/(3s-2) must
be an integer (14/10/2026). Scans all (s,t) with s,t <= 2000 satisfying the standard GQ divisibility and Higman
conditions (s+t | st(s+1)(t+1), t <= s^2, s <= t^2, s >= 2), and the five classical families with prime powers q."""
def ok_gq(s, t):
    return s >= 2 and t >= 1 and t <= s * s and s <= t * t and (s * t * (s + 1) * (t + 1)) % (s + t) == 0
hits = []
for s in range(2, 2001):
    for t in range(1, 2001):
        if not ok_gq(s, t):
            continue
        if (4 * (t + 1)) % (3 * s - 2) == 0:
            mu = 4 * (t + 1) // (3 * s - 2)
            v = 3 * (s * t + 1)
            k = 2 * (t + 1)
            if mu >= 1 and k * (k - 2) == mu * (v - k - 1):
                hits.append((s, t, v, k, mu))
print("orders (s,t) passing the GQ conditions with integer mu, s,t <= 2000:")
for h in hits:
    print("  GQ(%d,%d): 3-ovoid would give srg(%d,%d,1,%d)" % h)
