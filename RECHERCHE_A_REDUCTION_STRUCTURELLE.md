# Recherche A — support obligatoire et reconstruction

## Reprise directe et résultats obtenus

L'utilisateur a demandé directement de poursuivre l'étape binaire :
« bah tente de la resoudre cette etape alors pourquoi t'arreter ».
Cette reprise remplace l'attente d'une instruction directe consignée
après le message LAB 450. La priorité reste les lemmes de réduction.

Deux théorèmes ont été obtenus depuis l'essai initial ci-dessous :

- [Note 232](notes/232_CODEX_RIGIDITE_BINAIRE_LAPLACIEN.md) : si une
  boule générique et ses 60 ombres admettent une complétion de rang 37,
  elle est unique parmi **tous** les rangs. Le carré modulaire de la
  différence devient un laplacien entier ; les profils distincts
  forcent sa nullité. Preuve sans calcul de classification.
- [Note 233](notes/233_CODEX_DIFFERENCE_RANG4_IMPOSSIBLE.md) : deux
  complétions distinctes des mêmes ombres ne peuvent avoir une
  différence de rang au plus quatre sur F7. Cela ferme le cas (39,39)
  lorsque le bloc proche est inversible. La preuve combine un lemme
  de distance six des ombres avec un calcul exact sur quatre petits
  supports de différence, de 14 à 18 sommets. Les certificats entiers
  et rationnels sont enregistrés ; aucun statut de solveur flottant
  n'est utilisé comme preuve d'exclusion.

Ces résultats contrôlent de vraies complétions binaires, contrairement
au premier essai pondéré. Ils ne prouvent pas l'existence ou l'absence
d'une première complétion et ne ferment aucun rang global ni C1.
Le contrôle des différences de rang cinq ou six et l'existence des
données (G,N) restent ouverts. Aucun ancien balayage n'a été repris.

## Quadrilatère : connexité des murs opposés

Suite au message LAB 460, la [note 234](notes/234_CODEX_CONNEXITE_MURS_OPPOSES.md)
prouve que les deux graphes sur vingt sommets formés par les murs opposés
d'un quadrilatère sont toujours connexes, sans rang ni généricité. Les
identités entières des degrés extérieurs excluent les composantes cubiques
de tailles 8, 12, 16, ainsi que la taille 8 de déficit 2 ; la parité et le
budget total de déficit excluent alors toutes les partitions déconnectées.
Preuve transmise aux pairs au message 463, sans demande d'audit en double.

Correction préalable, transmise au message 461 et acceptée par LAB au 462 :
les quarante voisins simples ne sont 5-réguliers que si les quatre points
spéciaux sont appariés par deux arêtes. En général leurs degrés valent
`5−2e_x`, où `e_x` compte leurs voisins spéciaux. Les modèles doivent
conserver ces défauts.

Le nouvel obstacle franchi concerne des structures locales déconnectées ;
aucun rang global ni C1 n'est exclu. Il reste à contraindre les deux
structures connexes sur vingt sommets et leur couplage. Le message 462 de
LAP apporte séparément un scindage entier au rang 37 générique, qui n'est
pas utilisé ici.

Deux pistes très courtes n'ont pas donné d'obstruction : les profils
locaux où les deux arêtes entre spéciaux ont des troisièmes points distincts
passent encore les premiers tests spectraux ; la relaxation spectrale
ordinaire des graphes 5-réguliers est trop large pour exclure quarante
sommets. Ne pas transformer ces essais en nouvelles campagnes d'audit.

## Exploitation du dossier Convergences

L'utilisateur a fourni `DOSSIER_C1_CONVERGENCES.zip` et demandé d'en
tirer des conséquences avec notre contexte. La [note 235](notes/235_CODEX_EXPLOITATION_CONVERGENCES.md)
attribue le théorème des témoins de bord au dossier et établit :

- son application inconditionnelle au motif Makhnev de six points,
  avec projection totale et orthogonal de rang 38 ;
- son extension à tout support induit 4-régulier de douze points,
  avec exclusion de la valeur propre trois pour le support ;
- quatre formes nécessaires pour les collisions `H→h_H`, avec
  intersection d'au plus trois sommets entre supports distincts.

