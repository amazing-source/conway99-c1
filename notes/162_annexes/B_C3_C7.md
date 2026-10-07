*Annexe de la note 162 : rapport d’un agent de lecture (07/10/2026), versé tel quel. Les affirmations sur les autres dépôts sont celles du rapport ; voir la note 162 pour la synthèse et les réserves.*

# Audit des dépôts Conway 99 : branches C3 et C7

## Synthèse
- **C3 est résolu, et c'est le résultat nouveau le plus fort des trois dépôts.** Il l'est dans `conway99-c3-experimental`, par une preuve sans ordinateur fondée sur une obstruction par les discriminants, et entièrement vérifiée en Lean 4. Le dépôt `conway99-c3`, lui, est une campagne SAT inachevée qui se déclare non conclusive : « Rien n'est encore décidé ». Cette campagne a été rendue inutile le même jour par la preuve, mais n'a jamais été mise à jour.
- **C7 n'est pas nouveau comme énoncé.** Le dépôt le dit lui-même : Behbahani–Lam excluent déjà l'ordre 7 par ordinateur. La nouveauté est d'en donner la première preuve sans ordinateur. Cette preuve couvre bien le cas « Z₇ avec un point fixe » que Thakkar–Severini disent ouvert.
- **Mes propres vérifications :**
  - J'ai relancé `check_all.py` et `audit_verify.py` (C3), puis `checks/*.py` (C7) : toutes les sorties concordent avec ce que les dépôts annoncent.
  - J'ai écrit et lancé une recherche exhaustive indépendante en C du problème matriciel 12×12 de C7. Elle trouve 0 solution (7,4·10⁹ nœuds), et un contrôle positif retrouve bien une solution plantée.
  - L'API GitHub confirme que le run CI 35880776817 du dépôt C3 expérimental a réussi (commit `874903f`).
  - Pas de Lean dans ce conteneur : je n'ai pas recompilé les preuves, j'ai lu les journaux.
  - Les Actions du dépôt C7 ne sont pas accessibles depuis cette session.

---

## 1. C3 (ordre 3)

### 1a. Volet calcul (`/home/user/conway99-c3`, 22–23/09)
**Statut annoncé :** « Rien n'est encore décidé » (`README.md`). C'est une réduction exhaustive suivie d'un étage SAT inachevé.
- **τ = 6 orbites triangulaires** [D+L].
  - Première preuve : via Ishida (arXiv:2606.29183v2, prop. 4.4 et 8.7).
  - Puis une **preuve autonome** : Im E₃ est projectif sur Z₃[C₃], qui est un anneau local, donc libre, donc la trace est nulle.
- **26 graphes F possibles sur 156** [C] : 87 exclus par une entrée négative, 25 par un mineur négatif, 18 par un certificat de Farkas entier. Je l'ai reproduit : `PASS: 26 witnesses exact, 18 Farkas certificates exact`.
- **318 classes de phases → 125 → 46** à symétrie près [C]. Je l'ai reproduit.
- **Lemmes [D] de filtre par type et des triplets.** Les exclusions en dépendent, et le rapport classe leur relecture humaine comme « prioritaire ».
- **Étage quotient :**
  - 9 instances UNSAT avec preuve **DRAT** (CaDiCaL 3.0.1 + drat-trim, `certs/SUMMARY*.txt`) ;
  - m00028_sL0 UNSAT par cube-and-conquer (325/325, statut S, non certifié) ;
  - 3 381 cubes UNSAT, aucun SAT.
