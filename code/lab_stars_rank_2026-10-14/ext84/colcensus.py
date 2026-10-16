"""Census of exact outside-column domains (Codex's enumerate_column) over many rank-30 germs.
For each germ: number of the 40 outside labels with a non-empty complete domain, total domain size, incomplete count.
usage: python colcensus.py <out json> <glob> [<glob> ...]"""
import sys, json, glob, time
from itertools import combinations
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from four_star_completion_columns import prepare, inverse_on_range, enumerate_column
OUTSIDE = [p for p in combinations(range(4, 14), 2) if p[1] != (p[0] ^ 1)]
out = sys.argv[1]
files = sorted(set(sum((glob.glob(p) for p in sys.argv[2:]), [])))
res = []
t0 = time.monotonic()
for f in files:
    try:
        rec = json.loads(Path(f).read_text(encoding='utf-8'))
        if len(rec.get('labels', [])) != 44:
            continue
        gamma, t8, u15, kt, ku = prepare(rec)
    except Exception as ex:
        continue
    if kt.shape[1] != 14:
        continue
    ti, ui = inverse_on_range(t8), inverse_on_range(u15)
    nonempty, total, incomplete, sizes = 0, 0, 0, {}
    for lab in OUTSIDE:
        col = enumerate_column(lab, gamma, kt, ku, ti, ui, 2.0)
        k = len(col['domains'])
        sizes[str(lab)] = k
        total += k
        nonempty += (k > 0)
        incomplete += (not col['complete'])
    res.append(dict(file=f, nonempty=nonempty, total=total, incomplete=incomplete, U_rank=len(ui[0]), sizes=sizes))
    print("%s nonempty %d total %d incomplete %d" % (Path(f).name, nonempty, total, incomplete), flush=True)
Path(out).write_text(json.dumps(res, indent=1), encoding='utf-8')
print("germs %d, seconds %.1f" % (len(res), time.monotonic() - t0))
