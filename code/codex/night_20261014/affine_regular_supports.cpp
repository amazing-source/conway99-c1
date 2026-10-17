// Exhaustive degree-four support generator, n <= 12.
// At each step vertices with the same neighborhood in the processed prefix
// are interchangeable. Select an initial segment from each such block.
// This removes duplicate branches only; no full isomorphism claim is made.
#include <array>
#include <bit>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

using Rows = std::array<unsigned, 12>;
int order;
std::uint64_t nodes = 0, leaves = 0, limit = 0;
bool complete = true;

bool valid(const Rows& rows) {
    for (int x = 0; x < order; ++x) {
        if (std::popcount(rows[x]) > 4) return false;
        for (int y = x + 1; y < order; ++y)
            if (std::popcount(rows[x] & rows[y]) >
                (((rows[x] >> y) & 1) ? 1 : 2)) return false;
    }
    return true;
}

void visit(const Rows& rows, int v);

void choices(const Rows& rows, int v, const std::vector<std::vector<int>>& groups,
             int group, int need, unsigned selected) {
    if (!complete) return;
    if (group == int(groups.size())) {
        if (need) return;
        Rows next = rows;
        next[v] |= selected;
        for (int x = v + 1; x < order; ++x)
            if ((selected >> x) & 1) next[x] |= 1u << v;
        if (valid(next)) visit(next, v + 1);
        return;
    }
    const auto& block = groups[group];
    int maximum = std::popcount(rows[block[0]]) < 4 ? int(block.size()) : 0;
    maximum = std::min(maximum, need);
    unsigned added = 0;
    for (int count = 0; count <= maximum; ++count) {
        choices(rows, v, groups, group + 1, need - count, selected | added);
        if (count < maximum) added |= 1u << block[count];
    }
}

void visit(const Rows& rows, int v) {
    if (limit && nodes >= limit) { complete = false; return; }
    ++nodes;
    if (v == order) {
        ++leaves;
        std::cout << "{\"rows\":[";
        for (int x = 0; x < order; ++x) {
            if (x) std::cout << ',';
            std::cout << rows[x];
        }
        std::cout << "]}\n";
        return;
    }
    int need = 4 - std::popcount(rows[v]);
    if (need < 0 || need > order - v - 1) return;
    // Future-future edges are unset, so a row itself is its prefix signature.
    std::vector<std::vector<int>> groups;
    for (int x = v + 1; x < order; ++x) {
        int block = 0;
        while (block < int(groups.size()) && rows[groups[block][0]] != rows[x]) ++block;
        if (block == int(groups.size())) groups.emplace_back();
        groups[block].push_back(x);
    }
    choices(rows, v, groups, 0, need, 0);
}

int main(int argc, char** argv) {
    order = argc > 1 ? std::atoi(argv[1]) : 12;
    limit = argc > 2 ? std::strtoull(argv[2], nullptr, 10) : 0;
    if (order < 5 || order > 12) return 2;
    visit(Rows{}, 0);
    std::cout << "{\"summary\":{\"order\":" << order << ",\"nodes\":" << nodes
              << ",\"leaves\":" << leaves << ",\"complete\":"
              << (complete ? "true" : "false") << "}}\n";
    return complete ? 0 : 3;
}
