# 145 — Test décisif sur un réseau non rigide : 124 (d₈a₇², voisins D₈³ et A₁₅D₉)

*27/09 nuit. C1. En cours. Question : les lemmes locaux et la contrainte des DEUX voisins tuent-ils un réseau non rigide ?
(notes/144)*

## Données
- r = 224 et Γ = 4 (data/finishC/gamma/gamma_124.json). Aucune paire y n'est calculée.
- Nouvelles racines :
  - 112 signées dans D₈³ : deux blocs D₈ ⊃ A₇, de 28 racines chacun à signe près ; le d₈ de U remplit le 3ᵉ D₈ ;
  - 160 dans A₁₅D₉ : A₁₅ ⊃ A₇+A₇ (64 racines, e_i − e_j avec i ∈ I, j ∈ J) et D₉ ⊃ D₈ (16 racines, ±e_i ± e₉).
- m(x) = 28 − E(x), le même dans les deux voisins. **128/2048 vecteurs de norme 3 ne touchent rien** : c'est le plus contraint
  des 131 réseaux non rigides.
- **Budget de packing** (voisin D₈³, le plus serré) : Σ_u m(u) + hits_y(D₈³) ≤ 56.

## Bloc D₈ ⊃ A₇ (nouvelles racines ±(e_i + e_j) dans le voisin D₈³)
**Vecteurs pairs h.** (h, e_i − e_j) ∈ ℤ, (h, e_i + e_j) ∈ ℤ et |h_i + h_j| ≤ 1. Donc h|_B est l'un des vecteurs suivants :
0, ±e_i, e_i − e_j, (±½)⁸, ±(3/2, (−½)⁷).

**Vecteurs impairs.** Toutes les coordonnées sont ≡ ¼ (mod 1), ou toutes ≡ −¼, avec |v_i + v_j| ≤ 3/2.
- La nouvelle racine e_i + e_j est touchée ⟺ v_i + v_j = ±3/2.

**Identité de bloc** (somme sur les 28 nouvelles racines, w = 3 − 2n) :
- Σ_h [6|h_B|² + (Σ_i h_i)²] = 84 − 2H_B, où H_B = nombre de nouvelles racines du bloc touchées (par u ou y).
- Contributions par forme de h :

| forme de h\|_B | contribution |
|---|---|
| 0 | 0 |
| ±e_i | 7 |
| e_i − e_j | 12 |
| (±½)⁸ avec k signes moins | 12 + (4−k)² |
| ±(3/2, (−½)⁷) | 28 (toute la norme de h est alors dans le bloc) |

## Plan
1. Même inventaire pour A₁₅ ⊃ A₇+A₇ et D₉ ⊃ D₈ (voisin A₁₅D₉).
2. Le plan 2D V ⊥ racines(U) est vu par les DEUX voisins, via des directions différentes : (1_{B₂}, 1_{B₃}) dans D₈³, et
   (u_A, e₉) dans A₁₅D₉. Écrire la projection de (F) sur V, soit Σ_v P_V v P_V vᵀ = 7I₂, dans les deux cadres.
3. Recoller : chaque h a UNE forme par bloc dans chaque voisin, et sa norme totale vaut 4. Il faut en même temps :
   - l'identité de bloc dans les deux voisins ;
   - le packing ;
   - Z⁺.
   Chercher la contradiction sans énumérer les y. Seule l'information des types de y par bloc devrait servir.

## Résultat du test (27/09, ~17:50, calcul autorisé par l'utilisateur, capé)
- **Paires y de 124** (y_pairs_gamma.py, 259 s, 39 Mo) : 96 y₁ dominants, 25 orbites sous Γ, 1400 candidats y₂, **1286 paires**
  (liste complète, rien de tronqué) → data/finishC/ypairs/gpairs_124.json.
- **Étage h en mode général** (w = 1 sur les hits y ; w ∈ {1,3} sur les racines touchables par un vecteur de norme 3 ⊥ y ;
  w = 3 ailleurs), sondé sur les paires 0 à 3 avec 60 s par paire. Paire 2 : morte en 10,9 s. Paires 0, 1 et 3 : **TIMEOUT à 60 s**.
