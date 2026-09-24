# 80 — À la recherche de « l'étincelle » : arithmétique et posture « Γ n'existe pas » (2026-09-24, nuit)

*Consigne de l'utilisateur : ne pas copier C3, mais chercher une étincelle du même type ; essayer de raisonner en
supposant que C1 n'existe pas. Tout ici est mathématique (calculs de contrôle instantanés).*

## 0. Ce que change la posture « Γ n'existe pas »
Si Γ n'existe pas, il existe une preuve ; la question devient : *quelle quantité doit se contredire ?* Bilan des
outils : tout ce qui marche (L1, L7–L11, L14, L16) tue **l'ordre** (grilles, prismes, sommets peu tordus). Aucun ne
tue **le désordre** (torsion forte), or L16 prouve que la torsion forte est obligatoire. Une preuve de non-existence
doit donc contenir un mécanisme qui interdit la torsion forte. C'est la cible.

## 1. La torsion est exactement le moment cubique des droites
Avec u_L = projection unitaire de 1_L sur E₋₄ (notes/70) et L15 :
  **Σ_x |W(x)| = 1386 + 32·‖Σ_L u_L^{⊗3}‖²**,   **Σ_rot ν³ = 32‖Σ_L u_L^{⊗3}‖² − 4662**.
Torsion forte ⟺ système de droites « incohérent » (moment cubique grand, les u_L^{⊗3} presque orthogonaux, comme pour
des vecteurs aléatoires). Grid-full ⟺ forte cancellation. Au degré 3 tout est épuisé : tous les tenseurs cubiques
des configurations à ≤ 3 points se réduisent à T_P = Σ u_x^{⊗3} et C = Σ_triangles sym(u_a u_b u_c)
(relations Σ_{y~x} u_y = −4u_x ; paires D' = 10T_P − 3C, arête + point isolé = 3C − 16T_P, triples indépendants
= 19T_P/3 − C), et la seule condition de positivité est P ≤ 1151. Une borne dans l'autre sens demande le degré ≥ 4
(configurations de 7–8 points, nouvelles inconnues).

## 2. Lemme L17 (nouveau) : le 70-espace local se scinde en 2, 3, 5 ; tout y est déterminé sauf la colle en 7
x sommet, X = Γ₂(x), K = {v ∈ Z^X : sommes nulles sur chaque étiquette} (rang 70), K₃ = K ∩ ker(H − 3) (rang 40),
K₋₄ = K ∩ ker(H + 4) (rang 30).
**Énoncé.**
(a) K est **pair** (Σ v_z² ≡ Σ v_z = ½ Σ_a (somme en a) = 0 mod 2), det K = 2²¹·3⁸·5⁶.
(b) Pour p ∈ {2, 3, 5}, K ⊗ Z_p = K₃ ⊥ K₋₄ (les projecteurs (H+4)/7 et (3−H)/7 sont p-entiers).
(c) **Tout le 3- et le 5-discriminant est dans K₃, tout le 2-discriminant est dans K₋₄** : H agit sur disc(K) ≅
    disc(K^⊥) par l'opérateur d'étiquettes Φ = J − I − M (valeurs propres 12, −2, 0). En 3, Φ ≡ 0 sur disc(K^⊥)₃
    (parties constante et antisymétrique), alors que H = −4 est inversible mod 3 sur K₋₄ ; en 5, Φ ≡ −2 ≡ 3 sur
    disc(K^⊥)₅ (partie symétrique), alors que H ≡ 1 mod 5 sur K₋₄ ; en 2, Φ est nilpotent (valeurs propres paires)
    alors que H = 3 est inversible sur K₃.
(d) Donc **K₃ est pair, 2-adiquement unimodulaire, det K₃ = 3⁸·5⁶·7^k** avec des formes 3- et 5-adiques entièrement
    déterminées (constituants 3¹ de dim 8 et 5¹ de dim 6, tous deux « antisquare ») ; **K₋₄ est pair, det = 2²¹·7^k**,
    unimodulaire en 3 et 5 ; k = k(x) (L4).
