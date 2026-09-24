# Branche C1 de srg(99,14,1,2) — rapport de la session du 2026-09-24

*Chercheur F (idées) + chercheur R (attaques), budget non limité. Rien ici ne résout le problème.*
*Tout résultat utilisé est redérivé ici ; l'ancien repo conway-99-research n'a servi que d'index de noms.*
*« Obstruction » = preuve par l'absurde : on suppose que Γ existe et on cherche une conséquence impossible.
Les lemmes ci-dessous sont des conséquences obligatoires prouvées ; aucune n'est encore contradictoire.*

## 1. En bref

1. **Γ est forcément « tordu »** (L1, preuve complète) : sinon Γ serait un quotient de H(7,3), donc 99 | 3⁷.
   Même conclusion pour 6273 et 494019.
2. **La torsion n'a pas d'obstruction purement locale** : géométries tordues explicites (non SRG) pour t = 2, 3, 5, 7,
   dont une famille venant des plans projectifs (tri-incidence (S, −2S, S) sur Z_{q²+q+1}). Toute obstruction doit
   utiliser μ = 2 pour *toutes* les paires (« excès nul »).
3. **Mais les sommets presque non tordus sont impossibles** (nouveau, calcul exact + contrôles) :
   - **L8 : aucun sommet n'est dans ses 21 grilles** (3 exécutions, 2 encodages indépendants) ;
   - **L7** : même chose avec σ_x automorphisme — dans la branche C2, **le point fixe de l'involution est tordu** ;
   - **L10 : au plus 18 grilles par sommet** ; **L11** : les torsions d'un sommet touchent au moins 4 classes ;
     une étiquette tordue seule, ou une seule classe tordue, est impossible (réfuté par simple propagation) ;
   - **L9 (preuve à la main)** : une torsion entourée de transitions « mate » force l'absence d'une grille voisine.
4. Les trois pistes de ChatGPT : **A absorbée** (cohérence T/Δ = fermeture de grille) ; **B tuée comme source
   d'obstruction** (holonomie canonique mais non contrainte : 0 violation sur 15 765 configurations) ; **C survit
   comme lemme** (L4 : le recollement 7-adique du 70-espace vaut rank₇(A − 3I) − 15, pair, identique en tout sommet).
5. Arithmétique : rank₇(A − 3I) **impair** (L2) ; recollement 7-adique **non scindé** (L3).

## 1 bis. Mise à jour (après-midi du 2026-09-24)
- **Frontière par nombre d'étiquettes tordues** : 1 et 2 étiquettes impossibles (|C| = 2, 3, 4 exclus ; |C| = 5 en
  cours) ; 3 étiquettes : 128 motifs à symétrie près, 24 traités, tous UNSAT (≤ 73 s).
- **Validation de toute la méthode sur l'analogue q = 2** : le modèle enraciné reconstruit Gewirtz en 1,9 s, et
  imposer une fermeture en 3-cube est UNSAT (13 s) — Gewirtz est *maximalement* tordu (0/6720 fermetures).
- **Contre-poids honnête** : dans l'analogue q = 2, le seul SRG tordu connu est tordu au maximum ; la torsion forte
  n'est donc pas, en soi, un argument contre l'existence. Reste l'argument du groupe (|Aut(Gewirtz)| = 80 640,
  |Aut(Γ)| ≤ 3).
- **Nouvelles identités exactes** : P = 1386 − (1/6)Σ_x|W(x)| et Σ_x|W(x)| = 6048 + Σν³ (L15, via Hodge F21) : la
  torsion totale est un moment spectral ; la borner donnerait des sommets peu tordus, que la frontière exclut.
- **Correction** : un test de « 3-cycle étiqueté » était trop strict (2 conditions sur 3) ; sans effet sur les modèles
  SAT (λ exact), il n'avait biaisé que l'échantillonnage des τ aléatoires. Corrigé.
