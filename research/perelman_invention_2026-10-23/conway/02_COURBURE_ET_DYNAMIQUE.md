# 2. Courbure et dynamique : aucune évolution naturelle sur Conway (tests T1 et T2)

Statuts : **[P]** démontré ici · **[L]** littérature · **[E]** calcul reproductible (script et données du dossier
`../code`, `../data`) · **[A]** analogie · **[C]** conjecture · **[O]** ouvert ou obstacle formulé.

Question de départ (condition T1 du premier travail, `../etude_perelman/04_PRINCIPES_TESTABLES.md`) : existe-t-il une
évolution canonique non triviale, ou au moins une fonctionnelle naturelle non constante, sur un espace qui contient le
graphe cherché ? Chez Perelman, tout part de là (S1, S3, S6, S7). La réponse est non, et la raison est précise.

---

## 2.1 La classe 𝒦_k

**Définition.** 𝒦_k est la classe des graphes connexes, localement finis, k-réguliers, tels que :
- (i) chaque arête est dans exactement un triangle ;
- (ii) deux sommets à distance 2 ont exactement deux voisins communs.

Ce sont les graphes *amplement réguliers* de paramètres (k, 1, 2) [L : Brouwer–Cohen–Neumaier, *Distance-regular
graphs*, 1989, §1.1]. On n'exige ni la finitude ni un diamètre donné. Comme N(x) induit un couplage parfait, k = 2n est
pair.

**Lemme 2.1 (cadre)** [P ; c'est CARTE_MAITRESSE §1.4 pour k = 14, et la preuve y est la même mot pour mot].
Pour tout sommet x de G ∈ 𝒦_k :
- N(x) induit nK₂ ;
- chaque y ∈ Γ₂(x) a exactement deux voisins dans N(x), non adjacents ;
- y ↦ N(y) ∩ N(x) est une bijection de Γ₂(x) sur les non-arêtes de N(x), donc |Γ₂(x)| = k(k − 2)/2 ;
- la 2-boule incomplète (sommets de B₂(x), arêtes ayant une extrémité dans B₁(x)) est unique à isomorphisme près.

*Preuve.* Si a, b ∈ N(x) sont adjacents, l'arête ab est dans le triangle xab, d'où le couplage. Si y ∈ Γ₂(x) a pour
voisins communs a, b avec x, alors a ≁ b, sinon l'arête ab serait dans les triangles xab et yab. Réciproquement, une
non-arête {a, b} de N(x) a un second voisin commun y ≠ x, et y ∉ N(x), car un sommet de N(x) n'a qu'un voisin dans N(x).
Deux non-arêtes distinctes donnent des y distincts, puisque y a exactement deux voisins dans N(x). La structure est donc
déterminée par k. ∎

**Corollaire 2.2** [P]. Pour G ∈ 𝒦_k, |V(G)| ≥ 1 + k + k(k − 2)/2 = 2n² + 1. L'égalité a lieu si et seulement si G
est de diamètre 2, c'est-à-dire si et seulement si G est un srg(2n² + 1, 2n, 1, 2).

Pour k = 14, **les graphes de Conway sont exactement les membres de 𝒦₁₄ à 99 sommets, c'est-à-dire ses membres
minimaux**. Si un sommet x vérifie S₃(x) = ∅, alors V = B₂(x) et G est un graphe de Conway. Donc :

> « Conway n'existe pas » ⟺ « pour tout G ∈ 𝒦₁₄ et tout sommet x, S₃(x) ≠ ∅ ».

C'est un énoncé de **non-effondrement à l'échelle 3**, et il est *équivalent* au problème entier. On y revient au §4
(énoncé intermédiaire) : la classe naturelle n'offre aucun non-effondrement plus faible à démontrer d'abord.

**Exemples de membres.**
- K₃ (k = 2) ; les graphes de Hamming H(n, 3) (3ⁿ sommets) ; les srg(243, 22, 1, 2) connus (BvLS, jumeau, Γ₃, Γ₄).
- Les géométries tordues de l'équipe : t2 (20 sommets, k = 6) et t3 (39 sommets, k = 8), `notes/20_ATTAQUES_R.md`.
- Les produits cartésiens : G₁ □ G₂ ∈ 𝒦_{k₁+k₂} [P, immédiat]. Exemple : t2 □ t3 ∈ 𝒦₁₄ a 780 sommets (exp3).
- Les revêtements du 2-complexe (§3, Corollaire 3.2).

---

## 2.2 Théorème A.1 : tout ce qui est « naturel » est imposé par les paramètres

**(a)** [P, classique] Pour un srg(v, k, λ, μ), l'algèbre d'adjacence ⟨I, A, J⟩ est déterminée par les paramètres. Toute
fonction de A dans cette algèbre en dépend donc seule :
- spectre, noyau de la chaleur e^{−tL}, nombre de marches fermées de chaque longueur ;
- entropies et fonctionnelles de type 𝒲 construites sur la chaleur ;
- zêta d'Ihara (formule d'Ihara–Bass pour un graphe régulier).

