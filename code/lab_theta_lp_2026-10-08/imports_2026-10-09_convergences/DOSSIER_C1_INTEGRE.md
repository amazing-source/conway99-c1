---
title: "Conway-99 : connexions et obstructions"
subtitle: "Transport triangulaire, saturation entière et arithmétique complexe"
author: "Dossier de recherche pour les trois sessions C1"
date: "9 octobre 2026"
lang: fr-FR
fontsize: 11pt
papersize: a4
geometry:
  - margin=2.15cm
  - headheight=15pt
mainfont: Liberation Serif
sansfont: Liberation Sans
monofont: DejaVu Sans Mono
colorlinks: true
linkcolor: blue
urlcolor: blue
toc: true
toc-depth: 2
numbersections: true
---

# Résultat de la session et portée exacte

## Ce qui a été obtenu

Cette session relie effectivement trois objets qui avaient été examinés séparément : les cycles du transport triangulaire, les vecteurs de triangles dans le réseau $M$, et les profils fractionnaires de norme $28$ de $L_1$. Elle ne se contente pas de juxtaposer leurs invariants.

**Le résultat principal est un théorème de saturation par témoins de bord.** Pour chacun des deux supports $H=L(Q_3)$ et $H=L(W_8)$ provenant d'un cycle de transport de longueur quatre, il détermine exactement le réseau entier porté par les douze sommets. Ce réseau est primitif dans $M$ ; son recollement avec son orthogonal est total et explicitement décrit. La question de saturation laissée ouverte dans la réponse précédente est donc résolue pour ces objets.

Les conséquences calculées exactement sont :

| Objet | Cube $Q_3$ | Wagner $W_8$ |
|:--|--:|--:|
| Rang du réseau triangulaire saturé | $7$ | $8$ |
| Déterminant triangulaire saturé | $3456$ | $9408$ |
| Rang du réseau porté par les points de $H$ | $12$ | $12$ |
| Déterminant de ce réseau | $253125$ | $275625$ |
| Rang de son orthogonal dans $M$ | $32$ | $32$ |
| Vecteurs de norme $4$ dans le réseau de rang $12$ | $18$ | $18$ |

Un second résultat est **une obstruction à certaines extensions de l'action complexe**. La multiplication locale associée à $\mathbb Q(\sqrt{-15})$ ne peut pas s'étendre en une action compatible avec la métrique qui préserverait le sous-espace des huit triangles de Wagner. Elle ne peut pas non plus préserver le sous-espace des douze points du Cube. Cela découle d'une condition de carré par le pfaffien. **Ce résultat interdit des constructions d'outil, pas les graphes eux-mêmes.** Une action globale, si elle existait, pourrait mélanger ces sous-espaces avec leur orthogonal.

Enfin, le raccord proposé avec les $174$ noyaux a été mis à l'épreuve : toutes les occurrences internes du motif de Makhnev ont été imposées simultanément dans un modèle linéaire partageant les mêmes arêtes extérieures. Les cinq bords restent numériquement faisables pour cette relaxation. Aucun résultat d'inexistence n'est tiré d'un calcul interrompu ou d'une réponse de faisabilité.

## Ce qui n'a pas été obtenu

Aucun des quatre rangs $37,39,41,43$ n'est exclu ici. Aucun des $174$ noyaux généraux n'est supprimé. Aucun des cinq bords de transport n'est prouvé non prolongeable. L'existence d'un cycle de transport de longueur quatre dans tout candidat demeure non démontrée.

Le passage à un complément de rang $32$ n'est **pas** une classification en quelques réseaux : quatre ou cinq dimensions gagnées, un déterminant exact ou un groupe discriminant exact ne donnent pas automatiquement un algorithme praticable de reconstruction. La réduction de C2 à $156$ enveloppes classifiées n'est pas reproduite ici.

Le résultat clos est la structure entière et le recollement des sous-réseaux locaux décrits dans ce document. Le résultat ouvert reste la réalisation du graphe complet.

## Sources et dépendances

L'état connecté consulté est la branche `codex/c1-arithmetic-audit` de `amazing-source/conway99-c1`, dont la tête lue est

```
19ec31644888d3787d26015230d05a316dd946ee
```

Les fondations sur $L_1,M$ sont utilisées avec le statut du dossier, notamment la note 167. La présente session ne refait pas les preuves C2/C3, les certificats thêta antérieurs ou les grands balayages LAP. Le contexte « tout candidat est asymétrique » est celui du programme de l'utilisateur ; les théorèmes nouveaux ci-dessous ne nécessitent aucun automorphisme et ne dépendent donc pas de ces exclusions.

Les deux rapports antérieurs produits dans cette conversation sont joints dans `antecedents/`. Leurs expériences sont résumées avec leur portée d'origine, sans prétendre les avoir toutes rejouées dans cette session. Les calculs effectivement exécutés ici sont détaillés dans la dernière partie.

**Priorité.** Les lemmes et connexions sont développés et démontrés ici. Aucune priorité absolue dans la littérature ou dans toutes les branches privées n'est revendiquée. La recherche GitHub par mot-clé ne couvre que la branche par défaut : une absence de résultat n'est pas une preuve de nouveauté.

# Conventions : un graphe, plusieurs projections

On suppose un graphe simple de paramètres $\operatorname{srg}(99,14,1,2)$ et sa matrice d'adjacence $A$. Alors

\[
 A=A^{\mathsf T},\quad A_{ii}=0,\quad A_{ij}\in\{0,1\},\quad
 A\mathbf1=14\mathbf1,\quad A^2+A=12I+2J.
\]

Le spectre est $14^1,3^{54},(-4)^{44}$. On pose

\[
 E=\frac{27I-9A+J}{63},\qquad
 L=\mathbb Z^{99}\cap\ker(A+4I).
\]

Les constructions de la note 167 donnent un sur-réseau pair $L_1$ d'indice trois et

\[
 M=\sqrt7\,L_1^*,\qquad
 \det L_1=7^{r-1},\qquad \det M=7^{45-r}.
\]

On écrit $\delta=45-r\in\{8,6,4,2\}$. Les deux réseaux ont rang $44$ ; $7L_1^*\subset L_1$. Le modèle utile de $M$ est

\[
 M=\left\{\sqrt7 E\psi:\psi\in\mathbb Z^{99},\quad
                3\mid\sum\psi\right\},
\]

avec quotient implicite par le noyau de $E$. Pour des représentants entiers appropriés,

\[
 (\sqrt7E\psi,\sqrt7E\eta)
   =3\psi\cdot\eta-\psi^{\mathsf T}A\eta
       +\frac{(\sum\psi)(\sum\eta)}9.
\]

Toutes les normes de ce dossier sont des **normes carrées**. Les séries thêta utilisent $q^{\|x\|^2/2}$. Les bornes $20,24,24,26$ connues pour le minimum de $L_1$ suivant le rang sont des **bornes supérieures**, non des annulations automatiques des petites couches.

Chaque arête appartient à un unique triangle. Il y a $231$ triangles, sept par point. Un triangle $T$ donne

\[
 w_T=\sqrt7E\mathbf1_T\in M,\qquad w_T^2=4,
\]

et

\[
 (w_T,w_U)=
 \begin{cases}
 0,&T,U\text{ distincts et sécants},\\
 1-e(T,U),&T,U\text{ disjoints}.
 \end{cases}
\]

