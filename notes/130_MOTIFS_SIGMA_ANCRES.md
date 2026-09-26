# 130 — Motifs Σ ≠ ∅ de C2 : la famille « ancrée » (lemme de la queue en présence de paires frères)

*26/09, nuit. C1, pièce « motifs Σ ≠ ∅ » (note 42 de C2). Mathématiques ; l'énumération finie des orientations est un
contrôle exhaustif d'un lemme démontré à la main (`c1_experimental/motifs/`).*

## 0. Énoncés
| énoncé | statut |
|---|---|
| Lemme de la queue de C2 (25.1) et T⁺ (« structures ») valent tels quels en présence de paires frères | DÉRIVÉ |
| Famille ancrée d'un motif : blocs non puits de degré sortant ≥ 3, puits deux à deux frères | DÉRIVÉ |
| **Ancrés P₅ et 2P₃ : impossibles** (règle de la queue seule ; preuve à la main pour P₅) | DÉRIVÉ + exhaustif |
| **Ancrés P₃ et P₄ : impossibles** (T⁺ avec graphes D et partitions de Out) | exhaustif, un cas refait à la main |
| Ancré P₃+K₂ : impossible (modèle couplé de « structures » étendu aux paires frères, §6) | exhaustif |
| Ancrés restants : K₃ (une classe), 3K₂ (2 orientations), 2K₂ (24), K₂ (en cours) | exhaustif ; ouvert |

## 1. Cadre
- Motif Σ = ensemble exact des paires frères, σ_k = degré de k dans Σ (≤ 2, lemme des étoiles de C2).
- **Famille ancrée** : chaque paire non frère ij a ses deux orbites appariées « un bloc » par le même bloc (son ancre).
  On oriente j → k si jk est ancrée en k. On note d_k le degré entrant, o_k le degré sortant et w_k = d_k + σ_k,
  de sorte que o_k = 6 − w_k.
- Composantes de G_k : les classes ancrées en k (composantes du graphe D sur In(k)), les partenaires frères (prismes, un
  bloc chacun), et Out(k), qui est une réunion de composantes d'au moins 2 blocs chacune. Une composante réduite à un
  bloc m non frère voudrait dire μ_k = τ_k = σ sur m, donc une paire frère.

## 2. Lemme de la queue, forme « motif »
- **d_k ≠ 1.** Une seule paire ancrée en k serait appariée à elle-même, donc frère.
- Soit X ⊂ ij appariée par le pivot i avec D(X) ⊂ ik (arcs j → i et k → i). L'équilibre de C1 (C2 note 23 §8) en k,
  sur la réunion de composantes Out(k), donne (C2 25.1) : **o_k ≥ 3 + [k → j]**.
  - Out(k) est bien une réunion de composantes : In(k) est stable (classes ancrées) et les partenaires frères sont des
    prismes.
  - Parmi les o_k voisins de x dans C_{Out(k)} figurent l'intérieur de x en i, les deux racines de D(X), et
    l'intérieur en j si k → j.
  - Si jk est frère, [k → j] = 0.
- **Conséquences.**
  - Tout bloc qui a un arc sortant est un bras, donc o ≥ 3.
  - Un puits (o = 0) a toutes ses paires non frères ancrées en lui. Deux puits sont donc frères : **les puits forment une
    clique de Σ**.
  - Un bloc de o = 3 n'est jamais la queue d'une arête D orientée.
  - Valeurs permises de w : σ = 0 → w ∈ {0, 2, 3, 6} ; σ = 1 → {1, 3, 6} ; σ = 2 → {2, 6} ; et Σ_k w_k = 21 + |Σ|.
- **T⁺** (« structures », NOTE_S28) vaut aussi : |S| ≥ 3 + [j ∈ S] + |Π|, où S est la composante de i en k et Π
  l'ensemble des p ∈ S ∖ {i, j} en lesquels {i, k} est une composante de G_p.

