# VERIF R3-21 — lemme « aucune droite dans six grilles » (analogie C7)

Vérificateur adverse, 20/10/2026, contexte neuf. Lecture seule. Calcul : lecture du CSV de l'inventaire c = 3 (un
processus, moins de 10 s).

## Verdict

- **DÉJÀ CONNUE.**
  - Le lemme et ses effets ont été proposés le 19/10 :
    - `representation_2026-10-19/NOTE_MANDAT_REPRESENTATION_2026-10-19.md` §7, P1 (:366) ;
    - `uniform_test_2026-10-19/NOTE_ENONCE_RENFORCE_2026-10-19.md:103`.
  - L'objet est étudié depuis le **08/10** :
    - `work/c1_theta_lp_2026-10-07/NOTE.md` §17.28 (:1243-1248), §17.46 à §17.49 (:1689 et suivantes) ;
    - Codex, notes 201 à 203 (`Desktop/Recherche_Conway/c1-main-codex/notes/`).
- **Le lemme est ouvert.** Il n'est ni prouvé ni réfuté (§3).
- **Le compte annoncé est FAUX.**
  - Le lemme tuerait **9** des 35 gabarits c = 3 ouverts, et non 7.
  - Il faut ajouter **7841** et **9798**, qui ont chacun une droite à c = 6 à la racine.
- **Le coût annoncé (« local, quelques heures de travail ») n'est pas justifié.**
  - Le lemme équivaut à un sous-cas entier du problème (un Conway muni d'une droite à six grilles), et non à un lemme
    local (§4).
- « c = 6 disparaît de toutes les branches » : **juste** (§2).

## 1. Les gabarits concernés (vérification exacte)

Source : `work/exploration_2026-10-16/c3_hard_core_2026-10-18/c3_open_now.tsv`.
- C'est l'état du 19/10 à 15:03, au commit de96dd72 (« ledger 37 -> 35 open ») de `amazing-source/conway99-c1`.
- Aucun registre ni commit plus récent ne le modifie (`git log` de `origin/main` jusqu'au 20/10 16:51 ; recherche de
  fichiers `c3_open*`, `c3_ledger_now*` et `p3u_closed*` plus récents).
- Structure de chaque gabarit : `c3_inventaire_2026-10-19.csv`, colonnes `grilles`, `composantes_par_droite`,
  `sans_paire` et `etat_si_ouvert`.

| gabarit | grilles à la racine | c par droite | droite(s) de degré 6 | sans paire | état |
|---|---|---|---|---|---|
| **7841** | 01 02 03 04 05 06 12 | 6333333 | 0 | non | P3 (AWS), « règle P3U inactive tant que p3u_closed.json manque » |
| 9302 | 01 02 03 04 05 06 12 34 56 | 6333333 | 0 | oui | aucun outil ne ferme |
| 9791 | 01 02 03 04 05 06 12 13 24 56 | 6443333 | 0 | oui | idem |
| **9798** | 01 02 03 04 05 06 12 13 14 56 | 6533333 | 0 | non | P3 (AWS), idem 7841 |
| 9912 | 01 02 03 04 05 06 13 14 25 26 | 6443333 | 0 | oui | aucun outil ne ferme |
| 9966 | 01 … 06 12 13 24 35 46 | 6444433 | 0 | oui | idem |
| 10003 | 01 … 06 12 13 14 15 16 | 6633333 | 0 et 1 | oui | idem |
| 10006 | 01 … 06 12 13 23 45 46 56 | 6444444 | 0 | oui | idem |
| 10025 | 01 … 06 12 13 14 15 16 23 | 6644333 | 0 et 1 | oui | idem |

- **Les 7 gabarits cités contiennent bien une droite dans six grilles.**
- L'erreur de compte vient d'un mélange de deux énoncés :
  - RENF :103 dit « 7 des **19 gabarits sans paire** », ce qui est exact : les 7 sont les seuls à c = 6 parmi ces 19 ;
  - MAND :366 omet les deux gabarits alors en production P3.
- Or P3 n'est pas achevé et AWS est abandonné depuis le 20/10. 7841 et 9798 restent donc ouverts.
- **Réduction exacte : 35 → 26 ouverts.**
- Sur les 10 052 gabarits, 214 ont une droite à c = 6 : 205 sont déjà exclus par d'autres méthodes, 9 sont ouverts.

## 2. « c = 6 disparaît »

- On a **c(l) = 6 ⟺ g(l) = 6**.
  - Une composante de G_l à 6 sommets est un prisme, donc une grille contenant l (MAND §1.1 :62 ; P9 de
    NOTE_PROOFS_1410).
  - Six grilles par l donnent six composantes de 6 sommets.
- Sans droite dans six grilles, aucune droite n'a c = 6. Comme g ≠ 5 (« c ≤ g + ⌊(6 − g)/2⌋, g ≠ 5 », P8/P9, cité dans
  `work/stars_rank_2026-10-14/THREE_RESULTS_2026-10-15.md:101`), on obtient
  **g(l) ≤ 4 partout**.