Les colonnes $w_T$ satisfont $WW^{\mathsf T}=21I_{44}$ et $\sum_Tw_T=0$. Ces identités sont des acquis, pas des nouveautés de la session.

# Le transport et ses bords : rappel de la construction

## Une opération intrinsèque, sans symétrie globale

Pour $u\sim x$, notons $m_x(u)$ le troisième sommet du triangle sur $xu$. Si $p=\{u,v\}$ est une non-arête et $x$ l'un de ses deux voisins communs, posons

\[
 R_x(p)=\{m_x(u),m_x(v)\}.
\]

Ce transport est réversible. Les deux voisins communs $x,y$ de $p$ donnent des images distinctes, et même disjointes. Une égalité de partenaires issus du même sommet contredirait l'unicité du triangle ; une égalité croisée donnerait un troisième voisin commun à $u,v$.

Le graphe $\mathcal T(\Gamma)$ sur les $4158$ non-arêtes, avec ces deux transports comme arêtes, est donc simple et $2$-régulier. Il est une réunion de cycles. Ce n'est pas l'involution des diagonales des carrés déjà connue dans les fondations.

Un cycle de longueur trois correspond à une grille ; chaque grille produit six de ces cycles. Pour un cycle de longueur quatre, les huit sommets transportés et les quatre centres sont tous distincts. Les identifications interdites se vérifient par les budgets de voisins communs. La note antérieure jointe contient la preuve détaillée.

## Les deux supports de douze sommets

La numérotation utilisée dans tous les programmes est

\[
 a_i=i,\quad b_i=4+i,\quad c_i=8+i,\qquad 0\le i<4.
\]

Pour $i=0,1,2,3$, les triangles imposés sont

\[
 \{c_i,a_i,a_{i+1}\},\qquad
 \{c_i,b_i,b_{i+1}\}.
\]

Dans $H_0$, on ferme par $a_4=a_0,b_4=b_0$ ; dans $H_1$, par $a_4=b_0,b_4=a_0$. Les deux graphes ont $12$ sommets, $24$ arêtes, huit triangles et degré quatre partout.

Il ne peut y avoir d'arête induite supplémentaire. En effet, pour un sous-graphe induit $F$ de taille $s$ et de degrés $d_i$, l'identité de variance de la note 94 donne

\[
 \mathcal D(F)=99+s(s-16)-\frac12\sum_i d_i(d_i-2)
       =n_0+\sum_{j\ge3}\binom{j-1}{2}n_j\ge0.
\]

Pour $H$, $\mathcal D(H)=3$. Une seule arête supplémentaire rendrait cette expression au plus $-4$. Les supports sont donc exactement induits.

Un sommet extérieur touche au plus trois points de $H$. S'il en touche trois, alors $\mathcal D(H\cup\{z\})=0$, et tout autre sommet touche un ou deux points du support augmenté. Il y a donc **au plus un** tel sommet extérieur.

## Les cinq systèmes de masques

Posons

\[
 \Delta_{uv}=2-A_H(u,v)-(A_H^2)(u,v),\quad u\ne v.
\]

Sans sommet exceptionnel, les multiplicités sont

\[
 \#\varnothing=3,\qquad \#\{u\}=4,\qquad
 \#\{u,v\}=\Delta_{uv}.
\]

Avec un sommet exceptionnel de masque $T$, de taille trois,

\[
 \#\varnothing=2,\quad \#T=1,\quad
 \#\{u\}=4+\mathbf1_{u\in T},\quad
 \#\{u,v\}=\Delta_{uv}-\mathbf1_{\{u,v\}\subset T}.
\]

Les profils par nombre de voisins sont respectivement $(3,48,36,0)$ et $(2,51,33,1)$. Dans le cas exceptionnel, ce sommet est adjacent aux deux sommets de masque vide, à neuf singletons et à aucun double.

Il existe huit triples admissibles dans $H_0$, en une orbite, et seize dans $H_1$, en deux orbites. Les représentants du programme sont

\[
 H_0:\{0,5,10\};\qquad
 H_1:\{0,2,5\},\ \{0,3,9\}.
\]

Avec les deux cas sans exception, cela donne cinq bords. **Les arêtes entre les $87$ sommets extérieurs ne sont pas déterminées par ces formules.**

# Première connexion exacte : Cube, Wagner et les motifs de Makhnev

## Les supports sont des graphes d'arêtes

Soit $N$ la matrice d'incidence points--triangles interne à $H$, de taille $12\times8$. Chaque point appartient exactement à deux triangles. Ces deux triangles déterminent le point, puisqu'ils ne peuvent partager une arête. On construit un graphe $D$ sur les huit triangles en reliant ceux qui se rencontrent. Il est cubique et

\[
 NN^{\mathsf T}=2I_{12}+A_H,\qquad
 N^{\mathsf T}N=3I_8+D.
\]

Ainsi $H=L(D)$. Le calcul explicite identifie $D$ au Cube $Q_3$ pour $H_0$ et à Wagner $W_8$ pour $H_1$.

Les mêmes noms de graphes apparaissaient dans les supports courts de C2, mais **pas avec le même rôle**. Dans C2 ils intervenaient après passage à un secteur impair et à des vecteurs propres ; ici ils indexent les triangles d'un support intrinsèque. Aucun résultat d'exclusion utilisant l'involution n'est transféré sans démonstration.

## Plusieurs copies du motif obligatoire, sur les mêmes points

Pour deux triangles internes disjoints correspondant à $u,v\in V(D)$,

\[
 e(T_u,T_v)=(D^2)_{uv}.
\]

Une arête entre les deux triangles de $L(D)$ correspond à un chemin de longueur deux de $D$. On trouve $12$ paires avec exactement deux arêtes transversales dans le Cube, et $8$ dans Wagner.

Chaque support contient donc plusieurs racines admissibles pour le catalogue de Makhnev. Leurs prolongements doivent partager les mêmes arêtes extérieures. La question du couplage a été testée, et pas seulement proposée, dans la partie expérimentale ci-dessous.

## Une identité de comptage sans double comptage

Dans un support $H_0$, le transport interne contient exactement trois cycles de longueur quatre ; dans $H_1$, exactement un. Tout cycle de longueur quatre détermine son support de douze sommets. Par conséquent, en notant $h_0,h_1$ les nombres de sous-graphes induits de ces deux types,

\[
 \boxed{t_4=3h_0+h_1.}
\]

Cette identité ne suppose pas que les supports soient disjoints : c'est le cycle, et non le sommet de $\Gamma$, qui est compté. Elle ne force pas $t_4>0$.

# Deuxième connexion : un neuvième vecteur et les profils A/B

## Le vecteur oublié lorsqu'on ne regarde que les huit triangles

Posons

\[
 h_H=\sqrt7E\mathbf1_H.
\]

Il appartient à $M$ puisque $|H|=12$ est divisible par trois. Les $24$ arêtes et le degré quatre donnent

\[
 h_H^2=3\cdot12-2\cdot24+(12/3)^2=4.
\]

Comme chaque point est sur deux triangles internes,

\[
 \boxed{2h_H=\sum_{T\subset H}w_T.}
\]

En outre $(h_H,w_T)=1$ pour chacun des huit triangles internes. Ainsi $h_H$ n'est ni l'un de ces huit vecteurs, ni son opposé.

