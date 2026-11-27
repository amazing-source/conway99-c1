# Local repository handoff

No fetch, push, checkout, merge or commit performed. Raw status and branch history are in repositories.json. Preserve dirty files before consolidation.

## C:\Users\bfhdh\Desktop\Recherche_Conway\c1-asymmetry-audit

Remotes:
```
origin	https://github.com/amazing-source/conway99-c1.git (fetch) [blob:none]
origin	https://github.com/amazing-source/conway99-c1.git (push)
```

Branches:
```
claude/v7-simultaneous                              24dae2b8 [origin/claude/v7-simultaneous: behind 48] papers/rank7: cite Brouwer-van Eijl for the primes not dividing r-s
  codex/asymmetry-audit-20261012                      d9bc91ac Express fixed-sign S3 lifting exactly by ternary linear and quadratic equations
+ codex/c1-arithmetic-audit                           9ccfcefa (C:/Users/bfhdh/Desktop/Recherche_Conway/c1-codex) Record note260 publication and stronger-stage handoff
* codex/coheawood-hoffman-20261012                    538614f5 Record clean local checkpoint after template 599 closure
+ codex/norm16-far-forest                             5100eacf (C:/Users/bfhdh/Desktop/Recherche_Conway/c1-norm16-export) Add omitted-double P4 reduction and a PSD boundary survivor
+ codex/p3-n25-register                               80fc4070 (C:/Users/bfhdh/Desktop/Recherche_Conway/c1-p3-export) Share explicit P3/N25 support registers and encoding for the integer design search
+ main                                                f5199fea (C:/Users/bfhdh/Desktop/Recherche_Conway/c1-main-codex) Exclude low-norm mixed alpha branches and save paused research checkpoint
  remotes/origin/astra/bvls-boundary-release-20261011 5ca5e5de Coordination Astra: reconstruction de bord BVLS après Paley, sans dupliquer les revêtements actifs
  remotes/origin/claude/v7-simultaneous               f2b6454b dossiers_externes: version the external ChatGPT dossiers (Paley 25, BvLS, Hoffman alpha=22, K7 partial, CODE7) and the C3 proof PDF
  remotes/origin/codex/asymmetry-audit-20261012       d9bc91ac Express fixed-sign S3 lifting exactly by ternary linear and quadratic equations
  remotes/origin/codex/c1-arithmetic-audit            19ec3164 Record completed 48 main sweep and clean torsion-four closure reported by peers
  remotes/origin/codex/norm16-far-forest              5100eacf Add omitted-double P4 reduction and a PSD boundary survivor
  remotes/origin/codex/p3-n25-register                80fc4070 Share explicit P3/N25 support registers and encoding for the integer design search
  remotes/origin/lab/biplane243-2026-10-07            d3ddd3f2 lab: biplane configuration of norm 22 absent from both known srg(243,22,1,2)
  remotes/origin/lab/theta-lp-2026-10-08              491ea978 Lab: audit of claude/v7-simultaneous - comparison with Codex's independent audit
  remotes/origin/main                                 0a4cdd8f c3 ledger 537 -> 435 open with the night AWS runs (c3l2, c3p5, partial P4E, z_joint); P3 remainder launched on Spot
```

Status (first80 lines; full in JSON):
```
M code/codex/coheawood_completion.py
?? code/codex/analyze_solver_calibration.py
?? code/codex/coheawood_joint_design.py
?? code/codex/coheawood_sat.py
?? code/codex/root_component_bundle_microscope.py
?? code/codex/root_component_corner_moment_probe.py
?? code/codex/solver_telemetry.py
?? data/codex_asymmetry_synthesis_20261014/literature/kaski_ostergard_2004_sts19.txt
?? data/codex_asymmetry_synthesis_20261014/literature_expansion/babai_automorphism_handbook.txt
?? data/codex_asymmetry_synthesis_20261014/literature_expansion/brouwer_ihringer_kantor_4vertex.txt
?? data/codex_asymmetry_synthesis_20261014/literature_expansion/brouwer_vanmaldeghem_srg.pdf
?? data/codex_asymmetry_synthesis_20261014/literature_expansion/brouwer_vanmaldeghem_srg.txt
?? data/codex_asymmetry_synthesis_20261014/literature_expansion/coolsaet_degraer_spence_2006_45.txt
?? data/codex_asymmetry_synthesis_20261014/literature_expansion/haemers_spence_2001_64.txt
?? data/codex_asymmetry_synthesis_20261014/literature_expansion/maksimovic_rukavina_2022_twographs.txt
?? data/codex_asymmetry_synthesis_20261014/literature_expansion/spence_64_18_2_6.txt
?? data/codex_c3_microscope_20261018/cover_04491.json.gz
?? data/codex_c3_microscope_20261018/cover_06947.json.gz
?? data/codex_c3_microscope_20261018/cover_07320.json.gz
?? data/codex_c3_microscope_20261018/cover_07377.json.gz
?? data/codex_c3_microscope_20261018/cover_07470.json.gz
?? data/codex_c3_microscope_20261018/cover_07520.json.gz
?? data/codex_c3_microscope_20261018/cover_08650.json.gz
?? data/codex_c3_microscope_20261018/template_04192_hard_moment_bounds.json
?? data/codex_c3_microscope_20261018/template_05128_corner_cover.json
?? data/codex_c3_microscope_20261018/template_05128_corner_cover.log
?? data/codex_c3_microscope_20261018/template_05128_corner_cover_v2.json
?? data/codex_c3_microscope_20261018/template_05128_corner_cover_v2.log
?? data/codex_c3_microscope_20261018/template_05128_corner_moments.json
?? data/codex_c3_microscope_20261018/template_05128_corner_moments.log
?? data/codex_c3_microscope_20261018/template_05128_gram_cover.json
?? data/codex_c3_microscope_20261018/template_05128_kernel_profile.json
?? data/codex_c3_pilot_20261018/cpu_guard.budget.json
?? data/codex_c3_pilot_20261018/cpu_guard.budget.json.previous
?? data/codex_c3_pilot_20261018/cpu_guard.err
?? data/codex_c3_pilot_20261018/cpu_guard.log
?? data/codex_c3_pilot_20261018/cpu_guard.stop
?? data/codex_c3_pilot_20261018/g1_0_cover_pilot.log
?? data/codex_c3_pilot_20261018/g1_0_matching0_pilot.log
?? data/codex_c3_pilot_20261018/g1_1_cover_pilot.log
?? data/codex_c3_pilot_20261018/g1_2_cover_pilot.log
?? data/codex_c3_pilot_20261018/g2_0_cover_pilot.log
?? data/codex_c3_pilot_20261018/g2_11_cover_pilot.log
?? data/codex_c3_pilot_20261018/g2_15_cover_pilot.log
?? data/codex_c3_pilot_20261018/g2_3_cover_pilot.log
?? data/codex_c3_pilot_20261018/g2_5_cover_pilot.log
?? data/codex_coheawood/full.cnf
?? data/codex_coheawood/full.meta.json
?? data/codex_coheawood/full_marginals.cnf
?? data/codex_coheawood/full_marginals.meta.json
?? data/codex_coheawood/full_sat.drat
?? data/codex_coheawood/full_sat.err
?? data/codex_coheawood/full_sat.log
?? data/codex_coheawood/full_sat.solution
?? data/codex_coheawood/global_8workers_long.err
?? data/codex_coheawood/global_8workers_long.json
?? data/codex_coheawood/global_8workers_long.log
?? data/codex_coheawood/global_no_max_lp_8w.err
?? data/codex_coheawood/global_no_max_lp_8w.json
?? data/codex_coheawood/global_no_max_lp_8w.log
?? data/codex_coheawood/global_no_max_lp_8w.run.json
?? data/codex_coheawood/joint_k7_both.err
?? data/codex_coheawood/joint_k7_both.json
?? data/codex_coheawood/joint_k7_both.log
?? data/codex_coheawood/telemetry/
?? data/codex_domain_recovery_20261018/c4_19_all_variable_base.json
?? data/codex_domain_recovery_20261018/c4_19_all_variable_base.log
?? data/codex_domain_recovery_20261018/c4_19_factored_build.log
?? data/codex_domain_recovery_20261018/c4_19_star6_m4_certain_motifs.log
?? data/codex_domain_recovery_20261018/c4_19_star6_m4_native.cnf
?? data/codex_domain_recovery_20261018/c4_19_star6_m4_native.drat
?? data/codex_domain_recovery_20261018/c4_19_star6_m4_native.solver.log
?? data/codex_domain_recovery_20261018/c4_19_star6_m4_native_griddegree.cnf
?? data/codex_domain_recovery_20261018/c4_19_star6_m4_native_griddegree.drat
?? data/codex_domain_recovery_20261018/c4_19_star6_m4_native_griddegree.solver.log
?? data/codex_domain_recovery_20261018/c4_19_star6_m4_native_upper_table.cnf
?? data/codex_domain_recovery_20261018/c4_19_star6_m4_native_upper_table.drat
?? data/codex_domain_recovery_20261018/c4_19_star6_m4_native_upper_table.solver.log
?? data/codex_domain_recovery_20261018/c4_19_star6_m4_native_weighted.cnf
?? data/codex_domain_recovery_20261018/c4_19_star6_m4_native_weighted.drat
```

## C:\Users\bfhdh\Desktop\Recherche_Conway\c1-codex

Remotes:
```
origin	https://github.com/amazing-source/conway99-c1.git (fetch) [blob:none]
origin	https://github.com/amazing-source/conway99-c1.git (push)
```

Branches:
```
claude/v7-simultaneous                              24dae2b8 [origin/claude/v7-simultaneous: behind 48] papers/rank7: cite Brouwer-van Eijl for the primes not dividing r-s
  codex/asymmetry-audit-20261012                      d9bc91ac Express fixed-sign S3 lifting exactly by ternary linear and quadratic equations
* codex/c1-arithmetic-audit                           9ccfcefa Record note260 publication and stronger-stage handoff
+ codex/coheawood-hoffman-20261012                    538614f5 (C:/Users/bfhdh/Desktop/Recherche_Conway/c1-asymmetry-audit) Record clean local checkpoint after template 599 closure
+ codex/norm16-far-forest                             5100eacf (C:/Users/bfhdh/Desktop/Recherche_Conway/c1-norm16-export) Add omitted-double P4 reduction and a PSD boundary survivor
+ codex/p3-n25-register                               80fc4070 (C:/Users/bfhdh/Desktop/Recherche_Conway/c1-p3-export) Share explicit P3/N25 support registers and encoding for the integer design search
+ main                                                f5199fea (C:/Users/bfhdh/Desktop/Recherche_Conway/c1-main-codex) Exclude low-norm mixed alpha branches and save paused research checkpoint
  remotes/origin/astra/bvls-boundary-release-20261011 5ca5e5de Coordination Astra: reconstruction de bord BVLS après Paley, sans dupliquer les revêtements actifs
  remotes/origin/claude/v7-simultaneous               f2b6454b dossiers_externes: version the external ChatGPT dossiers (Paley 25, BvLS, Hoffman alpha=22, K7 partial, CODE7) and the C3 proof PDF
  remotes/origin/codex/asymmetry-audit-20261012       d9bc91ac Express fixed-sign S3 lifting exactly by ternary linear and quadratic equations
  remotes/origin/codex/c1-arithmetic-audit            19ec3164 Record completed 48 main sweep and clean torsion-four closure reported by peers
  remotes/origin/codex/norm16-far-forest              5100eacf Add omitted-double P4 reduction and a PSD boundary survivor
  remotes/origin/codex/p3-n25-register                80fc4070 Share explicit P3/N25 support registers and encoding for the integer design search
  remotes/origin/lab/biplane243-2026-10-07            d3ddd3f2 lab: biplane configuration of norm 22 absent from both known srg(243,22,1,2)
  remotes/origin/lab/theta-lp-2026-10-08              491ea978 Lab: audit of claude/v7-simultaneous - comparison with Codex's independent audit
  remotes/origin/main                                 0a4cdd8f c3 ledger 537 -> 435 open with the night AWS runs (c3l2, c3p5, partial P4E, z_joint); P3 remainder launched on Spot
```

Status (first80 lines; full in JSON):
```
M AGENTS.md
 M RECHERCHE_ACTIVE_C1.md
?? code/codex/norm16_dz_catalogue.exe
?? code/codex/norm16_edge_catalogue.exe
?? data/codex_norm16_dz_five_types.instance.txt
?? data/codex_norm16_dz_schur_survivors_0_0_2.txt
?? data/codex_norm16_dz_spectral_case0_orbit0.instance.txt
?? data/codex_norm16_dz_spectral_case0_orbit0.schur.txt
?? data/codex_norm16_edge_catalogue_0_3/
?? data/codex_norm16_edge_catalogue_0_4/
?? data/codex_norm16_edge_catalogue_0_4_refined/instance.txt
?? data/codex_norm16_edge_catalogue_0_4_refined/rows.txt
?? data/codex_norm16_edge_catalogue_0_4_refined/schur.txt
?? data/codex_norm16_edge_endpoints.json
?? data/codex_norm16_edge_first/
?? data/codex_norm16_even_core_full/instance.txt
?? data/codex_norm16_even_core_full/rows.txt
?? data/codex_norm16_even_core_full/schur.txt
?? data/codex_norm16_even_core_full/supports.jsonl
?? data/codex_norm16_even_core_other_probe/
?? data/codex_norm16_even_core_probe/
?? data/codex_norm16_independent_catalogue/instance.txt
?? data/codex_norm16_independent_catalogue/rows.txt
?? data/codex_norm16_independent_catalogue/schur.txt
?? data/codex_norm16_independent_catalogue/supports.jsonl
?? data/codex_norm16_independent_counts/instance.txt
?? data/codex_norm16_independent_counts/schur.txt
?? data/codex_norm16_independent_first/instance.txt
?? data/codex_norm16_independent_first/rows.txt
?? data/codex_norm16_independent_first/schur.txt
?? data/codex_norm16_independent_first/supports.jsonl
?? data/codex_norm16_p4_c1_first_boundary.json
?? data/codex_norm16_tight_cut_first/instance.txt
?? data/codex_norm16_tight_cut_first/rows.txt
?? data/codex_norm16_tight_cut_first/schur.txt
?? data/codex_norm16_tight_cut_first/supports.jsonl
```

## C:\Users\bfhdh\Desktop\Recherche_Conway\c1-main-codex

Remotes:
```
origin	https://github.com/amazing-source/conway99-c1.git (fetch) [blob:none]
origin	https://github.com/amazing-source/conway99-c1.git (push)
```

Branches:
```
claude/v7-simultaneous                              24dae2b8 [origin/claude/v7-simultaneous: behind 48] papers/rank7: cite Brouwer-van Eijl for the primes not dividing r-s
  codex/asymmetry-audit-20261012                      d9bc91ac Express fixed-sign S3 lifting exactly by ternary linear and quadratic equations
+ codex/c1-arithmetic-audit                           9ccfcefa (C:/Users/bfhdh/Desktop/Recherche_Conway/c1-codex) Record note260 publication and stronger-stage handoff
+ codex/coheawood-hoffman-20261012                    538614f5 (C:/Users/bfhdh/Desktop/Recherche_Conway/c1-asymmetry-audit) Record clean local checkpoint after template 599 closure
+ codex/norm16-far-forest                             5100eacf (C:/Users/bfhdh/Desktop/Recherche_Conway/c1-norm16-export) Add omitted-double P4 reduction and a PSD boundary survivor
+ codex/p3-n25-register                               80fc4070 (C:/Users/bfhdh/Desktop/Recherche_Conway/c1-p3-export) Share explicit P3/N25 support registers and encoding for the integer design search
* main                                                f5199fea Exclude low-norm mixed alpha branches and save paused research checkpoint
  remotes/origin/astra/bvls-boundary-release-20261011 5ca5e5de Coordination Astra: reconstruction de bord BVLS après Paley, sans dupliquer les revêtements actifs
  remotes/origin/claude/v7-simultaneous               f2b6454b dossiers_externes: version the external ChatGPT dossiers (Paley 25, BvLS, Hoffman alpha=22, K7 partial, CODE7) and the C3 proof PDF
  remotes/origin/codex/asymmetry-audit-20261012       d9bc91ac Express fixed-sign S3 lifting exactly by ternary linear and quadratic equations
  remotes/origin/codex/c1-arithmetic-audit            19ec3164 Record completed 48 main sweep and clean torsion-four closure reported by peers
  remotes/origin/codex/norm16-far-forest              5100eacf Add omitted-double P4 reduction and a PSD boundary survivor
  remotes/origin/codex/p3-n25-register                80fc4070 Share explicit P3/N25 support registers and encoding for the integer design search
  remotes/origin/lab/biplane243-2026-10-07            d3ddd3f2 lab: biplane configuration of norm 22 absent from both known srg(243,22,1,2)
  remotes/origin/lab/theta-lp-2026-10-08              491ea978 Lab: audit of claude/v7-simultaneous - comparison with Codex's independent audit
  remotes/origin/main                                 0a4cdd8f c3 ledger 537 -> 435 open with the night AWS runs (c3l2, c3p5, partial P4E, z_joint); P3 remainder launched on Spot
```

