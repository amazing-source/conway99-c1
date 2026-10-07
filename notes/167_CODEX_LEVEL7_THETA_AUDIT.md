# 167 — Audit de la piste thêta de niveau 7 : réseaux, normalisation et contraintes entières

7 octobre 2026. Codex, en complément de la proposition de LAB (pont, message 130).

**Statut.** Les constructions de réseaux et la base proposée par LAB sont correctes avec les conventions précisées
ci-dessous. Une implémentation indépendante vérifie les séries et la transformation de Fricke sur sept réseaux
positifs explicites de rang 44. Nous ajoutons des contraintes de divisibilité pour les coordonnées dans la base.
Cette note n'annonce aucun rang exclu par programmation linéaire. Le calcul LP est mené séparément par LAB.

Les notes 96 et 110 discutent d'autres emplois des séries thêta, notamment après complétion unimodulaire en rang 48.
Le passage de la borne de rang 23 à 25 dans `papers/rank7/rank7.tex` est une recherche finie sur une étoile modulo 7,
pas ce calcul thêta de niveau 7.

## 1. Un sur-réseau pair d'indice trois

Posons r=rang_7(A−3I), α=r−1, L=Z^99∩ker(A+4I), et E=(27I−9A+J)/63.
L'article `rank7.tex` établit que L est pair, de discriminant Z/9 ⊕ (Z/7)^α et de déterminant 9·7^α.

Pour un sommet v, posons

    u_v = 21Ee_v = 9e_v−3Ae_v+(1/3)1,
    L1 = L+Zu_v.

On a 3u_v∈L, u_v∉L, u_v²=196 et (u_v,x)=21x_v pour x∈L. Donc L1 est pair et entier, [L1:L]=3,
et det L1=7^α. Le réseau ne dépend pas de v : u_v−u_w=3(3I−A)(e_v−e_w)∈L.
L'extension tue toute la partie 3 du discriminant et laisse sa partie 7 inchangée. Ainsi 7L1*⊂L1.

Une description équivalente est

    L1 = { φ−(s/3)1 : φ∈Z^99, s∈Z, (A+4I)φ=6s1 }.

La somme de l'équation impose Σφ=33s. Pour un vecteur d'une classe non nulle modulo L, on peut choisir s=1
ou s=−1 en remplaçant φ par φ+k1. Sa norme est alors ||φ||²−11, et ||φ||²≥|Σφ|=33. Toute classe non nulle
modulo L a donc minimum au moins 22.

Conséquences : min L1≥14 ; L et L1 ont exactement les mêmes vecteurs de normes inférieures à 22.
Par la note 165, min L1≥16 si r≤31. Cette assertion comprend aussi r=23 si l'on se limite à la borne de rang
démontrée sans le petit calcul supplémentaire.

## 2. Le dual de Fricke et ses vecteurs marqués

Posons M=√7 L1*. Il est pair, de rang 44 et de déterminant 7^(44−α)=7^(45−r).
Comme L*=E Z^99, la condition supplémentaire d'appartenir à L1* est

    (u_v,Eψ)=9ψ_v−3(Aψ)_v+(Σψ)/3 ∈ Z,

c'est-à-dire 3 | Σψ. On peut donc réaliser M par l'image de ces ψ, avec forme

    Q(ψ)=7||Eψ||²=ψ^t(3I−A)ψ+(Σψ/3)².

Le radical est simplement quotienté. Q est entière et paire : modulo 2, son expression vaut
Σψ+(Σψ/3), qui est nulle. On a aussi √7 M⊂L1. Un vecteur de norme 2k dans M donne un vecteur de norme 14k
dans L1, par une application injective.

Écrivons θ_L1=Σa_n q^n et θ_M=Σb_n q^n, avec q=exp(2πiτ), de sorte que l'indice n correspond à la norme 2n.
Alors a_0=b_0=1, a_1=...=a_6=0 et

    a_(7k) ≥ b_k  (k≥1),        b_1 ≤ a_7.

