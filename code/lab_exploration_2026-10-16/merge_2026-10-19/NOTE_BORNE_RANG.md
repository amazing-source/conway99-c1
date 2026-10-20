# Borner le 7-rang par le haut : peut-on prouver r = 37 ?

LAB (agent), 20/10/2026, soir. Mission : prouver r = rang₇(A − 3I) = 37, c'est-à-dire exclure 39, 41 et 43, ou obtenir
un résultat partiel (« r ≠ 39 », « r ≥ 39 force une droite spéciale »…).

**Statuts.**
- **P** : preuve écrite ici, non relue par un tiers.
- **A** : déjà dans l'archive (référence donnée).
- **E** : calcul fait ici (script et journal dans ce dossier, un processus, moins de 5 min).
- **X** : ouvert.
- « **Réfuté** » : l'espoir annoncé est contredit par un calcul (E) ou une preuve (P).

Rien ici n'est relu par un humain. Rien n'exclut un rang.

---

## 0. Réponse courte

1. **Pas de preuve de r = 37.** Aucun des rangs 39, 41, 43 n'est exclu, et je n'ai pas de résultat partiel du type
   « r ≠ 39 ».
2. **Diagnostic (P + E).** Toutes les conséquences *linéaires* connues des équations du srg sur un objet local ou
   semi-local (droite, sommet, quatre étoiles, réseaux Λ₋(T), genre, signes) sont exactement cohérentes à chaque rang
   de la fenêtre. Elles ne donnent que des **minorations** de r.
   - Une majoration demande des vecteurs propres entiers dont la Gram est non dégénérée mod 7 (§3). Ce sont des
     structures spéciales (Fano, grilles, composantes, jumeaux), qu'aucune donnée locale ne force.
   - Localement, ce sont les **petits** rangs qui meurent (surdéterminés), et les grands qui survivent. Le sens de
     l'attaque « tout ramener à 37 » va donc à rebours de ce que permettent les outils.
3. **Ce qui est nouveau ici.**
   - (P) Pour toute droite T : dim C(T) = ρ(T) + r(T) = r − 38 + d(T) − r(T), où C(T) est l'espace des mots de D
     portés par le lointain. Tout mot de C nul sur N[T] est automatiquement dans D (§2.2).
   - (P) **Scindage orthogonal à tout rang.** Pour toute droite générique, E₋ ⊗ ℤ₇ = Λ₋(T) ⊥ Λ′_T, avec Λ′_T
     7-modulaire de rang 36, engendré par les 7Pe_u (u ∈ N[T]). L'archive (RD §2) ne l'énonçait qu'au rang 37 (§2.3).
   - (P) **Relations forcées en un sommet.** Les sept espaces C(T_i) des droites par un sommet ont entre eux au moins
     6r − 244 relations linéaires indépendantes : 2 au rang 41, 14 au rang 43. Au rang 43, cinq droites quelconques
     suffisent (§2.5).
   - (E) **Modèle de position générale.** Un sous-espace totalement isotrope *aléatoire* de la bonne dimension
     reproduit exactement, à chaque rang, toutes ces dimensions, y compris la fréquence des droites à torsion. Aucun
     argument de dimension sur les mots portés par des lointains ne peut donc exclure un rang (§4.2).
   - (E) **Étalonnage du p-rang sur des graphes réels à λ = 1** (§5.1).
     - Graphes srg(378,52,1,8) d'hémisystèmes : rang₃ = 104 et rang₅ = 90, pour une borne de 105. Ces valeurs sont
       les mêmes pour |Aut| = 6 et |Aut| = 600.
     - Le 5-rang bas s'explique par une structure héritée : A − 4I ≡ NᵀN (mod 5), N étant l'incidence du GQ sur GF(5).
     - Un p-rang bas signale une structure F_p cachée, pas une symétrie. On n'en connaît aucune pour Conway.
   - (E) **Conditions de sommet valables à tout rang, testées sur les témoins SAT de R7** (§5.2).
     - Le bloc réel 7P_v sur leurs 51 labels a 8 valeurs propres négatives et un rang 47 (au plus 30 exigé).
     - Son 7-rang est 47 (au plus 28 exigé).
     - Leur base à quatre étoiles viole déjà tout : rang 40, 7-rang 39 à 40.
     - La formule est validée exactement sur deux srg(243) réels (écart 0, rang 88 = g − k).
     - Le 7-rang de l'archive est retrouvé sur les 331 objets de rang 30 (331/331).
4. **Partiel.**
   - (P, conséquence de A) Tout bloc à quatre étoiles a un 7-rang au plus r − 15.
   - (E, échantillon biaisé) Parmi les 331 objets réels de l'archive :
     - 204 ont un 7-rang de 29 ou 30, et sont donc **impossibles à tout rang** ;
     - les 127 autres ont un 7-rang de 25 et **n'existent qu'aux rangs 41 et 43** ;
     - aucun n'est compatible avec r ≤ 39.

   Ce n'est pas un énoncé sur tous les objets (X).