Status (first80 lines; full in JSON):
```
M code/codex/root_component_cpu_guard.ps1
 M code/codex/root_component_lab_profile_export.py
 M notes/BOUCLE_TERRA_COMPOSANTES_PRISMES_2026_11_03.txt
 M notes/BOUCLE_TERRA_RESIDU_AFFINE_2026_11_04.txt
 M notes/REPRISE_111_2026_11_04.txt
 M notes/REPRISE_111_DIAGONALES_2026_11_04.txt
 M notes/REPRISE_111_PAIRES_2026_11_04.txt
 M notes/REPRISE_BETA_DUAL_STRUCTURE_2026_11_05.txt
?? code/codex/root_component_disjoint_cubic_core.py
?? code/codex/root_component_repeated_column_obstruction.py
?? data/codex_anatomy_20261024/full_catalogue_anatomy.progress.json
?? data/codex_anatomy_20261024/full_cut_census.progress.json
?? data/codex_collective_20261021/corner_descent.json
?? data/codex_collective_20261021/corner_descent_cyclic.json
?? data/codex_collective_20261021/corner_descent_cyclic.log
?? data/codex_collective_20261021/corner_descent_disjoint.json
?? data/codex_collective_20261021/corner_descent_hold.json
?? data/codex_collective_20261021/corner_descent_no_presolve.json
?? data/codex_collective_20261021/corner_descent_unrestricted_refined.json
?? data/codex_collective_20261021/corner_guided.json
?? data/codex_collective_20261021/corners_cadical_guided.json
?? data/codex_collective_20261021/scip_root_control.json
?? data/codex_deep_growth_20261025/frontier30to32.cnf
?? data/codex_deep_growth_20261025/frontier30to32.drat
?? data/codex_deep_growth_20261025/frontier30to32_cadical.log
?? data/codex_deep_growth_20261025/frontier30to32_dratcheck.log
?? data/codex_microscope_20261020/adjacent_grid_campaign.json
?? data/codex_microscope_20261020/adjacent_grid_campaign.run.log
?? data/codex_microscope_20261020/case003_cpu_guard.budget.json
?? data/codex_microscope_20261020/case003_cpu_guard.budget.json.previous
?? data/codex_microscope_20261020/case003_cpu_guard.log
?? data/codex_microscope_20261020/case003_cpu_guard.stop
?? data/codex_microscope_20261020/fixed_profiles_summary.json
?? data/codex_microscope_20261020/gz9179_grid_cell_matching_moments.json
?? data/codex_microscope_20261020/gz9179_grid_cell_moments.json
?? data/codex_microscope_20261020/gz9179_grid_cell_moments_complete_cuts.run.log
?? data/codex_microscope_20261020/gz9179_m00_components_linear.json
?? data/codex_microscope_20261020/gz9179_negative_grid_capacity_discovery.json
?? data/codex_microscope_20261020/gz9179_positive_case000_m00_core125_massbound.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m00_promoted20_extensions/core0097.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m00_promoted20_extensions/core0098.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m00_promoted20_extensions/core0099.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m00_promoted20_extensions/core0100.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m00_promoted20_extensions/core0101.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m00_promoted20_extensions/core0120.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m00_promoted20_extensions/core0121.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m00_promoted20_extensions/core0122.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m00_promoted20_extensions/core0123.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m00_promoted20_extensions/core0124.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m01_extensions/core0096.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m01_extensions/core0097.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m01_extensions/core0098.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m01_extensions/core0099.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m01_extensions/core0100.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m01_extensions/core0101.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m01_extensions/core0120.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m01_extensions/core0121.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m01_extensions/core0122.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m01_extensions/core0123.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m01_extensions/core0124.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m01_extensions/core0125.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m02_extensions/core0096.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m02_extensions/core0097.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m02_extensions/core0098.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m02_extensions/core0099.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m02_extensions/core0100.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m02_extensions/core0101.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m02_extensions/core0120.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m02_extensions/core0121.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m02_extensions/core0122.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m02_extensions/core0123.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m02_grid35_extensions/core0124.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m02_grid35_extensions/core0125.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m20_core000.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m20_extensions/core0001.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m20_extensions/core0002.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m20_extensions/core0003.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m20_extensions/core0004.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m20_extensions/core0005.native.input.rup.gz
?? data/codex_microscope_20261020/gz9179_positive_case000_m20_extensions/core0024.native.input.rup.gz
```

## C:\Users\bfhdh\Desktop\Recherche_Conway\c1-norm16-export

Remotes:
```
origin	https://github.com/amazing-source/conway99-c1.git (fetch) [blob:none]
origin	https://github.com/amazing-source/conway99-c1.git (push)
```

Branches:
```
claude/v7-simultaneous                              24dae2b8 [origin/claude/v7-simultaneous: behind 48] papers/rank7: cite Brouwer-van Eijl for the primes not dividing r-s
  codex/asymmetry-audit-20261012                      d9bc91ac Express fixed-sign S3 lifting exactly by ternary linear and quadratic equations
+ codex/c1-arithmetic-audit                           9ccfcefa (C:/Users/bfhdh/Desktop/Recherche_Conway/c1-codex) Record note260 publication and stronger-stage handoff
+ codex/coheawood-hoffman-20261012                    538614f5 (C:/Users/bfhdh/Desktop/Recherche_Conway/c1-asymmetry-audit) Record clean local checkpoint after template 599 closure
* codex/norm16-far-forest                             5100eacf Add omitted-double P4 reduction and a PSD boundary survivor
+ codex/p3-n25-register                               80fc4070 (C:/Users/bfhdh/Desktop/Recherche_Conway/c1-p3-export) Share explicit P3/N25 support registers and encoding for the integer design search
+ main                                                f5199fea (C:/Users/bfhdh/Desktop/Recherche_Conway/c1-main-codex) Exclude low-norm mixed alpha branches and save paused research checkpoint
  remotes/origin/astra/bvls-boundary-release-20261011 5ca5e5de Coordination Astra: reconstruction de bord BVLS après Paley, sans dupliquer les revêtements actifs
  remotes/origin/claude/v7-simultaneous               f2b6454b dossiers_externes: version the external ChatGPT dossiers (Paley 25, BvLS, Hoffman alpha=22, K7 partial, CODE7) and the C3 proof PDF
  remotes/origin/codex/asymmetry-audit-20261012       d9bc91ac Express fixed-sign S3 lifting exactly by ternary linear and quadratic equations
  remotes/origin/codex/c1-arithmetic-audit            19ec3164 Record completed 48 main sweep and clean torsion-four closure reported by peers
  remotes/origin/codex/norm16-far-forest              5100eacf Add omitted-double P4 reduction and a PSD boundary survivor
  remotes/origin/codex/p3-n25-register                80fc4070 Share explicit P3/N25 support registers and encoding for the integer design search
  remotes/origin/lab/biplane243-2026-10-07            d3ddd3f2 lab: biplane configuration of norm 22 absent from both known srg(243,22,1,2)
  remotes/origin/lab/theta-lp-2026-10-08              491ea978 Lab: audit of claude/v7-simultaneous - comparison with Codex's independent audit
  remotes/origin/main                                 0a4cdd8f c3 ledger 537 -> 435 open with the night AWS runs (c3l2, c3p5, partial P4E, z_joint); P3 remainder launched on Spot
```

Status (first80 lines; full in JSON):
```

```

## C:\Users\bfhdh\Desktop\Recherche_Conway\c1-p3-export

Remotes:
```
origin	https://github.com/amazing-source/conway99-c1.git (fetch) [blob:none]
origin	https://github.com/amazing-source/conway99-c1.git (push)
```

Branches:
```
claude/v7-simultaneous                              24dae2b8 [origin/claude/v7-simultaneous: behind 48] papers/rank7: cite Brouwer-van Eijl for the primes not dividing r-s
  codex/asymmetry-audit-20261012                      d9bc91ac Express fixed-sign S3 lifting exactly by ternary linear and quadratic equations
+ codex/c1-arithmetic-audit                           9ccfcefa (C:/Users/bfhdh/Desktop/Recherche_Conway/c1-codex) Record note260 publication and stronger-stage handoff
+ codex/coheawood-hoffman-20261012                    538614f5 (C:/Users/bfhdh/Desktop/Recherche_Conway/c1-asymmetry-audit) Record clean local checkpoint after template 599 closure
+ codex/norm16-far-forest                             5100eacf (C:/Users/bfhdh/Desktop/Recherche_Conway/c1-norm16-export) Add omitted-double P4 reduction and a PSD boundary survivor
* codex/p3-n25-register                               80fc4070 Share explicit P3/N25 support registers and encoding for the integer design search
+ main                                                f5199fea (C:/Users/bfhdh/Desktop/Recherche_Conway/c1-main-codex) Exclude low-norm mixed alpha branches and save paused research checkpoint
  remotes/origin/astra/bvls-boundary-release-20261011 5ca5e5de Coordination Astra: reconstruction de bord BVLS après Paley, sans dupliquer les revêtements actifs
  remotes/origin/claude/v7-simultaneous               f2b6454b dossiers_externes: version the external ChatGPT dossiers (Paley 25, BvLS, Hoffman alpha=22, K7 partial, CODE7) and the C3 proof PDF
  remotes/origin/codex/asymmetry-audit-20261012       d9bc91ac Express fixed-sign S3 lifting exactly by ternary linear and quadratic equations
  remotes/origin/codex/c1-arithmetic-audit            19ec3164 Record completed 48 main sweep and clean torsion-four closure reported by peers
  remotes/origin/codex/norm16-far-forest              5100eacf Add omitted-double P4 reduction and a PSD boundary survivor
  remotes/origin/codex/p3-n25-register                80fc4070 Share explicit P3/N25 support registers and encoding for the integer design search
  remotes/origin/lab/biplane243-2026-10-07            d3ddd3f2 lab: biplane configuration of norm 22 absent from both known srg(243,22,1,2)
  remotes/origin/lab/theta-lp-2026-10-08              491ea978 Lab: audit of claude/v7-simultaneous - comparison with Codex's independent audit
  remotes/origin/main                                 0a4cdd8f c3 ledger 537 -> 435 open with the night AWS runs (c3l2, c3p5, partial P4E, z_joint); P3 remainder launched on Spot
```

Status (first80 lines; full in JSON):
```

```

## C:\Users\bfhdh\Desktop\Recherche_Conway\c1-structures-audit

Remotes:
```
origin	https://github.com/amazing-source/conway99-structures-lab.git (fetch) [blob:none]
origin	https://github.com/amazing-source/conway99-structures-lab.git (push)
```

Branches:
```
* master                3e9690b [origin/master] id 1 (a1^8): pair classes for y1 classes 0 (819) and 1 (1957), swap-filtered, in the Golay frame (basis + scale 8 in the file) for C2's frame_dfs and frame_lp
  remotes/origin/HEAD   -> origin/master
  remotes/origin/master 3e9690b id 1 (a1^8): pair classes for y1 classes 0 (819) and 1 (1957), swap-filtered, in the Golay frame (basis + scale 8 in the file) for C2's frame_dfs and frame_lp
```

Status (first80 lines; full in JSON):
```
D  .gitignore
D  JOURNAL.md
D  NOTE_ASTRA_CERTIFICAT.md
D  NOTE_S11_DEUX_TRIANGLES_SECANTS.md
D  NOTE_S12_VERIF_C1_116.md
D  NOTE_S17_COEUR_CERTIFIE.md
D  NOTE_S21_PSI_STRUCTUREL.md
D  NOTE_S23_ENONCE_DOSSIER4.md
D  NOTE_S24_ASTRA_DOSSIER5.md
D  NOTE_S25_FAMILLE_9_243.md
D  NOTE_S26_ASTRA_ETOILES.md
D  NOTE_S27_INVOLUTION_GENRE_7ADIQUE.md
D  NOTE_S28_AD_NIVEAU_PAIRES.md
D  NOTE_S29_BLOC_PLEIN_LIGNES_RIGIDES.md
D  NOTE_S33_DEUX_BLOCS_TK7.md
D  NOTE_S38_ETAT_ET_PISTES.md
D  NOTE_S5_DISCRIMINANT_MOD4.md
D  NOTE_S8_TOUT_TORDU.md
D  REGISTRE.md
D  ad/HANDOFF_AD_SWEEP.md
D  ad/README.md
D  ad/ablate_mix.py
D  ad/ad_enum_dump.py
D  ad/ad_enum_dump2.py
D  ad/ad_reps_10to21.json
D  ad/ad_reps_6to9.json
D  ad/ad_reps_upto5.json
D  ad/ad_residues_n7_8.json
D  ad/alldd.py
D  ad/alldd_near.py
D  ad/certify.py
D  ad/certify_leaves.py
D  ad/depth_test.py
D  ad/depth_test2.py
D  ad/diag.py
D  ad/diag2.py
D  ad/export_residues.py
D  ad/forced.py
D  ad/general_model.py
D  ad/lp_cert.py
D  ad/near_ablate.py
D  ad/near_conn.py
D  ad/near_diag.py
D  ad/near_smart.py
D  ad/near_smart_ablate.py
D  ad/orbit_psd.py
D  ad/orient_test.py
D  ad/pair_level.py
D  ad/pair_level_relaxed.py
D  ad/proofs_ad2.py
D  ad/psd_cuts.py
D  ad/random_skel.py
D  ad/relaxed1017.log
D  ad/relaxed69.log
D  ad/relaxed69_todo.log
D  ad/relaxed69_todo2.log
D  ad/residue_star.py
D  ad/retest.py
D  ad/retest69.log
D  ad/retest69b.log
D  ad/retest_all.log
D  ad/retest_relaxed.py
D  ad/run_ad2.py
D  ad/run_all.py
D  ad/run_relaxed.py
D  ad/sib_model.py
D  ad/single_orbit_proof.py
D  ad/star_generic.py
D  ad/star_lemma.py
D  ad/star_test.py
D  ad/step1_fullblock.py
D  ad/test20.py
D  ad/test_mix.py
D  ad/test_mix2.py
D  ad/xcheck.py
D  astra/DOSSIER6_INVOLUTION_7ADIQUE.md
D  astra/POUR_SOL_G18_G20_NOS_NOMBRES.md
D  astra/PROBLEMES_OUVERTS_INVOLUTION.md
D  astra/PROBLEME_BLOC_PLEIN_POUR_SOL.md
D  astra/RAPPORT_ASTRA_DOSSIER5.md
```

## C:\Users\bfhdh\Desktop\Recherche_Conway\c2_experimental

Remotes:
```
origin	https://github.com/amazing-source/conway99-c2-experimental.git (fetch)
origin	https://github.com/amazing-source/conway99-c2-experimental.git (push)
```

Branches:
```
* master                89592e2 [origin/master] (C) gamma_c2: Gamma = Aut(U)/W(R) for 46 envelopes (make_gammas.py, C1's gamma_general.py)
  remotes/origin/HEAD   -> origin/master
  remotes/origin/master 89592e2 (C) gamma_c2: Gamma = Aut(U)/W(R) for 46 envelopes (make_gammas.py, C1's gamma_general.py)
```

Status (first80 lines; full in JSON):
```
M data/cert_results.txt
 M data/finishC/finishC_tracker.json
 M logs/cloud_tasks_rtA.txt
 M logs/cloud_tasks_rtB.txt
 D logs/cloud_tasks_tier6.txt
 M logs/docker_tasks_tier8.txt
 M logs/filter_all.log
 M logs/fixcamp_queue.log
 M logs/freestar_ansatz.log
 M logs/make_gammas.log
 M logs/prof_gen_m1n6_0_smooth.out
 M notes/22_annexes/D_revue_branche_C1.md
 M notes/46_LIGNE_D_ARRIVEE_C2.md
 M scripts/cloud_worker.sh
 M scripts/o24_search.py
 M scripts/win_lane.ps1
?? HANDOVER_2026-10-04.md
?? PLAN_AWS.md
?? aws_repo/
?? azure_layer_wip/
?? backups/
?? c2_cloud_calib/
?? c2_cloud_run.zip
?? c2_cloud_run/
?? c2_cloud_run_v10.zip
?? c2_cloud_run_v10/
?? c2_cloud_run_v2.zip
?? c2_cloud_run_v2/
?? c2_cloud_run_v3.zip
?? c2_cloud_run_v3/
?? c2_cloud_run_v4.zip
?? c2_cloud_run_v4/
?? c2_cloud_run_v5.zip
?? c2_cloud_run_v5/
?? c2_cloud_run_v6.zip
?? c2_cloud_run_v6/
?? c2_cloud_run_v7.zip
?? c2_cloud_run_v7/
?? c2_cloud_run_v8.zip
?? c2_cloud_run_v8/
?? c2_cloud_run_v9.zip
?? c2_cloud_run_v9/
?? data/ab_chunk/
?? data/bench/
?? data/cascade_snapshot_2026-10-02/
?? data/finishC/compbudget2_0.jsonl
?? data/finishC/compbudget2_1.jsonl
?? data/finishC/compbudget2_2.jsonl
?? data/finishC/compbudget2_3.jsonl
?? data/finishC/compbudget_0.jsonl
?? data/finishC/compbudget_1.jsonl
?? data/finishC/compbudget_2.jsonl
?? data/finishC/compbudget_3.jsonl
?? data/finishC/compbudget_4.jsonl
?? data/finishC/compbudget_5.jsonl
?? data/finishC/finishC_tracker_backup_2027.json
?? data/finishC/finishC_tracker_backup_2130.json
?? data/finishC/finishC_tracker_backup_2909.json
?? data/finishC/finishC_tracker_backup_2915.json
?? data/finishC/frame_dfs/
?? data/finishC/gamma_c2/gamma_025.json
?? data/finishC/gamma_c2/gamma_076.json
?? data/finishC/gamma_c2/gamma_077.json
?? data/finishC/gamma_c2/gamma_079.json
?? data/finishC/gamma_c2/gamma_080.json
?? data/finishC/gamma_c2/gamma_081.json
?? data/finishC/gamma_c2/gamma_082.json
?? data/finishC/gamma_c2/gamma_083.json
?? data/finishC/gamma_c2/gamma_084.json
?? data/finishC/gamma_c2/gamma_085.json
?? data/finishC/gamma_c2/gamma_086.json
?? data/finishC/gamma_c2/gamma_088.json
?? data/finishC/gamma_c2/gamma_089.json
?? data/finishC/gamma_c2/gamma_090.json
?? data/finishC/gamma_c2/gamma_091.json
?? data/finishC/gamma_c2/gamma_092.json
?? data/finishC/gamma_c2/gamma_093.json
?? data/finishC/gamma_c2/gamma_095.json
?? data/finishC/gamma_c2/gamma_098.json
?? data/finishC/gamma_c2/gamma_103.json
```

## C:\Users\bfhdh\Desktop\Recherche_Conway\c2_experimental\aws_repo

Remotes:
```
origin	https://github.com/amazing-source/conway99-c2-aws.git (fetch) [blob:none]
origin	https://github.com/amazing-source/conway99-c2-aws.git (push)
```

