# 257 — Norme 16 : connexité des ombres et huit exclusions supplémentaires

10 octobre 2026. Suite des notes 251, 255 et 256, sans hypothèse de rang.

**Théorème.** Dans toute occurrence de norme 16, le multigraphe C des
intersections au cœur entre les huit doubles est connexe. Le résultat
vaut pour des intersections paires ou impaires et pour les deux branches
de D. Dans le catalogue des 478 attaches, il exclut 17 attaches entières,
dont neuf déjà exclues dans la note 256 et **huit supplémentaires**.

Les nouvelles exclusions sont les attaches 45, 50, 51, 52, 53, 54 du
cas 2 (cœur 4+4), et 18, 19 du cas 3 (cœur 4+2+2). Les indices sont
ceux des fichiers, à partir de zéro.

Le résultat porte sur toute complétion de ces attaches. Il ne dépend
ni d'un catalogue de voisinages lointains ni d'une recherche interrompue.

## 1. Données réutilisées

Écrire f=1_P−1_Q, avec |P|=|Q|=8, et reprendre la partition

    cœur P∪Q : 16 ; doubles D : 8 ; simples B : 64 ; lointains Z : 11.

Chaque point du cœur voit exactement deux doubles et chaque double voit
quatre points du cœur. Pour d≠e, soit C_de le nombre de leurs voisins
communs dans le cœur, avec C_dd=0. Alors

    0 ≤ C_de ≤ 2,                 Σ_e C_de = 4.                 (1)

La note 251 donne, pour chaque double d,

    |N_Z(d)| = 4 + d_D(d).                                    (2)

Deux doubles ont au plus deux voisins communs au total, donc

    |N_Z(d)∩N_Z(e)| ≤ 2−C_de.                                 (3)

Cette dernière borne reste nécessaire lorsqu'ils sont adjacents : leur
borne effective est alors plus forte. Aucune indépendance de D n'est
supposée dans la preuve suivante.

## 2. Borne d'union et connexité

Pour U⊂D de taille k, poser c(U)=Σ_{d<e dans U} C_de. L'inégalité
d'union à deux termes et (2)-(3) donnent

    11 ≥ |⋃_{d∈U} N_Z(d)|
       ≥ 4k + Σ_{d∈U} d_D(d) − [k(k−1)−c(U)].                 (4)

Si U est une composante connexe de C, (1) implique c(U)=2k.
La composante a au moins trois sommets, puisque chaque multiplicité
est au plus deux. Si C était non connexe sur huit sommets, une de ses
composantes aurait donc k=3 ou k=4. Dans les deux cas, (4) donne

    11 ≥ 7k−k² + Σ_{d∈U} d_D(d) ≥ 12,

contradiction. Cela prouve le théorème.

Pour k=4, la contradiction se lit particulièrement simplement : quatre
doubles demandent au moins 16 incidences dans Z ; leurs six paires ne
peuvent avoir au total que quatre voisins communs dans Z. Leur union
devrait donc contenir au moins 12 des 11 points disponibles.

Cette preuve étend l'exclusion 2C4 de la note 256 à tout multigraphe
d'intersections non connexe, sans hypothèse de parité.

## 3. Cas d'égalité : restrictions sur quatre attaches encore ouvertes

Le même argument fournit une réduction supplémentaire. Supposons

    4|U| − |U|(|U|−1) + c(U) = 11.                            (5)

Toutes les inégalités de (4) sont alors des égalités. Il en résulte :

1. Aucun sommet de U n'est incident à une arête de D.
2. Chaque sommet de Z voit exactement un ou deux points de U.
3. Chaque paire d,e de U a exactement 2−C_de voisins communs dans Z.
4. Aucun simple ne voit deux points de U.

Pour le deuxième point, si r points de U voient un même z, la contribution
de z à la borne d'union est r−binom(r,2). Elle égale l'indicatrice r>0
exactement pour r≤2. L'égalité avec |Z|=11 exige aussi que chaque z
soit couvert. Le troisième point s'ensuit de la saturation de la somme
des bornes (3), puis le quatrième de μ=2.

Dans quatre attaches connexes du catalogue, D se partitionne U∪V avec
|U|=|V|=4 et c(U)=c(V)=7. Autrement dit, le multigraphe C possède une
coupure de poids deux. Le cas d'égalité s'applique des deux côtés :

    D indépendant ; 1≤|N_D(z)∩U|, |N_D(z)∩V|≤2 ;
    |N_D(b)∩U|, |N_D(b)∩V|≤1.

