// Exact exhaustive induced-edge histogram for nine-subsets of a <=63 vertex
// graph. Used here only on the 39-vertex four-root edge graph.
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>

std::array<std::uint64_t, 63> neighbors{};
std::array<std::uint64_t, 37> histogram{};
std::array<std::uint64_t, 37> witness{};
int order = 0;

void visit(int start, int left, std::uint64_t selected, int edges) {
    if (left == 1) {
        for (int v = start; v < order; ++v) {
            int count = edges + std::popcount(selected & neighbors[v]);
            ++histogram[count];
            witness[count] = selected | (std::uint64_t(1) << v);
        }
        return;
    }
    for (int v = start; v <= order-left; ++v)
        visit(v+1, left-1, selected | (std::uint64_t(1) << v),
              edges + std::popcount(selected & neighbors[v]));
}

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    std::ifstream input(argv[1]);
    int size, x, y;
    if (!(input >> order >> size) || order < 9 || order > 63) return 2;
    for (int k = 0; k < size; ++k) {
        if (!(input >> x >> y) || x < 0 || y < 0 || x >= order || y >= order || x == y)
            return 2;
        if ((neighbors[x] >> y) & 1) return 2;
        neighbors[x] |= std::uint64_t(1) << y;
        neighbors[y] |= std::uint64_t(1) << x;
    }
    visit(0, 9, 0, 0);
    std::cout << "{\"order\":" << order << ",\"subset_size\":9,\"histogram\":{";
    bool comma = false;
    for (int e = 0; e <= 36; ++e) if (histogram[e]) {
        if (comma) std::cout << ',';
        comma = true;
        std::cout << '"' << e << "\":" << histogram[e];
    }
    std::cout << "},\"dense_witnesses\":{";
    comma = false;
    for (int e = 17; e <= 36; ++e) if (histogram[e]) {
        if (comma) std::cout << ',';
        comma = true;
        std::cout << '"' << e << "\":[";
        bool inner = false;
        for (int v = 0; v < order; ++v) if ((witness[e] >> v) & 1) {
            if (inner) std::cout << ',';
            inner = true;
            std::cout << v;
        }
        std::cout << ']';
    }
    std::cout << "}}\n";
}