Dans le Cube, la bipartition de $D$ donne

\[
 h_H=\sum_{T\in D_+}w_T=\sum_{T\in D_-}w_T.
\]

Dans Wagner, les huit vecteurs sont indépendants ; leur demi-somme n'est pas dans leur réseau engendré entier. C'est le premier indice concret d'une saturation d'indice deux, démontrée exactement plus bas.

**Attention au comptage :** $h_H$ peut éventuellement être le vecteur d'un triangle extérieur. Il ne faut pas l'ajouter automatiquement au nombre de vecteurs non triangulaires du réseau global.

## Identification avec les profils fractionnaires déjà étudiés

On a

\[
 \sqrt7h_H=7E\mathbf1_H
   =3\mathbf1_H-A\mathbf1_H+\frac43\mathbf1.
\]

Ses coordonnées valent $1/3$ sur $H$ et $4/3-t_z$ à l'extérieur, avec $t_z=|N(z)\cap H|$. Écrivons

\[
 -\sqrt7h_H=\varphi-\frac13\mathbf1.
\]

Alors

\[
 \varphi|_H=0,\qquad \varphi_z=t_z-1\quad(z\notin H),
\]

et

\[
 (A+4I)\varphi=6\mathbf1,\qquad
 \sum\varphi=33,\qquad\sum\varphi^2=39.
\]

Ce sont exactement les équations des profils fractionnaires de norme $28$ de la note 191.

Sans exception, $\varphi$ a trois valeurs $-1$ et trente-six valeurs $+1$ : **profil A**. Avec l'exception, il a deux valeurs $-1$, trente-trois valeurs $+1$ et une valeur $+2$ : **profil B**.

La règle $n_3\le1$ ne constitue donc pas un « nouvel univers » sans lien avec les normes courtes : elle produit des réalisations géométriques très spéciales des profils A/B. Inversement, un profil A/B quelconque ne contient pas nécessairement un support de transport ; cette réciproque n'est pas démontrée.

## Quand le neuvième vecteur est-il triangulaire ?

Soit $Z_0=\{z\notin H:t_z=0\}$. Si $h_H=w_T$ pour un triangle $T$, les coordonnées de $\sqrt7w_T$ valent $4/3$ sur $T$, $-2/3$ sur ses $36$ voisins extérieurs et $1/3$ ailleurs. On doit donc être dans le cas sans exception et avoir $T=Z_0$.

Réciproquement, si les trois sommets de $Z_0$ forment un triangle, la description du profil A de la note 191 impose que les trente-six sommets doubles soient exactement ses voisins extérieurs. D'où