En particulier d_D(z)≤4, donc d_Z(z)≤2, et d_D(b)≤2. Les étoiles K1,3
sont interdites dans Z pour ces attaches. Parmi les sept anciennes
forêts de la branche D indépendant, seules les IDs 2, 3, 5, 6, 7 peuvent
subsister. Les quatre attaches sont toutes du cas 3 :

| Attache | U | V |
|---|---|---|
| 0 | 0,1,2,3 | 4,5,6,7 |
| 1 | 0,1,2,3 | 4,5,6,7 |
| 21 | 0,1,6,7 | 2,3,4,5 |
| 22 | 0,1,4,5 | 2,3,6,7 |

Il y a exactement cinq sommets Z voyant deux points de U et six en
voyant un, et de même pour V : les quatre doubles de chaque partie ont
ensemble 16 voisins dans Z, comptés avec multiplicité.

La branche à une arête était déjà absente pour ces quatre attaches
dans les données de la note 255. Les contraintes sur Z et B ci-dessus
sont les conséquences supplémentaires à exploiter ; ces quatre attaches
ne sont pas déclarées exclues.

## 4. Application au catalogue, sans nouvelle énumération de graphes

Le programme `code/codex/norm16_shadow_connectivity.py` lit les 478
attaches archivées. Il calcule C, ses composantes, les sous-ensembles
violant (4) et ceux satisfaisant (5). Le fichier
`data/codex_norm16_shadow_connectivity.json` conserve les sous-ensembles
témoins et les entiers de chaque certificat.

Les 17 attaches non connexes sont :

| Cas | Attaches |
|---|---|
| 2 | 44,45,46,50,51,52,53,54,81,82,84,85 |
| 3 | 18,19,26 |
| 4 | 0,3 |

Neuf figuraient déjà dans la note 256. Avec l'exclusion spectrale
distincte du cas 0/attache 52, les notes 256 et 257 couvrent **18 attaches
entières sur 478**. Les 460 autres ne sont pas exclues par ces deux notes ;
ce chiffre ne recompte pas les exclusions partielles ou combinées
d'autres notes. La norme 16 et C1 restent ouverts.

Les nouvelles exclusions retirent aussi 29 positions d'arêtes D de la
liste étiquetée de la note 255 : cette liste passe de 467 à 438.
Il ne s'agit pas d'un nombre de graphes à 99 sommets.

Commande, bibliothèque standard Python uniquement :

    python code/codex/norm16_shadow_connectivity.py

## 5. Explorations non concluantes à ne pas recommencer à l'identique

Avant le comptage ci-dessus, un modèle couplant les moments D-Z et les
attaches B au cœur et à D a été testé sur les cinq attaches paires
restantes et les trois forêts autorisées. Les quinze modèles possèdent
un témoin entier. Ils n'excluent donc aucune de ces attaches. Les scripts
`norm16_even_margins_probe.py` et `norm16_even_margins_integer.py`, ainsi
que leurs données, enregistrent cette limite ; ces témoins ne construisent
pas les arêtes entre simples.

Un autre pilote choisit un z isolé dans Z, puis ses douze voisins simples.
Le cadre cœur+D+z+N_B(z) a 37 sommets. Les douze simples forment un graphe
biparti simple sur P∪Q : degré 1 sur les huit points du cœur vus par les
deux doubles voisins de z, degré 2 ailleurs. La simplicité vient de μ=2 :
deux simples d'une même cellule partageraient p,q,z. Le voisinage complet
de z doit induire 7K2. Comme dans le cadre différent de la note 251, f et
la relation de l'étoile imposent un rang de Seidel au plus 35.

Les essais bornés de `norm16_even_isolated_star.py` n'ont trouvé ni cadre
37 compatible avec la PSD complète ni exclusion exhaustive : **UNKNOWN**.
Un seul couple de doubles a été testé par essai, pas une couverture des
couples. Les coupes de Rayleigh globales ajoutées au dernier essai ont
des coefficients entiers ; les flottants servent uniquement à choisir
un vecteur candidat, dont la négativité est ensuite calculée exactement.
Il n'y a donc aucune nouvelle exclusion issue de ce pilote, ni de nouveau
cadre de rang 35 à transmettre à un moteur résiduel.

La suite utile est l'exploitation des coupures de poids deux et de leurs
contraintes exactes sur B et Z, ou une autre obstruction pour le C8 pair.
Elle ne consiste pas à relancer les mêmes comptages faisables.