5. **Prochaine étape la plus prometteuse** (§7).
   - Abandonner l'objectif « r = 37 ».
   - Viser un objet fini **uniforme en rang** autour d'un sommet : le modèle combinatoire de R7/R8, plus les coupes
     réelles (0 ⪯ 7P_v[X,X] ⪯ 7I, rang ≤ 30) et 7-adiques (rang₇ ≤ 28), qui valent aux quatre rangs à la fois.
   - Les témoins SAT actuels les violent massivement. Une boucle CEGAR (SAT, puis contrôle spectral, puis coupe
     linéaire) est réalisable sur le PC du labo.
   - Contrôle positif obligatoire sur srg(243). Rien n'a été lancé.

---

## 1. D'où vient la fenêtre, et ce qui a déjà été tenté (A)

Sources lues : notes de Codex 99, 101, 102, 124, 127 (`scratchpad/codex_27ac387d/notes`) ; TL =
`work/c1_theta_lp_2026-10-07/NOTE.md` (§9–17.11, 17.22, 17.31, 17.40, 17.48–17.52, 17.80) ; RD =
`work/c1_index_2026-10-09/NOTE_RESEAUX_DE_DROITE.md` ; dans ce dossier, NOTE_FUSION, NOTE_OBSTRUCTION, NOTE_BOOST et
SYNTHESE_MECANISMES.

**Bas de la fenêtre.**
- r ≥ 37 vient du programme linéaire thêta (M₂₂(Γ₀(7))), des comptes de vecteurs duaux et des bornes de graines
  (a₇ ≤ 990).
- r = 35 est exclu par une identité entière exacte (TL 17.11 ; Codex 179–180).

**Haut de la fenêtre.**
- L22 (Codex 101) : formule d'oddité sur E₋, de déterminant 9·7^(r−1). Le 9 est un carré, donc r ≠ 45 ; r est impair.
- Donc r ∈ {37, 39, 41, 43}.

**Tentatives de majoration ou de « rang 37 », et pourquoi elles s'arrêtent.**

