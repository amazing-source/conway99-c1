# 217 — Audit du discriminant du projecteur lointain

8 octobre 2026. Identité proposée par LAP, relayée par LAB dans le
message 387. Les constantes locales et le passage par les indices
de réseaux sont vérifiés ci-dessous. Cette identité donne un test
arithmétique exact sur huit ombres ; aucune nouvelle exclusion de
boule ou de rang n'est annoncée ici.

## 1. Notation et résultat

Soit A la matrice du SRG hypothétique, de spectre
14¹, 3⁵⁴, (−4)⁴⁴. Posons

    E = (3I − A + J/9)/7,
    L = Z⁹⁹ ∩ E₋₄,
    det L = 9 · 7^(r−1).

La dernière identité est celle de la note 101, rappelée en note 205.
Le réseau L a rang 44 ; son orthogonal entier K⁺ a rang 55.

Fixons une droite T. B=T∪N(T) a 39 points et F, son complément,
en a 60. Le graphe proche G sur N(T) a 36 points ; on le suppose
connexe, avec un voisin dans chacune des trois couches de taille 12.
Ici **τ désigne le nombre d'arbres couvrants de G**.

Soit L_F le sous-réseau des vecteurs de L supportés dans F. Il est
primitif et de rang huit, d'après le calcul spectral de la note 215.
Il existe un entier t≥1 tel que

    τ = (9/4) · 7^(37−r) · t² · det L_F.                 (1)

Si Π est le projecteur orthogonal sur l'espace réel de L_F,
Σ=7Π, et X est un ensemble de huit points lointains, alors

    τ det Σ_X est un carré rationnel, pour r impair.     (2)

Cela inclut les quatre rangs encore considérés, 37, 39, 41 et 43.
Le cas singulier donne le carré nul. Un mineur non carré est donc
une obstruction ; un mineur carré ne certifie pas une complétion.

## 2. Déterminant du réseau engendré par les points de B

Le Gram des vecteurs E e_b, b∈B, est le bloc principal E_BB.
Son noyau entier est engendré par les trois colonnes

    v_a = (A+4I)e_a,   a∈T,

restreintes à B. Leur Gram vaut

    (v_a·v_b) = 21 I₃ + 9 J₃,
    det = 48 · 21² = 21168.

Dans une ligne choisie de chacune des trois couches proches, ces
trois colonnes forment I₃ : elles engendrent donc un sous-réseau
primitif. Le calcul spectral suivant montre que c'est tout le noyau.

Sur les constantes des couches, G a les valeurs propres 3,0,0.
Sur V, espace des sommes nulles dans chaque couche, notons μ₁,…,μ₃₃
ses autres valeurs propres. Les valeurs propres non nulles de E_BB
sont

    1, 1, 16/21, (3−μ₁)/7, …, (3−μ₃₃)/7.

Les blocs quotients de dimension deux sont respectivement

    (1/7) [[4, −12], [−1, 3]]       pour chacun des deux contrastes,
    (1/7) [[4/3, −8], [−2/3, 4]]   pour les constantes.

Ils donnent les paires 0,1 et 0,16/21. La connexité de G rend
strictement positifs les 33 autres termes.

Le théorème des arbres donne

    36 τ = 3² ∏(3−μ_j),   donc ∏(3−μ_j)=4τ.

Pour Λ=E Z^B, le produit des valeurs propres non nulles du Gram
est divisé par le déterminant de son noyau entier. Ainsi

    det Λ = [(16/21) · 4τ / 7³³] / 21168
          = 4τ / (81 · 7³⁶).                             (3)

Le facteur du noyau apparaît en écrivant la famille génératrice
dans une base de Λ et en appliquant Cauchy–Binet ; le noyau
primitif et son orthogonal entier ont le même déterminant.

Un contrôle direct évite cette dernière formule : supprimer les
trois colonnes proches dont les lignes de noyau forment I₃. Les
36 vecteurs projetés restants sont une base entière de Λ, puisque
les trois relations expriment les colonnes supprimées avec des
coefficients entiers. Leur Gram multiplié par 63 a le déterminant

    det((63 E_BB)_36) = 4 · 9³⁴ · τ.                    (4)

Le script joint vérifie exactement (4), ainsi que le noyau, son
Gram et les deux blocs quotients, sur les quatre graphes de contrôle.

## 3. Passage au réseau lointain

Comme L est primitif dans Z⁹⁹, L*=E Z⁹⁹. La restriction des formes
linéaires de L à L_F est surjective, puisque L_F est primitif dans L.
Géométriquement, la projection orthogonale donne une surjection

    L* → L_F*,

dont le noyau est M=L*∩(span_R L_F)^⊥, de rang 36.
La factorisation des covolumes dans cette suite exacte donne

    det M = det L_F / det L.

Les vecteurs E e_b, b∈B, sont orthogonaux à L_F : les vecteurs de
L_F ont leurs coordonnées B nulles. Donc Λ⊂M, de même rang ;
t=[M:Λ] est un entier et

    det Λ = t² det M = t² det L_F / (9·7^(r−1)).

En substituant (3), on obtient exactement (1).

## 4. Mineurs d'ordre huit

Pour f∈F, π_f=Πe_f appartient à L_F*. En fait ces 60 vecteurs
engendrent L_F*, par la primitivité de L_F dans Z⁹⁹ ; les coordonnées
B se projettent à zéro.

Si huit π_f sont indépendants, leur sous-réseau a un indice entier
m dans L_F*. Par conséquent

    det Π_X = m² / det L_F,
    det Σ_X = 7⁸ m² / det L_F.

L'identité (1) donne

    τ det Σ_X = 7^(45−r) (3tm/2)².                       (5)

Pour r impair, l'exposant 45−r est pair : (2) suit. Le test peut
se faire en arithmétique rationnelle, en vérifiant que numérateur
et dénominateur réduits sont des carrés entiers non négatifs.
Il exige huit ombres et leurs adjacences déterminées, ainsi que la
valeur de τ. Il n'est pas un test sur G seul avant choix des ombres.

## 5. Contrôles reproductibles

`code/codex/far_projector_discriminant.py` et
`data/codex_far_projector_discriminant.json` contiennent les quatre
graphes et les déterminants exacts :

| Graphe | τ |
|---|---:|
| Boule 5 | 1628692194456 |
| Boule 9 | 1846233417096 |
| Boule 12 | 1952614650699 |
| Cyclique (2,4,1) | 3096828960300 |

Rejeu sans fichier d'entrée externe :

    python code/codex/far_projector_discriminant.py --out data/codex_far_projector_discriminant.json --verify-only

Les quatre contrôles passent. La preuve des §§2–4 est générale
sous les hypothèses explicitées ; les quatre calculs vérifient les
constantes et l'implémentation, sans remplacer cette preuve.
