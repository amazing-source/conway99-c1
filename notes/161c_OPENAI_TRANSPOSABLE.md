# 161c — Dépôt openai/math : ce qui est transposable à Conway (07/10)

*Rapport d’un agent de lecture, versé tel quel. Il couvre les 372 familles, les sources LaTeX et les dossiers lean/ et
verification/. Le vérificateur de l’article Hadamard-6 a été audité puis exécuté en isolation (python3 -I).*


**Verdict global.** Aucun manuscrit n'attaque le problème, directement ou indirectement. Un seul article apporte une technique mathématique qu'on peut raisonnablement transposer : les certificats de moments exacts de l'article sur les matrices de Hadamard d'ordre 6 (rang 1 ci-dessous). Deux autres n'apportent qu'une méthode pour certifier de gros calculs (rangs 2 et 5). Tout le reste est non transférable, et j'explique pourquoi pour chacun.

**Périmètre du balayage.**
- J'ai parcouru les 372 familles de `/home/user/openai/math/overview.tex` (17 disciplines) et fait des recherches sur toutes les sources `.tex` de `preprints/*/build/`.
- **Absents de toute la collection :** DRAT/LRAT, nauty, partial difference set, Terwilliger, spherical design, star complement, Seidel switching / two-graph, MacWilliams / code autodual, Bose–Mesner, quadrangle généralisé, Moore graph.
- **Faux positifs :**
  - « strongly regular » n'apparaît que dans Borsuk (mention historique) et dans un article de Langlands (« strongly regular semisimple », sans rapport).
  - « Krein » ne désigne que des espaces de Krein (analyse).
  - « association scheme » n'apparaît que chez Sidorenko.
  - « Delsarte » n'apparaît que dans la bibliographie de l'article Hadamard-6.
- J'ai aussi regardé `lean/` (`formalization.yaml`, `docs/`, `ComparatorChallenges/`) et `reasoning_traces/` (10 PDF, rien de pertinent).

---

## 1. Certificats de Fourier exacts pour les matrices de Hadamard complexes d'ordre 6 — **PEUT-ÊTRE (meilleur candidat)**

`/home/user/openai/math/preprints/Exact-Fourier-certificates-for-complex-Hadamard-matrices-of-order-six-September-24-2026/`

**Ce qui est prouvé.**
- La conjecture d'annulation de Fourier de Matolcsi–Ruzsa–Weiner : toute matrice de Hadamard complexe 6×6 non équivalente à la matrice cubique S₆ a g_H(πα)=0 pour toute permutation de α=(1,1,1,−1,−1,−1).
- Il n'existe pas 7 bases mutuellement non biaisées dans ℂ⁶, donc N(6) ≤ 5 (par le théorème de complétion de Weiner).

**Technique.** Ce n'est pas un LP de Delsarte mais une hiérarchie de moments finie, avec des certificats exacts :
1. **Moments injectifs** (`build/sections/02-pair-moments.tex`, éq. injective-moment) : m_H(A) = moyenne, sur des injections uniformes lignes/colonnes, d'un monôme en les entrées. On a |m_H| ≤ 1.
2. **Lemme de contraction** (Lemma `lem:contraction`) : l'orthogonalité, sommée sur une étiquette de ligne libre, donne la relation linéaire exacte (7−p)·m(A) = −Σ_ℓ m(A_{i→ℓ}). Le facteur de taille finie (7−p) est essentiel. Quand plus aucune étiquette n'est libre (p=7), elle devient Σ_ℓ m(A_{i→ℓ}) = 0.
3. **Développement par motifs d'égalité** (Lemma `lem:partitions`) : un produit de sommes de caractères se développe en somme sur les partitions d'ensembles, avec les coefficients (6)_k/6ⁿ.
4. **Certificat « somme de carrés = 0 »** (Prop. `prop:pair-certificate`) : 3⟨|L|²⟩ + ⟨|g(α)g(q)|²⟩ = 0, identiquement modulo les relations. Chaque terme s'annule donc, ce qui donne une dichotomie structurelle : (M), ou bien H∘H est Hadamard.
5. **Certificat mixte** (`04-mixed.tex`, Lemma `lem:gram`) :
   - on moyenne sur une colonne partagée z, ce qui rend les entrées de Gram des fonctions-test égales à des moments à 3 facteurs ;
   - six formes quadratiques entières sont définies positives (98 pivots positifs vérifiés exactement) ;
   - après substitution, la constante vaut −613302797399911/6480, et la somme des valeurs absolues des autres coefficients vaut 179721388988719/6480 (échelle 5·10¹⁵) ;
   - comme tous les moments sont bornés par 1, c'est une contradiction.