| source | ce qui a été fait | pourquoi ça s'arrête |
|---|---|---|
| Codex 99 §3 | bornes de boules de droites (L21) | toutes les bornes locales sont des **minorations** (rang d'une sous-matrice). Une majoration demande des vecteurs du noyau mod 7 au-delà des rationnels, et « aucun mécanisme n'en fournit ». Heuristique de Cohen–Lenstra : k = 30, interdit par L22, d'où **k = 28 (r = 43) attendu** |
| Codex 102 §3–§9 | signe (discriminant) des blocs extrêmes ; L23 | le signe n'agit que sur les blocs extrêmes, et les blocs connus ont au plus 39 sommets. Au mieux r ≥ 39, sous condition (droite générique τ-carrée). « Aucune contradiction ne peut venir du genre » ; k = 28 est invisible localement |
| TL 17.40, 17.48–17.52 ; Codex 202–208 | rang de Gram des familles : ≤ 45 − r côté E₋, ≤ 56 − r côté K⁺ ; relations à un sommet ; « 37 est un cas d'égalité » | contraint des configurations, pas des nombres. Le plafond local en un sommet est 14, hyperbolique : il ne peut exclure ni 37, ni 39, ni 41 (Codex 207) |
| TL 17.22(e), 17.31 | au rang 43, série thêta affine en 6 paramètres | exclusion seulement si 2a₈ + 16a₉ + a₁₃ < 2632, ou b₂ < 922, ou b₃ < 6 696 790. Le comptage ne peut pas : b₂ ≥ 968 est prouvé. « Tout rang contient des paires de type 43 » |
| RD | det Λ₋(T), structure en 7, invariants de Hasse | seul 7 filtre : c'est L23 |
| NOTE_FUSION R4, OBSTRUCTION §3.2, BOOST §5, SYNTHESE §3.5 | tests par droite à ρ ≥ 2 | étoile morte 5/5 au rang 39 (1 à 2 h par droite). Aux rangs 41 et 43, l'étoile est heuristiquement satisfaisable et la double étoile non parcourue |
| nuit du 13-14/10 (`c1_night_2026-10-14/NOTE_NIGHT.md`) | fenêtre refaite sans les notes | redécouverte, plus faible. **Ne pas refaire** |

---

## 2. Le cadre exact

**Notations.**
- M = A − 3I (mod 7), C = Im M (dimension r) et Δ = A − 3I + 3J ≡ 3S, où S = J − I − 2A est la matrice de Seidel.
- δ_u = Δe_u. L̄ = E₋ mod 7 (dimension 44) et Ē₃ = E₃ mod 7 (dimension 54).
- Pour une droite T : N = N[T] (39 sommets), F = F(T) (60 sommets), d(T) = dim ker₇(3I − G_T).
- r(T) est le rang déséquilibré (Codex 126 et 127) et ρ(T) le rang du résidu. L'identité
  r = 38 − d + 2r(T) + ρ(T) est A.

### 2.1 Le code D et sa forme b

**Lemme 1 (A : Codex 102 §1 ; reformulé, P).**
D := C ∩ 1^⊥ = C ∩ C^⊥ = Im Δ, de dimension r − 1, et totalement isotrope.
- C = D ⊕ ⟨1⟩ et C^⊥ = ker M = D^⊥ ∩ 1^⊥.
- D = rad(L̄) = rad(Ē₃) = L̄ ∩ Ē₃.
- L̄/D = Q_r est non dégénéré, de dimension 45 − r et de type moins.

*Preuve.* M² ≡ 2J et M1 = 4·1, donc :
- D = M(1^⊥) ⊂ C ∩ 1^⊥, de dimension r − 1 ;
- Mx·My = 2(Σx)(Σy) = 0, donc D est isotrope ;
- 1·1 = 99 ≡ 1, donc 1 ∈ C ∖ C^⊥.

Les identités avec les réseaux sont celles de Codex 101–102. ∎

**Lemme 2 (P ; c'est la forme β de Codex 102 §1.3 dans d'autres coordonnées).**
On pose b(Δx, Δy) := −xᵀΔy. Cette forme est bien définie et non dégénérée sur D. De plus :
- b(δ_u, δ_w) = −Δ_uw ∈ {0, 3, 4}, valant 0 si u = w, 3 si u ∼ w et 4 sinon ;
- **b(d, δ_u) = −d_u** pour tout d ∈ D.

*Preuve.*
- Si Δx = 0, alors xᵀΔy = (Δx)ᵀy = 0 : la forme est bien définie.
- Si b(Δx, ·) = 0 sur D, alors Δx ⊥ F⁹⁹ : elle est non dégénérée.
- b(Δx, δ_u) = −(Δx)_u. ∎

**Lemme 3 (P).** Pour tout X ⊆ V, on a D ∩ F^{V∖X} = (span{δ_u : u ∈ X})^{⊥_b}. Les mots de D nuls sur X sont donc
l'orthogonal, pour b, des générateurs indexés par X. *Immédiat par le lemme 2.*

### 2.2 Droites

**Proposition 4 (P).** Soit C(T) := D ∩ F^{F(T)}.

(a) Tout mot de C nul sur N[T] est dans D.
- *Raison :* MC = ⟨1⟩, et (Mc)_t ne voit que N[t] ⊆ N[T].

(b) **dim C(T) = r − 38 + d(T) − r(T) = ρ(T) + r(T), pour toute droite.**
- *Preuve :* dim D|_N = 39 − dim(D^⊥ ∩ F^N).
- D^⊥ ∩ F^N = {y porté par N : My ∈ ⟨1⟩} = ⟨y_T⟩ ⊕ (ker M_NN ∩ ker M_FN), de dimension 2 + d − r(T), où
  y_T = 6·1_T + 1_{N(T)∖T}.
- Sur ℤ, (A − 3I)y_T = 6·1, ce qui se vérifie sommet par sommet : 24 − 18, 9 − 3, 6 − 0.
- On conclut avec l'identité A.

(c) **Cas générique** (d = 1, r(T) = 0) :
- C(T) = Im Res_T = rad(Ū_T), avec Ū_T = Λ₋(T) mod 7, de dimension r − 37 ;
- C = C_T ⊕ C(T), où C_T est l'espace engendré par les 39 lignes proches, de dimension 37 ;
- 1 ∈ C_T, puisque My_T = 6·1 ;
- D_T := C_T ∩ D = span{δ_u : u ∈ N[T]} est de dimension 36, b-non dégénéré, et **D = D_T ⊥_b C(T)**.

*Remarque.* Pour une droite déséquilibrée (r(T) > 0), C_T ∩ C(T) contient les r(T) vecteurs M_FN k, k ∈ ker M_NN.
C_T + C(T) est alors de codimension r(T) dans C.

Attention à ne pas confondre : le terme 2r(T) + ρ(T) de la formule de rang (NOTE_FUSION R5) n'est **pas** la dimension
de C(T), qui vaut r(T) + ρ(T).

**Reformulation (P).** r = 37 ⟺ D n'a aucun mot non nul porté par le lointain d'une droite générique. Il suffit de le
vérifier pour une seule droite.

### 2.3 Le scindage orthogonal

**Théorème 5 (P ; extension de RD §2, qui ne traite que le rang 37).** Soit T une droite générique et r ∈ {37, …, 43}
quelconque. Alors

    E₋ ⊗ ℤ₇ = Λ₋(T) ⊥ Λ′_T,     Λ′_T := E₋ ∩ Λ₋(T)^⊥ = span_{ℤ₇}{7Pe_u : u ∈ N[T]},

et Λ′_T est 7-modulaire de rang 36 : tous ses produits scalaires sont ≡ 0 mod 7. De façon équivalente,
Λ₋(T)^# ⊆ E₋^# (7-adiquement).

*Preuve.*
1. Soit x ∈ Λ₋(T)^#. Comme 7Π_T est 7-entier (cas générique, A), on a 7x ∈ Λ₋(T).
2. La réduction de 7x est dans rad(Ū_T) = C(T) ⊆ D = rad(L̄) (proposition 4).
3. Donc (7x, l) ∈ 7ℤ₇ pour tout l ∈ E₋, c'est-à-dire x ∈ E₋^#.
4. Ainsi π_{Λ₋(T)}(E₋) ⊆ Λ₋(T), d'où le scindage.
5. Le complément a pour discriminant (ℤ/7)^{(r−1)−(r−37)} = (ℤ/7)^{36}, donc il est 7-modulaire.
6. Pour u ∈ N[T], (7Pe_u, x) = 7x_u = 0 pour tout x ∈ Λ₋(T), et les réductions −δ_u engendrent D_T, de dimension 36.
   Le lemme de Nakayama conclut. ∎

**Conséquences (P).** Pour tout x ∈ E₋ :
- Π_T x est 7-entier ;
- (x, x) ≡ |Π_T x|² (mod 7) ;
- la classe de x dans Q_r est celle de Π_T x ;
- Ū_T/C(T) ≅ Q_r : **chaque droite générique porte toutes les classes de Q_r**.

**Énoncé jumeau sur Λ₃(T)**, de rang 18 : Λ̄₃(T)/C(T) ≅ Q′_r := Ē₃/D, de dimension 55 − r.
- La preuve est la même, à condition que le projecteur lointain du côté 3 soit 7-entier.
- C'est le cas dès que 7 ∤ τ·Θ, c'est-à-dire, puisque Θ ≡ −τ (§4.3), dès que la droite est générique.
- Je n'ai pas vérifié ce point à part.

L'opérateur d'angles O = Π_TΠ_{T′}Π_T sur Λ₋(T), pour deux droites génériques, est 7-entier et induit l'identité sur
Q_r. Tout cela est automatique et ne contraint rien.

### 2.4 Sommets

**Proposition 6 (A : Codex 101 §5.2 et 102 §2 ; rederivé, P).**
- Pour **tout** sommet v, V_v := span{δ_u : u ∈ N[v]} est b-non dégénéré de dimension 14.
  - Valeurs propres de −Δ sur le moulin (15 sommets) : 2 (×7), 4 (×7) et 0 (×1) ; discriminant de la partie non
    dégénérée 2²¹ ≡ 1.
  - La seule relation est Σ_{u∼v} δ_u = 3δ_v.
- Donc D = V_v ⊥ D_v, avec D_v := D ∩ F^{Γ₂(v)} de dimension **r − 15**.
- La Gram des 84 générateurs de D_v est −Σ_v, avec
  **Σ_v ≡ A₂₂ − 3I − 2J + 3·Inc + Par**, où :
  - Inc(w, w′) = |w ∩ w′| ;
  - Par(w, w′) = |w′ ∩ w̄|, w̄ étant la paire des partenaires.

  C'est la matrice M_x de Codex ; on a Σ_v² ≡ 0 et rang Σ_v = r − 15.
- Contrôle à la main : les sommes ponctuelles Σ_{w∋p} Σ_v(w′, w) sont nulles dans les trois cas p ∈ w′, p̄ ∈ w′ et
  ligne(p) ∩ w′ = ∅.
- Version réelle (P, validée en §5.2) : 7P_v = 3I − A₂₂ + J/9 − C₀, où C₀ ne dépend que des labels. C'est 7 fois un
  projecteur de rang 30.

### 2.5 Relations forcées entre les droites d'un sommet

**Proposition 7 (P).** Soient T₁, …, T₇ les droites par v. On a C(T_i) ⊆ D_v et dim C(T_i) ≥ r − 37, puisque
d − r(T) ≥ 1. L'application ⊕_i C(T_i) → D_v a donc un noyau de dimension au moins 7(r − 37) − (r − 15) = **6r − 244**,
soit 2 au rang 41 et 14 au rang 43.
- Au rang 43, déjà pour cinq droites quelconques par v : 30 > 28.
- Au rang 39, rien n'est forcé : 14 ≤ 24.

Ces relations, c₁ + … + c₇ = 0 avec c_i porté par F(T_i), sont un couplage forcé entre droites. §4.2 montre qu'il ne
contredit rien.

---

## 3. Pourquoi une borne supérieure ne peut pas venir du local

**Proposition 8 (A : TL 17.40 et 17.48 ; P).**
- r ≤ 45 − m si et seulement s'il existe x₁, …, x_m ∈ E₋ dont la Gram est inversible mod 7.
- De même, r ≤ 55 − m′ si et seulement s'il existe m′ vecteurs de E₃ dont la Gram mod 7 est inversible. Pour K⁺ et
  56 − r, voir TL 17.48.

*Raison :* les Grams mod 7 se factorisent par Q_r (resp. Q′_r), et ces quotients sont non dégénérés.

**Proposition 9 (P). Tout vecteur du noyau fabriqué par les identités du srg tombe dans D.**
- Sur 1^⊥ mod 7, tout polynôme en A vaut a + bM, puisque M² = 0 sur 1^⊥.
- Soit y de somme nulle avec f(A)y = ay + bMy ∈ ker M. Alors M f(A)y = aMy = 0.
  - Si a = 0, f(A)y = bMy ∈ D.
  - Sinon My = 0 : y était déjà un vecteur du noyau, et f(A)y = ay n'apporte rien.
- Les vecteurs de noyau locaux d'une droite sont des éléments de D :
  - κ = m_t − m_{t′} ;
  - y_T − 5·1.
- Un bloc principal ne fait que minorer r : rang d'une sous-matrice ≤ rang.

**Conséquence.** Une majoration de r exige des vecteurs propres entiers, c'est-à-dire des structures spéciales, dont la
Gram est non dégénérée mod 7. Les réseaux Λ₋(T) sont forcés, mais leur Gram a exactement le 7-rang 45 − r : c'est
circulaire.

C'est la forme précise du verrou de Codex 99 §3. Ce n'est pas une impossibilité démontrée : c'est l'absence de tout
mécanisme connu.

---

## 4. Les pistes proposées, testées

### 4.1 Espaces C_T engendrés par les lignes proches (P)

- C = C_T ⊕ C(T) pour une droite générique.
- Pour deux droites par v : dim(C_{T_i} ∩ C_{T_j}) = 37 − ρ + dim(C(T_i) ∩ C(T_j)).

C'est l'énoncé dual de §2.5. Au rang 37, tous les C_T sont égaux à C. Au rang r, deux C_T génériques se coupent en
dimension 37 − ρ dans la position générale.

### 4.2 Les sept droites d'un sommet : modèle de position générale (E)

**Modèle** (`borne_rang_vertex_gp.py`, graines 1 et 2, 7 essais par rang) :
- coordonnées : les 84 labels ;
- Z est l'espace des sommes ponctuelles nulles, de dimension 70, non dégénéré pour le produit scalaire mod 7 ;
- on tire D′ ⊂ Z totalement isotrope **aléatoire**, de dimension k = r − 15 ;
- on calcule les quantités du §2.

| r | k | dim(D′ ∩ F^{F_i}) | valeur forcée dans un srg | rang sur S_i | max dim C_i ∩ C_j | dim Σ C_i | relations | borne forcée |
|---|---|---|---|---|---|---|---|---|
| 37 | 22 | 0 ; 1 pour 6 droites sur 49 | 0 si d = 1 ; 1 si d = 2 | 22 ; 21 pour ces 6 | 0 | 0 à 2 | 0 | 0 |
| 39 | 24 | 2 | 2 | 22 | 0 | 14 | 0 | 0 |
| 41 | 26 | 4 | 4 | 22 | 0 | 26 | 2 | 2 |
| 43 | 28 | 6 | 6 | 22 | 0 | 28 | 14 | 14 |

**Lecture.**
- Le modèle aléatoire reproduit exactement toutes les dimensions forcées, à chaque rang.
- Au rang 37, il produit même des « droites à torsion » (rang 21 sur S_i et dim C = 1) à la fréquence d'environ
  1/7, comme 7 | τ (14 % des G_T, Codex 99).
- **Réfuté :** l'idée que l'intersection ou la somme des C(T_i), ou une codimension ≥ 2 pour toute droite générique,
  serait incohérente.
- **Limite du modèle :** il ignore le caractère 0/1 de A₂₂. C'est précisément là que les droites meurent (couche II de
  la SYNTHESE).

