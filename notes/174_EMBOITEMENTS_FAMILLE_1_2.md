# 174 — srg(6273,112,1,2) et srg(494019,994,1,2) : emboîtements par points fixes (12/10)

*Demande de Dilan : repartir sur les deux paramètres ouverts au-dessus de BvLS et voir ce qui émerge, notamment côté
symétrie et asymétrie. Code : `code/family_nesting/` (`nesting.py`, `bvls_fix.py`, sortie `nesting_output.txt`).*

## 0. La famille
srg(v,k,1,2) impose r = t, s = −(t+1), k = t² + t + 2 et t ∈ {1, 3, 4, 10, 31} :

| t | v | k | f (mult. de r) | g (mult. de s) | statut |
|---|---|---|---|---|---|
| 1 | 9 | 4 | 4 | 4 | Paley(9), unique |
| 3 | 99 | 14 | 54 | 44 | ouvert (Conway) |
| 4 | 243 | 22 | 132 | 110 | BvLS + 3 autres (notes 159, 165) |
| 10 | 6273 | 112 | 3280 | 2992 | ouvert |
| 31 | 494019 | 994 | 250914 | 243104 | ouvert |

Déjà établi pour v = 6273 et 494019 : pas d'étalement régulier (note 165, lemme 1), pas d'alignement total
(note 168, §4), et le graphe est forcément « tordu », car v n'est pas une puissance de 3 (note 30, L1). Le plancher de
symétrie Z₃ de 243, qui vient des revêtements, ne s'applique donc pas à ces deux graphes : c'est la même situation qu'à 99.

## 1. Le lemme des points fixes (démontré, élémentaire)
Soit g un automorphisme d'ordre premier **impair** p et Fix l'ensemble de ses points fixes.
1. Deux sommets fixes adjacents ont un unique voisin commun, qui est donc fixe. Deux sommets fixes non adjacents ont
   2 voisins communs, permutés par g ; comme p est impair, les deux sont fixes. Fix vérifie donc λ = 1 et μ = 2.
   - Si Fix contient deux sommets non adjacents, il est de diamètre ≤ 2 et régulier. Pour x ≁ y, le comptage
     Σ_{z∈N(x)} |N(z) ∩ N(y)| = 2k′_x − 2 est symétrique en x et y.
   - Fix est donc vide, K₁, K₃, ou un srg(v′,k′,1,2) **plus petit de la famille**.
2. Les triangles par un sommet fixe x qui ne sont pas dans Fix sont permutés en p-cycles. Un tel triangle ne peut pas
   avoir exactement un sommet fixe en plus de x, sinon il serait l'unique triangle d'une arête fixe. On en tire :
   - p | (k − k′)/2 ;
   - p | v si Fix = ∅ ;
   - v ≡ |Fix| (mod p).
3. **Un sommet non fixe a au plus un voisin fixe.** Sinon ses deux voisins fixes, adjacents ou non, l'auraient comme
   voisin commun et le fixeraient. D'où
   **|Fix|·(k − k′) ≤ v − |Fix|.**
4. Le caractère χ_r(g) = (a₁ + (t+1)|Fix| − (k+t+1))/(2t+1) est un entier, ≡ f (mod p), avec
   a₁ = #{x : x ~ g(x)} ≡ 0 (mod p).

## 2. Contrôle sur les 4 graphes à 243 sommets (calculé : nauty + échantillonnage du groupe)
Prédiction : p = 3 ⇒ Fix ∈ {∅, Paley(9)} ; p = 5 ⇒ Fix = K₃ ; p = 11 ⇒ Fix = K₁ ; congruences sur a₁. Observé :
- BvLS (|Aut| = 3 849 120) :
  - p = 3 : Fix = ∅ (a₁ = 0 ou 243) ou Paley(9) (a₁ = 36) ;
  - p = 5 : K₃ (a₁ = 30) ;
  - p = 11 : K₁ (a₁ = 22).
- Jumeau (4 320) : Fix = ∅ ou Paley(9) pour p = 3, et K₃ pour p = 5.
- Γ₃ (864) : Fix = ∅ (a₁ = 0 ou 243).
- Γ₄ (3 888) : Fix = ∅ (a₁ ∈ {0, 81, 162, 243}) ou Paley(9) (a₁ = 36).

