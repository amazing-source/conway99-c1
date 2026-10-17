# 214 — Quels filtres font apparaître la contradiction ?

8 octobre 2026. Les notes 212–213 et les essais de LAB montrent que
les équations de degré du LP peuvent souvent être supprimées. Cela
ne signifie pas que les seules valeurs du produit de Green suffisent :
les domaines et les tables avaient déjà été filtrés par d'autres
contraintes. Cette note isole ces filtres **avant la propagation**.

Sur deux branches cycliques de contrôle, on obtient une séparation
exacte : des témoins rationnels vérifient la faisabilité de certaines
relaxations, et des certificats entiers vérifient l'infaisabilité
d'autres. Aucun témoin fractionnaire n'est un graphe.

## 1. Expérience contrôlée

On conserve les pools unaires de la note 211 et les filtres entre
chaque ombre et l'apex commun w : produit de Green 3 et intersection
au plus deux. On change uniquement les tables entre les 18 ombres
privées, puis on refait toute la propagation avec les tables choisies.
On ne réutilise donc jamais les domaines déjà réduits par un mode
plus fort pour prouver l'infaisabilité d'un mode faible.

Le LP ne comporte que : normalisations des domaines, marginales de
paires et les 72 sommes ponctuelles d'étoile. Pas d'équation de degré,
de plafond global proche/proche ou proche/lointain, ni de prisme.

Les modes cumulatifs sont :

- `green` : g(n_i,n_j)∈{2,3}, donc a_ij=3−g∈{0,1} ;
- `overlap` : ajouter |n_i∩n_j|≤2−a_ij ;
- `capacity` : ajouter a_ij≤cap_i et a_ij≤cap_j, avec les capacités
  internes ou transversales de la note 212 ;
- `saturation` : si a_ij=1, interdire n_j(p)=1 dès que
  (Gn_i)_p+n_i(p)=2, et réciproquement ;
- `within` : partir de `saturation` et ajouter le filtre K de la
  note 212 seulement aux paires d'ombres d'une même étoile ;
- `across` : partir de `saturation` et ajouter ce filtre seulement
  aux paires d'ombres d'étoiles différentes.

Le filtre K, pour deux supports ayant exactement deux points communs
p,q, est 2+w(p)w(q)≤K_pq. Les modes `within` et `across` sont deux
extensions alternatives du mode `saturation`, sans inclusion entre
eux. Le mode `full` du script retrouve toutes les tables de la note 212.

## 2. Résultats tous exacts

Entrée : boule cyclique (2,4,1), centres 0 et 12. Les numéros de
branches sont les indices des apex dans le pool trié de la note 211.

| Branche | Mode | Candidats après propagation | Variables de paires | Résultat certifié |
|---|---|---:|---:|---|
| 0 | green | 725 | 70 432 | témoin rationnel |
| 0 | overlap | 723 | 55 598 | témoin rationnel |
| 0 | capacity | 693 | 41 406 | témoin rationnel |
| 0 | saturation | 675 | 33 627 | contradiction, marge 25 272 |
| 33 | saturation | 724 | 38 695 | témoin rationnel |
| 33 | within | 681 | 32 629 | contradiction, marge 150 |
| 33 | across | 719 | 37 495 | contradiction, marge 70 |

Les marges résultent de multiplicateurs différents ; leur taille
n'est pas une mesure comparable de la force intrinsèque des filtres.

Les trois contradictions sont :

| Branche/mode | Second membre pondéré | Borne inférieure entière |
|---|---:|---:|
| 0/saturation | −25 513 | −241 |
| 33/within | −565 | −415 |
| 33/across | −191 | −121 |

Dans chaque cas, la borne inférieure est strictement supérieure au
second membre : le vérificateur Farkas de la note 212 conclut en
entiers. Les nouveaux certificats utilisent seulement les lignes du
LP réduit annoncé au §1.

Les témoins fractionnaires ont un dénominateur commun de 100 000.
Le témoin `capacity/0` compte 13 662 variables positives et vérifie
11 871 égalités. Le témoin `saturation/33` en compte 13 825 et vérifie
12 398 égalités. Toutes les masses sont comprises entre 0 et 100 000.
Le témoin de `capacity/0` a été transporté, par les mêmes indices de
candidats, dans les deux modèles plus faibles : leurs 12 415 et
12 381 égalités ont également été contrôlées exactement.