### 4.3 Réseaux Λ₋(T) et réseau global E₋ (P)

- Le théorème 5 donne la seule relation : chaque Λ₋(T) se détache orthogonalement de E₋ ⊗ ℤ₇ et porte toutes les
  classes de Q_r.
- **Invariants de Hasse en 7.** Côté 3, on a Θ = Π_{θ≠3}(4 + θ) = −p′(−4) ≡ −p′(3) = −36τ ≡ −τ (mod 7), où
  p′ = χ_G/(x − 3) est à coefficients entiers. Le côté 3 ne donne donc aucune condition en 7 indépendante de L23.
  - **Vérification de cohérence au rang 37** :
    - Q′₃₇ (dimension 18) a un discriminant non carré, car E₃ a pour déterminant 11·7^(r−1), avec 11 ≡ 4 un carré, et
      sa forme discriminante est l'opposée de celle de E₋ ;
    - avec det Λ₃(T) = 5Θ/(256j′²) (RD §1) et (5|7) = −1, on obtient (Θ|7) = +1, soit (τ|7) = −1 : c'est exactement
      L23, et non une condition contraire.
  - La remarque est P (elle dépend des formules de RD, non relues) ; RD §3 ne traitait que le côté −4.
- Aux rangs ≥ 39, le type de la forme résiduelle est fixé localement par (τ|7), sans contrainte (RD §2 ; TL 17.80,
  corollaire C).

