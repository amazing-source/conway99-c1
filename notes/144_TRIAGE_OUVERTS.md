# 144 — Triage des 135 réseaux ouverts de la ligne (C) : types de blocs locaux

*27/09 nuit. C1. code/blockcatalog.py : 156 réseaux en 84 s, 37 Mo, sans aucune recherche. Données :
data/finishC/triage/catalog.jsonl. Tracker de C2 (lab) : 21 exclus, 2 partiels (0, 87), 133 ouverts.*

**Pour chaque réseau** : les racines de U, et les nouvelles racines de chaque voisin pair, triées par classe de l'ombre. Chaque
composante X du voisin qui contient de nouvelles racines, avec le sous-système Y des racines de U qu'elle contient (type de bloc
« X>Y »). Enfin, le nombre de vecteurs de norme 3 qui ne touchent AUCUNE nouvelle racine (m = 0 ; m est le même dans les deux
voisins).

## Faits
1. **Seuls 4 réseaux ouverts sont rigides** : 0, 10, 44, 87. Ce sont les seuls où les lemmes de notes/143 (K, T, T₀, H)
   s'appliquent tels quels, puisque les hits y sont fixés par les y.
2. **Dans les 131 autres, il y a toujours au moins 128 vecteurs de norme 3 (sur 2048 à signe près) qui ne touchent rien.** Les u
   ne sont donc JAMAIS forcés de toucher par le seul comptage : le motif des hits n'est plus déterminé par les y. La part des
   non-touchants a pour quartiles 0,06 / 0,39 / 0,53 / 0,66 / 1.
3. **131 réseaux ont de nouvelles racines dans LES DEUX voisins.** Les mêmes 7 h doivent alors satisfaire les identités de bloc
   dans deux cadres de Niemeier à la fois. La famille rigide n'avait qu'un voisin actif. C'est un levier NEUF, jamais testé.
4. **93 types de blocs distincts, mais 8 familles** (nombre de réseaux ouverts qui en contiennent) :

| famille | réseaux ouverts |
|---|---|
| A>A+A | 112 |
| A>A(n−1) | 57 |
| D>A(n−1) | 54 |
| D>mixte | 51 |
| E (rang max ou corang 1) | 33 |
| D>D(n−1) | 19 |
| D>D+D | 10 |
| A1>0 | 4 |

   Chaque famille a une théorie locale uniforme, à paramètres près. D>D+D est notes/143 ; E₇>A₇ est notes/48 de C2.

## Verdict provisoire (honnête)
- **La structure est favorable.** Il y a 8 familles, pas 135 cas, et deux voisins actifs dans 131 réseaux.
- **Mais la force de tuer venait de la rigidité**, que seuls 4 réseaux ouverts ont. Le cas non rigide n'a jamais été testé.
- **Expérience décisive** : un réseau non rigide à la main. Le candidat est **124** (d₈a₇², voisins D₈³ / A₁₅D₉), le plus contraint :
  128/2048 vecteurs non touchants seulement. Ses blocs : A15>A7+A7 et D9>D8, puis D8>A7 ×2.
  - Si les lemmes locaux et la double contrainte de voisins le tuent, la méthode passe aux familles.
  - Sinon, la ligne (C) « à la main » ne convergera pas, et on le dit.
- **Pièce suivante (C1)** : la théorie locale de A>A+A (112 réseaux), avec les hits de u, puis D>A(n−1), puis 124.

## Répartition (27/09 nuit)
- C2 : 87 à la main, puis 44 et 10.
- structures : argument uniforme sur T.
- C1 : réseaux non rigides.
