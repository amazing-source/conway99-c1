# 241 — Données exactes pour la piste thêta cubique par classes

9 octobre 2026. Suite au message LAB 478 : le programme par classes modulo
neuf et pondérations paires est annoncé faisable aux rangs 37,39,41,43.
La variante cubique sur V_-4 n'a pas été exécutée. Cette note fournit des
entrées pour cette variante, sans refaire le programme de degré zéro.

**Résultats de cette note.** Une pondération cubique sur V_-4 doit être
conservée par classes ou appariée avec une pondération impaire sur A8,
sinon elle s'annule au recollement. Les premiers coefficients cubiques
dans la classe de coordonnées −1/3 sont déterminés par les profils connus.
Les reflets de triangles par les racines sont tous de profil A, avec un
triplet négatif formé d'une arête et d'un sommet isolé. Cela renforce les
bornes sur le premier coefficient distinguant les profils A,B,C.

Les séries cubiques des neuf classes de A8 sont calculées exactement
jusqu'à q^32. Le programme modulaire cubique complet n'est pas construit
ni résolu ici. **Aucun rang ni configuration supplémentaire n'est exclu.**

## 1. Annulation et choix de la pondération auxiliaire

Poser V=ker(A+4I), de dimension 44, et P(x)=Σ_(v=1)^99 x_v³ sur V.
Le projecteur E a toutes ses entrées diagonales égales à 4/9. Ainsi

    Δ_V P(x) = 6·(4/9) Σ_v x_v = 0.

P est donc harmonique. Pour des classes L_c avec −L_c=L_(-c), les séries

    H_c(q)=Σ_(x∈L_c) P(x) q^(||x||²/2)

vérifient H_(-c)=−H_c et H_0=0. Une combinaison avec des facteurs
B_(-c)=B_c, comme les thêta non pondérées ou pondérées en degré pair de
A8, donne donc identiquement Σ_c H_c B_c=0. Cela n'invalide pas une
approche vectorielle gardant les classes séparées.

Pour un recollement scalaire, prendre plutôt sur
W={y∈R^9:Σy_j=0} le polynôme

    Q(y)=Σ_j y_j³.

Il est harmonique car Δ_W Q=6·(8/9)Σy_j=0. Ses séries de classes A8
sont impaires elles aussi. Le produit P(x)Q(y) est un polynôme harmonique
de degré six sur V⊕W : le laplacien de la somme orthogonale annule chaque
facteur séparément. Il est pair sous (x,y)↦(−x,−y), et n'est donc plus
annulé par cette symétrie.

Les poids associés sont 22+3=25 côté V, 4+3=7 côté A8, et **32** pour le
produit sur les 52 dimensions du recollement. C'est le poids à employer
si l'on adopte cette construction scalaire ; le niveau, le caractère et
la transformation exacte entre les deux cuspides doivent être ceux du
recollement effectivement choisi, pas être supposés par analogie.

La règle générale pour les thêta harmoniques et l'annulation en degré
impair sont exposées dans Elkies–Kominers, *Weighted Generating Functions
for Type II Lattices and Codes*, théorème 2.6 et discussion suivant sa
preuve : <https://arxiv.org/pdf/1111.2392>. Ici les annulations et les
harmonicités utiles sont également démontrées directement ci-dessus.

## 2. Séries cubiques de A8, avec une convention explicite

La classe k est paramétrée par

    y=m−(k/9)1,  m∈Z^9,  Σm_j=k,  0≤k≤8.

Si S=Σm_j² et C=Σm_j³, alors

    ||y||² = S−k²/9,
    Q(y) = C−kS/3+2k³/81.

Le script accumule exactement le nombre de tuples et la somme de leurs
cubes par (Σm_j,Σm_j²). Les coefficients archivés sont ceux de **81Q**,
donc tous entiers. Le premier terme de la classe k≠0 a exposant
k(9−k)/18, multiplicité binom(9,k), et coefficient cubique non normalisé

    binom(9,k) · k(9−k)(9−2k)/81.

Pour k=1,2,3,4, ces coefficients valent respectivement

    56/9, 280/9, 56, 280/9.

Les classes 8,7,6,5 ont les coefficients opposés aux mêmes exposants.
La classe zéro est identiquement nulle. Ces relations sont aussi
contrôlées sur toute la troncature q^32. L'identification entre l'indice
c du réseau C1 et l'indice k de A8 dépend du recollement : le fichier
fournit les classes séparées et ne fixe pas cette identification.

## 3. Coefficients de la classe de coordonnées −1/3 dans L1

On utilise les classifications déjà prouvées aux notes 178 et 191.
Écrire x=φ−(1/3)1 avec Σφ=33 et ||x||²=R. Alors

    P(x)=Σφ_v³−R−11/3.

Pour les normes 22,24,26, le profil est φ=1_S−1_T, avec
|S|−|T|=33 ; sa somme de cubes vaut donc 33. À la norme 28, les trois
profils A,B,C donnent les valeurs suivantes :

