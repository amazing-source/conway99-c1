import sys, json, gzip
fam, bpath, bis = sys.argv[2], sys.argv[3], [int(x) for x in sys.argv[4].split(",")]
sys.argv = ['py_extend.py', sys.argv[1], fam, bpath, '0', '0']
src_code = open('py_extend.py', encoding='utf8').read()
cut = src_code.index("OUT = next((a.split('=', 1)[1]")
exec(compile(src_code[:cut], 'py_extend.py', 'exec'))
src = json.loads(gzip.decompress(open(bpath, 'rb').read()))
core = src['core']; att = Attachments(core) if Q12K else None
for bi in bis:
    b = tuple(bytes.fromhex(src['boundaries_hex'][bi]))
    n = 0; rs = set(); ats = set()
    for a in (att.for_boundary(b) if Q12K else [()]):
        for sg in (P4 if YY else [None]):
            rows = materialize(core, b, a, sg); n += 1
            rs.add(tuple(rows)); ats.add((tuple(map(tuple, a)) if a else (), sg))
    print(fam, "boundary", bi, "attachments x sigma:", n, "distinct (attached, sigma):", len(ats), "distinct rows:", len(rs))
