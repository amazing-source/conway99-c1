# 242 — Rang 43 : les racines forcent des couches courtes

9 octobre 2026. Codex, exploitation des messages LAB 485 et 487.

**Résultat nouveau.** Au rang 43, s'il existe une racine dans M, les
cardinaux a_j des couches de norme 2j de L1 satisfont

    10 a8 + 2 a9 + 5 a10 + 2 a11 + a12 >= 328.                 (1)

En particulier, **l'absence des normes 16,18,20,22,24 force l'absence de
racines**. Les deux possibilités résiduelles k=1 et k=2 de la note 177
§8 sont ainsi exclues dans cette branche. Il reste k=0, avec 329 vecteurs
dans chacune des huit classes de norme 26. Ce résultat n'exclut ni la
branche sans racines ni le rang 43 entier.

La preuve combine une identité de moments quadratiques avec les
reflets triangulaires déjà établis dans la note 191. Elle donne aussi
une restriction plus forte, relative à chaque racine, à la fin du §4.

## 1. Conventions et données utilisées

On travaille dans V=V_-4, de dimension 44, avec les réseaux L1 et
M=sqrt(7) L1*, et au rang 43. Le déterminant de L1 vaut 7^42.
Pour une couche X, poser

    T(X) = sum_(x in X) x x^t,
    D(X) = T(X) - (sum_(x in X) ||x||² / 44) I.

Toutes les couches comprennent les deux signes. Écrire W_j=T(L1[2j]),
V_j=T(M[2j]), et H_j, R_j pour leurs parties sans trace respectives.
Le nombre de racines de M est b1=2k ; elles sont ±r_i, de norme deux,
deux à deux orthogonales (note 176).

L'anisotropie du quotient à 49 classes implique l'égalité d'ensembles

    L1[14j] = sqrt(7) M[2j].

Ainsi a_(7j)=b_j et H_(7j)=7 R_j. Les identités scalaires de la note 191
donnent, sans hypothèse d'absence supplémentaire,

    a13 = 2632+112k-2a8-16a9+7a10+2a11+a12,
    b2  = 1000-16k+25a8+11a9+8a10+3a11+a12.                 (2)

Les 462 vecteurs signés de triangles sont dans M[4]. Leur second
moment est **42 I**. Le coefficient 21 concerne les 231 représentants
non signés : NN^t=7I+A, donc 7 E NN^t E=21 E, où E projette sur V.

## 2. Une identité harmonique explicite

Le message 485 de LAB utilise les thêtas harmoniques de degré deux,
de poids 24 sur Gamma0(7), caractère trivial. Pour une matrice symétrique
S de trace nulle, poser P(x)=x^t S x. Le calcul ci-dessous donne

    H13 + 3 H12 + 4 H11 + 7 H10 + 6 H9 + 12 H8
        + 14 R2 + 728 R1 = 0.                              (3)

LAP fournit la même relation par son calcul de classes, relayé au
message 487, commit bd27d407c, fichiers w49evenk.py et s0_tensor.py.
La conséquence géométrique (1) est obtenue ici en exploitant cette
relation. Voici également une dérivation courte avec des êta-quotients.

### Base, signe et coefficients

Prendre

    F_j = eta(tau)^(4j) eta(7 tau)^(48-4j),  -1 <= j <= 13.