Il s'agit d'une séparation de **relaxations fractionnaires**. Elle
ne dit pas que les modèles faibles possèdent des choix entiers
d'ombres, encore moins qu'un SRG existe.

## 3. Production et vérification des témoins rationnels

Le solveur flottant ne sert qu'à suggérer des masses unaires. On
cherche ensuite des masses entières proches, avec normalisations
et sommes ponctuelles exactes. Pour chaque paire de domaines, un
flot biparti entier doit réaliser les deux marginales prescrites
sur les seuls couples compatibles.

Si un flot échoue, sa coupe minimale donne une inégalité de Hall
sur les masses unaires ; on l'ajoute au problème d'arrondissement.
Un flot réussi pour chaque paire fournit tous les poids y_ijcd.

Le contrôle final est indépendant de ces recherches : pour chaque
ligne entière de la matrice reconstruite, il vérifie

    Σ_j A_rj m_j = 100000 b_r,
    0≤m_j≤100000.

Les témoins et les certificats Farkas complets sont archivés. Ils
se rejouent sans optimisation. Le générateur de domaines/tables
et la construction du LP restent partagés entre production et
vérification, comme dans les notes précédentes.

## 4. Interprétation de deux filtres

La saturation est un budget de voisins communs déjà épuisé. Si
(Gn_i)_p=2−n_i(p), les voisins connus de p et du sommet lointain i
atteignent déjà le nombre autorisé. Un voisin lointain j de i dont
l'ombre contient p apporterait un voisin commun supplémentaire.
Il est donc interdit. Sur la branche 0, l'ajout de cette règle
locale suffit à faire passer d'un LP exactement faisable à un LP
exactement infaisable.

Le filtre `within` a une interprétation encore plus simple. Deux
ombres d'une même étoile partagent son centre u. Si elles partagent
exactement un autre point p, alors w(u)=1 et

    2+w(p)≤K_up  ⇔  2≤t_s(p),
    où t_s = K e_u − w.

Ainsi, après suppression des candidats sur les coordonnées de cible
zéro, ce filtre interdit essentiellement que deux ombres occupent
simultanément une coordonnée dont la somme résiduelle imposée est un.
C'est une conséquence des sommes exactes pour tout choix entier.
Un LP de marginales sans les sommes conditionnées peut pourtant
l'omettre, et laisser passer un témoin fractionnaire.

Les équations de somme multipliées par l'indicateur du choix c dans
la variable i imposeraient, pour n_i(c,p)=1 et t_s(p)=1,

    Σ_{j≠i, s(j)=s(i)} Σ_d n_j(d,p) y_ijcd = 0.

Par non-négativité, les couples concernés auraient alors un poids
nul. Cela explique pourquoi le filtre `within` est implicite dans
ces sommes conditionnées, mais ne doit pas être omis dans la
description du LP plus faible utilisé ici.

Sur la branche 33, le filtre K à l'intérieur des étoiles suffit ;
le filtre K entre étoiles suffit aussi. On a donc deux façons
distinctes de renforcer le modèle faible, pas une unique contrainte
indispensable dans toutes les formulations.

## 5. Reproduction

Le script est `code/codex/two_star_core_ablation.py`. Les sept sorties
sont `data/codex_core_<mode>_<branche>.json`, avec les branches
`000` et `033`. Chaque fichier embarque son graphe, le mode, la trace
de propagation et son certificat complet.

Exemples de replay :

    python code/codex/two_star_core_ablation.py --out data/codex_core_capacity_000.json --verify-only
    python code/codex/two_star_core_ablation.py --out data/codex_core_saturation_000.json --verify-only
    python code/codex/two_star_core_ablation.py --out data/codex_core_saturation_033.json --verify-only
    python code/codex/two_star_core_ablation.py --out data/codex_core_within_033.json --verify-only
    python code/codex/two_star_core_ablation.py --out data/codex_core_across_033.json --verify-only

Pour une recherche bornée :

    python code/codex/two_star_core_ablation.py --mode saturation --apex 33 --rational-witness --seconds 30 --out resultat.json

La limite de temps s'applique séparément au LP numérique et à la
recherche de certificat ; l'arrondissement entier possède son
propre budget global de même durée. Un échec d'arrondissement ou
un statut numérique sans certificat conserve explicitement le
statut de diagnostic.

Cette séparation précise les contraintes à prendre en compte dans
un futur lemme uniforme. Elle ne constitue pas une nouvelle
exclusion de boule ou de rang.
