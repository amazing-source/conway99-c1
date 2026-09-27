# 99 — Verrou principal : boules de droites (L21), triplets de droites, et ce que cela dit du verrou

*25/09, de 03 h à 05 h 30 (suite de la nuit). Consigne : « Continue sur le verrou principal ». Le verrou = aucune borne inférieure sur P (aucun
plafond de torsion) et aucune obstruction globale ; seule borne : L16, P ≤ 1151. Tout ce qui suit est vérifié ; les
résultats négatifs sont donnés comme tels.*

## 0. Résumé
| | énoncé | statut |
|---|---|---|
| **L21** | pour toute droite L : **k ≥ 23 − d(L)**, d(L) = dim ker₇(A_{G(L)} − 3I), G(L) = graphe cubique induit sur les 36 points voisins d'exactement un point de L ; d(L) = (composantes) + (7-rang du groupe du tas de sable de G(L)) | **preuve à la main**, identité vérifiée sur 700 configurations aléatoires (0 échec) |
| conséquence | une droite « 7-générique » (G(L) connexe, nombre d'arbres couvrants non divisible par 7) donne **k ≥ 22** | preuve à la main |
| explication | le rang du bloc « deux étoiles » de notes/97 vaut rang₇(A_{G(L)} − 3I) − 13 ; L20 est le cas « deux points de L » | preuve à la main |
| numérique | d(L) = 1 dans 85 % des configurations admissibles aléatoires, 2 dans 14 %, 3 dans 0,6 % (Cohen–Lenstra : 16 %) ; maximum trouvé par recuit : **d = 9** (deux étoiles (0;2,2,2), holonomie à 6 points fixes) | conjecture : d ≤ 9, donc k ≥ 14 |
| triplets de droites | modèle exact des comptages de triplets de droites (configurations à 9 points), 4 repères de l'espace des droites dont un (dim 132) invisible depuis les points ; validé sur BvLS | **négatif** : P ∈ [0, 1155] (retrouve L16 côté droites, rien de plus) |
| enraciné en une droite | même modèle vu d'une droite, avec la structure locale exacte ; validé sur BvLS | **négatif** : une droite sans prisme ni barreau de prisme est permise |
| F₃ | fonctions à valeurs dans F₃ de somme nulle sur chaque droite : les géométries tordues en ont (2, 5, 7) | **négatif** |
| heuristique | un Γ « tordu générique » aurait P ≈ 126 et k ≈ 30 | explique pourquoi aucune moyenne ne peut donner P ≥ 1152 |

**Le verrou principal reste entier.** Ce qui a changé : on sait maintenant que la voie 7-adique pousse k vers le haut
(k ≥ 22 pour une seule droite générique), donc toute stratégie qui aurait besoin d'un k petit (L19, « cible k ≤ 4 » de
notes/97) est irréaliste. Et la hiérarchie positive s'étend d'un cran (triplets de droites, 9 points) sans rien
donner.

## 1. Lemme L21 (boule d'une droite)
*Notations.* L = {x, a, ā} une droite. Pour p ∈ L, X_p = N(p) ∖ L (12 points). N(L) = X_x ⊔ X_a ⊔ X_ā (36 points,
chacun adjacent à exactement un point de L). G(L) = graphe induit sur N(L). Dans les coordonnées de x :
X_x = les 12 étiquettes, X_a = étoile(a), X_ā = étoile(ā).

