# Route R8 : audit du modèle, contrôle positif, coût, variante CEGAR (LAB, 20/10/2026, 15:10-16:40 UTC)

Mission : auditer R8 et estimer honnêtement son coût comme calcul de cluster. Le coordinateur a ensuite demandé
d'ajouter la variante spectrale (CEGAR).

Les calculs ont été arrêtés à 16:33 UTC. Le chien de garde a suspendu tous les processus boost à l'ouverture d'un jeu, et
j'ai tué mon propre processus suspendu. Tout ce qui suit a tourné avant cette heure, sauf ce qui est marqué NON LANCÉ
(liste complète au §7).

Conditions de mesure :
- un seul processus à la fois, au plus 300 s par lancement, mémoire déclarée (pic observé ≤ 0,75 Go) ;
- 7800X3D partagé et chargé à environ 77 % par d'autres travaux, donc les temps sont bruités ;
- CaDiCaL 3.0.1 (binaire `tools/win64`) et pysat 1.9 (glucose4 et cadical195 incrémental).

Statuts utilisés : PROUVÉ (preuve écrite ici), EXACT (calcul complet), SAT/UNSAT (verdict de solveur sans certificat),
MESURE (échantillon), EXTRAPOLATION.

## 0. En bref

1. **Le modèle est solide.** Toutes les contraintes de R8 (C1 exactes pour les étoiles 0..3, C1' bornées, C2' plafonds)
   sont des conséquences de srg(99,14,1,2) autour de n'importe quel sommet (PROUVÉ, §1). L'encodeur de l'archive
   (`five_cnf.py`) les traduit fidèlement. Je l'ai recoupé avec mon encodeur indépendant et mon vérificateur indépendant
   sur 4 610 affectations, avec 0 désaccord. **Aucune contrainte non solide n'a été trouvée.** « R8 INFAISABLE ⇒ pas de
   Conway » est donc correct.
   - Remarque : le problème à cinq étoiles, qui ajoute « lettre 4 exacte sur X », est aussi solide et strictement plus
     fort. Pour exclure Conway, il suffit donc aussi.
2. **Contrôle positif k = 22 réussi.**
   - Six srg(243,22,1,2) ont été vérifiés exactement. Leurs 108 structures locales satisfont toutes les contraintes, et les
     deux encodages les acceptent par propagation seule.
   - Un seul arc retourné donne UNSAT (18 cas sur 18).
   - L'analogue de R8 à k = 22 est SAT en 5,5 s et 6,5 s (mon encodeur) et en 18 s (encodeur de l'archive). Les trois
     solutions ont été vérifiées indépendamment.
3. **Renforcements prouvés.**
   - L4B (capacité serrée ⇒ lettre 4 exacte sur la base) et XPAIR (borne des paires de X) sont des conséquences de R8
     (PROUVÉ, §3).
   - Mesure : avec L4B + XPAIR, deux instances témoins passent de TIMEOUT à 60 s à 5,7 s et 19,7 s (gain ≥ 10× et ≥ 3×).
   - Cassage de symétrie : les 52 classes de M₀ ont été recalculées indépendamment et le lex-leader du stabilisateur est
     écrit. Leur effet n'a PAS été mesuré.
4. **Coût de R8 pur (MESURES + EXTRAPOLATION) : pas réaliste à 10⁵ heures-cœur, sauf dans le coin le plus optimiste.**
   - Aucun découpage essayé ne rend les cubes faciles :
     - arbre lookahead à la profondeur 40 : 5,7·10¹³ cubes, et 6 sur 6 sont encore en TIMEOUT à 30 s ;
     - à la profondeur 100 (871 arêtes sur 1 326 fixées) : TIMEOUT à 95 s avec trois encodages ;
     - rattachements de X : environ 10⁴⁰ à 10⁴¹ (étiquetés).
   - Montée en difficulté par relâchement d'une base : facteur ×2 à ×2,6 par label de base relâché. L'extrapolation à
     R8 donne :
     - de 5·10⁷ à 10¹² heures-cœur sans cassage de symétrie ;
     - de 2·10⁴ à 4·10⁸ heures-cœur avec un cassage idéal (÷3 072).
   - L'incertitude couvre au moins 8 ordres de grandeur (§4.5).