6. **Substitutions exactes** (`05-verification.tex`, Lemma `lem:exact-elimination`) :
   - élimination modulo 10⁹+7 puis d'autres modules, restes chinois, reconstruction rationnelle ;
   - puis vérification entière exacte de WP=0. Ce test est valable pour tout vecteur réel de moments, même non rationnel.

**Statut.**
- Un vérificateur Python (bibliothèque standard seulement) est fourni : `verification/verify.py`, lancé via `run.py` avec contrôle SHA-256. Je l'ai audité (aucune entrée/sortie fichier ni réseau, que des imports de calcul).
- Je l'ai exécuté sur une copie isolée (`python3 -I`, 74 s). La sortie est identique à l'annexe A : `rank table: 8871 909 897`, `46041 3429 2767`, et la ligne finale.
- Pas de formalisation Lean.

**Transfert à srg(99,14,1,2).** La correspondance est naturelle :

| Hadamard 6 | srg(99,14,1,2) |
|---|---|
| H unimodulaire, HH* = 6I | A ∈ {0,1}^{99×99}, (A−3I)(A+4I) = 2J |
| moment injectif m_H(A) | densité injective d(P) d'un motif induit étiqueté P sur t sommets, normalisée par (99)_t |
| contraction (7−p) | sommer sur un sommet libre x ∉ P : Σ_x A_{ux} = 14 − deg_P(u) ; Σ_x A_{ux}A_{wx} = λ ou μ moins le compte interne. Cela donne des relations exactes avec le facteur (99−t). |
| colonne partagée z | sommet commun z (équivaut à utiliser le vecteur v_z de la représentation euclidienne, Gram 27I−9A+J) |
| formes de Gram positives | matrices E_σ[F_iF_j] ⪰ 0 pour des comptages d'extensions enracinés en un type σ (sommet, arête, non-arête, triangle, P₃…) |

**Ce qu'on calculerait concrètement.**
1. Énumérer les motifs à t ≤ 6 ou 7 sommets compatibles avec les contraintes locales : pas de K₄, pas de « diamant » K₄−e (λ=1), pas de paire non adjacente ayant 3 voisins communs (μ=2). On attend quelques centaines à quelques milliers de classes.
2. Engendrer toutes les relations de contraction et de marginalisation, avec les coefficients exacts en n=99.
3. Résoudre numériquement le dual SDP : chercher des Y_σ ⪰ 0 donnant c₀ + Σ|c_P| < 0 (ou mieux, un LP qui utilise d(P) ≥ 0 et la normalisation).
4. Arrondir en entiers et revalider exactement : pivots positifs pour Y_σ, élimination modulaire puis vérification de WP=0, exactement comme dans `verify.py`.

**Évaluation honnête.**
- Les conditions à 3 points ont beaucoup de marge :
  - Krein : (r+1)(k+r+2rs) = −28 ≤ 153 et (s+1)(k+s+2rs) = 42 ≤ 160 ;
  - bornes absolues : 1034 et 1539, très loin de 99.
- Un certificat de bas degré est donc très improbable ; il faudrait au moins 6 à 7 sommets.
- Des approches SDP de type Schrijver / Terwilliger / Lasserre pour l'existence de SRG existent dans la littérature. À ma connaissance, aucune n'a exclu srg(99,14,1,2) ; je ne peux pas le vérifier ici.
- **Leçon tirée de l'article lui-même :** il cite Bandeira–Doppelbauer–Kunisky, selon qui les relaxations de degré ≤ 6 sur une seule matrice ne battent pas la borne de 7 bases. Le succès vient du couplage de plusieurs « vues » (plusieurs matrices de transition) et d'un ordre total plus élevé. Pour le 99-graphe, il faudrait donc coupler plusieurs types de racines simultanément, avec le sommet partagé z.
- **Gain le plus réaliste :** une identité « somme de carrés = 0 » de type (4), qui force des égalités structurelles (par exemple, un certain comptage local constant en chaque sommet ou chaque arête). Ces égalités pourraient être injectées comme contraintes dans CP-SAT. Le dual SDP indique précisément ces directions forcées.