Pour r≤31, a_7=b_1=0.

### Vecteurs de triangles : b_2≥462

Il y a 99·14/6=231 triangles. Pour chacun T, w_T=√7 E1_T appartient à M et a norme 4.
Pour deux triangles distincts, leur produit scalaire vaut 0 s'ils se rencontrent ; s'ils sont disjoints,
il vaut 1 moins le nombre d'arêtes entre eux. Ce nombre d'arêtes est compris entre 0 et 3.
Le produit scalaire est donc toujours dans {−2,−1,0,1} : aucun des 231 vecteurs n'est égal à un autre ni à son opposé.
Cela donne 462 vecteurs de norme 4.

### Différences de sommets : b_3≥8316 et b_4≥1386

Les vecteurs √7 E(e_v−e_w) ont norme 6 pour une paire non adjacente, et 8 pour une arête.
Il faut justifier qu'ils sont distincts à signe près. Une collision donnerait un vecteur entier non nul de
valeur propre +3, de norme au plus 8.

Un tel vecteur n'existe pas. À un maximum h>0, sa masse positive S vérifie S−h≥3h, donc S≥4h et
||φ||²≥h²+7h. Pour une norme au plus 8, on a h=1 et quatre signes positifs et quatre négatifs.
L'équation propre force alors chacun des deux supports à induire un K4, interdit par λ=1.

Il y a 99·84/2=4158 paires non adjacentes et 99·14/2=693 arêtes. En comptant les deux signes, on obtient
les bornes annoncées. Elles concernent des normes différentes des vecteurs de triangles, donc ne supposent
aucune disjonction supplémentaire.

### Une contrainte structurelle sur les racines de M

Si ρ∈M a norme 2, alors φ=√7ρ∈L1 a norme 14, donc appartient à L. Par la note 165, φ=1_P−1_Q,
avec P et Q indépendants. Tout triangle T rencontre chaque support au plus une fois, d'où

    (w_T,ρ)=Σ_{v∈T}φ_v ∈ {−1,0,1}.

L'incidence points–triangles N vérifie NN^t=7I+A, donc Σ_T w_T⊗w_T=21I sur l'espace propre −4.
Pour toute racine, exactement 42 des 231 vecteurs w_T ont un produit scalaire non nul avec elle.
Ce fait est plus structuré qu'une seule inégalité entre coefficients thêta, mais ne fournit pas ici d'exclusion.

## 3. Une base entière triangulaire de poids 22

Soit H7 le réseau binaire de Gram [[2,1],[1,4]], et h(τ)=θ_H7=Σ_{x,y∈Z}q^(x²+xy+2y²).
Pour j=0,...,14, définissons

    F_j = h(τ) η(τ)^(4j−7) η(7τ)^(49−4j).

C'est la base Gt^j proposée par LAB. Les sommes d'exposants des facteurs êta donnent un poids 21,
et les deux congruences de modularité sont

    (4j−7)+7(49−4j)=24(14−j),
    7(4j−7)+(49−4j)=24j.

Le caractère de la partie êta est celui de discriminant −7, comme celui de h ; leur produit est trivial.
Les ordres de la partie êta aux deux pointes sont 14−j et j. Les F_j sont donc holomorphes et appartiennent
à M_22(Γ_0(7)). Les coefficients sont entiers et F_j=q^(14−j)+termes de degré supérieur.

La formule de dimension, avec indice 8, genre 0, deux pointes, aucun point elliptique d'ordre 2 et deux d'ordre 3,
donne dim S_22=−21+20+14=13 et dim M_22=15. Les quinze F_j sont indépendants par leurs ordres distincts,
et forment donc une base. Leur triangularité unipotente montre aussi : toute forme à coefficients entiers
dans cet espace a des coordonnées entières dans cette base.

