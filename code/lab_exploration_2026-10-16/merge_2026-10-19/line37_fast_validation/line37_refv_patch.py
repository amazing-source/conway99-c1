# Make a validation copy of line37.cpp: file mode "filev" prints status, x, candidates, nodes and a hash of the
# candidate list (FNV-1a style over (var, qi, si, bits of dd), in list order), exactly as line37_fast's filev mode.
# Only output is added; the engine and the preparation are untouched.
import sys
src = open(sys.argv[1], encoding='utf-8').read()
NL = "\\" + "n"


def rep(a, b):
    global src
    assert a in src, a
    src = src.replace(a, b, 1)


rep('struct Outcome { string status; int x; long long cand, nodes; double t_build, t_prep, t_search; };',
    'struct Outcome { string status; int x; long long cand, nodes; double t_build, t_prep, t_search; unsigned long long chash; };\n'
    'static unsigned long long CH_ = 0;\n'
    'static inline void hmix_(unsigned long long v) { CH_ ^= v; CH_ *= 1099511628211ULL; }')
rep('    Outcome o{"", -1, 0, 0, 0, 0, 0};', '    Outcome o{"", -1, 0, 0, 0, 0, 0, 0};')
rep('    if (!okx) { o.status = "no-x"; return o; }',
    '    if (!okx) { o.status = "no-x"; return o; }\n'
    '    CH_ = 1469598103934665603ULL;\n'
    '    for (int v = 0; v < NV; v++) for (size_t c = 0; c < V[v].cand.size(); c++) {\n'
    '        const Tri& t = V[v].tri[V[v].cand[c].ti]; unsigned long long db; memcpy(&db, &t.dd, 8);\n'
    '        hmix_((unsigned long long)v); hmix_((unsigned long long)t.qi); hmix_((unsigned long long)t.si); hmix_(db);\n'
    '    }\n'
    '    o.chash = CH_;')
rep('    if (mode == "file") {', '    if (mode == "file" || mode == "filev") {\n        bool vv = (mode == "filev");')
rep('            Outcome o = test_line(s, s + 12, s + 24);\n            printf(',
    '            Outcome o = test_line(s, s + 12, s + 24);\n'
    '            if (vv) { printf("{\\"line\\": %d, \\"status\\": \\"%s\\", \\"x\\": %d, \\"candidates\\": %lld, \\"nodes\\": %lld, \\"chash\\": \\"%016llx\\"}' + NL + '",'
    ' idx++, o.status.c_str(), o.x, o.cand, o.nodes, o.chash); fflush(stdout); continue; }\n'
    '            printf(')
open(sys.argv[1], 'w', encoding='utf-8').write(src)
