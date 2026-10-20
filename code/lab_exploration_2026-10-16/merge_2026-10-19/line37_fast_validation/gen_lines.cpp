// gen_lines <count> <seed> [skip]: the bijection triples of "line37 rand <count> <seed>", in the same order (same
// mt19937_64 + std::shuffle as line37.cpp's main), one line of 36 integers (s01 s12 s20) per sample.
#include <cstdio>
#include <cstdlib>
#include <random>
#include <algorithm>
using namespace std;
int main(int argc, char** argv) {
    long long count = atoll(argv[1]); unsigned long long seed = strtoull(argv[2], 0, 10);
    long long skip = argc > 3 ? atoll(argv[3]) : 0;
    mt19937_64 rng(seed);
    int s01[12], s12[12], s20[12];
    for (long long it = 0; it < count; it++) {
        for (int* s : {s01, s12, s20}) { for (int i = 0; i < 12; i++) s[i] = i; shuffle(s, s + 12, rng); }
        if (it < skip) continue;
        for (int* s : {s01, s12, s20}) for (int i = 0; i < 12; i++) printf("%d ", s[i]);
        printf("\n");
    }
    return 0;
}