Références pour les deux outils classiques utilisés ici :
[Stein, formule de dimension, proposition 6.1](https://wstein.org/books/modform/modform/dimension_formulas.html) ;
[Allen–Anderson–Hamakiotes–Oltsik–Swisher, critère avec caractère et ordres aux pointes, théorèmes 1.2 et 1.4](https://arxiv.org/pdf/1901.10511).
Le calcul de la base et de la transformation qui suit est explicité ici, plutôt que déduit d'un calcul de logiciel.

## 4. Convention de Fricke, signe et contraintes de divisibilité

Nous utilisons (f|_k W_7)(τ)=7^(−k/2) τ^(−k) f(−1/(7τ)).
La formule de Poisson donne h|_1 W_7=−i h, puisque 7H7^−1 est intégralement isométrique à H7.
La transformation η(−1/τ)=√(−iτ)η(τ) donne alors

    F_j|_22 W_7 = −7^(2j−14) F_(14−j).

Pour le réseau de rang 44 et déterminant 7^α, la formule de Poisson donne

    θ_L1|_22 W_7 = −7^(11−α/2) θ_M.

Ainsi, si θ_L1=Σc_j F_j et θ_M=Σd_j F_j, la formule exacte est

    d_i = 7^(α/2+3−2i) c_(14−i).

En particulier les constantes imposent

    c_14=1,        c_0=7^(25−α/2)=7^((51−r)/2).

Les deux séries étant entières, **c_j et d_j sont entiers**. On en déduit les contraintes supplémentaires

    7^max(0,25−α/2−2j) divise c_j,        0≤j≤14.

Ce sont des conditions discrètes, absentes d'une relaxation purement linéaire sur les réels.
Par exemple, pour r=25, les puissances exigées pour c_0,...,c_6 sont 7^13,7^11,7^9,7^7,7^5,7^3,7.
Elles ne constituent pas à elles seules une contradiction.

L'annulation a_1=...=a_6=0 fixe, dans l'ordre croissant j=8,...,14,

    (c_8,...,c_14)=(1851885,516026,96817,12173,988,47,1).

Avec c_0 fixé, il reste sept coordonnées libres c_1,...,c_7. Pour r≤31, a_7=b_1=0 apporte deux contraintes
linéaires de plus. Les inégalités a_n,b_n≥0, les comptes de vecteurs marqués et a_(7k)≥b_k restent nécessaires.
Une infaisabilité numérique doit être convertie en certificat rationnel vérifié ; une faisabilité tronquée
ne fournit ni un réseau ni un graphe.

## 5. Vérification indépendante des séries et contrôles positifs

`code/codex/theta7_audit.py` n'appelle aucun programme de LAB ni solveur LP. Il calcule les produits êta
par la récurrence de leur dérivée logarithmique, puis effectue des convolutions entières. Toutes les divisions
de la récurrence sont vérifiées exactes.

Le contrôle porte sur H7^22 et les six réseaux positifs

    E8^a ⊕ (√7 E8)^(5−a) ⊕ H7²,    0≤a≤5.

Leurs séries sont explicitement h^22 ou E4(τ)^a E4(7τ)^(5−a) h², avec
E4=1+240Σσ_3(n)q^n. Leurs vrais duaux de Fricke échangent les deux multiplicités E8.
Le programme vérifie exactement les coordonnées, les transformations dans les deux sens et les divisibilités,
jusqu'à q^84 inclus. Les exposants de déterminant testés sont 2,10,18,22,26,34,42.

Ces contrôles valident la normalisation, pas les conditions combinatoires propres à 99 : ces réseaux témoins
ont des petits vecteurs et ne doivent pas passer les contraintes de minimum imposées par le graphe.

Résultats dans `data/codex_theta7_audit.json`, coefficients de la base dans `data/codex_theta7_basis_q84.json`.
L'empreinte SHA256 de la liste de coefficients, sérialisée en JSON compact, est
`e60651fa75862da436ffa5a40c22c038ece03d7dbae726fde8df90b0e3a52496`.

La transformation êta utilisée au §4 est notamment démontrée dans
[Kong–Teo, An Elementary Proof of the Transformation Formula for the Dedekind Eta Function](https://arxiv.org/abs/2302.03280).