Branches:
```
+ codex/t20-dual-hand                                        76ba508a9 (C:/Users/bfhdh/Desktop/Recherche_Conway/t20-codex) Clarify limits of Borcherds table transcription attribution
  lab-records-2026-10-07                                     fa5a181cd [origin/lab-records-2026-10-07: ahead 2, behind 2] Lab PC records: tracker at 156 of 156 (conversion of 2026-10-07 17:47 UTC), acceptance record of T18 and T20, final reports, tracker backup at 143
* master                                                     3f0a07921 [origin/master: ahead 349, behind 443] Paper table: root types with equal components grouped, asserted equal to the exact recomputation for all 156 lattices; caption no longer attributes an unchecked transcription to Borcherds
+ queue-ci                                                   1c0379166 (C:/Users/bfhdh/Desktop/Recherche_Conway/c2_experimental/qci_wt) [origin/queue-ci: ahead 7, behind 6] queue-ci: reset for the v10 rehearsal (same four jobs as v9)
  v10                                                        579766a2b v10: Y=13 pair filter (min L* >= 9/7), FD_MIN97=1 in env_exact; agent parses two-digit package versions; rehearsal workflow
  v2                                                         1e80b0991 [origin/v2: ahead 18, behind 18] v2 package fix: exclude run_jobs' RESULTATS_slice tarball from the MANIFEST (the CI rehearsal caught a manifest refusal after calibration)
  v3                                                         c022c8696 v3 fix: o24_run_fast creates data/finishC/o24_dfs before saving (the v3 rehearsal caught the O24 job failing at save time)
  v4                                                         10be103e4 v4: package v4 (golay_pairs jobs for 002, 004, 010 from golay_gen.py; golay job v4 with block loading and INCOMPLETE retry)
  v5                                                         97e9e1f7a v5 rebuild: the retry-path calibration compares verdicts only (node counts are CPU-dependent)
  v6                                                         75dfc6bbf v6: stream node limit 4e9 (run_jobs) and job kind resolve (the 28 unresolved INCOMPLETE pairs of 037, no node limit)
  v7                                                         d0933ecc4 v7: spare sub-jobs (stream x8, golay x10/x8) so that slow jobs can be split on demand; only jobs.json differs from v6
  v8                                                         b58eb1a09 v8: resolve lists of 023, 024, 026, 028 (118 INCOMPLETE K=0 pairs of the v2 stream, one per job); only the lists and jobs.json differ from v7
  v9                                                         5b1ea6c96 v9: fine jobs (one y1 per stream job; Golay 001 n=1700, 002 n=23040) for every open lattice; only jobs.json differs from v8
  remotes/origin/HEAD                                        -> origin/master
  remotes/origin/agent-backlog                               72e4bdade qagent: a refused queue transaction is no longer fatal (events kept for the next cycle); retries re-read the queue branch only; Q_LOOKAHEAD (local backlog of claimed jobs) and Q_SYNC_MIN (minimum interval between queue transactions). Defaults unchanged. Not yet rehearsed.
  remotes/origin/defer-mode                                  e03125329 HANDOFF section 16: deferral mode deployed (design, validation, measured coverage, fleet, lemma status)
  remotes/origin/defer-n4                                    d4ff4aa5e Deferral: norm-4 witnesses of T20 (Q_DEFER_N4=1): a pair with x of norm 4 and |(x,y1)| = |(x,y2)| = 3 (E = 10) is deferred with its own verdict and index list. Not yet rehearsed.
  remotes/origin/defer-quick                                 b263f243f Deferral, quick variant (Q_DEFER_NODES=0): a lemma-covered pair that passes the engine's two immediate tests is deferred without calling the engine's search (set-up was 0.3 s per pair, 70 % of a deferral job). Not yet validated.
  remotes/origin/lab-records-2026-10-07                      1ee9115c7 Lab PC records: tracker at 156 of 156 (conversion of 2026-10-07 17:47 UTC), acceptance record of T18 and T20, final reports, tracker backup at 143
  remotes/origin/lemma-archive/t20_n3_routeB                 bf5a0e33f Raw outputs of T20 Computation 9.29 (case I, n_3 = 2, route B): stage 1, stage 2, second program
  remotes/origin/lemma-run/selftest-i-0dee8516208b24d42      a15efe89a lemma run selftest on i-0dee8516208b24d42: FINISHED exit=0
  remotes/origin/lemma-run/t20_I1_340-i-019e86d399c17954f    95a4e0ce5 lemma run t20_I1_340 on i-019e86d399c17954f: FINISHED exit=0
  remotes/origin/lemma-run/t20_I_rest-i-02f356c70da99d700    b933f2f09 lemma run t20_I_rest on i-02f356c70da99d700: FINISHED exit=0
  remotes/origin/lemma-run/t20_Iv_A-i-0390fd53333c148ad      5bbdbc0ad lemma run t20_Iv_A on i-0390fd53333c148ad: INSTALLING
  remotes/origin/lemma-run/t20_Iv_B-i-0a03ce79bff09fa5d      7d8c0b997 lemma run t20_Iv_B on i-0a03ce79bff09fa5d: FINISHED exit=0
  remotes/origin/lemma-run/t20_Iv_C-i-092f5550d84f61e09      014b68258 lemma run t20_Iv_C on i-092f5550d84f61e09: FINISHED exit=0
  remotes/origin/lemma-run/t20_Iv_D-i-09169834049067883      12a885868 lemma run t20_Iv_D on i-09169834049067883: FINISHED exit=0
  remotes/origin/lemma-run/t20_Iv_E-i-0cd9427b48ee5704e      c6a3d9309 lemma run t20_Iv_E on i-0cd9427b48ee5704e: RUNNING
  remotes/origin/lemma-run/t20_Iv_F-i-0c5414832a6ac4ff5      0e2818ace lemma run t20_Iv_F on i-0c5414832a6ac4ff5: RUNNING
  remotes/origin/lemma-run/t20_Iv_G-i-05703a74fbb027423      e7d9c3caa lemma run t20_Iv_G on i-05703a74fbb027423: FINISHED exit=0
  remotes/origin/lemma-run/t20_Iv_H-i-004334efafb6ceb56      e5bd9b524 lemma run t20_Iv_H on i-004334efafb6ceb56: FINISHED exit=0
  remotes/origin/lemma-run/t20_Iv_I-i-032b7d25d335204f8      fa9934d59 lemma run t20_Iv_I on i-032b7d25d335204f8: FINISHED exit=0
  remotes/origin/lemma-run/t20_Iv_J-i-038ea54927e5a01c4      33bbe996e lemma run t20_Iv_J on i-038ea54927e5a01c4: FINISHED exit=0
  remotes/origin/lemma-run/t20_n3-i-04bb3ac564f658b79        4d1897bdd lemma run t20_n3 on i-04bb3ac564f658b79: RUNNING
  remotes/origin/lemma-run/t20_n3-i-0b8ae938c1fc89c62        df13c1d5f lemma run t20_n3 on i-0b8ae938c1fc89c62: RUNNING
  remotes/origin/lemma-run/t20_n3_sample-i-0cefd01aef8eade8a 0a4498e16 lemma run t20_n3_sample on i-0cefd01aef8eade8a: RUNNING
  remotes/origin/master                                      60fa90e40 Mandate C: the 72 star-less verdicts confirmed by exhaustive enumeration without solver (72 of 72)
  remotes/origin/queue                                       f134ddf44 control: credit_usd=13.76
  remotes/origin/queue-ci                                    93a85f547 qci-v10a done:1
  remotes/origin/queue-cid                                   5a8f10f44 qci-v10d done:1
  remotes/origin/run/frere-euc1-0                            51ad50203 frere-euc1-0 EN_COURS 2026-09-30T05:07:46Z
  remotes/origin/run/frere-eun1-0                            7e016bee9 frere-eun1-0 EN_COURS 2026-09-30T05:05:23Z
  remotes/origin/run/frere-euw2-0                            fc487ecad frere-euw2-0 EN_COURS 2026-09-30T05:11:29Z
  remotes/origin/run/frere-use1-0                            be7391006 frere-use1-0 EN_COURS 2026-09-29T22:03:09Z
  remotes/origin/run/frere-use2-0                            51b49b4ec frere-use2-0 EN_COURS 2026-09-29T23:08:32Z
  remotes/origin/run/frere-usw2-0                            97521504b frere-usw2-0 EN_COURS 2026-09-29T21:59:53Z
  remotes/origin/run/pere-euc1-0                             c46b5efa1 pere-euc1-0 EN_COURS 2026-09-30T05:07:54Z
  remotes/origin/run/pere-eun1-0                             87d9ec320 pere-eun1-0 EN_COURS 2026-09-30T05:05:53Z
  remotes/origin/run/pere-euw2-0                             9d100e6cb pere-euw2-0 EN_COURS 2026-09-30T05:11:35Z
  remotes/origin/run/pere-use1-0                             3f6bab4cb pere-use1-0 EN_COURS 2026-09-29T22:08:48Z
  remotes/origin/run/pere-use2-0                             5c5c39b77 pere-use2-0 EN_COURS 2026-09-29T23:15:03Z
  remotes/origin/run/pere-usw2-0                             68ee25c7a pere-usw2-0 EN_COURS 2026-09-29T22:00:13Z
  remotes/origin/run/q-i-0007aedf88590282f                   79bdcf2a5 q-i-0007aedf88590282f INTERRUPTED 2026-10-07T14:32:33Z
  remotes/origin/run/q-i-003d278c405e099f8                   11c005729 q-i-003d278c405e099f8 EN_COURS 2026-10-04T14:37:40Z
  remotes/origin/run/q-i-0058b87765fd902ac                   873f0e2ef q-i-0058b87765fd902ac FINI 2026-10-07T18:29:15Z
  remotes/origin/run/q-i-00602e633195b38d8                   d4ef142d8 q-i-00602e633195b38d8 FINI 2026-10-07T05:47:41Z
  remotes/origin/run/q-i-008a374f92faec021                   1f1cefd97 q-i-008a374f92faec021 ERREUR AGENT 2026-10-06T13:00:22Z
  remotes/origin/run/q-i-008bbb215228c6869                   e6e95aa6d q-i-008bbb215228c6869 STOP (terminated from the PC) 2026-10-06T23:47:04Z
  remotes/origin/run/q-i-00925e8996c5d49fc                   659cde539 q-i-00925e8996c5d49fc FINI 2026-10-07T05:32:55Z
  remotes/origin/run/q-i-009b8ce54f3a78709                   b313e1baf q-i-009b8ce54f3a78709 STOP (terminated from the PC) 2026-10-06T14:47:41Z
  remotes/origin/run/q-i-00a0ab97a6a8099fd                   a15f705c6 q-i-00a0ab97a6a8099fd STOP (terminated from the PC) 2026-10-07T12:49:30Z
  remotes/origin/run/q-i-00a7b5e21909a98d1                   e551926e1 q-i-00a7b5e21909a98d1 FINI 2026-10-07T15:19:39Z
  remotes/origin/run/q-i-01028dcab733e510e                   f44d89d2a q-i-01028dcab733e510e STOP (terminated from the PC) 2026-10-06T23:47:04Z
  remotes/origin/run/q-i-010bcc0075d83a855                   68af346bd q-i-010bcc0075d83a855 INTERRUPTED 2026-10-07T01:34:04Z
  remotes/origin/run/q-i-011cdbf73eb1c5524                   3e83af55c q-i-011cdbf73eb1c5524 FINI 2026-10-07T18:29:07Z
  remotes/origin/run/q-i-011dce74cd612fc52                   ba04654dc q-i-011dce74cd612fc52 FINI 2026-10-07T17:43:25Z
  remotes/origin/run/q-i-0126bbe8cfe58cfdd                   683c924b0 q-i-0126bbe8cfe58cfdd STOP (terminated from the PC) 2026-10-06T23:47:04Z
  remotes/origin/run/q-i-01342f629eff35dc3                   37680b3fb q-i-01342f629eff35dc3 FINI 2026-10-07T14:53:27Z
  remotes/origin/run/q-i-0149028a4e29f2bfe                   b238ac10d q-i-0149028a4e29f2bfe INTERRUPTED 2026-10-06T17:03:02Z
  remotes/origin/run/q-i-014f982e79fc44389                   bb7dc1ec3 q-i-014f982e79fc44389 EN_COURS 2026-10-07T14:53:36Z
  remotes/origin/run/q-i-0157fafabb9e40145                   4b3569d03 q-i-0157fafabb9e40145 STOP (terminated from the PC) 2026-10-06T23:49:30Z
  remotes/origin/run/q-i-01597373ced95afb1                   45d264d09 q-i-01597373ced95afb1 STOP (terminated from the PC) 2026-10-06T22:11:01Z
  remotes/origin/run/q-i-0163b9385e47e4dfd                   4f49770cd q-i-0163b9385e47e4dfd INTERRUPTED 2026-10-06T15:57:29Z
  remotes/origin/run/q-i-0175d90b21760467a                   57958d77e q-i-0175d90b21760467a FINI 2026-10-07T05:42:24Z
  remotes/origin/run/q-i-01866477c48c3d7d8                   349eb4534 q-i-01866477c48c3d7d8 STOP 2026-10-03T10:49:29Z
  remotes/origin/run/q-i-01ad68b6cbef7c9c0                   ac3f47979 q-i-01ad68b6cbef7c9c0 FINI 2026-10-07T20:23:33Z
  remotes/origin/run/q-i-01c02b0a392fd4661                   e53580e94 q-i-01c02b0a392fd4661 INTERRUPTED 2026-10-07T14:47:42Z
  remotes/origin/run/q-i-01cba7ba0fb3204e4                   5ced3c513 q-i-01cba7ba0fb3204e4 EN_COURS 2026-10-07T14:24:31Z
  remotes/origin/run/q-i-01d993ebe8987ed6a                   e59894d32 q-i-01d993ebe8987ed6a FINI 2026-10-07T20:19:03Z
  remotes/origin/run/q-i-0201ab6c589d46854                   704557cbd q-i-0201ab6c589d46854 STOP 2026-10-05T10:06:25Z
  remotes/origin/run/q-i-0242e76bf23d90e2f                   090543bb7 q-i-0242e76bf23d90e2f FINI 2026-10-06T17:53:49Z
  remotes/origin/run/q-i-0243e91a6c62ae950                   ef15273f1 q-i-0243e91a6c62ae950 EN_COURS 2026-10-04T14:40:26Z
  remotes/origin/run/q-i-024b07e5fa9d980a5                   24d663d9b q-i-024b07e5fa9d980a5 FINI 2026-10-07T18:31:17Z
  remotes/origin/run/q-i-025be10f67c1fb32a                   8df33eaa0 q-i-025be10f67c1fb32a INTERRUPTED 2026-10-02T07:37:41Z
  remotes/origin/run/q-i-025ec33081e30e55a                   f8206a4a1 q-i-025ec33081e30e55a INTERRUPTED 2026-10-06T14:22:39Z
  remotes/origin/run/q-i-0264624104d7e9d74                   6113f7f61 q-i-0264624104d7e9d74 INTERRUPTED 2026-10-03T08:01:14Z
  remotes/origin/run/q-i-026b674ec4b914602                   6340d69cc q-i-026b674ec4b914602 INTERRUPTED 2026-10-07T13:31:35Z
  remotes/origin/run/q-i-026e2eda9e2b5dfdb                   ad1816860 q-i-026e2eda9e2b5dfdb EN_COURS 2026-10-07T14:22:12Z
  remotes/origin/run/q-i-028bed5a8e755ec78                   50fab57f8 q-i-028bed5a8e755ec78 STOP (terminated from the PC) 2026-10-06T23:09:34Z
  remotes/origin/run/q-i-029b7027bf533447b                   76a12c91f q-i-029b7027bf533447b STOP 2026-10-03T10:51:41Z
  remotes/origin/run/q-i-029f440141955366f                   e9a751796 q-i-029f440141955366f STOP (terminated from the PC) 2026-10-06T22:40:17Z
  remotes/origin/run/q-i-02a5f5b29477f6f99                   d52626f8a q-i-02a5f5b29477f6f99 INTERRUPTED 2026-10-03T10:14:09Z
  remotes/origin/run/q-i-02aa613ee361fbc10                   d70288ec2 q-i-02aa613ee361fbc10 EN_COURS 2026-10-07T16:13:23Z
  remotes/origin/run/q-i-02c22281be51a85b0                   cc92890c2 q-i-02c22281be51a85b0 INTERRUPTED 2026-10-06T14:37:25Z
  remotes/origin/run/q-i-02cb727a152a622e4                   78357c595 q-i-02cb727a152a622e4 FINI 2026-10-06T17:50:31Z
  remotes/origin/run/q-i-02f5e47e7fe6aba80                   e46d780a7 q-i-02f5e47e7fe6aba80 STOP (terminated from the PC) 2026-10-06T22:11:01Z
  remotes/origin/run/q-i-02fc30d4640fca3fa                   48e9250be q-i-02fc30d4640fca3fa STOP 2026-10-03T10:50:50Z
  remotes/origin/run/q-i-03008ed0607c0af47                   ae0442441 q-i-03008ed0607c0af47 STOP (terminated from the PC) 2026-10-06T23:49:30Z
  remotes/origin/run/q-i-031bd5d874fc9c8e8                   fa7586317 q-i-031bd5d874fc9c8e8 FINI 2026-10-07T01:39:06Z
  remotes/origin/run/q-i-03216e01aa27ec88d                   89694a93a q-i-03216e01aa27ec88d STOP (terminated from the PC) 2026-10-06T14:47:41Z
  remotes/origin/run/q-i-032ff3b5eda1ce09e                   0f3019a1b q-i-032ff3b5eda1ce09e EN_COURS 2026-10-04T14:38:20Z
  remotes/origin/run/q-i-033e48138746dbc88                   5f8844d65 q-i-033e48138746dbc88 STOP (terminated from the PC) 2026-10-07T05:13:17Z
  remotes/origin/run/q-i-035c2a86b163858c2                   0cb00d479 q-i-035c2a86b163858c2 INTERRUPTED 2026-10-02T20:01:43Z
  remotes/origin/run/q-i-036c5c29f417b3487                   e38632934 q-i-036c5c29f417b3487 INTERRUPTED 2026-10-04T04:55:46Z
  remotes/origin/run/q-i-0371888c776e26bbf                   ddc2e15c2 q-i-0371888c776e26bbf INSTALLATION 2026-10-07T17:04:19Z
  remotes/origin/run/q-i-03dc85e2a3417e606                   5758bee66 q-i-03dc85e2a3417e606 STOP (terminated from the PC) 2026-10-07T05:13:17Z
  remotes/origin/run/q-i-03e9fcedad48e9625                   6db84b0e4 q-i-03e9fcedad48e9625 INTERRUPTED 2026-10-04T06:34:46Z
  remotes/origin/run/q-i-03f2d86e1f691f955                   97b3bdea5 q-i-03f2d86e1f691f955 STOP 2026-10-03T10:47:56Z
  remotes/origin/run/q-i-03fc279ba375a421c                   c5f2f3b12 q-i-03fc279ba375a421c STOP (terminated from the PC) 2026-10-06T22:11:01Z
  remotes/origin/run/q-i-0475a297578983215                   8f0a66709 q-i-0475a297578983215 INTERRUPTED 2026-10-03T08:01:17Z
  remotes/origin/run/q-i-04979887a2789fb83                   225685ba3 q-i-04979887a2789fb83 STOP 2026-10-03T10:50:45Z
  remotes/origin/run/q-i-04a2424fac34284e8                   f2c0e0df9 q-i-04a2424fac34284e8 INTERRUPTED 2026-10-03T08:01:21Z
  remotes/origin/run/q-i-04af0d2c393f35d5c                   0889903e1 q-i-04af0d2c393f35d5c STOP 2026-10-02T02:16:18Z
  remotes/origin/run/q-i-04ba84a7d64b81116                   c93eea803 q-i-04ba84a7d64b81116 INTERRUPTED 2026-10-07T14:49:13Z
  remotes/origin/run/q-i-04c611bf415f81b02                   7958e6ab7 q-i-04c611bf415f81b02 INTERRUPTED 2026-10-02T20:12:17Z
  remotes/origin/run/q-i-04dcdc6392cd9fe1d                   836db717b q-i-04dcdc6392cd9fe1d EN_COURS 2026-10-07T04:37:31Z
  remotes/origin/run/q-i-04eeecb80a5c72755                   bacf58eb3 q-i-04eeecb80a5c72755 INTERRUPTED 2026-10-06T14:22:06Z
  remotes/origin/run/q-i-050146d35c06c0336                   2623e442b q-i-050146d35c06c0336 FINI 2026-10-07T03:08:39Z
  remotes/origin/run/q-i-0520c5d3f009c5a4a                   b65e67d44 q-i-0520c5d3f009c5a4a INTERRUPTED 2026-10-01T22:36:07Z
  remotes/origin/run/q-i-052249d51da1a1596                   9525e2b60 q-i-052249d51da1a1596 EN_COURS 2026-10-07T18:46:29Z
  remotes/origin/run/q-i-054379e6cd4f03332                   07094c71d q-i-054379e6cd4f03332 STOP (terminated from the PC) 2026-10-06T22:11:01Z
  remotes/origin/run/q-i-05e123fd3b6f34dc7                   7985b04cc q-i-05e123fd3b6f34dc7 FINI 2026-10-07T06:05:18Z
  remotes/origin/run/q-i-05e20a652a9b41e97                   9409eddc6 q-i-05e20a652a9b41e97 STOP (terminated from the PC) 2026-10-07T09:24:11Z
  remotes/origin/run/q-i-061c40f7fb049da5d                   ae509f775 q-i-061c40f7fb049da5d INTERRUPTED 2026-10-03T03:17:53Z
  remotes/origin/run/q-i-062d6f242375b1fe4                   460d4cfb7 q-i-062d6f242375b1fe4 INTERRUPTED 2026-10-02T19:05:37Z
  remotes/origin/run/q-i-0633e9c6510b7a07f                   3e3a3c342 q-i-0633e9c6510b7a07f STOP (terminated from the PC) 2026-10-06T23:47:04Z
  remotes/origin/run/q-i-064db7733386366ef                   eb9612fac q-i-064db7733386366ef INTERRUPTED 2026-10-06T16:36:38Z
  remotes/origin/run/q-i-0677b8b475388ce7e                   7ca81f383 q-i-0677b8b475388ce7e INTERRUPTED 2026-10-07T14:33:35Z
  remotes/origin/run/q-i-0677d76eeb19369f0                   9e61a122b q-i-0677d76eeb19369f0 INSTALLATION 2026-10-07T15:06:12Z
  remotes/origin/run/q-i-067c8886509d5f9ea                   0ceb919d9 q-i-067c8886509d5f9ea STOP (terminated from the PC) 2026-10-06T23:47:04Z
  remotes/origin/run/q-i-069823739875ec782                   a6144c94e q-i-069823739875ec782 ERREUR AGENT 2026-10-06T23:35:18Z
  remotes/origin/run/q-i-06a7607e4c50e49d5                   a764e4b4e q-i-06a7607e4c50e49d5 STOP (terminated from the PC) 2026-10-07T05:13:17Z
  remotes/origin/run/q-i-06aec8054a564a8e5                   0387e316c q-i-06aec8054a564a8e5 FINI 2026-10-07T06:13:17Z
  remotes/origin/run/q-i-06f59d4983625a388                   dba82d08b q-i-06f59d4983625a388 STOP (terminated from the PC) 2026-10-06T23:09:34Z
  remotes/origin/run/q-i-070065653a5f0df24                   d81f6738c q-i-070065653a5f0df24 INTERRUPTED 2026-10-07T01:47:04Z
  remotes/origin/run/q-i-0717750673326e465                   b5f2dc7ca q-i-0717750673326e465 STOP (terminated from the PC) 2026-10-06T23:47:04Z
  remotes/origin/run/q-i-07194a18450f2a06e                   a69f5d6e8 q-i-07194a18450f2a06e STOP (terminated from the PC) 2026-10-07T12:49:30Z
  remotes/origin/run/q-i-07366de1470e7648a                   c4bbea996 q-i-07366de1470e7648a STOP (terminated from the PC) 2026-10-07T06:24:22Z
  remotes/origin/run/q-i-0738a86689ab8fb74                   babe09ca8 q-i-0738a86689ab8fb74 STOP (terminated from the PC) 2026-10-06T14:47:41Z
  remotes/origin/run/q-i-0742677fb55fcd71a                   47d505eab q-i-0742677fb55fcd71a INTERRUPTED 2026-10-06T17:10:10Z
  remotes/origin/run/q-i-074808dad30139068                   a9f4ecc73 q-i-074808dad30139068 INTERRUPTED 2026-10-03T00:30:49Z
  remotes/origin/run/q-i-0759cbe1f271decac                   e047cadaa q-i-0759cbe1f271decac INTERRUPTED 2026-10-02T09:03:19Z
  remotes/origin/run/q-i-077230baffaf0b835                   d7059efa0 q-i-077230baffaf0b835 FINI 2026-10-07T06:17:37Z
  remotes/origin/run/q-i-0775d0ef0fc2b023a                   2b110c27f q-i-0775d0ef0fc2b023a INTERRUPTED 2026-10-06T17:13:15Z
  remotes/origin/run/q-i-077b44162d0b9c0b4                   461b3480d q-i-077b44162d0b9c0b4 INTERRUPTED 2026-10-06T21:16:28Z
  remotes/origin/run/q-i-078d5c153bfd2caa9                   eec46947b q-i-078d5c153bfd2caa9 STOP 2026-10-05T10:09:34Z
  remotes/origin/run/q-i-07959d1a6ef559a4c                   5296defba q-i-07959d1a6ef559a4c STOP 2026-10-02T02:16:37Z
  remotes/origin/run/q-i-07a70e4361d9b0c50                   ad7f3cf5c q-i-07a70e4361d9b0c50 STOP (terminated from the PC) 2026-10-07T05:13:17Z
  remotes/origin/run/q-i-07a9545ff43eb7971                   b4120e8b3 q-i-07a9545ff43eb7971 STOP (terminated from the PC) 2026-10-07T06:24:22Z
  remotes/origin/run/q-i-07b69e1205a8909d8                   890a57216 q-i-07b69e1205a8909d8 INTERRUPTED 2026-10-04T10:10:21Z
  remotes/origin/run/q-i-07bab8da962e7387a                   26521a256 q-i-07bab8da962e7387a EN_COURS 2026-10-04T14:38:58Z
  remotes/origin/run/q-i-07dafa59b6d6bb72a                   9a9b6ffc1 q-i-07dafa59b6d6bb72a EN_COURS 2026-10-07T15:30:35Z
  remotes/origin/run/q-i-07ed9a020e51d514e                   68fd48167 q-i-07ed9a020e51d514e STOP (terminated from the PC) 2026-10-06T23:47:04Z
  remotes/origin/run/q-i-07f2923eeb11cfe80                   fa63a3f01 q-i-07f2923eeb11cfe80 STOP (terminated from the PC) 2026-10-06T22:40:17Z
  remotes/origin/run/q-i-080e1d0be9807b4a2                   aa533c0ad q-i-080e1d0be9807b4a2 INTERRUPTED 2026-10-06T17:02:41Z
  remotes/origin/run/q-i-0820ff9ccb2543e33                   0fcb0723a q-i-0820ff9ccb2543e33 INTERRUPTED 2026-10-02T19:07:40Z
  remotes/origin/run/q-i-083a27a437f31bb9a                   48b57d53f q-i-083a27a437f31bb9a STOP (terminated from the PC) 2026-10-06T23:49:30Z
  remotes/origin/run/q-i-0842035457bba071a                   6e17bbe52 q-i-0842035457bba071a EN_COURS 2026-10-07T14:13:42Z
  remotes/origin/run/q-i-08471079f0542dd91                   97bc32e5a q-i-08471079f0542dd91 FINI 2026-10-07T14:49:27Z
  remotes/origin/run/q-i-084bd5ac37cffb8f8                   2dfa32e26 q-i-084bd5ac37cffb8f8 STOP (terminated from the PC) 2026-10-06T23:09:34Z
  remotes/origin/run/q-i-087b3674d1c8f0bb5                   0a82d08a2 q-i-087b3674d1c8f0bb5 FINI 2026-10-07T05:58:18Z
  remotes/origin/run/q-i-08e6786e978c36698                   cf361e4ac q-i-08e6786e978c36698 STOP (terminated from the PC) 2026-10-06T14:47:41Z
  remotes/origin/run/q-i-08ef09bd21655765e                   4fccffd51 q-i-08ef09bd21655765e EN_COURS 2026-10-07T14:54:36Z
  remotes/origin/run/q-i-08fb99c895223117a                   bd04357c5 q-i-08fb99c895223117a INTERRUPTED 2026-10-02T07:35:28Z
  remotes/origin/run/q-i-090db4b47b2d5ab04                   215383dd1 q-i-090db4b47b2d5ab04 STOP (terminated from the PC) 2026-10-06T23:47:04Z
  remotes/origin/run/q-i-0915313793048bc43                   ccab1dfd3 q-i-0915313793048bc43 EN_COURS 2026-10-07T15:17:12Z
  remotes/origin/run/q-i-0917fa5309b737275                   6e4dbde52 q-i-0917fa5309b737275 FINI 2026-10-07T15:45:04Z
  remotes/origin/run/q-i-09726ab19a395f27e                   1fa6ccbbc q-i-09726ab19a395f27e INTERRUPTED 2026-10-06T17:38:50Z
  remotes/origin/run/q-i-099093797d31d4403                   1009a25a0 q-i-099093797d31d4403 EN_COURS 2026-10-07T18:14:57Z
  remotes/origin/run/q-i-0997f7ef90634e8ec                   6b2e24b7c q-i-0997f7ef90634e8ec INTERRUPTED 2026-10-02T05:55:14Z
  remotes/origin/run/q-i-09b06647445f6a2cf                   6df679235 q-i-09b06647445f6a2cf ERREUR AGENT 2026-10-06T23:29:54Z
  remotes/origin/run/q-i-09b558abf286ca037                   c755ef55f q-i-09b558abf286ca037 INTERRUPTED 2026-10-06T23:52:53Z
  remotes/origin/run/q-i-09c13ec16873de889                   2de51e01c q-i-09c13ec16873de889 STOP (terminated from the PC) 2026-10-06T14:47:41Z
  remotes/origin/run/q-i-09c31398edb79ef34                   5bca941de q-i-09c31398edb79ef34 STOP (terminated from the PC) 2026-10-06T14:47:41Z
  remotes/origin/run/q-i-09e5adb0d653f40fa                   48981d7f3 q-i-09e5adb0d653f40fa FINI 2026-10-07T03:45:07Z
  remotes/origin/run/q-i-09ea743f3176922f4                   963ab5ca7 q-i-09ea743f3176922f4 INTERRUPTED 2026-10-02T20:01:35Z
  remotes/origin/run/q-i-09ee6f02570710dff                   ee5053e5d q-i-09ee6f02570710dff INTERRUPTED 2026-10-02T17:07:39Z
  remotes/origin/run/q-i-09ef67e96d2352cfb                   623fb0f56 q-i-09ef67e96d2352cfb FINI 2026-10-07T05:48:04Z
  remotes/origin/run/q-i-0a075cb17c06082cc                   a1a909910 q-i-0a075cb17c06082cc EN_COURS 2026-10-07T15:03:44Z
  remotes/origin/run/q-i-0a270ba19d9869f80                   abf0e7b27 q-i-0a270ba19d9869f80 INTERRUPTED 2026-10-03T08:01:11Z
  remotes/origin/run/q-i-0a2d32e20518d811a                   d20690933 q-i-0a2d32e20518d811a STOP (terminated from the PC) 2026-10-06T23:47:04Z
  remotes/origin/run/q-i-0a2f259889b0c0e5a                   d9213892b q-i-0a2f259889b0c0e5a STOP (terminated from the PC) 2026-10-06T14:47:41Z
  remotes/origin/run/q-i-0a3fa380d1f25690d                   9438d6c55 q-i-0a3fa380d1f25690d EN_COURS 2026-10-07T18:15:16Z
  remotes/origin/run/q-i-0a4ce7e951acd259e                   4ad9bb6da q-i-0a4ce7e951acd259e STOP (terminated from the PC) 2026-10-06T23:09:34Z
  remotes/origin/run/q-i-0a53459bb549dca86                   5e60815a1 q-i-0a53459bb549dca86 STOP (terminated from the PC) 2026-10-07T06:24:22Z
  remotes/origin/run/q-i-0a5e721fef6a7ac8d                   305430761 q-i-0a5e721fef6a7ac8d FINI 2026-10-07T04:38:03Z
  remotes/origin/run/q-i-0a6ff036888ae8447                   261af52df q-i-0a6ff036888ae8447 FINI 2026-10-07T06:24:41Z
  remotes/origin/run/q-i-0a772da7196ebb00a                   da4b39f9b q-i-0a772da7196ebb00a STOP (terminated from the PC) 2026-10-06T23:09:34Z
  remotes/origin/run/q-i-0a7c9dc67e9e76433                   617108cca q-i-0a7c9dc67e9e76433 INTERRUPTED 2026-10-04T23:44:43Z
  remotes/origin/run/q-i-0a7dc0e6bb61be3cd                   5c329da83 q-i-0a7dc0e6bb61be3cd INTERRUPTED 2026-10-07T14:32:34Z
  remotes/origin/run/q-i-0b0c025dfd6c29b6f                   23983c360 q-i-0b0c025dfd6c29b6f INTERRUPTED 2026-10-07T14:54:34Z
  remotes/origin/run/q-i-0b114a7bba51b7119                   16f55b8e1 q-i-0b114a7bba51b7119 STOP (terminated from the PC) 2026-10-07T06:24:22Z
  remotes/origin/run/q-i-0b32ff8e508641004                   eb9ad15e6 q-i-0b32ff8e508641004 STOP 2026-10-03T10:48:25Z
  remotes/origin/run/q-i-0b4fc385fabe06abe                   613f3dec4 q-i-0b4fc385fabe06abe INTERRUPTED 2026-10-02T06:14:54Z
  remotes/origin/run/q-i-0b6bb9accab7b5dee                   07f1e34b5 q-i-0b6bb9accab7b5dee FINI 2026-10-07T05:57:35Z
  remotes/origin/run/q-i-0b80bdbe2a5abb9db                   c29aa0435 q-i-0b80bdbe2a5abb9db STOP 2026-10-03T10:49:47Z
  remotes/origin/run/q-i-0b92386c498ef6897                   31e7952bc q-i-0b92386c498ef6897 INTERRUPTED 2026-10-02T19:07:35Z
  remotes/origin/run/q-i-0bae02ff4441515c7                   fba30c09b q-i-0bae02ff4441515c7 FINI 2026-10-07T06:11:09Z
  remotes/origin/run/q-i-0bbc42c024eec5d23                   fa13fbd48 q-i-0bbc42c024eec5d23 INTERRUPTED 2026-10-06T17:18:27Z
  remotes/origin/run/q-i-0c035891697df1496                   15f815a1d q-i-0c035891697df1496 STOP (terminated from the PC) 2026-10-06T22:40:17Z
  remotes/origin/run/q-i-0c0a95abbac3d8463                   2e08205ef q-i-0c0a95abbac3d8463 FINI 2026-10-07T18:34:00Z
  remotes/origin/run/q-i-0c0cff7478663dd82                   fdafcfdc4 q-i-0c0cff7478663dd82 INTERRUPTED 2026-10-01T23:09:47Z
  remotes/origin/run/q-i-0c211c967b25c5abf                   05ab5a08c q-i-0c211c967b25c5abf STOP (terminated from the PC) 2026-10-06T14:47:41Z
  remotes/origin/run/q-i-0c222a1c58f635aa0                   6cb612289 q-i-0c222a1c58f635aa0 EN_COURS 2026-10-07T14:53:35Z
  remotes/origin/run/q-i-0c22c16693c33b110                   6504bb19d q-i-0c22c16693c33b110 FINI 2026-10-07T01:46:01Z
  remotes/origin/run/q-i-0c4106bf92aa9841b                   8afd7bbc9 q-i-0c4106bf92aa9841b STOP (terminated from the PC) 2026-10-06T23:49:30Z
  remotes/origin/run/q-i-0c6821cc13d29f85f                   a06833475 q-i-0c6821cc13d29f85f EN_COURS 2026-10-07T17:42:03Z
  remotes/origin/run/q-i-0c7aabf9c43272942                   7ab095d2b q-i-0c7aabf9c43272942 INTERRUPTED 2026-10-02T19:06:06Z
  remotes/origin/run/q-i-0c80b705ff7d53100                   2b14b1aba q-i-0c80b705ff7d53100 INTERRUPTED 2026-10-02T10:33:22Z
  remotes/origin/run/q-i-0c823996cee1fbfa2                   dfe23ee2e q-i-0c823996cee1fbfa2 INTERRUPTED 2026-10-02T07:35:12Z
  remotes/origin/run/q-i-0c853d82346e693bb                   b33527c53 q-i-0c853d82346e693bb STOP (terminated from the PC) 2026-10-07T05:13:17Z
  remotes/origin/run/q-i-0cc72c6ccf899202f                   5d07c33be q-i-0cc72c6ccf899202f INTERRUPTED 2026-10-05T09:13:52Z
  remotes/origin/run/q-i-0d05279cd32b9fef8                   561eb9156 q-i-0d05279cd32b9fef8 STOP (terminated from the PC) 2026-10-06T23:47:04Z
  remotes/origin/run/q-i-0d5b739cfde206c5e                   8f78ac46c q-i-0d5b739cfde206c5e FINI 2026-10-07T05:50:00Z
  remotes/origin/run/q-i-0d7dba9a8fea98b66                   d3926ca80 q-i-0d7dba9a8fea98b66 FINI 2026-10-07T03:39:46Z
  remotes/origin/run/q-i-0d941684217fe9ffc                   f0518c334 q-i-0d941684217fe9ffc STOP 2026-10-05T10:06:14Z
  remotes/origin/run/q-i-0daead8125bef0456                   1ae110b03 q-i-0daead8125bef0456 INTERRUPTED 2026-10-02T20:01:37Z
  remotes/origin/run/q-i-0daf9c8e1e1f54c5d                   2ac50338f q-i-0daf9c8e1e1f54c5d INSTALLATION 2026-10-07T15:05:36Z
  remotes/origin/run/q-i-0dd6dbc530afb831d                   73ef1f8ef q-i-0dd6dbc530afb831d FINI 2026-10-07T14:38:49Z
  remotes/origin/run/q-i-0dd8a09a554760841                   bd82754da q-i-0dd8a09a554760841 FINI 2026-10-07T14:58:14Z
  remotes/origin/run/q-i-0dda6d8e31bdc250b                   2ab4ae3fd q-i-0dda6d8e31bdc250b INTERRUPTED 2026-10-02T06:14:34Z
  remotes/origin/run/q-i-0e0430be182d1b78d                   793136bc0 q-i-0e0430be182d1b78d EN_COURS 2026-10-07T18:15:04Z
  remotes/origin/run/q-i-0e2a36273e29f0765                   e003a3c44 q-i-0e2a36273e29f0765 FINI 2026-10-07T04:57:35Z
  remotes/origin/run/q-i-0e34e16a2ac224f9c                   30700a452 q-i-0e34e16a2ac224f9c STOP CALIB 2026-10-03T03:23:30Z
  remotes/origin/run/q-i-0e3aa8e044356d325                   74f72f7fd q-i-0e3aa8e044356d325 FINI 2026-10-06T18:00:39Z
  remotes/origin/run/q-i-0e57eb9523cf5327c                   fd431649a q-i-0e57eb9523cf5327c INTERRUPTED 2026-10-07T01:25:43Z
  remotes/origin/run/q-i-0e96f254063ff8a35                   21b1114fd q-i-0e96f254063ff8a35 INTERRUPTED 2026-10-03T03:17:40Z
  remotes/origin/run/q-i-0ec3296d1c09b77da                   69ea0cae5 q-i-0ec3296d1c09b77da FINI 2026-10-07T04:05:58Z
  remotes/origin/run/q-i-0eed576952c30b1f5                   ccc96b8c3 q-i-0eed576952c30b1f5 EN_COURS 2026-10-07T15:01:17Z
  remotes/origin/run/q-i-0f06e472c8b3996e4                   b9b8610eb q-i-0f06e472c8b3996e4 FINI 2026-10-07T05:19:04Z
  remotes/origin/run/q-i-0f15fe75be3a8c87c                   77f486f31 q-i-0f15fe75be3a8c87c STOP (terminated from the PC) 2026-10-06T23:49:30Z
  remotes/origin/run/q-i-0f24682d95b245093                   4bf1fe2a5 q-i-0f24682d95b245093 FINI 2026-10-07T20:23:59Z
  remotes/origin/run/q-i-0f2b25fab00022eeb                   fc52bb8ee q-i-0f2b25fab00022eeb INTERRUPTED 2026-10-06T14:11:32Z
  remotes/origin/run/q-i-0f326fd9a585cbffe                   3b79b3b3b q-i-0f326fd9a585cbffe FINI 2026-10-07T05:36:27Z
  remotes/origin/run/q-i-0f3beb159e48bf3ae                   b984d0c7f q-i-0f3beb159e48bf3ae INTERRUPTED 2026-10-01T22:08:47Z
  remotes/origin/run/q-i-0f425e1b8555e34e6                   33dbb2477 q-i-0f425e1b8555e34e6 FINI 2026-10-07T05:25:45Z
  remotes/origin/run/q-i-0f665dd8b81803ce6                   521628ebf q-i-0f665dd8b81803ce6 INTERRUPTED 2026-10-01T23:09:54Z
  remotes/origin/run/q-i-0f6752b875bdd5220                   0ca882792 q-i-0f6752b875bdd5220 INSTALLATION 2026-10-07T18:15:55Z
  remotes/origin/run/q-i-0f869edb213034d9f                   a786c20ee q-i-0f869edb213034d9f FINI 2026-10-07T14:56:10Z
  remotes/origin/run/q-i-0f893510291059446                   9bd14bcb7 q-i-0f893510291059446 INTERRUPTED 2026-10-01T22:18:46Z
  remotes/origin/run/q-i-0f9b88829406a7ab3                   d16ee8dce q-i-0f9b88829406a7ab3 INTERRUPTED 2026-10-06T14:30:43Z
  remotes/origin/run/q-i-0fa10cb052a603b99                   2915ec487 q-i-0fa10cb052a603b99 INTERRUPTED 2026-10-01T23:09:53Z
  remotes/origin/run/q-i-0fa91a45f074cf15e                   9ace2bf4e q-i-0fa91a45f074cf15e EN_COURS 2026-10-07T14:24:08Z
  remotes/origin/run/q-i-0fabc2411a6580171                   2babc61ef q-i-0fabc2411a6580171 STOP (terminated from the PC) 2026-10-06T22:40:17Z
  remotes/origin/run/q-i-0fd371fb0c83bce5d                   300d75785 q-i-0fd371fb0c83bce5d FINI 2026-10-07T06:04:41Z
  remotes/origin/run/q-i-0fd53514a6dcce992                   edf63ac67 q-i-0fd53514a6dcce992 EN_COURS 2026-10-07T14:54:00Z
  remotes/origin/run/q-i-0ffabb9fb91879e62                   59ae5768b q-i-0ffabb9fb91879e62 FINI 2026-10-07T14:43:09Z
  remotes/origin/run/qci-a                                   9b267338e qci-a EN_COURS 2026-10-01T19:24:07Z
  remotes/origin/run/qci-b                                   7deb2d731 qci-b EN_COURS 2026-10-01T19:23:34Z
  remotes/origin/run/qci-c                                   a03e1aaf1 qci-c STOP 2026-10-01T19:24:47Z
  remotes/origin/run/qci-d                                   cfc48ec4e qci-d STOP 2026-10-01T19:24:53Z
  remotes/origin/run/qci-e                                   f4bb57626 qci-e DRAINED 2026-10-01T19:24:58Z
  remotes/origin/run/qci-v10a                                2652cdd08 qci-v10a FINI 2026-10-06T23:45:59Z
  remotes/origin/run/qci-v10d                                6602c7765 qci-v10d FINI 2026-10-07T12:48:51Z
  remotes/origin/run/qci-v2a                                 c2af9cad7 qci-v2a FINI 2026-10-01T22:23:02Z
  remotes/origin/run/qci-v2b                                 9dee2e94a qci-v2b STOP 2026-10-01T22:23:09Z
  remotes/origin/run/qci-v3a                                 06e1ec2a1 qci-v3a FINI 2026-10-01T23:22:03Z
  remotes/origin/run/qci-v4a                                 f9477ab86 qci-v4a FINI 2026-10-02T00:20:54Z
  remotes/origin/run/qci-v5a                                 ed55d2ebd qci-v5a FINI 2026-10-02T04:42:55Z
  remotes/origin/run/qci-v6a                                 0f9697b62 qci-v6a FINI 2026-10-02T08:39:52Z
  remotes/origin/run/qci-v7a                                 7ac1f1054 qci-v7a FINI 2026-10-02T10:22:28Z
  remotes/origin/run/qci-v8a                                 ebc1f1909 qci-v8a FINI 2026-10-02T16:07:39Z
  remotes/origin/run/qci-v9a                                 ca19307f4 qci-v9a FINI 2026-10-03T14:35:03Z
  remotes/origin/run/slice-19                                507071949 slice-19 EN_COURS 2026-09-30T05:15:24Z
  remotes/origin/run/slice-20                                9ea06c1b8 slice-20 EN_COURS 2026-09-30T05:05:44Z
  remotes/origin/run/slice-21                                3f9097fa2 slice-21 EN_COURS 2026-09-30T05:05:31Z
  remotes/origin/run/slice-22                                fc8d8b3a9 slice-22 EN_COURS 2026-09-30T05:15:41Z
  remotes/origin/run/slice-23                                6b2e23759 slice-23 EN_COURS 2026-09-30T05:15:46Z
  remotes/origin/run/slice-24                                d66eb7447 slice-24 EN_COURS 2026-09-30T05:15:49Z
  remotes/origin/run/slice-25                                816c1ab44 slice-25 EN_COURS 2026-09-30T05:05:51Z
  remotes/origin/run/slice-26                                7c1307a2f slice-26 EN_COURS 2026-09-30T05:05:54Z
  remotes/origin/run/slice-27                                f6a0f0975 slice-27 EN_COURS 2026-09-30T05:06:03Z
  remotes/origin/run/slice-28                                cb6e302fd slice-28 EN_COURS 2026-09-29T22:36:52Z
  remotes/origin/run/slice-29                                2785b32d9 slice-29 EN_COURS 2026-09-29T22:37:05Z
  remotes/origin/run/slice-30                                c1b74a4f8 slice-30 EN_COURS 2026-09-29T22:27:13Z
  remotes/origin/run/slice-31                                88f85d8c8 slice-31 EN_COURS 2026-09-29T22:17:16Z
  remotes/origin/run/slice-32                                0de1cfac8 slice-32 EN_COURS 2026-09-29T23:17:33Z
  remotes/origin/run/slice-33                                dfc9c8091 slice-33 EN_COURS 2026-09-29T22:47:38Z
  remotes/origin/run/slice-34                                f530032ba slice-34 EN_COURS 2026-09-29T22:07:37Z
  remotes/origin/run/slice-35                                b4a2759ea slice-35 EN_COURS 2026-09-29T22:27:50Z
  remotes/origin/run/slice-36                                c6bd067e4 slice-36 EN_COURS 2026-09-29T22:07:54Z
  remotes/origin/run/slice-37                                53f9b804a slice-37 EN_COURS 2026-09-29T22:48:58Z
  remotes/origin/run/slice-38                                4b3903fd4 slice-38 EN_COURS 2026-09-29T23:49:46Z
  remotes/origin/run/slice-39                                bc6f5cb52 slice-39 EN_COURS 2026-09-29T22:30:23Z
  remotes/origin/run/slice-40                                b6ca2d70a slice-40 EN_COURS 2026-09-29T22:21:08Z
  remotes/origin/run/slice-41                                0ada431cb slice-41 EN_COURS 2026-09-29T22:21:36Z
  remotes/origin/run/slice-42                                4db1b43a0 slice-42 EN_COURS 2026-09-29T22:32:15Z
  remotes/origin/run/slice-43                                56e8409de slice-43 EN_COURS 2026-09-29T22:32:43Z
  remotes/origin/run/slice-44                                8abd3c775 slice-44 EN_COURS 2026-09-29T22:23:15Z
  remotes/origin/run/toi-euc1-0                              c0cfca2a3 toi-euc1-0 EN_COURS 2026-09-30T05:08:02Z
  remotes/origin/run/toi-eun1-0                              5fbe58af8 toi-eun1-0 EN_COURS 2026-09-30T05:06:03Z
  remotes/origin/run/toi-euw2-0                              25b19d590 toi-euw2-0 EN_COURS 2026-09-29T23:31:00Z
  remotes/origin/run/toi-use1-0                              0aa183235 toi-use1-0 EN_COURS 2026-09-29T22:15:31Z
  remotes/origin/run/toi-use2-0                              86bd90a57 toi-use2-0 EN_COURS 2026-09-29T23:09:30Z
  remotes/origin/run/toi-usw2-0                              cfc76e6a4 toi-usw2-0 EN_COURS 2026-09-29T21:56:09Z
  remotes/origin/tail-runner                                 2912d9d65 Tail runner: heavy one-y1 stream jobs cut over all the cores of a machine (q/par_consumer.py, q/qtail.py, switch in qmachine.sh)
  remotes/origin/tmp/push-test-laptop                        9d1627d84 ypairs_c2: YP_WORKERS > 1 deals the loop over y1 to forked processes (same statements, output in the same order); default unchanged
  remotes/origin/v10                                         87672fb16 v10: Y=13 pair filter (min L* >= 9/7), FD_MIN97=1 in env_exact; agent parses two-digit package versions; rehearsal workflow
  remotes/origin/v10-fetch-retry                             c4a9b32d7 qagent: retry a failed queue fetch instead of killing the machine
  remotes/origin/v2                                          d89e731fb v2 package fix: exclude run_jobs' RESULTATS_slice tarball from the MANIFEST (the CI rehearsal caught a manifest refusal after calibration)
  remotes/origin/v3                                          e30cf9abb v3 fix: o24_run_fast creates data/finishC/o24_dfs before saving (the v3 rehearsal caught the O24 job failing at save time)
  remotes/origin/v4                                          af6bc8a3d v4: package v4 (golay_pairs jobs for 002, 004, 010 from golay_gen.py; golay job v4 with block loading and INCOMPLETE retry)
  remotes/origin/v5                                          f72cdb34a v5 rebuild: the retry-path calibration compares verdicts only (node counts are CPU-dependent)
  remotes/origin/v6                                          033eaad20 v6: stream node limit 4e9 (run_jobs) and job kind resolve (the 28 unresolved INCOMPLETE pairs of 037, no node limit)
  remotes/origin/v7                                          373530486 v7: spare sub-jobs (stream x8, golay x10/x8) so that slow jobs can be split on demand; only jobs.json differs from v6
  remotes/origin/v8                                          4fc2cf7d5 v8: resolve lists of 023, 024, 026, 028 (118 INCOMPLETE K=0 pairs of the v2 stream, one per job); only the lists and jobs.json differ from v7
  remotes/origin/v9                                          baf5c3f93 v9: fine jobs (one y1 per stream job; Golay 001 n=1700, 002 n=23040) for every open lattice; only jobs.json differs from v8
```

