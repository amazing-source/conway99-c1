import sys, time, json, random
ARGS = list(sys.argv)
sys.path.insert(0, '.')
import indep_model as M
prog = M.load_program(M.COVERS / 'core_000.json.gz')
assert [tuple(l) for l in prog.LABELS] == M.KL, 'label order differs'
assert prog.MATCH_BLOCKS == [(12, 4), (16, 0), (12, 8), (16, 8), (12, 16)], prog.MATCH_BLOCKS
assert prog.FLIP_LINES == [3, 6], prog.FLIP_LINES
assert prog.EXPECT == [M.expected_degree(u) for u in range(20)], (prog.EXPECT, [M.expected_degree(u) for u in range(20)])
print('EXPECT', prog.EXPECT)
print('OUTSIDE equal', [tuple(q) for q in prog.OUTSIDE] == M.OL, 'REGIONS', prog.REGIONS, 'Q12K', prog.Q12K, 'YOFF', prog.YOFF, 'EOFF', prog.EOFF)
sel = [(int(a), int(b)) for a, b in (x.split(':') for x in ARGS[1].split(','))]
for ci, bi in sel:
    cv = M.cover(ci); core = cv['core']; bd = tuple(bytes.fromhex(cv['boundaries_hex'][bi]))
    t = time.time()
    pa = [a for a, _ in prog.gen_attachments(core, bd)]
    t1 = time.time() - t; t = time.time()
    ma = M.my_attachments(core['edges'], bd)
    t2 = time.time() - t
    same = sorted(pa) == sorted(ma)
    rows_ok = all(prog.materialize(core, bd, a) == M.known_rows(core['edges'], bd, a) for a in pa)
    print(ci, bi, 'prog leaves', len(pa), 'my leaves', len(ma), 'same set', same, 'rows equal', rows_ok, 'times %.1f %.1f' % (t1, t2), flush=True)
