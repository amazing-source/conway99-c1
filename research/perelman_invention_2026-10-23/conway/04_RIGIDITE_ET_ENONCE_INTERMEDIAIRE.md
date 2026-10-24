# 4. Intégralité, cas d'égalité et énoncé intermédiaire (tests T3, T4 et S10)

Statuts : **[P]** démontré ici · **[L]** littérature · **[E]** calcul reproductible · **[A]** analogie ·
**[C]** conjecture · **[O]** ouvert ou obstacle formulé. Les références `EXPLORATION` renvoient à
`code/lab_exploration_2026-10-16/EXPLORATION.md`, et `CARTE` à `code/lab_chantier_2026-10-20/CARTE_MAITRESSE.md`.

---

## 4.1 T3 : l'intégralité comme substitut de la compacité

Chez Perelman, la compacité de Cheeger–Gromov–Hamilton transforme des estimées uniformes en limites, et les limites sont
des modèles (κ-solutions). Dans un problème fini, le schéma S3 se dégrade en : **un défaut entier petit est nul**.

La campagne satisfait déjà cette condition, et c'est la seule des cinq qu'elle exploite pleinement. La méta-leçon de la
carte (CARTE §4) le dit : toutes les exclusions obtenues combinent une donnée arithmétique globale, la positivité ou le
rang, et l'intégralité, sur un objet de classification finie. Exemples : C3 (mod 1 − ω), C2 (réseaux de Borcherds), la
fenêtre de rang (thêta de niveau 7), le test d'étoile au rang 37.

Le chapitre 3 en donne une illustration nette [P] :
- sur ℝ, tout membre de 𝒦_k a b₁ = 0 (Théorème 3.3(a)) : une relaxation réelle ne voit rien ;
- l'invariant qui distingue les graphes vit dans la **torsion** : H¹(X; 𝔽₃) vaut 6, 1 ou 0 selon le graphe (§3.6).

C'est un exemple exact de la réponse à la question 4 du mandat (une relaxation perd-elle une information globale ?).

---

## 4.2 T4 : des cas d'égalité rigides, imposés par les paramètres

### (a) La résonance k = 14 comme équation de soliton

L'équipe et Codex ont isolé un facteur k − 14 = (r − 3)(3 − s), où r, s sont les valeurs propres de la famille
(EXPLORATION, 16/10, l. 49–52 et 86–91) :
- pour une composante C du graphe cubique G[N(l)] d'une droite l,
  Σ_{z lointain} (n_C(z) − 2c/(k − 2))² = (k − 14)·c·(1 − c/(3(k − 2))) ;
- la couverture des grilles laisse (k − 4)(k − 14)/2 sommets sans voisin ;
- le débordement de la cinquième étoile vaut D_k = 8 + a − (k − 14)(k − 7)/2.

À k = 14, la variance est **nulle**. On obtient l'équidistribution exacte |N(z) ∩ C| = |C|/6 pour tout z lointain, et
θ = 3 est le degré du graphe cubique G_T.

**Lecture** [A]. C'est la forme finie d'une équation de soliton. Une quantité positive (une variance), qui serait le
« défaut » d'une monotonie, s'annule identiquement aux paramètres de Conway. Elle force alors une structure exacte.
- Chez Perelman, la rigidité du cas d'égalité est un **théorème** : 𝒲′ = 0 caractérise les solitons.
- Ici, elle est **donnée** par les paramètres.

Cela explique l'observation de l'équipe que « les données saturent chaque borne (marge 0) » (diagnostic du 16/10). À
k = 14, les inégalités qui donneraient une marge sont des égalités. T4 est donc satisfaite au sens fort. Mais cette
rigidité est une contrainte que Conway vérifie, et non une contradiction ; l'équipe l'utilise déjà, par exemple dans la
coupe d'équilibre proposée pour R8 (CARTE §6.2).

### (b) Proposition 4.1 (l'excès d'entrelacement : une quantité monotone à égalité rigide) [P]

Soit θ une valeur propre de A, de multiplicité m_θ, et H un sous-graphe induit à h sommets. On pose

    e_θ(H) = mult_θ(A_H) − (h − v + m_θ).

Alors :
- (i) e_θ(H) ≥ 0, et e_θ(V) = 0 ;
- (ii) e_θ est décroissante pour l'inclusion : H ⊂ H′ ⇒ e_θ(H) ≥ e_θ(H′) ;
- (iii) e_θ(H) = 0 si et seulement si les deux conditions suivantes valent :
  - tout vecteur propre de A_H pour θ se prolonge par zéro en un vecteur propre de A ;
  - la restriction E_θ → ℝ^{V∖H} est surjective.

*Preuve.*
- (i)–(ii) : par l'entrelacement de Cauchy, retirer un sommet fait baisser la multiplicité d'au plus 1.
- (iii) : notons W_H l'espace propre de A_H et E_θ ∩ ℝ^H les vecteurs propres de A portés par H, qui sont dans W_H. On
  a e = [dim W_H − dim(E_θ ∩ ℝ^H)] + [(v − h) − rang(E_θ → ℝ^{V∖H})], et les deux crochets sont ≥ 0. ∎

