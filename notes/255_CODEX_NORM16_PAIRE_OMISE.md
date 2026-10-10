# 255 — Norme 16 : la paire omise rigidifie l'unique arête double

10 octobre 2026. Suite théorique des notes251 et253. Aucun rang modulo
sept n'est supposé dans les théorèmes ci-dessous.

**Résultat.** Si D porte une arête de, le troisième sommet z* de son
triangle est isolé dans Z. De plus Z n'a aucun sommet de degré3. Les
sept formes restantes de Z dans cette branche se réduisent à **quatre** :

| Identifiant historique | Z |
|---|---|
| 8 | 2P4 + 3K1 |
| 9 | 3P3 + 2K1 |
| 11 | P4 + P3 + K2 + 2K1 |
| 12 | 2P3 + 2K2 + K1 |

Les formes10,13,14 sont exclues ; la15 l'était déjà par la note253.
En outre le cœur de défaut(2,2,2,2) force D indépendant. Avec les sept
formes de la branche indépendante, cela laisse11 formes de Z et au
plus51 paires cœur/Z au lieu de70. Ce nombre ne compte pas les attaches.

Sur les attaches archivées de la note169, les restrictions de cette note
ramènent les2145 positions d'arêtes D encore possibles à **467**. Il
s'agit d'un décompte étiqueté, sans quotient supplémentaire. Cela ne
ferme pas la norme16.

## 1. Les deux sommets omis ont exactement deux voisins D communs

On reprend les notations de la note253 : R=N_Z(d), T=N_Z(e), chacune
de taille5, R∩T={z*}, et Z\(R∪T)={u,v}. Posons k_x=d_Z(x).
Le budget local L_d>=0 donne

    k_u+k_v >= 4+k_z*.

Ni u ni v ne voit d ou e. Leurs voisinages dans D, de tailles2+k_u
et2+k_v, sont contenus dans les six autres sommets. Par inclusion-exclusion,

    |N_D(u)∩N_D(v)| >= k_u+k_v-2 >= 2+k_z*.

Toute paire distincte de Γ a au plus deux voisins communs. Donc k_z*=0,
k_u+k_v=4 et toutes les inégalités ci-dessus sont des égalités. En particulier :

- z* est isolé dans Z ; ses deux voisins D sont d,e ;
- u,v sont non adjacents et n'ont aucun voisin Z commun ;
- ils ont exactement deux voisins D communs, notés j,k ;
- N_D(u)∪N_D(v)=D\{d,e} ;
- ils n'ont aucun voisin B commun.

La somme des budgets locaux des extrémités vaut alors0. Ainsi L_d=L_e=0,
et chaque simple voisin de d ou e n'a qu'un seul voisin D, comme dans la
note253. Cette preuve exclut directement le cas « z* feuille ».

## 2. Un sommet de degré trois dans Z est impossible

La note251 donne W_Z=sum_x binom(k_x,2)<=4 dans la branche e(D)=1.
Si les deux degrés omis sont(2,2), un sommet supplémentaire de degré3
porterait ce budget à au moins1+1+3=5. Un degré3 éventuel est donc
l'un des deux sommets omis : disons k_u=3, k_v=1.

Le sommet u possède cinq voisins D parmi D\{d,e}, qui est de taille6.
Notons l l'unique sommet de ces six qui ne voit pas u. Les trois voisins
Z de u sont des feuilles, puisque les composantes permises sont K1,K2,
P3,P4,K1,3. Aucune de ces feuilles n'est v : u,v sont non adjacents.
Chacune appartient donc à R\{z*} ou T\{z*}.

Une telle feuille x a trois voisins D : exactement l'une des extrémités
d,e et deux des six autres sommets D. Comme ux est une arête, elle
admet au plus un voisin D commun. Parmi les deux derniers voisins de x,
au moins un doit donc être hors des cinq voisins D de u : **x voit l**.

Les trois feuilles voient ainsi toutes l. Deux d'entre elles voient
en outre la même extrémité d ou e. Cette paire de feuilles a alors
trois voisins communs distincts : u, l, et cette extrémité. Contradiction
avec μ=2. Ainsi Δ(Z)<=2 et k_u=k_v=2.

Les formes10 et13 contenaient une étoile : elles sont supprimées. Dans
la forme14=3K2+P4+K1, les seuls sommets de degré2 sont adjacents ; ils
ne peuvent donc être u,v. Cela donne les quatre formes annoncées.

