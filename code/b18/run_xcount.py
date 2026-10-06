import json, subprocess, time, sys
sups = json.load(open('supports18.json'))
tl = float(sys.argv[1]) if len(sys.argv) > 1 else 120
which = range(len(sups)) if len(sys.argv) < 3 else [int(a) for a in sys.argv[2].split(',')]
for s in which:
    rows = sups[s]
    D = '\n'.join(''.join('1' if v in r else '0' for v in range(9)) for r in rows) + '\n'
    t = time.time()
    try:
        out = subprocess.run(['./xcount'], input=D, capture_output=True, text=True, timeout=tl).stdout.strip()
    except subprocess.TimeoutExpired:
        out = f'TIMEOUT>{tl}s'
    print(s, out, round(time.time() - t, 1), flush=True)