Status (first80 lines; full in JSON):
```

```

## C:\Users\bfhdh\Desktop\Recherche_Conway\c2_experimental\external_c1

Remotes:
```
origin	https://github.com/amazing-source/conway99-c1.git (fetch)
origin	https://github.com/amazing-source/conway99-c1.git (push)
```

Branches:
```
* main                37842fc [origin/main] fullblock_symmetry.py: symmetry groups of the 4 full-block local systems (G = Stab_B6(m): orders 12 / 32 / 72 / 384 for 6-cycle / 2+4 / 3+3 / 2+2+2; the c+ <-> c- swap acts as pi in B6, nothing new), their actions on sat_local's indexing (60 far roots, 60 non-m pairs; data/fullblock_symmetry.json), and a sound lex-leader encoding X <=_lex X o g for all g on a prefix of roots (3-clause chain per position; unit-tested: exactly the orbit lex-minima satisfy it, 0/600 mismatches); a first-choice chain is also provided but useless for the 6-cycle (free action on far roots)
  remotes/origin/HEAD -> origin/main
  remotes/origin/main 37842fc fullblock_symmetry.py: symmetry groups of the 4 full-block local systems (G = Stab_B6(m): orders 12 / 32 / 72 / 384 for 6-cycle / 2+4 / 3+3 / 2+2+2; the c+ <-> c- swap acts as pi in B6, nothing new), their actions on sat_local's indexing (60 far roots, 60 non-m pairs; data/fullblock_symmetry.json), and a sound lex-leader encoding X <=_lex X o g for all g on a prefix of roots (3-clause chain per position; unit-tested: exactly the orbit lex-minima satisfy it, 0/600 mismatches); a first-choice chain is also provided but useless for the 6-cycle (free action on far roots)
```