5. **Variante CEGAR spectrale** (T_S ⪰ 0, U_S ⪰ 0, puis rang ≤ 30 et rang₇ ≤ 28 en contrôle).
   - Définitions vérifiées : le bloc H de NOTE_BORNE_RANG et le T de l'archive sont égaux terme à terme. T + U = 7Π et les
     rangs 30 et 40 sont validés (analogues sur de vrais srg(243)).
   - Le code est prêt : générateur de coupes entières exactes, encodeur PB→CNF testé exhaustivement.
   - **Pilote : une seule itération a tourné** (5 coupes, sur 11 à 15 labels). Il n'existe aucune donnée de convergence
     et aucun UNSAT.
6. **Recommandation.**
   - Ni R8 pur ni la variante CEGAR n'est aujourd'hui un dossier de cluster.
   - R8 pur : les mesures ne soutiennent pas le budget de 10⁵ heures-cœur.
   - La variante CEGAR est la meilleure piste : les témoins combinatoires violent massivement la positivité, à travers des
     motifs locaux de 9 à 15 labels. Mais son coût est inconnu. Étape suivante : un pilote LOCAL d'environ 1 à 2 jours en
     tranches de 5 min (§5.4, §6).

## 1. Énoncé de R8 et audit de solidité

### 1.1 Cadre

Γ est un srg(99,14,1,2) et v un sommet. Ses 14 voisins (les lettres) sont appariés en 7 droites {v, 2i, 2i+1}, car λ = 1.
On note mate(y) = y xor 1.

- **Lemme L0 (labels), PROUVÉ.**
  - Un non-voisin w de v est adjacent à exactement 2 lettres (μ = 2), et elles ne sont pas appariées. Sinon les deux
    lettres d'une même droite auraient deux voisins communs, v et w, contre λ = 1.
  - Pour i, j non appariées : i et j ne sont pas adjacents (sinon {v, i, j} serait un triangle et j = mate(i)). Elles ont
    donc μ = 2 voisins communs : v et exactement un non-voisin de v. Une lettre ne peut pas être ce voisin commun, car la
    seule voisine-lettre de i est mate(i).
  - Conclusion : w ↦ {i, j} est une bijection des 84 non-voisins sur les 84 paires non appariées (les labels).
  - L_y désigne les 12 labels qui contiennent y.
- **Lemme L1 (C1), PROUVÉ.** Pour un label l et une lettre y, on a |N(l) ∩ L_y| = c(l,y), avec c = 1 si y ∈ l ou
  mate(y) ∈ l, et c = 2 sinon.
  - Si y ∈ l : l ~ y et λ = 1. Le voisin commun n'est ni v (non adjacent à l) ni mate(y), car mate(y) ∉ l (les labels
    sont des paires non appariées). C'est donc un label de L_y.
  - Si mate(y) ∈ l : l et y ne sont pas adjacents, et μ = 2. mate(y) est un voisin commun ; l'autre est un label de L_y.
  - Sinon : ni v ni mate(y) ne sont des voisins communs, donc les deux sont des labels de L_y.
  - Contrôle : Σ_y c = 4·1 + 10·2 = 24 = 2·deg_Γ(l) = 2·12.
- **Lemme L2 (C2), PROUVÉ.** Pour deux labels l ≠ l', on a |l ∩ l'| + |N(l) ∩ N(l')| + [l ~ l'] = 2, où N désigne les
  voisins parmi les labels.
  - Les voisins communs dans le graphe sont exactement les lettres de l ∩ l' (v n'est adjacent à aucun des deux) et les
    labels communs.
  - On conclut par λ = 1 si l ~ l', et par μ = 2 sinon.
- **Restriction à un ensemble S de labels.**
  - Pour une lettre y avec L_y ⊆ S, C1 reste exacte.
  - Pour les autres lettres, on a seulement |N(l) ∩ L_y ∩ S| ≤ c(l,y) (C1').
  - Les voisins communs dans S donnent le plafond |l∩l'| + |N(l)∩N(l')∩S| + [l~l'] ≤ 2 (C2').

### 1.2 Énoncé exact