---

## 2. Snaky in 21 Maker moves — **PEUT-ÊTRE, uniquement comme méthode de certification**

`/home/user/openai/math/preprints/Snaky-in-21-Maker-moves-September-25-2026/`
Lean : `/home/user/openai/math/lean/OAI/GameTheory/SnakyTwentyOne/` (94 fichiers, 5,2 Mo) et `/home/user/openai/math/lean/OAI/Combinatorics/SnakyCertificate/`

**Ce qui est prouvé.** Maker obtient l'hexomino Snaky en 21 coups (plateau infini ; un sous-plateau fixe de 251 cases suffit).

**Technique.**
- Le certificat est un DAG de « cartes » (ensemble requis A_i, enveloppe T_i, hauteur h_i), toutes composées par une seule règle de combinaison prouvée une fois (`build/certificate-proof.tex`).
- Les cartes sont réutilisées sous les 8 permutations signées et sous translation : 722 lignes et 4 089 références pour la version 21 coups.

**Statut.**
- Deux reconstructions Python indépendantes et des identités SHA-256 (`verification/`).
- En Lean, le théorème `OAI.SnakyPrototype.snaky_winning_strategy_21_with_legal_states` (`ComparatorChallenges/SnakyTwentyOne.json`, axiomes propext, Quot.sound et Classical.choice seulement).
- Les données sont vérifiées par `decide +kernel`, sans `native_decide`, et un lemme générique `compose` assure la correction.
- **Divergence à noter :** l'appendice de l'article dit que la formalisation ne couvre que la reconstruction de la version 35 coups, alors que `lean/docs/187.md` annonce aussi la stratégie complète en 21 coups. C'est la formalisation qui va plus loin que le texte.

**Transfert.** Le modèle « règle de composition prouvée une fois + données finies vérifiées par le noyau » convient à vos énumérations nauty (configurations locales, arbre de cas sous Z₃). Limites :
- les vérifications de Snaky sont de petites inclusions d'ensembles ;
- des tests sur des matrices 99×99, ou des millions de lemmes DRAT, seraient trop lourds pour `decide` dans le noyau ;
- pour du SAT, il faut un vérificateur LRAT certifié (sous réserve : celui de `bv_decide` repose, je crois, sur `Lean.ofReduceBool`, donc sur la confiance dans le compilateur).

Aucun contenu mathématique transférable.

---

## 3. La conjecture de Hadamard circulante — **NON pour le problème** (outillage Lean marginal)

`/home/user/openai/math/preprints/The-circulant-Hadamard-conjecture-September-23-2026/build/sections/*.tex`
Lean : `/home/user/openai/math/lean/OAI/LinearAlgebra/CirculantHadamard/` (68 fichiers, environ 9 500 lignes)

**Ce qui est prouvé.** Une matrice de Hadamard circulante réelle n'existe qu'en ordre 1 ou 4 ; en conséquence, les longueurs de suites de Barker sont exactement 2, 3, 4, 5, 7, 11, 13. Formalisé : `OAI.CirculantHadamard.exists_iff_order_one_or_four`, axiomes standard.

**Technique.** Équation de norme hh* = n dans ℤ[C_n] :
- descente de Turyn à 2 (`reduction.tex`), qui donne n = 4u² avec u impair ;
- produit alterné de valeurs de caractères Δ(x) = Π_S x_S^{(−1)^{|S|}} (`products.tex`) ;
- Lemma `lem:comparison` : rapports de résidu 1 aux idéaux au-dessus de p, quand la valuation du scalaire égale l'exposant de la composante p ;
- critère de Kronecker : Δ est une racine de l'unité d'ordre impair ;
- au-dessus de 2, les termes du premier ordre vérifient L_{r,S} + L_{w,S} ≡ J_S/c_S ; seul S = ∅ survit, d'où la contradiction (`contradiction.tex`).