### 4.4 Comptages sur les 231 droites (P)

- Σ_T dim C(T) = 231(r − 37) si toutes les droites sont génériques, contre dim D = r − 1.
- La position générale prédit C(T) ∩ C(T′) = 0 pour deux droites quelconques.
  - D se restreint injectivement à N[T] ∪ N[T′] : 59 ou 60 coordonnées, soumises seulement aux 5 ou 6 équations des
    sommets des deux droites, contre dim D = r − 1 ≤ 42 < 54.
- Les mots sont donc nombreux et indépendants : aucune contradiction de comptage.

### 4.5 ρ ≥ 2

Aucune contradiction trouvée. Voici ce qui a été examiné.
- Les signes : déterminés localement (RD §2).
- L'indice de Witt : Λ̄_T, de dimension 26, contient C(T) totalement isotrope de dimension ρ ≤ 6 < 12.
- Le type de C(T)^⊥/C(T) ≅ Q_r ⊥ Q′_r : cohérent par simplification de Witt.
- Les traces : automatiques (A).

---

## 5. Étalonnages (E)

### 5.1 p-rang de graphes réels (`borne_rang_prank_calib.py`)

| graphe | paramètres | p | rang_p(A − rI) | min(f, g) + 1 | \|Aut\| |
|---|---|---|---|---|---|
| grille 3 × 3 (famille de Conway, k = 4) | srg(9,4,1,2) | 3 | 4 | 5 | 72 |
| Petersen | srg(10,3,0,1) | 3 | 5 | 5 | 120 |
| T(7) | srg(21,10,5,4) | 5 | 7 | 7 | 5040 |
| hémisystème FTWKB(5), graine 1 | srg(378,52,1,8) | 3 / 5 | 104 / 90 | 105 | 6 |
| graine 1, hémisystème complémentaire | idem | 3 / 5 | 104 / 90 | 105 | non mesuré |
| graine 2 | idem | 3 / 5 | 104 / 90 | 105 | non mesuré |
| graine 3 | idem | 3 / 5 | 104 / 90 | 105 | 600 |
| srg(243,22,1,2) (archive, `treasure_2026-10-19/line_modrank_243.log` ; 9 = 3² \| r − s) | | 3 | 67 (BvLS), 84, 90, 94, 95 | 111 | ≥ 108 |

