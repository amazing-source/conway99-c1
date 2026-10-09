"""C1, lab session, 2026-10-09/10. star37f.c = star37d.c + exact options for the study of collective conflicts.

    python star37f_patch.py star37d.c star37f.c
    gcc -O3 -march=native -o star37f star37f.c            (and -DSCALAR for the plain C build)

Options (environment variables; with none of them the program is star37d):
  STAR37_SAT    saturation rule for the two members of a line through the star vertex U (valid at every rank):
                if f, g are adjacent far vertices and p is a near point of g that is not in the shadow of f, then p and
                f are non-adjacent with exactly two common neighbours, one of which is g; so p has at most ONE
                neighbour of G(T) in the shadow of f. An adjacent-compatible pair violating this, in either direction,
                is removed.
  STAR37_FC=n   forward checking with dynamic slot order: at every node the alive sets of ALL remaining slots are
                computed; a branch is cut when one of them is empty; the slot with the fewest alive candidates is
                expanded. n >= 2: also cut when a member that still needs its partner has no adjacent-compatible alive
                candidate left; n >= 3: also cut when a near point still to be covered is reachable by too few slots.
  STAR37_FCMAX=m  forward checking only at depths <= m (default 9); deeper, the first unused slot is taken lazily.
  STAR37_CORES  after the search, the minimal conflicting sets of slots of the ball: sets of slots with no consistent
                selection (pair conditions, no point covered too often) all of whose proper subsets have one.
  STAR37_PAT    joint distribution of the Green values of three candidates (all triples of the three smallest slots)
                and of four candidates (random quadruples of the four smallest slots).
  STAR37_GREEN  (scalar build only) pair conditions reduced to the Green value alone: value 0 or 1 modulo 7, no rule on
                shared points, on partners or on coverage. For the cores "of the bilinear form alone".
The reference count of check mode applies the saturation rule from its definition; with STAR37_FC the numbers of
partial stars depend on the dynamic order and are not compared (the verdict and, in plant mode, the number of complete
stars are)."""
import sys
s = open(sys.argv[1], encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)

rep("static const double BND = 37.0 / 12;",
    "static const double BND = 37.0 / 12;\n"
    "static int SATF, FCD, FCMAXD = 9, GREENONLY, KLIM = 10, STOPFIRST, found;      /* options of star37f, see star37f_patch.py */\n"
    "static unsigned usedm[11]; static long long nsatk, nfc[11], DMX[11], totn;")

rep("    if (v == 1 && shared == 0 && !bapex[i] && !bapex[j]) return 1;",
    "    if (v == 1 && shared == 0 && !bapex[i] && !bapex[j]) {\n"
    "        if (SATF) for (int k = 1; k < 6; k++)\n"
    "            if (__builtin_popcountll(amask[bmem[j][k]] & bmask[i]) > 1 || __builtin_popcountll(amask[bmem[i][k]] & bmask[j]) > 1) return -1;\n"
    "        return 1;\n"
    "    }")

rep("static long long cntd[11], nrows, nsteps, nrej; static int nsol;",
    "static long long cntd[11], nrows, nsteps, nrej; static int nsol;\n"
    "static u64 SATm[MAXC]; static bs_t PS[10][36];              /* points with two G-neighbours in a shadow; candidates of a slot by such point */")

rep("    memset(PT, 0, sizeof PT); memset(NAP, 0, sizeof NAP); memset(VAL, 0, sizeof VAL); memset(QB, 0, sizeof QB); memset(RB, 0, sizeof RB); memset(TJ, 0, sizeof TJ);",
    "    memset(PT, 0, sizeof PT); memset(NAP, 0, sizeof NAP); memset(VAL, 0, sizeof VAL); memset(QB, 0, sizeof QB); memset(RB, 0, sizeof RB); memset(TJ, 0, sizeof TJ);\n"
    "    if (SATF) memset(PS, 0, sizeof PS);")

