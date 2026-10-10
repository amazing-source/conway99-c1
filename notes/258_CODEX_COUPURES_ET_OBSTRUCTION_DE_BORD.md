# 258 — Coupures de poids deux : première obstruction exacte au bord

10 octobre 2026. Exploration de la suite de la note 257.

**Résultat propre à ce tour.** Un support précis cœur+D+Z de 35 sommets,
pour le cas 3, attache 0 et forêt 2, passe les bornes locales et la PSD
de 3I−A+J/9 mais ne peut pas recevoir les 64 simples. L'impossibilité
dispose d'un certificat entier de Farkas, sans hypothèse de rang.
L'attache entière n'est pas exclue. Le bilan des notes 256-257 reste
18 attaches entières éliminées.

**Résultat des pairs à réutiliser.** Au message 549, LAB rapporte que son
nouveau test de voisinage complet exclut au rang 37 les deux supports
Codex précédemment transmis : `typed_world35_edge_0_4_9` et
`typed_world35_0_3_2`. Pour le premier, les 16 voisinages du cœur sont
morts ; pour le second, quatre suffisent (P3, P7, Q2, Q6). Un seul
voisinage impossible suffit à exclure son support.

Référence LAB : commit `4f06bd0`, branche `lab/theta-lp-2026-10-08`,
note 17.99, dossier `code/lab_cost37_2026-10-09`. Le test exploite le
rang résiduel ≤3 pour une base de Seidel de rang 33. Les bases de rang
31/32 et les supports dont chaque voisinage isolé survit demandent
d'autres étapes. Ce sont deux supports exclus, pas une campagne couvrant
la norme 16. Le résultat des pairs n'a pas été réaudité par Codex.

## 1. Structure précise issue du cas d'égalité

Dans les quatre attaches de la note 257, chaque Z voit un ou deux
doubles dans chacune des parties U,V, et chaque B au plus un de chaque
côté. Pour chaque paire d,e dans U, le nombre de Z qui les voit est
exactement 2−C_de ; de même dans V. Les cinq sommets Z qui voient deux
doubles d'une partie s'identifient donc aux cinq arêtes du multigraphe
L_U=2K4−C_U, et de même pour V. Les six autres Z reçoivent un singleton.

Dans l'attache 0, U={0,1,2,3}, V={4,5,6,7} :

- les cinq paires U sont 01,02,12,13,23, une fois chacune ;
- les paires V sont 47 deux fois, 56 deux fois, 57 une fois ;
- les singletons U ont multiplicités 2,1,1,2 ;
- les singletons V ont multiplicités 2,1,2,1.

Un isolé de Z reçoit deux singletons, une feuille reçoit un singleton
et une paire, un sommet de degré deux reçoit deux paires. Deux Z qui
reçoivent la même paire ont déjà leurs deux voisins communs dans D :
ils sont non adjacents et ne partagent aucun voisin dans Z ou B.

Cette représentation réduit les placements à des appariements de deux
listes d'étiquettes. Elle ne les rend pas tous impossibles à elle seule.

## 2. Support exclu et modèle exact de prolongement

Le support est déterminé par le cas 3, attache 0, forêt 2 et les huit
masques D-Z suivants (bit z = adjacency à Z_z) :

    75, 534, 1068, 432, 1570, 85, 281, 226.

Le fichier `data/codex_norm16_tight_seed_sample.json` enregistre ce
support et quatre autres témoins d'exploration. Aucun catalogue exhaustif
n'est revendiqué : la génération a été interrompue dès que l'existence
de supports survivants était acquise, pour travailler sur leur bord.

Pour le premier support, les simples possibles ont un voisin dans P,
un dans Q, au plus un double de U et au plus un de V. Avec r doubles,
ils voient 1+r sommets Z. On énumère tous leurs masques sur les 35 points
connus et on écarte uniquement ceux qui violent déjà λ=1 ou μ=2.
Il reste **3366 colonnes**, classées par cellule (p,q).

Pour chaque colonne t, soit x_t sa multiplicité, éventuellement réelle
non négative. La matrice entière M et le second membre b imposent :

    somme dans chaque cellule = multiplicité de la cellule ;
    somme des colonnes voyant i = 14−degré_F(i) ;
    somme des colonnes voyant i,j = 2−A_F(i,j)−(A_F²)(i,j).

Le système a 680 équations (certaines redondantes). Toute extension
en un SRG donnerait Mx=b, x≥0. Il est ici impossible même avec des
multiplicités réelles.

Le certificat sauvegardé dans
`data/codex_norm16_tight_boundary_first.json` contient un vecteur entier y
à 80 coordonnées non nulles tel que

    Mᵀy ≥ 0,                   bᵀy = −6.

Ainsi 0≤xᵀMᵀy=bᵀy=−6 serait nécessaire, contradiction. Le premier
certificat trouvé, également conservé, avait 604 coefficients et un
second membre −4 ; seul le certificat plus court est nécessaire.

Le contrôle des inégalités porte sur les 3366 colonnes complètes et
utilise des entiers Python. Les flottants ont servi à découvrir y ;
ils ne justifient aucune inégalité de la preuve finale. La génération
des colonnes ne suppose ni le rang 37 ni des arêtes entre simples.

Commande de contrôle du certificat enregistré, sans relancer l'optimiseur :

    python code/codex/norm16_tight_boundary.py --verify data/codex_norm16_tight_boundary_first.json

## 3. Limites rencontrées et cible restante

Les seuls moments core-D et D-Z sont faisables en entiers pour les
quatre attaches × cinq forêts, soit 20 modèles. Ajouter les incidences
réelles D-Z et B-Z est donc nécessaire pour avancer.

Un modèle conjoint `norm16_tight_block_model.py` cherche directement ces
incidences sans énumérer d'abord les supports 35. Pour la forêt 7, le
modèle oubliant les cellules du cœur admet un témoin, même en imposant
que deux simples ne partagent jamais trois voisins connus. Cela établit
une limite précise de cette relaxation ; cela ne construit pas un SRG.

Avec les cellules et leurs équations exactes rétablies, le pilote cas 3,
attache 0, forêt 7 comporte 33660 types de simples. Le test de 60 secondes
est **UNKNOWN**. Il ne permet ni exclusion ni affirmation de faisabilité.

Les sondes LP sur les quatre autres supports échantillonnés sont aussi
archivées. Trois ont renvoyé une infaisabilité numérique sans certificat
entier enregistré, et une un statut numérique indécis. Aucun n'est
compté comme exclusion démontrée dans cette note.

L'obstacle restant est de rendre l'inégalité de bord uniforme sur les
placements des étiquettes de la section 1. Une collection de supports
rejetés séparément ne résoudrait pas à elle seule cet obstacle. Ne pas
relancer le même décompte ou les relaxations déjà faisables.