Status (first80 lines; full in JSON):
```

```

## C:\Users\bfhdh\Desktop\Recherche_Conway\c2_experimental\external_c3\conway99-c3

Remotes:
```
origin	https://github.com/amazing-source/conway99-c3.git (fetch)
origin	https://github.com/amazing-source/conway99-c3.git (push)
```

Branches:
```
* main                8e95aa4 [origin/main] Resume from a fresh clone: regenerate cube base CNFs and verify their SHA-256
  remotes/origin/HEAD -> origin/main
  remotes/origin/main 8e95aa4 Resume from a fresh clone: regenerate cube base CNFs and verify their SHA-256
```

Status (first80 lines; full in JSON):
```

```

## C:\Users\bfhdh\Desktop\Recherche_Conway\c2_experimental\external_c3\conway99-c3-experimental

Remotes:
```
origin	https://github.com/amazing-source/conway99-c3-experimental.git (fetch)
origin	https://github.com/amazing-source/conway99-c3-experimental.git (push)
```

Branches:
```
* main                af18b15 [origin/main] PDF : contexte complet, corollaire 8 (|Aut| <= 2), vérification formelle, bibliographie vérifiée
  remotes/origin/HEAD -> origin/main
  remotes/origin/main af18b15 PDF : contexte complet, corollaire 8 (|Aut| <= 2), vérification formelle, bibliographie vérifiée
```

Status (first80 lines; full in JSON):
```

```

## C:\Users\bfhdh\Desktop\Recherche_Conway\c2_experimental\external_structures

Remotes:
```
origin	https://github.com/amazing-source/conway99-structures-lab.git (fetch)
origin	https://github.com/amazing-source/conway99-structures-lab.git (push)
```

Branches:
```
* master                e6484e3 [origin/master] sat_local.py --symbreak [--prefix=k]: C1's lex-leader clauses (full-block groups of order 12/32/72/384; reads conway99-c1 code/fullblock_symmetry.py); 2+2+2 still unknown at 285 s locally; random block types: mixed 2/2 iota die at step 2, free stars harder (step 1 unknown 2/3 at 60 s)
  remotes/origin/HEAD   -> origin/master
  remotes/origin/master e6484e3 sat_local.py --symbreak [--prefix=k]: C1's lex-leader clauses (full-block groups of order 12/32/72/384; reads conway99-c1 code/fullblock_symmetry.py); 2+2+2 still unknown at 285 s locally; random block types: mixed 2/2 iota die at step 2, free stars harder (step 1 unknown 2/3 at 60 s)
```

Status (first80 lines; full in JSON):
```
?? ad/__pycache__/
```

## C:\Users\bfhdh\Desktop\Recherche_Conway\c2_experimental\qci_wt

Remotes:
```
origin	https://github.com/amazing-source/conway99-c2-aws.git (fetch) [blob:none]
origin	https://github.com/amazing-source/conway99-c2-aws.git (push)
```