rep("            u64 mm = cmask[g]; while (mm) { int w = __builtin_ctzll(mm); mm &= mm - 1; PT[p][w].w[k >> 6] |= 1ULL << (k & 63); }",
    "            u64 mm = cmask[g]; while (mm) { int w = __builtin_ctzll(mm); mm &= mm - 1; PT[p][w].w[k >> 6] |= 1ULL << (k & 63); }\n"
    "            if (SATF) { u64 sat = 0, once = 0, m2 = cmask[g]; while (m2) { u64 a = amask[__builtin_ctzll(m2)]; m2 &= m2 - 1; sat |= once & a; once |= a; }\n"
    "                SATm[g] = sat; while (sat) { int w = __builtin_ctzll(sat); sat &= sat - 1; PS[p][w].w[k >> 6] |= 1ULL << (k & 63); } }")

rep("        int m0 = (v == 0 || v == 7 || v == 14) && w <= 1, m1 = (v == 1 || v == 8 || v == 15) && w == 0 && nap && !cd[off[p] + k].ap;",
    "        int m0 = (v == 0 || v == 7 || v == 14) && w <= 1, m1 = (v == 1 || v == 8 || v == 15) && w == 0 && nap && !cd[off[p] + k].ap;\n"
    "        if (GREENONLY) { m0 = v % 7 == 0; m1 = v % 7 == 1; }")

rep("    if (PLANT && plantg[cpos[g]] == g) {              /* planted star: its members are declared compatible with one another */",
    "    if (SATF && nap) {                                /* saturation rule, both directions */\n"
    "        bs_t kill; memset(&kill, 0, sizeof kill);\n"
    "        u64 sm = SATm[g]; while (sm) { int w = __builtin_ctzll(sm); sm &= sm - 1; for (int c = 0; c < 8; c++) kill.w[c] |= PT[p][w].w[c]; }\n"
    "        u64 mm = cmask[g] & ~(1ULL << U); while (mm) { int w = __builtin_ctzll(mm); mm &= mm - 1; for (int c = 0; c < 8; c++) kill.w[c] |= PS[p][w].w[c]; }\n"
    "        for (int c = 0; c < 8; c++) { nsatk += __builtin_popcountll(R->r1.w[c] & kill.w[c]); R->r1.w[c] &= ~kill.w[c]; }\n"
    "    }\n"
    "    if (PLANT && plantg[cpos[g]] == g) {              /* planted star: its members are declared compatible with one another */")

rep("        if (a >= 0) al = pa->w[c] & R->r0.w[c] & ~Ra->r1.w[c];\n"
    "        else { al = pa->w[c] & (R->r0.w[c] | (R->r1.w[c] & ~ti)); ti |= R->r1.w[c]; }\n"
    "        u64 s2 = news; while (s2) { int w = __builtin_ctzll(s2); s2 &= s2 - 1; al &= ~PT[b][w].w[c]; }",
    "        if (GREENONLY) al = pa->w[c] & (R->r0.w[c] | R->r1.w[c]);\n"
    "        else {\n"
    "        if (a >= 0) al = pa->w[c] & R->r0.w[c] & ~Ra->r1.w[c];\n"
    "        else { al = pa->w[c] & (R->r0.w[c] | (R->r1.w[c] & ~ti)); ti |= R->r1.w[c]; }\n"
    "        u64 s2 = news; while (s2) { int w = __builtin_ctzll(s2); s2 &= s2 - 1; al &= ~PT[b][w].w[c]; }\n"
    "        }")