**(b)** [P] Tout invariant qui ne dépend que de la 2-boule incomplète en x est constant sur 𝒦_k (Lemme 2.1).
C'est le cas de la courbure de Bakry–Émery, à toute dimension [L : la courbure de Bakry–Émery en x ne dépend que de la
2-boule incomplète ; Cushing–Liu–Peyerimhoff, *Bakry–Émery curvature functions on graphs*, Canad. J. Math. 2020].

**(c)** [P] Il en va de même des flots de Ricci discrets de type Ollivier, dw_e/dt = −κ_e(w) w_e, partant des poids
unité. Par le Théorème A.2, toutes les arêtes ont la même courbure. Or la courbure d'Ollivier est invariante par
homothétie des poids, donc w(t) = c(t)·1 est solution ; c'est la seule dès que le flot a la propriété d'unicité
habituelle. Le flot ne fait que changer l'échelle.

**Lecture.** Un graphe de Conway serait « d'Einstein » pour toutes les courbures locales usuelles, et un point fixe, à
l'échelle près, de tout flot construit sur elles. Dans le vocabulaire du premier travail, **la condition T1 échoue sur
l'objet lui-même** : aucune fonctionnelle naturelle ne distingue un graphe de Conway d'un autre, ni ne mesure une
distance à l'existence.

---

## 2.3 Théorème A.2 : courbures d'arête

Pour une idleness α ∈ [0, 1], on note m_x^α = α δ_x + (1 − α)/k Σ_{u∼x} δ_u et κ_α(x, y) = 1 − W₁(m_x^α, m_y^α)/d(x, y)
(Ollivier [L : J. Funct. Anal. 256, 2009]). La courbure de Lin–Lu–Yau est κ_LLY = lim_{α→1} κ_α/(1 − α) [L : Tohoku Math.
J. 63, 2011].

**Théorème A.2.** Pour toute arête xy d'un graphe G ∈ 𝒦_k :

    κ_α(x,y) = (1 + (2k − 1)α)/k   si 0 ≤ α ≤ 1/(k+1),
    κ_α(x,y) = 3(1 − α)/k          si 1/(k+1) ≤ α ≤ 1.

En particulier κ₀ = 1/k et κ_LLY = 3/k.

**Attribution.** La valeur κ_LLY = 3/k pour les graphes amplement réguliers de paramètres (k, 1, μ) avec μ > 1 est due à
Li–Liu [L : JUSTC 51 (2021) 889–893], citée par Huang–Liu–Xia [L : Combinatorica 44 (2024) 1177–1192, §1]. La formule
pour tout α s'obtient de la même façon ; la preuve est donnée ici pour être complète, car le §3 s'en sert.

*Preuve.* Soit z le troisième sommet du triangle de xy, A = N(x) \ {y, z} et B = N(y) \ {x, z}.
- Un a ∈ A n'est adjacent ni à y (sinon xy serait dans deux triangles) ni à z (le partenaire de a dans N(x) n'est pas z).
- Donc d(a, y) = 2, et a, y ont exactement deux voisins communs : x, et un sommet de B.
- Ainsi chaque a ∈ A a un unique voisin dans B, et symétriquement : **les arêtes entre A et B forment une bijection**.

*Majoration.*
- Si α ≥ (1 − α)/k : on laisse sur place les masses en z et la masse (1 − α)/k en x ; on envoie le reste de la masse de
  x, soit α − (1 − α)/k, en y ; on envoie chaque a sur son partenaire de B. Coût : α + (k − 3)(1 − α)/k.
- Sinon : on garde α en x et α en y, on envoie (1 − α)/k − α de y vers x, et A sur B. Coût : (k − 1)(1 − α)/k − α.