## 3. P₅ ancré est impossible (à la main)
Σ = {12, 23, 34, 45}, σ = (1, 2, 2, 2, 1, 0, 0) et Σw = 25.
- Sans puits, Σw ≤ 18. Avec un seul puits, Σw ≤ 22. **Les puits sont donc une paire frère.**
- **Puits {1,2}.** Le compte est exact : w₆ = w₇ = w₅ = 3 et w₃ = w₄ = 2.
  - Donc o₅ = o₆ = o₇ = 3 : aucune arête D entre 5, 6 et 7 au pivot 1, car la queue aurait o = 3.
  - Le graphe D en 1 est 2-régulier sur {3, 4, 5, 6, 7}, avec {5, 6, 7} indépendant. Il faudrait 6 demi-arêtes vers
    {3, 4}, qui n'en prennent que 4. Contradiction.
  - {4,5} est symétrique.
- **Puits {2,3}.** On a w₁ = w₅ = 3, {w₆, w₇} = {3, 2} et w₄ = 2.
  - Au pivot 3 (In = {1, 5, 6, 7}), seul le bloc q ∈ {6, 7} avec w = 2 a o ≥ 4.
  - Toute arête D doit donc avoir q pour queue. Or un 2-facteur (C₄ ou deux digones) sur 4 sommets a une arête sans q.
    Contradiction.
  - {3,4} est symétrique. ∎

## 4. Contrôle exhaustif (`c1_experimental/motifs/anchored_*.py`, `motiflib.py`)
Ordre des tests : orientations de K₇ ∖ Σ ; règle de la queue (§2) avec existence d'un graphe D (2-facteur des paires
permises) en chaque pivot ; puis T⁺ sur tous les choix de graphes D et de partitions de Out(k) ; puis un test à une racine
au niveau paires (zéros de pivot, zéros ancrés, F1, équilibre sur chaque composante), sans couplage entre racines.

| motif | règle de la queue | + T⁺ | + test à une racine |
|---|---|---|---|
| Σ = ∅ (contrôle, C2 Th. 25.3) | **0** | — | — |
| P₅ | **0** | | |
| 2P₃ | **0** | | |
| P₄ | 24 | **0** | |
| P₃ | 48 | **0** | |
| P₃+K₂ | 12 | 4 | 4 |
| K₃ | 80 | 8 | 8 |
| 3K₂ | 44 | 44 | |
| 2K₂ | 84 | 72 | |
| K₂ | 144 | 144 | |

- Les survivants de P₃+K₂ et de K₃ ont leurs puits sur une clique de Σ : {6, 7} pour P₃+K₂, le triangle {1, 3, 5} pour K₃.
- Ils demandent les contraintes couplées de « structures » (dichotomie par paire, symétrie e(P,P′)).
- Un cas de P₃ a été refait à la main : le digone {1,6} forcé en 3 met 3 dans Π pour l'arête D {5,6} au pivot 1,
  d'où 4 ≥ 5, absurde.

## 5. Portée et suite
- Ce n'est que la famille ancrée. Il reste, dans chaque motif, les paires tordues (chaînes, mélanges) et les carrés dis,
  comme pour Σ = ∅.
- Suite proposée à « structures » : le modèle par paires avec couplage sur les survivants ancrés, puis l'extension aux
  paires tordues et dis. La règle de la queue et T⁺ valent pour tout carré « un bloc », tordu compris.