rep("    if (d == 10) {\n"
    "        if ((c1m[10] & D1) != D1 || (c2m[10] & D2) != D2) return;\n"
    "        for (int k = 0; k < 10; k++) if (!cd[memb[k]].ap && partner[k] < 0) return;\n"
    "        nsol++; return;\n"
    "    }\n"
    "    const int b = pord[d]; unsigned nz = getset(d, b);",
    "    if (d == KLIM) {\n"
    "        if (KLIM == 10 && !GREENONLY) {\n"
    "            if ((c1m[10] & D1) != D1 || (c2m[10] & D2) != D2) return;\n"
    "            for (int k = 0; k < 10; k++) if (!cd[memb[k]].ap && partner[k] < 0) return;\n"
    "        }\n"
    "        nsol++; found = 1; return;\n"
    "    }\n"
    "    int b; unsigned nz;\n"
    "    if (FCD && d > FCMAXD) {                          /* below the forward-checking depth: first unused slot, lazily */\n"
    "        b = 0; while ((usedm[d] >> b) & 1) b++;\n"
    "        nz = getset(d, b); pord[d] = b;\n"
    "    } else if (FCD) {                                 /* forward checking on every remaining slot, smallest alive set first */\n"
    "        int bc = 1 << 30; b = -1; nz = 0;\n"
    "        for (int s = 0; s < 10; s++) if (!((usedm[d] >> s) & 1)) {\n"
    "            unsigned z = getset(d, s); if (!z) { nfc[d]++; return; }\n"
    "            int c = 0; for (int q = 0; q < 8; q++) c += __builtin_popcountll(AL[d][s].w[q]);\n"
    "            if (c < bc) { bc = c; b = s; nz = z; }\n"
    "        }\n"
    "        if (FCD >= 2) for (int m = 0; m < d; m++) if (!cd[memb[m]].ap && partner[m] < 0) {\n"
    "            int ok = 0;\n"
    "            for (int s = 0; s < 10 && !ok; s++) if (!((usedm[d] >> s) & 1)) { const row_t *Rm = getrow(memb[m], s); for (int q = 0; q < 8; q++) if (Rm->r1.w[q] & AL[d][s].w[q]) { ok = 1; break; } }\n"
    "            if (!ok) { nfc[d]++; return; }\n"
    "        }\n"
    "        if (FCD >= 3) {\n"
    "            u64 need2 = D2 & ~c1m[d], nd = (D1 & ~c1m[d]) | (D2 & ~c2m[d]);\n"
    "            while (nd) { int w = __builtin_ctzll(nd); nd &= nd - 1; int cnt = 0, want = ((need2 >> w) & 1) ? 2 : 1;\n"
    "                for (int s = 0; s < 10 && cnt < want; s++) if (!((usedm[d] >> s) & 1)) for (int q = 0; q < 8; q++) if (PT[s][w].w[q] & AL[d][s].w[q]) { cnt++; break; }\n"
    "                if (cnt < want) { nfc[d]++; return; } }\n"
    "        }\n"
    "        pord[d] = b;\n"
    "    } else { b = pord[d]; nz = getset(d, b); }")

rep("            if ((ti->w[c] >> k) & 1) for (int m = 0; m < d; m++) if ((getrow(memb[m], b)->r1.w[c] >> k) & 1) { a = m; break; }",
    "            if (!GREENONLY && ((ti->w[c] >> k) & 1)) for (int m = 0; m < d; m++) if ((getrow(memb[m], b)->r1.w[c] >> k) & 1) { a = m; break; }")

rep("            LVm[d + 1] = 0;\n"
    "            dfs(d + 1);\n"
    "            if (a >= 0) partner[a] = -1;",
    "            LVm[d + 1] = 0; usedm[d + 1] = usedm[d] | (1u << b);\n"
    "            dfs(d + 1);\n"
    "            if (a >= 0) partner[a] = -1;\n"
    "            if (STOPFIRST && found) return;")

rep("        memb[0] = i; ptie[0] = -1; c1m[1] = cmask[i] & ub; c2m[1] = 0; LVm[1] = 0;",
    "        memb[0] = i; ptie[0] = -1; c1m[1] = cmask[i] & ub; c2m[1] = 0; LVm[1] = 0; usedm[1] = 1u;")

