# VERIF R1-06 — (T15) « sauf au plus 34 blocs » et P ≤ 852

Vérificateur adverse, 20/10/2026, contexte neuf. Lecture seule. Calcul : `arith_checks.py` (scratchpad, un processus,
moins d'une seconde).

## Verdict

- **L'implication est DÉJÀ CONNUE.** (T15) avec P ≤ 852 exclut Conway. Sources :
  - `work/stars_rank_2026-10-14/AUDIT_EXCLUSIONS_2026-10-15.md:46` (O3, 15/10) ;
  - `THREE_RESULTS_2026-10-15.md:57-61` (§3 (c) et (d), 15/10) ;
  - la cible G11 de CONWAY_CONSTRAINTS (14/10).
- **La « forme affaiblie » est CASSÉE en tant qu'affaiblissement.**
  - Le seuil 34 est juste, mais l'énoncé est vide : il équivaut à « pas de Conway ».
  - Ce n'est pas une loi locale plus faible que (T15). C'est la contraposée du comptage.

## 1. Chaîne réécrite

| # | maillon | source exacte | statut |
|---|---|---|---|
| 1 | Un bloc est un triplet (v; l, m), l ≠ m droites par v. Il y en a 99·21 = 2079 = 231·18/2. | THREE_RESULTS:52 | P |
| 2 | t(l) est le nombre de prismes contenant l, égal au nombre de triangles transversaux de G_l. C'est un invariant de droite, lisible dans tout bloc contenant l. Σ_l t(l) = 2P. | THREE_RESULTS:14-17 ; CARTE §1.5 ; refait ici (les triangles de G_l sont transversaux, car l'arête de deux voisins d'un même point a est dans la droite par a) | P |
| 3 | Σ_blocs (t(l) + t(m)) = 18·Σ_l t(l) = 36P : chaque droite est dans 18 blocs (6 partenaires en chacun de ses 3 points). | THREE_RESULTS:57 ; refait | P |
| 4 | **Tout bloc d'un Conway est admissible, T et U PSD, de nullité ≥ 14.** (T15) s'applique donc aux 2079 blocs. | NOTE_PROOFS_1410.md:13-14 (P1), :35-40 (P6 : « nullity T_S4 ≥ 14 »), :60-73 (P10) ; CONWAY_CONSTRAINTS G9 (`work/asym_paley_2026-10-14/CONWAY_CONSTRAINTS.md:80`) ; THREE_RESULTS:99 (« P1, P10, G9 ») | P (LAB, 14/10) ; redérivé ici, voir ci-dessous |
| 5 | P ≤ 852 | certificat `c1-codex/data/codex_order9_prism_cap.json` | C relativement au recensement (E en double implantation) |
| 6 | Si E est l'ensemble des blocs qui violent (T15), alors 36P ≥ 15(2079 − \|E\|). Avec P ≤ 852 : 30 672 ≥ 31 185 − 15\|E\|, donc \|E\| ≥ 34,2, soit **\|E\| ≥ 35**. | calcul | P |

**Redérivation du maillon 4** (indépendante de P6/G9, en trois lignes).
- Soit Σ = N[v] ∪ S4, avec S4 les 44 étiquettes de X_l ∪ X_m ; |Σ| = 59.
- La nullité de T_S4 est la multiplicité de 3 dans A_Σ : Schur par rapport à N[v], où 3I − F₇ est inversible,
  det = −2²³.
- Par entrelacement, cette multiplicité est ≥ 54 − (99 − 59) = **14**.
- T_S4 ⪰ 0 par Haynsworth : λ₂(A_Σ) ≤ λ₂(A) = 3, donc n₋(3I − A_Σ) ≤ 1 = n₋(3I − F₇), d'où n₋(T_S4) = 0. U de même,
  avec 4I + F₇ > 0.
- La condition « nullité ≥ 14 » de (T15) ne retire donc aucun bloc : le compte 2079 est le bon.

## 2. Pourquoi la forme affaiblie est vide

- (T15) est un énoncé universel sur des structures locales abstraites (blocs admissibles PSD de nullité ≥ 14).
- « Sauf au plus 34 blocs » n'a de sens qu'à l'intérieur d'un graphe donné : c'est un énoncé global.
- Les maillons 3 à 6 **démontrent** que tout Conway (avec P ≤ 852) possède au moins 35 blocs avec t(l) + t(m) ≤ 14.
- « Tout Conway en a au plus 34 » est donc équivalent à « il n'existe pas de Conway ».
- La forme affaiblie ne servirait que dans une stratégie en deux temps :
  1. (T15) sur une classe 𝒞 de blocs reconnaissable localement ;
  2. une borne globale ≤ 34 sur les blocs hors de 𝒞.
- Aucune classe 𝒞 de ce type n'existe dans le matériau. Les comptes forcés connus se chiffrent en centaines :
  - au moins 945 blocs non grille si ρ ≤ 126 (THREE_RESULTS:54-55) ;
  - 9G ≤ 1134 blocs de grille ;
  - au moins 254 blocs non grille avec min t ≤ 7 (Codex, THREE_RESULTS:122-125).

**Forme correcte et utilisable** (P, avec P ≤ 852) : *tout Conway contient au moins 35 blocs (v; l, m), PSD de nullité
≥ 14, avec t(l) + t(m) ≤ 14.*
- 35 n'est que la borne de moyenne, sûrement loin d'être optimale.
- Avec t ≤ 12 (F3), une droite à t ≤ 2 rend ses 18 blocs violants.
- Le spectre du graphe des droites (18, 7⁵⁴, 0⁴⁴, (−3)¹³²) force davantage. Ce compte n'est pas fait ici.

## 3. Contrôles obligatoires

1. **Énoncés exacts.**
   - THREE_RESULTS:57-61 : « each line lies in 18 blocks, so the sum over the blocks of t(l) + t(m) equals 36 P » ; « any
     law 'every PSD four-star block of nullity >= 14 has t(l) + t(m) >= 15' excludes Conway (… P >= 866.25 > 852) ».
   - AUDIT O3 (:46) : variante « P ≥ 867 », la version entière de 866,25.
2. **Définitions.** t(l) dans (T15) (transversales du bloc) et t(l) dans 36P (prismes) coïncident (maillon 2). La nullité
   est celle de T_S4, de taille 44 × 44.
3. **Hypothèses.** Aucune hypothèse de rang ni de c(l). Les blocs de grille sont inclus, et (T15) les couvre aussi.
4. **Statuts.** Implication P ; P ≤ 852 est C relativement au recensement ; (T15) est **O**.
   - Fragilité : à la nullité 13, on observe t = (6, 8), soit t(l) + t(m) = 14 (THREE_RESULTS:69-70 ; AUDIT:104-106).
   - Une relation de plus suffirait donc à réfuter (T15) comme (T8).
   - Les 558 structures de nullité 14 (toutes à t(l) + t(m) ≥ 16) se répartissent ainsi (THREE_RESULTS:63-73) :
     - 532 sont des paires de grille ;
     - les 26 autres viennent de la lignée G1 c55, exclue par rang_F7 ≥ 29.
   - Ces données sont biaisées par famille. De même, les 331 objets de rang 30 de l'AUDIT échouent tous à DISC : aucun
     n'est un bloc de Conway (AUDIT, §3, points 3 et 4).
5. **Logique.**
   - Le seuil est entier : 15·2045 = 30 675 > 30 672 et 15·2044 = 30 660 ≤ 30 672. Le seuil 34 est donc exact pour
     l'argument de moyenne.
   - Moyenne requise : t(l) + t(m) > 30 672/2079 = 14,753.
6. **Redécouverte.**
   - L'implication date du 15/10 (O3, THREE_RESULTS §3 (d)).
   - La phrase « sauf au plus 34 » n'est écrite nulle part avant R1. Recherches « sauf 34 », « 35 blocs »,
     « t(l) + t(m) ≤ 14 » dans `work/`, hors `assemblage/`.
   - C'est une contraposée arithmétique, pas une nouveauté.
7. **Contrôle numérique.**
   - 36·852 = 30 672 ; 15·2079 = 31 185 ; écart 513 ; 513/15 = 34,2, donc au moins 35 exceptions.
   - (T15) partout donne P ≥ 3465/4 = 866,25 ; (T8) donne P ≥ 924.

## 4. Ce qui manquerait

- (T15) lui-même, énoncé local ouvert, ou une version restreinte à une classe 𝒞 de blocs, avec une borne globale ≤ 34 sur
  les blocs hors de 𝒞. La forme « sauf 34 » n'abaisse pas la difficulté.
- Si l'on veut un compte forcé plus fort que 35 (blocs à t(l) + t(m) ≤ 14), il faut un petit programme sur les valeurs t
  du graphe des droites, sous t ≤ 12 et avec les bornes spectrales. Ce calcul est faisable mais n'est pas fait ici.
