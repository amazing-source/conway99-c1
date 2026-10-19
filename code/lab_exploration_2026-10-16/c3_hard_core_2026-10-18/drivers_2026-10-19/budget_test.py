import sys, json, gzip, time
codex, bpath, bi, att_s, sig_s, budget = sys.argv[1:7]
sys.argv = ['py_extend.py', codex, '2K2', bpath, '0', '0', '--sat', '--lean', '--enc=seq', '--conflicts=' + budget]
src_code = open('py_extend.py', encoding='utf8').read()
cut = src_code.index("OUT = next((a.split('=', 1)[1]")
exec(compile(src_code[:cut], 'py_extend.py', 'exec'))
src = json.loads(gzip.decompress(open(bpath, 'rb').read()))
core = src['core']
b = tuple(bytes.fromhex(src['boundaries_hex'][int(bi)]))
rows = materialize(core, b, tuple(tuple(x) for x in json.loads(att_s)), tuple(json.loads(sig_s)))
t = time.process_time()
cert = frontier(rows, True)
print(json.dumps({k: cert.get(k) for k in ('status', 'conflicts', 'proof_lines', 'cpu_seconds')}), round(time.process_time() - t, 1))
