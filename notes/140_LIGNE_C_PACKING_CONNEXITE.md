# 140 — Ligne (C) : voisins de Niemeier, critère de packing, lemme de connexité, O₂₄ réduit à 141 classes

*27/09, soir. C1. Suite de notes/139. Tout ce qui suit est DÉMONTRÉ. La mention « vérifié » signifie en plus un calcul exact sur
les 156 enveloppes explicites de « structures » (involution/envelopes/U, 03b7321). Les outils sont code/envelope_pack.py,
code/packing_criterion.py et code/o24_ypairs.py.*

## 1. Les deux voisins pairs et les nouvelles racines
- Soit U impair unimodulaire de dim 24, de min ≥ 2, et U₀ sa partie paire. Alors U₀*/U₀ = {U₀, U∖U₀, S₁, S₂}, et les voisins
  pairs sont nb_j = U₀ ∪ S_j.
- nb_j est un réseau de Niemeier de nombre de Coxeter h_j, avec 24h_j racines de rang plein. Pour tout x, on a
  Σ_{ρ∈R(nb_j)} (ρ,x)² = 2h_j|x|².
- Les racines de U sont les racines de nb_j qui sont dans U₀. Les NOUVELLES racines sont les vecteurs de norme 2 de S_j :
  24h_j − r par voisin, r + 48 en tout. Ce sont aussi les χ₈/2.
- Accouplements : (S_j, U∖U₀) ⊂ ½ + ℤ et (S_j, U₀) ⊂ ℤ.

**Identité de réseau.** Pour tout x ∈ U de norme 3 :
- m(x) := #{β ∈ S_j, |β|² = 2 : |(β,x)| = 3/2} = r/8 − E(x) ;
- E(x) = Σ_{α>0} (α,x)² = Σ_i h_i|P_i x|² ;
- m(x) est le même pour j = 1 et j = 2. Vérifié sur les enveloppes explicites.

Conséquences :
- **n_x ≤ r/4 pour tout x de norme 3 : c'est un fait de réseau, pas une contrainte de repère.** Le filtre « admissible » de
  envelope_trap.py est donc vide sur un U explicite.
- Les exclusions 117, 134 et 142 (notes/139 §3 bis) restent valides, **sans les théorèmes thêta de Sol**. Leur forme exacte :
  U n'a aucun vecteur de norme 3 à projection spinorielle sur le gros D_n (fait de réseau, via l'identité par composante), puis
  le piège.
- De même pour y (norme 7) : m_j(y) = 4h_j + r/8 − E(y).

## 2. Critère de PACKING (contrainte de repère)
**(F) en une nouvelle racine β.**
- Les 42 u et les 2 y ont (·,β) ∈ ½ + ℤ ; les h ont (h,β) ∈ ℤ.
- Donc 42/4 + 2/4 + Σ_h(h,β)² + 2·#{vecteurs impairs du repère avec |(·,β)| = 3/2} = 14.
- Il en découle trois choses :
  - (i) **au plus UN** des 44 vecteurs impairs du repère vérifie |(·,β)| = 3/2 ;
  - (ii) |(h,β)| ≤ 1 pour tout h ;
  - (iii) Σ_h(h,β)² ∈ {1, 3}, et vaut 1 exactement quand β est touché à 3/2.
- **Conséquence :** les ensembles « 3/2 » des 42 u sont deux à deux disjoints (ceux des y aussi), d'où
  **Σ_u (r/8 − E(u)) ≤ 24·min(h₁,h₂) − r.**

**Exclusion par les seules données de racines : id 154 (a₂₃)**, relue et vérifiée par « structures ».
- Tout x de norme 3 a une projection ω_k avec k ≤ 3, donc E(x) ≤ 63 et m(x) ≥ 69 − 63 = 6.
- Il faudrait 42·6 = 252 nouvelles racines, et A₂₄ n'en a que 600 − 552 = 48.
- Vérifié sur l'enveloppe explicite : la somme des 42 plus petits m vaut 252.

Sur U explicite, envelope_pack.py fait trois tests :
- le test des 42 plus petits m ;
- le piège restreint aux vecteurs compatibles avec le budget ;
- le lemme de connexité (§3).