- Sonde τ aléatoire (14 étiquettes tordues, 0 grille) : pas de verdict en 1 h (difficulté, pas d'information).

## 1 ter. Mise à jour (soir du 2026-09-24) : la route Hodge / Σν³ est close (notes/60)
- **Correction d'une affirmation antérieure.** J'avais proposé de confiner le spectre rotationnel du laplacien de
  Hodge dans [−4, 3] par une méthode local→global (Garland). C'est **faux pour tout SRG de la famille avec t ≥ 2**
  (théorème H0) ; BvLS, qui existe, a 231 valeurs propres rotationnelles hors de l'intervalle analogue [−5, 4]
  (−20, −2, 7 ; prédites par théorie des représentations et vérifiées par calcul). Et l'identité de Garland est
  vide ici, le lien K₁₄ ne voyant pas les arêtes opposées.
- **Ce qui survit** (identités exactes, vérifiées sur 7 géométries) : la torsion est la non-commutation de Q avec
  l'opérateur des triangles, ||[Q, B_T]||² = 24(P_max − P) = 4Σ_x|W(x)| ; les traces par blocs H3. Une mutation
  (« évitement » sur les cochaînes fermées sur les triangles) équivaut à F2-SRG : reformulation, pas levier.
- **Recherche ciblée.** Reimbayev (arXiv:2608.19410, 2026) : les 208 fréquences d'ordre 7 dans srg(n,k,1,2)
  dépendent de deux variables libres, dont n₃ = ½Σ|W| (confirmation indépendante de L15) ; à (99,14) leur
  non-négativité ne donne que la borne triviale n₃ ≤ 4158. La liste publiée échoue la règle de somme sur les
  constantes (au moins deux coquilles), sans effet sur ces conclusions. Lou–Murin (2014) : faits locaux seulement
  (nombre de prismes par droite ≠ 11).
- **Bilan.** Borner Σν³ = majorer la torsion totale n₃ ; aucune méthode connue ne le fait ; c'est équivalent à
  « tout SRG PQ(2,t,2) est grid-full », au moins aussi dur que l'unicité de BvLS.

## 1 quater. Nouveau résultat mathématique (sans SAT) : P ≤ 1151 (notes/70, lemme L16)
- Dans l'espace propre E₋₄ (dimension 44), les 231 droites donnent des vecteurs dont les produits scalaires ne
  dépendent que de la configuration locale ; les 7 droites par un point y sont **deux à deux orthogonales** (fait
  propre à 99). La somme des cubes de ces produits est une norme au carré, donc ≥ 0, ce qui donne
  **12P = 13860 − 64‖Σ_L u_L^{⊗3}‖²**, d'où P ≤ 1155, et P ≤ 1151 en ajoutant les points.
- Conséquences : Γ est tordu (nouvelle preuve de L1, spectrale) ; torsion moyenne ≥ 14,2 paires par sommet ; au
  moins 705 paires de droites reliées par 2 arêtes. Démonstration de quelques lignes, vérifiable à la main.
- Limite honnête : c'est une condition nécessaire, pas une contradiction. Toutes les inégalités de ce type
  essayées (drapeaux, graphe des droites, conditions locales, tous degrés) vont dans le même sens ; une
  contradiction demanderait une borne *inférieure* sur P, que je n'ai pas.

## 1 quinquies. Nuit du 2026-09-24 : la seconde variable libre, et des résultats négatifs (notes/90)
- **L18 (nouveau, vérifié par comptage direct)** : dans srg(n,k,1,2), les fréquences d'ordre 7 de Reimbayev
  dépendent de deux statistiques de torsion, n₃ = ½Σ|W| et **S = nombre de couples (x, E) avec E adjacent à σ_x(E)**
  (σ_x = réflexion ponctuelle, involution de Bondarenko–Radchenko ; S = nombre de coïncidences τ_a(c) = τ_c(a)).
  z₁₁ = 4n₃ − 2S, et le polygone d'ordre 7 est exactement 0 ≤ S ≤ n₃. Avec L16 : 705 ≤ n₃ ≤ 4158, 0 ≤ S ≤ n₃.
- **Grilles avortées** : pour chaque sommet et chaque paire de classes, les 9 points de la grille potentielle ont une
  projection sur E₋₄ de norme² 18·(nombre d'arêtes manquantes) ; somme totale 2n₃ − S/2. Toute la torsion est dans
  un opérateur de défaut Δ (entier, nul ssi Γ est non tordu, positif sur E₋₄).
- **Résultat négatif** : la borne de Delsarte locale sur le schéma des étiquettes (B₇, 6 relations) est triviale ;
  les traces exactes de H sur les trois composantes irréductibles de K ne plafonnent pas la torsion.
- **Piste arithmétique propre à C1** : U_x = (2H + 1)σ_x est une similitude entière de norme 49 sur K ; la torsion y
  crée des valeurs propres qui sont des entiers algébriques de norme 49 (par exemple 3 − 5ω). C'est l'analogue, sans
  symétrie, de la structure d'Eisenstein de C3. Aucune contradiction obtenue.
- Lecture de Bondarenko–Radchenko (JCTB 2013) : leur preuve (σ_v automorphismes ⇒ F₃-espace ⇒ n = 3^m) échoue
  pour 99 parce que g = 44 > k = 14 : il reste 30 dimensions libres par sommet, et c'est là que vit la torsion.

## 2. Piste principale : « frontière de torsion » (notes/50)
On fixe ou on libère partiellement le système de transitions τ en un sommet et on impose toutes les équations SRG
dans le modèle enraciné exact (99 sommets). Chaque UNSAT exclut une famille de configurations locales en tout sommet
de tout srg(99,14,1,2). Résultats : les configurations presque non tordues tombent (souvent par propagation) ; un τ
générique ne tombe pas. La torsion est donc « étalée » en chaque sommet.
**Ce qui manque pour une contradiction** : soit pousser la frontière jusqu'au bout (équivaut au problème complet,
peu probable), soit trouver une identité globale qui limite la torsion totale (prismes, grilles, surface Σ, invariant
7-adique…) et la confronter à « forte torsion partout ». Aucune n'est trouvée à ce jour.

## 3. Méthode
- Fondations redérivées des axiomes (`notes/00`). Idées (`notes/10`), attaques et verdicts (`notes/20`), lemmes
  (`notes/30`), point de Hamming (`notes/40`), frontière de torsion (`notes/50`).
- Témoins : srg(9,4,1,2), BvLS (non tordus), Gewirtz (analogue q = 2, tordu et existant : garde-fou contre les arguments
  de « torsion pure »), puis les géométries tordues construites ici.
- Chaque UNSAT a un contrôle positif relâché (SAT) ; les résultats importants ont un second encodage indépendant.
- Calculs sous plafond mémoire (`run_capped.ps1`).

## 4. Verdicts des idées (détails `notes/20`)
| Idée | Verdict |
|---|---|
| A — algèbre T/Δ | absorbée (= fermeture de grille) |
| B — monodromie des transitions | tuée comme obstruction ; invariant conservé |
| C — 70-espace + transitions | lemme L4 |
| F2 rigidité locale q = 3 | tuée (exemples tordus) ; forme SRG = conjecture « tout PQ(2,t,2) est grid-full » (implique l'unicité de BvLS, ouverte) |
| F2' revêtement universel | tuée (H₁ = 0 des géométries tordues) |
| F3 ensembles serrés × τ | tuée |
| F4 Fano / cohérence de classes | tuée (locale) |
| F5 genre / oddité | lemmes L2, L3 |
| F6 Arf | absorbée par F5 |
| F11 variété plate cubique | tuée |
| F14 annulation de Krein | tuée |
| **F15 point de Hamming** | **lemme L8** |
| F16 rigidité ⇒ symétrie | L7 (côté C2) ; ouverte pour C1 |
| F17 torsion ⇒ plan projectif d'ordre t | ouverte, affaiblie (2e géométrie t = 3 non planaire) ; t = 6 tri-circulant : N = 34 aucune solution, N ≤ 60 en cours |
| F9, F10, F12, F13, F18 | encodages / non tranchées |

## 5. Nouveau à ma connaissance (à confronter à la bibliographie)
- La lecture « Γ = H(7,3) replié au rayon 2, obligatoirement tordu », et la torsion comme compression.
- Les géométries tordues comme témoins ; la famille tri-incidence (q = 3, 5, 7 ; échec pour q pair).
- L7–L11 (exclusions locales exactes) ; L9 à la main.
- L2–L4 (dérivation indépendante ; des énoncés voisins existent peut-être chez Brouwer–van Eijl).

## 6. Pour le PC du labo
1. Contrôle positif t = 10 du modèle enraciné (BvLS doit être SAT) — valide le code générique.
2. Certificats DRAT pour L7, L8, L10, L11.
3. Poursuivre la frontière : confined(K), |K| = 4, 5, 6 ; sources(S) croissants ; familles « g(x) ≥ G ».
4. Tri-circulants t = 6 au-delà de N = 60 ; graphes de Cayley tordus d'ordre 100–200.
