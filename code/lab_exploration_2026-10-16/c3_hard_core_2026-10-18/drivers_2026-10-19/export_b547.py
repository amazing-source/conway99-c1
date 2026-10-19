import sys, json, gzip
codex, bpath, bi, att_s, sig_s, outp = sys.argv[1:7]
sys.argv = ['py_extend.py', codex, '2K2', bpath, '0', '0', '--sat', '--lean', '--enc=seq']
src_code = open('py_extend.py', encoding='utf8').read()
cut = src_code.index("OUT = next((a.split('=', 1)[1]")
exec(compile(src_code[:cut], 'py_extend.py', 'exec'))
src = json.loads(gzip.decompress(open(bpath, 'rb').read()))
core = src['core']
b = tuple(bytes.fromhex(src['boundaries_hex'][int(bi)]))
attached = tuple(tuple(x) for x in json.loads(att_s)); sigma = tuple(json.loads(sig_s))
# check that this attachment is indeed produced by the enumeration
att = Attachments(core)
assert any(tuple(map(tuple, a)) == attached for a in att.for_boundary(b)), 'attachment not in enumeration'
rows = materialize(core, b, attached, sigma)
cert = frontier(rows, True)
print(cert['status'])
json.dump({'family': '2K2', 'core_index': src['core_index'], 'boundary_index': int(bi), 'boundary_hex': src['boundaries_hex'][int(bi)],
           'attachment': attached, 'sigma': sigma, 'known_labels': [list(l) for l in LABELS], 'rows': rows,
           'outside_labels': [list(q) for q in OUTSIDE], 'status': cert['status'],
           'selected_profiles': cert.get('selected_profiles'),
           'note': 'known order: K 0..7 (Q01 then Q02), Q12 8..11, Q34 12..15, Q56 16..19; corner = 2s+t'}, open(outp, 'w'))