On note :
- B = L₀ ∪ L₁ ∪ L₂ ∪ L₃ (44 labels) ;
- X = {{4,t} : t = 6..13} (8 labels) ;
- S = B ∪ X (52 labels, 1 326 variables d'arête) ;
- C4 = {{r,4}}, C5 = {{r,5}}, K = {02, 03, 12, 13}, B' = B \ (C4 ∪ C5) (36 labels), toujours pour r = 0..3.

**R8** demande un graphe Γ_S sur S avec :
- C1 exacte pour y ∈ {0,1,2,3} et pour tout l ∈ S, y compris l ∈ X ;
- C1' pour y ∈ {4,...,13} ;
- C2' pour toutes les paires de S.

**Théorème (PROUVÉ, L0-L2).** Tout srg(99,14,1,2), en tout sommet et pour tout étiquetage des droites, induit une
solution de R8. Donc R8 UNSAT ⇒ pas de srg(99,14,1,2), symétrique ou non, à tout rang.

**Remarque.** L₄ = C4 ∪ X est contenu dans S. La lettre 4 pourrait donc être exacte partout, et c'est le problème à cinq
étoiles de l'archive.
- R8 n'utilise la lettre 4 qu'en borne. C'est une relaxation.
- Avec L4B (§3), R8 et les cinq étoiles ne diffèrent plus que par « chaque x ∈ X a exactement un voisin dans L₄ » (au
  lieu de ≤ 1).
- Les deux énoncés sont solides. Pour exclure Conway, le plus fort (cinq étoiles) est le plus économique à réfuter ; R8
  ne sert qu'à localiser la frontière.

### 1.3 Audit du code de l'archive (`stars_rank_2026-10-14/five_cnf.py`, lu ligne à ligne)

- **C1 et C1'** : clauses binomiales « au plus c » ; « au moins c » par les sous-ensembles complémentaires. Exact, et
  appliqué à tous les labels de S pour les lettres-étoiles (valide puisque L_y ⊆ S).
- **C2'** : produits p ← e_it ∧ e_jt (avec `--reify`, aussi p → e). Compteur séquentiel dans le sens montant seulement :
  r_m est forcé dès que m produits sont vrais, et l'on interdit r_2 ou r_3 selon s = |l∩l'| et e_ij. Sound et complet
  pour « ≤ ». Le sens montant suffit, et `--reify` ne change pas la satisfiabilité (remarque de Codex, juste).
- **Lex-leader** (`--symbreak`) :
  - la chaîne a_i (« préfixe égal ») encode exactement x ≤_lex x∘g ;
  - le groupe G (D₄ sur les droites {0,1}, {2,3}, 4 et 5 fixes, groupe hyperoctaédral sur les 4 droites extérieures,
    ordre 3 072) préserve S et chaque contrainte ;
  - l'image lex-minimale d'une solution satisfait x* ≤ x*∘g pour tout g, donc toute sous-famille de G est sûre ;
  - avec `--m0`, l'archive restreint correctement G au stabilisateur de M₀.
- **Découpage M₀ (`r8_cases.py`).** L₀ est un couplage parfait (lettre 0 exacte, c = 1). Ses 10 395 couplages ont été
  recalculés par mon propre code (`build_cnf.m0_orbits`) : 52 orbites sous G₀ = {g : g(0) = 0} (ordre 768), comme dans
  l'archive. La classe 0 a une orbite de taille 1 (stabilisateur = G₀ entier, d'où les 767 éléments lex de c00).
- **Point d'attention (pas une erreur).** On ne doit jamais combiner le lex-leader du groupe G entier avec des unités M₀
  canoniques : ce sont deux formes normales différentes. L'archive ne le fait pas (`--m0` restreint au stabilisateur), et
  mon `build_cnf.py` refuse la combinaison.

### 1.4 Recoupement indépendant (EXACT sur les cas testés)

- `r8lib.py` est un encodeur réécrit sans importer l'archive.
  - C1 : formes directes.
  - C2' : TOTALISEUR tronqué sur produits réifiés, plus les clauses triangle directes pour s = 1 ; l'archive utilise un
    compteur séquentiel.
  - La numérotation des arêtes est la même que dans `five_cnf.py`.
  - `Model.check` est un vérificateur combinatoire direct.
- `test_encoding.py` : pour une affectation complète des arêtes, chacun de ces encodages est satisfiable si et seulement
  si la propagation unitaire ne trouve pas de conflit (les auxiliaires non forcés peuvent être mis à 0). On compare donc
  trois verdicts : vérificateur, mon CNF, CNF de l'archive.
  - R7 (51 labels) : 2 305 affectations. Les 5 témoins du 16/10 (graines 1, 2, 4, 5, 6) sont acceptés par les trois, et
    les 2 300 retournements ou tirages aléatoires sont rejetés par les trois.
  - R8 : 2 305 affectations (témoins + rattachements aléatoires du 8ᵉ label, retournements, aléatoires), toutes rejetées
    par les trois.
  - Total : 0 désaccord.