Les critères des êta-quotients donnent un poids 24, un caractère trivial
et des ordres aux deux pointes égaux à 14-j et j+2. Ils sont tous
strictement positifs. Les conditions et la formule des ordres sont
énoncées dans [Rouse–Webb, §1](https://arxiv.org/pdf/1311.1460).
Les quinze ordres à l'infini sont distincts. La formule de valence donne
ord_inf+ord_0<=16 ; les quinze premiers coefficients déterminent donc
une forme parabolique. Les F_j constituent une base.

Pour l'opérateur de Fricke normalisé au poids 24,

    F_j | W7 = 7^(2j-12) F_(12-j),
    Theta_M,P = -7^10 (Theta_L1,P | W7).                    (4)

Pour préciser le signe, Poisson pondéré donne
Theta_L1,P(-1/z)=-z^24 7^-21 Theta_L1*,P(z), car i^-22=-1.
Le changement x -> sqrt(7)x multiplie P par sept. Cela donne (4).
La modularité des thêtas harmoniques relève du cadre classique présenté
par [Elkies–Kominers, §2](https://arxiv.org/pdf/1111.2392) ; les facteurs
de cette normalisation sont calculés ici.

Écrire Theta_L1,P=sum c_j F_j. Le minimum connu de L1 est au moins 14,
donc c_j=0 pour j>=8. Désigner par R,D,X les coefficients de P sur
M[2], M[4], L1[26], et par h8,...,h12 ceux sur L1[16],...,L1[24].
L'égalité des couches donne le coefficient 7R à q^7 et 7D à q^14.
L'élimination triangulaire des coefficients q^7,...,q^14 fournit

    c0 = 364R + 48h8 + 24h9 + 28h10 + 16h11 + 12h12 + 4X + 7D.

En revanche (4), le premier coefficient de F13=q-52q²+... et celui
de F12=q²+... donnent

    c_-1=-2401R,    c0=-2548R-49D.

Soustraire et diviser par quatre donne (3), pour tout S, donc comme
identité de matrices sans trace. Le script associé conserve ce calcul
exact et un contrôle de normalisation sur E8^5 orthogonal H7^2.

## 3. Passage aux moments positifs

Restaurer les traces dans (3), puis utiliser (2). On obtient

    W13 + 3W12 + 4W11 + 7W10 + 6W9 + 12W8
        + 14V2 + 728V1 = C I,                              (5)

où

    C = 2828 + 112k + 35a8 + 7a9 + (35/2)a10 + 7a11 + (7/2)a12.

Chaque terme de gauche est positif semi-défini. C'est cette positivité,
appliquée dans une direction de racine, qui fournit l'exclusion.

### Preuve courte dans la branche sans normes 16 à 24

Dans cette branche, C=2828+112k. Si r est une racine et e=r/sqrt(2),
alors V1[e,e]=4 et V2[e,e]>=42 par les triangles. Ainsi (5) impose

    3500 <= 2828+112k, donc k>=6.

Or le comptage déjà acquis dans la note 177 §8 donne k<=2 dans cette
branche. Une racine est donc impossible. Les écarts de positivité sont
560 pour k=1 et 448 pour k=2.

## 4. Une borne uniforme dès qu'une racine existe

La note 191 §2 donne une meilleure minoration dans la direction e.
Les 42 triangles non orthogonaux à r, avec les deux signes, apportent
42 au moment V2[e,e]. Leurs 84 reflets distincts apportent encore 42.
Pour chaque autre ligne de racines ±s, les quatre vecteurs ±r±s
apportent huit. Tous ces vecteurs sont distincts. Donc

    V2[e,e] >= 84+8(k-1).

En ne gardant que V1 et V2 dans (5), on obtient

    C >= 728*4 + 14(84+8(k-1)) = 3976+112k.

Les termes en k s'éliminent. Il reste

    35a8+7a9+(35/2)a10+7a11+(7/2)a12 >= 1148,

ce qui est exactement (1). Cette preuve ne nécessite pas k<=2.
Les cardinaux comptent les deux signes ; en nombre de paires ±x,
le second membre de (1) devient 164.

**Version relative à une racine.** Pour 8<=j<=13, soit n_j(r) le
nombre de vecteurs de L1[2j] non orthogonaux à r. On a g=sqrt(7)r
dans 7L1*, donc (x,r)=sqrt(7)p avec p entier. Puisque x±g sont non
nuls, leur norme est au moins 14. Pour ||x||²<=26, cela donne
|p|<=1. Ainsi W_j[e,e]=(7/2)n_j(r) exactement. En conservant aussi
ces moments dans (5),

    10a8+2a9+5a10+2a11+a12
      >= 328+12n8(r)+6n9(r)+7n10(r)+4n11(r)+3n12(r)+n13(r). (6)

Ce filtre combine nombres de vecteurs et incidence avec chaque racine.
Par exemple, si seule la norme 18 est présente parmi 16 à 24, il faut
au moins 164 vecteurs de norme 18, avant même le terme supplémentaire
de (6). Ces seuils sont nécessaires, pas annoncés atteints.

## 5. Le cas sans racines : un tenseur pour les couches totales

Supposons maintenant a7=...=a12=0. Il reste a13=2632 et b2=1000.
L'annulation à l'infini et l'absence de racines donnent
Theta_L1,P=c1 F1+c0 F0. Si D=R2, la relation (3) et Fricke imposent

    Theta_L1,P = (-14F1-49F0) P(D),
    Theta_M,P  = (F12+14F11) P(D),

où P(D) désigne ici la contraction trace(S D). En notation tensorielle,

    H13=-14D, H14=7D,
    R2=D, R3=-34D, R4=464D, R5=-2412D, R6=-15108D.

Ainsi les deux tenseurs des couches M[4] et M[6] laissés par le premier
argument de valence sont liés. **Toutes les couches totales dépendent
d'un seul tenseur sans trace.** Cela ne signifie pas que les moments
de chacune des classes sont tous déterminés par un seul tenseur.

Soit F_ex le second moment des 538 vecteurs de M[4] autres que les
462 vecteurs signés des triangles. Le rétablissement des traces donne

    W13 + 14 F_ex = 2240 I,                                (7)
    V3  + 34 F_ex = 1453760 I.

En particulier 0<=F_ex<=160I. La note 177 montre que W13 ne peut être
isotrope ; D est donc non nul dans une éventuelle réalisation.
LAP a indépendamment obtenu les mêmes relations globales (message 487).
Son raffinement par classes donne, pour chaque paire de classes de
norme 26 orthogonales dans le plan discriminant,

    T(C)+T(C') = 560 I - (7/2) F_ex.                        (8)

Le calcul par classes, son information supplémentaire et ses données
restent attribués à LAP ; ils ne sont pas reproduits ici.

## 6. Reproduction et limite

    python code/codex/theta7_degree2_reduction.py

Le programme utilise la bibliothèque standard, des fractions exactes
et la récurrence des produits êta déjà disponible. Il génère
data/codex_theta7_degree2_reduction.json : coefficients de (3), traces,
budget de racine, transferts du cas sans racines, et un contrôle Fricke
sur le réseau positif E8^5 orthogonal H7^2 jusqu'à q^32. Il ne relance
aucun calcul par classes, aucun LP, aucune recherche de graphes.

La nouveauté utile est (1)/(6) et la suppression effective des racines
dans la branche sans normes 16 à 24. Le cas k=0 reste à exclure : (7)
et (8) sont des contraintes sur les 538 vecteurs supplémentaires,
elles ne démontrent pas encore leur impossibilité. Aucun rang global,
aucun nouveau noyau à douze sommets, aucun cas de ruban n'est exclu ici.