**Pourquoi ça ne transfère pas.**
- Tout repose sur une action régulière d'un groupe abélien, qui fournit une équation de norme scalaire. Avec Aut ∈ {1, Z₂, Z₃}, le 99-graphe n'est pas un graphe de Cayley : pas d'ensemble aux différences partielles, aucune prise pour la descente de corps.
- Sous Z₃ semi-régulier (sinon il faut adjoindre le bloc des points fixes), on obtient B = A(ω) ∈ M₃₃(ℤ[ω]), hermitienne, avec (B−3I)(B+4I) = 0. C'est une équation matricielle et non scalaire ; l'astuce de Δ n'a pas d'analogue.

**Remarque marginale.** Dans ℤ[ω], 7 = (2−ω)(2−ω̄) se décompose. P = (B+4I)/7 est un projecteur, ce qui définit un réseau hermitien sur ℤ[ω] dont les invariants locaux aux deux premiers au-dessus de 7 raffinent vos invariants de classe mod 7. `Kronecker.lean` et la structure de DVR locale (Lemma `lem:local-ring`) sont le type d'outil formel utile pour formaliser cela en Lean, mais les mathématiques sont la théorie standard des réseaux hermitiens. L'article n'apporte rien de nouveau ici.

---

## 4. Nombre maximal de bases mutuellement non biaisées en dimension 6 — **NON**

`/home/user/openai/math/preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026/`

**Ce qui est prouvé.** N(6) = 3, « computer-assisted », sous un contrat d'arithmétique binary64 et de compilateur (`build/sections/introduction.tex`, `rounding.tex`).

**Méthode.**
- Recouvrement de toutes les deuxièmes bases par des boules de phases.
- Étape A : complétion via un recouvrement de U(2).
- Étape B : raffinement tangent certifié.
- Étape C : boules de vecteurs, puis deux graphes 𝒪 (orthogonalité possible) et 𝒰 (non-biais possible) ; on exclut deux 6-cliques disjointes de 𝒪 avec 36 arêtes croisées dans 𝒰 (`exclusion.tex`).

**Statut.** Le code cité (`verification/code/*.cpp`, `extraction.json`) est **absent** de la publication : le dossier ne contient que `build/` et le README. Le résultat n'est donc pas vérifiable en l'état.

**Pourquoi ça ne transfère pas.** C'est un espace de modules continu. Votre problème est discret, avec une représentation euclidienne algébrique exacte ; un recouvrement flottant certifié n'apporte rien. Seule l'exclusion de cliques finale est générique, et vos outils SAT/nauty font mieux.

---

## 5. Nombres de Ramsey cycle–clique — **méthodologie, faible**

`/home/user/openai/math/preprints/Cycle-clique-Ramsey-numbers-September-25-2026/`

**Méthode.** Les cas finis sont traités par des règles de propagation prouvées (`build/sections/09-finite-rules.tex`). Des traces de déduction en JSONL (tours de propagation, chacun avec son témoin) se trouvent dans `verification/data/certificates.jsonl` ; elles sont revérifiées par deux vérificateurs indépendants (`verify.py`, `independent_checker.py`).

**Transfert.** C'est un modèle de journal de preuve spécifique au domaine, intermédiaire entre DRAT brut et formalisation complète. Utile pour des exécutions CP-SAT, qui n'émettent pas de DRAT. Rien de mathématique.

---

## 6. Nombre de croisements de K_n — **NON** (l'idée est déjà dans votre boîte à outils)

`/home/user/openai/math/preprints/The-crossing-number-of-complete-graphs-September-23-2026/build/main.tex`

**Technique.** Méthode polynomiale ; l'image d'évaluation est totalement isotrope pour une forme symétrique non dégénérée, donc sa dimension est au plus la moitié du nombre de coordonnées.

**Analogue pour le 99-graphe.**
- M = 27I − 9A + J vérifie M² = 63M ≡ 0 (mod 7). L'espace des lignes mod 7 est donc totalement isotrope, d'où rang₇(M) ≤ 49.
- On a aussi (A−3I)(A+4I) = 2J.
- C'est l'argument classique de p-rang / code auto-orthogonal, sans doute déjà couvert par vos invariants mod 7. L'article n'ajoute rien.

---