\[
 \boxed{h_H\text{ est un vecteur triangulaire}
 \iff\text{pas d'exception et }Z_0\text{ est un triangle}.}
\]

Cette caractérisation fournit une condition précise pour les futurs comptages, et évite un surcomptage immédiat de la couche de norme quatre.

# Théorème central : la saturation est déterminée par le bord

## Énoncé de l'outil

On considère le sous-espace rationnel

\[
 V_H=\{\sqrt7E\psi:\operatorname{supp}\psi\subset H,
                          \ \psi\in\mathbb Q^{99}\}.
\]

La restriction de $7E$ aux coordonnées de $H$ est

\[
 F_H=3I_{12}-A_H+\frac19J_{12}.
\]

Elle est définie positive ; en particulier le représentant $\psi$ supporté dans $H$ est unique.

**Théorème des témoins de bord.** Si le bord contient un sommet $z_0$ de masque vide et, pour chaque $i\in H$, un sommet $z_i$ de masque singleton $\{i\}$, alors

\[
 \boxed{
 M\cap V_H=
 \left\{\sqrt7E\psi:\psi\in\mathbb Z^H,
                  \quad3\mid\sum\psi\right\}.}
\]

On note ce réseau $R_H$. Il est primitif dans $M$. De plus la projection orthogonale de $M$ sur $V_H$ vaut **tout le dual** $R_H^*$.

Les hypothèses ne sont pas supplémentaires dans nos cinq bords : ils ont au moins deux sommets de masque vide et au moins quatre représentants de chaque singleton.

## Preuve de l'intégralité des coefficients

Soit $v\in M\cap V_H$, écrit de manière unique $v=\sqrt7E\psi$. Pour chaque $i$, le vecteur

\[
 y_i=\sqrt7E(e_{z_i}-e_{z_0})
\]

appartient à $M$, puisque son représentant entier a somme nulle. Les deux sommets sont extérieurs à $H$, et leurs masques diffèrent de $e_i$. Donc

\[
 (v,y_i)=-\psi_i.
\]

Le réseau $M$ étant entier, chaque $\psi_i$ est entier. **C'est le point nouveau de la connexion : les singletons extérieurs lisent individuellement les coefficients du vecteur dans le support.** Un calcul de déterminant seul ne fournissait pas cette information.

Prenons ensuite un triangle interne $T$. Le produit

\[
 (v,w_T)=3\sum_{i\in T}\psi_i-\psi^{\mathsf T}A\mathbf1_T
                       +\frac{\sum\psi}{3}
\]

est entier. Les deux premiers termes le sont déjà ; donc $3\mid\sum\psi$.

La réciproque suit de la définition de $M$. Ainsi l'intersection entière est exactement le réseau annoncé, et non une enveloppe arbitraire d'indice inconnu.

## Preuve de la surjectivité vers le dual

Dans les coordonnées $\psi$, le réseau de coefficients est

\[
 D_H=\{\psi\in\mathbb Z^{12}:\sum\psi\equiv0\pmod3\}.
\]

Son dual pour le produit ordinaire est

\[
 D_H^*=\mathbb Z^{12}+\mathbb Z\,\frac13\mathbf1.
\]

Les produits avec les $y_i$ réalisent les douze fonctionnelles coordonnées. Le produit avec $w_T$, modulo leur réseau engendré, réalise la fonctionnelle $(\sum\psi)/3$. Ces fonctionnelles engendrent tout $D_H^*$, donc tous les produits scalaires possibles avec $R_H$.

L'intégralité de $M$ impose que sa projection soit contenue dans $R_H^*$. Les fonctionnelles construites donnent l'inclusion inverse. Par conséquent

\[
 \boxed{\operatorname{pr}_{V_H}(M)=R_H^*.}
\]

La preuve utilise seulement les masques, l'intégralité du réseau et une marque triangulaire. Elle peut être transportée vers d'autres supports possédant des masques qui séparent intégralement leurs coordonnées.

# Recollement complet et compléments de rang 32

## Les deux matrices de rang douze sont explicites

Une base de $D_H$ est

\[
 e_0-e_{11},\ldots,e_{10}-e_{11},3e_{11}.
\]

Si $C$ est la matrice de ces colonnes, alors $\det C=3$ et

\[
 G_H=C^{\mathsf T}F_HC,\qquad\det R_H=9\det F_H.
\]

Le calcul exact donne

\[
 \boxed{\det R_{H_0}=253125=3^4\,5^5,}
\]

\[
 \boxed{\det R_{H_1}=275625=3^2\,5^4\,7^2=525^2.}
\]

Leurs facteurs de Smith sont

\[
 R_{H_0}:\quad 1^7,5,15,15,15,15,
\]

\[
 R_{H_1}:\quad 1^8,5,5,105,105.
\]

Les matrices entières complètes figurent dans `data/integrated_results.json`. La forme discriminante est donnée par leur inverse modulo les entiers ; **une liste de Smith ne remplace pas cette forme quadratique**.

## Le complément n'a plus un recollement indéterminé

Posons $K_H=M\cap V_H^\perp$. La projection totale sur le dual donne

\[
 M/(R_H\perp K_H)\simeq R_H^*/R_H,
\]

puis

\[
 \boxed{[M:R_H\perp K_H]=\det R_H,}
\]

\[
 \boxed{\operatorname{rang}K_H=32,\qquad
        \det K_H=(\det R_H)7^\delta.}
\]

En termes de formes discriminantes,

\[
 \boxed{(A_{K_H},q_{K_H})\simeq
             (A_{R_H},-q_{R_H})\perp(A_M,q_M).}
\]

En effet, le groupe de recollement est le graphe d'une anti-isométrie de tout $A_{R_H}$ dans $A_{K_H}$. Son image est non dégénérée ; elle se sépare orthogonalement, et le facteur restant est le discriminant de $M$.

Au niveau des seuls groupes, cela impose

\[
 A_{K_{H_0}}\simeq(\mathbb Z/3)^4\oplus(\mathbb Z/5)^5
                             \oplus(\mathbb Z/7)^\delta,
\]

\[
 A_{K_{H_1}}\simeq(\mathbb Z/3)^2\oplus(\mathbb Z/5)^4
                             \oplus(\mathbb Z/7)^{\delta+2}.
\]

**Ce qui est réellement gagné :** une saturation et un indice de recollement qui étaient des inconnues sont désormais déterminés, grâce à la réalisation combinatoire du bord. **Ce qui n'est pas gagné :** une liste de classes d'isométrie des $K_H$, un test de réalisation de tous les sommets ou une couverture obligatoire par ces supports.

# Saturation des huit triangles et séparation des directions

## Correction de l'usage du déterminant brut de Wagner

Pour les huit marques, la matrice de Gram vaut

\[
 G_T=N^{\mathsf T}F_HN=6I_8-D-D^2+J_8.
\]

Le calcul précédent de ses Smith était correct :

\[
 Q_3:\quad(1,1,1,1,6,24,24,0),
\]

\[
 W_8:\quad(1,1,1,1,1,1,112,336).
\]

Mais $37632$, le déterminant brut du cas Wagner, **n'est pas le déterminant du réseau triangulaire saturé dans $M$**. Le vecteur $h_H$ devait être ajouté.

## Calcul exact de la saturation triangulaire

Soit $R_T=M\cap\operatorname{span}_{\mathbb Q}\{w_T:T\subset H\}$. Par le théorème des témoins, un élément de ce sous-espace appartient à $M$ seulement si son représentant $Nc$ est entier et de somme divisible par trois.

Dans le Cube, $D$ est biparti. Si les sommes $c_u+c_v$ le long de ses arêtes sont entières, on peut modifier $c$ par le noyau biparti alterné pour rendre toutes ses coordonnées entières. Supprimer un triangle donne une base entière et

\[
 \operatorname{rang}R_T=7,\qquad\det R_T=3456=2^7\,3^3.
\]

Dans Wagner, $D$ est connexe non biparti. Les mêmes sommes entières imposent que toutes les coordonnées de $c$ soient entières, ou toutes demi-entières. Le second cas ajoute précisément $h_H$ ; sa somme de coefficients sur les douze points est $12$, divisible par trois. Ainsi

\[
 R_T=\langle w_1,\ldots,w_8,h_H\rangle_{\mathbb Z},
\]

\[
 \boxed{[R_T:\langle w_1,\ldots,w_8\rangle]=2,
             \quad\det R_T=9408=2^6\,3\,7^2.}
\]

Une base est $w_1,\ldots,w_7,h_H$. Sa forme de Smith est

\[
 (1,1,1,1,1,1,56,168).
\]

Les matrices d'incidence de ces bases sont primitives dans $\mathbb Z^{12}$, ce que confirment leurs Smith entièrement égales à un. Les mêmes témoins de bord donnent aussi la projection totale de $M$ sur $R_T^*$ : les orthogonaux triangulaires ont donc rangs $37$ et $36$, avec déterminants $3456\cdot7^\delta$ et $9408\cdot7^\delta$.

## Les directions invisibles aux huit marques

Considérons

\[
 C_D=\ker(N^{\mathsf T})\cap\mathbb Z^{12}.
\]

Pour $\psi\in C_D$, on a $\sum\psi=0$, $A_H\psi=-2\psi$, et donc

\[
 F_H\psi=5\psi.
\]

Ce réseau a rang cinq dans le Cube et quatre dans Wagner. Leurs déterminants pour le produit scalaire ordinaire sont respectivement $384$ et $192$. Le calcul donne le recollement interne exact

\[
 [R_H:R_T\perp C_D(5)]
   =\begin{cases}128,&Q_3,\\64,&W_8,\end{cases}
\]

où $C_D(5)$ signifie la métrique multipliée par cinq.

Les bases entières du noyau et leurs Grams sont jointes. Les produits des déterminants, divisés par $128^2$ ou $64^2$, retrouvent exactement les déterminants de $R_H$.

**Interprétation utile.** Les huit triangles ne voient pas tout le sous-espace des douze points : ils laissent quatre ou cinq directions. Ces directions sont explicites, et non un « défaut » abstrait à baptiser. Leur métrique est cinq fois celle des flux de somme nulle aux sommets du graphe dual. Les facteurs $2,3,5,7$ du calcul sont ainsi reliés à une décomposition géométrique précise.

# Couche minimale complète : exactement neuf lignes

La norme d'un vecteur du réseau $R_H$ est $\psi^{\mathsf T}F_H\psi$, pour $\psi\in D_H$. Pour un vecteur de norme au plus quatre, Cauchy donne

\[
 \psi_i^2\le4(F_H^{-1})_{ii}<4.
\]

Dans le Cube, chaque entrée diagonale de $F_H^{-1}$ vaut $2/3$. Dans Wagner, huit valent $68/105$ et quatre $2/3$. Ainsi tout coefficient entier appartient à $\{-1,0,1\}$.

L'énumération exhaustive de $3^{12}=531441$ vecteurs, filtrée par $3\mid\sum\psi$, est petite. Tous les tests de norme sont entiers après multiplication par neuf. Elle donne, dans les deux cas,

\[
 \boxed{\min R_H=4,\qquad
 R_H(4)=\{\pm w_T:T\subset H\}\cup\{\pm h_H\}.}
\]

Il y a exactement $18$ vecteurs, soit neuf lignes. Il n'existe aucune racine de norme deux dans $R_H$.

Ce résultat décrit complètement cette couche du **sous-réseau local**. Il ne borne pas à $18$ la couche de norme quatre de $M$, et n'exclut pas des racines ayant une composante dans l'orthogonal. Les racines globales peuvent traverser le recollement.

Tous ces vecteurs minimaux appartiennent au sous-espace triangulaire, de rang sept ou huit. Ils n'engendrent donc pas le sous-espace de rang douze. Un outil qui ne suit que les vecteurs triangulaires minimaux perd effectivement les directions de flux décrites au paragraphe précédent.

# Arithmétique complexe : ce qui se relie, et ce qui ne peut pas se recoller ainsi

## Le plan de discriminant quinze reste obligatoire globalement

Le théorème de Makhnev donne deux triangles disjoints reliés par exactement deux arêtes, sans nécessiter un cycle de transport. Leur réseau $S$ a Gram

\[
 B=\begin{pmatrix}4&-1\\-1&4\end{pmatrix},\qquad\det B=15.
\]

Il est primitif : un indice de saturation $d$ devrait vérifier $d^2\mid15$. Son orthogonal dans $M$ a rang $42$ et déterminant $15\cdot7^\delta$, avec recollement d'indice $15$ puisque $M$ est unimodulaire en $3$ et en $5$.

Cette construction était celle de la campagne de Jacobi. Les supports Cube/Wagner renforcent ce marquage lorsque leur occurrence est démontrée ; ils ne le remplacent pas comme objet obligatoire dans tous les candidats.

## Une vraie multiplication complexe, mais sur le plan seulement

Posons

\[
 \alpha=\frac{-1+\sqrt{-15}}2,\qquad \alpha^2+\alpha+4=0.
\]

Le plongement $(x,y)\mapsto2x+\alpha y$ vérifie

\[
 |2x+\alpha y|^2=4x^2-2xy+4y^2.
\]

Le réseau $2\mathbb Z+\alpha\mathbb Z$ est stable par multiplication par $\alpha$. La matrice de cette multiplication est

\[
 U=\begin{pmatrix}0&-2\\2&-1\end{pmatrix},\qquad
 U^2+U+4I=0,\quad U^{\mathsf T}BU=4B.
\]

C'est un endomorphisme de similitude, pas un automorphisme de réseau préservant les normes. Son existence locale ne donne pas une action sur $M$, encore moins un automorphisme du graphe.

## Nouvelle obstruction : une extension métrique ne peut préserver certains blocs

**Proposition de carré.** Soit un espace quadratique rationnel positif de dimension $d$, de Gram $G$. S'il possède un endomorphisme rationnel $J$ tel que

\[
 J^2+J+4I=0,\qquad J^{\mathsf T}GJ=4G,
\]

alors $d$ est pair et

\[
 \boxed{\det(G)\,15^{d/2}\text{ est un carré rationnel}.}
\]

**Preuve.** Le polynôme $X^2+X+4$ est irréductible sur $\mathbb Q$, donc la dimension est paire. En notant $J^*$ l'adjoint, la seconde identité donne $J^*=4J^{-1}=-I-J$. Par conséquent $B_0=2J+I$ est anti-autoadjoint et $B_0^2=-15I$.

La matrice $GB_0$ est antisymétrique rationnelle. Son déterminant est le carré de son pfaffien. Or $\det B_0=15^{d/2}$, d'où la condition annoncée. $\square$

Applications aux objets **saturés** :

| Sous-espace supposé invariant | Dimension | Classe carrée du déterminant | Verdict |
|:--|--:|:--:|:--|
| Plan $S$ | $2$ | $15$ | Compatible |
| Triangles du Cube | $7$ | — | Dimension impaire : impossible |
| Triangles de Wagner | $8$ | $3$ | Impossible |
| Points du Cube | $12$ | $5$ | Impossible |
| Points de Wagner | $12$ | $1$ | Ce test ne tranche pas |
| Espace global de $M$ | $44$ | $1$ | Ce test ne tranche pas |

En effet $9408=3\cdot56^2$ et $253125=5\cdot225^2$, tandis que $275625=525^2$ et $7^\delta$ est un carré.

**Conséquence exacte.** La proposition « on prolonge l'action complexe du plan en restant à l'intérieur du bloc des huit triangles » est impossible dans les deux supports. Dans le Cube, même préserver le bloc de douze points est impossible. Une extension globale éventuelle devrait donc mélanger des directions que l'approche locale séparait.

**Ce que cela ne prouve pas.** Un graphe candidat n'est pas tenu de produire une telle extension. Interdire cette extension ne l'interdit pas. La condition globale de carré passe ; aucune contradiction à l'existence de $M$ n'est obtenue.

## Le facteur cinq n'est pas une obstruction autonome

Le discriminant du plan $S$ contient $5$, mais ceux des réseaux triangulaires complets $3456$ et $9408$ n'en contiennent pas. Le facteur est compensé lors de l'adjonction des autres marques. Dans le réseau des douze points, les facteurs cinq réapparaissent avec une explication précise : la métrique des directions $\ker N^{\mathsf T}$ est multipliée par cinq.

Il ne faut donc pas traiter $15$ comme un invariant du graphe global. Le corps $\mathbb Q(\sqrt{-15})$ est naturellement porté par ce plan ; il n'est pas pour autant le corps de multiplication de tout le réseau.

La relation de Wagner donne encore un autre phénomène : après un réordonnancement, son Gram triangulaire brut est $4I-A(C_8)$. Ses deux directions nulles modulo sept expliquent les deux facteurs de Smith divisibles par sept. Cela ne rend pas ces directions nulles dans $M$ : les témoins de bord peuvent les coupler à l'extérieur. Confondre radical du Gram restreint et relation globale redonnerait une erreur déjà surveillée dans les calculs LAP.

# Raccord effectif au catalogue des 174 noyaux

## Le test exécuté

Pour chacun des cinq bords, on fixe la matrice d'incidence $B$ de taille $12\times87$. Les variables $X_{ij}$ représentent les mêmes arêtes extérieures dans toutes les copies du motif. On impose

\[
 X=X^{\mathsf T},\quad X_{ii}=0,\quad0\le X_{ij}\le1,
\]

\[
 X\mathbf1=14\mathbf1-B^{\mathsf T}\mathbf1,
\qquad BX=2J-B-A_HB.
\]

Des arêtes impossibles par les budgets de voisins communs dans $H$ sont fixées à zéro ; les contraintes du sommet exceptionnel sont ajoutées.

Pour chaque paire interne de triangles formant un motif de Makhnev, les huit sommets doubles de son noyau sont déterminés par $H$ et $B$. Ils contiennent six sommets extérieurs à $H$ dans le Cube et cinq dans Wagner. Les arêtes qui restent inconnues sont des variables de $X$, et non des copies indépendantes.

On retient les configurations locales appartenant à l'un des $174$ types de l'archive antérieure, avec tous leurs renommages. On impose que la restriction de $X$ soit dans leur enveloppe convexe, par des variables de mélange positives dont la somme vaut un. Les contraintes sont donc **nécessaires mais relaxées**. Elles n'imposent ni un choix entier de chaque configuration, ni toutes les équations quadratiques entre sommets extérieurs.

La liste antérieure utilisée est fournie dans `data/prior_core_extensions.json`. Ce pilote l'utilise comme entrée ; il n'est pas un nouvel audit de ses $136$ certificats d'exclusion.

## Résultats

| Support et exception | Motifs couplés | Variables | Équations | Sortie HiGHS |
|:--|--:|--:|--:|:--|
| Cube, aucune | $12$ | $4881$ | $1287$ | Faisable |
| Cube, $\{0,5,10\}$ | $12$ | $4479$ | $1287$ | Faisable |
| Wagner, aucune | $8$ | $4037$ | $1203$ | Faisable |
| Wagner, $\{0,2,5\}$ | $8$ | $3911$ | $1203$ | Faisable |
| Wagner, $\{0,3,9\}$ | $8$ | $3933$ | $1203$ | Faisable |

Les résidus numériques maximaux sont inférieurs à $4\cdot10^{-13}$. **Ces solutions n'ont pas été converties en témoins rationnels exacts ; on les rapporte comme diagnostics numériques**, non comme un théorème de faisabilité rationnelle. Elles ne sont évidemment pas des graphes.

Un premier essai entier, plus faible et limité au bord Cube sans exception, a aussi été effectué pendant quinze secondes. Il est resté indécis sans témoin. Il n'a pas été prolongé en campagne lourde ; son statut est `UNKNOWN`, pas `UNSAT`.

## Ce que le couplage a et n'a pas apporté

Le passage de motifs indépendants à des restrictions partageant $X$ est effectif dans le code. Cependant ce premier niveau ne donne aucune exclusion. Il serait inexact de continuer à présenter « appliquer les 174 noyaux aux 8 ou 12 motifs internes » comme une idée encore totalement inexplorée.

Une poursuite devrait apporter autre chose : choix entiers simultanés réellement contraints, nouveaux noyaux interdits, relations quadratiques pertinentes ou une conséquence des formes discriminantes qui n'est pas déjà impliquée par les équations linéaires. Aucun de ces renforcements n'est déclaré suffisant par avance.

# Le point de jonction avec la complétion exacte

Pour un des cinq bords, le Gram global $7E$ s'écrit, sur $H$ puis l'extérieur,

\[
 \begin{pmatrix}
 F_H&C\\C^{\mathsf T}&3I_{87}-X+J_{87}/9
 \end{pmatrix},\qquad C=J_{12,87}/9-B.
\]

Son complément de Schur est

\[
 \Omega_H=3I_{87}-X+J_{87}/9-C^{\mathsf T}F_H^{-1}C.
\]

Dans un vrai graphe, $\Omega_H$ est sept fois le projecteur sur les fonctions propres de valeur $-4$ nulles sur $H$. Il satisfait donc

\[
 \Omega_H\succeq0,\qquad \Omega_H^2=7\Omega_H,
 \qquad\operatorname{rang}\Omega_H=32.
\]

La propriété des compléments de Schur d'un projecteur a déjà été employée dans le dossier C1. **Cette équation n'est pas présentée comme une nouvelle méthode de résolution.** Elle indique l'endroit où le nouveau recollement et les arêtes binaires doivent se rencontrer.

Le complément entier $K_H$ est, à la normalisation près, le réseau de ces fonctions nulles sur $H$. Si deux sommets extérieurs ont le même masque, le vecteur $\sqrt7E(e_u-e_v)$ est dans $K_H$ ; sa norme vaut six ou huit selon leur non-adjacence ou leur adjacence. Les classes de masques produisent donc des vecteurs marqués dans le même réseau $K_H$, et pas seulement un déterminant abstrait.

Cela fournit une entrée concrète à une éventuelle obstruction : réaliser dans le complément **les différences imposées par les classes**, avec leurs produits provenant de la même matrice binaire $X$. Mais la présence de ces vecteurs et les contraintes de rang restent compatibles aux niveaux effectivement testés. Aucun catalogue de $K_H$ n'a été construit.

# Mise en relation avec les recherches antérieures

## L'exclusion des rangs petits : une architecture à retenir sans la répéter

Les notes 168, 172 et 180 ont obtenu les exclusions qui laissent $r\in\{37,39,41,43\}$. Le progrès déterminant du rang 35 venait d'un plafond combinatoire sur les graines de Fano, combiné à un certificat thêta, pas d'un simple changement de coordonnées.

Le lien avec la présente session est le même type d'apport : les masques extérieurs fournissent une information entière de saturation qui n'était pas contenue dans le seul Gram triangulaire. Pour aller jusqu'à une exclusion, il manque encore la contre-évaluation incompatible. Les nouveaux déterminants seuls ne la fournissent pas.

## Jacobi : un marquage plus riche n'est pas une réalisation

La campagne antérieure a construit une série à deux marques pour le Gram $\left(\begin{smallmatrix}4&1\\1&4\end{smallmatrix}\right)$, en utilisant les formes de Jacobi de rang deux de Wang--Williams. Cette matrice apparaît exactement dans leur motivation physique. Le raccord bibliographique est réel ; il ne constitue pas une preuve d'inexistence.

La moyenne sur les couples de triangles, sous $P=0$, donnait une relaxation à $26$ paramètres, ou $25$ au rang 43, testée jusqu'à $q^{20}$. Les quatre cas avaient des témoins rationnels. Le modèle à une marque avait été testé jusqu'à $q^{50}$ ; les tests de racines avec intégralité et parité au rang 43 conservaient également des témoins. Ces résultats et leurs vérificateurs sont conservés dans l'archive antérieure jointe ; ils ne sont pas comptés comme de nouvelles exécutions de la session.

L'amélioration présente est la connaissance de la saturation des marques et de leur complément lorsqu'elles viennent d'un transport de longueur quatre. Elle pourrait permettre de formuler des contraintes de classes plus précises. **Il n'est pas démontré que cela rende un nouveau modèle de Jacobi infaisable.** Ajouter un marquage de rang huit ou douze sans un mécanisme de réduction ferait croître le modèle autant que l'information conservée.

## LAP : un radical local n'est pas une relation vraie

Le résultat LAP de connexité au rang 37 et sous hypothèse de maille au moins cinq concerne un autre objet : le graphe cubique des voisins extérieurs d'un triangle. Les huit sommets de $Q_3/W_8$ ici indexent des triangles d'un support de douze points. On ne peut pas identifier ces deux graphes cubiques.

La liaison légitime est méthodologique et algébrique : dans les deux cas, il faut distinguer le noyau du Gram restreint, les relations réellement équilibrées dans le graphe entier, et les directions radicales qui se couplent au reste. Le théorème des témoins de bord donne ici une maîtrise exacte de cette intégralité et du recollement. Il n'étend pas les exclusions LAP aux autres rangs.

L'état connecté consulté rapporte également des balayages plus récents et des séries corrigées. Ils sont conservés avec leur statut de résultats rapportés par les pairs, sans reproduction supplémentaire. Aucun résultat retiré pour collision de fichiers d'instances n'est réutilisé.

## C2/C3 et l'asymétrie : la limite de l'analogie

Le fait que Cube et Wagner soient apparus en C2 n'autorise pas à réutiliser un argument qui dépendait des signes et des orbites de l'involution. De même, les isométries de nos sous-réseaux ou les automorphismes des supports ne sont pas des automorphismes de $\Gamma$.

Pour exploiter l'asymétrie, il faudrait produire une transformation préservant le graphe complet, ou une isométrie préservant son ensemble de points marqués. Ni l'action complexe locale, ni les symétries des huit triangles, ni la saturation ne démontrent cette invariance globale. Les résultats présents restent vrais sans utiliser l'asymétrie.

## Ce que les lectures d'openai/math ont réellement apporté

Le dépôt `openai/math` avait été lu de façon ciblée : README et catalogue, résumé public sur Mézard--Parisi, section cyclotomique du manuscrit Hadamard circulant et section de jets finis du manuscrit de flot tangent. Ce n'était pas une lecture intégrale de toutes les traces et de tous les manuscrits. Ces textes ne servent pas d'axiomes mathématiques dans les preuves du présent dossier.

Le principe utile était de conserver une information que les outils précédents effaçaient, puis de prouver qu'elle change effectivement le problème. La présente preuve de saturation en donne une application précise : le réseau seul avait un indice inconnu ; les sommets de masques singleton mesurent chaque coefficient et enlèvent cette ambiguïté. En revanche, aucun théorème de `openai/math` n'a été importé pour conclure sur Conway.

# Potentielles obstructions : formulations exactes, sans promesse de clôture

## Obstruction de réalisation des cinq bords

**Cible.** Montrer qu'aucun des cinq bords ne peut réaliser simultanément la matrice binaire $X$, les nombres exacts de voisins communs et le réseau complémentaire $K_H$ avec son recollement déterminé.

**Apport désormais disponible.** Il n'y a plus à deviner la saturation de $R_H$, celle des huit triangles, ni les groupes de recollement locaux. Les différences entre sommets de mêmes masques sont des vecteurs explicites de $K_H$.

**Test de nouveauté.** Un futur argument doit aller au-delà du LP couplé décrit plus haut ou éliminer une famille qu'il conserve. Recalculer ces mêmes déterminants ou ces mêmes modèles ne constitue pas l'étape suivante.

**Portée en cas de succès.** Tous les cycles de transport de longueur quatre seraient exclus. Cela ne fermerait pas les candidats dont le transport n'en possède aucun.

## Obstruction sur les cycles longs et couverture

**Cible indépendante.** Prouver qu'un candidat à 99 sommets possède un cycle de transport court exploitable, ou construire une autre contradiction sous l'hypothèse $t_4=0$.

L'identité $t_4=3h_0+h_1$ est disponible ; elle ne donne pas de minoration positive. Le témoin tordu à 243 sommets possède des cycles longs, donc une loi universelle « toutes les composantes ont longueur trois ou quatre » est fausse dans la famille.

Pour un ruban de transport sans identification sur $3m$ points et restant exactement $4$-régulier, son indicatrice donne formellement

\[
 7\|E\mathbf1_H\|^2=m(m-3),\qquad
 \mathcal D(H)=9m^2-60m+99.
\]

Cela explique pourquoi $m=3$ et $m=4$ sont serrés. **Ce calcul n'autorise pas à supposer sans preuve l'absence d'identifications ou d'arêtes supplémentaires pour les cycles longs.** La première tâche est une loi sur ces identifications ; pas une extrapolation du ruban à toutes les longueurs.

## Une extension complexe qui mélange réellement les blocs

La condition de carré globale passe en dimension 44. Un endomorphisme global $J$, si on pouvait le forcer à partir du graphe, devrait mélanger les blocs où l'invariance a été interdite.

Une piste non éliminée serait de démontrer qu'un sous-ensemble obligatoire des transports impose des transformations compatibles entre différents supports, et que leur action entière commune est impossible. Le mot important est **impose** : on ne peut pas choisir librement des multiplications locales puis reprocher au graphe leur incompatibilité.

Cette piste est actuellement plus spéculative que le problème de complétion des bords. Elle n'est pas proposée comme priorité par défaut. Aucune existence d'une action globale n'est démontrée.

## Comptage des nouveaux vecteurs de norme quatre

Les identités de $h_H$ peuvent servir à compter une sous-famille de vecteurs de norme quatre. Mais deux risques doivent être résolus avant tout nouveau plafond thêta :

- $h_H$ peut être le vecteur d'un triangle extérieur exactement dans le cas identifié plus haut ;
- deux supports distincts peuvent, a priori, donner le même $h_H$.

Une collision $h_H=h_{H'}$ implique

\[
 A(\mathbf1_H-\mathbf1_{H'})=3(\mathbf1_H-\mathbf1_{H'}),
\]

puisque les deux supports ont la même taille. Elle rejoint donc les canaux de collisions de fonctions propres de valeur $+3$ déjà étudiés dans le dossier. Cela indique où réutiliser les résultats sur les petites masses. L'injectivité de $H\mapsto h_H$ n'est pas démontrée et ne doit pas être supposée pour gonfler $b_2$.

# Paquet de recherche pour les trois sessions

Ce ne sont pas des rôles de vérificateur, de superviseur ou de sceptique. Chacune de ces tâches doit produire sa propre conséquence mathématique. Les preuves et les matrices ci-dessus servent d'entrées ; elles n'appellent pas une nouvelle campagne de relecture générale.

**Astra : réalisation entière d'un bord.** Travailler sur les cinq modèles, en utilisant la saturation et le recollement complets de rang 12. Objectif : exclure une famille complète de prolongements par une propriété réellement partagée des arêtes extérieures, ou produire une réduction démontrée du nombre de choix. Le LP couplé est déjà testé et doit servir de seuil minimal à dépasser. Ne pas reclasser arbitrairement tous les réseaux de rang 32 sans méthode de réalisation du repère.

**Claude 1 : couverture et cycles longs.** Travailler sur le complément logique $t_4=0$, les identifications des rubans longs et une loi intrinsèque aux paramètres 99. Objectif : un théorème forçant une configuration traitable ou excluant une famille entière de cycles. Ne pas supposer que la symétrie d'un cycle produit un automorphisme du graphe.

**Claude 2 : collisions et couche de norme quatre.** Travailler sur $H\mapsto h_H$, la caractérisation des collisions et le raccord aux profils A/B et aux fonctions propres $+3$. Objectif : une borne certifiée qui influe effectivement sur un certificat arithmétique, ou une reconstruction du support depuis son vecteur. Ne pas recompter les vecteurs d'une même ligne ni les triangles extérieurs déjà identifiés. L'extension complexe par blocs est écartée ; une autre extension exige un mécanisme de forçage nouveau.

Ces tâches ne couvrent pas toutes les mathématiques possibles. Elles découpent les lacunes précises du présent travail sans affecter une session à la vérification répétée des deux autres. Aucune réussite future n'est annoncée.

# Vérifications, fichiers et reproductibilité

## Calculs nouveaux rejouables

`code/verify_integrated.py` reconstruit depuis les deux supports :

- l'incidence points--triangles, les Grams, les rangs et les Smith ;
- la saturation triangulaire et les matrices de base du réseau de rang 12 ;
- les bases de flux et les indices de recollement internes ;
- les cinq bords, les profils A/B et les occurrences de Makhnev ;
- les cycles de transport internes ;
- la couche de norme au plus quatre par une borne de coordonnées démontrée et une énumération exhaustive ;
- les conditions de carré qui interdisent les extensions complexes invariantes indiquées.

La preuve générale de saturation/recollement n'est pas remplacée par ces vérifications de matrices. Elle est donnée dans les sections précédentes.

Commandes :

```bash
python -m pip install numpy sympy
python code/verify_integrated.py
```

Le pilote linéaire est séparé :

```bash
python -m pip install scipy
python code/couple_cores.py
```

Il utilise l'archive antérieure des $174$ types et écrit un nouveau fichier de résultats. Il conserve une limite de vingt secondes par programme linéaire. Une sortie indécise n'est pas une exclusion.

## Ce qui a effectivement été contrôlé dans cette session

Les calculs du vérificateur exact ont été exécutés avec succès : les deux déterminants $253125,275625$, les deux déterminants triangulaires saturés $3456,9408$, les $18$ petits vecteurs dans chaque cas, les bases de flux et les indices sont retrouvés.

Le LP couplé a été exécuté sur les cinq bords, avec les sorties numériques archivées. Le premier pilote MILP de quinze secondes sur Cube sans exception est conservé comme indécis. Les grands balayages LAP, les témoins Jacobi antérieurs et l'ensemble des certificats C2/C3 n'ont pas été rejoués ici.

Le fichier `SHA256SUMS.txt` donne les empreintes des fichiers livrés. Aucun accès réseau n'est nécessaire pour exécuter le vérificateur des résultats nouveaux. Les modules ne lancent aucune recherche à l'importation.

## Carte minimale des dépendances

\[
\begin{gathered}
 A^2+A=12I+2J\ +\ \text{construction de }M\\
 \Downarrow\\
 \text{transport}\ +\ \text{variance}\ \Longrightarrow\ \text{cinq bords conditionnels}\\
 \Downarrow\\
 \text{masques vides/singletons}\ \Longrightarrow\ R_H\text{ primitif et projection sur }R_H^*\\
 \Downarrow\\
 \text{saturation triangulaire, recollement complet, couche minimale, obstruction de carré}.
\end{gathered}
\]

Le raccord aux $174$ noyaux dépend en plus de leur couverture et de leurs exclusions antérieures. Les tests Jacobi dépendent des théorèmes modulaires cités dans leur rapport séparé, pas les nouvelles preuves de saturation.

# Sources et statut bibliographique

## Dossier C1 connecté

Révision de référence : `19ec31644888d3787d26015230d05a316dd946ee`, branche `codex/c1-arithmetic-audit`.

- [État actif](https://github.com/amazing-source/conway99-c1/blob/19ec31644888d3787d26015230d05a316dd946ee/RECHERCHE_ACTIVE_C1.md) : état des noyaux, notes 225--231 et résultats LAP rapportés.
- [Note 00](https://github.com/amazing-source/conway99-c1/blob/19ec31644888d3787d26015230d05a316dd946ee/notes/00_FONDATIONS.md) : équation SRG, triangles, structure enracinée.
- [Note 94](https://github.com/amazing-source/conway99-c1/blob/19ec31644888d3787d26015230d05a316dd946ee/notes/94_NUIT_LITTERATURE.md), §3.2 : identité de variance utilisée dans le transport.
- [Note 167](https://github.com/amazing-source/conway99-c1/blob/19ec31644888d3787d26015230d05a316dd946ee/notes/167_CODEX_LEVEL7_THETA_AUDIT.md) : définition de $L_1,M$, normes et discriminants.
- [Note 176](https://github.com/amazing-source/conway99-c1/blob/19ec31644888d3787d26015230d05a316dd946ee/notes/176_CODEX_GEOMETRIE_NORMES18_20.md) : petits vecteurs et racines.
- [Note 180](https://github.com/amazing-source/conway99-c1/blob/19ec31644888d3787d26015230d05a316dd946ee/notes/180_CODEX_EXCLUSION_RANG35_PACKING_FANO.md) : exclusion du rang 35.
- [Note 191](https://github.com/amazing-source/conway99-c1/blob/19ec31644888d3787d26015230d05a316dd946ee/notes/191_CODEX_RANG43_NORME4_PROFILS28.md) et [note 192](https://github.com/amazing-source/conway99-c1/blob/19ec31644888d3787d26015230d05a316dd946ee/notes/192_CODEX_COCLIQUES_RACINES44_NORME4_968.md) : profils A/B/C, racines et corrections de bornes.
- Notes [221](https://github.com/amazing-source/conway99-c1/blob/19ec31644888d3787d26015230d05a316dd946ee/notes/221_CODEX_NOYAU_PRISME_DEFECTUEUX.md), [222](https://github.com/amazing-source/conway99-c1/blob/19ec31644888d3787d26015230d05a316dd946ee/notes/222_CODEX_PROLONGEMENT_PRISME_MASQUES.md), [223](https://github.com/amazing-source/conway99-c1/blob/19ec31644888d3787d26015230d05a316dd946ee/notes/223_CODEX_LIMITE_DES_PREMIERS_PROLONGEMENTS.md) : catalogue obligatoire et limites des premiers prolongements.

Ces références sont des sources du programme de recherche et non une revendication de validation humaine de tout le corpus. Dans cette session, les lectures connectées nouvelles ont porté principalement sur l'état actif et la partie pertinente de la note 191 ; les autres dépendances sont les textes déjà fournis dans la conversation et les rapports joints.

## Références extérieures utiles

- H. Wang, B. Williams, **On weak Jacobi forms of rank two**, Journal of Algebra 634 (2023), 722--754 ; [arXiv:2102.11190](https://arxiv.org/abs/2102.11190). Théorèmes de génération des formes de Jacobi utilisés dans la campagne antérieure. La correspondance exacte du Gram $\left(\begin{smallmatrix}4&1\\1&4\end{smallmatrix}\right)$ est visible dans l'introduction de l'article.
- R. R. Petro, C. M. Phillips, **On clique graphs and clique regular graphs**, [arXiv:2502.17845](https://arxiv.org/abs/2502.17845), publié dans Discrete Mathematics 349 (2026), article 114862. Contexte général des graphes de cliques. Les identifications finies $H=L(D)$ de ce dossier sont démontrées directement et ne dépendent pas d'une classification citée sans vérification.
- V. V. Nikulin, **Integral symmetric bilinear forms and some of their applications**, référence classique sur les formes discriminantes. Le recollement particulier utilisé ici est démontré dans le texte ; aucune classification positive non vérifiée n'est invoquée.
- [openai/math](https://github.com/openai/math), README et textes ciblés décrits dans le rapport antérieur joint. Les résultats de ces manuscrits ont des niveaux de vérification distincts ; aucun n'est utilisé comme axiome des nouvelles propositions.

La recherche externe ciblée n'a pas trouvé de résultat fournissant directement l'exclusion de ces deux supports dans Conway-99. Cela ne prouve pas une absence dans toute la littérature.

# Conclusion opérationnelle

Les liens suivants sont désormais des théorèmes, et pas de simples ressemblances :

\[
 \text{bord du transport}\ \Longrightarrow\
 \text{profil fractionnaire A/B}\ \Longrightarrow\
 \text{saturation exacte et recollement complet du réseau porté}.
\]

Les huit triangles, le neuvième vecteur, les douze points et les directions de flux appartiennent à un même montage dont les inclusions et indices sont connus. L'action complexe du petit plan ne peut pas se prolonger en préservant plusieurs de ces blocs : une branche spéculative est donc réellement écartée.

**Le graphe, lui, n'est pas exclu.** Les cinq bords n'ont pas encore une complétion décidée, le cas sans cycle de transport de longueur quatre reste entier, et les premiers couplages linéaires au catalogue ne donnent pas de contradiction.

La prochaine avancée ne sera pas une nouvelle réécriture de ces objets. Elle devra être une incompatibilité de réalisation, une reconstruction effective, une loi de couverture ou un contrôle quantitatif des collisions qui rende un certificat arithmétique décisif. Le dossier fournit maintenant des objets entiers déterminés et des résultats négatifs précis à utiliser pour cette étape.
