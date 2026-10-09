# 227 — Exclusion des doubles moulins et suppression du coût forfaitaire

9 octobre 2026. Lemme découvert et démontré par LAB, message 433 du pont.
Exploitation de ses conséquences par Codex, sans nouvelle campagne d'audit.

**Résultat.** Deux moulins pondérés distincts ne peuvent avoir la même
projection. Cette exclusion ne dépend ni du rang ni de l'absence de
prismes. Elle permet de remplacer la borne C8 de la note 226 par

    C8 ≤ 872 C2022000 +816 C5683824 +2840 C5691760
         +2836 C127305925 +3312 C128354469 +4448 C245715219.  (1)

La formule (1) concerne la même sous-collection et conserve l'hypothèse
P=0, qui élimine la famille C14. Le terme constant **8 981 280** disparaît,
et les autres coefficients diminuent ou restent égaux. Aucun coût
moulin–cubique n'est omis : ces coûts sont imputés aux supports cubiques.

## 1. Lemme de LAB : pas de doubles moulins

Un moulin pondéré vaut u=2e_v+1_L, où L est constitué des six feuilles
de trois triangles par v. D'après la note 183, deux moulins distincts
ayant même projection auraient des supports disjoints et anticomplets.
Supposons qu'ils existent, de centres v1,v2, et notons s_i(x) le nombre
pondéré de voisins de x dans le moulin i. La relation propre +3 impose
s1(x)=s2(x) à tout point extérieur.

Les centres sont non adjacents et ont exactement deux voisins communs
c,c′, tous deux extérieurs aux moulins. Ils ne sont pas adjacents entre
eux : sinon leur arête aurait v1 et v2 pour deux voisins communs.

Soit d le troisième point du triangle contenant l'arête v1c. Le point d
est extérieur aux deux moulins et n'est pas adjacent à v2 : sinon il
serait le second voisin commun c′, qui n'est pas adjacent à c.

Le point d voit v1 et aucune de ses six feuilles, puisque le voisinage
de v1 est un appariement. Ainsi s1(d)=2. Mais d et v2 sont non adjacents,
et c est déjà l'un de leurs deux voisins communs. Le point d voit donc
au plus une feuille du second moulin : s2(d)≤1. Contradiction.

Une classe de supports cubiques et moulins de même projection contient
donc **au plus un moulin**.

## 2. Nouvelle taille maximale des classes

La note 183 donne, pour le degré pondéré commun d sur l'extérieur d'une
telle classe, Σd=88 et Σd²=128. Cauchy impose au moins

    ceil(88²/128)=61

points extérieurs. L'union des supports disjoints compte donc au plus
38 sommets. Si c est le nombre de supports cubiques et m le nombre de
moulins, on a désormais

    8c+7m≤38,    m∈{0,1}.

Ainsi c≤4 sans moulin, et c≤3 avec un moulin. La classe complète a
**taille au plus quatre**, au lieu de cinq dans la précédente enveloppe.

## 3. Imputer tous les coûts aux cubiques

On réutilise les coûts par paire de la note 226. A,B,C désignent les
types cubiques 2022000,5683824,5691760 ; M désigne un moulin.

| Paire | AA | AB | AC | BB | BC | CC | AM | BM | CM |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Coût maximal | 76 | 64 | 936 | 136 | 920 | 1544 | 544 | 520 | 1296 |

Pour une classe de composition (a,b,c,m), son coût est au plus

    76 binom(a,2)+136 binom(b,2)+1544 binom(c,2)
    +64ab+936ac+920bc+m(544a+520b+1296c).

Sous m∈{0,1} et 8(a+b+c)+7m≤38, cette expression est majorée par

    872a+816b+2840c.                                  (2)

Le calcul entier porte sur les 50 compositions de classes ayant au
moins deux supports. Les cas d'égalité sont (0,0,3,1), (1,0,2,1) et
(0,1,2,1). Les classes à un seul support n'ont aucune collision.
Le programme archive ces 50 inégalités ; il ne refait aucun comptage local.

Pour les trois types à treize arêtes, les classes ont toujours taille
au plus cinq. Leurs coûts diagonaux maximaux sont 1418,1656,2224.
Les coefficients α=(2836,3312,4448) vérifient pour toute paire de types

    4 B_ij ≤ α_i+α_j.

Dans une classe à au plus cinq supports, chaque support appartient à au
plus quatre paires. La somme des coûts est donc au plus la somme des
coefficients α. Avec (2), on obtient (1).

## 4. Portée et fichiers

Il s'agit d'une exclusion complète d'une famille de collisions et d'une
amélioration de la borne C8, non d'une exclusion de C1 ou du rang 37.
Les relations moulin–cubique subsistent dans le comptage. Les masses
sept et neuf restent traitées par les bornes de la note 226.

- Source du nouveau lemme : LAB, message 433.
- Nouvelle combinaison : `code/codex/mass8_no_twin_mills.py`.
- Coefficients et inégalités entières : `data/codex_mass8_no_twin_mills.json`.
- Coûts de paires réutilisés : `data/codex_small_collision_new_channels.json`.

La forme (1) a été transmise à LAB au message 434 pour son optimisation
couplée avec les autres canaux. Aucune conclusion numérique nouvelle
sur le rang 37 n'est présumée ici.