**Lecture et honnêteté.** C'est une quantité monotone à égalité rigide (S3), dans sa version finie. Le prolongement par
zéro est le principe d'extension A7 de l'équipe (EXPLORATION, 16/10). Les comptages du type mult₃(A_W) ≥ 11 sont des
instances de e ≥ 0. La proposition **réorganise** donc les arguments d'entrelacement de l'équipe en une seule quantité.
Elle ne ferme rien.

### (c) Lemme 4.2 (rang saturé) [P, standard]

Soit M une matrice symétrique sur un corps et S un ensemble d'indices tel que rang M_SS = rang M. Alors
M = M_{·S} X M_{S·} pour tout inverse généralisé X de M_SS. En particulier M_FF = M_FS X M_SF.

*Preuve.* Les lignes de S engendrent l'espace des lignes. ∎

Avec M = A − 3I sur 𝔽₇, si un ensemble S atteint rang₇(M_SS) = r = rang₇(M), toute la matrice mod 7 est déterminée par
les lignes de S. La forme de Green de la réduction du rang 37 (`THEOREME_REDUCTION_R37.md`, Prop. 3.6) en est une
instance. C'est la rigidité de l'égalité dans le canal 7-adique : l'égalité des rangs local et global force la
détermination du global par le local.

---

## 4.3 S10 : l'énoncé intermédiaire unique

### (a) Ce qui caractérise l'énoncé intermédiaire de Perelman

Le non-effondrement, puis les voisinages canoniques, ont quatre traits :
1. c'est un énoncé **universel sur une classe fermée** par les opérations utilisées (limites, homothéties, chirurgie) ;
2. il est **strictement plus faible** que la conclusion, et démontré d'abord ;
3. il est démontré par une **quantité monotone à cas d'égalité rigide** (𝒲, Ṽ) ;
4. une fois acquis, la machinerie existante (compacité, classification) fait le reste.

### (b) Les énoncés intermédiaires de la campagne

Ce sont Q7, ODD-PURE + Z, N9-NG, H-MATCH et T15. Le diagnostic de l'équipe du 16/10 les ramène à un seul : « un bloc
local ne porte pas la nullité que le spectre global impose, sauf s'il est plein de grilles ». Confrontons-le aux quatre
traits.

| trait | campagne | verdict |
|---|---|---|
| 1. classe fermée | universel sur les « blocs admissibles ». Cette classe n'est fermée par aucune opération, et elle est bien plus grosse que les blocs réalisables : les données viennent de structures impossibles dans Conway (CARTE §5 n° 6, R1-40) | en partie |
| 2. plus faible, implique la conclusion | oui : ODD-PURE + Z + P ≤ 852 + fermeture c ≥ 4 ⇒ pas de Conway (L08-027, P non relu) | oui |
| 3. quantité monotone à égalité rigide | **aucune**. La marge n'est pas uniforme (λ_max jusqu'à 0,99993, L08-028), donc aucune inégalité à écart uniforme ne peut conclure | **non** |
| 4. machinerie aval | P ≤ 852 force une paire sans grille à c_min ≤ 4 | oui |

**La campagne a l'architecture de Perelman** : un énoncé intermédiaire unique, et un comptage global qui force son
applicabilité. **Il lui manque exactement le trait 3.**

### (c) L'alternative au niveau de la classe est vide

Dans 𝒦₁₄, l'énoncé intermédiaire naturel serait un non-effondrement à l'échelle 3 (S₃(x) ≠ ∅). Il est **équivalent** au
problème (Corollaire 2.2). On ne connaît aucun énoncé plus faible au niveau de la classe ; le trait 2 y échoue.

### (d) Proposition 4.3 : le lemme impair est la conclusion « pas de respirateur » de S1

Cadre de l'équipe (N9NG_ATTACK, R5 ; EXPLORATION, 16/10) : T = T_S ⪰ 0 est un bloc, g une permutation formelle des
lettres d'ordre 2 avec gKg = K, et Δ = gΓg − Γ. Le lemme de signe R5 dit que pour x ∈ ker T,
E((x ± gx)/2) = −¼ xᵀΔx.

**(i)** [P] Si x et gx sont tous deux dans ker T, alors x₋ = (x − gx)/2 ∈ ker T.

*Preuve.* R5 appliqué à x donne E(x₋) = −¼ xᵀΔx. Appliqué à gx, avec gΔg = −Δ, il donne E(x₋) = +¼ xᵀΔx. Les deux
valeurs sont ≥ 0 (T ⪰ 0), donc nulles, et E(x₋) = 0 entraîne Tx₋ = 0. ∎