## 6. Modèle couplé de « structures » étendu aux paires frères (ad/sib_model.py, écrit par C1 dans leur labo)
- Ajouts :
  - pivot 'sib' ;
  - prismes {m} aux deux bouts (8.1 par l'équilibre) ;
  - zéros aux deux blocs ;
  - (S3) ;
  - dichotomie de constante 0 pour une paire frère : (Q²)[U,U′] = 4 − Sh − n_s = 0.
- Contrôles : verdicts identiques à ceux de general_model sur 8 feuilles mortes et 3 faisables (Σ = ∅, M1 n = 6 job 12).
- **Résultats sur les survivants ancrés** (`code/motifs/run_sib_anchored.py`, tous les choix de graphe D) :
  - **P₃+K₂ : 12/12 morts.**
  - **K₃ : 8 vivants sur 80, une seule classe à symétrie près.** Les puits sont le triangle {1,3,5}, avec In = {2,4,6,7}
    partout ; sur {2,4,6,7}, une source (o = 6) et un 3-cycle.
  - 3K₂ : 2 vivants sur 44 (le bloc libre 3 est le puits).
  - 2K₂ : 24 vivants sur 84.
  - K₂ : balayage partiel, beaucoup de vivants.
- Bilan de la famille ancrée : **P₅, 2P₃, P₄, P₃ et P₃+K₂ sont morts** ; restent K₃ (une classe), 3K₂, 2K₂ et K₂.

## 7. Identités Alt entre paires frères (C1, 26/09 nuit) — une contrainte absente du modèle par paires
**Cadre.** Q = (q_UW) est la matrice des orbites (42 × 42) ; Q² + Q = 12I + 4J − B⁺ᵀB⁺ (secteur pair).
- Base de C2 (carnet §8) : s_P = (e_P₀ + e_P₁)/√2 et a_P = (e_P₀ − e_P₁)/√2. On pose
  Q_S = sᵀQs, K = sᵀQa, Q_A = aᵀQa.
- J et B⁺ᵀB⁺ n'ont pas de partie Alt. D'où, exactement :
  - Q_A² + Q_A + KᵀK = 12I ;
  - Q_S K + K Q_A + K = 0.
- Q_S et K sont entièrement « niveau paires » :
  - (Q_S)_YX = (φ_Y₀(X) + φ_Y₁(X))/2 ;
  - K_YX = (φ_X₀(Y) − φ_X₁(Y))/2.
  Seule Q_A porte des signes d'orbite.

**Paire frère P** (8.1 : toute racine disjointe de P a exactement un voisin dans P ; aucune racine qui rencontre P n'en a).
- (Q_A)_PP = −2 ; (Q_A)_PR = K_RP = 0 si R rencontre P.
- Pour R disjointe, le bloc 2 × 2 est :
  - une permutation, avec (Q_A)_PR = ±1 et K_RP = 0 ;
  - ou de type (2,0), avec K_RP = φ_P₀(R) − 1 = ±1 et (Q_A)_PR = 0.

**Identité (P, P′).** Si P = ta et P′ = tb sont frères (ils partagent t), l'entrée (P, P′) de Q_A² + Q_A + KᵀK = 12I s'écrit
  Σ_{R ⊂ [7] ∖ {t,a,b}} [(Q_A)_PR (Q_A)_P′R + K_RP K_RP′] = 0   (6 paires R).
- C'est l'étape du Théorème D de C2, sans supposer les R frères.

**Forme au niveau orbite.** Soit P₀ une orbite de la paire frère P, et A_P l'ensemble des orbites lointaines voisines de P₀ (q = 1).
- q_P₀Z + q_P₁Z = 1 pour Z disjointe de P.
- (Q² + Q)_{P₀,W} donne :
  - (E1) Σ_{Z ∈ A_P} q_ZW = 3 si W rencontre P en un bloc ;
  - (E2) Σ_{Z ∈ A_P} q_ZW = 2 + q_P₀W si W est disjointe de P.
- (E1) avec W = P′₀ redonne l'identité (P, P′) : |A_P ∩ A_P′| = 3 sur les 12 orbites de [7] ∖ {t,a,b}.
- En sommant (E1)/(E2) sur W ∈ Y :
  Σ_{Z ∈ A_P} φ_Z(Y) = 6 (Y rencontre P en un bloc), ou 4 + φ_P₀(Y) (Y disjointe).
  C'est bilinéaire : le choix de l'orbite de X qui est dans A_P quand φ_P₀(X) = 1 multiplie des φ.
- **Version impaire** : Σ_{Z ∈ A_P} T_P₀Z T_ZW = −B_{t,P₀} B_{t,W} si W rencontre P en t. Par exemple, pour K₃, parmi les 3 orbites de
  A_P ∩ A_P′, exactement une a T_P₀Z T_ZP′₀ = +1.

**Au niveau paires, l'identité (P, P′) se lit ainsi.** Pour chaque R, le type (perm/(2,0)) et le signe K sont des données de paires ; le signe
perm est libre.
- Conséquence minimale : le nombre de R où P et P′ ont le même type est pair.
- Modèle : `c1_experimental/motifs/alt_sib.py` (un one-hot à 4 états par (P, R) et un one-hot joint par (P, P′, R)), ajouté à
  sib_model.

## 8. Bloc « plein » (toute orbite par c y pivote ou est frère) : q:7 force g⁻ = 20
- τ_c = η_c, donc Q_c = −2P_π − I, avec det = (−3)⁶ ≡ 1 (un carré) et t_c = 0. Avec notes/129 §4–5 :
  - **g⁻ = 20**, ρ_c = 2 ;
  - K_c est un plan anisotrope (disc carré).
- Sont concernés : les puits de toute configuration ancrée d'un motif, et le bloc A (d = 6) des configurations AD.
- Identités locales au bloc plein (RSF de C2 avec μ = τ) :
  - n(σa, b) = n(a, b), d'où **Σ_{z ∋ a} s_z = 0 pour toute étiquette a** (s_z = 1_{Φ(z)} − 1_{Φ(−z)}) ;
  - Σ_f s_f s_fᵀ = 11I − J + P_σ (indépendant de μ).
- Test lointain diagonal : Z_ff ≡ 4(s_f·δ_f + s_f·πs_f) (mod 7), avec δ_f = 1_z − 1_{−z}.
  - Comme K_c est anisotrope, k_f = 0 ⟺ Z_ff ≡ 0.
  - Σ_f Z_ff ≡ 0 est automatique (trace d'un nilpotent).
- Deux blocs pleins c, d : sur étoile(d) ∖ étoile(c), T = 0. La matrice Z^(c) (10 × 10) y est donc de rang ≤ 2. C'est une
  condition sur les ombres de RSF(star(c)) seules, qu'on ne peut évaluer sans solution locale (aucune n'est connue à m = 7).

## 9. K₃ ancré : état
- Sur les 216 choix de graphes D aux puits :
  - **tout puits à deux digones meurt** (niveau paires ; certificat PL avec dichotomie de 45, environ 97 groupes) ;
  - il reste les 27 choix où chaque puits porte un C₄.
- **L'identité (P, P′) tue les 6 choix où les trois puits portent trois C₄ différents.** Il en reste 21. Il faut l'intégralité
  (le PL relâché est faisable) et la dichotomie. Script : `k3_alt_test.py`.
- Structure utile (à la main) : pour la racine u de 13, les équilibres aux blocs 2, 4, 6, 7 et au puits 5 donnent
  φ_u(24) = a, φ_u(27) = 2 − a, φ_u(46) = c, φ_u(47) = 2 − c, φ_u(26) = e, φ_u(67) = 2 − e, avec
  φ_u(57) = a + c + e − 2 ∈ [0, 2].
  - Les 6 paires de {2,4,6,7} vont donc par couples {24,27}, {46,47}, {26,67}, groupés par les digones aux blocs 2, 4, 6.
  - Le type est constant dans un couple, et le signe K y est opposé.
  - Même chose pour 15 et 35.
- L'identité Sym × Alt (bilinéaire) n'est pas décidée par le MILP linéarisé en 240 s. Je n'insiste pas (règle des 5 minutes).

## 10. État au 26/09, fin de nuit, et coordination
- **K₂ ancré : 144/144 orientations vivantes dans sib_model.** Le niveau paires ne mord pas du tout.
  - Profils w : 120 en (0,2,2,3,3,6,6), qui ont une étoile totalement libre.
  - 24 en (2,2,2,2,2,6,6), qui n'en ont pas : 5 blocs à digone D plus 4 étiquettes libres.
- **Profils des autres survivants.**
  - 3K₂ : les 2 survivants sont (3,3,3,3,3,3,6), sans étoile libre.
  - 2K₂ : 36 en (0,2,3,3,3,6,6) et 48 en (1,2,2,3,3,6,6). Le bloc w = 1 n'a pas de pivot mais porte une paire frère.
  - K₃ : la classe survivante est (0,2,2,2,6,6,6).
- **Transmis à C2 pour son modèle d'orbite U** (colonnes frères, lignes I complètes) : les 27 orientations K₃ + 3K₂ + 2K₂, au
  format ptype (`data/ptype_anchored_C1.json`, script `code/motifs/export_ptype.py`). Résultats attendus dans
  `logs/run_U_sibanch.out` de C2.
- **Lemme de queue et Σ ≠ ∅.** Le lemme 25.1 de C2, sous sa forme générale, vaut tel quel quand Σ ≠ ∅. L'équilibre porte sur
  toute réunion de composantes ; un partenaire frère est une composante singleton ; ik n'est jamais frère quand D(X) ⊂ ik.
  - Son filtre v6 l'avait désactivé pour les motifs, d'où l'explosion de la famille Σ tordue (K₃ : 212 classes d'orientations,
    3K₂ : 625, 2K₂ : 4 078, K₂ : 5 720).
  - « structures » a relu et confirmé ; C2 le rebranche.
- (★) de C2 (équilibre général pour tout S, avec budget d'écart), ajouté en forme linéaire à sib_model
  (`c1_experimental/motifs/star_budget.py`) : 31 000 lignes, non résolu en 60 s sur K₃. Laissé au pipeline de « structures ».

## 11. K₂ ancré, classe « tournoi régulier sur Z₅ » (K2_or12) : la paire frère est de type perm partout (à la main)
**Cadre** (indices 0 à 6).
- Blocs Z₅ = {0,…,4} ; puits 5 et 6, avec la paire frère 56.
- Arcs i → i+1 et i → i+2. Donc S1_k := {k, k+1} est ancrée en k+1 et S2_k := {k, k+2} en k+2.
- En j, digone D entre S1_{j−1} et S2_{j−2}, soit In(j) = {j−1, j−2}. Composantes de G_j : {j−1, j−2} (fermée) et
  Out(j) = {j+1, j+2, 5, 6}.
- u et ū sont les racines des orbites frères 56/0 et 56/1. Par 8.1, φ_u(R) + φ_ū(R) = 2 pour toute paire R de Z₅.

**Étape 1 (équilibres de u).**
- En j ∈ Z₅, sur {j−1, j−2} : φ_u(S1_{j−1}) + φ_u(S2_{j−2}) = 2. Sur Out(j) : φ_u(S1_j) + φ_u(S2_j) = 2 (u a ses deux
  intérieurs dans Out(j), et φ_u(j5) = φ_u(j6) = 0).
- On en tire a := φ_u(S1_k), **constant en k**, et φ_u(S2_k) = 2 − a.
- a ∈ {0, 2} veut dire que 56 est de type (2,0) sur les 10 paires ; a = 1, de type perm sur les 10.

**Étape 2 : a = 2 est impossible** (a = 0 l'est aussi, par échange de u et ū).
- A_{P₀} (les orbites lointaines voisines de u) est l'ensemble des 10 orbites S1.
- (E2) sommée sur les deux orbites d'une paire S2 = Y : Σ_{Z∈S1} φ_Z(Y) = 4 + φ_u(Y) = 4. Les deux partenaires D des orbites de
  Y sont des orbites S1 (digone à l'ancre de Y) et comptent déjà 2 + 2.
- **Aucune arête q = 1 ne relie donc S1 et S2.**
- Soit W une orbite de S1_k (pivot k+1, D(W) ⊂ S2_{k−1}). Équilibre en k+4 sur {k+2, k+3} : φ_W(S2_{k+2}) + φ_W(S1_{k+3}) = 2.
  Le premier terme est nul (S2_{k+2} ≠ S2_{k−1}), donc φ_W(S1_{k+3}) = 2, et ce pour **les deux** orbites de S1_k.
- Dichotomie de S1_{k+3} (paire ancrée, n_s = 0, partenaires D dans S2_{k+2}) : il y a au moins 3 orbites non partenaires à
  φ = 2 (les deux orbites de S1_k et u), alors que la dichotomie en autorise au plus 2. **Contradiction.** ∎

**Conséquence.** Dans K2_or12, u touche exactement une orbite de chaque paire de Z₅.
- Pour W ∈ S1_k : φ_W(S1_{k+2}) = 1 et φ_W(S2_{k+2}) + φ_W(S1_{k+3}) = 2. Ses voisins dans les orbites Z₅ totalisent 5 (partenaire
  compris), ce qui est cohérent avec (E2).
- Pour W′ ∈ S2_k : φ(S1_k) + φ(S2_{k+4}) = 1, φ(S2_{k+1}) = φ(S1_{k+3}) = 1, et φ(S1_{k+1}) = 2 (partenaire).
- Le cas a = 1 reste ouvert à la main. C'est le travail du modèle U de C2.
- Ingrédients : équilibre (notes/23 §8 de C2), dichotomie, (E2) sommée, c'est-à-dire l'identité Sym × Alt de §7 (absente de
  sib_model).

### 11 bis. K2_or12 : squelette unique et identités de paires (suite)
- **Graphes D.** Sur les 289 choix de graphes D aux puits qui passent T⁺, un seul est faisable dans sib_model : le 5-cycle
  consécutif 0-1-2-3-4 aux deux puits. Le squelette est alors **entièrement invariant par Z₅**.
  - Le point faisable trouvé par le MILP a bien a = 1 (cohérent avec §11).
  - Les autres classes ancrées sont presque aussi rigides : 3K2_or14 a 1 choix D, 2K2_or15 1 (sur 4), K2_or0 2 (sur 8), K3_or0 21.
  - Les 26 squelettes à D fixé sont dans `data/fixedD_anchored_C1.json`, transmis à C2 pour U.
- **Orbites puits** F_m = {5, m} : pivot 5, avec F_m⁺ ↔ F_{m+1}⁻.
  - Équilibres en Z₅ et au puits 6, puis symétries e(S1_k, F_j) et e(S2_k, F_j), avec a = 1.
  - Les **deux** orbites de F_m vérifient φ(S1_m) = 1, φ(S1_{m+1}) = 0, φ(S2_m) = 1, φ(S2_{m−1}) = 0 ; de même au puits 6.
  - Il reste, pour F_m⁺ : C = φ(S1_{m+2}) ∈ {1, 2} et D = φ(S1_{m+3}) ≥ C − 1. Pour F_m⁻ : C ∈ {0, 1} et D ≥ C − 1.
  - Contrainte commune : C⁺ + C⁻ + D⁺ + D⁻ = 4.
  - Toutes les autres valeurs de φ s'en déduisent : φ(S2_{m+1}) = 2 − C, φ(S2_{m+2}) = 2 − D, et les φ(G_j) par les équilibres.
- **Dichotomies.**
  - Pour S1_j : #{W ∈ S1_{j−3} : x_W = 0} + #{Z ∈ F_{j−2} : C_Z = 2} + #{Z ∈ F_{j−3} : D_Z = 2} + (termes du puits 6) = 2.
  - Pour S2_j : #{W ∈ S1_{j−2} : x_W = 2} + #{Z ∈ F_{j−1} : C_Z = 0} + #{Z ∈ F_{j−2} : D_Z = 0} + (puits 6) = 2.
  - Ici x_W = φ_W(S2_{k+2}) pour W ∈ S1_k, avec Σ_{W∈S1_k} x_W = 2.
- **État.** Il reste de la liberté au niveau paires, ce qui est cohérent avec sib_model. La suite est au niveau orbite (U de C2), puis
  au secteur impair (modèle signé), puisque U n'a pas de signes.

## 12. Résultats du modèle d'orbite U de C2 sur les squelettes à D fixé (26/09, nuit)
Modèle U : secteur pair seul, colonnes frères, D fixé. Certificats revérifiés par orbit_verify_U, étendu aux frères et au filtre 8.1.
- **2K2_or15 (a0) : MORT.** Écart de Farkas 103,7. C'était l'unique classe et l'unique choix D : **toute la famille ancrée de 2K₂
  est morte.**
- **K2_or12 (a0), tournoi régulier sur Z₅ : MORT.** Écart 157,2.
- **3K2_or14 (a0) : FAISABLE** dans U (112 512 colonnes, solution PL sauvée). C'est la cible pour le secteur impair et q:7.
  Structure :
  - un seul puits, le bloc 2, plein, de profil (4,4,4) : ses digones D apparient {0,4}, {1,3}, {5,6}, exactement comme les paires
    frères ;
  - chaque autre bloc a son frère, un digone venu d'une autre paire frère (cycle A → B → C → A) et 3 blocs libres.
- En cours chez C2 : K2_or0 (a0, a1) et la DFS des puits de K₃ (au bloc 0, la double digone {16, 35} et le C₄ 1-5-3-6 sont morts).
- Les deux classes tuées ont deux puits pleins frères. La mort vient déjà du secteur pair, sans les signes. Le certificat (dual
  d'IPM, dense) ne se concentre pas sur le bloc croisé de notes/131 §6. C2 extraira un certificat à support minimal pour K2_or12,
  en vue d'une preuve à la main.
