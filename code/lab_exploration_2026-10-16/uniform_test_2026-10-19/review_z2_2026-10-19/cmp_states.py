import sys, json, gzip, runpy, io, contextlib
CAT, VER, CODEX = sys.argv[1], sys.argv[2], sys.argv[3]
CDIR = sys.argv[4]
sys.path.insert(0, CODEX)
from root_component_z_distribution import row_catalogue, RECTANGLES
d = json.loads(gzip.decompress(open(CAT, 'rb').read()))
for g in [9748, 5986, 5984, 9997, 5128]:
    mine = {int(k): set(map(tuple, v)) for k, v in json.load(open('states_%d.json' % g)).items()}
    # verifier enumeration: run its module code with a cert stub (need certificate_explicit) -> use a fake cert file
    stub = 'stub_%d.json' % g
    json.dump({'template_index': g, 'certificate_explicit': {'y_eq': {}, 'y_ub': {}, 'y_up': {}}}, open(stub, 'w'))
    sys.argv = ['z2_verify.py', CAT, stub]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        gl = runpy.run_path(VER, run_name='__main__')
    ver = {}
    for qi, z in gl['types']:
        ver.setdefault(qi, set()).add(tuple(z))
    cat = row_catalogue(d['open'][g]['template'], max_free=7)
    cod = {qi: set(map(tuple, r['states'])) for qi, r in enumerate(cat['row_types'])}
    same_mv = all(mine.get(q, set()) == ver.get(q, set()) for q in range(21))
    same_mc = all(mine.get(q, set()) == cod.get(q, set()) for q in range(21))
    print(g, 'mine==verifier', same_mv, 'mine==codex', same_mc, 'total', sum(len(mine[q]) for q in range(21)),
          'stub-cert verdict', json.loads(buf.getvalue())['valid'], 'free_dim', cat['free_dimension'])
