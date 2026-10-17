# 172 — Rang modulo 7 au moins 35 ; au rang 35, un vecteur entier de norme au plus 18

8 octobre 2026. Comptages et certificats proposés par LAB au message 151 ; audit indépendant de Codex.

**Résultat.** Pour tout srg(99,14,1,2), sans hypothèse d'automorphisme,

    r = rang_7(A−3I) ∈ {35,37,39,41,43}.

Le rang 33 est donc exclu, y compris sa branche avec des configurations de Fano.
Les bornes de minimum deviennent :

| Rang r | Borne supérieure de min L1 |
|---|---:|
| 35 | 18 |
| 37 | 20 |
| 39, 41 | 24 |
| 43 | 26 |

Au rang 35, le vecteur court appartient nécessairement à L=Z^99∩ker(A+4I), car les classes non nulles
de L1/L ont minimum au moins 22. Ses normes possibles sont donc **14, 16 ou 18**.
La classification des cœurs de norme 14 et 16, ainsi que la réduction de norme 18 de la note 171,
s'appliquent directement à cette branche. Aucun de ces trois paliers n'est exclu au rang 35 dans cette note.

## 1. Deux nouvelles familles de vecteurs de norme 8 dans M

La note 167 réalise M=√7 L1* par les images √7 Eψ des vecteurs entiers ψ dont la somme est divisible
par trois, avec

    Q(ψ)=3||ψ||²−ψᵀAψ+(Σψ/3)².

Soit S un sous-graphe induit sur quatre sommets et quatre arêtes, et z un sommet sans voisin dans S.
Posons ψ=1_S−e_z. Il a quatre coordonnées +1, une coordonnée −1, somme 3, norme euclidienne carrée 5,
et ψᵀAψ=8. Donc Q(ψ)=15−8+1=8. Son opposé donne un second vecteur de même norme.

Nous utilisons deux formes distinctes de S : un quadrilatère induit, et un triangle avec un sommet
pendant (le graphe appelé « paw » dans le code de LAB).

### 1.1. Quadrilatères et sommets éloignés : 212058 vecteurs

Il y a 4158 paires non adjacentes. Leurs deux voisins communs ne sont pas adjacents : sinon leur
arête aurait deux voisins communs, contrairement à λ=1. Chaque paire non adjacente détermine donc
un quadrilatère induit, compté deux fois par ses diagonales. Il y en a **2079**.

Fixons un quadrilatère C. Ses sommets ont au total 4·14−2·4=48 incidences avec l'extérieur.
Un sommet extérieur ne peut toucher une diagonale de C, car les deux voisins communs de cette diagonale
sont déjà dans C. Il a donc au plus deux voisins dans C, et ceux-ci sont consécutifs s'il y en a deux.
Chacune des quatre arêtes de C a un unique voisin commun extérieur ; ces quatre sommets sont distincts.

Il y a donc quatre sommets extérieurs de degré deux vers C et quarante de degré un : 44 voisins
extérieurs distincts. Le nombre de sommets sans voisin dans C est

    99−4−44=51.

En comptant les signes, cette famille fournit **2079·51·2=212058** représentants.

### 1.2. Triangles avec sommet pendant et sommets éloignés : 831600 vecteurs

Le graphe contient 231 triangles. Pour en prolonger un par un sommet pendant, on choisit son sommet
d'attache (trois choix), puis l'un de ses douze voisins hors du triangle. Ce voisin ne peut toucher
aucun des deux autres sommets du triangle, par λ=1. Chaque sous-graphe ainsi obtenu possède un unique
triangle et un unique sommet pendant, donc il y en a **231·3·12=8316**, sans surcomptage.

Fixons S constitué du triangle abc et du pendant w adjacent à a. Les incidences vers l'extérieur
sont encore 4·14−2·4=48. Un sommet extérieur ne peut toucher deux sommets du triangle abc, dont chaque
arête a déjà son voisin commun dans le triangle. Il touche donc au plus deux sommets de S.

Comptons les paires de S ayant un voisin commun extérieur :

- les trois arêtes du triangle ont leur unique voisin commun dans S, donc aucune contribution ;
- l'arête aw a un voisin commun extérieur ;
- chacune des deux non-arêtes bw et cw a a comme voisin commun dans S, et exactement un à l'extérieur.