Branches:
```
+ codex/t20-dual-hand                                        76ba508a9 (C:/Users/bfhdh/Desktop/Recherche_Conway/t20-codex) Clarify limits of Borcherds table transcription attribution
  lab-records-2026-10-07                                     fa5a181cd [origin/lab-records-2026-10-07: ahead 2, behind 2] Lab PC records: tracker at 156 of 156 (conversion of 2026-10-07 17:47 UTC), acceptance record of T18 and T20, final reports, tracker backup at 143
+ master                                                     3f0a07921 (C:/Users/bfhdh/Desktop/Recherche_Conway/c2_experimental/aws_repo) [origin/master: ahead 349, behind 443] Paper table: root types with equal components grouped, asserted equal to the exact recomputation for all 156 lattices; caption no longer attributes an unchecked transcription to Borcherds
* queue-ci                                                   1c0379166 [origin/queue-ci: ahead 7, behind 6] queue-ci: reset for the v10 rehearsal (same four jobs as v9)
  v10                                                        579766a2b v10: Y=13 pair filter (min L* >= 9/7), FD_MIN97=1 in env_exact; agent parses two-digit package versions; rehearsal workflow
  v2                                                         1e80b0991 [origin/v2: ahead 18, behind 18] v2 package fix: exclude run_jobs' RESULTATS_slice tarball from the MANIFEST (the CI rehearsal caught a manifest refusal after calibration)
  v3                                                         c022c8696 v3 fix: o24_run_fast creates data/finishC/o24_dfs before saving (the v3 rehearsal caught the O24 job failing at save time)
  v4                                                         10be103e4 v4: package v4 (golay_pairs jobs for 002, 004, 010 from golay_gen.py; golay job v4 with block loading and INCOMPLETE retry)
  v5                                                         97e9e1f7a v5 rebuild: the retry-path calibration compares verdicts only (node counts are CPU-dependent)
  v6                                                         75dfc6bbf v6: stream node limit 4e9 (run_jobs) and job kind resolve (the 28 unresolved INCOMPLETE pairs of 037, no node limit)
  v7                                                         d0933ecc4 v7: spare sub-jobs (stream x8, golay x10/x8) so that slow jobs can be split on demand; only jobs.json differs from v6
  v8                                                         b58eb1a09 v8: resolve lists of 023, 024, 026, 028 (118 INCOMPLETE K=0 pairs of the v2 stream, one per job); only the lists and jobs.json differ from v7
  v9                                                         5b1ea6c96 v9: fine jobs (one y1 per stream job; Golay 001 n=1700, 002 n=23040) for every open lattice; only jobs.json differs from v8
  remotes/origin/HEAD                                        -> origin/master
  remotes/origin/agent-backlog                               72e4bdade qagent: a refused queue transaction is no longer fatal (events kept for the next cycle); retries re-read the queue branch only; Q_LOOKAHEAD (local backlog of claimed jobs) and Q_SYNC_MIN (minimum interval between queue transactions). Defaults unchanged. Not yet rehearsed.
  remotes/origin/defer-mode                                  e03125329 HANDOFF section 16: deferral mode deployed (design, validation, measured coverage, fleet, lemma status)
  remotes/origin/defer-n4                                    d4ff4aa5e Deferral: norm-4 witnesses of T20 (Q_DEFER_N4=1): a pair with x of norm 4 and |(x,y1)| = |(x,y2)| = 3 (E = 10) is deferred with its own verdict and index list. Not yet rehearsed.
  remotes/origin/defer-quick                                 b263f243f Deferral, quick variant (Q_DEFER_NODES=0): a lemma-covered pair that passes the engine's two immediate tests is deferred without calling the engine's search (set-up was 0.3 s per pair, 70 % of a deferral job). Not yet validated.
  remotes/origin/lab-records-2026-10-07                      1ee9115c7 Lab PC records: tracker at 156 of 156 (conversion of 2026-10-07 17:47 UTC), acceptance record of T18 and T20, final reports, tracker backup at 143
  remotes/origin/lemma-archive/t20_n3_routeB                 bf5a0e33f Raw outputs of T20 Computation 9.29 (case I, n_3 = 2, route B): stage 1, stage 2, second program
  remotes/origin/lemma-run/selftest-i-0dee8516208b24d42      a15efe89a lemma run selftest on i-0dee8516208b24d42: FINISHED exit=0
  remotes/origin/lemma-run/t20_I1_340-i-019e86d399c17954f    95a4e0ce5 lemma run t20_I1_340 on i-019e86d399c17954f: FINISHED exit=0
  remotes/origin/lemma-run/t20_I_rest-i-02f356c70da99d700    b933f2f09 lemma run t20_I_rest on i-02f356c70da99d700: FINISHED exit=0
  remotes/origin/lemma-run/t20_Iv_A-i-0390fd53333c148ad      5bbdbc0ad lemma run t20_Iv_A on i-0390fd53333c148ad: INSTALLING
  remotes/origin/lemma-run/t20_Iv_B-i-0a03ce79bff09fa5d      7d8c0b997 lemma run t20_Iv_B on i-0a03ce79bff09fa5d: FINISHED exit=0
  remotes/origin/lemma-run/t20_Iv_C-i-092f5550d84f61e09      014b68258 lemma run t20_Iv_C on i-092f5550d84f61e09: FINISHED exit=0
  remotes/origin/lemma-run/t20_Iv_D-i-09169834049067883      12a885868 lemma run t20_Iv_D on i-09169834049067883: FINISHED exit=0
  remotes/origin/lemma-run/t20_Iv_E-i-0cd9427b48ee5704e      c6a3d9309 lemma run t20_Iv_E on i-0cd9427b48ee5704e: RUNNING
  remotes/origin/lemma-run/t20_Iv_F-i-0c5414832a6ac4ff5      0e2818ace lemma run t20_Iv_F on i-0c5414832a6ac4ff5: RUNNING
  remotes/origin/lemma-run/t20_Iv_G-i-05703a74fbb027423      e7d9c3caa lemma run t20_Iv_G on i-05703a74fbb027423: FINISHED exit=0
  remotes/origin/lemma-run/t20_Iv_H-i-004334efafb6ceb56      e5bd9b524 lemma run t20_Iv_H on i-004334efafb6ceb56: FINISHED exit=0
  remotes/origin/lemma-run/t20_Iv_I-i-032b7d25d335204f8      fa9934d59 lemma run t20_Iv_I on i-032b7d25d335204f8: FINISHED exit=0
  remotes/origin/lemma-run/t20_Iv_J-i-038ea54927e5a01c4      33bbe996e lemma run t20_Iv_J on i-038ea54927e5a01c4: FINISHED exit=0
  remotes/origin/lemma-run/t20_n3-i-04bb3ac564f658b79        4d1897bdd lemma run t20_n3 on i-04bb3ac564f658b79: RUNNING
  remotes/origin/lemma-run/t20_n3-i-0b8ae938c1fc89c62        df13c1d5f lemma run t20_n3 on i-0b8ae938c1fc89c62: RUNNING
  remotes/origin/lemma-run/t20_n3_sample-i-0cefd01aef8eade8a 0a4498e16 lemma run t20_n3_sample on i-0cefd01aef8eade8a: RUNNING
  remotes/origin/master                                      60fa90e40 Mandate C: the 72 star-less verdicts confirmed by exhaustive enumeration without solver (72 of 72)
  remotes/origin/queue                                       f134ddf44 control: credit_usd=13.76
  remotes/origin/queue-ci                                    93a85f547 qci-v10a done:1
  remotes/origin/queue-cid                                   5a8f10f44 qci-v10d done:1
  remotes/origin/run/frere-euc1-0                            51ad50203 frere-euc1-0 EN_COURS 2026-09-30T05:07:46Z
  remotes/origin/run/frere-eun1-0                            7e016bee9 frere-eun1-0 EN_COURS 2026-09-30T05:05:23Z
  remotes/origin/run/frere-euw2-0                            fc487ecad frere-euw2-0 EN_COURS 2026-09-30T05:11:29Z
  remotes/origin/run/frere-use1-0                            be7391006 frere-use1-0 EN_COURS 2026-09-29T22:03:09Z
  remotes/origin/run/frere-use2-0                            51b49b4ec frere-use2-0 EN_COURS 2026-09-29T23:08:32Z
  remotes/origin/run/frere-usw2-0                            97521504b frere-usw2-0 EN_COURS 2026-09-29T21:59:53Z
  remotes/origin/run/pere-euc1-0                             c46b5efa1 pere-euc1-0 EN_COURS 2026-09-30T05:07:54Z
  remotes/origin/run/pere-eun1-0                             87d9ec320 pere-eun1-0 EN_COURS 2026-09-30T05:05:53Z
  remotes/origin/run/pere-euw2-0                             9d100e6cb pere-euw2-0 EN_COURS 2026-09-30T05:11:35Z
  remotes/origin/run/pere-use1-0                             3f6bab4cb pere-use1-0 EN_COURS 2026-09-29T22:08:48Z
  remotes/origin/run/pere-use2-0                             5c5c39b77 pere-use2-0 EN_COURS 2026-09-29T23:15:03Z
  remotes/origin/run/pere-usw2-0                             68ee25c7a pere-usw2-0 EN_COURS 2026-09-29T22:00:13Z
  remotes/origin/run/q-i-0007aedf88590282f                   79bdcf2a5 q-i-0007aedf88590282f INTERRUPTED 2026-10-07T14:32:33Z
  remotes/origin/run/q-i-003d278c405e099f8                   11c005729 q-i-003d278c405e099f8 EN_COURS 2026-10-04T14:37:40Z
  remotes/origin/run/q-i-0058b87765fd902ac                   873f0e2ef q-i-0058b87765fd902ac FINI 2026-10-07T18:29:15Z
  remotes/origin/run/q-i-00602e633195b38d8                   d4ef142d8 q-i-00602e633195b38d8 FINI 2026-10-07T05:47:41Z
  remotes/origin/run/q-i-008a374f92faec021                   1f1cefd97 q-i-008a374f92faec021 ERREUR AGENT 2026-10-06T13:00:22Z
  remotes/origin/run/q-i-008bbb215228c6869                   e6e95aa6d q-i-008bbb215228c6869 STOP (terminated from the PC) 2026-10-06T23:47:04Z
  remotes/origin/run/q-i-00925e8996c5d49fc                   659cde539 q-i-00925e8996c5d49fc FINI 2026-10-07T05:32:55Z
  remotes/origin/run/q-i-009b8ce54f3a78709                   b313e1baf q-i-009b8ce54f3a78709 STOP (terminated from the PC) 2026-10-06T14:47:41Z
  remotes/origin/run/q-i-00a0ab97a6a8099fd                   a15f705c6 q-i-00a0ab97a6a8099fd STOP (terminated from the PC) 2026-10-07T12:49:30Z
  remotes/origin/run/q-i-00a7b5e21909a98d1                   e551926e1 q-i-00a7b5e21909a98d1 FINI 2026-10-07T15:19:39Z
  remotes/origin/run/q-i-01028dcab733e510e                   f44d89d2a q-i-01028dcab733e510e STOP (terminated from the PC) 2026-10-06T23:47:04Z
  remotes/origin/run/q-i-010bcc0075d83a855                   68af346bd q-i-010bcc0075d83a855 INTERRUPTED 2026-10-07T01:34:04Z
  remotes/origin/run/q-i-011cdbf73eb1c5524                   3e83af55c q-i-011cdbf73eb1c5524 FINI 2026-10-07T18:29:07Z
  remotes/origin/run/q-i-011dce74cd612fc52                   ba04654dc q-i-011dce74cd612fc52 FINI 2026-10-07T17:43:25Z
  remotes/origin/run/q-i-0126bbe8cfe58cfdd                   683c924b0 q-i-0126bbe8cfe58cfdd STOP (terminated from the PC) 2026-10-06T23:47:04Z
  remotes/origin/run/q-i-01342f629eff35dc3                   37680b3fb q-i-01342f629eff35dc3 FINI 2026-10-07T14:53:27Z
  remotes/origin/run/q-i-0149028a4e29f2bfe                   b238ac10d q-i-0149028a4e29f2bfe INTERRUPTED 2026-10-06T17:03:02Z
  remotes/origin/run/q-i-014f982e79fc44389                   bb7dc1ec3 q-i-014f982e79fc44389 EN_COURS 2026-10-07T14:53:36Z
  remotes/origin/run/q-i-0157fafabb9e40145                   4b3569d03 q-i-0157fafabb9e40145 STOP (terminated from the PC) 2026-10-06T23:49:30Z
  remotes/origin/run/q-i-01597373ced95afb1                   45d264d09 q-i-01597373ced95afb1 STOP (terminated from the PC) 2026-10-06T22:11:01Z
  remotes/origin/run/q-i-0163b9385e47e4dfd                   4f49770cd q-i-0163b9385e47e4dfd INTERRUPTED 2026-10-06T15:57:29Z
  remotes/origin/run/q-i-0175d90b21760467a                   57958d77e q-i-0175d90b21760467a FINI 2026-10-07T05:42:24Z
  remotes/origin/run/q-i-01866477c48c3d7d8                   349eb4534 q-i-01866477c48c3d7d8 STOP 2026-10-03T10:49:29Z
  remotes/origin/run/q-i-01ad68b6cbef7c9c0                   ac3f47979 q-i-01ad68b6cbef7c9c0 FINI 2026-10-07T20:23:33Z
  remotes/origin/run/q-i-01c02b0a392fd4661                   e53580e94 q-i-01c02b0a392fd4661 INTERRUPTED 2026-10-07T14:47:42Z
  remotes/origin/run/q-i-01cba7ba0fb3204e4                   5ced3c513 q-i-01cba7ba0fb3204e4 EN_COURS 2026-10-07T14:24:31Z
  remotes/origin/run/q-i-01d993ebe8987ed6a                   e59894d32 q-i-01d993ebe8987ed6a FINI 2026-10-07T20:19:03Z
  remotes/origin/run/q-i-0201ab6c589d46854                   704557cbd q-i-0201ab6c589d46854 STOP 2026-10-05T10:06:25Z
  remotes/origin/run/q-i-0242e76bf23d90e2f                   090543bb7 q-i-0242e76bf23d90e2f FINI 2026-10-06T17:53:49Z
  remotes/origin/run/q-i-0243e91a6c62ae950                   ef15273f1 q-i-0243e91a6c62ae950 EN_COURS 2026-10-04T14:40:26Z
  remotes/origin/run/q-i-024b07e5fa9d980a5                   24d663d9b q-i-024b07e5fa9d980a5 FINI 2026-10-07T18:31:17Z
  remotes/origin/run/q-i-025be10f67c1fb32a                   8df33eaa0 q-i-025be10f67c1fb32a INTERRUPTED 2026-10-02T07:37:41Z
  remotes/origin/run/q-i-025ec33081e30e55a                   f8206a4a1 q-i-025ec33081e30e55a INTERRUPTED 2026-10-06T14:22:39Z
  remotes/origin/run/q-i-0264624104d7e9d74                   6113f7f61 q-i-0264624104d7e9d74 INTERRUPTED 2026-10-03T08:01:14Z
  remotes/origin/run/q-i-026b674ec4b914602                   6340d69cc q-i-026b674ec4b914602 INTERRUPTED 2026-10-07T13:31:35Z
  remotes/origin/run/q-i-026e2eda9e2b5dfdb                   ad1816860 q-i-026e2eda9e2b5dfdb EN_COURS 2026-10-07T14:22:12Z
  remotes/origin/run/q-i-028bed5a8e755ec78                   50fab57f8 q-i-028bed5a8e755ec78 STOP (terminated from the PC) 2026-10-06T23:09:34Z
  remotes/origin/run/q-i-029b7027bf533447b                   76a12c91f q-i-029b7027bf533447b STOP 2026-10-03T10:51:41Z
  remotes/origin/run/q-i-029f440141955366f                   e9a751796 q-i-029f440141955366f STOP (terminated from the PC) 2026-10-06T22:40:17Z
  remotes/origin/run/q-i-02a5f5b29477f6f99                   d52626f8a q-i-02a5f5b29477f6f99 INTERRUPTED 2026-10-03T10:14:09Z
  remotes/origin/run/q-i-02aa613ee361fbc10                   d70288ec2 q-i-02aa613ee361fbc10 EN_COURS 2026-10-07T16:13:23Z
  remotes/origin/run/q-i-02c22281be51a85b0                   cc92890c2 q-i-02c22281be51a85b0 INTERRUPTED 2026-10-06T14:37:25Z
  remotes/origin/run/q-i-02cb727a152a622e4                   78357c595 q-i-02cb727a152a622e4 FINI 2026-10-06T17:50:31Z
  remotes/origin/run/q-i-02f5e47e7fe6aba80                   e46d780a7 q-i-02f5e47e7fe6aba80 STOP (terminated from the PC) 2026-10-06T22:11:01Z
  remotes/origin/run/q-i-02fc30d4640fca3fa                   48e9250be q-i-02fc30d4640fca3fa STOP 2026-10-03T10:50:50Z
  remotes/origin/run/q-i-03008ed0607c0af47                   ae0442441 q-i-03008ed0607c0af47 STOP (terminated from the PC) 2026-10-06T23:49:30Z
  remotes/origin/run/q-i-031bd5d874fc9c8e8                   fa7586317 q-i-031bd5d874fc9c8e8 FINI 2026-10-07T01:39:06Z
  remotes/origin/run/q-i-03216e01aa27ec88d                   89694a93a q-i-03216e01aa27ec88d STOP (terminated from the PC) 2026-10-06T14:47:41Z
  remotes/origin/run/q-i-032ff3b5eda1ce09e                   0f3019a1b q-i-032ff3b5eda1ce09e EN_COURS 2026-10-04T14:38:20Z
  remotes/origin/run/q-i-033e48138746dbc88                   5f8844d65 q-i-033e48138746dbc88 STOP (terminated from the PC) 2026-10-07T05:13:17Z
  remotes/origin/run/q-i-035c2a86b163858c2                   0cb00d479 q-i-035c2a86b163858c2 INTERRUPTED 2026-10-02T20:01:43Z
  remotes/origin/run/q-i-036c5c29f417b3487                   e38632934 q-i-036c5c29f417b3487 INTERRUPTED 2026-10-04T04:55:46Z
  remotes/origin/run/q-i-0371888c776e26bbf                   ddc2e15c2 q-i-0371888c776e26bbf INSTALLATION 2026-10-07T17:04:19Z
  remotes/origin/run/q-i-03dc85e2a3417e606                   5758bee66 q-i-03dc85e2a3417e606 STOP (terminated from the PC) 2026-10-07T05:13:17Z
  remotes/origin/run/q-i-03e9fcedad48e9625                   6db84b0e4 q-i-03e9fcedad48e9625 INTERRUPTED 2026-10-04T06:34:46Z
  remotes/origin/run/q-i-03f2d86e1f691f955                   97b3bdea5 q-i-03f2d86e1f691f955 STOP 2026-10-03T10:47:56Z
  remotes/origin/run/q-i-03fc279ba375a421c                   c5f2f3b12 q-i-03fc279ba375a421c STOP (terminated from the PC) 2026-10-06T22:11:01Z
  remotes/origin/run/q-i-0475a297578983215                   8f0a66709 q-i-0475a297578983215 INTERRUPTED 2026-10-03T08:01:17Z
  remotes/origin/run/q-i-04979887a2789fb83                   225685ba3 q-i-04979887a2789fb83 STOP 2026-10-03T10:50:45Z
  remotes/origin/run/q-i-04a2424fac34284e8                   f2c0e0df9 q-i-04a2424fac34284e8 INTERRUPTED 2026-10-03T08:01:21Z
  remotes/origin/run/q-i-04af0d2c393f35d5c                   0889903e1 q-i-04af0d2c393f35d5c STOP 2026-10-02T02:16:18Z
  remotes/origin/run/q-i-04ba84a7d64b81116                   c93eea803 q-i-04ba84a7d64b81116 INTERRUPTED 2026-10-07T14:49:13Z
  remotes/origin/run/q-i-04c611bf415f81b02                   7958e6ab7 q-i-04c611bf415f81b02 INTERRUPTED 2026-10-02T20:12:17Z
  remotes/origin/run/q-i-04dcdc6392cd9fe1d                   836db717b q-i-04dcdc6392cd9fe1d EN_COURS 2026-10-07T04:37:31Z
  remotes/origin/run/q-i-04eeecb80a5c72755                   bacf58eb3 q-i-04eeecb80a5c72755 INTERRUPTED 2026-10-06T14:22:06Z
  remotes/origin/run/q-i-050146d35c06c0336                   2623e442b q-i-050146d35c06c0336 FINI 2026-10-07T03:08:39Z
  remotes/origin/run/q-i-0520c5d3f009c5a4a                   b65e67d44 q-i-0520c5d3f009c5a4a INTERRUPTED 2026-10-01T22:36:07Z
  remotes/origin/run/q-i-052249d51da1a1596                   9525e2b60 q-i-052249d51da1a1596 EN_COURS 2026-10-07T18:46:29Z
  remotes/origin/run/q-i-054379e6cd4f03332                   07094c71d q-i-054379e6cd4f03332 STOP (terminated from the PC) 2026-10-06T22:11:01Z
  remotes/origin/run/q-i-05e123fd3b6f34dc7                   7985b04cc q-i-05e123fd3b6f34dc7 FINI 2026-10-07T06:05:18Z
  remotes/origin/run/q-i-05e20a652a9b41e97                   9409eddc6 q-i-05e20a652a9b41e97 STOP (terminated from the PC) 2026-10-07T09:24:11Z
  remotes/origin/run/q-i-061c40f7fb049da5d                   ae509f775 q-i-061c40f7fb049da5d INTERRUPTED 2026-10-03T03:17:53Z
  remotes/origin/run/q-i-062d6f242375b1fe4                   460d4cfb7 q-i-062d6f242375b1fe4 INTERRUPTED 2026-10-02T19:05:37Z
  remotes/origin/run/q-i-0633e9c6510b7a07f                   3e3a3c342 q-i-0633e9c6510b7a07f STOP (terminated from the PC) 2026-10-06T23:47:04Z
  remotes/origin/run/q-i-064db7733386366ef                   eb9612fac q-i-064db7733386366ef INTERRUPTED 2026-10-06T16:36:38Z
  remotes/origin/run/q-i-0677b8b475388ce7e                   7ca81f383 q-i-0677b8b475388ce7e INTERRUPTED 2026-10-07T14:33:35Z
  remotes/origin/run/q-i-0677d76eeb19369f0                   9e61a122b q-i-0677d76eeb19369f0 INSTALLATION 2026-10-07T15:06:12Z
  remotes/origin/run/q-i-067c8886509d5f9ea                   0ceb919d9 q-i-067c8886509d5f9ea STOP (terminated from the PC) 2026-10-06T23:47:04Z
  remotes/origin/run/q-i-069823739875ec782                   a6144c94e q-i-069823739875ec782 ERREUR AGENT 2026-10-06T23:35:18Z
  remotes/origin/run/q-i-06a7607e4c50e49d5                   a764e4b4e q-i-06a7607e4c50e49d5 STOP (terminated from the PC) 2026-10-07T05:13:17Z
  remotes/origin/run/q-i-06aec8054a564a8e5                   0387e316c q-i-06aec8054a564a8e5 FINI 2026-10-07T06:13:17Z
  remotes/origin/run/q-i-06f59d4983625a388                   dba82d08b q-i-06f59d4983625a388 STOP (terminated from the PC) 2026-10-06T23:09:34Z
  remotes/origin/run/q-i-070065653a5f0df24                   d81f6738c q-i-070065653a5f0df24 INTERRUPTED 2026-10-07T01:47:04Z
  remotes/origin/run/q-i-0717750673326e465                   b5f2dc7ca q-i-0717750673326e465 STOP (terminated from the PC) 2026-10-06T23:47:04Z
  remotes/origin/run/q-i-07194a18450f2a06e                   a69f5d6e8 q-i-07194a18450f2a06e STOP (terminated from the PC) 2026-10-07T12:49:30Z
  remotes/origin/run/q-i-07366de1470e7648a                   c4bbea996 q-i-07366de1470e7648a STOP (terminated from the PC) 2026-10-07T06:24:22Z
  remotes/origin/run/q-i-0738a86689ab8fb74                   babe09ca8 q-i-0738a86689ab8fb74 STOP (terminated from the PC) 2026-10-06T14:47:41Z
  remotes/origin/run/q-i-0742677fb55fcd71a                   47d505eab q-i-0742677fb55fcd71a INTERRUPTED 2026-10-06T17:10:10Z
  remotes/origin/run/q-i-074808dad30139068                   a9f4ecc73 q-i-074808dad30139068 INTERRUPTED 2026-10-03T00:30:49Z
  remotes/origin/run/q-i-0759cbe1f271decac                   e047cadaa q-i-0759cbe1f271decac INTERRUPTED 2026-10-02T09:03:19Z
  remotes/origin/run/q-i-077230baffaf0b835                   d7059efa0 q-i-077230baffaf0b835 FINI 2026-10-07T06:17:37Z
  remotes/origin/run/q-i-0775d0ef0fc2b023a                   2b110c27f q-i-0775d0ef0fc2b023a INTERRUPTED 2026-10-06T17:13:15Z
  remotes/origin/run/q-i-077b44162d0b9c0b4                   461b3480d q-i-077b44162d0b9c0b4 INTERRUPTED 2026-10-06T21:16:28Z
  remotes/origin/run/q-i-078d5c153bfd2caa9                   eec46947b q-i-078d5c153bfd2caa9 STOP 2026-10-05T10:09:34Z
  remotes/origin/run/q-i-07959d1a6ef559a4c                   5296defba q-i-07959d1a6ef559a4c STOP 2026-10-02T02:16:37Z
  remotes/origin/run/q-i-07a70e4361d9b0c50                   ad7f3cf5c q-i-07a70e4361d9b0c50 STOP (terminated from the PC) 2026-10-07T05:13:17Z
  remotes/origin/run/q-i-07a9545ff43eb7971                   b4120e8b3 q-i-07a9545ff43eb7971 STOP (terminated from the PC) 2026-10-07T06:24:22Z
  remotes/origin/run/q-i-07b69e1205a8909d8                   890a57216 q-i-07b69e1205a8909d8 INTERRUPTED 2026-10-04T10:10:21Z
  remotes/origin/run/q-i-07bab8da962e7387a                   26521a256 q-i-07bab8da962e7387a EN_COURS 2026-10-04T14:38:58Z
  remotes/origin/run/q-i-07dafa59b6d6bb72a                   9a9b6ffc1 q-i-07dafa59b6d6bb72a EN_COURS 2026-10-07T15:30:35Z
  remotes/origin/run/q-i-07ed9a020e51d514e                   68fd48167 q-i-07ed9a020e51d514e STOP (terminated from the PC) 2026-10-06T23:47:04Z
  remotes/origin/run/q-i-07f2923eeb11cfe80                   fa63a3f01 q-i-07f2923eeb11cfe80 STOP (terminated from the PC) 2026-10-06T22:40:17Z
  remotes/origin/run/q-i-080e1d0be9807b4a2                   aa533c0ad q-i-080e1d0be9807b4a2 INTERRUPTED 2026-10-06T17:02:41Z
  remotes/origin/run/q-i-0820ff9ccb2543e33                   0fcb0723a q-i-0820ff9ccb2543e33 INTERRUPTED 2026-10-02T19:07:40Z
  remotes/origin/run/q-i-083a27a437f31bb9a                   48b57d53f q-i-083a27a437f31bb9a STOP (terminated from the PC) 2026-10-06T23:49:30Z
  remotes/origin/run/q-i-0842035457bba071a                   6e17bbe52 q-i-0842035457bba071a EN_COURS 2026-10-07T14:13:42Z
  remotes/origin/run/q-i-08471079f0542dd91                   97bc32e5a q-i-08471079f0542dd91 FINI 2026-10-07T14:49:27Z
  remotes/origin/run/q-i-084bd5ac37cffb8f8                   2dfa32e26 q-i-084bd5ac37cffb8f8 STOP (terminated from the PC) 2026-10-06T23:09:34Z
  remotes/origin/run/q-i-087b3674d1c8f0bb5                   0a82d08a2 q-i-087b3674d1c8f0bb5 FINI 2026-10-07T05:58:18Z
  remotes/origin/run/q-i-08e6786e978c36698                   cf361e4ac q-i-08e6786e978c36698 STOP (terminated from the PC) 2026-10-06T14:47:41Z
  remotes/origin/run/q-i-08ef09bd21655765e                   4fccffd51 q-i-08ef09bd21655765e EN_COURS 2026-10-07T14:54:36Z
  remotes/origin/run/q-i-08fb99c895223117a                   bd04357c5 q-i-08fb99c895223117a INTERRUPTED 2026-10-02T07:35:28Z
  remotes/origin/run/q-i-090db4b47b2d5ab04                   215383dd1 q-i-090db4b47b2d5ab04 STOP (terminated from the PC) 2026-10-06T23:47:04Z
  remotes/origin/run/q-i-0915313793048bc43                   ccab1dfd3 q-i-0915313793048bc43 EN_COURS 2026-10-07T15:17:12Z
  remotes/origin/run/q-i-0917fa5309b737275                   6e4dbde52 q-i-0917fa5309b737275 FINI 2026-10-07T15:45:04Z
  remotes/origin/run/q-i-09726ab19a395f27e                   1fa6ccbbc q-i-09726ab19a395f27e INTERRUPTED 2026-10-06T17:38:50Z
  remotes/origin/run/q-i-099093797d31d4403                   1009a25a0 q-i-099093797d31d4403 EN_COURS 2026-10-07T18:14:57Z
  remotes/origin/run/q-i-0997f7ef90634e8ec                   6b2e24b7c q-i-0997f7ef90634e8ec INTERRUPTED 2026-10-02T05:55:14Z
  remotes/origin/run/q-i-09b06647445f6a2cf                   6df679235 q-i-09b06647445f6a2cf ERREUR AGENT 2026-10-06T23:29:54Z
  remotes/origin/run/q-i-09b558abf286ca037                   c755ef55f q-i-09b558abf286ca037 INTERRUPTED 2026-10-06T23:52:53Z
  remotes/origin/run/q-i-09c13ec16873de889                   2de51e01c q-i-09c13ec16873de889 STOP (terminated from the PC) 2026-10-06T14:47:41Z
  remotes/origin/run/q-i-09c31398edb79ef34                   5bca941de q-i-09c31398edb79ef34 STOP (terminated from the PC) 2026-10-06T14:47:41Z
  remotes/origin/run/q-i-09e5adb0d653f40fa                   48981d7f3 q-i-09e5adb0d653f40fa FINI 2026-10-07T03:45:07Z
  remotes/origin/run/q-i-09ea743f3176922f4                   963ab5ca7 q-i-09ea743f3176922f4 INTERRUPTED 2026-10-02T20:01:35Z
  remotes/origin/run/q-i-09ee6f02570710dff                   ee5053e5d q-i-09ee6f02570710dff INTERRUPTED 2026-10-02T17:07:39Z
  remotes/origin/run/q-i-09ef67e96d2352cfb                   623fb0f56 q-i-09ef67e96d2352cfb FINI 2026-10-07T05:48:04Z
  remotes/origin/run/q-i-0a075cb17c06082cc                   a1a909910 q-i-0a075cb17c06082cc EN_COURS 2026-10-07T15:03:44Z
  remotes/origin/run/q-i-0a270ba19d9869f80                   abf0e7b27 q-i-0a270ba19d9869f80 INTERRUPTED 2026-10-03T08:01:11Z
  remotes/origin/run/q-i-0a2d32e20518d811a                   d20690933 q-i-0a2d32e20518d811a STOP (terminated from the PC) 2026-10-06T23:47:04Z
  remotes/origin/run/q-i-0a2f259889b0c0e5a                   d9213892b q-i-0a2f259889b0c0e5a STOP (terminated from the PC) 2026-10-06T14:47:41Z
  remotes/origin/run/q-i-0a3fa380d1f25690d                   9438d6c55 q-i-0a3fa380d1f25690d EN_COURS 2026-10-07T18:15:16Z
  remotes/origin/run/q-i-0a4ce7e951acd259e                   4ad9bb6da q-i-0a4ce7e951acd259e STOP (terminated from the PC) 2026-10-06T23:09:34Z
  remotes/origin/run/q-i-0a53459bb549dca86                   5e60815a1 q-i-0a53459bb549dca86 STOP (terminated from the PC) 2026-10-07T06:24:22Z
  remotes/origin/run/q-i-0a5e721fef6a7ac8d                   305430761 q-i-0a5e721fef6a7ac8d FINI 2026-10-07T04:38:03Z
  remotes/origin/run/q-i-0a6ff036888ae8447                   261af52df q-i-0a6ff036888ae8447 FINI 2026-10-07T06:24:41Z
  remotes/origin/run/q-i-0a772da7196ebb00a                   da4b39f9b q-i-0a772da7196ebb00a STOP (terminated from the PC) 2026-10-06T23:09:34Z
  remotes/origin/run/q-i-0a7c9dc67e9e76433                   617108cca q-i-0a7c9dc67e9e76433 INTERRUPTED 2026-10-04T23:44:43Z
  remotes/origin/run/q-i-0a7dc0e6bb61be3cd                   5c329da83 q-i-0a7dc0e6bb61be3cd INTERRUPTED 2026-10-07T14:32:34Z
  remotes/origin/run/q-i-0b0c025dfd6c29b6f                   23983c360 q-i-0b0c025dfd6c29b6f INTERRUPTED 2026-10-07T14:54:34Z
  remotes/origin/run/q-i-0b114a7bba51b7119                   16f55b8e1 q-i-0b114a7bba51b7119 STOP (terminated from the PC) 2026-10-07T06:24:22Z
  remotes/origin/run/q-i-0b32ff8e508641004                   eb9ad15e6 q-i-0b32ff8e508641004 STOP 2026-10-03T10:48:25Z
  remotes/origin/run/q-i-0b4fc385fabe06abe                   613f3dec4 q-i-0b4fc385fabe06abe INTERRUPTED 2026-10-02T06:14:54Z
  remotes/origin/run/q-i-0b6bb9accab7b5dee                   07f1e34b5 q-i-0b6bb9accab7b5dee FINI 2026-10-07T05:57:35Z
  remotes/origin/run/q-i-0b80bdbe2a5abb9db                   c29aa0435 q-i-0b80bdbe2a5abb9db STOP 2026-10-03T10:49:47Z
  remotes/origin/run/q-i-0b92386c498ef6897                   31e7952bc q-i-0b92386c498ef6897 INTERRUPTED 2026-10-02T19:07:35Z
  remotes/origin/run/q-i-0bae02ff4441515c7                   fba30c09b q-i-0bae02ff4441515c7 FINI 2026-10-07T06:11:09Z
  remotes/origin/run/q-i-0bbc42c024eec5d23                   fa13fbd48 q-i-0bbc42c024eec5d23 INTERRUPTED 2026-10-06T17:18:27Z
  remotes/origin/run/q-i-0c035891697df1496                   15f815a1d q-i-0c035891697df1496 STOP (terminated from the PC) 2026-10-06T22:40:17Z
  remotes/origin/run/q-i-0c0a95abbac3d8463                   2e08205ef q-i-0c0a95abbac3d8463 FINI 2026-10-07T18:34:00Z
  remotes/origin/run/q-i-0c0cff7478663dd82                   fdafcfdc4 q-i-0c0cff7478663dd82 INTERRUPTED 2026-10-01T23:09:47Z
  remotes/origin/run/q-i-0c211c967b25c5abf                   05ab5a08c q-i-0c211c967b25c5abf STOP (terminated from the PC) 2026-10-06T14:47:41Z
  remotes/origin/run/q-i-0c222a1c58f635aa0                   6cb612289 q-i-0c222a1c58f635aa0 EN_COURS 2026-10-07T14:53:35Z
  remotes/origin/run/q-i-0c22c16693c33b110                   6504bb19d q-i-0c22c16693c33b110 FINI 2026-10-07T01:46:01Z
  remotes/origin/run/q-i-0c4106bf92aa9841b                   8afd7bbc9 q-i-0c4106bf92aa9841b STOP (terminated from the PC) 2026-10-06T23:49:30Z
  remotes/origin/run/q-i-0c6821cc13d29f85f                   a06833475 q-i-0c6821cc13d29f85f EN_COURS 2026-10-07T17:42:03Z
  remotes/origin/run/q-i-0c7aabf9c43272942                   7ab095d2b q-i-0c7aabf9c43272942 INTERRUPTED 2026-10-02T19:06:06Z
  remotes/origin/run/q-i-0c80b705ff7d53100                   2b14b1aba q-i-0c80b705ff7d53100 INTERRUPTED 2026-10-02T10:33:22Z
  remotes/origin/run/q-i-0c823996cee1fbfa2                   dfe23ee2e q-i-0c823996cee1fbfa2 INTERRUPTED 2026-10-02T07:35:12Z
  remotes/origin/run/q-i-0c853d82346e693bb                   b33527c53 q-i-0c853d82346e693bb STOP (terminated from the PC) 2026-10-07T05:13:17Z
  remotes/origin/run/q-i-0cc72c6ccf899202f                   5d07c33be q-i-0cc72c6ccf899202f INTERRUPTED 2026-10-05T09:13:52Z
  remotes/origin/run/q-i-0d05279cd32b9fef8                   561eb9156 q-i-0d05279cd32b9fef8 STOP (terminated from the PC) 2026-10-06T23:47:04Z
  remotes/origin/run/q-i-0d5b739cfde206c5e                   8f78ac46c q-i-0d5b739cfde206c5e FINI 2026-10-07T05:50:00Z
  remotes/origin/run/q-i-0d7dba9a8fea98b66                   d3926ca80 q-i-0d7dba9a8fea98b66 FINI 2026-10-07T03:39:46Z
  remotes/origin/run/q-i-0d941684217fe9ffc                   f0518c334 q-i-0d941684217fe9ffc STOP 2026-10-05T10:06:14Z
  remotes/origin/run/q-i-0daead8125bef0456                   1ae110b03 q-i-0daead8125bef0456 INTERRUPTED 2026-10-02T20:01:37Z
  remotes/origin/run/q-i-0daf9c8e1e1f54c5d                   2ac50338f q-i-0daf9c8e1e1f54c5d INSTALLATION 2026-10-07T15:05:36Z
  remotes/origin/run/q-i-0dd6dbc530afb831d                   73ef1f8ef q-i-0dd6dbc530afb831d FINI 2026-10-07T14:38:49Z
  remotes/origin/run/q-i-0dd8a09a554760841                   bd82754da q-i-0dd8a09a554760841 FINI 2026-10-07T14:58:14Z
  remotes/origin/run/q-i-0dda6d8e31bdc250b                   2ab4ae3fd q-i-0dda6d8e31bdc250b INTERRUPTED 2026-10-02T06:14:34Z
  remotes/origin/run/q-i-0e0430be182d1b78d                   793136bc0 q-i-0e0430be182d1b78d EN_COURS 2026-10-07T18:15:04Z
  remotes/origin/run/q-i-0e2a36273e29f0765                   e003a3c44 q-i-0e2a36273e29f0765 FINI 2026-10-07T04:57:35Z
  remotes/origin/run/q-i-0e34e16a2ac224f9c                   30700a452 q-i-0e34e16a2ac224f9c STOP CALIB 2026-10-03T03:23:30Z
  remotes/origin/run/q-i-0e3aa8e044356d325                   74f72f7fd q-i-0e3aa8e044356d325 FINI 2026-10-06T18:00:39Z
  remotes/origin/run/q-i-0e57eb9523cf5327c                   fd431649a q-i-0e57eb9523cf5327c INTERRUPTED 2026-10-07T01:25:43Z
  remotes/origin/run/q-i-0e96f254063ff8a35                   21b1114fd q-i-0e96f254063ff8a35 INTERRUPTED 2026-10-03T03:17:40Z
  remotes/origin/run/q-i-0ec3296d1c09b77da                   69ea0cae5 q-i-0ec3296d1c09b77da FINI 2026-10-07T04:05:58Z
  remotes/origin/run/q-i-0eed576952c30b1f5                   ccc96b8c3 q-i-0eed576952c30b1f5 EN_COURS 2026-10-07T15:01:17Z
  remotes/origin/run/q-i-0f06e472c8b3996e4                   b9b8610eb q-i-0f06e472c8b3996e4 FINI 2026-10-07T05:19:04Z
  remotes/origin/run/q-i-0f15fe75be3a8c87c                   77f486f31 q-i-0f15fe75be3a8c87c STOP (terminated from the PC) 2026-10-06T23:49:30Z
  remotes/origin/run/q-i-0f24682d95b245093                   4bf1fe2a5 q-i-0f24682d95b245093 FINI 2026-10-07T20:23:59Z
  remotes/origin/run/q-i-0f2b25fab00022eeb                   fc52bb8ee q-i-0f2b25fab00022eeb INTERRUPTED 2026-10-06T14:11:32Z
  remotes/origin/run/q-i-0f326fd9a585cbffe                   3b79b3b3b q-i-0f326fd9a585cbffe FINI 2026-10-07T05:36:27Z
  remotes/origin/run/q-i-0f3beb159e48bf3ae                   b984d0c7f q-i-0f3beb159e48bf3ae INTERRUPTED 2026-10-01T22:08:47Z
  remotes/origin/run/q-i-0f425e1b8555e34e6                   33dbb2477 q-i-0f425e1b8555e34e6 FINI 2026-10-07T05:25:45Z
  remotes/origin/run/q-i-0f665dd8b81803ce6                   521628ebf q-i-0f665dd8b81803ce6 INTERRUPTED 2026-10-01T23:09:54Z
  remotes/origin/run/q-i-0f6752b875bdd5220                   0ca882792 q-i-0f6752b875bdd5220 INSTALLATION 2026-10-07T18:15:55Z
  remotes/origin/run/q-i-0f869edb213034d9f                   a786c20ee q-i-0f869edb213034d9f FINI 2026-10-07T14:56:10Z
  remotes/origin/run/q-i-0f893510291059446                   9bd14bcb7 q-i-0f893510291059446 INTERRUPTED 2026-10-01T22:18:46Z
  remotes/origin/run/q-i-0f9b88829406a7ab3                   d16ee8dce q-i-0f9b88829406a7ab3 INTERRUPTED 2026-10-06T14:30:43Z
  remotes/origin/run/q-i-0fa10cb052a603b99                   2915ec487 q-i-0fa10cb052a603b99 INTERRUPTED 2026-10-01T23:09:53Z
  remotes/origin/run/q-i-0fa91a45f074cf15e                   9ace2bf4e q-i-0fa91a45f074cf15e EN_COURS 2026-10-07T14:24:08Z
  remotes/origin/run/q-i-0fabc2411a6580171                   2babc61ef q-i-0fabc2411a6580171 STOP (terminated from the PC) 2026-10-06T22:40:17Z
  remotes/origin/run/q-i-0fd371fb0c83bce5d                   300d75785 q-i-0fd371fb0c83bce5d FINI 2026-10-07T06:04:41Z
  remotes/origin/run/q-i-0fd53514a6dcce992                   edf63ac67 q-i-0fd53514a6dcce992 EN_COURS 2026-10-07T14:54:00Z
  remotes/origin/run/q-i-0ffabb9fb91879e62                   59ae5768b q-i-0ffabb9fb91879e62 FINI 2026-10-07T14:43:09Z
  remotes/origin/run/qci-a                                   9b267338e qci-a EN_COURS 2026-10-01T19:24:07Z
  remotes/origin/run/qci-b                                   7deb2d731 qci-b EN_COURS 2026-10-01T19:23:34Z
  remotes/origin/run/qci-c                                   a03e1aaf1 qci-c STOP 2026-10-01T19:24:47Z
  remotes/origin/run/qci-d                                   cfc48ec4e qci-d STOP 2026-10-01T19:24:53Z
  remotes/origin/run/qci-e                                   f4bb57626 qci-e DRAINED 2026-10-01T19:24:58Z
  remotes/origin/run/qci-v10a                                2652cdd08 qci-v10a FINI 2026-10-06T23:45:59Z
  remotes/origin/run/qci-v10d                                6602c7765 qci-v10d FINI 2026-10-07T12:48:51Z
  remotes/origin/run/qci-v2a                                 c2af9cad7 qci-v2a FINI 2026-10-01T22:23:02Z
  remotes/origin/run/qci-v2b                                 9dee2e94a qci-v2b STOP 2026-10-01T22:23:09Z
  remotes/origin/run/qci-v3a                                 06e1ec2a1 qci-v3a FINI 2026-10-01T23:22:03Z
  remotes/origin/run/qci-v4a                                 f9477ab86 qci-v4a FINI 2026-10-02T00:20:54Z
  remotes/origin/run/qci-v5a                                 ed55d2ebd qci-v5a FINI 2026-10-02T04:42:55Z
  remotes/origin/run/qci-v6a                                 0f9697b62 qci-v6a FINI 2026-10-02T08:39:52Z
  remotes/origin/run/qci-v7a                                 7ac1f1054 qci-v7a FINI 2026-10-02T10:22:28Z
  remotes/origin/run/qci-v8a                                 ebc1f1909 qci-v8a FINI 2026-10-02T16:07:39Z
  remotes/origin/run/qci-v9a                                 ca19307f4 qci-v9a FINI 2026-10-03T14:35:03Z
  remotes/origin/run/slice-19                                507071949 slice-19 EN_COURS 2026-09-30T05:15:24Z
  remotes/origin/run/slice-20                                9ea06c1b8 slice-20 EN_COURS 2026-09-30T05:05:44Z
  remotes/origin/run/slice-21                                3f9097fa2 slice-21 EN_COURS 2026-09-30T05:05:31Z
  remotes/origin/run/slice-22                                fc8d8b3a9 slice-22 EN_COURS 2026-09-30T05:15:41Z
  remotes/origin/run/slice-23                                6b2e23759 slice-23 EN_COURS 2026-09-30T05:15:46Z
  remotes/origin/run/slice-24                                d66eb7447 slice-24 EN_COURS 2026-09-30T05:15:49Z
  remotes/origin/run/slice-25                                816c1ab44 slice-25 EN_COURS 2026-09-30T05:05:51Z
  remotes/origin/run/slice-26                                7c1307a2f slice-26 EN_COURS 2026-09-30T05:05:54Z
  remotes/origin/run/slice-27                                f6a0f0975 slice-27 EN_COURS 2026-09-30T05:06:03Z
  remotes/origin/run/slice-28                                cb6e302fd slice-28 EN_COURS 2026-09-29T22:36:52Z
  remotes/origin/run/slice-29                                2785b32d9 slice-29 EN_COURS 2026-09-29T22:37:05Z
  remotes/origin/run/slice-30                                c1b74a4f8 slice-30 EN_COURS 2026-09-29T22:27:13Z
  remotes/origin/run/slice-31                                88f85d8c8 slice-31 EN_COURS 2026-09-29T22:17:16Z
  remotes/origin/run/slice-32                                0de1cfac8 slice-32 EN_COURS 2026-09-29T23:17:33Z
  remotes/origin/run/slice-33                                dfc9c8091 slice-33 EN_COURS 2026-09-29T22:47:38Z
  remotes/origin/run/slice-34                                f530032ba slice-34 EN_COURS 2026-09-29T22:07:37Z
  remotes/origin/run/slice-35                                b4a2759ea slice-35 EN_COURS 2026-09-29T22:27:50Z
  remotes/origin/run/slice-36                                c6bd067e4 slice-36 EN_COURS 2026-09-29T22:07:54Z
  remotes/origin/run/slice-37                                53f9b804a slice-37 EN_COURS 2026-09-29T22:48:58Z
  remotes/origin/run/slice-38                                4b3903fd4 slice-38 EN_COURS 2026-09-29T23:49:46Z
  remotes/origin/run/slice-39                                bc6f5cb52 slice-39 EN_COURS 2026-09-29T22:30:23Z
  remotes/origin/run/slice-40                                b6ca2d70a slice-40 EN_COURS 2026-09-29T22:21:08Z
  remotes/origin/run/slice-41                                0ada431cb slice-41 EN_COURS 2026-09-29T22:21:36Z
  remotes/origin/run/slice-42                                4db1b43a0 slice-42 EN_COURS 2026-09-29T22:32:15Z
  remotes/origin/run/slice-43                                56e8409de slice-43 EN_COURS 2026-09-29T22:32:43Z
  remotes/origin/run/slice-44                                8abd3c775 slice-44 EN_COURS 2026-09-29T22:23:15Z
  remotes/origin/run/toi-euc1-0                              c0cfca2a3 toi-euc1-0 EN_COURS 2026-09-30T05:08:02Z
  remotes/origin/run/toi-eun1-0                              5fbe58af8 toi-eun1-0 EN_COURS 2026-09-30T05:06:03Z
  remotes/origin/run/toi-euw2-0                              25b19d590 toi-euw2-0 EN_COURS 2026-09-29T23:31:00Z
  remotes/origin/run/toi-use1-0                              0aa183235 toi-use1-0 EN_COURS 2026-09-29T22:15:31Z
  remotes/origin/run/toi-use2-0                              86bd90a57 toi-use2-0 EN_COURS 2026-09-29T23:09:30Z
  remotes/origin/run/toi-usw2-0                              cfc76e6a4 toi-usw2-0 EN_COURS 2026-09-29T21:56:09Z
  remotes/origin/tail-runner                                 2912d9d65 Tail runner: heavy one-y1 stream jobs cut over all the cores of a machine (q/par_consumer.py, q/qtail.py, switch in qmachine.sh)
  remotes/origin/tmp/push-test-laptop                        9d1627d84 ypairs_c2: YP_WORKERS > 1 deals the loop over y1 to forked processes (same statements, output in the same order); default unchanged
  remotes/origin/v10                                         87672fb16 v10: Y=13 pair filter (min L* >= 9/7), FD_MIN97=1 in env_exact; agent parses two-digit package versions; rehearsal workflow
  remotes/origin/v10-fetch-retry                             c4a9b32d7 qagent: retry a failed queue fetch instead of killing the machine
  remotes/origin/v2                                          d89e731fb v2 package fix: exclude run_jobs' RESULTATS_slice tarball from the MANIFEST (the CI rehearsal caught a manifest refusal after calibration)
  remotes/origin/v3                                          e30cf9abb v3 fix: o24_run_fast creates data/finishC/o24_dfs before saving (the v3 rehearsal caught the O24 job failing at save time)
  remotes/origin/v4                                          af6bc8a3d v4: package v4 (golay_pairs jobs for 002, 004, 010 from golay_gen.py; golay job v4 with block loading and INCOMPLETE retry)
  remotes/origin/v5                                          f72cdb34a v5 rebuild: the retry-path calibration compares verdicts only (node counts are CPU-dependent)
  remotes/origin/v6                                          033eaad20 v6: stream node limit 4e9 (run_jobs) and job kind resolve (the 28 unresolved INCOMPLETE pairs of 037, no node limit)
  remotes/origin/v7                                          373530486 v7: spare sub-jobs (stream x8, golay x10/x8) so that slow jobs can be split on demand; only jobs.json differs from v6
  remotes/origin/v8                                          4fc2cf7d5 v8: resolve lists of 023, 024, 026, 028 (118 INCOMPLETE K=0 pairs of the v2 stream, one per job); only the lists and jobs.json differ from v7
  remotes/origin/v9                                          baf5c3f93 v9: fine jobs (one y1 per stream job; Golay 001 n=1700, 002 n=23040) for every open lattice; only jobs.json differs from v8
```