**Lecture.**
- Le p-rang est à la borne de van Eijl pour Petersen et T(7), un cran dessous pour la grille et pour le 3-rang des
  hémisystèmes.
- Il est **très en dessous** dans deux cas.
  - Le 5-rang des hémisystèmes (90 sur 105) :
    - pour les quatre graphes, quel que soit |Aut| (6 ou 600) ;
    - car A + 26I = NᵀN (lignes de l'hémisystème, concourantes en un point) et 26 ≡ 1, r = 4 ≡ −1 (mod 5) ;
    - donc A − 4I ≡ NᵀN et rang₅ ≤ rang₅ N, N étant l'incidence d'un GQ construit sur GF(5).
  - BvLS (code de Golay ternaire : 67 sur 111) ; ses échanges remontent à 84–95.
- **Un p-rang bas est hérité d'une structure F_p, pas de la symétrie.**
- Pour Conway, A + 7I = N_L N_Lᵀ (incidence des droites), mais 3 ≢ −7 mod 7 : cela ne factorise pas A − 3I. On ne
  connaît aucune structure F₇.
- Rien ne suggère donc un petit 7-rang. L'heuristique de Codex 102 §9 (r = 43) n'est pas contredite.

### 5.2 Conditions de sommet valables à tout rang (`borne_rang_vertex_block.py`, `borne_rang_rank30_objects.py`)

Pour un ensemble X de labels dont toutes les adjacences sont fixées, on considère H = 7P_v[X,X] (§2.4).

**Conditions nécessaires à tout r ∈ {37, …, 43} (P)** :
- 0 ⪯ H ⪯ 7I et rang H ≤ 30 (bloc principal de 7 × un projecteur de rang 30) ;
- rang₇ Σ_v[X,X] ≤ r − 15 ≤ 28 (bloc principal de la Gram de D_v).

| objet | labels | valeurs propres de H (min / max) | nb < 0 | rang réel (≤ 30) | 7-rang (≤ 28 ; ≤ 22 au rang 37) |
|---|---|---|---|---|---|
| srg(243) BvLS, contrôle (formule locale contre complément de Schur exact : écart 0) | 220 | −6·10⁻¹⁴ / 9 | 0 | 88 = g − k | — |
| srg(243) échange aut108, contrôle (écart 0) | 220 | −4·10⁻¹⁴ / 9 | 0 | 88 | — |
| témoins SAT de R7, graines 1, 2, 4, 5 (`scratchpad/r7b`) | 51 | −1,26 à −1,03 / 6,98 à 7,17 | 8 | 47 | 47 |
| leurs bases à quatre étoiles | 44 | −0,94 à −0,80 | 5 à 6 | 40 | 39 à 40 |
| 331 objets de rang 30 de l'archive (`stars_rank_2026-10-14/rank30_psd_objects_2026-10-15.json`) | 44 | ≥ 0, ≤ 7 | 0 | 30 | 25 (127), 29 (202), 30 (2) ; l'archive est retrouvée 331/331 |

**Lecture.**
1. La formule locale est juste : elle est exacte sur deux graphes réels.
2. Les solutions combinatoires (SAT) sont spectralement très loin du réel : au mieux 47 contre 30.
3. Pour l générique, le 7-rang d'un bloc à quatre étoiles vaut 22 + rang₇(Res_l sur la double étoile de m) (A :
   NOTE_FUSION §4.1). Dans tous les cas, il est au plus r − 15 (P).
   - 204 des 331 objets sont impossibles à tout rang.
   - Les 127 autres demandent r ∈ {41, 43}, car 25 > 24.
   - **Aucun objet connu n'est compatible avec r ≤ 39.** C'est un échantillon de marches symétriques (Z5h, G1) : X.