NEWFUN = r'''/* ---------- minimal conflicting sets of slots (STAR37_CORES) ---------- */
static long long CK[11], CKMIN[11], CPOS[10], CNT_CORE, CDIST[8], SDIST[8], CBALLS, CTESTS;
static int subset_feasible(const int *sl, int k) {    /* a consistent selection on the slots sl[0..k-1] (in this order)? */
    u64 ubs = ~(1ULL << U); int fsave = FCD; FCD = 0;
    KLIM = k; STOPFIRST = 1; found = 0;
    for (int x = 0; x < k; x++) pord[x] = sl[x];
    for (int x = 0; x < 10; x++) partner[x] = -1;
    for (int i = off[sl[0]]; i < off[sl[0] + 1] && !found; i++) {
        install(0, i, -1);
        memb[0] = i; ptie[0] = -1; c2m[1] = 0; c1m[1] = cmask[i] & ubs; LVm[1] = 0; usedm[1] = 1u << sl[0];
        dfs(1);
    }
    KLIM = 10; STOPFIRST = 0; FCD = fsave; CTESTS++;
    return found;
}
static void cores(void) {
    static unsigned core[1024]; int nc = 0, kmin = 0, dist[36], q[36], h = 0, tl = 0;
    for (int i = 0; i < 36; i++) dist[i] = -1;
    dist[U] = 0; q[tl++] = U;
    while (h < tl) { int x = q[h++]; for (int e = 0; e < 3; e++) { int y = nb[x][e]; if (dist[y] < 0) { dist[y] = dist[x] + 1; q[tl++] = y; } } }
    for (int p = 0; p < 10; p++) { int dd = dist[SL[ord[p]]]; if (dd > 7 || dd < 0) dd = 7; SDIST[dd]++; }
    for (int k = 2; k <= 10; k++)
        for (unsigned m = 0; m < 1024; m++) if (__builtin_popcount(m) == k) {
            int sub = 0; for (int c = 0; c < nc; c++) if ((core[c] & m) == core[c]) { sub = 1; break; }
            if (sub) continue;
            int sl[10], n = 0; for (int p = 0; p < 10; p++) if ((m >> p) & 1) sl[n++] = p;
            if (subset_feasible(sl, k)) continue;
            core[nc++] = m; CK[k]++; CNT_CORE++; if (!kmin) kmin = k;
            for (int p = 0; p < 10; p++) if ((m >> p) & 1) { CPOS[p]++; int dd = dist[SL[ord[p]]]; if (dd > 7 || dd < 0) dd = 7; CDIST[dd]++; }
        }
    CKMIN[kmin]++; CBALLS++;
}

/* ---------- joint distribution of the Green values of three and of four candidates (STAR37_PAT) ---------- */
static long long PT3[343], PT4[117649], PT3n, PT4n;
static void patterns(void) {
    static unsigned char *V[4][4]; static int hc[2048][36];
    int n[4], o[4], tot = off[4]; for (int a = 0; a < 4; a++) { n[a] = nsl[a]; o[a] = off[a]; }
    if (tot > 2048) return;
    for (int g = 0; g < tot; g++) for (int z = 0; z < 36; z++) { int t = 0; for (int k = 0; k < 6; k++) t += Gm[cpts[g][k]][z]; hc[g][z] = t; }
    for (int a = 0; a < 4; a++) for (int b = a + 1; b < 4; b++) {
        V[a][b] = realloc(V[a][b], (size_t)n[a] * n[b] + 1);
        for (int i = 0; i < n[a]; i++) for (int j = 0; j < n[b]; j++) {
            int g = o[a] + i, h = o[b] + j, t = S9 + 3 * cd[g].rsm + 3 * cd[h].rsm - 3 + 70;
            for (int k = 0; k < 6; k++) t += hc[g][cpts[h][k]];
            V[a][b][(size_t)i * n[b] + j] = (unsigned char)(t % 7);
        }
    }
    for (int i = 0; i < n[0]; i++) for (int j = 0; j < n[1]; j++) {
        int v01 = V[0][1][(size_t)i * n[1] + j]; const unsigned char *r02 = V[0][2] + (size_t)i * n[2], *r12 = V[1][2] + (size_t)j * n[2];
        for (int k = 0; k < n[2]; k++) PT3[v01 * 49 + r02[k] * 7 + r12[k]]++;
    }
    PT3n += (long long)n[0] * n[1] * n[2];
    for (int t = 0; t < 4000000; t++) {
        int i = rnd() % n[0], j = rnd() % n[1], k = rnd() % n[2], l = rnd() % n[3];
        int idx = V[0][1][(size_t)i * n[1] + j];
        idx = idx * 7 + V[0][2][(size_t)i * n[2] + k]; idx = idx * 7 + V[0][3][(size_t)i * n[3] + l];
        idx = idx * 7 + V[1][2][(size_t)j * n[2] + k]; idx = idx * 7 + V[1][3][(size_t)j * n[3] + l]; idx = idx * 7 + V[2][3][(size_t)k * n[3] + l];
        PT4[idx]++;
    }
    PT4n += 4000000;
}

static inline int satfree(int g, int h) {             /* the two shadows respect the saturation rule in both directions */
    u64 ubs = ~(1ULL << U), m = cmask[h] & ubs;
    while (m) { int w = __builtin_ctzll(m); m &= m - 1; if (__builtin_popcountll(amask[w] & cmask[g]) > 1) return 0; }
    m = cmask[g] & ubs;
    while (m) { int w = __builtin_ctzll(m); m &= m - 1; if (__builtin_popcountll(amask[w] & cmask[h]) > 1) return 0; }
    return 1;
}

'''
rep("/* positive control: a combinatorial star (one candidate per slot, exact coverage, two members sharing at most one",
    NEWFUN + "/* positive control: a combinatorial star (one candidate per slot, exact coverage, two members sharing at most one")

