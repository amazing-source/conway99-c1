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