- L'affirmation est juste. Son poids est limité : NOTE thêta §17.48 (:1842) dit « excluding six-grid lines only leaves
  tau_g ≤ 1134, not enough » pour la route du rang 37.

## 3. Déjà prouvé ou réfuté ailleurs ? Non. État connu

- **08/10, NOTE thêta §17.46** (:1716-1719).
  - Le lemme équivaut à la non-existence d'un design : 60 noms dans (ℤ₃ × ℤ₂)⁶, 20 triangles et 6 couplages.
  - « Conversely a system (names, graph on B) with these properties is a strongly regular graph (99,14,1,2) with a line in
    six grids. »
  - « Nothing is known about it here. »
- **08/10, §17.47.**
  - Les noms sont les 60 étoiles ordonnées du graphe de Petersen, pour la solution de colonnes canonique.
  - D'autres solutions de colonnes existent.
  - CP-SAT, 240 s : UNKNOWN.
- **08/10, addendum de §17.46** (session portable, `pencil_det.py`).
  - Le réseau lointain est de rang 13 sur B, avec det(L_far)·t² = 324·5¹²·7^(r−32).
  - Hermite ne contredit qu'à r ≤ 31 : « NEGATIVE ; do not recompute ».
- **08/10, Codex 202 et 203** (r ≥ 37).
  - Motifs de « hubs » exclus autour d'une droite à six grilles : (2,2,1) et (2,2,2).
  - « On a line in six grids, if two points have three hub lines each, the third has only one. »
  - Codex 203:24 : « Ils n'excluent ni toutes les droites dans six grilles, ni un rang entier. »
- **19/10, MAND §5 (Corollaire 2) et §6.3 ; RENF :82-86.**
  - 420Π_T est entier et explicite, de rang 13 et de diagonale 91.
  - Plus de 536 classes de colonnes à S₆ × S₃ près, en moins de 5 min, énumération inachevée.
  - CaDiCaL, 280 s : UNKNOWN.
  - « La méthode des résidus de C7 devient applicable ; elle n'est pas encore appliquée. »

## 4. Ce qu'il faudrait prouver exactement, et coût honnête

**Énoncé.** Aucun srg(99,14,1,2) n'a de droite T = {t₁, t₂, t₃} contenue dans six grilles G_k = T ∪ X_k (k = 1, …, 6).

**Forme finie équivalente** (NOTE thêta §17.46 et MAND §5). Il s'agit de montrer qu'il n'existe pas de données
(x, R) vérifiant les conditions suivantes.
- B est l'ensemble des 60 sommets lointains.
- Les noms x : B → (ℤ₃ × ℤ₂)⁶ donnent la colonne et la ligne de l'unique voisin v_k(b) ∈ X_k.
- (N1) Chaque nom utilise chaque colonne deux fois : un synthème des six grilles, avec ses trois duades bijectées sur les
  colonnes.
- (N2) Pour k ≠ j, #{b : x_k(b) = v, x_j(b) = v′} vaut 1 si v et v′ ont même colonne, 2 sinon.
- R est un graphe 8-régulier sur B. Il porte 20 triangles qui partitionnent B, et 6 couplages parfaits M_k disjoints
  (b ∼ b′_k : même nom en k, différent partout ailleurs).