## 3. Lemme de CONNEXITÉ
**Énoncé.** Les 42 u sont connexes pour la relation |(u,u')| = 1. Il n'existe pas de partition A ⊔ B, avec A et B non vides et
(A,B) = 0.

**Preuve.**
- On note G = 3I − T la Gram des u, et C_co = −(u_o,h_c). Le bloc (u,u) de Γ² = 7Γ donne T² + T = 12I − CᵀC.
- Si T_AB = 0, alors (CᵀC)_AB = 0.
- C_co ≠ 0 ⟺ c ∈ paire(o), et chacune des 21 paires de K₇ porte exactement 2 orbites. Deux paires e ∈ P_A et f ∈ P_B sont
  donc disjointes ou égales.
- Il existe e ≠ f, donc disjointes. On prend g = {x,y} avec x ∈ e et y ∈ f. Une orbite de g est dans A (conflit avec f) ou
  dans B (conflit avec e). Contradiction. ∎

**Conséquence de réseau.** N est contenu dans le span d'UNE composante du graphe « |(x,x')| = 1 » sur les vecteurs de norme 3
admissibles. Cette composante doit être de rang ≥ 22 et passer le piège.

**Mise en garde.** J'avais cru exclure 132 (d₆⁴) par ce lemme, en pensant qu'il n'y avait que 2 types orthogonaux. Le test
explicite montre que la glue (s,v) donne aussi les types croisés : le graphe est connexe, et 132 N'EST PAS exclu par ce lemme.

## 4. Autres faits démontrés, disponibles pour les arguments par famille
- **(L5) Caractéristique.** Pour tout ε ∈ {±1}⁴⁴, Σ ε_u u + Σ ε_y y est un vecteur CARACTÉRISTIQUE de U.
  - Raison : (F) appliqué à un χ₈ donne 7χ ≡ Σu + Σy mod 2U.
  - Sa norme 140 − εᵀTε est ≥ 8 et ≡ 0 (8).
- **(L7) Étoiles.** Pour chaque bloc c, les 12 F_o = C_co u_o vérifient (F_o,h_c) = −1, ΣF_o = −3h_c et Σ_{o≠o'}(F_o,F_o') = 0.
- **Profils des h.** Chaque nouvelle racine β touche 1 ou 3 des h. Σ_c(h_c,β) est donc impair pour toute nouvelle racine β.
- **Décomposable ⇒ exclu :** la preuve générale est celle de « structures » (Gram projetée G₁² = 7G₁). Elle couvre 152 et 153.

## 5. O₂₄ : réduction à 141 classes de paires (y₁,y₂)
- **Forme normale.** a₁ = 1 − 4·1_{T₁} et a₂ = ε_D(1 − 4·1_{T₂}), avec D ∈ Golay mod Ω.
- **Orthogonalité.** y₁ ⊥ y₂ ⟺ D est une octade coupant A = T₁ ⊔ T₂ en 3 points, ou une dodécade la coupant en 4.
- **Classes.** Stab_{M₂₄}(T₁) (ordre 23040) × l'échange donnent **141 orbites**, qui couvrent 3 302 040 configurations. Dans 4
  d'entre elles, A est une octade. Confirmé indépendamment par « structures ».
- **Le piège est VIDE sur O₂₄**, pour une raison démontrée.
  - Il se ramène à « aucun v de norme 3 avec |(v,y₁)| = |(v,y₂)| = 3 », c'est-à-dire D ∉ {O + O'}.
  - Or l'orthogonalité l'interdit, puisque |O∩O'| ≥ |T₁∩T'| + |T₂∩T|.
- **Test d'engendrement.** Pour les 141 classes, les vecteurs de norme 3 de y⊥ engendrent N_max (indice 1).
- **Suite :** la recherche octades/u par classe (C2 + « structures », PL exact avec certificat de Farkas).

## 6. État de (C)
- **Exclues : 10.**
  - 145, 146, 151, 152, 153, 155 : Sol, relu ;
  - 117, 134, 142 : C1, maintenant sans dépendance thêta ;
  - 154 : packing ;
  - le lemme « décomposable » recouvre 152 et 153.
- O₂₄ : 141 classes, en cours.
- Le passage d'envelope_pack.py (packing + connexité) sur les 156 est en cours.