Les deux premières extensions sont théoriques. Le calcul associé
établit le Gram de rang six et énumère 4095 sous-ensembles propres de
chacun des deux supports explicites pour la dernière. Il ne rejoue
pas les vérifications du dossier, ni ses LP faisables. Le recollement
de rang 32 pour Cube/Wagner reste un apport extérieur, conditionnel
à leur présence ; aucune existence obligatoire d'un cycle de transport
de longueur quatre n'est ajoutée. LAB prend la piste complémentaire
des cycles longs (message 466).

## Premier essai, conservé comme historique

9 octobre 2026. Révision consultée :
`19ec31644888d3787d26015230d05a316dd946ee`.

Cet essai initial était un travail théorique dans le cadre de la demande antérieure de rechercher
des réductions de C1. Le message de pair 453 propose ce mandat ; il
n'est pas traité comme une nouvelle autorisation de calcul. Aucun
balayage, solveur ou calcul de recherche n'a été lancé pour cette note.

## Question effectivement attaquée et résultat

Objet candidat : le voisinage fermé d'un sommet, muni des 84 étiquettes
extérieures obligatoires. Le lemme d'existence est acquis (note 00, F3).
Le lemme de contrôle souhaité serait que ces données permettent de
reconstruire les adjacences extérieures, par les identités spectrales.

**La version réelle de ce lemme de contrôle est fausse.** On construit
ci-dessous au moins dix millions de matrices réelles distinctes sur
les mêmes sommets étiquetés, ayant exactement la même étoile enracinée
et les mêmes incidences vers celle-ci, et satisfaisant

    A = A^t,  diag(A) = 0,  A1 = 14·1,
    A² + A = 12I + 2J.

Elles ont toutes des entrées négatives : ce ne sont pas des graphes.
Le nombre de matrices ne dénombre pas des classes d'isomorphisme.
Ce résultat ne falsifie pas une éventuelle unicité des complétions
**binaires**. Il montre précisément pourquoi ce contrôle ne peut être
obtenu en supprimant leurs contraintes d'entrées.

**Effet de cet essai initial sur C1 : aucune exclusion, aucune réduction substantielle.**
Le verrou binaire reste entier. La tentative ne justifie ni une
nouvelle campagne spectrale ni une nouvelle classification finie.

Résultat antérieur le plus proche : notes 00 F4 et 157 §2.2–2.3,
décomposition du sous-constituant extérieur et projecteur de rang 30.
Cette décomposition et la reconstruction par un support de 45 sommets
ne sont pas nouvelles. L'apport de cette tentative est uniquement un
témoin explicite de la liberté de la relaxation réelle, diagonale
nulle comprise ; ce n'est pas un nouvel obstacle franchi vers C1.

## 1. Le bloc extérieur et son espace libre

Écrire les voisins de la racine comme `i+`, `i−`, pour `1≤i≤7`.
Les 84 étiquettes sont `(ij,ε,δ)`, avec `i<j` et `ε,δ∈{−1,1}`.
Soit B leur matrice d'incidence avec les 14 voisins, et M la matrice
des sept paires de voisins. Alors

    BB^t = 11I + J − M.

Sur R^14, posons

    S = (I+M)/2 − J/14,   D = (I−M)/2.

Les projecteurs orthogonaux sur les trois parties de im(B^t) sont

    E0 = J84/84,   Es = B^t S B / 10,   Ea = B^t D B / 12.

Leurs rangs sont 1, 6, 7. Leurs diagonales constantes sont
respectivement 1/84, 1/14, 1/12. Ainsi

    K = I − E0 − Es − Ea

projette sur ker(B), de dimension 70, et a diagonale 5/6.

Pour tout projecteur orthogonal P de rang 40 dans ker(B), ayant
diagonale constante 10/21, définir

    C = 12E0 − 2Es − 4K + 7P.

On a immédiatement diag(C)=0, C1=12·1 et

    BC = 2J − (I+M)B,
    C²+C = 12I + 2J − B^tB.

Pour la seconde identité, vérifier sur les quatre espaces orthogonaux
E0, Es, Ea, K : les deux membres y valent respectivement 156, 2, 0,
12. Sur K, C a pour valeurs 3 et −4, puisque P²=P.

