# VERIF R1-01 / R3-01 — DISC : classe 2 seule (8T, rang 30), classe 1 seule (15U, rang 40)

Vérificateur adverse, 20/10/2026, contexte neuf. Lecture seule. Calculs : `arith_checks.py` et un balayage des sorties
JSON de Codex (scratchpad, un processus, moins d'une minute).

## Verdict

**DÉJÀ CONNUE. La mathématique TIENT. L'effet est nul : DISC ne sert dans aucun calcul encore ouvert.**

- **Antériorité.**
  - `work/stars_rank_2026-10-14/NOTE_PROOFS_1410.md:340-341` (LAB, 14-15/10) : « (SQ3) … with k even (L2) this is a perfect
    square divisible by 49 ».
  - `disc_scan.py:6-8` et `:83-84` : le test exige déjà la classe 2.
  - Message LAB n° 886 du pont (16/10, 08:09) : « La classe de carrés doit donc valoir 2 ou 14 (**2 seul avec ta parité
    L2/L22**) ».
- **Correction de récit.** La forme faible n'a pas été « perdue ». Elle a été **gardée exprès** comme partie robuste :
  - `EXT84_2026-10-16.md:16-17` : « The robust part (no lemma of Codex) » ;
  - Codex, message n° 888 : « je l'integre … sans supposer la parite2 seule » ;
  - `JOURNAL_C1_NUIT_2026_10_14.md:6195` : « Aucun lemme de parite n'est utilise ici ».
  - Raison plausible : L2 porte le drapeau « [P] [?] » dans `30_LEMMES.md:30`, faute de contrôle machine.

## 1. Chaîne réécrite

| # | maillon | source exacte | statut |
|---|---|---|---|
| 1 | Pour M entière symétrique de rang r, tous les mineurs principaux r × r non nuls sont dans une même classe de ℚ*/ℚ*² : det M_H = disc(R)·[R : R_H]². | NOTE_PROOFS_1410:332-337 (testé sur Petersen, Paley 9 et 25 et un srg(243)) | P |
| 2 | M = 3I − A est de rang 45 ; disc R = det(M\|W)/det Λ₃ = (−11·7⁴⁴)/(11·7^(14+k)) = −7^(30−k). | NOTE_PROOFS_1410:337-339 ; det Λ₃ = 11·7^(14+k) : L2 et L4 (`cw/conway99-c1/notes/30_LEMMES.md:30-44`, `:54-63`) | P (L2 « [P] [?] », L4 « [P] [C] ») |
| 3 | (SQ3) det(A_H − 3I) = 7^(30−k)·n² pour \|H\| = 45 ; (SQ-4) det(A_H + 4I) = 2·7^(40−k)·n² pour \|H\| = 55. (SQ-4) utilise det Λ₋₄ = 9·7^(14+k) (L22, `30_LEMMES.md:298-305`). | NOTE_PROOFS_1410:340-342 | P |
| 4 | Schur par rapport à N[v] (moulin F₇) : det(3I − F₇) = −2²³ et det(4I + F₇) = 2·3⁸·5⁶. D'où **det(8T_I) = 2⁶⁷·7^(30−k)·n²** et **det(15U_I) = 3³²·5³⁴·7^(40−k)·n²**. | recalculé ici, exactement et numériquement sur le moulin ; même classe que 2⁶⁹·7^(30−k) (NOTE_PROOFS_1410:255) | C |
| 5 | Les deux k sont le même : L4 donne rang₇(A − 3I) = k(x) + 15, avec k(x) = rang₇((H − 3I)\|_K). L17 donne det K₋₄ = 2²¹·7^k et det K₃ = 3⁸·5⁶·7^k, et l'exposant de 7 y est le rang du recollement 7-adique de K₃ ⊥ K₋₄ dans K (7-unimodulaire), c'est-à-dire rang₇((H − 3I)\|_K). | `30_LEMMES.md:54-63` (L4), `:228-236` (L17) ; identification refaite ici | P |
| 6 | k est pair : L2 donne α pair (2-adique et 11-adique), L4 donne k = α − 14. Dans la fenêtre r ∈ {37, 39, 41, 43}, k ∈ {22, 24, 26, 28}. | L2, L4 ; fenêtre (C, L06) | P |
| 7 | **Classe(det 8T_I) = 2 et classe(det 15U_I) = 1.** Les classes 14 et 7 ⟺ k impair. Contrôle : k = 23 donne exactement 14 et 7. | calcul | P (statut du plus faible : L2) |

## 2. DISC dans les calculs encore ouverts : aucun usage

- **Code de Codex** (`Desktop/Recherche_Conway/c1-main-codex/code/codex/*.py`, recherche de `DISC_CLASSES`, `--disc`,
  `square_class`).
  - Seul `conway_core_repair.py` implante DISC : `DISC_CLASSES = ((2,14),(1,7))` à la ligne 36, option `--disc` à la
    ligne 679.
  - Aucun autre module ne l'importe et il n'existe pas d'autre implantation.
  - Les paquets AWS en contiennent une copie (`work/scratchpad_LAB_2026-09-30/files/aws_c1/pkg_*`), mais aucun script de
    lancement ni d'analyse de `aws_c1/` ne l'appelle.
  - Toutes ses sorties (`c1-main-codex/data/codex_local_global_20261015/core_repair_*`) sont datées du **16/10**, comme
    la source (`c1-asymmetry-audit/code/codex/conway_core_repair.py`, modifiée le 16/10 à 13:51).
- **Sorties `--disc`.** Dans les 9 fichiers qui enregistrent des contrôles DISC, **tous les contrôles échouent**, pour
  chaque classe (2, 14, 1, 7) ; aucun n'a passé grâce à 14 ou 7.
  - Les sorties ne gardent que les obstructions, si bien que les colonnes conservées ne s'auditent pas.
  - Mais la route du 16/10 n'a revendiqué aucun bloc de 45 admissible.
- **Registre c = 3.** Méthodes P1 à K2BC (`c3_inventaire_2026-10-19.md:32-55`) : aucune n'est DISC.
- **R8.** `merge_2026-10-19/r8_route/NOTE_R8_ROUTE.md:319` : « DISC (archive, PROUVÉ) : non utilisé dans ce pilote ».
- **Route du rang 37.**
  - `line37.cpp` et `line37_fast.cpp` n'ont pas de test DISC.
  - Le δ(T) ∈ {1, 3} de `THEOREME_REDUCTION_R37.md:124` est la classe du discriminant du **résidu lointain mod 7**,
    autre objet, sans rapport avec 14/7.
- **Rang 39, ordre 2 (20/10).** `star39o2.cpp:10-11` prévoit un vidage pour un test de classe de carrés (`o2_sqclass.py`)
  du projecteur lointain de rang 8, autre objet.
  - Le fichier `o2_sqclass.py` est absent.
  - Toutes les exécutions de `engine_runs_2026-10-20.log` ont `dump8 = 0`.
- Conclusion : **resserrer DISC ne change aucun résultat ni aucun calcul en cours.** Un filtre plus faible ne crée pas de
  fausse exclusion ; il ne peut qu'avoir manqué des coupes dans la route du 16/10, close.

## 3. Contrôles obligatoires

1. **Énoncés exacts.** Lus à la source : NOTE_PROOFS_1410:254-261 et :332-348, disc_scan.py, 30_LEMMES L2, L4, L17 et L22,
   EXT84 :10-21, `disc_batch.py:2-3` et `:44-46` (accepte {2, 14} : `odd <= {2, 7} and 2 in odd`), pont n° 886 à 888,
   JOURNAL :6193-6196.
2. **Définitions.**
   - k = r − 15 avec r = rang₇(A − 3I), convention de l'équipe ; la même chose que k(x) de L4 et que l'exposant de L17.
   - 8T est restreint à 30 étiquettes au même sommet ; N[v] ∪ I est un complément étoilé de 45 sommets.
3. **Hypothèses.** Aucune symétrie. Rang quelconque dans la fenêtre. Les seules dépendances sont L2 et L4 (parité),
   L22 pour U, et l'existence d'un I de rang plein.
4. **Statuts.** P, maillon le plus faible L2 (« [?] »). Ces énoncés ne sont pas relus par un humain. La parité de r est
   recoupée par le dépôt externe (W66 : r_ext pair, d'où r impair) et par la fenêtre thêta.
5. **Logique.** Les classes sont dans ℚ*/ℚ*², donc 2⁶⁷ ~ 2⁶⁹ ~ 2. L'équivalence « 14 ⟺ k impair » est vérifiée
   numériquement.
6. **Redécouverte.** 14-15/10 (NOTE_PROOFS_1410, disc_scan.py) ; 16/10 (pont n° 886) ; relectures 02, 03 et 05 du 16/10 ;
   L09-COND-242 et 249. R1 et R3 le disent eux-mêmes.
7. **Contrôle numérique.** det(3I − F₇) = −8 388 608 = −2²³ ; det(4I + F₇) = 205 031 250 = 2·3⁸·5⁶ ; classes 2 et 1 pour
   k ∈ {22, 24, 26, 28}, classes 14 et 7 pour k = 23.

**Petites inexactitudes de R1-01.**
- « 645 germes » : les sources disent 643. EXT84 :20 donne 643, plus HB ; JOURNAL :6196 donne 643, HB et urep compris.
- « Perdue » : il s'agit d'un choix de robustesse, voir le verdict.

## 4. Ce qui manquerait

- Rien pour l'énoncé, à la relecture humaine près de L2 et L4.
- Pour un éventuel réemploi de `conway_core_repair.py --disc` : passer `DISC_CLASSES` à `((2,),(1,))`, sous L2 et L4.
  - Le gain n'est pas mesuré.
  - Aucun germe vivant en classe 14 n'a jamais été vu : les 643 échouent déjà aux premiers 3 et 5.