**(a) G(L) est cubique.** Pour u ∈ X_p : u a exactement un voisin dans X_p (l'autre point de sa droite par p ; un
second donnerait un triangle hors droite). Pour p' ∈ L ∖ {p} : u ≁ p', et μ(u, p') = 2 donne exactement un voisin
commun autre que p, qui est dans X_{p'}. Donc u a exactement un voisin dans chaque partie : une arête du couplage
interne (droites par p) et deux arêtes du 2-facteur de Lou–Murin C(L). Les 10 autres voisins de u sont hors de la boule.

**(b) Réduction.** Sur la boule L ∪ N(L) (39 points), A − 3I = [[J₃ − 4I₃, R], [Rᵀ, A_G − 3I]], R = incidence
(chaque u ∈ N(L) a un seul voisin sur L). Le bloc J₃ − 4I₃ a pour déterminant −16, inversible mod 7, d'inverse
−(I + J)/4. Comme RᵀR = D (blocs J₁₂ sur les trois parties) et RᵀJR = J₃₆, le complément de Schur est
S = A_G − 3I + (D + J)/4 ≡ A_G − 3I + 2D + 2J (mod 7).
Soit U = ⟨1_{X_x}, 1_{X_a}, 1_{X_ā}⟩. La forme standard est non dégénérée sur U (12 ≢ 0 mod 7), donc
F₇³⁶ = U ⊕ U^⊥. A_G 1_{X_p} = 1_{N(L)} (un voisin dans chaque partie), donc A_G préserve U, et U^⊥ par symétrie ;
D et J sont nuls sur U^⊥. Sur U^⊥, S = A_G − 3I. Sur U, A_G − 3I agit par J₃ − 3I₃ (valeurs propres 0, −3, −3 :
rang 2) et S par 25J₃ + 21I₃ ≡ 4J₃ (rang 1). Donc rang₇ S = rang₇(A_G − 3I) − 1 et
  **rang₇ (A − 3I)[L ∪ N(L)] = 3 + rang₇ S = 2 + rang₇(A_{G(L)} − 3I).**

**(c) Borne.** Une sous-matrice principale a un rang au plus égal : 38 − d(L) ≤ rang₇(A − 3I) = 15 + k, d'où
**k ≥ 23 − d(L)**.

**(d) Tas de sable.** 3I − A_G est le laplacien du graphe cubique G(L). Par la forme de Smith,
dim ker₇(3I − A_G) = c(L) + r₇(K(G(L))), où c = nombre de composantes et K = groupe critique (tas de sable), d'ordre
le nombre d'arbres couvrants τ par composante. Pour G(L) connexe : **d(L) = 1 ⟺ 7 ∤ τ(G(L))**, et alors k ≥ 22.
(Vérifié : 317 configurations admissibles aléatoires, 0 exception.)

**(e) Cas particulier : L20.** Même calcul sur L ∪ X_x ∪ X_a (27 points). Le graphe induit est 2-régulier : un cycle
de longueur 4m par cycle de longueur m du graphe de classes de τ_a. Sur U (dim 2), A − 3I agit par [[−2, 1], [1, −2]]
(rang 2) et S par 4J₂ (rang 1). Pour un cycle C_n, 2cos(2πj/n) ≡ 3 (mod 7) exige une racine primitive 8ᵉ de l'unité
(3² ≡ 2), d'où rang₇(A_{C_n} − 3I) = n − 2·[8 | n]. On obtient 2 + 24 − 2e = 15 + (11 − 2e) : **c'est L20.** Pour un
seul point de L (B₁(x)), le même calcul donne 15 (moulin inversible).

**(f) Ce que L21 explique.** L'observation « deux étoiles couplées » de notes/97 (rang presque toujours 22, jamais
moins de 18 au hasard, minimum trouvé 14) est exactement 23 − d(L) : d = 1 générique, d = 9 au minimum trouvé.

**(g) Contrôles.** Identité rang(S₂₄) = rang₇(A_G − 3I) − 13 = rang(boule) − 15 : 0 échec sur 700 configurations
(τ_a, τ_ā, σ) aléatoires (`code/line_ball.py`). Admissibilité locale (λ ≤ 1, μ ≤ 2 dans la boule) testée.

## 2. Jusqu'où d(L) peut-il monter ?
Recuit simulé (`code/line_ball_sa.py`, `code/line_ball_types.py`) par paire de types (τ_a, τ_ā), holonomie σ libre :
max d = 9 pour (0;2,2,2) × (0;2,2,2) ; 8 pour (0;2,2,2) × (2;2,2), (2;2,2) × (2;2,2) et (0;2,4) × (0;2,4) ; 7 pour
(0;2,4) × (2;4), (0;2,2,2) × (4;2), (2;2,2) × (4;2) et (4;2) × (4;2) ; configuration « grille » (σ = id, τ = mates) :
d = 6 (six prismes K₃ × K₂) ; tous les autres couples ≤ 6. Sans la contrainte d'admissibilité, mêmes ordres de
grandeur (écarts ≤ 2). Réserve : un seul représentant par type pour τ_a et τ_ā (même couplage quand les types
coïncident) ; la position relative de τ_a et τ_ā n'est pas explorée, et le recuit n'est qu'une minoration du maximum.
- **Si d ≤ 9 toujours, alors k ≥ 14** (et k = 14 imposerait d = 9 sur les 231 droites). Non prouvé : l'espace est
  de ~10¹¹ orbites, trop pour une énumération. Pistes de preuve : si l'un des trois graphes 2-réguliers
  « deux points de L » n'a aucun cycle de longueur ≡ 0 (mod 8), l'élimination d'une partie donne d ≤ 12 ; au-delà,
  d ≥ 13 impose un vecteur u ≠ 0 avec (M + T₁)u = 0 et (M + 3 + Σᵀ)u = 0, ce qui force σ à fixer ou échanger des
  points des 4-cycles alternés (analyse à terminer).
- **Dichotomie rigoureuse** : k ≥ 22, ou bien *toutes* les droites de Γ sont 7-dégénérées (G(L) non connexe ou
  7 | τ(G(L))). Heuristique de Cohen–Lenstra : une droite est dégénérée avec probabilité ≈ 1/6.

## 3. Conséquence pour le verrou : la voie 7-adique ne donnera pas le verrou
- Toutes les bornes locales sur k sont des **minorations** (rang d'une sous-matrice), et elles montent : k ≥ 10
  (prouvé), k ≥ 22 dès qu'une droite est générique, k ≥ 14 si d ≤ 9. Une contradiction demanderait une **majoration**
  globale de k (des vecteurs du noyau mod 7 au-delà des 54 rationnels), et aucun mécanisme n'en fournit.
- Heuristique : pour un Γ « générique », le déficit 30 − k est le 7-rang d'un groupe de type Cohen–Lenstra, donc
  k = 30 (ou 28) est attendu. L19 (« presque vide si k est grand ») et la cible « k ≤ 4 » de notes/97 ne sont donc
  pas des voies réalistes vers la non-existence.

## 4. Triplets de droites : l'ordre 9 par les droites (négatif)
*Objets.* L'espace des droites R²³¹ se scinde selon G_L = N_LᵀN_L en quatre sous-espaces propres : 21 (dim 1), 10
(dim 54, côté E₃), 3 (dim 44, côté E₋₄ : Π₃ = K/21) et 0 (dim 132 : combinaisons de droites nulles en chaque point).
Leurs projecteurs ont des entrées qui ne dépendent que de la relation entre deux droites (même, sécantes, disjointes
avec e = 0…3 arêtes), calculées exactement via (7I + A)⁻¹ = (64/315, −19/630, 1/315) :
Π₀ ∝ (120, −20, −6, 1, 8, 15), Π₁₀ ∝ (180, 70, −18, −7, 4, 15), Π₃ ∝ (4, 0, 1, 0, −1, −2), Π₂₁ = J/231.
**Le repère de dimension 132 est invisible pour toutes les matrices de Gram de points** (E₃, E₋₄) utilisées jusqu'ici.
*Modèle* (`code/line_triples_gen.py`, t général). Comptages X[r₁,r₂,r₃] de triplets ordonnés (L, M, N), symétriques.
Exactement connus : {m,m,m} = 20790 (concourantes ; pas de triangle de droites), {m,m,e} = e·N(e), {m,e,e'} en
fonction de P et de la distribution locale en un point p relativement à une droite N (types A/B si p ∈ N(N), avec
n_A = 6P ; (a, b, c) si p est à distance 2). Inconnus : les 20 comptages de triplets de droites deux à deux disjointes
(9 points), Q₂ = Σ_L π(L)². Contraintes : marges, idempotence de chaque projecteur, positivité des Gram enracinés
agrégés, pour les 4 repères et leurs produits de Hadamard.
*Validation* : sur BvLS (t = 10), tous les comptages recalculés directement (0 écart), 0 équation violée, toutes les
matrices de Gram (y compris les produits de Hadamard jusqu'au degré 3) semi-définies positives
(`code/validate_bvls_triples.py`).
*Résultats pour 99* (`code/line_triples_sdp.py`) : degré 1 : P ∈ [0, 1386] ; degrés 2, 3, 4 (14, 34, 69 noyaux) :
**P ∈ [0, 1155]**, c'est-à-dire exactement L16 côté droites. Le système exact est cohérent (rang 15, 10 paramètres
libres). Le relâchement impose déjà Q₂ ≥ 4P²/231 (Cauchy–Schwarz) et Q₂ ≤ 24P, rien d'autre.
*Incident* : un premier calcul mal mis à l'échelle annonçait P ≤ 178 (statut « inaccurate »). Mise à l'échelle
corrigée : artefact. Noté ici pour mémoire.
*Version enracinée en une droite* : §4 bis.

## 4 bis. Enraciné en une droite : une droite sans prisme est-elle possible ? (négatif)
*Idée.* Si une petite valeur de π(L) était impossible, toutes les droites porteraient beaucoup de prismes, d'où une
borne inférieure sur P. Plus finement : avec μ_L = Σ_{e ⊂ L} m(e) (prismes dont un barreau est sur L), on a
Σ_L μ_L = 3P et Σ_L π(L) = 2P ; si le couple (π, μ) = (0, 0) était exclu, P = 0 le serait aussi.
*Modèle* (`code/line_rooted_sdp.py`). Pour une droite L fixée, y[r₁,r₂,r₃] = #{(M,N) : rel(L,M) = r₁,
rel(L,N) = r₂, rel(M,N) = r₃}. Exact : marges n_r(π), structure des droites par un point de L (y[m,m,·] en fonction
de μ_L ; y[m,e,m] = e·n_e ; y[m,3,·] = 15π en e' = 1), identités par droite tirées de (Π²)_{LN} = Π_{LN},
positivité des Gram enracinés pour tous les produits de Hadamard jusqu'au degré 3. Version fine : décomposition exacte
de y[m,e,·] selon le type local du point de L relativement à N (par exemple y[m,2,3] = y[m,0,3] = 0,
y[m,2,2] = y[m,2,0] = 2n₂ + A₂, y[m,1,3] = nombre de N de type A), avec 4 paramètres auxiliaires bornés.
*Validation* : droite de BvLS, contraintes vérifiées au point réel (écart 9·10⁻¹¹), versions grossière et fine.
*Résultats pour 99* : version grossière, π(L) = 0, 1, …, 7 tous faisables ; version fine, **π(L) = 0 faisable avec
μ_L ∈ [0, 18]**, c'est-à-dire tout l'intervalle. Une droite entièrement tordue (ni prisme, ni barreau de prisme) n'est
exclue par rien de ce qui précède. Aucune borne inférieure sur P. Calcul arrêté après ce cas, qui tranche la question.

## 5. Autres pistes examinées ce jour
- **Fonctions F₃ de somme nulle sur les droites** (colorations où chaque droite est monochrome ou arc-en-ciel). Idée :
  la torsion les tuerait, et une raison globale les imposerait. Calcul (`k3` sur les exemples) : srg(9) 4, H(3,3) 8,
  tordue t=2 (20) : 5, tordue t=3 (39) : 2, (42) : 7, tri-incidence t=5 (93) : 2, BvLS : 12. La torsion ne les tue
  pas sur ces exemples. Abandonné pour ces exemples, NON TESTÉ en diamètre 2 (re-scopé 27/09).
- **Heuristique du Γ tordu générique.** Si les τ_a se comportaient comme des couplages aléatoires, chaque arête serait
  barreau de 6/11 prisme en moyenne, d'où P ≈ 693·(6/11)/3 ≈ 126, loin sous 1151 ; k ≈ 30. Une borne inférieure
  P ≥ 1152 reviendrait à prouver que Γ est presque un quotient de Hamming (une version « stable » de L1). Tous les
  relâchements essayés (ordre ≤ 8, triplets de droites) restent faisables autour de P ≈ 126 ; une méthode par
  moyennes ou par positivité ne distingue pas ce régime d'un vrai SRG.
- **Orientation cohérente des droites** (cocycle ±1 sur les paires d'arêtes opposées, droites orientées
  cycliquement). Vérifié à la main : un prisme ne crée aucune frustration (le triangle des trois barreaux a un produit
  de signes +1, et les trois liens entre ses deux droites ont le même signe). Lien avec la torsion non établi ; idée
  notée, non développée.

## 6. Ce qu'il faudrait pour le verrou
Une information **exacte et non moyennée** que la structure tordue générique viole : intégralité fine (du type
π(L) ≠ 11 de Lou–Murin), une majoration globale de k, un argument de revêtement pour le cas tordu, ou l'exhaustion.
Les trois familles essayées (positivité jusqu'à 9 points par les droites, arithmétique 7-adique locale, codes F₃) sont
maintenant épuisées au niveau où elles sont calculables sur le portable.