Status (first80 lines; full in JSON):
```

```

## C:\Users\bfhdh\Desktop\Recherche_Conway\c2_experimental\qwatch

Remotes:
```
origin	https://github.com/amazing-source/conway99-c2-aws.git (fetch)
origin	https://github.com/amazing-source/conway99-c2-aws.git (push)
```

Branches:
```
* queue                                    fbe9525 [origin/queue] q-i-0201ab6c589d46854 release:1 release:1 release:1
  remotes/origin/queue                     fbe9525 q-i-0201ab6c589d46854 release:1 release:1 release:1
  remotes/origin/run/q-i-07b69e1205a8909d8 93891dd q-i-07b69e1205a8909d8 INSTALLATION 2026-10-03T14:37:49Z
  remotes/origin/run/q-i-0e34e16a2ac224f9c 0330ac6 q-i-0e34e16a2ac224f9c STOP CALIB 2026-10-03T03:23:30Z
```

Status (first80 lines; full in JSON):
```

```

## C:\Users\bfhdh\Desktop\Recherche_Conway\conway99-involution

Remotes:
```
origin	https://github.com/amazing-source/conway99-involution.git (fetch)
origin	https://github.com/amazing-source/conway99-involution.git (push)
```

Branches:
```
master                           e3f14c2 [origin/master] Lab 2026-09-22 phase 2: scripts, logs and notes left uncommitted until now (CNF files stay ignored)
* math-c2-programme                a121d14 [origin/math-c2-programme] Notebook §34: block-triangle exact counts (positivity, tight); AD configurations status
  remotes/origin/HEAD              -> origin/master
  remotes/origin/master            e3f14c2 Lab 2026-09-22 phase 2: scripts, logs and notes left uncommitted until now (CNF files stay ignored)
  remotes/origin/math-c2-programme a121d14 Notebook §34: block-triangle exact counts (positivity, tight); AD configurations status
```

