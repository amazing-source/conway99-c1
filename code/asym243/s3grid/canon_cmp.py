import subprocess, glob, os
def g6(fn):
    E = [tuple(map(int, l.split())) for l in open(fn) if l.strip()]
    n = 1 + max(max(e) for e in E); adj = [set() for _ in range(n)]
    for u, v in E: adj[u].add(v); adj[v].add(u)
    bits = [1 if j in adj[i] else 0 for j in range(1, n) for i in range(j)]
    bits += [0] * (-len(bits) % 6)
    head = chr(126) + chr(63 + (n >> 12 & 63)) + chr(63 + (n >> 6 & 63)) + chr(63 + (n & 63)) if n > 62 else chr(n + 63)
    return head + "".join(chr(63 + int("".join(map(str, bits[i:i + 6])), 2)) for i in range(0, len(bits), 6))
R = '/home/user/strongly-regular-graphs-research/results/srg243_family/'
files = [R + f for f in ['bvls243.edges', 'twin243.edges', 'gamma3_aut864.edges', 'gamma4_aut3888.edges']] + sorted(glob.glob('graphs/z3r_*.edges'))
inp = "\n".join(g6(f) for f in files) + "\n"
out = subprocess.run(['/tmp/solvers/nauty_src/nauty2_8_8/labelg', '-q'], input=inp, capture_output=True, text=True).stdout.split()
known = {out[i]: os.path.basename(files[i]) for i in range(4)}
for f, c in zip(files[4:], out[4:]):
    print(os.path.basename(f), '->', known.get(c, 'NEW GRAPH'))
