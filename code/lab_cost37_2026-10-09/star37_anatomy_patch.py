"""Anatomy copy of star37d.c (scalar build only, integer conditions): where and why the star of a random ball dies.
Adds, without changing the search:
  NH[g]        : Green norm modulo 7 of every shadow that passes the combinatorial filters (g = 0 is kept as candidate);
  HV[d][w][v]  : for the member placed at depth d and every candidate of the next slot still alive after the d - 1
                 earlier members: weight class w (0 = no shared point, 1 = one shared point of demand 2, 2 = more or a
                 shared point of demand 1) and Green value v modulo 7 of the pair (v = 0: compatible as non-adjacent,
                 v = 1: compatible as adjacent, 2..6: incompatible). Independent conditions would give v uniform on
                 the seven residues at every depth;
  DMX[d]       : number of balls whose deepest consistent partial star has d members;  NLEV[d]: balls reaching depth d.
python anat.py star37d.c star37e.c ; gcc -O3 -march=native -DSCALAR -o star37e star37e.c"""
import sys
s = open(sys.argv[1], encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a, s.count(a))
    s = s.replace(a, b)

rep("static const double BND = 37.0 / 12;",
    "static const double BND = 37.0 / 12;\n"
    "static unsigned char rowv[65536][512]; static long long HV[11][3][7], NH[7], DMX[11], NLEV[11], PCNT[11][24];")

rep("        int z = tq[QB[p][k]] + tr[RB[p][k]] + cst, w = z >> 5, v = z & 31;",
    "        int z = tq[QB[p][k]] + tr[RB[p][k]] + cst, w = z >> 5, v = z & 31;\n"
    "        rowv[ridx[g][p]][k] = (unsigned char)((v % 7) | ((w > 2 ? 2 : w) << 3));")

rep("        unsigned nz1 = 0;",
    "        { int idx = ridx[memb[0]][b]; for (int k = 0; k < nsl[b]; k++) { unsigned char x = rowv[idx][k]; HV[1][x >> 3][x & 7]++; } }\n"
    "        unsigned nz1 = 0;")

rep("    int a = ptie[d - 1]; u64 news = c1m[d - 1] & cmask[memb[d - 1]] & D2;",
    "    int a = ptie[d - 1]; u64 news = c1m[d - 1] & cmask[memb[d - 1]] & D2;\n"
    "    { int idx = ridx[memb[d - 1]][b]; const bs_t *pa0 = &AL[d - 1][b];\n"
    "      for (int c = 0; c < 8; c++) { u64 m = pa0->w[c]; while (m) { int k = __builtin_ctzll(m); m &= m - 1; unsigned char x = rowv[idx][64 * c + k]; HV[d][x >> 3][x & 7]++; } } }")

rep("                if ((n0 + nq[q] + 2 * GQ1[va][q] + nr[r] + 2 * (GQ2[x1][r] + GQ2[x2][r]) + 2 * GQ2[va][r]) % 7) continue;\n"
    "                u64 m = (1ULL << U) | (1ULL << va) | (1ULL << x1) | (1ULL << x2) | (1ULL << y1) | (1ULL << y2);\n"
    "                if (!shadow_ok(m)) continue;",
    "                int gv = (n0 + nq[q] + 2 * GQ1[va][q] + nr[r] + 2 * (GQ2[x1][r] + GQ2[x2][r]) + 2 * GQ2[va][r]) % 7;\n"
    "                u64 m = (1ULL << U) | (1ULL << va) | (1ULL << x1) | (1ULL << x2) | (1ULL << y1) | (1ULL << y2);\n"
    "                if (!shadow_ok(m)) continue;\n"
    "                NH[gv]++; if (gv) continue;")

rep("        for (int p = 0; p < 10; p++) if (nsl[p] > maxslot) maxslot = nsl[p];",
    "        for (int p = 0; p < 10; p++) if (nsl[p] > maxslot) maxslot = nsl[p];\n"
    "        { int dm = 0; for (int d = 0; d <= 10; d++) if (cntd[d]) { dm = d; NLEV[d]++; } DMX[dm]++;\n"
    "          for (int d = 1; d <= 10; d++) { long long c = cntd[d]; int bin = 0; while (c > 0 && bin < 23) { c >>= 1; bin++; } PCNT[d][bin]++; } }")

rep(r'''    if (CHECK) printf("check: %lld mismatches''',
    r'''    { long long t = 0; for (int g = 0; g < 7; g++) t += NH[g];
      printf("Green norm mod 7 of the shadows passing the combinatorial filters (%.0f per ball):", (double)t / tested);
      for (int g = 0; g < 7; g++) printf(" %.4f", (double)NH[g] / t); printf("   (kept: residue 0)\n"); }
    printf("pair value mod 7 between the member placed at depth d and the candidates of the next slot still alive, by weight class\n");
    for (int d = 1; d <= 9; d++) for (int w = 0; w < 3; w++) { long long t = 0; for (int v = 0; v < 7; v++) t += HV[d][w][v]; if (!t) continue;
        printf("  depth %d weight %d: n = %-12lld", d, w, t); for (int v = 0; v < 7; v++) printf(" %.4f", (double)HV[d][w][v] / t); printf("\n"); }
    printf("balls by deepest consistent partial star:"); for (int d = 0; d <= 10; d++) if (DMX[d]) printf("  %d members: %lld", d, DMX[d]); printf("\n");
    printf("balls reaching depth d:"); for (int d = 1; d <= 10; d++) printf(" %lld", NLEV[d]); printf("\n");
    for (int d = 4; d <= 8; d++) { printf("  number of partial stars at depth %d, balls by size class (0, 1, 2-3, 4-7, ...):", d); for (int b = 0; b < 24; b++) printf(" %lld", PCNT[d][b]); printf("\n"); }
    if (CHECK) printf("check: %lld mismatches''')
open(sys.argv[2], "w", encoding="utf-8", newline="\n").write(s); print("anatomy copy written")