- **Énumérations certifiées par DRAT** pour 7 classes sur 46. Les classes 29, 43, 44 et 45 restent incomplètes. Il reste environ 40 instances.
- **Les CNF et les preuves DRAT ne sont pas dans le dépôt.** Elles sont régénérables, avec leur SHA-256 dans `*.gen.json`.
- **Auto-audit (Claude) :** 6 erreurs de programme corrigées (portes ET CP-SAT, lecture du retour chariot de drat-trim, faux positif de Sturm, etc.) et 2 affirmations corrigées (« 33 complètes / 13 » → 35 / 11 ; « le niveau 2.5 n'élimine rien »). Aucune relecture humaine.

### 1b. Preuve mathématique (`/home/user/conway99-c3-experimental`, 23/09)
**Énoncé Lean** (`c3formal/Challenge.lean`, `srg99_aut_cube`) :
> pour `G.IsSRGWith 99 14 1 2` et `σ : G ≃g G` avec `∀ v, σ (σ (σ v)) = v`, alors `∀ v, σ v = v`

Le même fichier donne aussi :
- les formes « groupe » : `orderOf σ ≠ 3` et `¬ 3 ∣ Nat.card (G ≃g G)` ;
- une forme booléenne sur `Fin 99` qui n'utilise aucune bibliothèque de graphes ;
- des tests de non-vacuité sur srg(9,4,1,2).

**Énoncés du PDF** (`pdf/preuve_c3.tex`, 7 pages) :
- Thm 1 : « Γ n'a aucun automorphisme d'ordre 3 sans point fixe ».
- Prop 2 : même conclusion « ayant exactement trois points fixes ».
- Cor 3 : « Γ n'a aucun automorphisme d'ordre 3 ».
- Thm 5 (forme matricielle) : il n'existe pas de couple (Q, M) avec Q ∈ M₃₃(Z) symétrique, Q𝟙 = 14·𝟙, Q² + Q = 12I + 6J, M ∈ M₃₃(Z[ω]) hermitienne avec M² + M = 12I, et Q ≡ M (mod 1−ω).
- Lemme 7 : au plus 3 points fixes.
- Cor 8 : (i) |G| ∈ {1, 2, 7, 11} avec MM04 et CW25 ; (ii) |G| ∈ {1, 2} avec Behbahani–Lam.

**Architecture de la preuve :**
1. **Réduction.** On pose Q = A₀ + A₁ + A₂ et M = A₀ + ωA₁ + ω²A₂.
2. **Bases entières.** On prend des bases B, B′ des noyaux saturés, avec des inverses à gauche C, C′.
3. **Identités GK = 77I et G′K′ = 7I.** Elles donnent d = 7^a·11^b et d′ = 7^c ≡ 1 (mod 3).
4. **Valuation 11-adique.** Avec ⟨𝟙,𝟙⟩ = 33, on a 33·d = det(T)²·det G_W et 11 ∤ det G_W, donc b est impair et d ≡ 2 (mod 3).
5. **Réduction modulo 3.** On a N̄ = 2N̄′, d'où r = r′ et d ≡ d′ (mod 3).
6. **Contradiction** entre les étapes 4–5 et l'étape 3.
- **Cas du triangle fixe** : sans recours à Ishida. Les coordonnées fixes sont divisibles par 3, on utilise le Gram pondéré G̃ et 𝟙ᵀD𝟙 = 99.
- **Lemme 7** : comptage élémentaire (n_x ∈ {2, 8, 14}). Il remplace Makhnev–Minakova.

**L'étincelle** (`notes/P1_recollement.md`, `IDEES.md` D1) : « l'invariant après le rang ».
- La preuve τ = 6 lisait la **trace** du module libre E₃·Z₃⁹⁹ ≅ Z₃[C₃]¹⁸.
- L'invariant suivant est son **discriminant**, dont les deux spécialisations (x = 1 et x = ω) sont congrues modulo 3.
- Côté trivial, 𝟙 a pour norme 33 = 3·11, ce qui injecte 11, qui n'est pas un carré modulo 3. Côté ω, seul 7 ≡ 1 intervient.
- Bonus : la preuve redonne τ = 6 et r = 18.

**Mathématique pur ou assisté par ordinateur :**
- La preuve n'utilise **aucun calcul** : elle ne se sert même pas des valeurs 0, 1, 2 des entrées de Q.
- **Vérification formelle.** Lean v4.35.0-rc2 + Mathlib, 3 754 lignes, aucun `sorry`, axiomes `propext`, `Classical.choice` et `Quot.sound` uniquement (`logs/lean_axioms_final.log`).
- **Comparateur.** `lake comparator --paranoid` répond « Your solution is okay! » sur Windows sans bac à sable, puis sur GitHub Actions avec bac à sable (`logs/github_actions_run_35880776817.log`, conclusion « success » confirmée par l'API). Six vérificateurs de noyau acceptent la preuve.
- **Tests numériques**, qui ne font pas partie de la preuve : graphes T(n) et environ 1 650 réseaux aléatoires, sans aucune violation.

**Audits :** tous faits par Claude, sans relecture humaine. Le dépôt l'écrit : « Aucune relecture humaine indépendante à ce jour ».
- Incidents : deux plantages de mémoire (`leanchecker`, `con-leche`), qui n'étaient pas des rejets de la preuve.
- Correction de littérature : {1, 2, 7, 11, 77} → {1, 2, 7, 11}.
- Dépendances retirées : Ishida (v1 → v2) puis Makhnev–Minakova (lemme 7).
- Ma propre relecture des étapes 1 à 6, du §4 et du lemme 7 ne trouve pas d'erreur. Ce n'est pas un arbitrage.

**Lacunes restantes :**
- Aucune relecture par un tiers humain.
- Le Cor 8 n'est pas formalisé (MM04, CW25 et BL11 y sont admis), et il est dépassé depuis C7.
- La « Généralisation » (remarque du §6) n'est pas démontrée (voir §4).

**Fichiers :** `c3formal/Challenge.lean`, `c3formal/C3formal/FixLemma.lean` (`C3.no_order3`), `AUDIT_ENONCE.md`, `pdf/preuve_c3.tex`, `notes/P1_recollement.md`, `JOURNAL.md`.

---

## 2. C7 (`/home/user/amazing-source/conway-C7`, 02/10)
**Énoncé** (`tex/order7.tex`, Thm 1.1) :
> « A strongly regular graph with parameters (99,14,1,2) has no automorphism of order 7. Consequently, 7 does not divide the order of its automorphism group. »

**Cor 1.2 :** « either |Aut Γ| divides 6, or |Aut Γ| is odd and divides 3³·11 ».

**Architecture :**
1. **Orbites.** Unique point fixe x. Le voisinage de x forme deux 7-cycles L et R. Le reste forme 12 orbites extérieures : 3 LL, 3 RR, 6 mixtes.
2. **Identités.** La matrice C (12×12) vérifie C𝟙 = 12𝟙, Cu = 0 et C² + C = 12I + 12J − 2uuᵀ. C'est la forme close de CW25 Eq. (5).
3. **Diagonale nulle.** L'irréductibilité de Φ₇ donne 54 − d ≡ 0 (mod 6), d'où a = 4 et tr C = 0.
4. **Compression de Gram (l'étincelle, due à ChatGPT).** G = 3C + 12I − 4J − 2uuᵀ vaut 21 fois un projecteur de rang 4 : ce sont 12 vecteurs de R⁴.
5. **Bloc LL/RR.** C_aa′ ≥ 1, puis h ∈ {3, 4, 5} par Cauchy–Schwarz, puis les résidus α et l'identité √α_l = √α_j + √α_k. Il reste **six configurations** (Thm 7.6).
6. **Orbites mixtes.** On décompose R⁴ = W⁻ ⊕ W⁺. La ligne a₁ de C aboutit alors à une somme de carrés impossible dans les six cas.

**Mathématique pur ou assisté par ordinateur :**
- **Le papier est sans ordinateur.**
- **Le Lean ne formalise pas l'analyse de cas faite à la main** des §§ 6–8. Il la remplace par un recensement fini (29 blocs étiquetés) vérifié par `decide +kernel`, et produit par un script non fiable (`gen_core.py`) dont le noyau Lean revérifie le résultat. Les §§ 3–5 sont formalisés de façon structurelle (la diagonale nulle par une autre voie : traces et C_ii ≤ 3).
- Axiomes standard uniquement. Le comparateur a tourné **seulement sous Windows sans bac à sable** ; le journal l'écrit lui-même : « WARNING: Sandbox disabled, this run is not trustworthy ». Le mode paranoïaque passe (lean4lean : 34 354 déclarations).
- Un workflow CI existe, mais **aucun journal de CI n'est présent** dans le dépôt.

**Nouveauté :**
- **Le dépôt reconnaît explicitement BL11.** README : « The exclusion of order 7 was known before only through the computer-aided orbit-matrix computations of Behbahani and Lam (2011) ». Le résumé dit la même chose.
- Il cite aussi Lou–Murin 2014 (point fixe unique, tr ∈ {0, 14}), Walker 2026 (énumération par ordinateur, avec déjà la diagonale nulle) et Machuca 2026 (réfutation SAT certifiée DRAT).
- **Ce qui est nouveau :** une preuve **sans ordinateur** du cas cyclique Z₇ que CW25 laissait ouvert, c'est-à-dire exactement le cas « Z₇ à un point fixe ».
- **Sur Thakkar–Severini (TS26).** Leur v2 (vérifiée en ligne) dit « Order 7 is restricted but not ruled out ». Cela contredit BL11, qu'ils citent pourtant, et ils attribuent à tort à CW25 l'exclusion des ordres 9 et 11. La formulation du papier C7, « open from the computer-free point of view », est la bonne.
- **Ce qui est publiable :** les §§ 6–8 (compression de rang 4 et analyse de cas), comme complément de CW25.

**Audits :**
- « independently audited » (README) signifie que Claude a audité le jet de ChatGPT. Il n'y a pas d'audit humain.
- Mes vérifications : `checks/*.py` concordent avec le papier. Ma recherche indépendante du problème matriciel (diagonale nulle) trouve 0 solution, et le contrôle positif fonctionne.

**Fichiers :** `tex/order7.tex`, `order7.pdf` (14 pages), `lean/Challenge.lean`, `lean/Conway7/Final.lean`, `lean/logs/`, `checks/`, `scripts/fullsearch.c`.

---

## 3. Autres découvertes

| Énoncé | Type | Statut | Nouveauté | Fichiers |
|---|---|---|---|---|
| Lemme de recollement : pour une action libre de C₃ et un projecteur 3-entier, d₁ ≡ d_ω (mod 3) ; étendu aux points fixes quand β = 0 | lemme sur les réseaux | DÉRIVÉ + testé (≈1 650 cas aléatoires, 318 avec β = 0) | plausible | `notes/P1_recollement.md`, `scripts/glue*.py`, `logs/glue*.log` |
| Critère p = 3 général : exclut une action libre d'ordre 3 pour (105,52,21,30), (105,52,29,22), (261,52,11,10), (714,248,97,80), (1221,610,279,330), (1221,610,329,280) ; avec points fixes (β = 0) aussi (722,103,12,15) et (1148,481,210,195) | corollaire sur les familles de srg | heuristique de script, **sans preuve générale écrite** ; je n'ai vérifié à la main que (714,248,97,80) | oui si démontré | `scripts/criterion_scan*.py`, `logs/criterion_scan*_1300.log` |
| Tous ces jeux de paramètres sont « ? » dans les tables de Brouwer | vérification | j'ai contrôlé sur les copies | — | `data/brouwer_srgtab*.html` |
| d_S = d₁·d_ω² (le réseau complet ne voit pas l'obstruction) | observation | « DÉRIVÉ » sans preuve écrite trouvée | faible | `IDEES.md` D10, `logs/D10_dS.log` |
| Extension à C_p (symboles de Legendre ; graphe de Moore à p = 13, srg(352,26,0,2), srg(1276,50,0,2)) | piste | spéculation, non réalisée (PARI absent) | — | `IDEES.md` D3 |
| Preuve élémentaire de « Fix vide ou triangle » (MM04) | lemme | vérifié en Lean | nouvelle preuve | `FixLemma.lean` |
| τ = 6 par modules projectifs sur Z₃[C₃] (sans Ishida) | lemme | [D], rendu inutile par le Thm 5 | mineure | `rapport/audit_c3.tex` §2 |
| f = 27 d'infinityscroll redondant ; « pas de C₄ » et « lemme B » d'ibenarb impliqués par l'étage quotient | remarques | [D] | — | `rapport/nuit.tex` |
| BvLS srg(243,22,1,2) : contrôle des modèles (81 + 81 orbites) et identité d'Ishida à p = 2 | validation | fait | — | `validate_quotient.py`, `validate_lean.py` |
| Outillage SAT : totalizer tronqué (×20–30), symétries lex-leader (lemme démontré), cubes à « deux doubles » | méthode | validé | technique | `lean_encoding.py`, `stageq_sym.py`, `cube_q_inc.py` |
| Pistes négatives : condition spectrale sur C, LQB, phases globales, ansatz | négatif | [N] | — | `rapport/nuit.tex` |
| C7 : H = 12I + 3J − 2uuᵀ − 4C vérifie H² = 28H | remarque | script uniquement | — | `scripts/norank.py` |

Aucun résultat sur des codes correcteurs dans ces dépôts. Les « réseaux » sont ceux du discriminant.

---

## 4. Incohérences, erreurs, surclaims
1. **`conway99-c3` est périmé.**
   - README : « Rien n'est encore décidé ».
   - LISEZMOI : « rien n'a été poussé sur GitHub », alors que le journal (11:05) note la publication du dépôt.
   - Le résumé et le tableau B du rapport (classe 4 « non ») contredisent ses propres annexes.
   - Rien ne renvoie à la preuve du dépôt expérimental.
2. **Corollaires non croisés.** Le Cor 8 (C3) ignore C7, et le Cor 1.2 (C7) ignore C3. L'énoncé combiné sans ordinateur, |Aut| ∈ {1, 2, 11}, n'apparaît nulle part.
3. **Ordre 11.**
   - Les dépôts ne l'excluent que via Lou–Murin, avec la mention « non vérifié ». Wilbrink 1984 n'y est cité que pour la structure locale.
   - Le texte de CW25, que j'ai consulté en ligne, ne l'exclut pas.
   - Votre registre attribue l'exclusion à Wilbrink 1984. C'est **à vérifier à la source** : si c'est exact, on obtient |Aut| ∈ {1, 2} entièrement sans ordinateur.
4. **Surclaim C7.** « independently audited » désigne un audit par une IA. La CI est annoncée, mais aucune trace d'un run réussi n'est dans le dépôt.
5. **Le Lean de C7 ne vérifie pas l'argument écrit à la main des §§ 6–8.** Il vérifie le théorème par recensement fini.
6. **Remarque « Généralisation » de C3.** Les conditions sont informelles (« vérifiées au cas par cas »). Le script retire de son produit, sans justification écrite, les premiers qui divisent k − θ′.
7. **Nombre de pages faux.** `audit_c3.pdf` est annoncé à 18 pages et en fait 19 ; `preuve_c3.pdf` à 6 pages et en fait 7.
8. **Statut de l'entrée « sans point fixe ».** Dans `conway99-c3`, elle est étiquetée « articles de revues », alors que Behbahani–Lam est un résultat assisté par ordinateur. La question est levée ensuite par le lemme 7.
9. **Hygiène avant publication.** Le dépôt expérimental redistribue des données de tiers (texte d'Ishida, tables de Brouwer), ainsi que des binaires `.exe`/`.zip` et `__pycache__`. Son propre README demande de retirer `data/` avant publication.
10. **Paternité.** C7 nomme « ChatGPT and Claude » comme auteurs. C'est en principe incompatible avec les politiques d'arXiv et de la plupart des revues (les auteurs doivent être des humains responsables) ; à vérifier avant soumission.

---

## 5. Publications possibles (par ordre)
1. **Pas d'automorphisme d'ordre 3** : obstruction par les discriminants, lemme 7, cas du triangle, Lean. C'est nouveau ; relu seulement par Claude, sans aucune relecture humaine.
2. **C7 sans ordinateur** : solide, mais la nouveauté est de méthode seulement.
3. **Critère p = 3 pour toute la famille des srg** : il faut d'abord écrire le théorème général et sa preuve.
4. **Article de formalisation** : les deux développements Lean et le contrôle des énoncés par `comparator`.
5. **Pipeline SAT de C3** : il n'est plus utile. Au mieux un appendice ou une remarque (τ = 6 par modules projectifs).

**Regroupement suggéré :**
- **Article A** : (1) + (2) + l'énoncé combiné « |Aut Γ| ∈ {1, 2, 11} sans ordinateur », et {1, 2} si l'ordre 11 est réglé à la source (Wilbrink ou Lou–Murin) ; {1, 2} de toute façon avec BL11.
- **Note B** : (3).
- **Papier C**, pour un public de méthodes formelles (type ITP/CPP) : (4).

Sources consultées en ligne : [Thakkar–Severini, arXiv:2608.11211](https://arxiv.org/pdf/2608.11211), [Cesarz–Woldar, arXiv:2308.02978](https://arxiv.org/abs/2308.02978), [Wikipédia](https://en.wikipedia.org/wiki/Conway%27s_99-graph_problem).