*Minoration.* On utilise des fonctions 1-lipschitziennes, prolongées de {x, y, z} ∪ A ∪ B à G par McShane (il suffit
d'être 1-lipschitzien pour la distance de G restreinte).
- f = 0 sur {x, z} ∪ B, f(y) = 1, f = −1 sur A. Le seul couple à vérifier est (a, y), à distance 2. On obtient
  E_{m_y} f − E_{m_x} f = α + (k − 3)(1 − α)/k.
- f(x) = 1, f(y) = 0, f = 1 sur B, f = 0 sur A ∪ {z}. On obtient (k − 1)(1 − α)/k − α.

Chaque borne est atteinte dans son domaine. Les deux formules coïncident en α = 1/(k + 1), où elles valent 3/(k + 1). ∎

**Conséquence** [L]. Par le théorème de Bonnet–Myers de Lin–Lu–Yau, tout G ∈ 𝒦_k est **fini** et de diamètre au plus
⌊2k/3⌋ (Huang–Liu–Xia, Cor. 1.4(ii)). C'est 9 pour k = 14. Le théorème s'applique à un graphe localement fini *a priori
infini* et en déduit la finitude, ce dont le §3 a besoin. (Brouwer–Cohen–Neumaier, Thm 1.13.2, donnait déjà diam ≤ k.)

[E] Contrôle par programmation linéaire sur BvLS et le jumeau (`exp7_ollivier_check.py`) : κ₀ = 0,045455 = 1/22 et
κ_{1/2}/(1/2) = 0,136364 = 3/22 sur toutes les arêtes tirées.

---

## 2.4 Théorème A.3 : sur les non-arêtes, la première courbure non paramétrique

Soit Γ un srg(v, k, 1, 2), x ≁ y, de voisins communs a, b. Le **graphe d'appariement** B_xy est le graphe biparti, à
arêtes de Γ, entre X″ = N(x) \ {a, b} et Y″ = N(y) \ {a, b}. On note a′, b′ les partenaires de a, b dans N(x), et a″, b″
ceux de a, b dans N(y).

(Dans le code, B_xy s'appelle « graphe de transport » et η s'appelle `eps`. Le nom est changé ici pour éviter la
confusion avec les « cycles de transport » de l'équipe, notes 236–240, qui sont des chaînes de triangles autour de
centres. Le lien entre les deux objets n'est pas établi ici.)

**(a) Structure** [P].
- a′, b′, a″, b″ sont de degré 1 ; tous les autres sommets de B_xy sont de degré 2.
- B_xy n'a pas de 4-cycle.
- Donc B_xy est la réunion disjointe de **deux chemins**, dont les extrémités sont a′, b′, a″, b″, et de **cycles
  pairs de longueur ≥ 6**.

*Preuve.*
- a′ et y sont à distance 2, de voisins communs a et un sommet de Y″ ; b n'en est pas un, car a′ ≁ b.
- Pour u ∈ X″ \ {a′, b′}, on a u ≁ a, b, donc ses deux voisins communs avec y sont dans Y″ (diamètre 2).
- Un 4-cycle u₁w₁u₂w₂ donnerait à u₁, u₂ trois voisins communs x, w₁, w₂. S'ils sont non adjacents, c'est exclu par
  μ = 2 ; s'ils sont adjacents, l'arête u₁u₂ serait dans deux triangles. ∎

**(b) Parité d'appariement et courbure** [P]. Posons η(x, y) = 1 si a′ et b′ sont les deux extrémités d'un même chemin,
et η(x, y) = 0 sinon. Alors

    κ₀(x, y) = (k + 2)/(2k)   si η(x, y) = 0,
    κ₀(x, y) = (k + 1)/(2k)   si η(x, y) = 1.

Pour Conway, ces valeurs sont 4/7 et 15/28.

*Preuve.*
- Les mesures m_x, m_y sont uniformes sur k atomes. Le polytope de transport est k fois celui des matrices
  bistochastiques, dont les sommets sont des permutations (Birkhoff). L'optimum est donc atteint en une bijection
  σ : N(x) → N(y).
- On peut supposer σ(a) = a et σ(b) = b : si σ(a) = w et σ(u) = a, l'échange donne d(u, w) ≤ d(u, a) + d(a, w).
- Le coût restant est Σ_{u∈X″} d(u, σ(u)), avec d ∈ {1, 2} (diamètre 2, et u ≠ σ(u)). Il vaut
  (k − 2) + (k − 2 − ν), où ν est le couplage maximum de B_xy.
- Les cycles pairs et les chemins à nombre pair de sommets ont un couplage parfait. Si η = 0, les deux chemins vont
  d'un côté à l'autre et ν = k − 2. Si η = 1, chaque chemin a un sommet de trop d'un côté et ν = k − 3.
- On conclut par κ₀ = 1 − W₁/2. ∎

**(c) Grilles et revêtements** [P].
- Si le carré xayb est dans une grille 3×3, les deux chemins sont les arêtes a′b″ et b′a″, donc η = 0. Un graphe où
  tout carré est dans une grille (« grid-full ») a η ≡ 0.
- η ne dépend que des deux composantes-chemins de B_xy. Il dépend des arêtes de Γ₂(x) issues de y, qui ne sont pas
  dans la 2-boule incomplète de x : il n'est donc pas fixé par le cadre.
- Dans un revêtement du §3, les composantes-chemins se relèvent telles quelles, car la classe de cohomologie ne vit que
  sur les cycles (Théorème B.6). η est donc conservé, ce que confirment les données (exp10 : mêmes comptes de η sur
  chaque srg(243) et sur son revêtement triple).

**(d) Données** [E] (`exp1_curvature_topology_243.py`, `exp10_transport_graphs.py`).

| graphe | paires à distance 2 | η = 1 | composantes cycliques par paire |
|---|---:|---:|---|
| BvLS (grid-full) | 26 730 | 0 | toujours 6 hexagones |
| jumeau | 26 730 | 6 480 | 2 à 6 |
| Γ₃ | 26 730 | 4 320 | 1 à 6 |
| Γ₄ (tordu) | 26 730 | 0 | 1 à 6 |
| Γ₅ (sans étalement) | 5 940 (échantillon) | 0 | 1 à 6 |
| Γ₆, Γ₇, Γ₈ (sans étalement) | 5 940 (échantillon) | 984, 792, 768 | 0 à 6 |
| t2 (k = 6, diamètre 3) | 240 | 120 | 0 |
| t3 (k = 8, diamètre 3) | 936 | 234 | 0 |

(Les échantillons portent sur 27 sommets x et toutes les paires {x, y} à distance 2 ; exp10 et exp11.)

La programmation linéaire confirme κ₀ = 0,545455 = 24/44 (η = 0) et 0,522727 = 23/44 (η = 1) sur le jumeau. Γ₄ montre
que η ≡ 0 n'implique pas grid-full.

**Lecture.** η est la seule information de courbure d'Ollivier sur Conway que les paramètres ne fixent pas. C'est une
**parité**, et non une grandeur qui pourrait décroître le long d'un flot. [A] On peut la lire comme un caractère
d'orientation : le chemin issu de a′ revient ou non du côté de x, comme un ruban qui se referme droit ou en ruban de
Möbius. Pour Conway, la distribution de η est inconnue. Aucune identité de comptage ne la fixe à ma connaissance.

---

## 2.5 Ce que cela dit des conditions T1 et T2

**T1 (évolution canonique)** : elle échoue sur l'objet (Théorème A.1). Une dynamique ne peut vivre qu'ailleurs :
- sur la classe 𝒦₁₄ : revêtements, quotients, produits (§3) ;
- sur les configurations partielles : complétions du cadre, route Ω de l'équipe ;
- sur les blocs locaux admissibles de l'équipe.

Dans les deux derniers cas, le « flot » naturel est une recherche locale (recuit, CDCL), essayée sans succès (CARTE §4.A).
Surtout, on ne connaît **aucune quantité monotone à cas d'égalité rigide** sur ces espaces. Sans elle, une dynamique ne
démontre pas une non-existence ; elle échantillonne.

**T2 (échelle)** : sur Conway, la distance ne prend que les valeurs 0, 1 et 2. Il n'y a pas de séparation d'échelles.
Sur la classe 𝒦₁₄, les échelles existent jusqu'à 9 (Huang–Liu–Xia). L'induction sur les échelles de Perelman (S4) n'a
de support que sur la classe. Sur le graphe lui-même, la seule hiérarchie est combinatoire (sommet, droite, étoile,
bloc), et c'est celle des « étages » de l'équipe.

---

## 2.6 Apport par rapport à la campagne

| résultat | statut | apport |
|---|---|---|
| A.1 (no-go) | P | Ferme avec preuve la route « flot de Perelman sur le graphe » : toute fonctionnelle spectrale ou 2-locale est constante. Généralise la constatation empirique de l'équipe que les relaxations et tests locaux sont satisfiables (CARTE §4.B, §4.F) |
| A.2 (arêtes) | L (+ formule en α, P) | Rien de neuf sur le fond ; c'est l'outil du §3 (finitude de π₁) |
| A.3 (non-arêtes) | P (+ E) | Un invariant local nouveau, η, le seul qui échappe aux paramètres côté Ollivier. Il distingue les quatre srg(243). Sans usage d'exclusion pour l'instant |
| Corollaire 2.2 | P (trivial) | Reformulation extrémale : Conway = membre minimal de 𝒦₁₄ ; le non-effondrement à l'échelle 3 est équivalent au problème. Sert au §4 |
