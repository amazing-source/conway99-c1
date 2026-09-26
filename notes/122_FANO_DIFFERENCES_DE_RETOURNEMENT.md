# 122 — Fano tendu : différences de retournement, parités de branche, forme réduite de P-Ψ

*26/09, soir. Mathématiques pures, en dialogue avec « structures », C2 et Astra (modèle externe ; ses résultats arrivent
par l'utilisateur). DÉRIVÉ = preuve écrite ; les seuls calculs sont des contrôles exacts d'énoncés dérivés à la main
(identités vérifiées sur les configurations stockées).*

## 0. Résumé
| résultat | statut |
|---|---|
| **lemme des différences de retournement** : T(L) est sans triangle ssi poids(d(L)) ≠ 1 ; C6+C6 ssi d = (1,1,1) | DÉRIVÉ ; **refait à la main par « structures »** (les 8 cas de M) ; 91 droites contrôlées |
| identité des branches : E(XW) + E(YW) + N_X(W) + N_Y(W) ≡ 0 (mod 2) | DÉRIVÉ ; 9 × 21 contrôles, 0 écart |
| P-Ψ par bloc ⟺ trois relations F₂ ; les blocs à m = 1 épinglent π sans condition ; seules les étiquettes MM contraignent | DÉRIVÉ, refait par « structures » |
| droites « tout-CM » : P-Ψ toujours résoluble, retournements déterminés par les types de σ | DÉRIVÉ, refait par « structures » |
| si toutes les droites sont tout-CM cycliques : S = {Z : p_Z = 2} est ∅, le complémentaire d'une droite, le complémentaire d'un point, ou tout | DÉRIVÉ |

## 1. Lemme des différences de retournement
**Cadre.** Au Fano, τ_{X_s} apparie les deux autres classes Y, Z de chaque droite L ∋ X : τ_{X_s}(Y_t) = Z_{t⊕f(X_s,L)}.
On pose **d_X(L) = f(X₀,L) ⊕ f(X₁,L)**.
- d_X vaut 0 si les deux étiquettes de X induisent le même couplage Y–Z, et 1 si elles induisent le couplage opposé.
- C'est un invariant de jauge : renommer Y ou Z change f(X₀) et f(X₁) ensemble, et renommer X les échange.

**Énoncé.** Soit T(L) le graphe des arêtes τ sur les 12 paires de la famille de L. Il est 2-régulier, et ses cycles ont
une longueur multiple de 3.
- (a) Si poids(d(L)) = 1, T(L) contient un triangle. Il y a alors deux voisins communs sur une arête, et λ = 1 est
  violé.
- (b) Si d(L) = (1,1,1), T(L) = C6+C6, ou 4 triangles.
- (c) Si poids(d(L)) ∈ {0, 2}, T(L) = C12, ou il contient des triangles.
- Donc, en tout sommet de Fano tendu : **poids(d(L)) ≠ 1 pour chaque droite, et T(L) = C6+C6 ⟺ d(L) = (1,1,1)**.

**Preuve.**
- On suit T depuis le bloc AB : {A_s,B_t} → (par A_s) {A_s,C_u} → (par C_u) {C_u,B_{t′}} → (par B_{t′}) {B_{t′},A_{s′}},
  avec u = t ⊕ f(A_s), t′ = s ⊕ f(C_u) et s′ = u ⊕ f(B_{t′}).
- On écrit f(X_s) = f(X₀) ⊕ d_X·s. L'application de retour π : (s,t) ↦ (s′,t′) est alors **affine sur F₂²**, de partie
  linéaire M = [[d_A + d_B + d_A d_B d_C, 1 + d_B d_C], [1 + d_A d_C, d_C]].
- Les longueurs de cycle de T sont 3 fois celles de π.
- **Poids 1** : les trois cas donnent M d'ordre 3, sans valeur propre 1. Alors M + I est inversible, et π a un unique
  point fixe, donc un 3-cycle de T.
- **Poids 3** : M = I, et π est une translation, nulle (4 triangles) ou d'ordre 2 (C6+C6).
- **Poids 0 ou 2** : M est une transvection. Soit π a 2 points fixes, soit π² est une translation non nulle, et π est un
  4-cycle, donc C12. ∎

**Relecture indépendante.** « Structures » a refait l'application de retour et les 8 valeurs de M : pour le poids 1, le
polynôme caractéristique est x² + x + 1, irréductible ; pour les poids 0 et 2, on a des transvections avec
(M − I)² = 0. La conséquence sur les parties du plan de Fano est aussi confirmée.

**Contrôle.** Sur les 91 droites des configurations stockées (témoin, 8 σ tendus frais, 4 réglages Ψ-compatibles), toutes
admissibles : poids 0 → C12 (18 droites), poids 2 → C12 (51), poids 3 → C6+C6 (22), aucun poids 1.

**Lien avec β (Astra).** Dans le cas C6+C6, de classe doublée D, on a β = 0 sur le bloc opposé à D et β = 1 sur les deux
autres. C'est la constance par bloc vérifiée en notes/119 et à la main. Donc β n'est défini (constant) que sur les
droites de d = (1,1,1).

## 2. Identité des parités de branche
**Définitions.** Pour z ∈ VW, F5 donne atterrissage via W = atterrissage via V + V ou + W (en F₂³).
- La branche de z est « via W » si la somme vaut W. On note E(VW) le nombre de paires de VW en branche « via W ».
- Soit φ_W la fonction qui sépare les deux autres droites par W sur C4(L). On pose N_V(W) = Σ_{s,u} φ_W(classe de
  σ_V^{(s)}(W_u)).

**Énoncé.** Pour toute droite L = {X,Y,W} et tout W ∈ L : **E(XW) + E(YW) + N_X(W) + N_Y(W) ≡ 0 (mod 2).**

**Preuve.**
- La somme des 4 conditions P-Ψ d'un bloc est automatique : les 8 atterrissages via W des étiquettes de X ∪ Y se
  partagent 4/4 entre les deux droites, par le circulant de σ_W.
- On réécrit chaque terme par F5 : φ_W(b′) = φ_W(a′) + 1 + ε. ∎

**Contrôle** : 9 configurations × 21 couples (droite, point), 0 écart.

**Conséquences.**
- Sur chaque droite, les parités de branche des 3 blocs sont fixées par σ à un bit global près.
- Le e_i d'Astra (parité du nombre de sommets de R_i en branche « b = U ⊕ a ») est E(R_i) mod 2. Il ne dépend pas de U,
  car 4 est pair.

## 3. P-Ψ réduite (avec le critère à 3 inconnues de « structures »)
- **Codage.** On pose w_Z(k,v) = c_v ⊕ m_v·k : C0 = (0,0), C1 = (1,0), M0 = (0,1), M1 = (1,1). Avec F_v = c_v ⊕ m_v f_v,
  P-Ψ sur le bloc XY (troisième point Z) équivaut à : F_{x₀} ⊕ F_{x₁} = m_{y₀}, F_{y₀} ⊕ F_{y₁} = m_{x₀},
  F_{x₀} ⊕ F_{y₀} = 1.
- **Épinglages.**
  - Un bloc à m = 1 épingle π_B de façon toujours cohérente, puisque les deux C sont un C0 et un C1 (6 placements
    vérifiés par « structures »).
  - Un bloc à m = 2 exige « même C par classe ».
  - Un bloc à m = 0 laisse π_B libre.
- **Comptage.** Seules les étiquettes MM créent des conditions, et #MM = #CC + 6 − 2(m_A + m_B + m_C).
- **Droite tout-CM** : m = 1 dans les trois blocs et chaque étiquette C dans exactement un bloc.
  - Elle est toujours résoluble, et les 6 retournements sont déterminés par les types de σ.
  - Pour les motifs cycliques, d_X = [p_{Z′} = 2], où Z′ est le troisième point du bloc où les X sont M. Donc
    **poids(d) = #{Z ∈ L : p_Z = 2}**.
- **Si toutes les droites sont tout-CM cycliques**, le §1 impose que S = {Z : p_Z = 2} ne rencontre aucune droite en
  exactement un point. Les complémentaires possibles de S sont ∅, un point, une droite ou le plan entier.
  - Au témoin, S = {3,4,5,6}, qui n'est pas un complémentaire de droite. C'est cohérent avec sa mort.
- **Classes MM** : si les deux étiquettes de X sont mélangées dans le bloc XY, P-Ψ donne
  d_X = m_{y₀} ⊕ μ_{x₀} ⊕ μ_{x₁}. P-Ψ fixe donc d, donc la structure de T, par les types de σ.

## 4. État du Fano tendu
- P-Ψ laisse passer, au moins, les droites tout-CM, où τ est déterminé par σ. Le résidu est donc un problème en σ seul.
- Il reste à combiner cinq ingrédients pour conclure :
  - le §1 (admissibilité) ;
  - la contrainte τ–σ d'Astra (β_j = β_k = 1 ⟹ e_i = 0, par point) ;
  - le §2 (les e fixés par σ à un bit par droite près) ;
  - les triades (notes/120) ;
  - KBLDP.
- Travail en cours avec Astra, via l'utilisateur et « structures ».