4. **La violation n'est pas locale** (`borne_rang_minimal_nonpsd.py`, E). Dans les témoins R7 :
   - les plus petits blocs principaux non semi-définis trouvés ont 9 à 11 labels, minimaux pour le retrait d'un label ;
   - aucun bloc de 5 labels ou moins n'est mauvais (recherche exhaustive, graine 2 ; 3 labels ou moins pour les
     autres graines) ;
   - en revanche, sur les 51 labels, la valeur propre la plus basse vaut environ −1.

   Des clauses « no-good » sur des motifs de 9 à 11 labels seraient donc des coupes faibles. Il faut les coupes
   linéaires par vecteur propre (§7).

---

## 6. Bilan

**Prouvé (P).**
- Lemmes 1 à 3 : cadre (D, b), mots portés par un ensemble.
- Proposition 4 : dim C(T) = ρ + r(T) pour toute droite ; D = D_T ⊥ C(T) pour une droite générique.
- Théorème 5 : scindage orthogonal à tout rang.
- Proposition 6 : sommets, dim D_v = r − 15 partout (déjà A).
- Proposition 7 : au moins 6r − 244 relations entre les C(T_i).
- Propositions 8 et 9 : équivalence « majoration ⟺ vecteurs de Gram non dégénérée mod 7 », et aucun vecteur fabriqué
  par les identités ne sort de D.
- Côté 3 en 7 équivalent à L23.

**Calculé (E).**
- Le modèle de position générale reproduit toutes les dimensions forcées.
- Étalonnage du p-rang.
- Formule de bloc de sommet validée sur srg(243), et violations par les témoins SAT de R7.
- 7-rangs des 331 objets.

**Réfuté.**
- Une contradiction par dimensions ou intersections des C(T), aux droites d'un sommet ou sur les 231 droites (§4.2,
  §4.4).
- Une contradiction par les formes ou les signes pour ρ ≥ 2 (§4.5).
- « Le côté 3 fournit une condition en 7 de plus » (§4.3).

**Ouvert (X).**
- r = 37, ou toute majoration.
- « Tout bloc à quatre étoiles de rang réel 30 a un 7-rang ≥ 25 ». S'il était vrai, il exclurait 37 et 39, à
  l'inverse du but. Il est seulement lu sur un échantillon biaisé.
- Le rang 43 par le cadre des classes de Q₄₃ (TL 17.13, 17.22).

---

## 7. Prochaine étape la plus prometteuse

**Ne plus chercher de théorème « r = 37 » par des arguments locaux, de dimension ou de genre.** Les §3 et §4 montrent
qu'ils sont cohérents à chaque rang. L'étalonnage (§5.1) dit que le petit rang demanderait une structure F₇ cachée,
dont on ne connaît aucune trace.

