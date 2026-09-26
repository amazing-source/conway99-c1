# 119 — Au Fano tendu : la condition Ψ par paire (lemme P-Ψ) et les systèmes F₂ par droite

*26/09, fin de matinée. Retour aux mathématiques pures (demande de l'utilisateur). DÉRIVÉ = preuve écrite ; les
seuls calculs sont des contrôles exacts d'énoncés dérivés à la main (identités vérifiées paire par paire, énumération
des 64 réglages de retournements d'une droite). La proposition « Ψ_R annule les comptes permis » est démontrée à la main
par « structures » (NOTE_S21_PSI_STRUCTUREL, labo conway99-structures-lab).*

## 0. Résumé
| résultat | statut |
|---|---|
| **Lemme P-Ψ** : au Fano tendu, pour toute paire y, θ(z_X(y)) + θ(z_Y(y)) = 0 (84 conditions) | DÉRIVÉ ; **relu et refait à la main par « structures »** (S21 §4) ; identité contrôlée sur 4 configurations, 84 paires sur 84 |
| P-Ψ est strictement plus fort que les 21 conditions I_R = 0 de notes/118 | les 480 retournements « I_R = 0 » du témoin violent P-Ψ sur 14 à 42 paires |
| le second vecteur du noyau effectif ne donne rien de plus (identité 0 = 0) | DÉRIVÉ à la main, noyau décomposé sous Stab(R) ≅ D₄ |
| P-Ψ se lit, droite par droite, comme un système affine sur F₂ en les 6 bits de retournement | DÉRIVÉ |
| pour σ du témoin et pour 8 σ tendus frais, 2 à 6 droites sur 7 n'ont **aucun** réglage | contrôle exact (64 réglages par droite) |
| cas « tout mélangé » d'une droite : résolu à la main (ν_A + ν_B + ν_C = 1) | DÉRIVÉ |
| « aucun sommet de Fano tendu » (le lemme visé) | **ouvert** : il reste à montrer qu'une droite échoue toujours |

## 1. Rappels
- Fano tendu en x : le graphe de classes de chaque τ_u est formé des 3 droites d'un plan de Fano Π par la classe de u.
  Le lemme du triangle force l'état tendu : aucune arête σ n'est interne à une droite. Les comptes sont alors exacts
  (notes/115-116 ; forme close au lemme 1 de S21).
- Pour un bloc R = {X,Y}, on note W = Φ(X,Y) et C4 = [7] ∖ {X,Y,W}. M_W désigne les deux paires de C4 alignées
  avec W, c'est-à-dire les traces de C4 sur les deux autres droites par W. Le signe s_R vaut ±1 sur ces deux paires.
- La fonctionnelle Ψ_R = Σ_{c∈C4} s(c)[9e_Wc + e_Xc + e_Yc] + 4(e_{M_W⁺} − e_{M_W⁻}) vérifie :
  **⟨c(z), Ψ_R⟩ = 0 pour tout z dont les classes évitent R et tel que c_R(z) > 0.**
  C'est la preuve à la main de S21 ; le contrôle exhaustif est celui de notes/118.

## 2. Lemme P-Ψ
**Énoncé.** À un sommet de Fano tendu, soit y ∈ R = {X,Y}. Soient z_X(y) et z_Y(y) ses partenaires τ par son
étiquette de X et par celle de Y ; ils sont dans les blocs XW et YW. Alors
  **θ(z_X(y)) + θ(z_Y(y)) = 0**, où θ(z) = s_R(classe d'atterrissage de z via W).
Autrement dit, les partenaires σ_W de z_X(y) et de z_Y(y) tombent sur les deux droites différentes par W.

**Preuve.**
1. L'identité pairblk (notes/118) donne Σ_{z~y} c(z) = r(y), avec
   r(y)_R′ = 12[y∈R′] + Σ_{w∈R′, w≠y} (2 − |y∩w|) − c_R′(y).
   En retirant les quatre spéciaux : Σ_{z ∈ N_gén(y)} c(z) = t(y) := r(y) − Σ_{z∈spec(y)} c(z).
2. Un voisin générique z de y a ses classes disjointes de R, et c_R(z) ≥ 1 puisque y ∈ R. Donc ⟨c(z),Ψ_R⟩ = 0, et
   par suite **⟨t(y), Ψ_R⟩ = 0**.
3. Ψ_R(R) = 0, et Σ_{w∈R′}(2 − |y∩w|) = 8 − 2|R∩R′|. D'où Σ_R′ Ψ_R(R′)(8 − 2|R∩R′|) = 84·Σ_c s(c) + 4·8 − 4·8 = 0.
   Les comptes de y lui-même vérifient ⟨c(y), Ψ_R⟩ = 0 pour tout atterrissage (S21, position de R). Donc ⟨r(y), Ψ_R⟩ = 0.
4. Les spéciaux de y :
   - les partenaires τ z_X, z_Y donnent ⟨c(z), Ψ_R⟩ = 6θ(z) (S21, blocs XW et YW) ;
   - les partenaires σ (blocs {X, a_y} et {Y, b_y}, atterrissage via X égal à Y) donnent −18 s(a_y) − 18 s(b_y) = 0,
     car {a_y, b_y} ∈ M_X ∪ M_Y est coupé par M_W.
5. Donc 0 = ⟨t(y), Ψ_R⟩ = −6(θ(z_X) + θ(z_Y)). ∎

*Relecture indépendante par « structures »* (S21 §4) : chaque étape a été refaite avec la forme close des comptes, dans
le repère de chaque spécial.
- Partenaire τ : s(a) + 5s(b) ou s(a) + 7s(b), selon la branche F5 ; c'est 6θ dans les deux cas.
- Partenaire σ : −18·s(A) dans les deux branches.

*Contrôle exact* : ⟨t(y), Ψ⟩ = −6(θ + θ), calculé directement depuis la définition de t(y), tient pour 84 paires sur 84
au témoin et sur 3 configurations tendues fraîches.

**Le noyau effectif ne donne rien de plus.**
- Sous Stab(R) ≅ D₄, le noyau effectif (de dimension 5) se décompose en trois parties :
  - une composante triviale de dimension 3 (2 dimensions universelles et 1 de plus) ;
  - deux caractères signes de dimension 1 : l'un est φ_Y − φ_X, l'autre est Ψ_R.
- Le vecteur trivial supplémentaire donne, dans le même calcul, −24 = −24 : aucune condition. **Seul Ψ mord.**

## 3. Forme par droite : un système affine sur F₂
- **Notations.** On pose w_Z(u, v) = φ_Z(classe d'atterrissage de la paire {Z_u, v} via Z), où φ_Z distingue les deux
  autres droites par Z. Le retournement f_x est défini par τ_x(y_b) = z_{b⊕f_x}.
- **P-Ψ en la paire {x, y}** (bloc XY, troisième point Z) :
  **w_Z(bit τ_x(y), x) ⊕ w_Z(bit τ_y(x), y) = 1**, c'est-à-dire w_Z(bit(y) ⊕ f_x, x) ⊕ w_Z(bit(x) ⊕ f_y, y) = 1.
- **Types.** Chaque étiquette v de la droite a, vis-à-vis de chacune des deux autres classes Z de la droite, un type
  lu sur la permutation colorée σ_Z (couleur = droite par Z) :
  - C0 : σ_Z⁻¹(v) et σ_Z(v) sont tous deux sur la droite « suivante » ;
  - C1 : tous deux sur la « précédente » ;
  - M0 ou M1 : ils sont sur des droites différentes (types « mélangés »).
- **Fait (DÉRIVÉ).** Pour chaque (Z, L), #C0 = #C1 = m_{Z,L}. La matrice de transport de σ_Z entre les trois droites
  par Z est circulante, de paramètre p_Z. En coupant par (pas entrant, pas sortant) : (+,+) = p − m, (−,−) = 4 − p − m,
  (+,−) = (−,+) = m.
- **Système.** Pour f_v inconnu et g = f ⊕ [M1] :
  - paire mélangée–mélangée : f_x ⊕ f_y = 1 ⊕ bit(x) ⊕ bit(y) ⊕ μ_x ⊕ μ_y ;
  - mélangée–constante : f_x fixé ;
  - constante–constante : c_x ≠ c_y.
  Les parités « somme des 4 équations d'un bloc » sont automatiques.
- **Cas « tout mélangé » (m = 0 pour les 3 blocs).** Les 12 équations forment l'octaèdre K₂,₂,₂. Le système est
  résoluble si et seulement si ν est constant sur chaque classe et **ν_A + ν_B + ν_C = 1**, où ν_v = μ^{Z₁}_v + μ^{Z₂}_v.
- **Cas m = 1 dans un bloc.** Chaque étiquette mélangée y reçoit une valeur de g fixée. La droite est résoluble si et
  seulement si chaque étiquette mélangée dans ses deux blocs reçoit deux valeurs compatibles.

## 4. Portée observée (contrôle exact, pas un théorème)
- Témoin : 4 droites sur 7 sans aucun réglage. Pour 8 σ tendus frais (solutions de KBLDP) : 2 à 6 droites mortes
  chacun.
- **Ces 9 σ sont donc impossibles pour tout τ de type Fano**, sans même utiliser l'admissibilité ni les niveaux cellule
  ou paire × bloc.
- Les motifs (m par bloc) ne suffisent pas à décider : une droite avec m = 1 partout peut être morte ou vivante. La
  mort vient des raccords entre blocs, via les étiquettes mélangées dans leurs deux blocs.

## 5. Suite
- Le lemme « aucun sommet de Fano tendu » revient à ceci : pour tout σ tendu (F5, KBLDP), au moins une droite a un
  système F₂ incompatible. Il faut un argument global.
- Les données de chaque droite ne dépendent que des permutations colorées σ_A, σ_B, σ_C restreintes aux étiquettes de
  la droite. Chaque σ_Z couple ses trois droites, et KBLDP porte sur les classes d'atterrissage, plus fines que les
  couleurs.
- Piste : trouver la combinaison sans retournement (noyau à gauche du système) qui est toujours violée. Le cas « tout
  mélangé » donne ν_A + ν_B + ν_C = 1 ; sa somme sur les 7 droites vaut 1 (7 est impair), à confronter à la structure
  de σ.