La matrice complète

            [ 0    1^t   0 ]
    A(P) =  [ 1     M    B ]
            [ 0    B^t   C ]

est donc symétrique, de diagonale nulle, de sommes de lignes 14 et
satisfait exactement A(P)²+A(P)=12I+2J. Les autres blocs se vérifient
directement avec M²=I, B1=12·1 et B^t1=2·1.

## 2. Construction explicite de P

Sur les quatre étiquettes d'une paire ij, prendre la base orthonormée
des quatre fonctions `1/2`, `ε/2`, `δ/2`, `εδ/2`, nulles ailleurs.
Noter respectivement ces vecteurs e00_ij, ei_ij, ej_ij, e11_ij.

Les deux lignes de B associées à i sont

    somme_(j≠i) (e00_ij + ei_ij),
    somme_(j≠i) (e00_ij − ei_ij).

L'espace engendré par les six ei_ij pour i fixé est orthogonal aux
espaces analogues des autres indices. Sa partie contenue dans ker(B)
est l'hyperplan de somme nulle, de dimension cinq. Tous les e11_ij
sont dans ker(B) et orthogonaux à ces sept espaces.

Pour chaque i, choisir un vecteur s_i∈{−1,1}^6 comportant trois signes
de chaque sorte. Sur les six coordonnées ei_ij, prendre le projecteur

    F_i = I6 − (11^t + s_i s_i^t)/6.

Il a rang quatre, diagonale 2/3, et image dans ker(B).
La somme orthogonale des sept F_i a rang 28. Sa diagonale dans les
84 coordonnées initiales vaut 1/3 : une étiquette ij reçoit 1/6
de l'espace i et 1/6 de l'espace j.

Il reste à prendre sur les 21 coordonnées e11_ij un projecteur Q de
rang 12 et de diagonale 4/7. En ordonnant arbitrairement ces coordonnées
en trois groupes de sept, choisir dans chaque groupe le projecteur
réel sur les modes de Fourier 1 et 2, chacun avec sinus et cosinus :

    (Q7)_ab = (2/7)[cos(2π(a−b)/7) + cos(4π(a−b)/7)],
    a,b∈{0,…,6},
    Q = diag(Q7,Q7,Q7).

L'orthogonalité des modes montre Q7²=Q7, rang(Q7)=4 et
diag(Q7)=4/7. Dans les 84 coordonnées initiales, la diagonale de Q
vaut (1/4)(4/7)=1/7.

La somme orthogonale de Q et des F_i fournit donc P, de rang
12+7·4=40, avec diagonale 1/3+1/7=10/21, comme requis.

Chaque choix s_i est identifié à son opposé : il y a
C(6,3)/2=10 projecteurs F_i distincts. Les sept choix indépendants
donnent 10^7 projecteurs P, donc autant de matrices A(P) distinctes
sur les sommets étiquetés.

## 3. Où ces témoins échouent exactement

Considérons les deux étiquettes `(ij,+,+)` et `(ij,−,−)`.
Entre ces deux coordonnées,

    (E0)_uv = 1/84,  (Es)_uv = 1/14,  (Ea)_uv = −1/12.

Ainsi K_uv=0 et (12E0−2Es)_uv=0. Les deux contributions des espaces
mixtes i et j à P_uv valent chacune −1/6, tandis que la contribution
doublement impaire vaut 1/7. Par conséquent

    P_uv = −1/3 + 1/7 = −4/21,
    C_uv = −4/3.

Cette violation est exacte et indépendante des sept choix s_i.
La construction satisfait même les deux positivités spectrales
27I−9A+J≥0 et 44I+11A−2J≥0 : elles découlent de l'identité quadratique,
de la régularité et du spectre 14^1,3^54,(−4)^44. Elle échoue déjà à
la non-négativité des entrées, bien avant la construction d'un graphe.

Conclusion de la tentative : le petit objet enraciné est obligatoire,
mais aucun lemme de contrôle de ses réalisations binaires n'a été
obtenu. Cette note ne modifie pas l'état des 174 noyaux ni des quatre
rangs encore ouverts.