Tout concorde, y compris les classes de a₁.

## 3. Le tableau (démontré pour p impair ; p = 2 non traité)
**srg(6273,112,1,2).**

| p | Fix possible |
|---|---|
| 3 | ∅ ou Paley(9) |
| 5 | K₃ |
| 7 | **K₁** |
| 11 | K₃ |
| 17, 41 | ∅ |

Le lemme 3 **exclut** Fix = srg(99), pour p = 7 (9 702 > 6 174), et Fix = srg(243), pour p = 3 ou 5
(21 870 > 6 030). Les diviseurs premiers de |Aut| sont dans {2, 3, 5, 7, 11, 17, 41}.

**srg(494019,994,1,2).**

| p | Fix possible |
|---|---|
| 3 | ∅, Paley(9) ou **srg(243)** |
| 5 | Paley(9) ou **srg(99)** |
| 7 | K₁ ou **srg(99)** |
| 11 | Paley(9) |
| 19, 107 | ∅ |
| 31 | K₃ |
| 71 | K₁ |

Fix = srg(6273) est exclu (5 532 786 > 487 746). Les diviseurs premiers de |Aut| sont dans
{2, 3, 5, 7, 11, 19, 31, 71, 107}.

**srg(99,14,1,2), pour comparaison.**

| p | Fix possible |
|---|---|
| 3 | ∅ ou K₃ |
| 5 | Paley(9) |
| 7 | K₁ |
| 11 | ∅ |

Pour p = 5, l'inégalité est une **égalité** (9·10 = 90) : chaque sommet hors du Paley(9) a exactement un voisin dedans.

## 4. Ce qui émerge
- **La famille s'emboîte par symétrie.** Un membre symétrique contient des membres plus petits comme sous-graphes fixes.
  L'inégalité du lemme 3 décide quels emboîtements survivent :
  - 9 ⊂ 99 (p = 5, cas limite) ;
  - 9 ⊂ 243 (p = 3, observé) ;
  - 9 ⊂ 6273 ;
  - 9, 99 et 243 ⊂ 494019 ;
  - **jamais** 99 ou 243 ⊂ 6273, ni 6273 ⊂ 494019.
- **Lien Conway ↔ 494019.** Un srg(494019) avec un automorphisme d'ordre 5 ou 7 dont le sous-graphe fixe n'est pas
  réduit à Paley(9) ou K₁ contient un graphe de Conway. Contraposée : si Conway-99 n'existe pas, tout automorphisme
  d'ordre 5 d'un srg(494019) fixe exactement un Paley(9), et tout automorphisme d'ordre 7 un seul sommet. Pour 6273, le
  lemme 3 coupe le lien avec 99.
- **Asymétrie.** Pour 6273 et 494019, aucun mécanisme connu n'impose de symétrie : pas de revêtement, pas de grilles.
  Le tableau dit seulement quelle forme aurait une symétrie *si* il y en a une. Comme à 99, rien n'exclut un graphe
  asymétrique.
- **Pourquoi 99 est le cas « K₇ » (note 173).** En un point c d'une coclique de Hoffman, les α_H − 1 autres points sont
  les arêtes d'un graphe t-régulier sur les k blocs par c. Ce graphe contracté par les mates est 2t-régulier sur k/2
  sommets, sans boucle :

  | t | 2t | k/2 − 1 | conséquence |
  |---|---|---|---|
  | 1 | 2 | 1 | multi-arête **forcée** : explique Paley(9) |
  | 3 | 6 | 6 | simple ⇔ **graphe complet K₇** : 99 est le seul cas serré |
  | 4, 10, 31 | 8, 20, 62 | 10, 55, 496 | lâche |

## 5. Statut bibliographique
Makhnev et Minakova (Discrete Math. Appl. 14(2), 2004) étudient les automorphismes des srg(v,k,1,2) pour
u = t ∈ {1,3,4,10,31} par la méthode de Higman. Je n'ai pas pu lire l'article (accès refusé). Le lemme et le tableau
recoupent très probablement leurs résultats. La nouveauté ne doit donc pas être revendiquée avant vérification.