## 7. Réseaux et certificats d'optimalité (3 articles) — **NON**

- `/home/user/openai/math/preprints/Universal-optimality-of-the-triangular-lattice-September-23-2026/`
- `/home/user/openai/math/preprints/An-atomic-certificate-for-triangular-lattice-universal-optimality-September-26-2026/`
- `/home/user/openai/math/preprints/A-sharp-Fourier-certificate-for-planar-circle-packing-September-23-2026/`

**Technique.** Fonctions auxiliaires de type Cohn–Elkies / Cohn–Kumar–Miller–Radchenko–Viazovska dans ℝ², certifiées par arithmétique d'intervalles (code fourni).

**Pourquoi ça ne transfère pas.** La représentation euclidienne du 99-graphe (99 vecteurs unitaires de ℝ⁴⁴, produits scalaires −2/7 et 1/28) est un ensemble sphérique à deux distances et un 2-design. Elle sature les conditions LP à deux points de Delsarte ; un certificat à deux points ne peut pas l'exclure. Il faut au moins trois points (SDP), ce qui renvoie au rang 1. Aucun article sur Leech, les séries thêta de réseaux de graphes ou les codes : « theta series » n'apparaît qu'en théorie des nombres (BSD, formes modulaires).

---

## 8. Non transférables (vérifiés)

- **Borsuk en dimension 9** (`A-nine-dimensional-counterexample-to-Borsuks-covering-assertion-September-23-2026/build/sections/introduction.tex`) : les SRG n'y apparaissent qu'à titre historique (ensembles à deux distances de Bondarenko, Jenrich–Brouwer). La preuve est topologique (degré mod 2 d'applications impaires sur ℝP³, puis obstruction combinatoire sur 10 étiquettes). Formalisée dans `lean/OAI/Geometry/Borsuk/Counterexample.lean`. Rien pour srg(99).
- **Sidorenko** (`A-counterexample-to-Sidorenkos-conjecture-September-23-2026/build/sections/introduction.tex`) : le « schéma d'association » est celui des matrices symétriques sur F_q (Huo–Wan). Il sert à construire un noyau à corrélation négative ; c'est asymptotique et constructif.
- **Ryser** (`A-Counterexample-to-Rysers-Covering-Conjecture-September-23-2026/build/paper.tex`) : plans projectifs sur F_{s^n} plus estimations probabilistes, pour s et n grands. Formalisé dans `lean/OAI/Combinatorics/Ryser/`. Non.
- **Graphes de Ramanujan déterministes** (`Deterministic-nonbipartite-Ramanujan-graphs-in-every-fixed-degree-September-23-2026/`) : asymptotique, par switches d'arêtes. srg(99) est trivialement Ramanujan (max|θ| = 4 < 2√13 ≈ 7,21). Non.
- **Autres familles parcourues, sans prise :**
  - complexité de Weisfeiler–Leman ;
  - mélange de la chaîne de switches (switch d'arêtes, pas le switching de Godsil–McKay) ;
  - plan non 5-colorable (preuve analytique, pas de SAT) ;
  - Saxl / Foulkes ; Alperin / Donovan ; groupes infinis ; cônes d'hyperbolicité.
  - Les lemmes de trace d'adjacence dans `lean/OAI/Combinatorics/TriangleRemoval/Spectral/` ne servent que si vous formalisez le comptage de triangles via tr A³.

---

## Recommandation

1. **Seul essai mathématique qui vaille :** implémenter la hiérarchie de densités injectives du rang 1 pour srg(99,14,1,2). Concrètement : motifs à ≤ 6 ou 7 sommets, contraction exacte en n=99, Gram enracinées avec sommet partagé, puis arrondi et revalidation exacte en reprenant `verify.py` comme modèle. Viser d'abord les égalités forcées (directions nulles du dual), à injecter dans CP-SAT, plutôt qu'une contradiction directe, qui est peu probable.
2. **Pour certifier vos calculs :** reprendre le modèle de Snaky (règle de composition prouvée une fois + `decide +kernel` sur les données) et celui des traces JSONL avec double vérificateur (rang 5).
3. Ne rien attendre de la descente de corps, des certificats de Fourier à deux points, ni du recouvrement certifié en binary64.