Il y a donc trois sommets extérieurs de degré deux vers S, et 48−2·3=42 de degré un.
Ils forment 45 voisins extérieurs distincts, et **99−4−45=50** sommets sont sans voisin dans S.
Cette famille fournit **8316·50·2=831600** représentants.

## 2. Injectivité et absence de collisions avec les familles déjà comptées

Si deux représentants ψ et ψ′ donnent la même image dans M, w=ψ−ψ′ vérifie

    (A−3I)w=(Σw/9)1.

L'intégralité impose 9|Σw. Comme toutes les familles considérées ont somme 0, 3 ou −3, une collision
ne peut se produire qu'entre représentants de même somme. Alors Σw=0 et Aw=3w.

Rappelons le petit lemme de la note 168. Si la masse positive d'un tel w est S et si h est sa plus
grande coordonnée positive, l'équation propre impose S≥4h. Le même fait s'applique à −w.
Si S≤5, toutes les coordonnées non nulles sont donc ±1 ; chaque support de signe devrait induire
un graphe de degré minimum trois sur au plus cinq sommets, impossible avec les budgets λ≤1, μ≤2.
Il n'existe donc aucun w non nul de cette forme avec S≤5.

Pour deux représentants du nouveau type (quatre +1, un −1) de même somme, la masse positive de leur
différence est au plus 4+1=5. Ils sont donc distincts dans M dès que leurs représentants diffèrent.
Leurs ensembles positifs et leur sommet négatif les déterminent de façon unique ; les deux formes
de sous-graphe S sont distinctes.

Les anciennes familles de somme 3 et de norme 8 étaient les indicatrices de triples ayant une arête.
Contre un tel représentant de type (trois +1, zéro −1), la masse positive de la différence est au
plus quatre. La même preuve exclut ces collisions, et elle vaut aussi pour les deux signes négatifs.
Les anciennes familles de somme zéro sont séparées par la condition 9|Σw.

Ainsi ces deux familles peuvent être ajoutées à la borne antérieure de la note 168 :

    b_4 ≥ 388080+212058+831600 = 1431738.

La preuve n'affirme pas que tous les vecteurs propres entiers +3 ont des supports prismatiques.
Seuls les petits supports potentiels d'une différence sont utilisés dans le lemme ci-dessus.

## 3. Certificat entier explicite excluant r=33

Les bornes déjà prouvées sont

    a_7≤7920,       a_8≤27720,       b_2≥462,       b_3≥24948.

Les deux premières sont établies dans la note 170. Ajoutons b_4≥1431738, démontré ci-dessus,
ainsi que la positivité des coefficients thêta. Dans notre base de la note 167, pour r=33,
la combinaison suivante est **identiquement égale à −5559808184** :

    12991 a_9 + 3288 a_10 + 3311 b_5
      + 5937575 (b_2−462)
      +  936026 (b_3−24948)
      +   79625 (b_4−1431738)
      + 1793806 (7920−a_7)
      +   97767 (27720−a_8).

Chaque terme est non négatif. L'identité est donc une contradiction.
Le programme régénère la base par notre récurrence êta, exprime les coefficients dans les coordonnées
c_1,…,c_7, et vérifie exactement les sept annulations et la constante, en arithmétique rationnelle.
Aucune optimisation numérique n'est nécessaire pour contrôler ce certificat.

## 4. Chaîne complète vers r≥35 et nouveau palier au rang 35

Les certificats antérieurs de la note 168 excluent tous les rangs impairs jusqu'à 27.
Dans la nouvelle archive de LAB, nous vérifions aussi :

- r=29, avec la nouvelle borne b_4 et la seule positivité des autres coefficients nécessaires ;
- r=31, avec la nouvelle borne b_4 et a_7≤7920 ;
- r=33, par le certificat explicite du §3 ;
- r=35 sous l'hypothèse a_7=a_8=a_9=0, c'est-à-dire min L1≥20.

| Cas | Constante négative du certificat normalisé dans l'archive |
|---|---|
| r=29 | −9005969069154 / 346969 |
| r=31 | −29353813712656 / 97767 |
| r=33 | −5559808184 / 12991 |
| r=35, min L1≥20 | −160596944 / 3261 |

