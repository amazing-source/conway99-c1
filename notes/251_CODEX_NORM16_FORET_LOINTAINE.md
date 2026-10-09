# 251 — Norme seize : quinze forêts lointaines et soixante-quinze supports connus

10 octobre 2026, heure de Paris. Recherche motivée par la famille couvrante
proposée au message LAB525. Les résultats ci-dessous ne dépendent pas du rang.

**Théorème.** Soit f un vecteur propre entier de valeur -4 et de norme
carrée16 dans un srg(99,14,1,2). Reprendre la partition de la note166 :
P,Q, les deux supports indépendants de huit points ; D, les huit points
extérieurs ayant deux voisins de chaque signe ; B, les64 points ayant
un voisin de chaque signe ; Z, les onze points sans voisin dans P union Q.
Alors :

1. D induit au plus une arête.
2. Z possède cinq arêtes si D est indépendant, six sinon.
3. Z est une forêt dont les composantes non triviales sont K2, P3, P4,
   ou K1,3. Pj désigne ici le chemin sur j sommets.
4. Il reste sept formes de Z dans le premier cas, huit dans le second.

Avec les cinq cœurs de la note166, cela donne une liste couvrante de
**75 graphes induits explicitement connus sur les27 sommets P union Q
union Z**. Les formes listées sont nécessaires ; leur réalisabilité
dans un SRG n'est pas affirmée. Ce ne sont pas75 complétions à99 sommets.

## 1. Données acquises, sans refaire les classifications

La note166 prouve la binarité f=1_P-1_Q, l'indépendance de P,Q et la
classification des cinq matrices d'incidence4-régulières entre eux.
Leurs défauts ont pour types8,6+2,4+4,4+2+2,2+2+2+2.

La note169 donne déjà478 orbites des premières attaches de D au cœur,
réparties en243,118,86,27,4. Après choix d'une attache, les multiplicités
des64 points simples dans les cellules (p,q) sont fixées. Ni les cinq
cœurs ni les478 attaches ne sont régénérés ici.

Les identités de degrés de la note166 sont

    d_Z(d)=4+d_D(d)                    pour d dans D,
    d_Z(b)=1+d_D(b)                    pour b dans B,
    d_D(z)=2+d_Z(z)                    pour z dans Z,
    e(Z)=e(D)+5.                                           (1)

Chaque point du cœur a exactement deux voisins dans D. On note

    W_D=sum_{d dans D} binom(d_D(d),2),
    W_Z=sum_{z dans Z} binom(d_Z(z),2),
    W_B=sum_{b dans B} binom(d_D(b),2).

## 2. Le budget qui interdit deux arêtes dans D

Les28 paires de D ont au total56-e(D) voisins communs, avec multiplicité.
Compter leurs centres selon la partition du graphe donne :

- P union Q contribue16, car chacun de ses points a deux voisins D ;
- D contribue W_D ;
- B contribue W_B ;
- Z contribue sum_z binom(2+d_Z(z),2)=11+4e(Z)+W_Z.

En utilisant (1), l'identité devient

    5e(D)+W_D+W_Z+W_B=9.                                 (2)

Tous les termes sont non négatifs. Donc e(D)<=1 et W_D=0. On a
e(Z)=5 ou6, avec respectivement W_Z<=9 ou W_Z<=4.

## 3. Trois points de Z forcent une forêt très courte

