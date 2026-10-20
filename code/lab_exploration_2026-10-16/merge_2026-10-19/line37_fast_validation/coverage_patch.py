# scratch copy of line37_fast.cpp with coverage counters for the rare code paths (diagnostic only)
import sys
s = open(sys.argv[1], encoding='utf-8').read()
NL = "\\" + "n"


def rep(a, b):
    global s
    assert a in s, a
    s = s.replace(a, b, 1)


rep('static inline int pc64(uint64_t a)', 'static long long C_degen = 0, C_np = 0, C_r1kept = 0, C_nf2 = 0, C_partex = 0, C_nob1 = 0, C_psd_degen_skip = 0, C_cut = 0;\n'
    'static inline int pc64(uint64_t a)')
rep('        if (piv < 1e-7 || piv7 < 1e-7) degenAt = n;', '        if (piv < 1e-7 || piv7 < 1e-7) { degenAt = n; C_degen++; }')
rep('    if (!ok || np > ccap[A]) return false;\n    // commit', '    if (!ok || np > ccap[A]) return false;\n    if (np > 0) C_np++;\n    // commit')
rep('        uint64_t ex = _mm512_cmpeq_epi8_mask(_mm512_permutexvar_epi8(sp, rcl), _mm512_set1_epi8(2));\n        m0 &= ~ex; m1 &= ~ex;',
    '        uint64_t ex = _mm512_cmpeq_epi8_mask(_mm512_permutexvar_epi8(sp, rcl), _mm512_set1_epi8(2));\n        C_partex += pc64((m0 | m1) & ex);\n        m0 &= ~ex; m1 &= ~ex;')
rep('        for (int i = 0; i < 5; i++) if (pc64(nbm[namesA[i]] & mb) > 1) { m1 ^= bit; break; }\n    }\n    *m1out = m1;',
    '        for (int i = 0; i < 5; i++) if (pc64(nbm[namesA[i]] & mb) > 1) { m1 ^= bit; C_nf2++; break; }\n    }\n    C_r1kept += pc64(m1);\n    *m1out = m1;')
rep('    if (REAL && degenAt < 0) {         // nasg >= 1 here', '    if (degenAt >= 0) C_psd_degen_skip++;\n    if (REAL && degenAt < 0) {         // nasg >= 1 here')
rep('    bool b1mode = (marg[B1] == 0 && Kx[B1] == 1);\n    if (b1mode) {', '    bool b1mode = (marg[B1] == 0 && Kx[B1] == 1);\n    if (depth == 0 && !b1mode) C_nob1++;\n    if (b1mode) {')
rep('    init_static(); init_static_tables();',
    '    init_static(); init_static_tables();\n'
    '    atexit([] { fprintf(stderr, "COV degen_events %lld forward_calls_with_degenerate_block %lld commits_with_partners %lld r1_kept %lld nf2_rejects %lld partner_exclusions %lld roots_without_b1mode %lld' + NL + '",'
    ' C_degen, C_psd_degen_skip, C_np, C_r1kept, C_nf2, C_partex, C_nob1); });')
open(sys.argv[2], 'w', encoding='utf-8').write(s)
