# 169 — Sous-cas (A) : les deux pistes (holonomies d'ordre supérieur, 7-adique) (11/10)

*Suite de la note 168. Notations : R, S, Z, K, a = M_RR, b = M_SS, X = M_RS ; E_r et E_s désignent les espaces
propres de A restreints à Z (r = 3, s = −4 à 99 ; r = 4, s = −5 à 243).*

## 1. Piste « holonomies » : la balance des angles
Dans chaque plan apparié, on note θ l'angle entre R et E_r. Les valeurs propres appariées de a sont λ = cos 2θ ·
(2r+1)/2 − 3/2, et celles de M² sont c = (r+2)(r−1) − 3λ. On pose :
- m = dim(R ∩ E_r), le nombre de fonctions de droites qui sont vecteurs propres de valeur r ;
- m′ = dim(R ∩ E_s), le nombre de fonctions de droites de somme nulle sur **toutes** les droites transverses (car
  M v = −(r+2)v ⇔ N_tᵀ v = 0).

**Identité de trace (démontrée).**

  (m − m′) + Σ_appariés cos 2θ = tr(Π_R U) = 3·dim R/(2r + 1),

où U = (2/(2r+1))(A + ½) est la réflexion E_r/E_s. Cette identité découle de la seule identité de blocs (note 168),
donc de λ = 1, μ = 2.

**Balance** : on dit que la configuration est équilibrée si Σ_appariés cos 2θ = 0. De façon équivalente, les
valeurs propres appariées c de M² sont symétriques par c ↦ (r−1)² + (r+2)² − c.

**Données à 243** (`code/asym243`, intersections calculées directement par SVD) :
- **46/46** partitions en grilles testées des 4 graphes connus sont équilibrées : m − m′ = 36 = 3·108/9 ;
- spectres observés de M² sur Z :
  - BvLS : 9¹⁴⁴ et 36⁷², sans partie appariée ;
  - jumeau : 18 ↔ 27 (32 et 32) ;
  - Γ₃ : 18 ↔ 27 et 12,4377 ↔ 32,5623 (racines de y² − 45y + 405) ;
  - Γ₄ : 18 ↔ 27.

  À chaque fois les paires somment à 45 = 3² + 6².

**Conséquence à 99 (démontrée).** La balance exigerait m − m′ = 3·44/7 = 132/7, qui n'est pas entier. Donc :

> **Tout graphe du sous-cas (A) est déséquilibré** : Σ_appariés cos 2θ = 132/7 − (m − m′) ≠ 0.
> Si la balance est un théorème général pour les revêtements à fibres-grilles, **le sous-cas (A) est impossible.**

**Statut de la balance : non démontrée.** Ce que j'ai établi :
- elle n'est **pas** conséquence des traces d'ordre ≤ 2, qui sont automatiques à partir de l'identité de blocs ;
- à 243, la seconde loi (grilles d'une même partie) est elle aussi automatique au niveau des opérateurs, donc elle ne
  l'explique pas ;
- les 4 graphes testés sont tous apparentés (systèmes de droites affines, revêtements de BH). La balance pourrait donc
  être un effet de leur symétrie (le Z₃ de revêtement) plutôt qu'un théorème.

*Prochaine étape :* chercher l'opérateur qui la produirait. Ce serait une isométrie Ω de R qui commute avec Π_R et
envoie E_r sur E_s sur la partie appariée, c'est-à-dire qui conjugue a en −3 − a sur cette partie. Il faut aussi la
tester sur tout nouveau srg(243,22,1,2) : ceux issus des squelettes de type nouveau, et un futur graphe sans
symétrie.

## 2. Piste 7-adique
**Réduction (démontrée).** Dans le sous-cas (A), Π_R n'a que des dénominateurs en 3. Sur Z₇, on a donc
Z = R ⊕ S de façon intègre, et

  rang₇(A − 3I) = 15 + k₇ = 1 + rang₇(N|_Z),  avec N = A + 4 ≡ 5K + M (mod 7) et N² = 7N.

**Inégalité (démontrée).** On a Π_R N Π_R = 5 + a et 3(5 + a) = 25 − M²|_R, d'où

  14 + k₇ ≥ rang₇(M²|_R − 4).

Sur R, M² − 4 a pour valeurs propres 0 (m), 21 ≡ 0 (m′) et c − 4. Le 7-rang compte donc, au plus, les valeurs
appariées c ≢ 4 modulo un premier au-dessus de 7. En l'état, c'est une borne faible : avec k₇ ≤ 28, au plus 42
valeurs appariées « génériques » sur 44 − m − m′.

**Statut** : la piste ne conclut pas seule. Elle deviendrait décisive couplée à une information sur la répartition des
c mod 7, par exemple si la balance (c ↔ 29 − c, et 29 ≡ 1 mod 7) était établie.

## 3. Bilan
| énoncé | statut |
|---|---|
| identité de trace (m − m′) + Σ cos 2θ = 3 dim R/(2r+1) | démontré |
| (A) ⇒ configuration déséquilibrée | démontré |
| balance pour les 46 partitions testées à 243 | calculé |
| balance en général ⇒ (A) impossible | démontré (implication) |
| balance en général | **ouvert** : c'est le maillon manquant |
| borne 7-adique 14 + k₇ ≥ rang₇(M²\|_R − 4) | démontré, faible |