## 3. Une signature obligatoire dans le graphe des ombres au cœur

Pour x≠y dans D, posons C_xy=|N(x)∩N(y)∩(P∪Q)|, et C_xx=0.
Chaque ligne de C a somme4. Les deux extrémités d,e vérifient C_de=0.
Pour tout autre x dans D, la saturation des paires dx,ex par la
note253 donne

    |N_Z(x)∩{u,v}| = C_dx+C_ex.

L'union des deux voisinages D de u,v couvre les six autres doubles,
et leur intersection est exactement{j,k}. On obtient donc la signature

    {C_dx+C_ex : x dans D\{d,e}} = {2,2,1,1,1,1},

les deux valeurs2 étant précisément portées par j,k. Les sommets j,k
partagent déjà u et v, donc C_jk=0. Chacun des quatre autres doubles x
voit exactement l'un de u,v ; ainsi j et x, puis k et x, ont déjà au
moins un voisin Z commun. Par conséquent

    C_jx<=1 et C_kx<=1 pour x hors{d,e,j,k}.

Ce sont des restrictions sur les seules attaches au cœur, avant toute
énumération D–Z. `norm16_edge_omitted_pair.py` les applique aux données
existantes sans recalculer les cinq cœurs ni les478 attaches :

| Cœur de défaut | Arêtes après note253 | Après cette note |
|---|---:|---:|
| 8 | 909 | 247 |
| 6+2 | 497 | 66 |
| 4+4 | 499 | 136 |
| 4+2+2 | 184 | 18 |
| 2+2+2+2 | 56 | 0 |
| Total | 2145 | 467 |

Le dernier zéro a aussi une preuve directe : pour ce cœur, les arêtes
de défaut sur P, comme sur Q, sont quatre paires disjointes de
multiplicité2. Deux ombres D ont donc une intersection sur P de taille0
ou2, et de même sur Q. Toutes les valeurs de C sont paires. La signature
qui exige quatre valeurs1 est impossible. **Pour ce cœur, D est forcément
indépendant.**

## 4. Premier cadre de la branche à une arête

Le compteur D–Z accepte désormais les deux lignes des extrémités fixées.
Elles sont classées modulo Aut(Z), puis les six autres lignes sont
énumérées modulo le stabilisateur de ces deux lignes. Les égalités de
la note253 et les bornes de voisins communs sont imposées avant les
mineurs spectraux exacts de la note254. Son Schur utilise bien
H=3I-A_D+J/9-Ct M^-1 C, avec l'arête de dans A_D.

Pilote sur le cœur0, attache4 : après le théorème, seule l'arête D(1,4)
reste. Les34 classes de paires de lignes sur les quatre forêts sont
entièrement parcourues. Les mineurs d'ordre<=4 laissent33 incidences ;
la PSD complète exacte8x8 en laisse **deux**, toutes deux sur la
forêt9=3P3+2K1 et de rang de Seidel33 modulo7. Ce sont des bases locales,
pas des graphes à99 sommets. Elles ne sont pas quotientées par toutes
les symétries possibles de D.

Une base et les domaines nécessaires de ses64 simples sont exportés
dans `codex_norm16_typed_world35_edge_0_4_9.json` :48 cellules,
1818 colonnes locales, budget W_B=1. Les domaines excluent aussi les
paires dont le quota de voisins communs est déjà saturé dans la base.
Ils ne fixent pas les produits mutuels des futurs sommets dans W36.
Deux sommets distincts d'une cellule ne sont pas obligatoirement
représentés par deux colonnes distinctes : le moteur doit gérer leurs
vecteurs résiduels et leurs produits.

Les467 positions restantes n'ont pas été toutes cataloguées. Le moteur
de cellule de LAB reste nécessaire pour poursuivre les bases survivantes.

## Reproduction

    python code/codex/norm16_edge_omitted_pair.py
    g++ -std=c++20 -O3 code/codex/norm16_dz_catalogue.cpp -o code/codex/norm16_edge_catalogue.exe
    python code/codex/norm16_edge_catalogue.py --orbit 4 --directory data/codex_norm16_edge_catalogue_0_4_refined
    python code/codex/norm16_typed_world35.py --source data/codex_norm16_world35_edge_seed.json --output data/codex_norm16_typed_world35_edge_0_4_9.json

Les données de la note253 sont conservées comme état historique. Cette
note réduit leur liste ; elle ne change pas rétroactivement leur numérotation.
