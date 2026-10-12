"""units for pi_a (a=1, mate 2) realising each B_xa type = partition of 6 (pairs (3,4),(5,6),...,(13,14))."""
def partitions(n, mx=None):
    mx = mx or n
    if n == 0: yield (); return
    for p in range(min(n, mx), 0, -1):
        for rest in partitions(n - p, p): yield (p,) + rest
P = [(2 * j + 1, 2 * j + 2) for j in range(1, 7)]
for tau in partitions(6):
    name = 't' + ''.join(map(str, tau)); lines = []; i = 0
    for l in tau:
        block = P[i:i + l]; i += l
        if l == 1: lines.append(f"pi 1 {block[0][0]} {block[0][1]}")
        else:
            for j in range(l): lines.append(f"pi 1 {block[j][1]} {block[(j + 1) % l][0]}")
    open(name + '.units', 'w').write("\n".join(lines) + "\n"); print(name, len(lines))
