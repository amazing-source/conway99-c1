# 3. Topologie du complexe triangles-carrés et géométrisation des srg(v, k, 1, 2) (test T5)

Statuts : **[P]** démontré ici · **[L]** littérature · **[E]** calcul reproductible · **[A]** analogie ·
**[C]** conjecture · **[O]** ouvert ou obstacle formulé.

Condition T5 du premier travail : un invariant topologique non trivial, pour un min-max à dérive négative (S7).
Chez Perelman, c'est une classe non triviale de π₂ ou π₃ qui rend la largeur positive tant que la variété existe. Ce
chapitre construit l'invariant naturel, le calcule sur toute la famille connue, et montre exactement pourquoi il ne
donne rien pour Conway. En chemin, on obtient une description structurelle de la famille entière.

---

## 3.0 Ce que l'équipe avait déjà

- **F21 (Hodge)**, `notes/10_IDEES_F.md` : sur le complexe K de Conway, L₁ = 15I + Q, d'où H₁(K; ℚ) = 0.
- **L1**, `notes/30_LEMMES.md` (résultat de Makhnev 1988, Mat. Zametki 44(5), Thm 2 ; preuve indépendante de l'équipe) :
  Γ est tordu. Grid-full ⇒ le revêtement universel de K est H(7, 3) ⇒ 99 | 3⁷, absurde. Remarque de l'équipe : pour un
  pg(2, t, 2) grid-full, v est une puissance de 3.
- **F2′**, `notes/20_ATTAQUES_R.md` : revêtement universel et divisibilité. La piste est tuée hors du diamètre 2, et
  ouverte pour le srg. Les géométries tordues t2, t3 ont H₁ = 0 sur 𝔽₂, 𝔽₃, 𝔽₅, 𝔽₇ et ℚ ; elles sont « déjà
  universelles ».
- **Note 165** : étalement régulier ⟺ revêtement triple du graphe de Brouwer–Haemers BH = srg(81, 20, 1, 6). Il n'y a
  pas d'étalement régulier pour v = 99, 6273, 494019. La torsion est la courbure d'une connexion ℤ₃ sur BH. Dichotomie :
  (a) ℤ₃-revêtement, ou (b) monodromie S₃.

**Ce qui est nouveau ci-dessous :**
- l'étude de π₁(X) et H¹(X; 𝔽_p) pour toute la classe : finitude, structure locale des revêtements, codes parfaits ;
- la jauge radiale, qui localise la cohomologie ;
- les classes d'étalement comme classes de cohomologie ;
- le calcul exact de π₁ pour les huit srg(243) connus, dont les quatre sans étalement de l'équipe, avec leurs
  revêtements universels.

---

## 3.1 Le complexe et ses revêtements

Pour G ∈ 𝒦_k (chapitre 2), X(G) est le 2-complexe dont les 2-cellules sont les triangles (les droites) et les
quadrangles. Dans 𝒦_k, tout 4-cycle est induit, et chaque paire à distance 2 est la diagonale d'exactement un
quadrangle. Pour Conway : 99 sommets, 693 arêtes, 231 triangles et 2079 quadrangles. On a donc χ = 1716 et, avec
b₁ = 0, b₂ = 1715.

**Lemme 3.1 (boucles courtes)** [P]. Toute marche fermée de longueur ≤ 4 dans G ∈ 𝒦_k est homotope à zéro dans X(G).

*Preuve.* On retire les allers-retours, ce qui raccourcit la marche. Une marche fermée sans aller-retour de longueur 3
est un triangle. De longueur 4, uabcu, on a b ≠ u et c ≠ a. Si b ∼ u, l'arête ub serait dans les triangles uab et ubc
avec a ≠ c. Donc d(u, b) = 2 ; a et c sont ses deux voisins communs, et la marche est le bord d'un quadrangle. ∎

**Corollaire 3.2 (revêtements)** [P]. Soit p : X̂ → X(G) un revêtement connexe et Ĝ son 1-squelette.
- (a) Ĝ ∈ 𝒦_k et X̂ = X(Ĝ).
- (b) p envoie B₂(x̂) bijectivement sur B₂(x), et c'est un isomorphisme des 2-boules incomplètes (arêtes ayant une
  extrémité dans B₁).
- (c) Pour toute transformation de revêtement h ≠ 1 et tout x̂, on a d(x̂, h x̂) ≥ 5.

