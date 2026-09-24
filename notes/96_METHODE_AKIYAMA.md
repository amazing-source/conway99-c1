# 96 — La méthode des réseaux d'Akiyama (sept. 2026) et sa transposition à 99

*Découverte de la nuit du 25/09 : K. Akiyama, « Nonexistence of a strongly regular graph with parameters
(266,45,0,9): a certificate-free Lean proof », arXiv:2609.08319 (8 sept. 2026, 25 p., texte intégral lu).
C'est une non-existence **nouvelle** d'un cas ouvert, obtenue par une méthode arithmétique globale (réseaux entiers,
séries thêta), et entièrement formalisée en Lean. Aucune application à 99 n'existe : la méthode a quelques jours.*

## 1. Le mécanisme pour (266, 45, 0, 9)
1. **Repère local serré.** On fixe o, X = Γ(o) (45 points, indépendants), Y = Γ₂(o) (220 points), S = MᵀM (M :
   incidence X–Y), H = Γ[Y]. La matrice entière L = 9I + 3J − S − 3H vérifie L² = 45L + 90J. Elle est donc positive,
   de valeurs propres 165 (×1) et 45 (×11). Z^Y modulo son radical donne un réseau entier de rang 12 où les g_y ont
   norme 3.
2. **Centroïde entier** (rang de L mod 11 égal à 12) : Σ g_y = 11c avec c dans le réseau.
3. Forme lorentzienne, repère serré de rang 11 (les u_y, norme 9/4, Σ⟨v,u_y⟩² = 45|v|²) ; sur-réseau pair maximal,
   dont le discriminant est anisotrope et tué par 15 (plus une classe d'ordre 4 portée par les u_y).
4. **Complétion marquée** : on recolle un D₇ (classe spinorielle d'ordre 4, norme 7/4) pour tuer la partie 2 ; les
   t_y = (u_y, s) ont norme 4. On ajoute un complément de rang 6 pris dans une table finie (4 cas), ce qui donne un
   réseau pair unimodulaire L de rang 24 contenant les 220 vecteurs marqués.
5. **Isolement des racines** (l'identité de repère contre l'intégralité : 220 ≤ 180 est absurde), puis **identité de
   Venkov** : en rang 24, la série thêta harmonique de degré 2 est une forme parabolique de poids 14, donc nulle. D'où
   Σ_r r rᵀ = (|R|/12) I, puis |R| = 288 et le système de racines A₁₁D₇E₆ (nombre de Coxeter 12).
6. **Moments** des projections des vecteurs marqués sur A₁₁ et E₆ (masses 275 et 220), bornes de trace qui éliminent
   3 des 4 compléments, puis l'équation 4x + 4y − 2z = 50 sans solution. La branche « type A » (e_y = 0) est fermée
   par la non-existence d'un 2-(56,12,9) quasi-symétrique (Munemasa–Tonchev, reprouvé sans classification).

## 2. Les objets analogues pour 99 (calculés et vérifiés ici)
Au sommet x : Y = Γ₂(x) (84 points), M (14 × 84, 2 étiquettes par point), S = MᵀM (étiquettes partagées),
P' = MᵀPM (P = involution des mates : couples d'étiquettes mates), H = Γ[Y] (12-régulier).
Valeurs propres jointes (H, S, P') sur 1^⊥ : K₃ (40) : (3, 0, 0) ; K₋₄ (30) : (−4, 0, 0) ; mates-symétriques (6) :
(−2, 10, 10) ; mates-antisymétriques (7) : (0, 12, −12). Et sur 1 : (12, 24, 24). On obtient deux **repères serrés
entiers exacts** :
- **L₋₄ = 24I + 2J − 8H − 3S − P'** : valeur propre 56 sur K₋₄, 0 ailleurs (vérifié sur les 5 espaces propres
  joints). On obtient 84 vecteurs de norme 20 dans un réseau pair de rang 30, avec Σ_y ⟨v,v_y⟩² = 56|v|² et Σ v_y = 0.
- **L₃ = 60I − 2J + 15H − 4S + P'** : valeur propre 105 sur K₃. On obtient 84 vecteurs de norme 50 en rang 40
  (Σ⟨v,v_y⟩² = 105|v|²).
Ces réseaux sont (K₋₄)^# et (K₃)^# remis à l'échelle (K_θ = Z⁸⁴ ∩ espace propre, primitif). Leur arithmétique locale
est celle de L17 (parties 2, 3, 5 déterminées) et, en 7, de L19 (recollement (Z/7)^k, 2 ≤ k ≤ 30).

## 3. Ce qui change, et pourquoi la transposition n'est pas immédiate
- **Densité du repère.** 266 : 220 vecteurs en dimension 11 (20 par dimension), normes et produits minuscules
  (0 à 3). 99 : 84 vecteurs en dimension 30 ou 40 (2 à 3 par dimension), normes 20 ou 50. L'argument d'isolement des
  racines (220 ≤ 180) repose sur cette densité. À 99 l'inégalité analogue a une grosse marge.
- **Le premier 2.** La constante du repère est 45 (impaire) pour 266, d'où des sur-réseaux automatiquement pairs et
  un discriminant sans partie 2 (à la classe d'ordre 4 près). À 99 elle vaut 56 = 8·7 : partie 2 non triviale, et la
  partie 7 est l'invariant global k de L19.
- **Rang de complétion.** 30 + (≥ 2) ⇒ rang 32, ou 40, ou 48. En rang 24 la série thêta harmonique de degré 2 est
  nulle (S₁₄ = 0), et c'est le levier décisif. En rang 32, 40, 48 elle vit dans S₁₈, S₂₂, S₂₆ (dimension 1) : on
  obtient seulement une proportionnalité entre les seconds moments des racines et ceux de la couche de norme 4. C'est
  beaucoup plus faible, et il n'y a pas de classification exploitable (les réseaux unimodulaires pairs de rang 32
  se comptent par milliards).
- **Où est la torsion.** Les repères L₋₄, L₃ contiennent H, donc toute la torsion en x. Un Γ non tordu (quotient de
  H(7,3), impossible par L1) donnerait un repère « de type racines ». La torsion le déforme, et c'est cette
  déformation qu'une contrainte de réseau devrait interdire.

## 4. Verdict et plan (non exécuté cette nuit)
C'est la seule méthode **globale et arithmétique** nouvelle rencontrée qui ait tué un cas ouvert récemment, et elle
s'articule exactement avec nos objets (K₃, K₋₄, L17, L19). Mais les trois leviers qui la font marcher à 266 (repère
très dense, constante impaire, rang 24) manquent à 99. Plan si l'on veut l'essayer :
1. Calculer la forme discriminante de (K₋₄)^#(56) et de (K₃)^#(105) (L17 en donne l'essentiel ; en 7, en fonction
   de k), puis leurs sur-réseaux pairs maximaux (anisotropes, donc de petit rang à chaque premier).
2. Chercher le plus petit complément donnant un unimodulaire pair (rang 32 ?) et écrire l'identité thêta harmonique de
   degré 2 dans S₁₈ = ⟨ΔE₆⟩. Elle relie les seconds moments des racines et de la couche de norme 4 ; voir si les 84
   vecteurs marqués (après recollement) tombent dans une couche basse.
3. Tester d'abord la mécanique sur BvLS (243), qui existe : tout ce qui « contredirait » BvLS est faux.
Coût : plusieurs jours de travail. Faisable sur le portable (algèbre exacte, pas de recherche exhaustive).
