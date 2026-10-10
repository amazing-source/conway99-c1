# 254 — Cadre compact et réduction spectrale exacte des incidences de norme 16

10 octobre 2026. Recherche consécutive au message LAB535. Les résultats
de cette note ne supposent pas le rang global, sauf les paragraphes qui
mentionnent explicitement l'espace de Seidel de dimension36.

**Résultats.** Le cadre cœur+D+Z de norme16 a35 sommets et deux relations
de Seidel forcées, donc rang≤33. Son admissibilité spectrale réelle se
ramène exactement à une matrice rationnelle8×8. Ce filtre permet d'exclure
toutes les incidences D–Z des trois premières attaches du cœur8, dans
la branche D indépendant. D'autres attaches survivent ; la norme16
n'est pas exclue et le catalogue global n'est pas achevé.

Un premier cadre35 de rang33 passant le filtre réel complet, avec les
types des64 simples et leurs domaines locaux, est livré dans
`data/codex_norm16_typed_world35_0_3_2.json` pour le moteur de LAB.

## 1. Deux relations à conserver dans tout cadre complet cœur+D+Z

Soient f=1_P-1_Q et h=1_P+1_Q. Dans la norme16, poser

    g=3h+1_D-1_Z,        u=1_P-1_D+1_Z.

Les identités de degrés donnent sur les99 sommets

    Af=-4f,             Ag=3g+5*1,             Au=-4u+2*1.

Leurs sommes sont0,45,11. Pour S=J-I-2A,

    Sf=7f,    Sg=7(5*1-g),    Su=7(1+u).

Les vecteurs f,g donnent donc deux relations indépendantes modulo sept,
entièrement portées par le cadre35. La troisième n'est pas indépendante :
u+g=4*1_P+3*1_Q, donc u+g=4f modulo sept. Le rang de Seidel du cadre
est au plus33. Ajouter un seul simple peut le porter à34, pas35.

Si le rang du cadre est33 et si l'espace global de LAB est non dégénéré
de dimension36, les35 vecteurs engendrent un espace de dimension≤33
à cause des deux relations vraies. Le rang33 force alors un engendrement
non dégénéré de dimension33. Le résidu orthogonal a dimension3.

Pour un cadre de rang32 ou moins, cette conclusion de non-dégénérescence
ne suit plus des seules deux relations. Il faut traiter les relations
supplémentaires ou ajouter des sommets ; le moteur ne doit pas supposer
automatiquement que dimension de l'engendrement = rang de Gram.

Les identités réelles donnent aussi les annulations

    (3I-A+J/9)g=0,
    (4I+A-2J/11)f=(4I+A-2J/11)u=0.

## 2. Généralisation aux autres normes binaires

La construction vaut pour tout vecteur binaire f=1_P-1_Q de valeur−4,
avec |P|=|Q|=m. Toujours avec h=f², définir

    g=(A+4I)h/2-1,
    u=1_P+h-Ah/2+1.

Ces vecteurs sont entiers : Ah est pair, puisque Af est divisible par4.
L'identité A²+A=12I+2J donne directement

    (A-3I)g=(2m-11)*1,       sum g=9(2m-11),
    (A+4I)u=(18-2m)*1,      sum u=11(9-m).

Un sommet extérieur avec t voisins de chaque signe porte g=t-1 et
u=1-t. Les sommets simples t=1 disparaissent donc des deux supports.
Sur le cœur, si a_v est le degré dans son propre signe, les valeurs
sont g=3+a_v et u=1_P-a_v. Les deux relations de Seidel restent vraies,
avec u+g=4*1_P+3*1_Q.

Si e=e(P)=e(Q), un calcul de norme donne

    ||u||²=2m²-25m+99-14e,          <f,u>=m.

En particulier, pour la norme18, u est lui-même un vecteur propre entier
de valeur−4, de norme carrée36 si e=0, de norme carrée22 si e=1, et de
produit scalaire9 avec f. Ce couplage est une contrainte à exploiter,
pas une exclusion déjà obtenue de ces deux branches.

## 3. Le Schur exact de la borne spectrale supérieure

La matrice 3I-A+J/9 du SRG est positive semi-définie. Noter A_C l'adjacence
du cœur, V l'incidence16×8 du cœur vers D, X l'incidence8×11 entre D et Z,
et A_D,A_Z leurs adjacences internes. Poser

    M=3I_16-A_C+J_16/9,
    C=J_(16,8)/9-V,
    H=3I_8-A_D+J_8/9-C^t M^-1 C,
    Q=3I_11-A_Z-J_11/7,
    K=3J_(8,11)-7X.

Alors la condition spectrale sur les35 sommets équivaut à

    R = H-K Q^-1 K^t/49 >= 0.                            (1)

En effet, M est positive définie. Le cœur est4-régulier, ses valeurs
propres autres que±4 sont dans[-2,2] (note166). Sur le vecteur constant,
M a valeur7/9 ; sur les autres directions, ses valeurs sont positives.

Chaque colonne de V a somme4. L'élimination du cœur donne exactement
Q sur Z et3J/7-X sur D×Z, d'où(1) par un second complément de Schur.

Q est également positive définie pour les14 forêts de note253. Les
contributions de chaque composante à1^t(3I-A_Z)^-1 1 sont

    K1 :1/3 ; K2 :1 ; P3 :13/7 ; P4 :14/5 ; K1,3 :3.