- À comparer aux rigides : 87 meurt en ~0,3 s par paire, 132 entre 0,5 et 49 s.
- **Premier signal : en non rigide, la liberté des racines « touchables » rend l'étage h LOURD.** Mesure en cours : une paire
  à 900 s, et 36 paires à 60 s.

## Lemme U (élagage prouvé pour le non rigide, à brancher dans la recherche)
**Énoncé.** Soit β une nouvelle racine, de l'un ou l'autre voisin, telle que w(β) = Σ_c (h_c,β)² = 1, et que β ne soit touchée ni
par y₁ ni par y₂. Il existe alors x ∈ U de norme 3 tel que :
- x ⊥ y₁, y₂ et |(x,β)| = 3/2 ;
- (x, h_c) ∈ {0, ±1} pour tout c, avec EXACTEMENT deux valeurs non nulles (motif D₇).

**Preuve.**
1. D'après le lemme de packing, w = 1 ⟺ β est touchée par exactement un vecteur impair du repère.
2. Ce vecteur n'est pas un y, donc c'est un u.
3. Or (u, h_c) = −C_{cu}, dont la colonne est une racine ±e_c ± e_d de D₇.

**Version partielle** (pendant la recherche) : sur les h déjà choisis, x doit avoir |(x,h)| ≤ 1 et au plus deux valeurs non nulles.

**Comptage.** Le nombre de racines w = 1 qui ne sont pas des hits y vaut Σ_u m(u), où les u sont 42 vecteurs distincts
qui ont le motif D₇.

L'étage h actuel n'utilise PAS ce lemme : il ne demande qu'un x ⊥ y quelconque. C'est le candidat naturel pour rendre
la recherche non rigide petite.

## Lemme U+ (forme forte) et résultat (27/09, ~18:00-18:10)
**Lemme U+.**
- Un u ne touche QUE des nouvelles racines qui finissent à w = 1 et qui ne sont pas des hits y. La raison est le packing :
  une racine touchée l'est par exactement un vecteur impair.
- **Un candidat x est donc valide à un nœud** si :
  1. |(x,h)| ≤ 1 pour les h choisis, avec au plus deux valeurs non nulles ;
  2. x ne touche aucun hit y ;
  3. x ne touche AUCUNE racine dont la couverture courante vaut w ≥ 2.
- Les cellules ne se vérifient que sur les candidats valides.
- Un point flexible à w = 1 sans candidat valide doit monter à 3.
- Toutes ces conditions sont monotones le long de la recherche.

**Mesures sur 124.**

| paires | outil | mode | budget | mortes | timeouts | h trouvés |
|---|---|---|---|---|---|---|
| 40 | Python (pair_h_check) | général nu | 60 s | 11 | 29 | 0 |
| 25 | Python (pair_h_check) | U+ | 120 s | 19 | 6 | 0 |
| 40 | numba (frame_dfs de C2) | U+ | — | **40** | 0 | 0 |

- Les deux lectures sont cohérentes : aucune contradiction. Le surcoût de mon Python par nœud dépasse souvent le gain, mais
  l'élagage est réel : la paire 7 passe de plus de 60 s à 0,4 s.
- **frame_dfs avec U+ :** médiane 1,6 s, max 5,7 s, profondeur de mort ≤ 4. La paire 0 passe de 152 s à 1,9 s.
- **Contrôle d'identité (C2) :** sur le rigide 87 en mode général forcé, les comptes de nœuds sont identiques avec et sans U+.
  Pas de régression.
- **Pas de contrôle positif naturel.** Aucun vrai repère n'existe. D'où la double implémentation, le contrôle d'identité et la
  vérification directe des conditions du lemme.
- **Conséquence (à confirmer sur 102, 111, 126, trois autres familles, en cours).** Si le mécanisme se généralise, la ligne (C)
  devient calculable sur toute la masse non rigide. Le coût serait dominé par l'énumération des paires y (259 s pour 124).