[A] C'est exactement la conclusion (C1) de S1 : une orbite périodique (g² = 1) d'une opération le long de laquelle une
énergie est monotone est un point fixe. Combiné à la positivité du secteur impair (Φ ⪰ 2I sur 1^⊥), cela redonne le
**lemme impair** de l'équipe.

**(ii)** [P, sur la structure de l'argument] Dans le cas restant d'ODD-PURE (x ∈ ker T mais gx ∉ ker T), R5 donne
seulement E(x₋) = E(x₊) = ε > 0 (EXPLORATION l. 174–177). L'opération g ne préserve pas l'énergie (Δ ≠ 0), et elle
n'envoie pas ker T dans lui-même. Il n'y a donc pas d'orbite le long de laquelle itérer une monotonie. S1 ne dit rien
non plus dans ce cas : sa conclusion porte sur les orbites périodiques du flot lui-même.

**(iii)** [E de l'équipe] La positivité et R5 ne peuvent pas suffire. Les blocs à grille vérifient T ⪰ 0 et R5, et ont
δ = 9 − rang D = 1 (HB ; 872 côtés à δ > 0, tous à grille, EXPLORATION l. 196–209). ODD-PURE y est faux. Toute preuve
doit donc utiliser l'hypothèse « sans grille » de façon essentielle.

**Conclusion.** La transposition de S1 est complète. Elle donne exactement le lemme impair, déjà démontré par l'équipe.
Le cas ouvert d'ODD-PURE est **précisément** l'endroit où le mécanisme s'arrête. C'est un obstacle formulé exactement,
pas une difficulté vague.

### (e) Ce qu'il faudrait pour une preuve « à la Perelman » d'ODD-PURE [O]

Il faudrait une fonctionnelle Φ sur les blocs admissibles (et non sur le seul ker T d'un bloc) telle que :
- (1) Φ soit invariante par les permutations formelles V₄ ;
- (2) sa variation par g contrôle l'asymétrie : Φ(gx) − Φ(x) ≥ c·E(x₋) pour x ∈ ker T ;
- (3) la même inégalité vaille relativement au bloc permuté gTg, pour que l'orbite se referme.

Alors (2) et (3), appliqués en x et en gx, donnent E(x₋) ≤ 0.

Par (iii), une telle Φ ne peut pas exister sans un terme qui s'annule exactement sur les grilles. [A] Le candidat
naturel est la **torsion** : le nombre de carrés hors grille, que la note 165 identifie à une courbure. L'analogie est
celle de Bochner, où une courbure positive tue les formes harmoniques ; ici, la torsion devrait tuer les vecteurs
impairs du noyau.

Programme testable sur les données de l'équipe : écrire T sur le secteur impair comme « laplacien signé + couplage Γᵃ »,
et chercher une identité de Weitzenböck où la contribution du couplage est majorée par un compte de torsion nul sur les
grilles. Je l'énonce comme programme ; ce n'est pas un résultat.

### (f) Recommandation

Elle rejoint la conclusion propre de l'équipe du 16/10 (EXPLORATION l. 212–214) : abandonner les bornes de contraction
uniformes, et classer la saturation exacte (λ_max = 1) comme un problème d'algèbre linéaire rationnelle, avec
l'intégralité. Données utiles :
- les vecteurs extrêmes sont h-impairs (EXPLORATION l. 218–223) ;
- dans le cas h-invariant, ODD-PURE se ramène à ODD9-NG.

**Ce que la lecture perelmanienne ajoute : rien d'opérationnel.** Elle redit, dans un autre vocabulaire, ce que
l'équipe avait conclu le 16/10 : les marges ne suffiront pas, il faut une mesure. La Proposition 4.3 et le §4.3(e)
décrivent où le mécanisme S1 s'arrête et la forme qu'aurait l'ingrédient manquant ; ils ne donnent aucun moyen de le
trouver.

---

## 4.4 Apport par rapport à la campagne

| résultat | statut | apport |
|---|---|---|
| §4.1 : T3 = intégralité ; b₁ = 0 contre H¹(𝔽₃) ≠ 0 | P (+ E) | Une instance exacte de la méta-leçon de l'équipe |
| §4.2(a) : la résonance k = 14 lue comme équation de soliton | A | Explique la « marge 0 » des données : à k = 14, les inégalités sont des égalités |
| Prop. 4.1 (excès) | P | Réorganisation des arguments d'entrelacement de l'équipe ; ne ferme rien |
| Lemme 4.2 (rang saturé) | P (standard) | Cadre commun de la forme de Green du rang 37 |
| §4.3(b)–(c) : S10 appliqué à la campagne | A/P | Architecture correcte ; il manque exactement une quantité monotone à égalité rigide ; au niveau de la classe, l'énoncé intermédiaire naturel équivaut au problème |
| Prop. 4.3 | P (+ A) | Le lemme impair = « pas de respirateur » ; le cas ouvert d'ODD-PURE est exactement là où S1 s'arrête |
| §4.3(e) | O | Forme précise de l'ingrédient manquant, et un programme de test (identité de Weitzenböck avec terme de torsion) |
