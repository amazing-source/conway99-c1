# 249 — Trois prismes jumeaux hors grille imposent des apices indépendants

9 octobre 2026. Exploration consécutive au message LAB 517.

**Résultat nouveau.** Si trois prismes distincts ont même projection sur
l'espace propre -4 et ne sont pas contenus dans une grille, leurs trois
apices communs sont indépendants. Les configurations avec une ou deux
arêtes entre ces apices sont exclues, par la preuve ci-dessous.

**Conséquence sans grille :** avec les notations des notes 185 et 194,

    C14 <= P,       C14 + 2 tau <= 2P.                     (1)

La seconde inégalité est nouvelle. Elle ne prouve pas qu'une classe de
prismes hors grille a au plus deux membres : le cas de trois membres
avec apices indépendants reste ouvert. Aucun rang n'est exclu.

**Contexte corrigé.** LAB a retiré au message 518 la quasi-contradiction
numérique proposée au 517 : son numérateur contenait des représentants
omis dans la collection de notre borne 31 976. Il rapporte un seuil
corrigé de 25 201, avec d'autres canaux encore trop coûteux. Aucune
campagne de boules n'est lancée sur cette proposition. Le présent
lemme n'utilise ni ce budget ni le rang 37.

## 1. Données communes d'une classe

On reprend la géométrie de la note 194, sans nouveau calcul de réseau.
Les prismes X_i d'une même classe sont disjoints et anticomplets. Ils
ont les mêmes trois apices Theta={a,b,c}, et le même ensemble B de
soixante sommets ayant exactement un voisin dans chacun des X_i.
Chaque apex complète un barreau de chaque prisme en triangle.

Si d_Theta(a) est le degré d'un apex a parmi les trois apices,

    |N(a) inter B| = 4 - 2 d_Theta(a).                    (2)

Ces assertions découlent de u=(A-3I)1_X=2*1_Theta+1_B et
(A+4I)u=12*1. Une classe hors grille a au plus trois membres (note194).

## 2. Un apex de degré un interdit trois membres

Supposons d_Theta(a)=1, avec a adjacent à b mais pas à c. Par (2),
il existe un sommet w dans B adjacent à a. Dans chaque prisme X_i,
notons v_i l'unique voisin de w. Il ne peut appartenir :

- au barreau de a : l'arête a-v_i aurait son partenaire de barreau
  et w pour deux voisins communs, contrairement à lambda=1 ;
- au barreau de b : a et v_i sont non adjacents et ont déjà deux
  voisins communs, b et le sommet de la même face triangulaire que
  v_i sur le barreau de a. Le sommet w serait un troisième.

Tous les v_i appartiennent donc au barreau de c. Ils sont autant de
voisins communs distincts de w et c. Il ne peut y en avoir trois,
puisque toute paire distincte a au plus deux voisins communs.

Ainsi, dès que la classe a au moins trois membres, Theta ne possède
aucun sommet de degré un. Un graphe sur trois sommets sans degré un
est vide ou complet. Le cas complet donne une grille avec chaque X_i.
Dans le cas hors grille, Theta est donc indépendant. Cela élimine
exactement les deux formes non vides et non complètes de Theta.

## 3. Deux nouveaux couplages de comptage

L'identité de la note 185 est

    2 C14 = sum_prismes e(Theta).

Chaque support C14 (grille privée d'un sommet, sans supposer qu'il se
complète en grille) contient deux prismes. Dans un graphe sans grille,
une classe de taille m=1,2,3 et d'apices ayant e arêtes contribue

    m à P,   binom(m,2) à tau,   m*e/2 à C14.

Pour m=1,2 on a e<=2. Pour m=3 le nouveau lemme impose e=0. L'inégalité

    m*e/2 + 2 binom(m,2) <= 2m

vaut donc dans chaque classe. En sommant, on obtient la seconde partie
de (1). La première vient déjà de e<=2. Notamment tau=P impose C14=0.

Posons aussi

    T = sum_classes binom(m,2)*e.

Ce nombre est exactement celui des paires de supports C14 de même
projection ayant une intersection de deux sommets : supprimer cette
intersection donne deux prismes jumeaux ; l'intersection est une arête
entre leurs apices. Réciproquement chaque telle arête donne une paire.
Pour m=3 sa contribution est nulle ; pour m=2 sa contribution à T
égale sa contribution à C14. Ainsi

    T <= C14,     T <= 2 tau.                             (3)