*Preuve.*
- (b) Deux chemins de longueur ≤ 2 issus de x̂, d'extrémités de même image, se projettent en une marche fermée de
  longueur ≤ 4. Elle est homotope à zéro (3.1), donc se relève en marche fermée : les extrémités coïncident. La
  surjectivité vient du relèvement des chemins. Les triangles et quadrangles passant par x se relèvent fermés, d'où
  l'isomorphisme des 2-boules incomplètes.
- (a) Par (b), Ĝ a le même cadre que G en chaque sommet, d'où λ = 1 et μ = 2. Toute marche fermée sans aller-retour de
  longueur 3 ou 4 dans Ĝ se projette sur un triangle ou un quadrangle de G : les 2-cellules relevées sont exactement les
  triangles et quadrangles de Ĝ.
- (c) Un chemin de longueur ≤ 4 de x̂ à h x̂ se projette sur une marche fermée de longueur ≤ 4, homotope à zéro, dont le
  relevé issu de x̂ est fermé. Donc h x̂ = x̂. ∎

*Remarque.* Les arêtes **intérieures** à Γ₂(x) ne se relèvent pas forcément dans B₂(x̂) : c'est exactement là que vit la
cohomologie (§3.4).

---

## 3.2 Finitude du groupe fondamental et taille du revêtement universel

