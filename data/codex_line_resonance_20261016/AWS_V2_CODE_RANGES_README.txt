AWS v2: complete canonical code ranges, prepared 18 October 2026.

Runtime commit:10c2e827f37400e03621565943ff7c327e4a883d.
No instance is launched by these files.

909 remaining Gram cases:449 type7,12 type9,448 type19.
84637 codes still lack a proof, after reusing21890 existing code proofs.
10978 tasks of at most8 new codes each, with the FULL code cover retained.
Task counts:51 type9,4367 type19,6560 type7.
The type9-only files are a small first campaign:364 codes,51 tasks.

Each task pins the exact complete code-list hash, uses one solver worker,
and inherits proofs from its immutable seed. All-colour E3 removes whole
orbits; every runtime recomputes and checks the canonical cover.
The first-component catalogues preserve the same permutation/matching indices.

Per new code:5CPU-second weak prefilter, then the stronger model within a
nominal180CPU seconds. The stronger model has full99-coordinate residuals,
component relations, up to6 new cross triangles,2 new star triangles, and
the frozen earlier exclusion frontier at neighbouring roots IF their
prism sum is<=51. No budget is imposed above51.

There is no per-Gram900CPU ceiling. External wall timeout remains7200s per
task. CPU stop_search can overshoot during solver phases. Nominal budgets
are not hard runtime bounds and never guarantee exclusions. Full nominal
solver allocation is4231.85 CPU hours; most easy branches should finish
earlier, but the new long-run distribution is not yet measured.

For deployment, use code_sha256_lf and input_sha256_lf from the metadata.
The metadata includes909 seed files, the complete Gram/template cover,
the E3 tables, and the immutable frontier. Keep paths relative to repo root.
Do not copy local cpu_guard budget/stop/log files. Bind each worker to its
own allowed CPU with taskset. Package versions are in the requirements file.
Select parallelism from measured RAM per worker, retaining system headroom.

Merge reports using root_component_merge_branches.py; only complete covers
with every code INFEASIBLE exclude a Gram. Missing, timed-out and UNKNOWN
codes remain open. The pointwise union can mix ranges, never incompatible
frames or code catalogues. Sources and hashes are retained.

Local pilot reservation:Codex next runs t9_g193_r2_10. Omit this task from
a concurrent cloud start until Codex reports its result.