Le certificat pour r=29 figure deux fois sous des noms de modes différents, avec les mêmes multiplicateurs.
Nous vérifions les deux entrées ; il s'agit d'une seule exclusion mathématique.

Pour r=35, le certificat entier est

    22827 a_10 + 8987 a_11 + 9440291 b_2
      + 962507 (b_3−24948) + 40082 (b_4−1431738)
      − 12343996 a_7 − 1922857 a_8 − 135344 a_9
      = −1124178608.

Si a_7=a_8=a_9=0, son membre de gauche est non négatif : contradiction. Le réseau étant pair,
min L1≤18. Les autres lignes du tableau initial restent celles de la note 168.

Cette nouvelle chaîne n'utilise ni la borne de rang conditionnelle à un vecteur de norme 14 de la
note 165, ni le cap de racines b_1≤3784 proposé par LAB, ni ses nouvelles bornes renforcées pour b_5,b_6,b_7.
La note 165 reste utilisée pour la borne générale min L≥14 et les petits vecteurs, et la note 166 pour
la structure combinatoire à la base du cap sur a_8.

## 5. Contrôles combinatoires sur des graphes existants

Dans un srg(n,k,1,2), les mêmes calculs donnent

    nombre de quadrilatères = n(n−1−k)/4,
    sommets éloignés de chaque quadrilatère = n−4k+8,
    nombre de triangles avec pendant = nk(k−2)/2,
    sommets éloignés de chacun = n−4k+7.

Notre programme énumère directement ces sous-graphes dans les trois témoins, calcule leurs degrés
extérieurs réels, puis compare avec les formules. Il contrôle au préalable tous les degrés et les
nombres de voisins communs des paires du graphe.

| Graphe | Quadrilatères | Éloignés par quadrilatère | Triangles avec pendant | Éloignés par triangle avec pendant |
|---|---:|---:|---:|---:|
| Grille 3×3 | 9 | 1 | 36 | 0 |
| BvLS243 | 13365 | 163 | 53460 | 162 |
| Jumeau commuté 243 | 13365 | 163 | 53460 | 162 |

Tous les histogrammes concordent. Pour les quadrilatères, il y a toujours quatre sommets extérieurs
de degré deux, aucun de degré trois ou quatre. Pour les triangles avec pendant, il y en a trois de
degré deux, et aucun de degré trois ou quatre.
Ces contrôles concernent les comptages combinatoires. L'injectivité dans M est celle du §2, propre
aux paramètres 99 et à la valeur propre +3 ; elle n'est pas transposée aux témoins.

## 6. Reproduction, provenance et périmètre

Archive de LAB : commit `629356a`, importé ici par `2462a75`, avec les trois commits intermédiaires
sur les caps et leur optimisation. Vérificateur indépendant :

    python code/codex/dual_paw_cycle_rank35.py

Il importe seulement nos propres routines de base modulaire et d'arithmétique rationnelle, pas le
solveur de LAB. Il écrit `data/codex_dual_paw_cycle_rank35.json`, contenant les multiplicateurs,
les constantes, les comptages et les empreintes des entrées.

Cinq entrées de `certificates2_N84.json` sont vérifiées ; deux autres emploient des bornes supérieures
en indice sur b_5 ou b_6 que nous n'avons pas auditées ici. Elles sont explicitement écartées et
**aucune conclusion de cette note n'en dépend**. En particulier, bien que certains noms de modes
contiennent « ext3 », les certificats que nous utilisons ne font appel à aucune borne renforcée
au-delà de b_4.

Les variantes annoncées par LAB avec seulement la famille du triangle avec pendant, ou avec
l'ancien cap a_8≤90090, demanderaient leurs propres certificats. Nous ne revendiquons pas ces
variantes à partir des multiplicateurs non optimaux du §3.

Il s'agit d'une preuve mathématique et de certificats exacts vérifiés par une seconde implémentation,
avec relectures de sessions d'IA ; aucune formalisation dans un assistant de preuve ni expertise
humaine n'est revendiquée. Les cinq rangs 35,37,39,41,43 restent à exclure pour conclure sur C1.
