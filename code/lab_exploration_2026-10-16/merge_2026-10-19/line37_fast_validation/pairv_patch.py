# Adds a mode "pairv <lines.txt> <npairs>" to a copy of line37.cpp (kind=ref) or line37_fast.cpp (kind=fast): after each
# tested line, R = Rval(A, B) and h = hval(A, B, R) for npairs pseudo-random pairs of candidates of distinct far vertices
# (any orientation, compatible or not; the same pairs in both programs, since the candidate lists are identical), and
# prints one line per line: count of pairs and a hash of (indices, R, bits of h).  Diagnostic only.
import sys
kind, src_path, dst_path = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(src_path, encoding='utf-8').read()
NL = "\\" + "n"
if kind == "ref":
    ncand = "(int)V[va].cand.size()"
    nvar = "NV"
    compute = ("int R = Rval(va, ca, vb, cb); double h = hval(va, ca, vb, cb, R);")
else:
    ncand = "ncv[va]"
    nvar = "NV"
    compute = ("int gA = wbase[va] + ca, gB = wbase[vb] + cb; atab(gA); int R = Rval_f(gA, gB); double h = hval_f(gA, gB, R);")
mode = (
    '    if (mode == "pairv") {\n'
    '        FILE* f = fopen(argv[2], "r"); long long np = atoll(argv[3]); limit_s = 600;\n'
    '        int s[36], idx = 0;\n'
    '        while (true) {\n'
    '            bool okr = true;\n'
    '            for (int k = 0; k < 36; k++) if (fscanf(f, "%d", &s[k]) != 1) { okr = false; break; }\n'
    '            if (!okr) break;\n'
    '            Outcome o = test_line(s, s + 12, s + 24);\n'
    '            unsigned long long hh = 1469598103934665603ULL, r = 88172645463325252ULL ^ (unsigned long long)idx; long long done = 0, r1 = 0;\n'
    '            if (o.status == "UNSAT" || o.status == "SAT" || o.status == "TIMEOUT") {\n'
    '                for (long long t = 0; t < np; t++) {\n'
    '                    r ^= r << 13; r ^= r >> 7; r ^= r << 17; int va = (int)(r % ' + nvar + ');\n'
    '                    r ^= r << 13; r ^= r >> 7; r ^= r << 17; int vb = (int)(r % ' + nvar + ');\n'
    '                    r ^= r << 13; r ^= r >> 7; r ^= r << 17; unsigned long long ra = r;\n'
    '                    r ^= r << 13; r ^= r >> 7; r ^= r << 17; unsigned long long rb = r;\n'
    '                    if (va == vb) continue;\n'
    '                    int na = ' + ncand + ', nb = ' + ncand.replace('va', 'vb') + ';\n'
    '                    if (na == 0 || nb == 0) continue;\n'
    '                    int ca = (int)(ra % (unsigned long long)na), cb = (int)(rb % (unsigned long long)nb);\n'
    '                    ' + compute + '\n'
    '                    unsigned long long hb; memcpy(&hb, &h, 8);\n'
    '                    unsigned long long vals[6] = {(unsigned long long)va, (unsigned long long)ca, (unsigned long long)vb, (unsigned long long)cb, (unsigned long long)R, hb};\n'
    '                    for (int k = 0; k < 6; k++) { hh ^= vals[k]; hh *= 1099511628211ULL; }\n'
    '                    done++; r1 += (R <= 1);\n'
    '                }\n'
    '            }\n'
    '            printf("{\\"line\\": %d, \\"status\\": \\"%s\\", \\"pairs\\": %lld, \\"R01\\": %lld, \\"phash\\": \\"%016llx\\"}' + NL + '", idx++, o.status.c_str(), done, r1, hh);\n'
    '        }\n'
    '        return 0;\n'
    '    }\n')
anchor = '    if (mode == "file"'
assert anchor in s
s = s.replace(anchor, mode + anchor, 1)
open(dst_path, 'w', encoding='utf-8').write(s)