Status (first80 lines; full in JSON):
```

```

## C:\Users\bfhdh\Desktop\Recherche_Conway\conway99-lab-archive\temp_session_eeaf2d22\scratchpad\conway-99-research

Remotes:
```
origin	https://github.com/YesterdaysLemon/conway-99-research.git (fetch)
origin	https://github.com/YesterdaysLemon/conway-99-research.git (push)
```

Branches:
```
* main                                          85e705c [origin/main] Merge pull request #5 from YesterdaysLemon/codex/wave39-rank-proof-checkpoint
  remotes/origin/HEAD                           -> origin/main
  remotes/origin/codex/wave206-global-extension ad0f098 Document Conway instance separation checkpoint
  remotes/origin/codex/wave212-global-coupling  2b9e52c Seal Wave 212 symbolic coupling checkpoint
  remotes/origin/main                           85e705c Merge pull request #5 from YesterdaysLemon/codex/wave39-rank-proof-checkpoint
```

Status (first80 lines; full in JSON):
```

```

## C:\Users\bfhdh\Desktop\Recherche_Conway\srg-research-audit

Remotes:
```
origin	https://github.com/amazing-source/strongly-regular-graphs-research.git (fetch) [blob:none]
origin	https://github.com/amazing-source/strongly-regular-graphs-research.git (push)
```

Branches:
```
* main                2e460b8 [origin/main] Correct the C2 note: the transfer-pair recertification was not carried out
  remotes/origin/HEAD -> origin/main
  remotes/origin/main 2e460b8 Correct the C2 note: the transfer-pair recertification was not carried out
```

Status (first80 lines; full in JSON):
```

```

## C:\Users\bfhdh\Desktop\Recherche_Conway\t20-codex

Remotes:
```

```

Branches:
```

```

Status (first80 lines; full in JSON):
```

```

## C:\Users\bfhdh\Downloads\conway_c2_researcher2_start_2026_09_30\conway_c2_researcher2_start_2026_09_30

Remotes:
```
origin	https://github.com/amazing-source/conway99-c2-researcher2.git (fetch)
origin	https://github.com/amazing-source/conway99-c2-researcher2.git (push)
```

Branches:
```
* main                7c0758f [origin/main] Route C resume status, AWS adaptive run and Azure state (2026-10-01)
  remotes/origin/HEAD -> origin/main
  remotes/origin/main 7c0758f Route C resume status, AWS adaptive run and Azure state (2026-10-01)
```

Status (first80 lines; full in JSON):
```
?? work/AUDIT_156_PLAN_2026-10-04.md
?? work/CASCADE_STUDY_2026-10-02.md
?? work/CASCADE_STUDY_2026-10-03_cost.md
?? work/FINAL_STATEMENT_C2_DRAFT_2026-10-07.md
?? work/HANDOVER_2026-10-04.md
?? work/REVUE_GLOBALE_2026-10-16.md
?? work/ROUTE_C_SPEEDUPS_2026-10-01.md
?? work/ROUTE_C_SPEEDUPS_2026-10-02_addendum_v5.md
?? work/ROUTE_C_SPEEDUP_AUDIT.md
?? work/VERIF_CUBE_OBSTRUCTION_2026-10-04.md
?? work/asym_paley_2026-10-14/
?? work/asym_paley_data_2026-10-14/
?? work/asym_window_2026-10-14/
?? work/audit_v7_2026-10-12/
?? work/c1_biplane_test_2026-10-07/
?? work/c1_coclique_frame_2026-10-13/
?? work/c1_cores_sat_2026-10-09/
?? work/c1_cost37_2026-10-09/
?? work/c1_index_2026-10-09/
?? work/c1_lap_reps48_2026-10-09/
?? work/c1_lap_sweep48_2026-10-09/
?? work/c1_lap_sweep48t_2026-10-09/
?? work/c1_night_2026-10-14/
?? work/c1_theta_lp_2026-10-07/
?? work/c1_triangles_2026-10-13/
?? work/c2_consolidation_2026-10-14/
?? work/c2_elegant_2026-10-13/
?? work/c3_review_2026-10-13/
?? work/chantier_2026-10-20/
?? work/chatgpt_wagner_2026-10-04/
?? work/coheawood_2026-10-12/
?? work/exploration_2026-10-16/
?? work/indep_wagner_check/
?? work/lambda1_construction_2026-10-14/
?? work/s3_question_2026-10-12/
?? work/scratchpad_LAB_2026-09-30/
?? work/scratchpad_rescue_tools/
?? work/spreadfree_243_2026-10-12/
?? work/stars_rank_2026-10-14/
?? work/t20_hand/
?? work/tools_codex_revive/
```

## C:\Users\bfhdh\Downloads\conway_c2_researcher2_start_2026_09_30\conway_c2_researcher2_start_2026_09_30\work\scratchpad_LAB_2026-09-30\files\recovery_x\ar

Remotes:
```

```

Branches:
```

```

Status (first80 lines; full in JSON):
```

```

