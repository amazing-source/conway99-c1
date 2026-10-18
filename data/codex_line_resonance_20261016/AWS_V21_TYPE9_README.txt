Tuned type9 continuation, runtime 7da4d547c46f250d1e20e69a6f71e2174a2b68c4.
50 tasks,356 codes,12 Grams. Launch nothing automatically.
The reserved local task t9_g193_r2_10 supplies the first8 codes: retain
Codex's reports when merging the full cover.

Compared with v2:1 presolve iteration, exact binary propagation before
large rotated tables, and proven residual coordinate/sign bounds.
The runtime archive includes the branch-union helper and its dependencies.
All code-cover hashes, frames and known proofs are preserved.

Keep one solver worker per assigned CPU. Measured v2 Windows peak was
5.5GiB; start conservatively, e.g.64 workers on512GiB, and measure Linux RSS.
The per-task external timeout is7200s. Per-code nominal CPU budget180s.
Missing or UNKNOWN cases are still open; only complete INFEASIBLE unions
close a Gram. This is a better encoding, not a guarantee of completion.

New options for Gram products, eigen equations and frozen Gram row profiles
are included in source but are NOT enabled in these tasks.

RESERVED LOCAL RANGE COMPLETED:all8 new codes are now INFEASIBLE.
Their proofs, plus the two prior ones, are supplied in
root_component_signature_aws_v21_local_9_193_r2_10.json.
Keep this file with the50 task outputs. A union can then be made with:
python -I code/codex/root_component_merge_branches.py data/codex_line_resonance_20261016 --glob "root_component_signature_aws_v21_*.json" --output data/codex_line_resonance_20261016/root_component_signature_union_aws_v21.json
Only whole-case INFEASIBLE results exclude a Gram.