Sur les14 formes, leur somme est au plus33/5<7. La formule de
modification par une matrice de rang un prouve donc la positivité de
Q=3I-A_Z-J/7. La formule(1) vaut aussi lorsque D possède une arête ;
le pilote ci-dessous traite uniquement D indépendant.

R possède la relation constante R1=0, issue de g. Il reste nécessaire
de vérifier sa positivité : les seuls degrés et les nombres locaux de
voisins communs ne l'imposent pas.

## 4. Filtrer pendant la construction

Le programme `norm16_schur_data.py` calcule H et Q^-1/49 exactement,
avec un même dénominateur entier positif L. Pour chaque attache X,
la matrice entière testée est

    L R = (L H)-K(L Q^-1/49)K^t.

Dans `norm16_dz_catalogue.cpp`, les mineurs principaux d'ordres1 et2
filtrent les domaines de lignes et leurs compatibilités ; ceux d'ordres3
et4 filtrent chaque nouvelle ligne pendant la recherche. Les calculs
sont entiers, en128 bits. Une borne explicite impose |(LR)_ij|<10^9,
donc la somme des24 produits de quatre entrées tient en128 bits signés.
Si la borne est dépassée, le programme s'arrête avec une erreur au lieu
d'utiliser un résultat susceptible d'avoir débordé.

Les survivants des mineurs≤4 ne sont pas déclarés PSD. Le pilote
`norm16_independent_catalogue.py` peut leur appliquer ensuite une
élimination exacte sans fractions sur toute la matrice8×8. Les divisions
de Bareiss sont contrôlées ; les entiers Python ont une taille arbitraire.
Le mode `--count-only` omet explicitement ce second étage.

## 5. Résultats finis et état du comptage

Indices de cœurs et d'attaches dans les JSON des notes166/169 :

- cœur0, attache0, forêt2 :1696 incidences locales deviennent0 ;
- cœur0, attache0, forêt7 :832116 incidences locales deviennent0 ;
- pour cette attache0, les sept comptes après mineurs≤4 sont
  0,0,68,0,76,200,0. Les344 candidats restants échouent tous au test
  PSD complet ; la branche D indépendant de cette attache est exclue ;
- les attaches1 et2 du même cœur sont également exclues dans cette
  branche, après exploration exhaustive des sept forêts ;
- les attaches3 et4 conservent respectivement3110 et68241 supports
  passant le test PSD complet. Ils ne sont pas des complétions SRG.

Les71351 supports de ces cinq attaches ont les rangs de Seidel :
31 pour241,32 pour10174 et33 pour60936.

Un second pilote de comptage, portant sur les dix-huit premières
attaches du cœur0, a déjà rencontré6303880 candidats passant les
mineurs≤4. Sur126 recherches,49 sont interrompues à leur limite locale,
donc ce nombre est seulement un compte partiel, avant le test PSD
complet et avant les derniers stabilisateurs des attaches. **Il n'existe
pas encore de décompte global des cadres de norme16.** La campagne de
comptage a été arrêtée après cet échantillon : multiplier les cas sans
exploiter leur test de rang n'apporterait pas l'estimation finale recherchée.

Les résumés archivés distinguent EXHAUSTED et STOPPED. Ne pas présenter
la somme du second pilote comme6303880 formes réalisables ou distinctes
à tout isomorphisme près, ni comme une exclusion globale.

## 6. Premier monde35 utilisable par LAB

Le fichier `codex_norm16_world35_seed.json` décrit un survivant PSD
de cœur0, attache3, forêt2. Le JSON `codex_norm16_typed_world35_0_3_2.json`
contient son adjacency35×35, ses types, les deux relations de Seidel
et les domaines locaux des64 sommets simples restants. Le rang est33.

Les indices sont P=0..7, Q=8..15, D=16..23, Z=24..34. Un masque entier
utilise le bit i pour l'adjacence au sommet i. Les47 cellules non vides
contiennent64 simples avec multiplicité, pour7580 colonnes par cellule
au total. Dans la cellule complète autour de P0, il reste huit simples,
ayant97 à252 colonnes chacun avant les produits de Seidel et l'isotropie.

Tous les D sont déjà placés. Un simple avec r voisins D a exactement
r+1 voisins Z et11-2r voisins simples. Les six voisins proches connus
de chaque P (quatre Q et deux D), complétés par ses huit simples,
doivent induire7K2. Le même test s'applique autour de chaque Q.

Ce cadre demande un résidu de dimension3 au rang global37. Il est fourni
pour mesurer le coût effectif du moteur sur une entrée survivant au filtre
réel, sans attendre un catalogue volumineux et sans dupliquer le moteur LAB.

## 7. Résultat de pair reçu

LAB annonce au message535 avoir terminé l'exclusion exhaustive de la
norme14 au rang37 :33508 orbites de800427 bases,38141 recherches,
aucun survivant, sans utiliser L23. Il rapporte des contrôles indépendants
et des cellules plantées. Source : commit ff0052f, branche
`lab/theta-lp-2026-10-08`, note17.95 et `fano37.c`.

Ce résultat est utilisé avec sa portée annoncée, sans lancer un audit
en double. Il laisse ouvertes les branches de normes16,18 et20 de
l'échelle couvrante au rang37. La présente note ne clôt aucune de ces
trois branches entières.