- Pour b ≠ b′ : (accords des noms) + |N_R(b) ∩ N_R(b′)| vaut 1 si b ∼ b′, 2 sinon.
- Pour v ∈ X_k : le nombre de voisins de b dans le bloc de v vaut 1, 1 ou 2, selon que v = v_k(b), v est adjacent à
  v_k(b) dans le prisme, ou ni l'un ni l'autre.
- Conséquences, non indépendantes, que l'on peut utiliser comme leviers :
  - R² + R + EᵀE = 12I + 2J ;
  - trois équations de vecteurs propres de R ;
  - 420Π_T = 180I − 60R + 25J + Σ_k W_k, entier, PSD, de rang 13, avec (420Π)² = 420·420Π.

**Ce qui diffère de C7** (analogie, pas transposition).
- En C7, le Gram venait de la matrice d'orbites d'un automorphisme : 12 vecteurs de ℝ⁴, avec des résidus α = 12z²
  entiers.
- Ici il n'y a **aucun groupe** (Aut = 1 en C1), mais 60 vecteurs de ℝ¹³.
- La partie colonnes n'est pas unique.
- Un argument de résidus reste à inventer. Il n'existe pas en l'état.

**Coût honnête.**
- **Étape 1 : classifier les solutions de colonnes.**
  - Plus de 536 classes, énumération inachevée, une génération ordonnée est à écrire.
  - Coût **inconnu**. Mesurable par un pilote (estimateur de Knuth sur l'arbre de génération) de moins de 5 min.
- **Étape 2 : signes et graphe R, par classe** (360 bits de signes, puis R sur 60 sommets).
  - Coût **non mesuré**. Les solveurs CDCL et CP-SAT ne concluent pas, même sur des sous-modèles (45 s, 240 s, 280 s :
    UNKNOWN).
  - Avec au moins 536 classes, même une heure par classe ferait au moins 536 heures.
- Une solution complète est un Conway. Le problème est donc **un sous-cas entier de l'existence**, très structuré (39
  sommets fixés), mais pas un « lemme local ».
- « Quelques heures » ne vaut au mieux que pour finir l'étape 1.
- Avant tout lancement, il faut faire le pilote de mesure, puis une décision chiffrée. Sinon, pas de calcul.

**Gain si c'est prouvé.**
- Registre c = 3 : 35 → 26 ouverts.
- c ≤ 5 et g ≤ 4 partout.
- Aucune exclusion de C1, d'un rang ou d'une branche à lui seul.
- Branche c ≥ 4 (`c1-main-codex/data/codex_line_resonance_20261016/root_component_cover79.json`) :
  - les deux gabarits encore ouverts, n° 9 et 19, ont c = (4, 4, 4, 4, 4, 4, 4) : **le lemme ne les touche pas** ;
  - le n° 7 a une droite à c = 6 ; il est déjà exclu à la racine pondérée (C + P), et le lemme l'exclurait pour toute
    racine ;
  - la branche c ≥ 4 ne serait donc pas fermée par ce lemme.

## 5. Contrôles obligatoires (récapitulatif)

1. Énoncés : MAND :306 (formule de 420Π) et :366 (P1) ; RENF :103 ; NOTE thêta :1716-1719 ; Codex 203:24. Lus à la
   source.
2. Définitions :
   - « droite dans six grilles » : g(l) = 6 ⟺ c(l) = 6 ⟺ degré 6 dans le graphe des grilles à la racine ;
   - les gabarits notent les c des sept droites de la racine.
3. Hypothèses : aucune ; le lemme est général. Les résultats partiels de Codex 202 et 203 supposent r ≥ 37.
4. Statuts :
   - lemme : O ;
   - Corollaire 2 : P (LAB, 19/10, non relu) ;
   - inventaire : E (rejeu du registre, sans nouveau verdict).
5. Logique : « tue 7 des 35 » devient « tue 9 des 35 ». L'implication « lemme ⇒ ces gabarits tombent » est correcte, car
   chacun impose c = 6 à une droite de la racine.
6. Redécouverte : voir le verdict et §3.
7. Contrôle numérique : script de lecture du CSV. Il donne 9 ouverts à c = 6, dont 7 sans paire, et 214 gabarits à c = 6
   en tout, dont 205 exclus.