| Norme R | Profil | 3P(x) |
|---|---|---:|
| 22 | 33 valeurs +1 dans φ | 22 |
| 24 | 34 valeurs +1, une −1 | 16 |
| 26 | 35 valeurs +1, deux −1 | 10 |
| 28 | A : 36 valeurs +1, trois −1 | 4 |
| 28 | B : 33 valeurs +1, une +2, deux −1 | 22 |
| 28 | C : 35 valeurs +1, une −2 | −14 |

Soit N_j le nombre de vecteurs de norme 2j dans cette **seule classe**,
et D_j la somme de 3P sur cette couche. Il s'agit de la classe de résidu
6 modulo neuf dans la convention « coordonnées c/9 ». Alors

    D_11=22 N_11,  D_12=16 N_12,  D_13=10 N_13,
    D_14=4 N_A+22 N_B−14 N_C
        =4 N_14+18(N_B−N_C).                         (1)

Ces coefficients sont signés ; on ne peut pas leur imposer globalement
la positivité des coefficients d'une thêta non pondérée. La classe +1/3
porte les valeurs opposées. Les coefficients de la série non séparée
sur tout L1 s'annulent.

## 4. Reflets triangulaires : toujours un profil A avec une arête négative

Soit g=1_P−1_Q=√7r, où r est une racine de M. Les deux supports ont
taille sept. Leurs sommets ont quatre voisins dans l'autre support.
Tout sommet extérieur au support est soit sans voisin dans P∪Q, soit
adjacent à exactement un point de P et un point de Q (notes 165–176).

Prendre un triangle T non orthogonal à r et orienter g pour que g(T)=1.
Alors T={p,a,b}, avec p∈P et a,b hors de P∪Q. Poser S=N(T)\T, de taille 36,
et f_T=7E1_T. Le vecteur −f_T est dans la classe −1/3 et s'écrit

    −f_T = 1_S−1_T−(1/3)1.

Le reflet de −f_T par r, après le même changement d'échelle, est

    x=−f_T+g.

Les six points de P\{p} ne touchent aucun point de T : a et b ont déjà
p comme unique voisin dans P. Le sommet p a quatre voisins dans Q.
Les voisins q_a,q_b de a,b dans Q sont distincts l'un de l'autre et des
quatre voisins de p : autrement une arête de T aurait un second troisième
point de triangle. Exactement six points de Q sont donc dans S. Noter q
le septième, qui ne touche aucun sommet de T.

Dans la partie entière φ de x, p passe de −1 à 0, les six points de
P\{p} passent de 0 à 1, six points de Q passent de 1 à 0, et q passe de
0 à −1. Le triplet négatif est exactement **{a,b,q}**, où ab est une
arête et q est isolé de a,b. Il reste 36 coordonnées +1. Ainsi x est
toujours de type A, avec P(x)=4/3, et jamais de type B ou C.

Avec k lignes de racines dans M, les comptages sans doublon de la note
191 donnent 42k tels reflets dans cette classe. Ils sont distincts des
231 vecteurs −f_T, dont le triplet négatif est un triangle. Par conséquent

    N_A ≥ 231+42k.                                    (2)

## 5. Inégalités prêtes à intégrer au programme impair

Soit C22 le nombre de cocliques de taille 22. La bijection de la note 192
donne N_C=22 C22 dans la classe −1/3, à tous les rangs pour L1. Les
équations (1)–(2) imposent

    D_14 = 4N_14+18N_B−396 C22,
    4N_14−396 C22 ≤ D_14
        ≤ 22N_14−4158−756k−792 C22,
    D_14 ≡ 4N_14 (mod 18).

Sans coclique de taille 22, cela donne notamment

    4N_14 ≤ D_14 ≤ 22N_14−4158,
    D_14 ≥ 924.

Cette absence entraîne également k=0 par la note 192. Ces contraintes
portent sur les coefficients signés, reliés aux nombres de vecteurs et
aux objets géométriques ; elles ne remplacent pas la construction de
l'espace modulaire ni sa résolution.

## 6. Artefacts et limites

    python code/codex/odd_theta_inputs.py

Le calcul exact, bibliothèque standard Python seulement, produit
`data/codex_odd_theta_inputs.json` : six poids de profils, neuf séries
cubiques A8 jusqu'à q^32, conventions de normalisation et inégalités.
Il n'emploie ni solveur ni matrice d'un hypothétique graphe à 99 sommets.
La preuve géométrique du §4 est portée par le texte, pas par ce calcul.

Le message 478 rapporte aussi que le filtrage de second niveau des rubans
six avec triangle de centres laisse 279 masques et un LP faisable pour
chaque fermeture. Ce niveau n'a pas été relancé. Le programme par classes
de degré zéro annoncé par LAP, commit a07172a4d, laisse les quatre rangs
37,39,41,43 ouverts, même avec les huit absences combinées indiquées.
Ces résultats de pairs sont conservés avec leur portée ; cette note ne
leur substitue aucune nouvelle affirmation d'infaisabilité.