### 1.5 Verdict d'audit

**Aucune contrainte non solide.** Le seul « point faible » est de méthode et non de logique : l'acceptation n'est testée
positivement sur des solutions réelles qu'à k = 22 (§2), puisqu'il n'existe aucune solution de R8 connue.

## 2. Contrôle positif k = 22 (srg(243,22,1,2))

- **Graphes.** bvls243, twin243_switched, new243_trade_aut108, new243_trade_aut108_b, new243_trade_aut162 et
  new243_tricayley_Z3x4_grids25.
  - A² = 22I + A + 2(J − I − A) vérifiée exactement pour les six (`control243.py`).
- **Structures locales.** 6 sommets × 3 réétiquetages aléatoires des droites par graphe, soit 108 structures sur les 92
  labels de l'analogue de R8 (étoiles 0..3 + les 16 labels {4,t}).
  - Résultat : 108/108 satisfont C1 (lettres 0..4 exactes), C1' et C2'.
  - L4B : 108/108.
  - XPAIR : 108/108, avec z + a ≈ 52-60 ≤ 120, donc pas serré à k = 22, comme prévu.
- **CNF + structure plantée en unités** (`planted_suite.py`).
  - Mon encodeur (avec L4B, XPAIR et lettre 4 exacte) : 6/6 SAT par propagation, environ 2,5 s.
  - Un arc retourné : 18/18 UNSAT.
  - Encodeur de l'archive (cinq étoiles, `--base`) : 6/6 SAT.
- **Résolution libre** (`solve_check.py`, CaDiCaL 3.0.1), analogue de R8 à k = 22 :
  - mon encodeur, sans implications : SAT en 6,5 s ;
  - mon encodeur, avec L4B + XPAIR : SAT en 5,5 s ;
  - `five_cnf.py 22 0,1,2,3 --reify --xk 16` : SAT en 18,0 s.
  - Les 3 solutions (340 arêtes) sont vérifiées OK par le vérificateur indépendant.

## 3. Renforcements prouvés et effet mesuré

- **L4B (capacité serrée), PROUVÉ.** Dans R8, tout y ∈ B a exactement c(y,4) voisins dans L₄.
  - Chaque x ∈ X a exactement 2 voisins dans chaque L_r (C1 exacte). Les labels de K comptent deux fois, donc
    |N(x) ∩ B| = 8 − κ_x, où κ_x = |N(x) ∩ K|.
  - Par C1' (lettre 4) sur B : Σ_{y∈B} |N(y) ∩ X| ≤ Σ_y c(y,4) − Σ_{c∈C4} |N(c) ∩ B| = 80 − (24 − Σκ_c), puisque
    |N(c) ∩ B| = 1 + 1 + 2 + 2 − κ_c.
  - D'où 64 − Σκ_x ≤ 56 + Σκ_c, soit Σκ_x + Σκ_c ≥ 8.
  - Or Σκ_x + Σκ_c = Σ_{z∈K} |N(z) ∩ L₄| ≤ 4·2 = 8.
  - Toutes les inégalités sont donc des égalités. La preuve vaut pour tout k.