**Viser un objet fini uniforme en rang autour d'un sommet** : une seule instance pour 37 à 43.
- **Modèle.** Modèle combinatoire de R7, puis de R8 (quatre étoiles exactes, plus les labels {4,t} ; A,
  REVUE_GLOBALE §8–9), plus :
  - (R) **coupes réelles valides** :
    - si z est un vecteur propre de H = H₀ − A₂₂[X,X] de valeur propre négative, la coupe linéaire
      Σ z_iz_j A_ij ≤ zᵀH₀z est satisfaite par toute vraie structure ;
    - de même pour 7I − H ;
    - un mineur 31 × 31 non nul donne une coupe de rang ;
  - (M) **7-rang ≤ 28** sur tout sous-ensemble de labels ;
  - (D) **DISC** (SQ3, A).
- **Pourquoi c'est prometteur.**
  - Les témoins SAT de R7 violent (R) et (M) de très loin (§5.2), et dès la base à quatre étoiles.
  - Les seuls objets connus qui satisfont (R) sont les 645 germes de rang 30 (A : `stars_rank_2026-10-14/EXT84_2026-10-16.md`
    §1–2).
    - Tous échouent à DISC.
    - Aucun n'accepte un seul label extérieur : les domaines de colonne de l'outil de Codex sont vides, et la norme de
      Schur n'est jamais atteinte.
  - Le mécanisme est celui-ci : dès que le bloc atteint le rang 30, chaque nouveau label est déterminé par sa ligne de
    Gram, et sa norme doit valoir la constante H_ww. C'est une équation exacte, et l'extension devient presque
    déterministe.
  - **Ce qui manque à l'archive, c'est l'exhaustivité** : les germes viennent de marches dans des familles symétriques.
    La boucle CEGAR ci-dessous est une façon de l'obtenir.
- **Plan et coût.**
  1. Contrôle positif d'abord : la même boucle sur srg(243) (k = 22, 220 labels) doit continuer à trouver les vraies
     structures. C'est la leçon de la rétractation CP du 18/10.
  2. Pilote CEGAR (CP-SAT ou cadical avec coupes PB) sur R7 : 1 à 2 min par appel SAT. Nombre d'itérations inconnu,
     d'où un pilote de 5 minutes avant toute estimation.
  3. Si R7 + (R) + (M) tombe, passer à R8 et à la cinquième étoile, avec certificat : preuve DRAT des coupes ajoutées,
     coupes vérifiées en arithmétique exacte.

  Rien n'a été lancé.

**Alternatives, moins bonnes.**
- **Test par droite uniforme en rang** : double étoile, rang réel ≤ 8 exact et 7-rang ≤ 6. Il est valable aux quatre
  rangs, mais il coûte environ 10¹⁵ nœuds par droite à ρ = 6, fois environ 10¹¹ classes : hors de portée.
- **Thêta au rang 43** : il faut 2a₈ + 16a₉ + a₁₃ ≥ 2632. Il faudrait un plafond par classe de Q₄₃ (49 classes) sur les
  vecteurs de norme 18 et 26. Deux vecteurs de norme 18 d'une même classe diffèrent d'un vecteur de √7M de norme 28, 42
  ou 56 ; la norme 14 est exclue par Codex 176. Sans borne connue.

---

## 8. Fichiers (nouveaux, dans `merge_2026-10-19/`)

| fichier | contenu |
|---|---|
| `NOTE_BORNE_RANG.md` | cette note |
| `borne_rang_vertex_gp.py`, `borne_rang_vertex_gp.log` | modèle de position générale en un sommet (§4.2) |
| `borne_rang_prank_calib.py`, `borne_rang_prank_calib.log` | p-rangs des graphes réels (§5.1) |
| `borne_rang_vertex_block.py`, `borne_rang_vertex_block.log` | bloc de sommet 7P_v : validation sur srg(243), témoins R7 (§5.2) |
| `borne_rang_rank30_objects.py`, `borne_rang_rank30_objects.log` | les 331 objets de rang 30 de l'archive (§5.2) |
| `borne_rang_minimal_nonpsd.py`, `borne_rang_minimal_nonpsd.log` | taille des plus petits blocs non semi-définis des témoins R7 (§5.2, point 4) |

**Données lues, non modifiées :**
- `work/lambda1_construction_2026-10-14/ftwkb5_data/*.edges` ;
- `work/stars_rank_2026-10-14/kreps_check/*.edges` ;
- `work/stars_rank_2026-10-14/rank30_psd_objects_2026-10-15.json` ;
- `scratchpad/r7b/r7_seed*.json`.

**Exécutions** : dans `scratchpad/boost/runs/borne_rang/`, un processus, chacune sous 5 minutes.