Pour z dans Z, poser k_z=d_Z(z) et E_z=N(z) inter D, donc |E_z|=2+k_z.
Pour deux points distincts z,z' de Z, leurs voisins communs dans D
ne peuvent dépasser le budget laissé par leurs voisins communs dans Z :

    |E_z inter E_z'| <= 2-A_Z(z,z')-(A_Z^2)(z,z').

Pour trois points U={u,v,w}, la réunion de leurs E_z est contenue dans
D, de taille huit. La borne d'inclusion-exclusion tronquée donne donc

    sum_{z dans U} k_z + e_Z(U)
       +sum_{paires de U}|N_Z(z) inter N_Z(z')| <=8.        (3)

Un triangle donnerait au moins6+3+3=12 : Z est sans triangle.
Sur un chemin u-v-w, les extrémités ont v comme voisin commun et
e_Z(U)=2. Ainsi

    d_Z(u)+d_Z(v)+d_Z(w)<=5.                              (4)

Un sommet de degré au moins quatre viole (4) avec deux de ses voisins.
Si v a degré trois, deux quelconques de ses voisins doivent avoir
degré un : sa composante est K1,3. Les autres composantes ont degré
maximal deux. Aucun cycle n'est possible, ni un chemin d'au moins cinq
sommets : trois sommets consécutifs de degré deux violeraient (4).
Les seules autres composantes sont donc K1,K2,P3,P4.

## 4. Les quinze formes restantes

Écrire a,b,c,d les nombres de composantes K2,P3,P4,K1,3. Le nombre
d'isolés complète à onze sommets. Les conditions sont simplement

    a+2b+3c+3d=5+e(D),
    2a+3b+4c+4d<=11,
    b+2c+3d<=9-5e(D).

Leurs solutions donnent la liste suivante. Toutes les unions sont
disjointes ; les isolés sont omis de la colonne centrale.

| Arêtes dans D | Composantes non triviales de Z | Isolés |
|---|---|---:|
| 0 | P3 + K1,3 | 4 |
| 0 | P3 + P4 | 4 |
| 0 | K2 + 2P3 | 3 |
| 0 | 2K2 + K1,3 | 3 |
| 0 | 2K2 + P4 | 3 |
| 0 | 3K2 + P3 | 2 |
| 0 | 5K2 | 1 |
| 1 | 2P4 | 3 |
| 1 | 3P3 | 2 |
| 1 | K2 + P3 + K1,3 | 2 |
| 1 | K2 + P3 + P4 | 2 |
| 1 | 2K2 + 2P3 | 1 |
| 1 | 3K2 + K1,3 | 1 |
| 1 | 3K2 + P4 | 1 |
| 1 | 4K2 + P3 | 0 |

Le programme `code/codex/norm16_far_forest.py` génère ces seules petites
solutions entières, puis les matrices d'adjacence et les75 graphes sur27
points. Il utilise uniquement Python standard et les cinq cœurs archivés.
Le JSON `data/codex_norm16_far_forest.json` donne les arêtes explicites,
les degrés et le budget restant W_B de (2).

Les rangs modulo sept des matrices de Seidel de ces75 supports sont :

| Rang | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Nombre de supports | 1 | 2 | 14 | 4 | 26 | 4 | 24 |

Ces rangs ne sont pas des dimensions affirmées de leur engendrement dans
l'espace global : la restriction de la forme peut être dégénérée.

## 5. Un cadre de37 points pour la piste de LAB

Fixer p dans P et ajouter Y=N(p) sans Q aux27 points connus. Y a dix
points : deux dans D et huit dans B. Leurs attaches au cœur sont parmi
les données déjà classifiées de la note169.

Dans N(p), les quatorze points induisent7K2. Les quatre points de
N(p) inter Q sont indépendants ; chacun a un partenaire distinct dans Y.
Les six autres points de Y induisent3K2. Une fois les quatre partenaires
identifiés par les attaches, il reste au plus quinze appariements sur
ces six points pour fixer les arêtes internes de Y.

Chaque z de Z a exactement deux voisins dans Y : p,z sont non adjacents,
et aucun point de Q n'est voisin de z. Deux points distincts de Z ne
peuvent avoir la même paire de voisins dans Y, sinon cette paire aurait
p et ces deux points pour trois voisins communs. Les onze points de Z
s'identifient donc à onze arêtes distinctes d'un graphe simple sur Y.
Une arête de Γ interne à Y est interdite dans ce graphe, puisqu'elle
a déjà p comme unique voisin commun.

Le degré d'un point de Y dans ce graphe est son nombre de voisins dans Z.
Pour les deux points D il vaut4 ou5, par (1)-(2) ; pour un point B il
vaut1+d_D(b). Les arêtes entre Z et Y restent à choisir avec ces contraintes
et le graphe induit de Z, qui est désormais l'une des quinze forêts.

Le cadre possède37 points et deux relations indépendantes entre leurs
vecteurs de Seidel modulo sept : f=1_P-1_Q et la relation de l'étoile
complète g=4e_p+1_{N(p)}. En effet S(A+4I)=0 modulo sept. Son rang est
donc **au plus35**, jamais36. Au rang global37, un cadre de rang35
demande une dimension résiduelle ; on peut aussi lui ajouter un sommet
avant de viser un bloc non dégénéré de dimension36. La note252 donne
un premier cadre explicite de rang35. **Il reste à borner/énumérer leurs
attaches.** Les75 supports partiels ne constituent pas75 instances
complètes du test. Ce paragraphe corrige la première version du10 octobre,
qui avait oublié la relation de l'étoile complète.

## 6. Réponse sur les normes18 et20 et sur la couverture

Les profils sont connus : tous les vecteurs de normes18 et20 sont
binaires, sur9+9 et10+10 points respectivement ; chaque signe est
indépendant ou contient une seule arête, avec le même nombre d'arêtes
des deux côtés. Le degré croisé est4 plus le degré intérieur. Les
notes171 et176 donnent les histogrammes extérieurs. **Aucun catalogue
complet de leurs cœurs n'est fourni par les données actuelles.**

La présente famille couvre toutes les occurrences de norme16. Elle ne
force pas cette norme au rang37 et ne remplace pas les autres branches
de l'échelle14/16/18/20 annoncée par LAB. Aucune grille ni coclique de22
points n'est supposée forcée au rang37. La nouveauté est la rigidité du
sous-graphe lointain de norme16, pas une exclusion de rang.