**Théorème 3.3.** Soit G ∈ 𝒦_{2n}, et soit Ũ le 1-squelette du revêtement universel de X(G).
- **(a)** [P ; c'est F21 pour Conway] Si G est fini, le laplacien de Hodge vérifie Δ₁ = ∂₁ᵀ∂₁ + ∂₂∂₂ᵀ = (k + 1)I + S avec
  ‖S‖ ≤ k − 2. Donc Δ₁ ⪰ 3I et b₁(X(G)) = 0.
- **(b)** [P, à partir de L] Ũ ∈ 𝒦_k est fini, de diamètre ≤ ⌊2k/3⌋. Donc **π₁(X(G)) est fini**.
- **(c)** [P] Depuis tout sommet de G ∈ 𝒦_{2n} : |S₁| = 2n, |S₂| = 2n(n − 1) et |S_i| ≤ (n − 2)|S_{i−1}| pour i ≥ 3. Pour
  Conway, |Ũ| ≤ 1 + 14 + 84(1 + 5 + ⋯ + 5⁷) = 8 203 119, donc **|π₁(X(Γ))| ≤ 82 859**.
- **(d)** [C, et P conditionnel] Propriété (L) : tout z ∈ S_i(x) est sur au moins i droites qui rencontrent S_{i−1}(x).
  Sous (L), |S_i| ≤ C(n, i)2ⁱ et |G| ≤ 3ⁿ. Pour Conway, |Ũ| ≤ 2187 et |π₁| ≤ 22. Si de plus H₁(X(Γ); ℤ) = 0, alors π₁
  est parfait, donc trivial (le plus petit groupe parfait non trivial, A₅, est d'ordre 60).

*Preuve de (a).*
- Diagonale : 2 + (1 + (k − 2)), car chaque arête est dans un triangle et dans k − 2 quadrangles.
- Deux arêtes ux, uy ayant un sommet commun : le terme ±1 de ∂₁ᵀ∂₁ est annulé par exactement une 2-cellule. C'est le
  triangle si x ∼ y, et sinon l'unique quadrangle de diagonale xy, par μ = 2.
- Deux arêtes disjointes : S_{ef} est le nombre signé de quadrangles où elles sont opposées.
- Chaque arête est dans k − 2 quadrangles, donc les sommes de ligne de |S| sont ≤ k − 2. On conclut par Gershgorin. ∎

*Preuve de (b).* Ũ est le 1-squelette d'un revêtement, donc Ũ ∈ 𝒦_k par 3.2(a), a priori infini. Le théorème de
Bonnet–Myers de Lin–Lu–Yau, avec κ_LLY = 3/k (Théorème A.2, Li–Liu), donne la finitude et diam ≤ ⌊2k/3⌋
(Huang–Liu–Xia, Combinatorica 2024, Cor. 1.4(ii)). Brouwer–Cohen–Neumaier, Thm 1.13.2, donne déjà diam ≤ k. ∎

*Preuve de (c).* Soit z ∈ S_i avec i ≥ 2, w ∈ S_{i−1} un voisin de z et a ∈ S_{i−2} un voisin de w.
- d(z, a) = 2. Les deux voisins communs de z et a sont w et un w₂ ∈ S_{i−1}, avec w ≁ w₂ (sinon l'arête ww₂ serait dans
  deux triangles). Donc z est sur au moins deux droites qui rencontrent S_{i−1}.
- Symétriquement, pour i ≥ 3, un sommet de S_{i−1} a au moins deux droites vers S_{i−2}. Au plus n − 2 de ses droites
  rencontrent donc S_i.
- Une droite rencontre S_i en au plus deux points, et si c'est deux, elle rencontre S_{i−1} en un seul. Le double
  comptage des couples (sommet de S_i, droite vers S_{i−1}) donne 2|S_i| ≤ 2(n − 2)|S_{i−1}|.

Pour Conway, il reste à sommer jusqu'au diamètre 9. ∎

*(d).* La preuve est la même, avec i au lieu de 2. (L) est démontrée pour i ≤ 2. Le cas i = 3 résiste : ma tentative
bute sur un 8-cycle à deux cordes croisées, et elle n'est pas rédigée ici. Données [E] : 0 violation de (L) sur environ 1,8 million de tests, sur dix
graphes (exp3 : t2, t3, H(3,3), H(4,3), t2□t3, t2□t2 ; exp4 : les quatre revêtements à 729 sommets). La borne 3ⁿ est
l'analogue, pour 𝒦_{2n}, du théorème de Mulder sur les (0,2)-graphes (|V| ≤ 2^k) [L : H. M. Mulder, Discrete Math. 28
(1979)]. Je n'ai pas trouvé de version publiée pour 𝒦_{2n}.

---

## 3.3 Géométrisation : un srg(v, k, 1, 2) est un modèle simplement connexe quotienté par un code parfait

**Théorème 3.4** [P].
- **(a)** Soit Γ un srg(v, k, 1, 2), Ũ son revêtement universel et H = π₁(X(Γ)), qui agit par transformations de
  revêtement. Alors H agit librement sur V(Ũ), **chaque H-orbite est un 2-code parfait de Ũ** (les boules B₂(h x̃),
  h ∈ H, partitionnent V(Ũ)), et Γ ≅ Ũ/H, avec |Ũ| = v·|H|.
- **(b)** Réciproquement, soit G ∈ 𝒦_k fini et H ≤ Aut(G) agissant librement, dont toutes les orbites sont des 2-codes
  parfaits. Alors G/H est un srg(v, k, 1, 2) avec v = 1 + k + k(k − 2)/2, et G → G/H est un revêtement de 2-complexes.
  Si G est simplement connexe, π₁(X(G/H)) ≅ H.

*Preuve.*
- (a) Par 3.2(c), deux points d'une orbite sont à distance ≥ 5, donc les 2-boules de l'orbite sont disjointes. Par
  3.2(b), chacune a |B₂(x)| = v sommets, puisque Γ est de diamètre 2. Comme |H|·v = |Ũ|, elles partitionnent Ũ.
- (b) La distance minimale ≥ 5 dans les orbites rend la projection injective sur les 2-boules. Un triangle ou un
  quadrangle de G/H se relève : deux relevés d'un même sommet dans B₂(x) seraient à distance ≤ 4. Donc G/H ∈ 𝒦_k. Toute
  orbite rencontre B₂(x) (propriété de recouvrement), donc G/H est de diamètre ≤ 2, et c'est un srg par le Corollaire
  2.2. ∎

**Corollaire 3.5 (le cas grid-full)** [P + L]. Si tout carré d'un srg(v, k, 1, 2) avec k ≥ 4 est dans une grille
(condition (∗) de Makhnev), alors **(v, k) ∈ {(9, 4), (243, 22)}**. Dans le second cas, Γ = H(11, 3)/H, et chaque
H-orbite est un code parfait aux paramètres du code de Golay ternaire.

*Preuve.* L'argument L1 de l'équipe donne Ũ ≅ H(n, 3) pour n = k/2. Par 3.4(a), les orbites sont des codes parfaits
2-correcteurs de H(n, 3), de taille 3ⁿ/(2n² + 1). Par le théorème de van Lint–Tietäväinen [L : codes parfaits sur
un alphabet de cardinal une puissance d'un premier], un code parfait 2-correcteur ternaire non trivial a les paramètres
du code de Golay [11, 6, 5]₃. Un code trivial a un seul mot, ce qui impose 3ⁿ = 2n² + 1, soit n = 2. ∎

Ce corollaire précise la remarque de L1 (« v est une puissance de 3 ») : seuls 9 et 243 sont possibles. Il est
probablement connu sous une autre forme ; je ne l'ai pas trouvé dans les notes de l'équipe.

**BvLS.** BvLS est le graphe des classes du code de Golay ternaire C [L], c'est-à-dire H(11, 3)/C pour les translations
de C. Le complexe de H(n, 3) est le 2-squelette du produit (Δ²)ⁿ, qui est contractile, donc X(H(n, 3)) est simplement
connexe [P]. Par 3.4(b), **π₁(X(BvLS)) ≅ C ≅ (ℤ/3)⁶** [P]. Le calcul le confirme [E] : l'énumération de classes donne un
revêtement universel à 177 147 = 3¹¹ sommets.

[A] C'est le schéma de Thurston : chaque Γ est un modèle simplement connexe quotienté par un groupe agissant librement.
Le graphe de Hamming joue le rôle de l'espace plat, les codes parfaits celui des réseaux, et BvLS est le « tore plat » de
la famille. Les graphes tordus ont d'autres modèles (§3.6).

---

## 3.4 La jauge radiale : où vit la cohomologie

On reprend les notations du §2.4 : pour w ∈ Γ₂(x), avec N(w) ∩ N(x) = {a, b}, B_xw est le graphe d'appariement entre
X″ = N(x) \ {a, b} et Y″ = N(w) \ {a, b}. Il est fait de deux chemins et de cycles pairs.

**Théorème 3.6 (jauge radiale)** [P]. Soit Γ un srg(v, k, 1, 2), x un sommet et A un groupe abélien.
- (i) Toute classe de H¹(X(Γ); A) a un **unique** représentant c nul sur toutes les arêtes ayant une extrémité dans
  B₁(x).
- (ii) Ce c est porté par les arêtes intérieures à Γ₂(x). Pour chaque w ∈ Γ₂(x), la fonction w′ ↦ c(w → w′) sur Y″ est
  **nulle sur les deux chemins** de B_xw et **constante sur les sommets Y″ de chaque cycle**.
- (iii) Réciproquement, H¹(X(Γ); A) est isomorphe au groupe des fonctions antisymétriques c sur les arêtes orientées de
  Γ₂(x) qui vérifient (ii) et les conditions de cocycle sur les triangles et quadrangles contenus dans Γ₂(x).

*Preuve.*
- *Existence.* Soit c un cocycle. On pose f(x) = 0, f(u) = c(x → u) pour u ∈ N(x), et f(y) = c(x → a) + c(a → y) pour
  y ∈ Γ₂(x) de voisins a, b dans N(x). Ce f est bien défini grâce au quadrangle xayb. Alors c − δf est nul sur les
  arêtes x–u et u–y, et sur les arêtes u–u′ de N(x) par le triangle xuu′.
- *Unicité.* Si δg est nul sur ces arêtes avec g(x) = 0, alors g est nul sur B₂(x) = V.
- *Contraintes (ii).*
  - Pour u ∈ X″ \ {a′, b′} de voisins w′, w″ dans Y″, le quadrangle u w′ w w″ donne c(w → w′) = c(w → w″) : constance
    le long de chaque composante.
  - Le quadrangle a′ w′ w a, où w′ est le voisin de a′, donne c(w → w′) = 0.
  - Le triangle w a a″ donne c(w → a″) = 0.
  - La nullité se propage le long des deux chemins.
- *(iii).* Les 2-cellules qui rencontrent B₁(x) sont les triangles xuu′ et uyy′, les quadrangles xayb, uw′ww″, a′w′wa
  et uu′y′y. Il n'y a pas de quadrangle avec deux sommets opposés dans N(x), car μ = 2. Sous (ii), les conditions de
  cocycle de toutes ces cellules sont satisfaites. Il ne reste que les cellules intérieures à Γ₂(x). La bijection
  c ↦ [c] vient de l'existence et de l'unicité. ∎

**Corollaire 3.7** [P]. S'il existe un sommet x tel que tous les graphes B_xw, w ∈ Γ₂(x), sont sans cycle, alors
H¹(X(Γ); A) = 0 pour tout A, donc H₁(X(Γ); ℤ) = 0. En effet H¹(X; A) = Hom(H₁(X), A), puisque H₀ est libre ; on
prend A = ℚ/ℤ, et H₁ est fini. Sous (L), on a alors π₁ = 1.

**Données** [E] (`exp10_transport_graphs.py`, `exp1_curvature_topology_243.py`).
- BvLS : chaque B_xw a exactement six hexagones, et dim H¹(𝔽₃) = 6.
- Graphes tordus à 243 : de 1 à 6 composantes cycliques.
- Dans les revêtements triples, les cycles de valeur non nulle sont exactement ceux qui disparaissent : leurs sommets X″
  deviennent isolés, à distance 3. On le voit sur la distribution du nombre de cycles par paire : BvLS {6} devient
  {0, 4} ; le jumeau {2, 3, 4, 6} devient {0, 1, 2, 4}.
- t2 et t3 (diamètre 3, hors du cadre du théorème) n'ont aucun cycle, et sont simplement connexes : c'est cohérent.
- Γ₅ à Γ₈ (sans étalement) ont de 0 à 6 cycles par paire et pourtant H¹ = 0 (exp11). Les cycles sont donc nécessaires à
  une classe, pas suffisants : ce sont les conditions de cocycle intérieures à Γ₂(x) qui tranchent.

[A] La jauge radiale est l'analogue fini d'une jauge en coordonnées normales. Toute la cohomologie se lit sur la 2-boule
d'un sommet, et plus précisément sur les cycles des graphes d'appariement. L'invariant topologique devient ainsi un
objet combinatoire local, du type de ceux que l'équipe étudie.

---

## 3.5 Les étalements réguliers donnent des classes mod 3

**Proposition 3.8** [P]. Soit Γ un srg(v, k, 1, 2) muni d'un étalement régulier 𝒮 (note 165), dont les droites admettent
une orientation compatible avec tous les couplages de prismes (cas (a) de la note 165). On pose c = +1 sur les arêtes de
𝒮 dans le sens de l'orientation et 0 ailleurs. Alors c est un cocycle mod 3, et si v > 3k − 3, ce n'est pas un cobord.

*Preuve.*
- *Cocycle.*
  - Sur une droite de 𝒮 : 1 + 1 + 1 ≡ 0.
  - Un autre triangle ne contient aucune arête de 𝒮, car une arête est dans un seul triangle.
  - Un quadrangle contenant une arête uw de 𝒮 s'écrit uwpq, avec p ∈ N(w) hors de la droite de u. Le partenaire p′ de u
    sur la droite L_p (couplage parfait entre L_u et L_p) est un voisin commun de u et p distinct de w. Donc q = p′, et
    pq est une arête de 𝒮 ; l'orientation compatible fait se compenser les deux arêtes.
- *Non trivialité.* Si c = δf, alors f est constante sur les composantes de Γ − 𝒮. Ce graphe est un revêtement triple de
  Q = Γ/𝒮 = srg(v/3, k − 2, 1, 6) (note 165). S'il n'était pas connexe, chaque composante serait isomorphe à Q et serait
  un sous-graphe induit de Γ. Comme v/3 > k − 1, Q n'est pas complet, et la composante aurait une paire non adjacente
  avec 6 voisins communs, contre μ(Γ) = 2. Donc f est constante et δf = 0 ≠ c. ∎

Le contenu est celui de la note 165 (étalement régulier, revêtement de BH, cas (a), absence d'étalement à 99) ; la
proposition n'en est qu'une relecture cohomologique. Seul le calcul suivant est nouveau. [E] Sur les quatre srg(243) à
étalement, **H¹(X; 𝔽₃) est exactement
engendré par les classes d'étalement** : 11 étalements et un espace de dimension 6 pour BvLS ; un étalement et un espace
de dimension 1 pour chaque graphe tordu (`exp2_spread_cocycle.py`).

---

## 3.6 Calculs : la topologie des srg(243) et des géométries tordues

**Théorème 3.9** [E]. Calculs exacts (rangs mod p par python-flint ; énumération de classes de Todd–Coxeter sur le
groupoïde fondamental ; effondrement de présentation) :

| complexe | sommets | H₁ sur 𝔽₂, 𝔽₃, 𝔽₅, 𝔽₇ | \|π₁\| | revêtement universel | méthode |
|---|---:|---|---:|---:|---|
| H(2,3), H(3,3), H(4,3) | 9, 27, 81 | 0 | 1 | lui-même | exp8, exp9 |
| t2 (k = 6) | 20 | 0 (équipe) | 1 | lui-même | exp8, exp9 |
| t3 (k = 8) | 39 | 0 (équipe) | 1 | lui-même | exp8, exp9 |
| BvLS | 243 | 0, 6, 0, 0 | 729 | 177 147 = 3¹¹ | exp1, exp9 |
| jumeau | 243 | 0, 1, 0, 0 | 3 | 729 | exp1, exp9 |
| Γ₃ | 243 | 0, 1, 0, 0 | 3 | 729 | exp1, exp8, exp9 |
| Γ₄ | 243 | 0, 1, 0, 0 | 3 | 729 | exp1, exp8, exp9 |
| revêtement triple de BvLS | 729 | 0, 5 (𝔽₂, 𝔽₃) | 243 | 177 147 | exp6, exp9 |
| revêtements triples des trois tordus | 729 | 0, 0 (𝔽₂, 𝔽₃) | 1 | lui-même | exp6, exp8, exp9 |
| **Γ₅ à Γ₈ (sans étalement régulier)** | 243 | 0, 0, 0, 0 | **1** | **lui-même** | exp11 |

Γ₅ à Γ₈ sont les quatre srg(243, 22, 1, 2) sans étalement régulier trouvés par l'équipe les 12 et 13 octobre
(`code/lab_spreadfree_243_2026-10-12/NOTE_SPREADFREE.md`). Γ₅ est le graphe de Cayley `tricayley_Z3x4_grids25`, Γ₆ et Γ₈
les deux graphes d'automorphismes d'ordre 108, Γ₇ celui d'ordre 162. Le script vérifie qu'ils sont srg(243, 22, 1, 2) et
n'ont aucun étalement régulier. Leurs graphes d'appariement ont pourtant des cycles (de 1 à 6 composantes cycliques par
paire), et η prend la valeur 1 sur 768 à 984 des 5940 paires échantillonnées pour Γ₆, Γ₇ et Γ₈ (0 pour Γ₅) : les cycles
existent, mais les conditions de cocycle intérieures à Γ₂(x) les tuent tous.

**Conséquences.**
- **π₁(X(jumeau)) ≅ π₁(X(Γ₃)) ≅ π₁(X(Γ₄)) ≅ ℤ/3**, et π₁(X(BvLS)) ≅ (ℤ/3)⁶.
- Les revêtements universels des trois graphes tordus sont **trois membres simplement connexes de 𝒦₂₂ à 729 sommets** :
  - cospectraux, de spectre 22¹, 19², 7⁷², 4²⁰⁴, 1¹²⁰, (−2)⁹⁰, (−5)²⁰⁰, (−8)⁴⁰ ;
  - deux à deux non isomorphes : nombre de grilles par sommet {55 : 9, 19 : 180, 13 : 540}, {23 : 729} et {31 : 729} ;
  - non distance-réguliers, de profil de sphères (1, 22, 220, 400, 82, 4) en tout sommet ;
  - chaque fibre y est un 2-code parfait de trois sommets à distance mutuelle 5 (exp10 : déplacement minimal 5).
- La matrice de voltage M (§3.8) a pour spectre {19, 7³⁶, 4³⁶, 1⁶⁰, (−2)⁴⁵, (−5)⁴⁵, (−8)²⁰}. Ce sont toutes des valeurs
  22 − 3j, celles de H(11, 3).

**Contrôles de la méthode.**
- L'énumération (`exp9_universal_cover.py`) redonne H(2, 3) et H(3, 3) simplement connexes, et 3¹¹ sommets pour BvLS,
  valeur prouvée par ailleurs.
- L'effondrement (`exp8_simple_connectivity.py`) donne une preuve indépendante de la simple connexité des revêtements de
  Γ₃ et Γ₄. Il reste bloqué sur celui du jumeau, ce qui ne prouve rien ; l'énumération conclut.
- Un revêtement triple connexe d'un espace dont π₁ est d'ordre 3 est universel. C'est donc bien le revêtement
  d'étalement.

**Lecture : la géométrisation à 243.** Les huit srg(243, 22, 1, 2) connus se rangent en trois types :
- le modèle plat H(11, 3) quotienté par le code de Golay (π₁ d'ordre 3⁶) : BvLS ;
- trois modèles tordus à 3⁶ sommets quotientés par ℤ/3 : le jumeau, Γ₃ et Γ₄ ;
- quatre graphes **simplement connexes**, qui sont leur propre revêtement universel : Γ₅ à Γ₈.

**Loi observée** [E, sur les huit graphes] : π₁(X(Γ)) est un 3-groupe abélien élémentaire engendré par les classes
d'étalement, et **Γ n'a pas d'étalement régulier si et seulement si X(Γ) est simplement connexe**.

L'équipe avait observé que t2 et t3 sont « déjà universels » (F2′). La loi « tordu ⇒ universel » est fausse à 243 (le
jumeau, Γ₃ et Γ₄ sont tordus et ont π₁ = ℤ/3). La bonne ligne de partage n'est pas la torsion mais l'**étalement**.

---

## 3.7 Conséquences pour Conway, et l'obstacle exact

**Faits** [P/L].
- Conway est tordu (L1, Makhnev), donc son revêtement universel n'est pas H(7, 3) (voir aussi le Corollaire 3.5).
- Il n'a pas d'étalement régulier (note 165), donc pas de classe d'étalement.
- |π₁(X(Γ))| ≤ 82 859 sans condition, et ≤ 22 sous (L).

**Conjecture 3.10** [C]. Pour tout srg(v, k, 1, 2) Γ, H¹(X(Γ); 𝔽₃) est engendré par les classes d'étalement, et π₁(X(Γ))
est le 3-groupe abélien élémentaire dual. En particulier, **un srg(99, 14, 1, 2) aurait un complexe X(Γ) simplement
connexe**. Cela entraîne qu'en jauge radiale le système de 3.6(iii) n'a que la solution nulle pour tout groupe de
coefficients, c'est-à-dire H₁(X(Γ); ℤ) = 0 ; sous (L), ce dernier énoncé équivaut à la simple connexité (3.3(d)).
- *Indice :* la loi vaut sur les huit srg(243) connus, et en particulier sur les quatre graphes sans étalement régulier
  Γ₅ à Γ₈, qui sont du type de Conway et sont simplement connexes (§3.6, exp11).
- *Faiblesse de l'indice :* un seul jeu de paramètres, et des graphes trouvés par des méthodes qui favorisent la
  symétrie.

**Question 3.11** [O]. Peut-on démontrer la simple connexité pour un srg sans étalement régulier ? Sous (L), il suffit de
montrer H₁(X(Γ); ℤ) = 0 (Théorème 3.3(d)).

**L'obstacle exact pour T5** [P, sur la structure de l'argument ; E pour l'existence des exemples].
1. Un min-max topologique de type S7 demande une classe non triviale.
   - b₁ = 0 sur tout corps de caractéristique 0 (Théorème 3.3(a)).
   - Le seul mécanisme connu de torsion, les étalements réguliers, manque à 99.
   - Si la Conjecture 3.10 tient, X(Conway) n'apporte aucune entrée de type H¹ ou π₁.
2. Un π₁ non trivial ne donnerait pas non plus de contradiction à lui seul. Le Théorème 3.4 le transforme en une action
   libre, à orbites codes parfaits, sur un membre plus gros de 𝒦₁₄. Rien n'interdit a priori de telles actions, et il
   en existe à 243.
3. **Le type topologique prédit pour Conway est réalisé dans la famille.** Γ₅ à Γ₈ sont des srg(243, 22, 1, 2) sans
   étalement régulier, à complexe simplement connexe et 𝔽_p-acyclique pour p ≤ 7. Aucun invariant de la seule topologie
   de X ne peut donc exclure Conway ; une obstruction devrait dépendre de k = 14 lui-même, c'est-à-dire repasser par
   l'arithmétique des paramètres.

Le canal topologique est donc **complet mais vide** pour Conway. Il explique la structure de la famille (L1, BvLS, les
graphes tordus et les graphes sans étalement à 243), et il ne donne aucune obstruction. La moitié « topologique » du
premier travail (S7) ne s'applique pas, et la raison est démontrée par des exemples.

Si la Conjecture 3.10 est vraie, un graphe de Conway serait son propre revêtement universel, comme Γ₅ à Γ₈. Cela ne
fait pas de ces graphes un banc d'essai pour les lois locales de Conway : l'équipe a établi que srg(243) ne convient pas
à cet usage (L07 §4.15), car la résonance k = 14 n'y existe pas.

---

## 3.8 Pourquoi le mécanisme de C3 ne passe pas par les ℤ₃-revêtements

C3 (fiche L04) ferme le cas d'un automorphisme d'ordre 3. Il le fait par la congruence modulo 1 − ω d'une structure
entière Q et d'une structure hermitienne M sur ℤ[ω], dont les déterminants sont incompatibles. Un ℤ₃-revêtement de X(Γ)
fournit une paire naturelle (A, M), où M est la matrice de voltage [P] :
- M ∈ Mat₉₉(ℤ[ω]) est hermitienne, et M ≡ A (mod 1 − ω) ;
- **M² = 14I + M + 2Ŝ**, où Ŝ est la matrice de voltage à distance 2. Autrement dit, N := (M − 3I)(M + 4I)/2 a
  **tous ses coefficients dans μ₃** : N_uw = ω^(transport le long d'une géodésique) ;
- tr M^j = tr A^j pour j ≤ 4, par le Lemme 3.1. Donc χ_M ≡ χ_A = t⁵⁴(t + 1)⁴⁵ (mod 3), et les quatre premiers moments
  coïncident.

Dans C3, M est une compression de A sur un sous-espace invariant. Son spectre est donc contenu dans {14, 3, −4}, avec des
multiplicités contraintes, et c'est ce qui crée le conflit de déterminants. Ici M n'est pas une compression de A : ses
valeurs propres sont celles du revêtement (à 243, ce sont les 22 − 3j, hors du spectre de A). Les déterminants ne sont
pas fixés, et aucun conflit n'apparaît. [P pour les identités ; la dernière phrase porte sur ce mécanisme précis, et ne
prouve pas qu'aucun autre argument arithmétique ne marche.]

---

## 3.9 Une loi tuée : « A − kI est nilpotente mod 3 »

**Observation** [P/L]. Parmi les paramètres admissibles de srg(v, k, 1, 2), v ∈ {9, 99, 243, 6273, 494019} [L], tous
sauf Conway ont leurs valeurs propres ≡ k (mod 3) :
- (9, 4) : 4, 1, −2 ;
- (243, 22) : 22, 4, −5 ;
- (6273, 112) : 112, 10, −11 ;
- (494019, 994) : 994, 31, −32 ;
- pour Conway, 3 ≢ 14 (mod 3).

C'est aussi le cas de H(n, 3) et des revêtements à 729 sommets. Comme A = BBᵀ − nI, où B est l'incidence points-droites,
on a A − kI ≡ BBᵀ (mod 3) [P]. Une loi « A − kI est nilpotente mod 3 sur tout membre de 𝒦_k » exclurait donc Conway.

**Elle est fausse** [E] (`data/t2_twisted.json`, `t3_twisted.json`, calcul direct) :
- t2 a pour spectre 6, 2, 1, −2, −3 ;
- t3 a χ_{A−8I} ≡ t²¹(t − 1)¹⁸ (mod 3).

Conway partage son type spectral 3-adique avec les géométries tordues, et non avec la famille 243. La loi est tuée en une
minute par les témoins de l'équipe. C'est le bon usage de ces témoins, qui ne sont pas des blocs de Conway.

---

## 3.10 Apport par rapport à la campagne

| résultat | statut | apport |
|---|---|---|
| 3.1–3.2 : boucles courtes, revêtements dans 𝒦_k, déplacement ≥ 5 | P | Base rigoureuse de L1 et F2′ (que l'équipe utilisait sans l'écrire en général) |
| 3.3(b) : π₁ fini, diam Ũ ≤ 9 | P (outil L) | Nouveau. Le revêtement universel de Conway, s'il existe, est un graphe fini explicitement borné |
| 3.3(c) : \|π₁\| ≤ 82 859 | P | Nouveau, inconditionnel, faible |
| 3.3(d) : \|π₁\| ≤ 22 sous (L) | C/P | Nouveau. Réduit la simple connexité à H₁ = 0 sous (L) |
| 3.4 : géométrisation par codes parfaits | P | Nouveau sous cette forme. Unifie L1 (Makhnev), BvLS = Golay et la famille 243 |
| 3.5 : grid-full ⇒ v ∈ {9, 243} | P + L | Précise la remarque de L1 (puissance de 3) |
| 3.6–3.7 : jauge radiale | P | Nouveau. Ramène H¹ aux cycles des graphes d'appariement d'une seule 2-boule |
| 3.8 : classes d'étalement | P | Lecture cohomologique de la note 165 (cas (a)) |
| 3.9 : π₁ des huit srg(243) connus ; trois revêtements universels à 729 sommets | E | Nouveau. Loi « π₁ ≠ 1 ⟺ étalement régulier » sur les huit graphes ; Γ₅ à Γ₈ simplement connexes ; trois graphes simplement connexes, cospectraux, non isomorphes, dans 𝒦₂₂ |
| 3.10 et 3.11 | C/O | Cible précise : X(Conway) simplement connexe. Désigne Γ₅ à Γ₈ comme banc d'essai topologique de Conway |
| §3.7 : obstacle exact pour T5 | P (structure) + E (exemples) | Ferme la route « min-max topologique » : le type topologique prédit pour Conway est réalisé par de vrais srg(243) |
| §3.8 : C3 ne passe pas par les ℤ₃-revêtements | P (identités) | Dit pourquoi : M n'est pas une compression de A |
| §3.9 : loi mod 3 | E (réfutation) | Une loi qui aurait tué Conway, réfutée par t2 et t3 |