La borne issue seulement de m<=3 aurait donné T<=2 C14.

## 4. Une borne exploitable du canal (4,4) hors masse six

Le message 517 demandait les coûts hors C6. Ils ne deviennent pas tous
nuls sans grille. Voici toutefois une borne complète pour la famille
(4,4) contre elle-même et les anciennes familles équilibrées, en
retirant son canal C6 déjà inclus dans le coût 31 976 de la note195.

Noter A,B,C les comptes des trois types cubiques 2022000,5683824,5691760
(ces lettres désignent ici des comptes, pas les ensembles du §1), et
D,E,F ceux des types à treize arêtes 127305925,128354469,245715219.
La somme des pertes de masses sept et huit de cette famille satisfait

    C_44,hors6 <= 272 Omega
                 +108 A+64 B+160 C+100 D+144 E+64 F
                 +(608/3) C14+(160/3) T.                 (4)

En particulier, par (3), le dernier couple de termes est <=256 C14.

Justification du changement sur les cubiques : une classe contient
au plus un moulin pondéré (lemme LAB, note227). Les supports sont
disjoints et anticomplets, et leurs moments imposent au moins 61 points
extérieurs. La classe contient donc au plus quatre cubiques sans
moulin, ou trois cubiques avec un moulin. Le nombre de partitions d'un
cubique est t=6,4,8 selon son type ; celui du moulin est douze.
Avec un moulin, le coût total est au plus

    sum_i (t_i^2+12 t_i),

car il y a au plus trois cubiques et
sum_{i<j}t_i*t_j <= sum_i t_i^2. Sans moulin, il est au plus
(3/2)sum_i t_i^2, encore inférieur à la même expression puisque t_i<=8.
Les coefficients sont donc 108,64,160. Aucun coût forfaitaire pour
les 3465 moulins n'est nécessaire.

Le terme 272 Omega est celui de la note185. Les coefficients 100,144,64
sont ceux de la note183 pour les supports à treize arêtes. Pour C14,
sa positivité de Gram donne 12n0+n1<=38m+10n2 ; une paire disjointe
coûte au plus64. D'où (608/3)C14+(160/3)n2, puis n2=T par le §3.

Portée : (4) ne doit pas être ajoutée à une ancienne formule contenant
déjà les mêmes pertes. Elle ne couvre pas toute la collection avec
(6,3),(7,1),(9,0). Pour la sous-collection de sommes 0,+3,-3, le coût
C7<=5402 Omega de la note226 ne requiert pas P=0. En revanche ses bornes
complètes C8 et C9 utilisaient P=0 : sans grille ne suffit pas à les
réutiliser telles quelles. Les changements de somme avec triangle
négatif non annulé (note183 §5) ne disparaissent pas avec les grilles.

## 5. Deux essais ciblés et leur limite

`nongrid_triple_prism_boundary.py` fixe les dix-huit points des trois
prismes et les trois apices. Il impose seulement les multiplicités des
voisinages extérieurs, les degrés et les nombres de voisins communs.
Il donne 344 profils pour Theta vide, 248 pour une arête, 199 pour deux.
Le premier modèle est numériquement faisable (résidu maximal 2,85e-14).
Les deux autres sont infaisables numériquement ; leur exclusion est
désormais établie par la preuve du §2, sans dépendre du solveur.
La faisabilité du premier modèle ne construit pas un graphe.

Une seule optimisation nouvelle du coût C6 a été faite en imposant les
apices indépendants dans le modèle de paires existant. Son certificat
rationnel, contrôlé sur les colonnes et leurs bornes, donne

    coût <= 31977714286763/1000000000,
    donc coût <= 31976 par intégralité et parité.

Ce modèle ne donne donc aucune amélioration du plafond 31976. Il ne
force pas un troisième prisme : le lemme permet d'y envoyer toutes les
paires d'une classe de taille trois, mais la réciproque n'est pas imposée.
Cette piste n'est pas prolongée par un balayage.

Enfin, le plancher14430 cité au message517 concernait les paires de
grilles (note197, amélioré à16496 en198), pas les paires hors grille.
Il ne fournit pas un plancher pour ces dernières.
