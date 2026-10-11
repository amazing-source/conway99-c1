# 168 — Sous-cas (A) de C1 : approche mathématique (11/10)

*Le sous-cas (A) (note 166) : Γ = srg(99,14,1,2) partitionné en 11 grilles 3×3 G₀, …, G₁₀, deux grilles quelconques
étant reliées par un couplage parfait σ_ij. Les énoncés « démontré » ont une preuve complète ci-dessous. Les
identités de blocs ont été vérifiées numériquement, à 10⁻¹⁵ près, sur les représentations en grilles des
srg(243,22,1,2) connus, où la même algèbre s'applique avec r = 4.*

## 1. Cadre : A = D + M
Notations :
- D est la partie « dans les grilles » : diagonale par blocs, chaque bloc étant la grille K3×K3, de valeurs propres
  4, 1⁴, (−2)⁴.
- M est la partie « entre grilles » : une somme de matrices de permutation P_ij (i ≠ j). C'est la matrice
  d'adjacence du **graphe transverse** Tr, 10-régulier, dont chaque arête est dans exactement un triangle (une
  droite transverse).
- Dans chaque grille, l'espace des fonctions de somme nulle se décompose en Z_i = R_i ⊕ S_i, avec R_i les
  « fonctions de droites » (lignes ou colonnes, valeur propre 1, dimension 4) et S_i les fonctions mixtes (valeur
  propre −2, dimension 4). On pose Z = ⊕Z_i (dimension 88), R = ⊕R_i et S = ⊕S_i (dimension 44 chacun).

La partition en grilles est équitable de quotient 3I + J. Donc Z est A-invariant, et A|_Z a pour valeurs propres
3 et −4, chacune de multiplicité 44.

## 2. Les identités de blocs (démontré)
On pose K = +1 sur R et −1 sur S. Alors D + ½ = (3/2)K sur Z, et (A + ½)² = 49/4 sur Z, d'où

  **M² + (3/2)(KM + MK) = 10 sur Z.**

En blocs (R, S), avec a = M_RR, b = M_SS et X = M_RS :
- (M²)_RS = 0 : **M² préserve R et S** ;
- a² + XXᵀ = 10 − 3a ;
- b² + XᵀX = 10 + 3b ;
- aX + Xb = 0.

*Forme générale pour srg(v,k,1,2) avec une partition équitable en grilles reliées par des couplages :* remplacer 10
par (r + 2)(r − 1). Vérifié sur BvLS, Γ₃ et Γ₄ (r = 4).

## 3. Conséquences spectrales (démontré)
1. **Les valeurs propres de a** valent 2, −5, ou sont « appariées » λ ∈ (−5, 2). Celles de b valent 5, −2, ou −λ. X
   entrelace a et −b.
2. **Le spectre de M sur Z est symétrique et contenu dans ±[2, 5].**
   - Dans un plan apparié, M a pour valeurs propres ±√(10 − 3λ).
   - Les traces tr M = 0 et tr M² = 990 imposent que les multiplicités de 2 et −2 soient égales, ainsi que celles de 5
     et −5.

   Le spectre complet de Tr est donc {10, (−1)¹⁰} ∪ (88 valeurs ±μ avec 2 ≤ |μ| ≤ 5).
3. **Traces impaires.** tr M^(2s+1) = 10^(2s+1) − 10 pour tout s.
   - Pour s = 1 : 990 = 6 × 165 triangles. ✓
   - Pour s = 2 : le graphe transverse a exactement **c₅ = 5544** pentagones. Ce sont des pentagones de cellules
     distinctes (deux sommets à distance 2 sont dans des cellules différentes).
   - Interprétation : la somme des points fixes des holonomies de pentagone, sur les 11·10·9·8·7 = 55 440
     pentagones ordonnés de cellules, vaut 10·c₅ = 55 440. **L'holonomie de pentagone a en moyenne exactement
     1 point fixe**, comme une permutation aléatoire uniforme.
4. **Identité locale de Parseval** (vraie pour toute bijection entre deux grilles) :
   4e + 18t = 72, où e est le nombre d'arêtes communes entre la grille et la grille transportée et t = ‖Π_R P Π_S‖²
   la « fuite » des fonctions de droites vers les fonctions mixtes. Les traces d'ordre ≤ 4 ne contiennent donc que de
   l'information locale.

## 4. Théorème : alignement total impossible à 99, possible seulement à 9 et 243 (démontré)
**Théorème.** Soit Γ un srg(v,k,1,2) muni d'une partition équitable en grilles 3×3 reliées par des couplages, où
chaque σ_ij est un isomorphisme de grilles (« aligné »). Alors (2r + 1) divise (r − 1)·dim R.

*Preuve.*
1. Alignement ⇔ P_ij(R_j) = R_i pour tout i, j ⇔ X = 0.
2. Alors a² + 3a − (r+2)(r−1) = 0, donc les valeurs propres de a sont r − 1 et −(r + 2).
3. Comme tr a = 0 (M n'a pas de bloc diagonal), (r − 1)m = (r + 2)m′ avec m + m′ = dim R, d'où
   m′ = (r − 1)·dim R/(2r + 1). ∎

| v | r | 2r + 1 | dim R = 4v/9 | (r−1)·dim R/(2r+1) | alignement total |
|---|---|---|---|---|---|
| 243 | 4 | 9 | 108 | 36 | **possible** (BvLS) |
| **99** | 3 | 7 | 44 | **88/7** | **impossible** |
| 6273 | 10 | 21 | 2788 | 25092/21 | impossible |
| 494019 | 31 | 63 | 219564 | non entier | impossible |

C'est le même partage 9 / 243 contre 99 / 6273 / 494019 que pour les étalements réguliers (note 165, lemme 1), avec
cette fois une preuve **sans hypothèse de règles cohérentes**. Ce théorème remplace et renforce le point 3 du §3 de
la note 167.

**Corollaire (sous-cas A).** Au moins un recollement est vrillé. Plus précisément, le nombre p de plans appariés
vérifie p ≥ 1, et p ≤ rang(X) ≤ 4·#(paires vrillées).

## 5. Bilan et suite
- **Établi.** Le sous-cas (A) se ramène exactement à 55 permutations de 9 points soumises aux 110 lois de recollement
  Σ_k H_ikj = 2J − I − D_i − D_j^(i) (note 167 §2). Toute l'information spectrale « gratuite » est épuisée : elle
  donne la symétrie du spectre de Tr, la moyenne 1 des holonomies de pentagone, et le vrillage obligatoire.
- **Ce qui manque pour conclure.** Une contrainte **globale non spectrale**. Deux pistes concrètes :
  1. *Piste 7-adique.* rang₇(A − 3I) = 1 + rang₇(N|_Z) avec N ≡ 5K + M (mod 7), N² ≡ 0. Calculer k₇ à partir des
     données de recollement et le confronter aux exclusions déjà démontrées (k₇ pair, 10 ≤ k₇ ≤ 28, k₇ ≠ 6, 8 ;
     article rank7).
  2. *Piste des holonomies d'ordre supérieur.* Les traces tr M⁶ et tr M⁸ donnent les statistiques des hexagones et
     octogones de cellules en fonction des λ_i. Les nombres c_i = 10 − 3λ_i sont des entiers algébriques totalement
     réels dans (4, 25) : contraintes d'intégralité.
- **En parallèle.** Le calcul SAT exact du sous-cas (A) tourne (`conway_grids.py`, normalisation corrigée et
  validée).