- **XPAIR, PROUVÉ (avec L4B).** Si y ∈ B' n'a aucun voisin dans C4, ses 2 voisins de L₄ forment une paire {x, x'} ⊂ X.
  - Ces paires sont distinctes, et chacune est une non-arête : x et x' partagent la lettre 4, donc C2' donne au plus
    1 − [x~x'] voisin commun.
  - D'où #{y ∈ B' sans voisin dans C4} + #arêtes(X) ≤ C(8,2) = 28.
  - C'est la borne n₁ + n₂ ≥ 8 + a de l'archive. Elle est encodée par un totaliseur.
- **Graphe Ω.** Le fait « 36 paires distinctes de L₄ hors de M₄ » découle déjà des plafonds C2' sur les paires de L₄,
  qui sont dans S. Rien de neuf à encoder.
- **Effet mesuré** (instances témoins I(s,m) du §4.4, CaDiCaL 3.0.1, plafond 60 s) :

| instance | r8_imp (L4B+XPAIR) | five_imp (+ lettre 4 exacte) | r8_plain (mon encodeur nu) | archive (reify) |
|---|---|---|---|---|
| I(1,10,a) | UNSAT 5,71 s (91 562 conflits) | UNSAT 5,74 s (82 278) | TIMEOUT | TIMEOUT |
| I(1,11,a) | UNSAT 19,73 s (409 574) | non lancé | TIMEOUT | TIMEOUT |

  - Lecture : L4B + XPAIR apporte au moins un facteur 10. Les effets séparés de L4B et de XPAIR ne sont PAS mesurés.
  - Conséquence pratique : tout futur calcul doit inclure L4B, et sans doute XPAIR.
- **Symétrie.**
  - `build_cnf.py --m0case k` fixe M₀ au représentant de la classe k et ajoute le lex-leader du stabilisateur. C'est sûr
    (§1.3).
  - `--lex all|N` donne le lex-leader du groupe entier ou d'un échantillon.
  - L'effet de ces options n'est PAS mesuré. L'archive avait : 3 071 éléments, 11,9 M clauses, TIMEOUT à 1 h.

## 4. Taille de la recherche (MESURES)

Tous les arbres partent des 52 classes de M₀ (poids 52). Les poids de Knuth sont des estimateurs sans biais du nombre de
nœuds de l'arbre décrit, mais leur variance est énorme ; seul l'ordre de grandeur compte.

### 4.1 Arbre des couplages M₀ → M₁ → M₂ → M₃ (`knuth_match.py`)

- La propagation n'élague RIEN : les 10 395 couplages de chaque étoile restent compatibles à chaque niveau.
- Cela fait 52 · 10 395³ ≈ 5,8·10¹³ cubes, avec seulement 304 littéraux d'arête fixés.
- Inutilisable comme découpage.

### 4.2 Arbre lookahead binaire (`knuth_la.py` : propagation et littéraux ratés sur 20 à 40 candidats, heuristique (n₊+1)(n₋+1), conquête CaDiCaL)

| profondeur | marches | ouvertes | poids W (cubes) | arêtes fixées | conquête |
|---|---|---|---|---|---|
| 10 | 4 | 4 | 5,3·10⁴ | 197-235 | 4/4 TIMEOUT à 30 s |
| 40 | 6 | 6 | 5,7·10¹³ | 511-616 | 6/6 TIMEOUT à 30 s |
| ≈ 100 | 4 | 1 (3 fermées à 95-99) | ≈ 6·10³¹ | 871 | TIMEOUT à 40 s ; même cube TIMEOUT à 95 s avec l'archive, r8_plain et five_imp |

- **Arbre DPLL avec lookahead.** Les marches se ferment vers la profondeur 95-100 : environ 52·2⁹⁵ ≈ 10³⁰ nœuds (ordre
  de grandeur sur 4 marches). Ce n'est pas faisable.
- **Anatomie du cube dur de profondeur 100** (`cube_anatomy.py`) :
  - il reste 220 arêtes base-base libres, 230 base-X libres (seulement 3 arêtes base-X vraies fixées) et 5 X-X libres ;
  - la relaxation « C1 seule » est faisable en 0,1 s (CP-SAT, diagnostic) ; le modèle complet est INCONNU à 120 s.
  - La difficulté n'est donc pas un pur comptage C1 : elle vient de C1 + plafonds, sur une base presque fixée et un X
    libre.

### 4.3 Arbre des rattachements de X (`knuth_rows.py`)

- Principe : 32 lignes (x, r) ; chaque N(x) ∩ L_r est une paire, et les options sont testées par propagation.
- Poids sur 6 marches : 1,7·10³⁸ à 2,7·10⁴¹ rattachements étiquetés (moyenne ≈ 5·10⁴⁰), soit environ 10³⁷ à symétrie
  près (÷ 3 072).
- Conquête de la base, X fixé : 5/6 TIMEOUT à 40 s, 1/6 UNSAT en 0,38 s.
- Inutilisable.

### 4.4 Montée en difficulté par relâchement (`release_scan.py`, r8_imp, CaDiCaL 3.0.1)

- Instance I(s, m, o) : R8 + les arêtes entre labels de base NON relâchés fixées comme dans la base du témoin R7 de graine
  s ; on relâche les m premiers labels dans l'ordre aléatoire o.
- I(s, 0) est UNSAT (le témoin refuse le 8ᵉ label), et I(s, 44) = R8.

| m | ordre a | ordre b |
|---|---|---|
| 0 | UNSAT 0,64 s (952 conflits) | |
| 4 | UNSAT 0,60 s (952) | |
| 8 | UNSAT 1,15 s (2 785) | UNSAT 10,9 s (218 832) |
| 9 | UNSAT 2,44 s (14 198) | UNSAT 26,4 s (550 339) |
| 10 | UNSAT 5,71 s (91 562) | UNSAT 45,0 s (846 404) |
| 11 | UNSAT 19,7 s (409 574) | TIMEOUT 90 s |
| 12 | TIMEOUT 60 s | |
| 16, 20 | TIMEOUT 60 s | |

- Facteur de croissance par label relâché :
  - en temps : ×2,6 (a) et ×2,0 (b) en moyenne géométrique ;
  - en conflits : ×5,3 (a) et ×2,0 (b).
- **EXTRAPOLATION à m = 44**, à partir de T(11) ≈ 20-90 s et d'un facteur ×2 à ×2,6 sur 33 labels : T(R8) ≈ 2·10¹¹ à
  5·10¹⁵ s pour un CDCL seul, soit 5·10⁷ à 10¹² heures-cœur.
- Avec un cassage de symétrie idéal (÷ 3 072, jamais atteint en pratique) : environ 2·10⁴ à 4·10⁸ heures-cœur.
- Avec le facteur en conflits ×5,3, c'est bien pire.

### 4.5 Synthèse des coûts et incertitude

| route | mesure | coût |
|---|---|---|
| R8 par CDCL seul (archive) | TIMEOUT à 2 h (plusieurs configurations) | > 2 h |
| cube-and-conquer, lookahead p = 10 | 5,3·10⁴ cubes, tous > 30 s | > 440 h-cœur (borne basse seulement) |
| cube-and-conquer, lookahead p = 40 | 5,7·10¹³ cubes, tous > 30 s | > 4,8·10¹¹ h-cœur |
| rattachements de X d'abord | environ 10³⁷ cubes à symétrie près | hors de portée |
| extrapolation par relâchement | ×2 à ×2,6 par label | 5·10⁷ à 10¹² h-cœur ; 2·10⁴ à 4·10⁸ avec symétrie idéale |

- **Fourchette honnête pour R8 pur : de 10⁴ (coin très optimiste) à plus de 10¹² heures-cœur.**
- Le budget de 10⁵ heures-cœur n'est atteint que si trois conditions sont réunies :
  - la croissance s'effondre au-delà de m = 11 ;
  - le cassage de symétrie gagne au moins 10³ ;
  - aucun phénomène de comptage (type pigeonnier, que la résolution ne sait pas faire) ne domine.
- **Réserves.**
  - Un seul témoin et deux ordres.
  - L'extrapolation porte sur 33 pas.
  - Le CDCL n'est pas « arborescent » : les estimations de Knuth (§4.1-4.3) majorent des méthodes arborescentes, pas le
    CDCL.
  - Le PC était chargé.

## 5. Variante CEGAR spectrale (demande du coordinateur)

### 5.1 Définitions vérifiées

- **Construction.** P_s est le projecteur sur l'espace propre de s = −4, et N = N[v] = {v} ∪ 14 lettres.
  - T = 7 · (complément de Schur de P_s sur les labels). Le bloc NN est singulier, de rang 14 : on utilise la
    pseudo-inverse.
  - U est l'analogue avec P_r, r = 3.
- **Égalités vérifiées.**
  - `spectral.py`, vrais srg(243), k = 22 : T = T0 − Γ et U = U0 + Γ avec T0, U0 locaux (erreur 2·10⁻¹⁶) ; T + U = 9Π
    (Π = projecteur sur ker B) ; spectres dans [0, r − s] ; rang T = g − k = 88 et rang U = f − k = 110.
  - Pour Conway : rangs 30 et 40, et 8T0 et 15U0 sont entiers.
  - Le H de `borne_rang_vertex_block.py` (même construction, validé par l'autre agent sur srg(243)) coïncide terme à
    terme avec le T = 3I − Γ − BᵀQB de l'archive (`kval`). C'est une assertion dans `cegar.py`, vérifiée à l'exécution sur
    les 44 labels de base.
- **Faits utilisables, pour tout S** (sous-matrices principales) :
  - T_S ⪰ 0 et U_S ⪰ 0 (compléments de Schur de matrices PSD) ;
  - U_S ⪰ 0 entraîne T_S ⪯ 7Π_S ⪯ 7I ;
  - rang T_S ≤ 30 et rang U_S ≤ 40.
- **rang₇(8T_S) ≤ 28.**
  - 8T ≡ −Σ (mod 7), où Σ est la matrice de NOTE_BORNE_RANG.
  - det(3I − W) = −2²³ n'est pas divisible par 7, donc le bloc NN est inversible mod 7 et rang₇(A − 3I) = 15 +
    rang₇(8T).
  - On conclut avec la fenêtre r₇ ≤ 43 de l'archive (audit IA, non re-dérivée ici).
  - Sans la fenêtre, (A − 3I)² ≡ 2J (mod 7) et Sylvester donnent seulement r₇ ≤ 50, soit rang₇(8T_S) ≤ 35.
- **DISC** (archive, PROUVÉ) : non utilisé dans ce pilote.

### 5.2 Coupes exactes (`cegar.py`)

- Pour q entier porté par Y ⊆ S : qᵀ(8T_Y)q ≥ 0 équivaut à Σ_{i<j∈Y} q_i q_j x_ij ≤ ⌊qᵀ(8T0_Y)q / 16⌋. Le membre de
  gauche est entier, donc l'arrondi est valide.
- Version U : Σ (−q_i q_j) x_ij ≤ ⌊qᵀ(15U0_Y)q / 30⌋.
- Construction de q :
  - vecteur propre négatif du bloc courant ;
  - sous-bloc creux obtenu par croissance puis réduction gloutonnes ;
  - arrondi entier ;
  - violation vérifiée en arithmétique entière.
- Encodage : `pbenc.py`, BDD réduit à mémoïsation d'intervalles, testé exhaustivement sur 300 contraintes aléatoires
  contre toutes les affectations.
- Option `--planted` : chaque coupe est évaluée sur des structures réelles (k = 22) et doit les respecter. C'est le
  contrôle de validité du générateur. Il est prêt, mais NON LANCÉ.

### 5.3 Ce qui a tourné

- Une seule itération, sur la base à quatre étoiles (k = 14, 44 labels).
- Le premier modèle SAT viole T ⪰ 0.
- 5 coupes de type T :
  - supports de 11, 12, 12, 14 et 15 labels ;
  - |q|∞ ≤ 8 ;
  - violations de 1 à 3 unités ;
  - bornes de 160 à 469.
- Cohérent avec NOTE_BORNE_RANG (sous-blocs non PSD minimaux de 9 à 11 labels sur les témoins R7).
- Durée : environ 3 min entre le lancement et l'écriture des coupes (résolution + coupes, non séparées). Suspendu ensuite.
- Coupes sauvées : `data/cegar/cuts_k14.jsonl`.

### 5.4 Pilote que je lancerais (NON LANCÉ) et coût attendu

Chaque étape est reprenable grâce au fichier de coupes, en tranches de 5 min.

1. **k = 22.** CEGAR quatre et cinq étoiles avec `--planted` (les 6 graphes) : aucune coupe ne doit violer une vraie
   structure, et l'on doit converger vers un modèle PSD. Environ 30 à 60 min.
2. **k = 14, quatre étoiles, T, U ⪰ 0.** Nombre d'itérations jusqu'au premier modèle PSD ; il doit exister, puisque les
   645 germes de l'archive sont PSD de rang 30. Puis rang et rang₇ de ce modèle. Environ 1 à 3 h.
3. **R_k + spectral, k = 1..8** (k labels {4,t}).
   - Critère : UNSAT ou modèle PSD de rang ≤ 30.
   - L'indice de l'archive (aucun des 645 germes de rang 30 n'accepte une seule colonne extérieure) suggère que
     « quatre étoiles + rang ≤ 30 + 1 label » pourrait déjà être vide. Ce serait une instance minuscule devant R8.
   - Environ 1 jour.
4. **R8 + toutes les coupes accumulées** : quelques essais de 280 s.

- **Limite connue.** Rang ≤ 30 et rang₇ ≤ 28 ne sont pas convexes. Seules des coupes « no-good » sont possibles, et elles
  sont faibles. Si le résidu est un problème de rang, la boucle ne convergera pas avec ces seules coupes.
- **Coût total du pilote** : environ 1 à 2 jours mono-cœur. Il ne nécessite pas de cluster.

## 6. Recommandation et chaîne de preuve

- **R8 pur : pas de lancement sur cluster.** Le budget de 10⁵ heures-cœur n'est soutenu par aucune mesure, et la
  fourchette extrapolée couvre de 10⁴ à plus de 10¹² heures-cœur. S'il faut absolument un calcul combinatoire, il
  faut :
  - viser les cinq étoiles plutôt que R8 (plus fort, aussi solide) ;
  - garder L4B et XPAIR ;
  - utiliser les classes M₀ ;
  - mesurer d'abord l'effet de la symétrie sur des sous-cas symétriques.
- **Route recommandée : le pilote CEGAR local du §5.4, avant tout cluster.**
  - S'il donne UNSAT sur un R_k petit, l'instance finale sera probablement certifiable en local.
  - S'il ne converge pas, un cluster n'y changerait rien.
- **Chaîne pour qu'un UNSAT devienne une preuve** (l'une ou l'autre route) :
  1. **Modèle.** Deux encodeurs indépendants (r8lib et five_cnf, même numérotation), accord vérifié sur tous les cubes ;
     chaque famille de clauses justifiée par L0-L2 (§1).
  2. **Symétrie.** Classes M₀ :
     - exhaustivité par énumération des orbites, avec un contrôle Σ tailles = 10 395 à ajouter ;
     - lex-leader du stabilisateur comme lemme écrit ;
     - ou bien certificats de dominance VeriPB.
  3. **Cubes.** Arbre binaire complet par construction, avec un script de complétude ou une preuve de tautologie de la
     disjonction des cubes.
  4. **Conquête.** CaDiCaL 3.0.1 en `--lrat` (ou DRAT binaire), vérifié par un vérificateur formellement prouvé
     (cake_lpr). drat-trim (patché Windows) est acceptable mais non prouvé. À ces tailles, il faut vérifier au vol,
     sans stocker les preuves.
  5. **Coupes CEGAR.**
     - Chaque coupe est stockée sous la forme (Y, q, borne), avec une vérification entière de qᵀ(8T0_Y)q et du lemme
       T ⪰ 0.
     - L'encodage PB→CNF est une extension définitionnelle (BDD) ; on peut aussi garder les coupes en PB et utiliser un
       solveur PB avec journal VeriPB.
  6. **Contrôles positifs.** Le pipeline complet (coupes comprises) doit donner SAT à k = 22 et accepter les structures
     plantées.

## 7. NON LANCÉ (à cause de l'arrêt de 16:33 ou faute de temps)

- **Encodage** :
  - effets séparés de L4B et XPAIR ;
  - five_imp sur I(1,11,a) et au-delà ;
  - kissat (le build pysat plante sur ce PC) et autres solveurs.
- **Symétrie** : aucune résolution des CNF `--m0case` ni `--lex`, donc aucune mesure du gain.
- **Relâchement** : témoins 2, 4, 5 et 6, autres ordres, m ≥ 12 avec un plafond de 280 s, ajustement avec intervalles.
- **CEGAR** : le contrôle k = 22 (`--planted`), la convergence quatre étoiles, R_k + spectral pour k ≥ 1, et R8 + coupes.
  Seule une itération a tourné.
- **Certification** : aucune preuve DRAT ou LRAT, car il n'y avait aucun UNSAT d'intérêt à certifier.

## 8. Fichiers (tous nouveaux, dans `r8_route/`)

- **Scripts** :
  - `r8lib.py` (modèle, vérificateur, encodeur indépendant, groupe) ;
  - `build_cnf.py` (CNF, implications, M₀, lex) ;
  - `runbox.py` (lanceur borné : objet job Windows, mémoire et temps, refus si suspended.json) ;
  - `test_encoding.py`, `control243.py`, `planted_suite.py`, `solve_check.py` ;
  - `knuth_match.py`, `knuth_la.py`, `knuth_rows.py`, `cube_solve.py`, `cube_anatomy.py`, `release_scan.py` ;
  - `spectral.py`, `pbenc.py`, `cegar.py`.
- **Données** (`data/`) : test_encoding.json, c243/ (contrôle, structures plantées, solutions k = 22), km_test, kla_*,
  krows_test, cube_cmp, anatomy_d100, release*, cegar/cuts_k14.jsonl, runlog.jsonl (chaque lancement avec temps et
  mémoire de pointe).
- **CNF** : régénérables par `build_cnf.py` (environ 14 Mo chacune). Elles ne sont pas copiées ; elles restent dans
  `scratchpad/boost/runs/r8route/`.