rep("    for (int j = i + 1; j < 10; j++) if (!((used >> j) & 1) && !cd[plantg[j]].ap && !(cmask[plantg[i]] & cmask[plantg[j]] & ub)) {",
    "    for (int j = i + 1; j < 10; j++) if (!((used >> j) & 1) && !cd[plantg[j]].ap && !(cmask[plantg[i]] & cmask[plantg[j]] & ub) && (!SATF || satfree(plantg[i], plantg[j]))) {")

rep('''    ALLOW3 = getenv("STAR37_NT") != NULL; long long with3 = 0, with3t = 0, nou = 0; if (ALLOW3) ALLOW4 = 1;''',
    '''    ALLOW3 = getenv("STAR37_NT") != NULL; long long with3 = 0, with3t = 0, nou = 0; if (ALLOW3) ALLOW4 = 1;
    SATF = getenv("STAR37_SAT") != NULL; FCD = getenv("STAR37_FC") ? atoi(getenv("STAR37_FC")) : 0; GREENONLY = getenv("STAR37_GREEN") != NULL;
    if (getenv("STAR37_FCMAX")) FCMAXD = atoi(getenv("STAR37_FCMAX"));
    int CORES = getenv("STAR37_CORES") != NULL, PAT = getenv("STAR37_PAT") != NULL;
#ifndef SCALAR
    if (GREENONLY) { fprintf(stderr, "STAR37_GREEN needs the scalar build (-DSCALAR)\\n"); return 1; }
#endif''')

rep("        for (int p = 0; p < 10; p++) if (nsl[p] > maxslot) maxslot = nsl[p];",
    "        for (int p = 0; p < 10; p++) if (nsl[p] > maxslot) maxslot = nsl[p];\n"
    "        { int dm = 0; for (int d = 0; d <= 10; d++) if (cntd[d]) dm = d; DMX[dm]++; for (int d = 1; d <= 10; d++) totn += cntd[d]; }")

rep("            for (int d = 0; d <= REFD; d++) if (refcnt[d] != cntd[d]) bad = 1;",
    "            if (!FCD) for (int d = 0; d <= REFD; d++) if (refcnt[d] != cntd[d]) bad = 1;")

rep("        }\n    }\n    double wall = now() - t00;",
    "        }\n        if (PAT) patterns();\n        if (CORES) cores();\n    }\n    double wall = now() - t00;")