(e) La formule d'oddité pour K₃ donne **k/2 ≡ k₇ (mod 2)** (k₇ = type de la forme de colle 7-adique locale) ; en
    comparant à la colle globale (L2–L3) via le réseau T_x engendré par les 77·E₃e_v, v ∈ B₁(x) (constituant 7¹ de
    dimension 14, de déterminant carré mod 7), on retrouve exactement la relation L3. **Tout est cohérent** : aucune
    contradiction au niveau du genre, quel que soit k.
*Contrôle.* Mécanisme vérifié sur BvLS (analogue : colle en 3, `code/local_split_check.py`) : en p = 5, le
5-discriminant (Z/5)¹² est entièrement dans K₋₅ (rangs de Gram mod 5 : 110 plein pour K₄, 76 = 88 − 12 pour K₋₅),
comme prédit ; en 7 et 11 tout est plein ; en 2, K₋₅ est plein comme prédit.
*Portée.* Structure arithmétique locale complète et vérifiée, mais cohérente : une contradiction ne peut pas venir du
seul genre de ces réseaux ; il faudrait une information plus fine (vecteurs précis, structure de H dans K₃/K₋₄).

## 3. Structure d'Eisenstein des droites orientées (sans symétrie)
Pour une droite orientée L = (a,b,c) : z_L = p_a + ω p_b + ω² p_c ∈ E₋₄ ⊗ C (les rotations multiplient par ω,
l'inversion conjugue). Produits hermitiens h(z_L,z_M) = 27·Σ_{a_i = b_j} ω^{i−j} − 9·Σ_{a_i ~ b_j} ω^{i−j} :
108 (même), 0 (inverse), 45ω^k (sécantes), −27ω^k ou 0 (prisme dont le couplage préserve / renverse l'orientation),
−18ω^k ou 9ω^k (e = 2 « aligné » / non), −9ω^k (e = 1), 0 (e = 0).
- Modulo √−3 cette structure redonne exactement le réseau réel des droites mod 3 (la torsion s'y annule) ; l'information
  nouvelle (phases d'orientation) commence au niveau suivant.
- La famille des deux orientations a des statistiques **indépendantes du choix des orientations**, et c'est une
  « tight frame » : Σ_L (z_L z_L* + z̄_L z̄_L*) = 1134·I₄₄.
- Graphe à gains Z/3 associé : A^ω = −A/2 − (i√3/2)D (D = orientation induite par les droites) ; tous les triangles
  sont équilibrés ; un quadrangle l'est ssi deux côtés sont parcourus dans le sens de leur droite ; tr((A^ω)⁴) =
  54054 − 12·U (U = quadrangles déséquilibrés). Si H¹(K; F₃) = 0, aucune orientation ne rend tout équilibré (sinon
  3-coloration, contredit χ ≥ 5). Les orientations « équilibrées » forment un code ternaire contenant les gradients
  des fonctions « arc-en-ciel » (constantes ou bijectives sur chaque droite), dont la dimension est liée au réseau
  des droites (dim R − 1 = dim C'^⊥ ≤ 21).
- Inégalités testées (degré 3 hermitien, deux orientations) : dominées par les droites sécantes (|h| = 45), toujours
  satisfaites. Pas de contradiction.

## 4. Autres tests (tous satisfaits, avec marge)
- Fusion frame des 99 sous-espaces V_x = vect(droites par x) : Σ_x P_x = (63/4)·I₄₄ (exact). Inégalités de degré 2
  (Grassmannienne « G₄ moyennée », bornes de Welch sur Sym² et Λ²) : toujours satisfaites, y compris à torsion
  maximale (la contribution des paires de sommets non adjacents compense).

## 5. Bilan honnête et suite
- Aucune contradiction. Les deux nouveautés solides : l'identité torsion = moment cubique (§1) et L17 (§2).
- Diagnostic : au niveau du genre, l'arithmétique locale est cohérente ; au degré ≤ 3, la positivité est épuisée.
- Pistes qui restent crédibles : (i) le degré 4 (configurations de 7–8 points + positivité), prolongement direct de ce
  qui a donné L16 ; (ii) l'anneau que crée la torsion elle-même : les géométries tordues ont un spectre de Hodge
  irrationnel (corps quadratiques Q(√33), Q(√57) sur nos exemples), donc le réseau rotationnel devient un module sur
  un ordre de corps de nombres. C'est l'analogue natif de C1 du ℤ[ω] de C3, sauf qu'il viendrait de la torsion, pas
  d'une symétrie.
