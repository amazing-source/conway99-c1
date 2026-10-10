# 260 — Le double omis d'un P4 et une entrée qui survit au bord

10 octobre 2026. Exploration après la note 259. **Aucune nouvelle attache
entière n'est exclue.** On obtient une description courte d'un P4 dans Z,
puis une réduction finie d'une sous-branche des quatre attaches à coupure
de poids deux. Cette sous-branche a encore des survivants.

## 1. Géométrie imposée par un P4

Supposons que x–a–b–y soit une composante de Z. Pour z∈Z, écrire
E_z=N(z)∩D. Les feuilles ont |E_x|=|E_y|=3 et les centres
|E_a|=|E_b|=4, par d_D(z)=2+d_Z(z).

Puisque a,b sont adjacents, |E_a∩E_b|≤1. Si cette intersection était
vide, E_a et E_b partitionneraient les huit doubles. Or x a au plus un
voisin D commun avec a (adjacent) et au plus un avec b (ils partagent
déjà a comme voisin Z). Il aurait donc au plus deux voisins D,
contradiction.

Ainsi E_a∩E_b={d}. Il existe un unique double e omis par leur union.
Le double d ne touche ni x ni y : sinon une arête d–a ou d–b aurait
deux voisins communs. Chaque feuille doit toucher e, et exactement un
double dans chacune des deux parties de taille trois. En posant
A=E_a\{d}, B=E_b\{d}, on a donc

    D={d,e} ⊔ A ⊔ B,         |A|=|B|=3,
    E_a={d}∪A,              E_b={d}∪B,
    E_x={e,a_i,b_j},         E_y={e,a_k,b_l}.

Les deux couples (a_i,b_j),(a_k,b_l) sont différents, car x,y ne
peuvent partager trois doubles. La preuve utilise les seules bornes
λ=1, μ=2 et les degrés de la partition norme 16. Elle ne suppose pas
le rang 37. La contrainte sur les centres s'inscrit dans les bornes
d'union déjà utilisées dans les notes 251 et 256.

Dans les quatre attaches à coupure U∪V de la note 257, a et b voient
chacun deux doubles de chaque côté. Leur double commun d et leur
double omis e appartiennent donc au même côté de la coupure.

## 2. Sous-branche C_de=1 et Z=P3+P4+4K1

On se limite ici aux attaches 0,1,21,22 du cas 3 et à la forêt
historique 2. C_de désigne le nombre de voisins communs de d,e au
cœur. La restriction C_de=1 est une hypothèse de cette sous-branche,
pas une propriété de tous les P4.

La forme de la section 1 permet de construire les quatre colonnes du
P4 sans choisir les sept autres sommets Z. Pour chacune des quatre
attaches, on obtient 88 placements après normalisation du renversement
du P4 et application des capacités C_ij+nombre de Z communs≤2.

Le centre du P3 restant doit voir quatre doubles T. Toute paire de T
doit encore disposer d'une place de voisin Z commun après le P4 ;
de plus |T∩E_z|≤2 pour chacun des quatre sommets du P4. **80 des
88 placements ne permettent aucun tel T.** Dans chacun des huit
autres, T est unique. C'est une obstruction entière de capacité sur
huit doubles, sans programme linéaire.

On complète ensuite les deux feuilles du P3 et les quatre isolés.
Les isolés portent chacun une paire U–V ; leur choix est un petit
problème de capacités avec les degrés résiduels des huit doubles.
Il reste 32 supports normalisés par attache, soit 128 au total.
Le quotient par isomorphismes préservant P,Q,D,Z comporte 64 classes.
Chaque correspondance est enregistrée par une permutation explicite.

Le test exact du Schur de 3I−A+J/9 laisse 56 de ces classes. Ces
chiffres concernent uniquement cette sous-branche ; ils ne mesurent
ni les attaches restantes de C1, ni des complétions du SRG.

## 3. La limite rencontrée et le support transmis

Le test de bord de la note 258 a été essayé sur une partie de ces
classes. Plusieurs donnent des certificats entiers d'infaisabilité,
mais d'autres restent numériquement faisables et passent la PSD
exacte. La série de tests a été interrompue à ce constat. Il n'est
donc pas justifié d'exclure toute la sous-branche C_de=1.

Une entrée qui passe ces deux étapes est :

    cas 3, attache 0, forêt 2,
    D_Z_row_masks = [209,308,78,1570,658,297,101,1050].

Son rang de Seidel modulo sept vaut exactement 33. Le modèle de bord
est faisable en variables réelles (résultat numérique) ; aucune
réalisation entière, ni aucun SRG, n'est affirmé. Le fichier
`data/codex_norm16_typed_world35_tight_boundary_survivor.json` fournit
les 50 cellules, leurs multiplicités totalisant 64, et 3423 colonnes
locales pour une application du moteur de rang résiduel de LAB.
Cette entrée résiste aux filtres précédant ce moteur, contrairement
au support exclu sans rang dans la note 258.

Un autre essai a ajouté toutes les arêtes B-B aux équations exactes
cœur-B, avec les capacités D-B nécessaires : le pilote cas3/0 est
UNKNOWN à 30 secondes. Le modèle avec seulement le P4 connu et les
sept autres Z non placés laisse aussi des relaxations faisables.
Ces essais ne sont pas des exclusions supplémentaires.

## 4. Fichiers et portée reproductible

`code/codex/norm16_p4_c1_reduction.py` réalise la réduction de la
section 2. Son mode normal énumère les seuls petits supports décrits
ci-dessus et calcule leur PSD exacte. L'option `--solve` est désormais
bornée par `--max-boundaries` (un essai par défaut) et s'arrête sur
une relaxation faisable. Ne pas reprendre une campagne complète de
certificats pour cette branche déjà connue comme survivante à ces
filtres.

`data/codex_norm16_p4_c1_reduction.json` conserve les supports, leurs
permutations et les essais de bord réellement terminés. Les verdicts
numériques sans certificat entier ne sont pas des exclusions prouvées.

`code/codex/norm16_p4_boundary.py` contient la relaxation ne fixant
que le P4. L'option `--full-b` de `norm16_tight_transport.py` contient
l'essai d'arêtes B-B complètes. Aucun de ces modèles n'est un test
complet d'existence du graphe à 99 sommets.