rep(r'''    if (CHECK) printf("check: %lld mismatches''',
    r'''    printf("options: saturation rule %s (adjacent-compatible pairs removed in the rows computed: %.1f per ball), forward checking level %d%s\n", SATF ? "ON" : "off", (double)nsatk / tested, FCD, GREENONLY ? ", GREEN VALUES ONLY" : "");
    printf("nodes per ball %.1f; balls by deepest consistent partial star:", (double)totn / tested); for (int d = 0; d <= 10; d++) if (DMX[d]) printf("  %d: %lld", d, DMX[d]); printf("\n");
    if (FCD) { printf("branches cut by forward checking per ball, by depth:"); for (int d = 1; d <= 9; d++) printf(" %.1f", (double)nfc[d] / tested); printf("\n"); }
    if (PAT) {
        long long e3 = 0, mn3 = 1LL << 60, mx3 = 0, e4 = 0, mn4 = 1LL << 60, mx4 = 0;
        for (int i = 0; i < 343; i++) { if (!PT3[i]) e3++; if (PT3[i] < mn3) mn3 = PT3[i]; if (PT3[i] > mx3) mx3 = PT3[i]; }
        for (int i = 0; i < 117649; i++) { if (!PT4[i]) e4++; if (PT4[i] < mn4) mn4 = PT4[i]; if (PT4[i] > mx4) mx4 = PT4[i]; }
        printf("Green values of three candidates (the three smallest slots, all %lld triples): 343 patterns, %lld never realised, smallest / mean / largest count %lld / %.0f / %lld\n", PT3n, e3, mn3, (double)PT3n / 343, mx3);
        printf("Green values of four candidates (the four smallest slots, %lld random quadruples): 117649 patterns, %lld never realised, smallest / mean / largest count %lld / %.0f / %lld\n", PT4n, e4, mn4, (double)PT4n / 117649, mx4);
    }
    if (CORES && CBALLS) {
        printf("minimal conflicting sets of slots: %lld balls, %.1f sets per ball, %.0f feasibility tests per ball\n", CBALLS, (double)CNT_CORE / CBALLS, (double)CTESTS / CBALLS);
        printf("  sets per ball by size:"); for (int k = 2; k <= 10; k++) if (CK[k]) printf("  %d: %.2f", k, (double)CK[k] / CBALLS); printf("\n");
        printf("  balls by size of their smallest conflicting set:"); for (int k = 2; k <= 10; k++) if (CKMIN[k]) printf("  %d: %lld", k, CKMIN[k]); printf("\n");
        { long long t = 0; for (int p = 0; p < 10; p++) t += CPOS[p]; printf("  share of each slot in these sets, by rank (0 = fewest candidates):"); for (int p = 0; p < 10; p++) printf(" %.3f", (double)CPOS[p] / t); printf("\n"); }
        { long long ta = 0, tc = 0; for (int x = 0; x < 8; x++) { ta += SDIST[x]; tc += CDIST[x]; }
          printf("  slot points by distance from U in G(T), share among all slots / among the slots of these sets:"); for (int x = 2; x < 8; x++) if (SDIST[x]) printf("  d=%d: %.3f / %.3f", x, (double)SDIST[x] / ta, (double)CDIST[x] / tc); printf("\n"); }
    }
    if (CHECK) printf("check: %lld mismatches''')

rep("/* C1, lab session, 2026-10-09. Rank-37 star test for connected, prism-free, torsion-free line balls: fast version.",
    "/* star37f.c: generated from star37d.c by star37f_patch.py (options STAR37_SAT, STAR37_FC, STAR37_CORES, STAR37_PAT,\n"
    "   STAR37_GREEN: see that file). Without these options the program is star37d.\n"
    "   C1, lab session, 2026-10-09. Rank-37 star test for connected, prism-free, torsion-free line balls: fast version.")
open(sys.argv[2], "w", encoding="utf-8", newline="\n").write(s); print("star37f.c written")
