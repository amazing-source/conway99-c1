# Coexistence au-delà des cocliques de Hoffman : propagation des défauts

12 octobre 2026. Suite de la demande directe : chercher un mécanisme qui
dépasse le seul cas des cocliques de 22, sans continuer mécaniquement les
familles à sept, huit, neuf voisinages libres d'un même bord.

## 1. Résultat et portée

On démontre une loi de propagation valable pour **toute coclique** de C1,
puis un lemme d'extension ne fixant aucun modèle de bord :

> Si C est une coclique de 21 sommets et si tout sommet extérieur possède
> au plus quatre voisins dans C, alors C se prolonge en une coclique de 22.

Plus généralement, aucun sommet extérieur à une coclique de 21 ne peut
avoir six ou sept voisins dans celle-ci. Si C est maximale par inclusion,
il existe donc **entre deux et six sommets à cinq voisins dans C**.
Chacun doit être adjacent à au moins un autre de ces sommets.
Tous les sommets dont le nombre de voisins dans C diffère de quatre sont
concentrés dans un ensemble d'au plus **30 sommets**.

Ces restrictions concernent toutes les cocliques de 21, avec les réserves
explicites ci-dessus ; elles ne supposent ni asymétrie, ni symétrie, ni
rang modulaire, ni parenté avec le bord 37c3bb63972f. Ce n'est pas une
exclusion complète de alpha=21, ni une preuve que alpha=22 est obligatoire.
Le lemme d'extension ci-dessus a une preuve combinatoire complète (§5).

## 2. Un même défaut pour toutes les tailles

Soient A la matrice d'un SRG(99,14,1,2), C une coclique de taille c,
delta=22-c et x=1_C. Poser

    q = 4*1 - (A+4I)x.

Alors q_v=0 pour v dans C, et q_v=4-b_v ailleurs, où
b_v=|N(v) intersection C|. Le voisinage d'un sommet étant 7K2,
0 <= b_v <= 7, donc -3 <= q_v <= 4.

L'identité A²+A=12I+2J donne EXACTEMENT

    A q = 3 q + 2 delta*1.                         (1)

En effet (A-3I)(A+4I)=2J et (A-3I)4*1=44*1.
Ainsi, en chaque sommet v, la somme des défauts de ses voisins est
3q_v+2delta. Les choix de voisinages ne peuvent donc répartir librement
les défauts : ils doivent les transporter dans un même graphe.

Les comptages d'incidences donnent

    sum q_v = 18 delta,
    sum q_v² = 2 delta(delta+14),
    sum q_v(q_v-1) = 2 delta(delta+5).               (2)

Pour les vérifier, sur les 99-c sommets extérieurs,
sum b_v=14c et sum b_v²=2c²+12c ; développer (4-b_v) et (4-b_v)².
Chaque q_v(q_v-1) est un entier positif ou nul, et vaut au moins deux
si q_v n'est ni zéro ni un. Par conséquent :

    |supp(q)| <= 2 delta(delta+14),
    #{v hors C : b_v n'est ni 3 ni 4} <= delta(delta+5).

À c=22, q=0 : le bord de Hoffman est le cas sans défaut.
À c=21, le support a au plus30 sommets et il y a au plus6 exceptions
aux tailles3 et4. À c=20, les bornes sont64 et14. Pour des cocliques
plus petites, la borne de support devient moins utile, mais (1) reste
exacte. Il n'y a pas encore de contradiction uniforme pour toutes les tailles.

**Antériorité et usage.** Les comptages de base ne sont pas revendiqués
comme nouveaux. Voir Lou--Murin, *On the strongly regular graph of parameters
(99,14,1,2)*, §4, théorème4.3 et la forme voisine du comptage de chemins
dans le lemme4.2 :
https://math.mit.edu/research/highschool/primes/materials/2014/Lou-Murin.pdf
L'usage ici est la concentration des défauts, le lemme d'extension21→22,
et le recollement simultané sur ce support. La recherche bibliographique
effectuée ne constitue pas une preuve de nouveauté de ces conséquences.

## 3. Le support est un bord commun de petite taille

Écrire S=supp(q), F=A[S,S], Z=V\S et H=A[S,Z]. Sans construire Z,
toute réalisation impose

    F q_S = 3 q_S + 2 delta*1_S,
    H^T q_S = 2 delta*1_Z,
    H H^T = 12I + 2J - F² - F,
    H 1_Z = 14*1_S - F 1_S.                        (3)

La troisième équation impose une UNIQUE population de sommets de Z
qui réalise simultanément tous les déficits de voisins communs de S.
Un domaine non vide pour chaque ligne séparément ne suffit pas.

Les c sommets de C appartiennent à Z. Parmi les colonnes de H, il faut
en sélectionner c avec somme de colonnes b_i=4-q_i pour i dans S.
Les autres sommets de Z ont chacun exactement quatre voisins dans C.

Si D=A[Z,Z], le recollement à cette population exige encore

    H D = 2J - (F+I)H,
    D 1_Z = 14*1_Z - H^T 1_S,                      (4)
    D²+D = 12I+2J-H^T H.

Cette réduction déplace le bord de la coclique entière vers les sommets
qui portent ses écarts. Elle n'élimine pas les obligations de la région Z.
Les équations matricielles générales de complétion étaient déjà acquises
(note171) ; le choix du support et les restrictions ci-dessous sont l'étape
exploitée ici, pas une nouvelle revendication pour ces équations seules.

## 4. À21, les excès de six et sept sont impossibles

Ici delta=1 et le budget sum q(q-1) vaut12.
Supposons b_v=6, donc q_v=-2. Ce sommet consomme6 unités du budget.
Par (1), la somme des défauts de ses voisins vaut -4. Les défauts
négatifs de ces voisins ont donc une valeur absolue totale au moins4.
Pour q<0, q(q-1)>=2|q| : ces voisins consomment au moins8 unités
supplémentaires. Le total14 dépasse12, contradiction.

Si b_v=7, q_v=-3 consomme déjà12 unités ; sa somme de voisins devrait
être -7, ce qui nécessiterait encore des défauts négatifs. Contradiction.

Cette preuve ne suppose pas que C soit maximale. Plus généralement,
pour b_v=4+t, t>0, les mêmes arguments donnent l'inégalité nécessaire

    t(t+1) + 2 max(0,3t-2delta) <= 2delta(delta+5).

C'est un filtre uniforme de coexistence entre un sommet et ses voisins.

## 5. Preuve du lemme d'extension21→22

Supposons que tous les b_v soient au plus4 et que C ne se prolonge pas.
Alors b_v>=1. Tous les défauts sont positifs ou nuls.
Un sommet b_v=1 porterait q_v=3 et serait voisin d'un point p de C.
Or (1) impose en p une somme de défauts égale à2 : impossible avec des
défauts positifs ou nuls. Donc les seuls défauts non nuls valent1 ou2.

Les deux premières égalités (2) imposent six défauts2 et six défauts1.
Noter U et W ces deux ensembles de six sommets, et F le graphe induit
sur U union W. Soient e_U, e_UW, e_W ses trois nombres d'arêtes.
La loi (1), sommée sur chaque classe, donne

    4 e_U + e_UW = 48,
    e_UW + e_W = 15.

D'où e_W=4e_U-33 et e_U>=9.

**Fait sur six sommets.** Un graphe induit sur six sommets d'un C1 a
au plus neuf arêtes. S'il en a neuf, c'est le prisme triangulaire.

Preuve : un sommet de degré4 a quatre voisins induisant au plus deux
arêtes (le voisinage est un appariement), et le sixième sommet, non
adjacent, a au plus deux voisins parmi ces quatre. Il y a alors au plus
huit arêtes. Un sommet de degré5 laisse un appariement sur ses cinq
voisins, soit au plus sept arêtes. Sinon le degré maximal est3, donc
il y a au plus neuf arêtes, avec égalité seulement si le graphe est cubique.
Un cubique sans triangle sur six sommets serait K3,3, qui possède des
paires à trois voisins communs. Il y a donc un triangle ; les trois
autres sommets forment nécessairement un autre triangle, avec un
appariement entre les deux. C'est le prisme.

Ainsi F[U] est le prisme, e_UW=12 et e_W=3. Pour w dans W, la loi (1)
est 2 deg_U(w)+deg_W(w)=5. Donc deg_U(w)<=2 ; la somme étant12 sur
six sommets, chaque w a exactement deux voisins dans U.

Ces deux voisins ne peuvent être une non-arête du prisme, car elle a
déjà deux voisins communs dans U. Ils ne peuvent être une arête d'un
triangle, car elle a déjà son unique voisin commun. Il reste seulement
les trois arêtes de l'appariement entre triangles, chacune pouvant
recevoir au plus un voisin commun supplémentaire.
Il faudrait y placer les six sommets de W : impossible.

La supposition que C ne se prolonge pas est donc fausse. Il existe
un sommet extérieur sans voisin dans C, et son ajout donne22 sommets.
La preuve est entièrement combinatoire et ne dépend d'aucun verdict SAT.

## 6. Ce qui est forcé pour une coclique21 maximale

Maximale signifie ici : aucun sommet ne peut être ajouté directement.
On n'a donc pas besoin de supposer que alpha du graphe soit égal à21.
Les tailles possibles sont1,2,3,4,5. Poser a=n_1, b=n_2, e=n_5.
Les moments imposent

    3a+b+e=6,
    n_3=6+3a+3e,
    n_4=66-a-3e.                                   (5)

La section5 impose e>0. En un sommet de défaut-1, la loi (1) donne
une somme voisine -1 : il doit rencontrer un autre défaut négatif.
Ainsi e>=2 et le graphe induit par les e sommets de taille5 n'a aucun
sommet isolé. Le budget impose e<=6 et a<=1.

Les seules paires numériques restantes (a,e) sont

    (0,2),(0,3),(0,4),(0,5),(0,6),(1,2),(1,3).

Ce sont sept **profils de degrés**, pas sept graphes ni sept familles
dont l'existence serait établie. Ils couvrent les cocliques21 maximales.
Ils ne sont pas le décompte des anciennes familles de bords à points libres.

Dans le graphe des défauts négatifs E, la loi se précise en

    deg_E(v) = 1 + sum_{w voisin de v, q_w>0} q_w.

Par exemple, si e=2, les deux sommets sont adjacents et aucun d'eux
n'est adjacent à un défaut positif. Cette contrainte doit être propagée
avec les équations des sommets de défaut nul, et pas seulement testée
à l'intérieur de E.

## 7. Mise en œuvre et apprentissage sur les survivants

Code dans `code/codex/`, résultats dans `data/codex_coclique_defects/`.

- `coclique_defect_core.py` impose la loi pondérée sur S et les bornes
  de voisins communs pour toutes ses paires. Le cas six défauts2 et six
  défauts1 est INFEASIBLE en0,078s ; la preuve humaine de§5 le remplace
  comme fondement du théorème.
- Les profils (a,e)=(0,2) et (0,3) donnent chacun un noyau local faisable,
  en moins d'une seconde. Ils ont18 et21 sommets. Ce ne sont pas des SRG.
- `coclique_defect_gluing.py` énumère les colonnes possibles de H, puis
  exige les nombres de sommets, les degrés et TOUS les quotas de paires
  de (3), ainsi qu'une sélection de21 colonnes pour C. Les domaines ont
  respectivement407 et459 colonnes. Ils sont complets :1131 et1212
  nœuds d'énumération, sans plafond.
- Deux colonnes qui partagent trois voisins ne peuvent coexister.
  Le premier témoin à18 sommets violait cette règle. Le mode
  `--pair-consistency` l'impose à toutes les paires et trouve de nouvelles
  populations compatibles. Cela ne réalise pas encore D.
- `coclique_defect_completion.py` impose simultanément (4) et les
  incidences avec la coclique. Les DEUX populations retenues sont
  impossibles, dès la propagation booléenne :225 puis588 affectations
  forcées conduisent à réclamer deux voisins communs alors qu'un seul
  candidat reste disponible. Les raisons et équations sont enregistrées.
  C'est l'exclusion de ces populations précises, pas de tous les noyaux
  des profils(0,2) et(0,3).

On réinjecte cette obligation dans le choix de H : pour une colonne R,
poser h_i(R)=2-[i dans R]-|N_F(i) intersection R|. Un voisin futur de R
doit être une colonne T qui vérifie

    |R intersection T|<=1,
    h_i(R)>0 pour tout i dans T,
    h_i(T)>0 pour tout i dans R.

Ces restrictions sont réciproques. Si R est utilisé, sa population de
voisins possibles doit couvrir son degré et chacun de ses h_i(R).
Si R appartient à C, seuls les sommets hors C peuvent servir ; sinon
il lui faut quatre voisins dans C. Le mode `--neighbour-capacity`
impose ces inégalités PENDANT le choix des colonnes, pour ne pas simplement
énumérer des populations dont le recollement échoue après coup.

Le pilote renforcé sur le noyau(0,2) trouve une nouvelle population en
27,72s ; elle échoue encore aux équations linéaires simultanées (4).
Le pilote sur le noyau(0,3) termine UNKNOWN au plafond30s : aucune
exclusion n'est déduite de ce plafond. Les bornes de capacité doivent
encore être remplacées ou complétées par un choix COMMUN des voisins
de chaque colonne, puis leur réciprocité entre colonnes. Allonger le
même pilote ne résoudrait pas l'obligation manquante identifiée.

## 8. Contrôles utiles et frontière

`check_coclique_defects.py` effectue des contrôles courts :

- loi de défaut analogue sur les34 cocliques de la grille3x3 ;
- fait sur les graphes de six sommets : neuf arêtes au maximum, avec
  exactement60 prismes étiquetés au maximum ;
- rejeu entier des trois contradictions de propagation enregistrées ;
- contrôle positif de toute la chaîne, qui RECONSTRUIT le SRG(9,4,1,2)
  depuis le support de défaut d'une coclique de deux sommets.

Résultat `checks.json` : PASS. Aucun ancien dossier n'a été réaudité.
Les valeurs propres numériques des deux noyaux ont été inspectées à
titre exploratoire, sans certificat négatif trouvé ; elles ne sont
utilisées ni comme exclusion ni comme preuve de positivité exacte.

La frontière de preuve reste explicite : nous disposons d'une réduction
uniforme, d'un lemme d'extension21→22 et de restrictions valables pour
toutes les cocliques21 maximales. Il reste à exclure ou réaliser leurs
noyaux et leurs populations communes. L'existence de C1 reste ouverte.
Les exclusions Hoffman à six voisinages libres restent acquises,
mais ne sont pas nécessaires aux preuves des sections2–6.

## 9. Les composantes du support ne répartissent pas librement la charge

Autre conséquence uniforme, sans hypothèse de rang modulaire : si delta>0
et T est une composante PROPRE du graphe induit sur supp(q), sa charge
totale w=sum_{v dans T}q_v vérifie

    w<0 ou w>18delta.                               (6)

Preuve : la matrice P=27I-9A+J est positive semi-définie ; sur les espaces
propres de A de valeurs14,3,-4, ses valeurs sont0,0,63. Pour le vecteur
q_T obtenu en annulant q hors T, la loi (1) à l'intérieur de T donne

    q_T^T P q_T = w(w-18delta) >= 0.

L'égalité w=0 est impossible : Pq_T aurait la valeur -18delta en chaque
sommet de T, tandis qu'un vecteur de forme quadratique nulle pour P>=0
appartient au noyau de P. L'égalité w=18delta est également impossible
si T est propre : en un sommet d'une autre composante du support,
Pq_T vaut w, car ce sommet n'est adjacent à aucun sommet de T.

À21 maximale, les défauts négatifs sont les e<=6 valeurs-1. La masse
positive totale vaut18+e<=24. Il ne peut donc y avoir deux composantes
de charge positive, chacune devant avoir charge au moins19. Il y en a
exactement une ; toutes les autres, s'il y en a, ont une charge négative.
Cela ne signifie pas que toutes leurs valeurs individuelles sont négatives.

Sur le noyau témoin(0,2), les charges des deux composantes sont20 et-2 ;
sur le noyau(0,3), le support est connexe, de charge18. Aucun de ces deux
témoins n'est exclu par(6). La règle sert à contraindre directement les
futurs noyaux, sans décider d'abord leurs bords ou leurs symétries.

## 10. Deux défauts négatifs imposent un cycle et ses attaches

Dans le profil (a,e)=(0,2), écrivons H pour les quatre sommets de charge2,
L pour les douze de charge1 et E pour les deux de charge-1. Les sommets
de E sont adjacents et sans voisin dans H union L : l'équation de charge
en chacun impose deg_E=1+masse_positive_voisine, et deg_E<=1.

Posons p=e(H), t=e(H,L), s=e(L). Les équations pondérées donnent

    4p+t=32,     t+s=30.

Pour chaque l dans L, 2deg_H(l)+deg_L(l)=5, donc deg_H(l)<=2 et t<=24.
Ainsi p>=2. Les bornes sur les voisins communs interdisent un diamant,
donc p<=4. Le budget de voisins communs des paires de H, après avoir
compté leurs voisins déjà dans H, est

    B=12-p-sum_{h dans H} binom(deg_H(h),2).

Si n_j compte les sommets de L ayant j voisins dans H, alors
n_2-n_0=t-12=20-4p. Chaque sommet compté par n_2 consomme une unité de B.
Pour p=2, n_2>=12>B. Pour p=3, la somme des binomiaux vaut au moins2,
donc n_2>=8>B. Pour p=4, il faut n_2>=4 et B>=4 ; le seul graphe
admissible est C4 (l'autre graphe à quatre arêtes est la patte, avec B=3).
Toutes les inégalités deviennent alors des égalités.

Conclusion uniforme : H=C4, quatre sommets X de L occupent chacun une
arête distincte de ce cycle, les huit autres sommets Y ont chacun un
unique voisin dans H, et il y a deux Y par sommet de H. Chaque X a un
voisin dans L ; chaque Y en a trois. Ceci décrit TOUT le profil (0,2),
pas seulement un noyau témoin. Les arêtes internes de L restent libres
sous les contraintes de voisins communs.

La première énumération normalisée (`coclique_two_exceptions.py`) a
rencontré 249 classes d'isomorphisme en60s, mais n'a PAS terminé.
Ce nombre n'est donc ni un total, ni une exclusion. Le but de la
normalisation est d'appliquer les obligations de coexistence à toute
cette forme, et non de constituer un catalogue pour lui-même.

## 11. Le bord de la coclique limite la densité des défauts négatifs

Soit E l'ensemble des e sommets de charge-1, p=e(E), et d_i leurs
degrés dans E. Chacun a cinq voisins dans C. Si t_c=|N(c) intersection E|,
alors sum_{c dans C}t_c=5e et

    sum_{c dans C} binom(t_c,2) >= 5e-21.

Ces voisins communs doivent tenir dans le budget des paires de E :

    5e-21 <= e(e-1)-p-sum_i binom(d_i,2).             (7)

Pour e=6, p>=8 donnerait une somme des binomiaux au moins14 et un
budget au plus8, inférieur à9 : donc p<=7. Pour e=5, p>=7 donnerait
une somme au moins13 et un budget au plus0, inférieur à4 : donc p<=6.
En particulier la masse positive totale attachée à E, égale à2p-e,
est au plus8 pour e=6 et au plus7 pour e=5. Ces restrictions portent
sur tous les noyaux de ces profils, indépendamment de leurs symétries.

## 12. Exclusion d'une branche entière du profil (1,3)

Dans ce profil, il y a un sommet u de charge3, dix-huit de charge1,
trois de charge-1, et aucun de charge2. Supposons que les trois défauts
négatifs E forment un triangle. Chaque sommet de E a une masse positive
voisine égale à deg_E-1=1 ; u ne peut donc être adjacent à E.

L'équation en u impose exactement onze voisins dans le support,
tous de charge1, et donc trois voisins de charge nulle. Si z est l'un
de ces trois derniers, sa colonne R=N(z) intersection supp(q) contient u
et vérifie sum_R q=2. Elle doit contenir au moins un sommet de E, mais
ne peut en contenir deux : une paire de E, déjà adjacente et ayant le
troisième sommet de E comme voisin commun, n'en accepte pas d'autre.
Par conséquent R={u,e} pour un e dans E.

Aucun de ces trois z n'est donc adjacent à un voisin de u dans le
support. Dans N(u)=7K2, les trois z devraient être appariés entre eux.
C'est impossible. Le profil (1,3) avec E=K3 est ainsi EXCLU par parité,
sans énumération des noyaux. Le cas E=P3 reste ouvert à ce stade.

## 13. Pilotes de recollement réciproque et obligation manquante

`coclique_defect_joint.py` choisit simultanément les populations de
colonnes, leur appartenance à C et les nombres d'arêtes entre types.
Un même nombre sert aux équations des deux extrémités. Le contrôle
positif sur la grille3x3 passe. Les deux pilotes sur les noyaux témoins
(0,2) et (0,3) terminent UNKNOWN à120s, sans exclusion ; ils ont
respectivement 84047 et138996 variables de nombres d'arêtes. Leurs
journaux montrent environ27s et38s de présolve : ce n'est pas une
raison de relancer les mêmes modèles plus longtemps sans renforcement.

Dans (0,2), les deux sommets de E ont un unique voisin commun z, de
charge nulle. Sa colonne R contient E et une masse positive4. Les
voisins de z hors du support ont tous une colonne sans E, donc de
forme {h}, h dans H, ou {l,l'}, l,l' dans L. Les premiers ont des
multiplicités imposées ; les seconds forment un graphe simple sur L
avec les degrés h_i(R)=2-[i dans R]-|N_F(i) intersection R|.

Le test de ces seuls facteurs (`coclique_negative_edge.py`, version1)
laisse survivre les101 colonnes R du premier noyau témoin. Ce constat
n'est pas une conclusion de faisabilité globale : il manque encore
l'appariement effectif dans N(z), puis la coexistence de ces voisins
avec une seule et même population extérieure.

Le test d'appariement effectif (`coclique_defect_star.py`) laisse lui
aussi survivre les101 racines seules. Son couplage au problème de
population commune en exclut19 et laisse82 témoins, en24,41s, sans
timeout. Portée : ce seul noyau F, pas tous les noyaux (0,2).
Le contrôle positif sur la grille3x3 conserve ses quatre racines réelles.

`coclique_defect_triangles.py` choisit ensuite les MÊMES arêtes pour tous
les triangles centrés dans le support. Il interdit aussi un triangle
extérieur dont une arête a déjà son voisin commun dans le support, et
un chemin extérieur qui ajouterait un troisième voisin commun à une
paire déjà saturée. Sur le noyau témoin, 36080 variables d'arêtes,
58878 coupures de triangles et200500 coupures de chemins donnent encore
une population admissible en33,16s. Mais cette population est impossible
au recollement linéaire complet, même en autorisant à changer ses
appariements. La section suivante en donne une preuve entière courte.

## 14. Transformer une coexistence impossible en une coupure de famille

Pour une colonne R choisie, la même liste de voisins extérieurs doit
réaliser simultanément tous les nombres h_i(R). Pour N' son voisinage
extérieur, toute pondération entière beta des coordonnées donne

    sum_i beta_i h_i(R) = sum_{z dans N'} sum_{i dans R_z} beta_i.

Si x_T est la population totale de type T, c_T sa partie dans C,
et R est dans C, on obtient donc la condition nécessaire UNIFORME

    sum_i beta_i h_i(R)
        <= sum_{T voisin possible de R} max(0,sum_{i dans T}beta_i)
                                                * (x_T-c_T).       (8)

Il ne suffit plus que chaque quota dispose séparément d'assez de
candidats. (8) compare toutes leurs superpositions avec une seule
population. Elle s'applique à tout support de défaut, pas seulement à
c=21. Pour R hors C, la version non colorée utilise x_T, en retirant
R lui-même s'il appartient à un type candidat ; on peut aussi pondérer
les équations de degré et les quatre voisins dans C.

Exemple exact tiré de la population qui passe le couplage des triangles :
le sommet extérieur numéro73 est dans C, de colonne R={9,13}.
Prendre beta_7=beta_17=1, beta_10=beta_11=-1,
beta_9=beta_13=-2, les autres coordonnées étant nulles.
Les six équations donnent un membre gauche égal à2. Dans la population
choisie, la seule arête autorisée de poids positif est (23,73), de
poids1 ; toutes les autres ont un poids nul ou négatif. Il faudrait

    2 <= d_{23,73} <= 1.

C'est une contradiction entière, sans confiance nécessaire dans le
verdict du solveur. Les six équations, leurs coefficients et les19
arêtes de poids non nul sont conservés dans
`core_a0_e2_triangles_farkas_sparse.json`. L'oracle LP ne sert qu'à
TROUVER les coefficients ; `coclique_completion_certificate.py`
reconstruit puis vérifie l'inégalité en arithmétique entière.

Le gain méthodologique est de réinjecter (8) pendant la sélection de
la population. La coupure exclut toute population qui contient ce
type R dans C sans les ressources nécessaires, et pas seulement le
témoin rejeté. Elle ne constitue pas à elle seule l'exclusion du noyau
ou du profil. Les arêtes entre colonnes disjointes, leur réciprocité et
les derniers quotas entre sommets extérieurs restent à imposer.

## 15. Séparateurs globaux : les choix locaux existent et ne coexistent pas

La boucle `coclique_defect_cut_loop.py` réalise maintenant le passage
suivant, avec des témoins et des certificats sauvegardés à chaque étape :

1. Choisir une population H satisfaisant le Gram, C et les capacités.
2. Pour CHAQUE sommet extérieur, choisir séparément un vrai sous-ensemble
   de voisins, satisfaisant son degré, son quota dans C et TOUS les
   nombres de voisins communs avec le support. Ces choix sont binaires,
   contrôlés en entiers ; ils ne sont pas seulement des comptes fractionnaires.
3. Imposer une seule variable d_{uv}=d_{vu} aux deux extrémités, et
   chercher un séparateur du système linéaire simultané.
4. Transformer le séparateur en une inégalité valable pour toutes les
   populations du même support, puis reprendre la sélection avec cette
   nouvelle obligation.

Dans `learned_cuts_e2_pruned`, les populations000,001,002 ont chacune
81/81 choix individuels satisfaisants. Pourtant elles n'ont AUCUNE
réalisation réciproque, même fractionnaire. Les trois certificats entiers
donnent respectivement

    920 <= 841,     637 <= 530,     1447 <= 1349.

Les fichiers contiennent chaque coefficient entier de la preuve. Ces
exemples matérialisent une incompatibilité de coexistence APRÈS la
réussite de tous les tests individuels indiqués. Ils ne disent pas que
tous les voisinages locaux SRG complets existent, ni que toutes les
populations ont été exclues.

### Inégalité globale valable pour toute taille de coclique

Une cellule a est un type de colonne R_a avec son appartenance ou non
à C ; sa population est p_a. Posons d_a=14-|R_a|, kappa_a=0 dans C et4
hors C, et h_a=(h_i(R_a))_i. Choisissons des poids entiers alpha_a,
gamma_a et beta_a. Définissons

    L_a = alpha_a d_a + gamma_a kappa_a + beta_a . h_a,

    K_ab = alpha_a+alpha_b + beta_a . 1_{R_b} + beta_b . 1_{R_a}
           + gamma_a [b dans C] + gamma_b [a dans C].

En sommant les équations pondérées de tous les sommets, le membre
gauche est sum_a p_a L_a. Chaque arête réelle entre cellules a,b
contribue exactement K_ab. Une paire de cellules distinctes porte au
plus p_a p_b arêtes, et une même cellule au plus binom(p_a,2). Donc

    sum_a p_a L_a <= sum_{a<b, admissibles} max(0,K_ab) p_a p_b
                    + sum_{a, admissibles} max(0,K_aa) binom(p_a,2). (9)

Les arêtes C-C, celles entre colonnes d'intersection>=2 et celles qui
contredisent un h_i=0 sont inadmissibles. (9) est une conséquence de la
réciprocité de TOUTES les arêtes, sans hypothèse de symétrie ou de rang.
Elle vaut pour n'importe quel bord connu avec ces équations de
recollement ; la restriction à un support de défaut sert à rendre les
domaines plus petits. Elle n'est donc pas limitée à c=21 ou22.

Un séparateur initial peut donner des poids différents à des copies
d'une même cellule. On les moyenne dans la cellule, puis on multiplie
par un dénominateur commun. Le membre gauche reste inchangé à facteur
près, tandis que la convexité de max(0,x) assure que la borne droite
ne croît pas. Le séparateur devient ainsi une véritable coupure en
variables de populations, applicable aussi à des populations futures.

Les produits sont créés seulement lorsqu'une coupure en a besoin et
réutilisés dans les suivantes. La boucle conserve les certificats,
les coupures, les choix locaux et les statistiques. Elle peut reprendre
plusieurs dossiers antérieurs avec `--resume-from`, sans réapprendre
les mêmes contradictions. Les timeouts restent des UNKNOWN, jamais
des exclusions de noyaux.

`check_coclique_coexistence_v2.py` reconstruit les nouvelles combinaisons
linéaires et leurs bornes sans utiliser le code de l'oracle. Il contrôle
aussi les choix individuels, les coupures de familles, la réduction C4
sur les64 graphes à quatre sommets et la densité des défauts négatifs.
La grille3x3 demeure admissible pour le maître et ne possède aucun
séparateur impossible. Les anciens résultats ne sont pas réaudités.

### Reprise des coupures et frontière entière

Le premier pilote apprend trois coupures avant UNKNOWN au plafond20s.
Le second élimine d'emblée les arêtes interdites par h_i=0, apprend
quatre nouvelles coupures et termine UNKNOWN au plafond30s. Ces
timeouts n'effacent aucun acquis : la reprise combinée recharge les
sept certificats, puis en apprend trois autres. Elle s'arrête sur une
population dont le système réciproque FRACTIONNAIRE est réalisable.
Les temps de présolve observés sont autour de26s dans la reprise ; les
plafonds20/30s étaient donc trop courts pour exploiter le modèle enrichi.
La reprise emploie six workers,90s par sélection, et des journaux datés.

Cette dernière population, `learned_cuts_e2_combined/population_003.json`,
a encore81/81 choix locaux linéaires. De plus, les18 voisinages centrés
dans le support admettent chacun séparément l'appariement requis.
Cependant le système réciproque BINAIRE est INFEASIBLE en52,28s,
avec1 386 507 branches et510 430 conflits. Le verdict entier est ici
celui de CP-SAT, sans certificat DRAT/équivalent fourni ; il n'est pas
présenté comme un certificat Farkas. La simple réduction modulo2 du
système reste compatible, donc elle ne fournit pas l'explication de
cette impossibilité entière. Ce test de parité ciblé n'est pas une
reprise de la campagne des rangs.

`coclique_defect_exact.py` ajoute aussi TOUS les quotas entre deux
sommets extérieurs. Son contrôle positif reconstruit exactement la
grille3x3. Sur cette même population C1, le modèle complet termine
également INFEASIBLE en51,33s. C'est la même population exclue, pas
une deuxième exclusion. On a2587 variables d'arêtes et166949 variables
auxiliaires de voisins communs.

La frontière suivante est donc précise : conserver les dix coupures
de populations acquises, puis extraire de l'obstruction ENTIÈRE une
coupure de famille supplémentaire. Une famille qui passe les seules
inégalités fractionnaires n'est pas déclarée réalisable. Aucune
exclusion de tous les noyaux (0,2), de toutes les cocliques21, ou de C1
n'est acquise. En revanche l'exclusion analytique (1,3,E=K3), la forme
C4 imposée à (0,2) et les règles (7)–(9) sont uniformes dans leur portée.

## 16. Saturer les paires ferme le dernier ancien survivant

Suite demandée par Dilan : attaquer toute la famille (0,2), en utilisant
des sous-cas pour extraire des lois et des certificats réutilisables.

**Lemme des paires saturées.** Si deux sommets extérieurs u,v ont déjà
deux voisins communs dans le support, ils sont non adjacents et ne peuvent
avoir aucun voisin commun supplémentaire. Pour tout sommet extérieur w :

    d_uw + d_vw <= 1.                                      (10)

La preuve est immédiate de lambda=1, mu=2. Cela couple les ressources
utilisées par deux voisinages, même lorsque chacun peut remplir ses quotas
séparément. En particulier deux copies d'une colonne de taille2 doivent
avoir des voisinages extérieurs disjoints. Pour des poids quelconques sur
les demandes de deux tels sommets, une ressource w contribue au plus le
maximum de ses deux scores positifs, et non leur somme.

Le dernier survivant de§15, `learned_cuts_e2_combined/population_003.json`,
est maintenant exclu par un **certificat arithmétique indépendant du verdict
CP-SAT**. On ajoute2288 inégalités(10) aux quotas réciproques. Le séparateur
utilise finalement dix de ces inégalités et des équations de quotas ;
la vérification entière donne

    99 <= 97.

Fichier `integer_frontier_probe/saturated_pair_certificate.json`, outil
`coclique_saturated_pairs.py`. Ceci prouve l'impossibilité du graphe pour
cette population en utilisant davantage de conditions SRG. Ce n'est PAS
une certification du système linéaire binaire plus faible pris isolément.
Les essais à une seule des dix inégalités ne donnent pas de certificat
(certains atteignent6s) : ne pas annoncer une preuve à une seule paire.

Pour Ax=b, Gx<=1, 0<=x<=1, le certificat est constitué d'entiers y et
z>=0, et vérifie exactement

    y.b - sum z > sum_j max(0,(yA-zG)_j).                    (11)

Le LP trouve les coefficients ; seules les opérations entières fondent
la contradiction. Le vérificateur reconstruit les équations et les
intersections des colonnes depuis les fichiers d'entrée.

### Une coupure de populations, pas seulement un témoin rejeté

On moyenne y et z entre copies des mêmes cellules. Garder les notations
L_a,K_ab et p_a de§15. Pour une paire de cellules saturées a,b et une
cellule centrale c autorisant les deux arêtes, prendre un poids z_abc>=0.
Nécessairement c diffère de a et b. Le nombre de triplets vaut

    T_abc = p_a p_b p_c                 si a != b,
    T_aac = binom(p_a,2) p_c            si a = b.

La somme des inégalités(10) apporte, sur une arête entre a et c,
le coefficient z_abc p_b si b!=a, ou z_aac(p_a-1) si b=a.
Noter M_ac(p) la somme de ces contributions, et P_ac(p) le nombre
de paires possibles entre cellules (p_a p_c ou binom(p_a,2)). Alors

    sum_a p_a L_a <= sum_abc z_abc T_abc(p)
                    + sum_ac max(0,K_ac-M_ac(p)) P_ac(p).   (12)

Cette loi vaut pour tout support et toute population admissible. Les
poids moyennés du certificat ne réduisent pas son écart : le membre
gauche et les pénalités de triplets restent inchangés à facteur près,
et la convexité de max(0,x) ne peut augmenter la borne des arêtes.
On multiplie par un dénominateur commun pour obtenir des entiers.

`coclique_packing_family_cut.py` réalise cette transformation. L'ancien
survivant viole la coupure moyennée par659<=657. Elle est ajoutée aux
dix anciennes coupures, avec2867 termes d'arêtes et dix termes de
triplets. La portée de cette instanciation est TOUTES les populations
du même support, pas tous les supports (0,2) à la fois.

Le maître enrichi trouve encore une population en46,19s. Une nouvelle
combinaison de trois quotas la rejette par2<=1 ; elle devient une
douzième coupure. Le maître à douze coupures trouve un nouveau témoin
en33,95s, qui passe la relaxation réciproque avec TOUTES les2329
inégalités de paires saturées de cette population. Un nouveau candidat
n'est donc pas présenté comme un SRG. Données : `learned_cuts_e2_packing/`
et `learned_cuts_e2_packing_continuation/`.

## 17. Toute la famille se réduit à onze répartitions de cycles

Soient e,f les deux sommets négatifs et z leur unique voisin commun.
Poser U=N(e)\{f,z} et V=N(f)\{e,z}. Ces ensembles sont disjoints et
ont chacun12 sommets, tous de charge nulle. N(e)=7K2 impose un
appariement parfait sur U ; de même sur V. Un u dans U est non adjacent
à f et a déjà e comme voisin commun avec f. Il n'est pas adjacent à z,
car e-z a déjà f comme voisin commun. Il a donc exactement un voisin
dans V. La même propriété de l'autre côté donne un appariement parfait
entre U et V.

**Conclusion uniforme :** le graphe induit sur U union V est une union
disjointe de cycles dont les longueurs sont multiples de4. En parcourant
un cycle, les couleurs suivent U,U,V,V. Les longueurs sont4k_i avec
sum k_i=6. Les onze partitions de6 donnent les onze répartitions
possibles ; ce ne sont PAS onze graphes C1 ni onze familles exclues.

On peut numéroter les appariements internes de U et les arêtes U-V,
puis choisir une forme canonique de l'appariement interne de V pour
chaque partition. Aucune symétrie du graphe complet n'est supposée.
La réduction vaut en fait autour de n'importe quelle arête d'un
SRG(99,14,1,2) ; la structure des défauts rend ici toutes les charges
de U et V nulles et leurs attaches au support très contraintes.

## 18. Le multiensemble résiduel est déterminé par le bord

Noter H les quatre sommets du carré, L les douze sommets positifs
restants, et B=S union U union V union {z}. On a |B|=43.
Les voisinages de e et f sont déjà complets dans B.

Tout sommet t hors B est de charge0 et n'est adjacent ni à e ni à f.
La loi Aq=3q+2 impose donc une masse positive2 dans son voisinage :
son attache au support est **soit un singleton {h}, h dans H, soit
une paire {i,j}, i,j dans L**. Il n'existe aucun autre type.

Poser R=N(z) intersection (H union L) et epsilon=|R intersection H|.
La masse de R vaut4 ; epsilon vaut0 ou1, donc |R intersection L|=4-2epsilon.
Pour chaque h dans H, le nombre de futurs sommets de type {h} est

    m_h = 4 + [h dans R].                                (13)

En effet h a six voisins dans le support, 2-[h dans R] dans chacun
de U,V, et [h dans R] fois le voisin z. Son degré encore à remplir
vaut14-(6+4-[h dans R]).

Pour une paire i,j de L, sa multiplicité future est exactement

    m_ij = 2 - [i~j] - |N_B(i) intersection N_B(j)|.        (14)

Un futur sommet ne peut contribuer à cette paire que s'il est de ce
type précis. Chaque m_ij est donc un entier0,1,2 (au plus1 si i~j).
Les quotas de degrés, de nombre total et d'appartenance à C restent
obligatoires ; leur vérification ne doit pas être omise.

Il y a16+epsilon singletons et40-epsilon sommets de type paire. Le
multigraphe des types paires sur L a donc40-epsilon arêtes comptées
avec multiplicité. Ses degrés valent7+[i dans R] sur les quatre X,
et6+[i dans R] sur les huit Y. Ces identités résultent du degré14,
des degrés3/4 dans S et des4-[i dans R] voisins dans U union V union {z}.

En ajoutant tous les singletons au bord, on obtient59 ou60 sommets
et les voisinages des SIX centres H union {e,f} sont complets.
Il ne reste que40 ou39 sommets, tous indexés par des paires de L.
Leurs arêtes, leurs attaches aux sommets de charge0 du bord et leur
appartenance à la coclique ne sont pas déterminées par(14).

## 19. Exploitation effective sur tous les noyaux variables

`coclique_two_exception_cycles.py` ne choisit aucun des249 anciens noyaux.
Les arêtes libres de L, les attaches à U,V,z et la partie connue de C
sont des variables. Les bornes de voisins communs sont imposées sur le
graphe induit réel. Les modes et leur portée sont conservés séparément :

- `variable_core_cycles` : un témoin nécessaire sur43 sommets dans
  chacune des onze répartitions ; pas d'exclusion.
- `variable_core_triangle_h0` : les trois voisinages e,f,z sont complets,
  avec epsilon=0, donnant51 sommets ; onze témoins nécessaires. Ce test
  ajoute d'autres contraintes que la fermeture des quatre H ci-dessous.
- `variable_core_cycles_population` : ajout de la population résiduelle
  forcée par(13)–(14) et de ses quotas de C ; onze témoins nécessaires.
- `variable_core_hcomplete_h0` et `..._h1` : les six voisinages H,e,f
  sont complets sur59/60 sommets, avec population résiduelle commune ;
  chacune des onze répartitions a encore un témoin, soit22 au total.

Tous ces témoins ont été vérifiés directement en comptant leurs
voisinages et les résidus ; ils ne sont PAS des graphes à99 sommets.
Ils montrent que ces niveaux précis de contraintes ne suffisent pas
à exclure une répartition de cycles. Agrandir leur catalogue n'est
pas l'étape suivante.

Les témoins sont ensuite confrontés au recollement global :

- Cinq populations issues des témoins à43 sommets sont rejetées par
  des certificats arithmétiques (`negative_edge_population_certificates`).
  Leurs nombres de choix locaux linéaires faisables sont79 ou80 sur81 :
  ne pas les compter comme nouveaux exemples où les81 choix existent.
- Sur quatre populations issues des témoins à59/60 sommets, les deux
  témoins epsilon=1 testés donnent les contradictions8<=7 et2<=0.
  La première utilise quatre inégalités de paires saturées ; la seconde
  est déjà une combinaison de quotas d'un sommet. Les deux témoins
  epsilon=0 passent cette relaxation. Portée : ces populations, pas
  toutes les configurations epsilon=1 ou les répartitions concernées.
- Un premier test des types résiduels du bord59 avec six cycles de4
  laisse passer les37 types colorés requis face aux six voisinages
  fermés. `coclique_closed_border.py` conserve ce résultat nécessaire.

La frontière de la famille entière est désormais une coexistence
commune des39/40 sommets de types paires avec ce bord, en faisant encore
varier celui-ci. Les lois(10)–(14) sont acquises. Ni la famille(0,2),
ni un des onze types de cycles pris dans toute sa généralité ne sont
exclus à ce stade.

## 20. Essais entiers conservés avec leur portée

Le dernier ancien survivant passe séparément les appariements de tous
les centres du support, leur couplage avec bornes supérieures et les
capacités restantes. Le système linéaire binaire complet reste UNSAT
(nouveau pilote23,05s). Son exclusion certifiée utile est maintenant§16.

`coclique_parity_cuts.py` cherche des sommes d'équations modulo2 aux
solutions fractionnaires. Si leur support impair est J et leur second
membre vaut b modulo2, toute affectation F subset J de mauvaise parité
donne la loi entière

    sum_{j dans F}(1-x_j) + sum_{j dans J\F}x_j >= 1.       (15)

1113 coupures ont été trouvées en douze étapes et vérifiées par XOR
exact des équations sources. Elles coupent des solutions fractionnaires,
sans fournir une contradiction de toute la population à ce plafond.
Ce n'est pas une campagne de rangs modulaires.

`coclique_neighbourhood_hull.py` explore également la loi des prix
antisymétriques : dans un graphe réciproque, la somme des prix des
voisinages vaut zéro ; elle doit appartenir à la somme des intervalles
de prix des choix entiers admissibles. La génération de colonnes atteint
1134 choix puis un plafond LP, sans certificat. Ne pas relancer ce
pilote à l'identique ni annoncer une faisabilité de cette relaxation.

### État final de cette étape et contrôle ciblé

Le nouveau témoin à douze coupures,
`learned_cuts_e2_packing_continuation/population_000.json`, passe la
relaxation réciproque avec paires saturées, mais son modèle SRG complet
est INFEASIBLE en45,84s (2585 variables d'arêtes,165181 auxiliaires,
41664 branches,661 conflits). C'est un verdict CP-SAT, sans certificat
indépendant pour ce NOUVEAU témoin. Ne pas lui attribuer le certificat
99<=97 de l'ancien témoin. Tous les nouveaux pilotes sont terminés.

`check_coclique_coexistence_v3.py` reconstruit les nouvelles combinaisons
à partir des voisinages et les vérifie en entiers, indépendamment de
l'oracle de séparation : PASS pour neuf certificats arithmétiques,
les deux nouvelles coupures de populations,55 graphes induits témoins,
les onze répartitions de cycles et1113 coupures de parité. Les anciens
dossiers n'ont pas été réaudités. Rapport `checks_coexistence_v3.json`.

La suite utile est de coupler les choix réels des39/40 sommets restants
sur des bords variables, avec réemploi des contraintes de paires saturées.
Un certificat sur un bord fixé doit devenir une condition sur ses variables
avant de multiplier ces bords. La famille entière et C1 restent ouverts.

## 21. Transporter les contradictions lorsque le bord varie

Reprise du12 octobre au soir : conserver le cadre(0,2), une étape à la
fois, avec les règles de coexistence globales comme objectif. Les nouveaux
calculs ne modifient ni les anciens solveurs ni les travaux S3 du pair.

Soit B le bord59/60 de§18, W=B\S, et M le multigraphe sur les douze L dont
chaque arête ij représente un sommet restant de type{ i,j }. La multiplicité
m_ij est forcée par(14), mais le bord et ces multiplicités restent variables.
Pour u dans W poser

    d_u = 14 - deg_B(u),
    r_ui = 2 - [u~i] - |N_B(u) intersection N_B(i)|, i dans L.

**Lemme des facteurs simultanés.** Les voisins futurs de u définissent un
sous-multigraphe F_u de M, avec exactement d_u arêtes et degré r_ui en i.
Si u,v ont déjà tous leurs voisins communs dans B, les arêtes de F_u et F_v
doivent être disjointes, en distinguant les copies d'une même arête de M.

Preuve : chaque voisin futur de u possède exactement deux attaches i,j
dans L. Il contribue une fois au degré futur de u, et une fois à chacun
des deux quotas de voisins communs u-i et u-j. Un voisin futur partagé
par u,v augmenterait leur nombre de voisins communs au-delà du quota.

Une copie de type ij n'est utilisable par u que si d_u>0, r_ui>0, r_uj>0,
et si le graphe induit par{u,i,j} possède au plus une arête. Cette dernière
condition vient de N(t)=7K2 pour le futur sommet t : trois de ses voisins
ne peuvent contenir un chemin à deux arêtes. Noter A_u(ij) cette condition
nécessaire d'utilisation, sans la présenter comme suffisante.

**Triangles déjà fermés.** Si i~j, un sommet futur de type ij forme le
triangle i-j-t. Dans N(i), son partenaire est déjà j ; il ne peut pas
servir de partenaire à un autre voisin de i. Même propriété pour j.
Plus généralement, si y_u,ij compte les copies utilisées par u :

    sum_{u dans W, u~i} y_u,ij <= (1-[i~j]) m_ij,

et de même avec j. Ce sont des capacités communes à tous les facteurs,
pas seulement des tests indépendants pour chaque u.

Le bord historique epsilon0 avec six cycles4 viole cette règle : l'arête
27-12 n'a encore aucun voisin commun ; les seuls types encore possibles
pour ce partenaire sont déjà fermés par un triangle. Le certificat exact
de transport donne1<=0. Les deux autres bords testés donnent3<=1 et2<=0.
Ces exclusions portent sur toutes les complétions de ces bords induits,
sans fixer les couleurs des copies résiduelles dans la coclique.

## 22. Une loi de capacité directement exprimée sur un bord variable

Soit K un ensemble de sommets de W deux à deux saturés dans B. Pour chaque
u dans K choisir des entiers alpha_u et beta_ui. Poser

    D = sum_{u dans K} (alpha_u d_u + sum_i beta_ui r_ui),
    s_u(ij) = alpha_u + beta_ui + beta_uj.

Alors toute complétion impose

    D <= sum_{ij} m_ij max(0, s_u(ij) : u dans K, A_u(ij)).   (16)

Une copie d'une arête de M peut être utilisée par au plus un membre de K.
Sa contribution à D est donc au plus le meilleur score positif autorisé.
En sommant sur les copies on obtient(16), y compris pour des prix négatifs.

**Différence de portée avec§16 :** ici m_ij, d_u, r_ui, A_u(ij) et la
saturation des paires sont des expressions en arêtes du bord lui-même.
L'inégalité est ajoutée conditionnellement à ces saturations, avec sa
borne recalculée lorsque B change. Elle ne fige ni le noyau positif, ni
les attaches aux cycles, ni les autres arêtes de B. Elle est aussi valable
pour les autres répartitions de cycles et pour l'autre valeur d'epsilon,
si les sommets nommés sont présents. Aucun automorphisme n'est supposé.

`coclique_variable_border_cuts.py` extrait les prix par LP puis vérifie la
contradiction en entiers. Le modèle variable réemploie les prix, pas les
valeurs numériques m,d,r du témoin rejeté. Trois premières conditions
viennent des bords précédents. Cinq sont apprises sur de nouveaux bords.
Un modèle ajoutant tous les facteurs entiers individuels et les capacités
de partenaires apprend encore quatre conditions de coexistence à deux.
Enfin une condition à trois est extraite ci-dessous : treize conditions
au total dans `variable_border_cuts_v4/combined_13_cuts.json`.

Ce sont treize conditions sur des bords VARIABLES, distinctes des douze
coupures antérieures sur les populations d'un support FIXÉ. On ne les
additionne pas pour annoncer vingt-cinq familles disjointes exclues.
Les contradictions peuvent se recouvrir et leur union ne couvre pas
encore tous les bords(0,2).

## 23. Chaque paire peut coexister, mais pas les trois

Le bord `variable_border_cuts_v4/border_005.json` passe le premier oracle
fractionnaire sur309 groupes de taille1 ou2. Le groupe K={21,23,42} est
deux à deux saturé : ses paires, toutes non adjacentes, ont respectivement
les voisins communs déjà présents{13,16}, {0,16}, {16,55}.

Prendre les demandes pondérées

    u=21 : r_21,10 + r_21,14 - r_21,12 = 2+2-1 = 3,
    u=23 : r_23,10 + r_23,14           = 2+1   = 3,
    u=42 : r_42,10 + r_42,14 - r_42,4 = 1+2-1 = 2.

La demande totale vaut8. Après les interdictions d'utilisation, seules
sept copies peuvent fournir une contribution positive, au plus1 chacune :

    {5,14}, {6,10}, {7,10}, {8,14}, {9,10}, {10,13}, {13,14}.

Toutes ont multiplicité1. L'inégalité(16) donne donc **8<=7**.
Il s'agit d'un nouveau certificat sur un nouveau bord ; ne pas le confondre
avec le précédent8<=7 de§19 sur une population fixée.

`coclique_clique_witness.py` conserve en plus des témoins ENTIERS explicites
pour les trois singletons et les trois paires de K. Ils réalisent tous les
degrés d_u et les douze quotas r_ui, respectent A_u(ij), et les deux facteurs
d'une paire ne partagent aucune copie. Même en interdisant à un sommet
d'utiliser deux copies du même type, les six sous-groupes restent faisables.
Les choix diffèrent selon la paire : les trois réalisations ne sont pas
compatibles entre elles, exactement ce que prouve8<=7.

Portée précise : coexistence des facteurs résiduels avec les contraintes
énoncées ; pas existence de voisinages SRG complets ni de graphes à99.
Le certificat est installé comme une condition(16) sur le bord variable,
plutôt que comme l'interdiction de cette seule liste d'arêtes.

## 24. Les types doubles imposent une bipartition

Le lemme des paires saturées de§16 renforce encore les facteurs. Deux copies
d'un type ij partagent déjà i et j. Elles ne peuvent partager aucun autre
voisin. En particulier un u dans W ne peut choisir les deux copies :

    y_u,ij <= 1.                                            (17)

Chaque F_u est donc simple sur les types, même lorsque M a une arête double.
Les premiers pilotes de facteurs autorisaient encore y<=m ; ils constituent
une relaxation plus faible, conservée comme telle, et ne prouvent aucune
réalisabilité. La variante `--simple` ajoute(17).

Définir Gamma_B sur W en reliant les paires déjà saturées dans B. Pour un
type ij, soit T_ij l'ensemble des u demandant une copie de ce type. Alors :

- si m_ij=1, Gamma_B[T_ij] doit être sans arête ;
- si m_ij=2, Gamma_B[T_ij] doit être biparti.

Preuve : colorier un sommet demandeur par la copie réelle qu'il utilise.
La copie est unique par(17), et deux sommets reliés dans Gamma_B ne peuvent
utiliser la même. Réciproquement, une telle coloration suffit à distribuer
les copies pour CES contraintes de saturation, pas pour toutes celles du SRG.

Cette réduction montre exactement ce que les seuls contrôles par paires
laissent manquer : avec deux copies, chaque paire de demandes peut se
distribuer, mais un cycle impair de demandes incompatibles ne le peut pas.
Pour un cycle impair Q de Gamma_B, on obtient la condition nécessaire

    sum_{u dans Q} y_u,ij <= m_ij (|Q|-1)/2.                 (18)

Dans(16), on peut également remplacer m_ij fois le meilleur score par la
somme des m_ij meilleurs scores positifs admissibles DISTINCTS. C'est
valable parce qu'un même u n'utilise pas deux copies. La variante `--simple`
de l'oracle et du modèle encode cette borne renforcée.

Plus généralement, pour un groupe K quelconque, la capacité d'un type est
bornée par le meilleur poids d'un sous-ensemble admissible dont le graphe
de saturation est coloriable avec m_ij couleurs. Cette formulation fournit
une règle de coexistence pour des groupes plus grands qu'une paire ou une
clique ; elle ne suppose aucune taille particulière de coclique C dans sa
preuve, seulement les types et saturations connus du bord considéré.

Contrôle nouveau `check_coclique_coexistence_v4.py` : treize conditions de
bord, quatre certificats de transport complémentaires et les six témoins
entiers des sous-groupes, vérifiés depuis les graphes et les entiers sans
importer l'oracle ni un solveur. Les quatre certificats complémentaires ne
sont pas quatre bords supplémentaires aux treize déjà cités.

Les premiers modèles à facteurs tous couplés par paires atteignent90 puis
120 secondes sans verdict. Les modèles à conditions apprises produisent
des bords nécessaires en15–30 secondes. UNKNOWN reste distinct d'UNSAT.
Le pilote à treize conditions et tous les couples termine UNKNOWN600,14s
(2 068 112 branches,622 081 conflits). La variante à facteurs simples et
dix-sept conditions termine UNKNOWN300,56s (165 849 branches,1022 conflits).
Ces différences de compteurs ne mesurent pas un pourcentage de preuve.
La famille(0,2), chaque répartition entière, alpha21 et C1 restent ouverts.

## 25. Une obstruction arithmétique sans hypothèse de coclique

La même question de coexistence peut se poser sans choisir de types :
pour N'IMPORTE QUEL bord induit B d'un C1, noter A son adjacency et D
l'incidence entre B et les sommets absents. L'identité SRG par blocs impose

    K_B = 12I + 2J - A - A² = D D^t,
    (K_B)_uu = d_u = 14-deg_B(u).

Pour des poids ENTIERS z_u, chaque sommet absent t reçoit une charge
entière c_t=sum_{u~t} z_u. On connaît déjà, à partir du seul bord,

    Q = z^t K_B z = sum_t c_t²,
    T = sum_u z_u d_u = sum_t c_t.

Pour tout entier k, (c_t-k)(c_t-k-1)>=0. En sommant :

    Q >= (2k+1)T - (99-|B|) k(k+1).                        (19)

En particulier Q>=|T|. Cette obligation arithmétique est plus forte que
la seule positivité Q>=0 sur le même vecteur. Elle porte sur une population
COMMUNE de sommets absents ; des quotas séparément admissibles ne peuvent
pas contourner une somme de carrés ou de produits consécutifs impossible.
La preuve n'utilise ni coclique21/22, ni profil(0,2), ni automorphisme.

`coclique_residual_squares.py` utilise des vecteurs propres flottants comme
pistes de recherche, les arrondit puis réduit leur support. Seuls les
entiers et la vérification de(19) fondent les certificats. Sur le bord
`variable_border_cuts_v4/border_005.json`, quatre choix sur7 ou8 sommets
pondérés donnent respectivement Q=9<11=|T|, 17<19, 16<18 et22<24.
Les voisins communs et degrés utilisés sont ceux de TOUT le bord ; il ne
s'agit pas d'interdire le seul sous-graphe induit sur les7/8 sommets pondérés.

Les quatre inégalités sont exprimées linéairement dans les degrés et les
comptes de voisins communs du modèle variable, déjà disponibles. Elles
s'ajoutent aux treize conditions de capacité, soit dix-sept conditions
réutilisables, sans supposer que leurs domaines d'exclusion sont disjoints.
La variante `--square-cuts` permet d'apprendre les suivantes de la même façon.

Le contrôle indépendant V4 vérifie les quatre nouveaux certificats en
entiers. Un contrôle positif sur la grille3x3 vérifie l'identité par blocs
et les inégalités sur243 vecteurs de poids dans{-1,0,1}, avec les paramètres
SRG de cette grille. Il ne prétend pas disposer d'un exemple positif C1.

### Réinjection effective et état final de V4

Le modèle léger conservant les dix-sept conditions sur un bord variable
trouve un nouveau bord en17,28s. Quatre NOUVEAUX certificats(19) le rejettent :
Q=15<17,14<16,10<12,13<15. Ils sont ajoutés dans
`variable_border_cuts_square_learning_v4/cuts.json`, qui contient désormais
**21 conditions :13 de capacité et8 de carrés entiers**. Les nouveaux
certificats sont vérifiés indépendamment. Un nouveau bord satisfaisant ces
21 conditions n'a pas encore été recherché ; le dernier bord en satisfaisait
17 et vient d'être exclu. Ce pilote léger ne contient pas les facteurs tous
couplés du modèle plus fort resté UNKNOWN : ne pas mélanger leurs statuts.

Les21 conditions ne comptent pas21 familles disjointes et ne couvrent pas
encore tout(0,2). Elles montrent que la boucle extrait maintenant aussi
des contraintes indépendantes de l'hypothèse de coclique, et les transporte
lorsque le bord varie. Les trois familles de lois ont leurs preuves :
facteurs et capacités communes ; répartition des copies et cycles impairs ;
charges entières et produits de deux entiers consécutifs.

L'interdiction des cycles impairs est prouvée en§24. Le modèle `--simple`
impose déjà y<=1 et les capacités par paires ; il ne code PAS encore une
coloration complète pour chaque type double. Cette étape et le renforcement
par les nouveaux certificats(19) donnent une frontière précise, sans relancer
à l'identique les pilotes90/120/600/300 secondes ni agrandir un catalogue.

Tous les nouveaux pilotes V4 sont terminés. Journaux, configurations et
mesures de ressources sont conservés ; les calculs couplés sont restés sous
environ1Go de mémoire de travail au pic observé. Les solveurs historiques et
l'observateur ont continué. Le contrôle V4 confirme les13 conditions de
capacité, leurs bornes renforcées, huit certificats de carrés, quatre preuves
de transport complémentaires et les six sous-groupes propres du triplet.
Les exemples de transport et certaines conditions excluent les mêmes bords.

## 26. V5 : les copies sont effectivement partagées

La reprise suivant le message586 attaque la frontière de§24. Dans
`coclique_copy_sharing.py`, chaque type ij possède deux emplacements,
actifs si et seulement si m_ij>=1 et m_ij=2. Les variables binaires
x_(u,ij,c) désignent les MÊMES copies pour tous les u. On impose

    x_(u,ij,0) + x_(u,ij,1) = y_(u,ij) <= 1,
    x_(u,ij,c) + x_(v,ij,c) <= 1 si uv est saturée dans B.

Chaque copie a au plus douze voisins dans W et au plus un partenaire
auprès de chacun de ses deux ancrages non adjacents. Si les ancrages sont
adjacents, aucun partenaire supplémentaire n'est permis. L'échange des
deux noms de copies permet de fixer la première incidence sur la copie0.
Il ne s'agit pas d'imposer un automorphisme au graphe.

Deux pilotes à deux travailleurs sont terminés UNKNOWN :180,08s avec
21 conditions, puis180,10s avec25 conditions et les quotas par copie de
§28. Le premier fait1 020 466 branches et225 919 conflits ; le second
639 560 branches et184 291 conflits. Ces compteurs ne sont ni un
pourcentage de preuve ni la mesure d'une famille exclue. Les options
supplémentaires `--gram` et `--partners` existent, mais n'ont pas été
exécutées dans cette campagne ; ne pas leur attribuer un résultat.

Pour exploiter la contrainte sans attendre davantage le même calcul,
`coclique_copy_cycles.py` sépare les violations sur des bords variables.
Avec une copie, il cherche une arête entre demandeurs ; avec deux,
un cycle impair. Une coupe conditionnelle(18) est réinjectée sous les
prédicats de saturation de ses arêtes. Tous les comptes sont recalculés
sur le nouveau bord. L'absence de ces deux défauts équivaut exactement
au partage des copies POUR LES CONTRAINTES DE SATURATION. Elle ne
garantit pas les quotas individuels, les degrés ni tous les voisins
communs du SRG. La séparation finie ci-dessous n'est pas allée jusqu'à
une affectation satisfaisant tous ces contrôles.

## 27. Des cycles sans corde donnent5<=4

Le nouveau bord `copy_sharing_light_v5/border_000.json` satisfait les
21 conditions V4 et possède des facteurs simples individuels. Dans
les facteurs effectivement choisis, trois types doubles présentent
les cycles sans corde suivants dans Gamma_B :

| Type | Cycle des demandeurs | Demande | Capacité des deux copies |
|---|---|---:|---:|
| {5,8} | 24,29,19,43,50 | 5 | 4 |
| {6,10} | 49,38,33,42,51 | 5 | 4 |
| {8,15} | 28,23,20,26,29 | 5 | 4 |

Une couleur peut occuper au plus deux sommets d'un C5. Deux copies
servent donc au plus quatre demandeurs. Chaque sous-ensemble propre
de chacun de ces cinq sommets est coloriable avec deux couleurs ;
les témoins explicites sont dans le contrôle V5. Aucun triangle de
saturation n'explique l'échec sur ces mêmes cinq sommets.

Portée essentielle : c'est l'affectation de facteurs CHOISIE qui est
exclue. Ce n'est pas une preuve que toute autre affectation sur ce
bord échoue. Indépendamment, quatre nouvelles inégalités de carrés
excluent le bord entier :15<17,24<26,14<16,14<16, avec des poids
distincts. Ne pas confondre ces deux niveaux de certificat.

## 28. L'égalité arithmétique force chaque copie

La loi(19) donne davantage qu'une inégalité. Si elle est une égalité,

    sum_t (c_t-k)(c_t-k-1) = 0,

chaque terme entier non négatif est nul. Donc CHAQUE copie vérifie
c_t dans {k,k+1}. De même,

    Q - 2aT + M a² = sum_t (c_t-a)² = 0
    implique c_t=a pour chaque copie, où M=99-|B|.            (20)

Cette propagation d'une égalité globale vers toutes les colonnes
ne suppose aucune coclique, aucun type de cycle ni automorphisme.

Application aux voisinages complets : soit s dans B de degré14 dans B.
Pour z=1_(N(s)), chaque sommet absent est non adjacent à s. Les seuls
comptes du bord imposent T=2M et Q=4M. Ainsi(20), avec a=2, impose

    |N(t) intersect N(s)| = 2 pour CHAQUE t absent.

On peut aussi le lire directement dans mu=2. Le calcul de variance
explique comment cet exemple s'insère dans la loi générale des charges.
Pour les bords60 de cette campagne, les six voisinages complets donnent
T=78, Q=156, variance nulle. Si t a le type ij et I_t est son ensemble
de voisins dans W, sa contrainte exacte est

    |I_t intersect N(s)| = q_s,ij := 2-|{i,j} intersect N(s)|.

En sommant les copies, on obtient la réciprocité de colonne

    sum_(u dans W intersect N(s)) y_(u,ij) = m_ij q_s,ij.     (21)

Pour s=e et s=f, (21) donne respectivement

    sum_(u dans U) y_(u,ij) + y_(z,ij) = 2 m_ij,
    sum_(v dans V) y_(v,ij) + y_(z,ij) = 2 m_ij.

La simple existence de chaque facteur individuel ne forçait pas(21).
Le premier témoin V5 la viole sur127 couples(s,type), malgré ses
quotas de lignes corrects. `coclique_closed_star_balance.py` impose
(21) simultanément pour les six sommets0,1,2,3,16,17, en laissant le
bord variable. Trois témoins nouveaux satisfont ces égalités agrégées ;
cela ne remplace toujours pas les quotas COPIE PAR COPIE.

## 29. Un chemin biparti peut encore être impossible

Voici une obligation strictement au-delà de la seule bipartition.
Fixer un type T à au plus deux copies, un demandeur u, et un sommet s
dont le voisinage est complet. Si u demande une copie, TOUS ses
voisins demandeurs dans Gamma_B doivent utiliser l'autre copie.
Par conséquent, parmi ceux qui appartiennent aussi à N(s), il peut
y en avoir au plus q_s,T. Sous ces hypothèses :

    y_(u,T)=1 implique
    sum_(v dans N_Gamma(u) intersect N(s)) y_(v,T) <= q_s,T.  (22)

La nécessité de(22) ne dépend pas du profil(0,2) : elle vaut dès
que l'on connaît les deux copies possibles, les saturations et le
quota d'un voisinage complet. C'est une contrainte sur la coexistence
de la coloration et des capacités, pas une recherche de rang.

Un sous-ensemble de q+1 feuilles suffit à certifier une violation.
Les q+2 demandeurs centre+feuilles ne peuvent tous choisir ce type :
leur somme de y est au plus q+1. La coupe est activée seulement quand
les arêtes de saturation et les attaches des feuilles à s sont présentes.
`coclique_copy_stars.py` transporte cette règle sur les bords variables.

Deux premiers exemples, sur `copy_cycle_closed_learning_v5/border_001.json` :

| Type double | s | Centre | Feuilles | Quota d'une copie |
|---|---:|---:|---|---:|
| {5,15} | 1 | 25 | 21,48 | 1 |
| {7,11} | 0 | 34 | 35,47 | 1 |

Dans chaque cas Gamma_B induit un P3, donc il est biparti. Les deux
feuilles doivent néanmoins prendre la même copie et occupent deux
places d'un quota1 :2<=1. Chacun des six sous-ensembles propres non
vides des trois demandeurs admet une coloration respectant ces
capacités partielles ; les colorations sont sauvegardées. Il s'agit
encore des contraintes indiquées, pas de voisinages SRG complets.
Ces deux règles sont réinjectées ; le témoin suivant les satisfait
mais donne deux nouvelles obstructions analogues. On n'abandonne donc
pas le partage lorsqu'une coloration existe : on couple ses charges.

## 30. Bilan reproductible V5 et frontière

Les sept nouveaux bords sont obtenus en21,71 ;38,95 ;17,81 ;34,56 ;
32,09 ;23,80 ;42,08 secondes. Les trois derniers imposent(21).
Chacun est ensuite exclu par quatre nouveaux certificats entiers de
carrés, indépendamment des coupures sur les choix de facteurs.
Les deux modèles monolithiques de§26 sont UNKNOWN180s. Tous ces
pilotes sont terminés ; aucun nouveau calcul V5 n'est laissé en cours.

Fichier de reprise : `copy_star_learning_v5/cuts.json`,304 conditions :
13 capacités V4,36 carrés dont28 nouveaux,251 capacités de cycles
(208 arêtes,24 triangles,18 cycles5 et un cycle7), quatre capacités
de voisinage complet(22). Il ne s'agit PAS de304 familles disjointes.
Les255 règles sur copies concernent les variables de facteurs, donc
leur fichier exige un modèle avec facteurs ; les49 autres portent
sur le bord. Le dernier témoin en satisfaisait259 ;45 nouvelles règles
l'ont rejeté. Aucun nouveau bord à304 conditions n'a été recherché.

`check_coclique_coexistence_v5.py` vérifie indépendamment, en entiers
et sans importer les séparateurs ni CP-SAT, les251 cycles,28 carrés,
quatre capacités(22), les facteurs des sept témoins, les identités de
variance, les colorations propres des trois C5 et des quatre P3.
Six preuves locales supplémentaires forcent un type par des prix de
degrés ; elles n'ont pas donné de cycle impair FORCÉ par les seuls
quotas. Un contrôle positif sur la grille3x3 vérifie la propagation
des égalités, avec123 cas d'égalité. Résultat : PASS.

Les sondes CP-SAT sur un bord fixe sont documentées séparément dans
`copy_sharing_light_v5/copy_probe.json`. Leurs UNSAT ne sont pas des
certificats indépendants ; aucune nouvelle exclusion n'en est déduite.
Les journaux bruts, paramètres et empreintes de code aux lancements
sont conservés. Le pilote à copies réelles a été observé vers0,98Go
de mémoire de travail ; la télémétrie n'est pas un relevé continu de
pics pour tous les pilotes. Deux travailleurs étaient utilisés.

Frontière précise : une coloration doit maintenant satisfaire ensemble
les six vecteurs de quotas et les comptes de voisins communs entre tous
les anciens sommets ; puis il reste à coupler les arêtes entre copies.
Les quotas et les coupes ne constituent pas encore une complétion SRG.
Aucune classe entière parmi les onze partitions n'est fermée par V5 ;
(0,2), alpha21 et C1 restent ouverts. Le solveur co-Heawood et son
observateur historiques ont continué sans intervention.

## 31. V6 : traiter la famille entière et éliminer le bloc restant

Le recadrage relayé en589 demande de sortir de l'accumulation de sous-cas.
La V6 n'ajoute donc pas un bord à la liste des304 coupures. Elle construit
un modèle commun à TOUT(0,2), puis démontre un critère de complétion valable
pour tout bord C1 contenant au moins un voisinage complet. Ce critère ne
suppose ni coclique21/22, ni automorphisme, ni classe de cycles.

Les quatre H forment le C4 déjà démontré. Deux H adjacents ont leur unique
voisin commun X dans le support ; deux H opposés ont déjà leurs deux
voisins communs H dans le support. Leurs voisins supplémentaires sont
donc disjoints. Chaque H possède deux voisins dans C et six voisins de
charge nulle hors de C, en plus de ses six voisins positifs. On peut
numéroter ces quatre paires de C et ces quatre groupes de six sans
restreindre les graphes. Ceci donne un SEUL bord :

    B = C union H union L union Z_H,  |B|=21+4+12+24=61,
    M = {e,f} union Z_0,             |M|=2+36=38.           (23)

Les quatre voisinages H sont complets dans B. La coclique C entière est
dans B. Les arêtes L-L, les incidences aux deux exceptions, le voisin
commun z et les cycles4k restent variables. Les ordres de signatures
utilisés dans le code ne sont que des choix de noms à l'intérieur des
groupes échangeables ; ils ne sont pas stricts et autorisent les doublons.

Un premier modèle exact sur99 sommets a terminé UNKNOWN240,32s :
4230 variables d'arêtes,375693 produits,523748 branches,272164 conflits,
deux travailleurs. Il impose les degrés14 et seulement les majorations
de voisins communs c_uv<=2-a_uv. Elles suffisent : pour chaque u,
la somme réelle vaut14*13=182 et la somme des majorants vaut également
14*1+84*2=182. Toutes les inégalités sont donc des égalités. Le contrôle
positif de cet encodeur sur la grille3x3 passe. Cela ne constitue aucune
exclusion de(0,2).

Le bord(23) permet une étape plus ciblée : chercher UNE matrice binaire D,
61 lignes et38 colonnes, commune à tous les sommets, telle que

    D D^t = K := 12I+2J-B-B².                              (24)

Ici B désigne aussi sa matrice d'adjacence. (24) impose simultanément
tous les degrés et tous les voisins communs des61 anciens sommets.
Les38 sommets sont des colonnes réelles partagées ; des facteurs locaux
individuellement réalisables ne suffisent pas. Les arêtes entre ces38
sommets ne sont plus recherchées dans cette première étape : les§32–34
décrivent EXACTEMENT les possibilités restantes.

## 32. Théorème de fermeture d'une factorisation binaire

Soit B une matrice d'adjacence sur n sommets, m=99-n>0. Supposons :

* D est binaire de taille n par m et satisfait(24) ;
* B contient un sommet s de degré14, donc son voisinage complet.

Noter d=14*1-B1, F=2J-(B+I)D et D^+ l'inverse de Moore–Penrose.
Définir

    E0 = D^+ F,        P = I-D^+D.                         (25)

P est le projecteur orthogonal sur ker D. Alors E0 est symétrique,
E0 P=0, et toutes les complétions SRG de B,D sont EXACTEMENT les matrices

    A = [ B    D  ],    E = E0+3P-7Q,                      (26)
        [ D^t  E  ]

où Q est un projecteur orthogonal vérifiant PQ=Q et où E est ENTIÈRE.
Il n'est pas nécessaire d'ajouter séparément « diagonale nulle et
coefficients0/1 » : l'intégralité les force, comme démontré au§34.

En particulier, si ker D=0, il n'y a aucune arête restante libre :

    E = (D^t D)^(-1) D^t [2J-(B+I)D],
    complétion C1 <=> tous les coefficients de E sont entiers. (27)

Ne pas escamoter l'hypothèse : la nullité peut être non nulle. (26),
et non seulement(27), est le critère couvrant TOUS les cas. Il ne s'agit
pas d'un catalogue de rangs : une seule formule décrit la liberté
résiduelle et son couplage. Trouver D, puis éliminer la liberté de Q
si elle existe, reste un travail mathématique réel.

## 33. Preuve de la fermeture, y compris le cas singulier

La diagonale de(24) et la binarité de D donnent D1=d. Un calcul direct
fournit

    KB-BK = 2(d1^t-1d^t),
    K1 = -2m*1+(B+15I)d.                                 (28)

Pour un sommet complet s, la ligne s de D est nulle. Poser w=B e_s,
l'indicatrice de son voisinage. (28) donne Kw=2d et

    w^t d=2m,    w^t K w=4m,
    ||D^t w-2*1||²=0.

Ainsi D^t w=2*1 et surtout 1_m appartient à im D^t. Cette conséquence
de variance nulle, déjà rencontrée en V5, rend maintenant possible la
fermeture de TOUT le bloc restant.

Pour z dans ker D^t, on a d^t z=0, puis

    D D^t Bz=KBz=2d(1^t z),
    D[D^t Bz-2(1^t z)*1_m]=0.

Le vecteur entre crochets appartient à im D^t, puisque 1_m y appartient.
Il est aussi dans ker D ; il est donc nul. Par conséquent z^t F=0.
Cela prouve que les colonnes de F appartiennent à im D : DE0=F.
En outre F annule ker D, car ce noyau est orthogonal à1_m. Donc E0P=0.

La matrice

    F D^t = 2*1*d^t-(B+I)K

est symétrique par(28). Comme E0 agit sur im D^t et y est déterminée
par DE0=F, elle est elle-même symétrique. En utilisant la seconde
identité(28), on obtient F1=D(14*1-D^t1), donc

    E0*1=14*1-D^t1.                                     (29)

Soit A0 le bloc(26) avec E=E0. Il est symétrique et régulier de degré14.
Le défaut polynomial A0²+A0-12I-2J n'a que son bloc inférieur droit L
éventuellement non nul. Il commute avec A0, d'où DL=0. Sur ker D,
E0, D^tD et J sont nuls : L y vaut -12I. Par symétrie,

    E0²+E0+D^tD = 12(I-P)+2J.                           (30)

Toute autre solution symétrique de DE=F est E=E0+T avec T=PTP. Elle
reste régulière puisque P1=0. L'équation polynomiale complète équivaut
à T²+T=12P. Sur ker D, les seules valeurs propres possibles de T sont
3 et-4 ; par le théorème spectral, T=3P-7Q, avec Q projecteur contenu
dans P. Cela prouve(26) dans les deux sens au niveau réel.

## 34. Pourquoi l'intégralité suffit et comment la vérifier

Soit A une matrice symétrique ENTIÈRE vérifiant A1=14*1 et
A²+A=12I+2J. Pour chaque ligne i, soustraire la somme de ligne à
l'équation diagonale donne

    a_ii² + sum_(j!=i) a_ij(a_ij-1) = 0.                 (31)

Tous les termes sont des entiers non négatifs. Ils sont donc tous nuls :
a_ii=0 et a_ij dans{0,1}. A est exactement une matrice d'adjacence C1. Appliqué
à(26), cela démontre le critère d'intégralité, sans test supplémentaire
de chacune des arêtes restantes. La même preuve vaut pour
A²+A=(k-mu)I+mu J et A1=k*1, donc dépasse ce seul problème et les cocliques.

Le cas singulier donne aussi des conditions nécessaires explicites.
Si h=tr P, la diagonale nulle de E impose

    Q_ii=(E0_ii+3P_ii)/7,
    -3P_ii <= E0_ii <= 4P_ii,
    (tr E0+3h)/7 est un entier entre0 et h.              (32)

Ces contraintes ne remplacent pas Q²=Q. Elles servent à propager
l'intégralité et les capacités d'une seule complétion commune.

Implémentation : `coclique_global_completion.py`, calcul rationnel exact.
Trois contrôles NOUVEAUX : grille3x3 avec bord5 (noyau de dimension1),
grille3x3 avec bord6 (noyau nul), et application au graphe BvLS déjà
disponible avec39 sommets effacés (noyau nul). Dans ce dernier contrôle,
les741 arêtes potentielles entre les39 sommets sont reconstruites d'un
seul calcul rationnel ; elles coïncident avec le bloc effacé. Ce n'est
pas un nouvel audit des quatre graphes243 étudiés auparavant.

Le contrôle singulier conserve les deux choix de projecteur. Le bon
choix restitue le graphe ; l'autre donne une matrice de coefficients
1/4 et3/4, bien qu'elle satisfasse les équations RÉELLES. Il illustre
pourquoi l'intégralité est une obligation et ne peut pas être supposée.
Certificats : `data/codex_coclique_defects/global_completion_v6/`.

## 35. Calcul global V6 : portée et limite

`coclique_global_boundary.py` utilise le bord(23) avec toutes les arêtes
restantes variables et les38 colonnes partagées. Il impose(24), les
comptes exacts de voisins dans C, les quatre voisinages H complets et
leurs quotas par colonne. Ce modèle couvre TOUT(0,2) : aucun noyau,
epsilon ou type de cycles n'est fixé. Il a3528 variables d'incidence
et128106 produits, contre4230 et375693 dans le modèle sur99 complet.
La taille du codage des produits est réduite d'environ66%, et non le
nombre de graphes de la famille. Un témoin est nécessaire jusqu'au
contrôle(26)/(27) ; le programme ne transforme pas SAT de(24) en SRG.
La recherche de Q dans le cas singulier n'est pas encore implémentée.

Le pilote à deux travailleurs termine UNKNOWN300,15s :1 617 370 branches,
573 963 conflits, construction3,78s. Il n'a produit ni factorisation D
ni certificat d'impossibilité. En particulier, le critère d'intégralité
n'a pas encore été appliqué à un nouveau candidat C1 issu de ce pilote.
La mémoire observée atteint environ1,11Go (pic du processus mesuré lors
des échantillons), contre environ3,19Go observés pour le modèle complet.
Les deux modèles étant différents, leurs débits de conflits ne mesurent
pas un gain de vitesse de preuve. Tous les nouveaux pilotes V6 sont finis.

Le contrôle indépendant `check_coclique_coexistence_v6.py` relit les
trois nouveaux certificats rationnels sans importer le constructeur :
PASS. Il vérifie aussi que l'autre choix de projecteur du contrôle
singulier satisfait les équations réelles mais échoue à l'intégralité.
Journaux et paramètres : `global_profile_v6/` et `global_boundary_v6/` ;
certificats : `global_completion_v6/`, sous `data/codex_coclique_defects/`.

Le théorème ne prouve pas que toute factorisation de(24) échoue :
(0,2), alpha21 et C1 restent ouverts. Il fournit une obstruction globale
précise à viser : l'existence d'une factorisation binaire dont la
complétion forcée, ou sa correction par un unique Q, est entière.

L'objectif calculatoire suivant est donc(24) sur le bord unique61/38,
avec le critère(26) disponible pour fermer tout le bloc restant. Le
modèle exact de99 et le modèle réduit ne doivent pas être relancés à
l'identique sous prétexte que leur statut est UNKNOWN. Aucune nouvelle
exclusion de bord ni nouvelle coupure particulière n'a été ajoutée aux304
conditions de V5. Le solveur co-Heawood et son observateur restent actifs.

## 36. V7 : les libertés affines portent aussi tout le défaut quadratique

13 octobre2026, après redémarrage du PC. Les anciens processus co-Heawood
et leur observateur se sont arrêtés avec le PC ; les mentions précédentes
« restent actifs » décrivent le12 octobre, pas la situation du13.

La formule à projecteur du§32 peut être transformée en un système discret
fini, y compris lorsque D est singulière. On conserve EXACTEMENT les
hypothèses du§32 ; aucune indépendance automatique des colonnes n'est supposée.

Définir l'espace vectoriel rationnel

    V_D = { T : T=T^t, diag T=0, D T=0 },   delta=dim V_D.     (33)

Les solutions réelles symétriques à diagonale nulle de DE=F forment soit
l'ensemble vide, soit un espace affine E_*+V_D. Si N est une base colonne
de ker D, de dimension h, toute matrice symétrique annulée par D est de
la forme NSN^t, S symétrique h par h. Par conséquent

    delta = h(h+1)/2-rang[S -> diag(NSN^t)]
          <= h(h-1)/2.                                      (34)

La dernière borne vient de h lignes indépendantes de N : leurs produits
extérieurs sont linéairement indépendants. En particulier h=1 implique
delta=0 : un noyau non nul n'entraîne PAS nécessairement de liberté sur E
une fois la symétrie et la diagonale nulle imposées.

Choisir delta paires J={(u_i,v_i)} telles que l'évaluation T -> (T_uv)_J
soit injective sur V_D. Ceci se fait par élimination rationnelle. On
normalise une base T_i pour avoir (T_i)_(u_j,v_j)=1 si i=j,0 sinon. Il
existe alors une matrice rationnelle E_base, nulle sur les paires J, telle
que toutes les complétions linéaires s'écrivent

    E=E_base+sum_i x_i T_i,     x_i=E_(u_i,v_i).              (35)

Pour un graphe, les delta x_i sont binaires ; toutes les autres arêtes
en sont des fonctions affines rationnelles. Il faut encore imposer que
TOUTES ces entrées appartiennent à{0,1}, et non seulement les x_i.

THÉORÈME. Parmi les matrices d'adjacence E satisfaisant DE=F, il suffit
de vérifier l'équation des voisins communs sur les delta paires J :

    (D^tD+E²+E)_(u,v)=2,                 (u,v) dans J.         (36)

Toutes les autres équations du graphe entier en découlent.

Preuve. La fermeture linéaire et le voisinage complet garantissent
E1=14*1-D^t1, comme au§33. Construire A avec les trois blocs et poser
L=D^tD+E²+E-12I-2J. Le défaut de A est nul hors de L. A est symétrique
et régulière, donc son défaut polynomial commute avec A : DL=0. Puisque
E est une matrice d'adjacence, la diagonale de L vaut le degré total
moins14, donc zéro. Ainsi L appartient au MÊME espace V_D que les
variations linéaires de E. (36) annule ses delta coordonnées injectives,
donc L=0. Réciproquement toute vraie complétion satisfait ces conditions.

Cette preuve vaut aussi pour A²+A=(k-mu)I+mu J avec les hypothèses de
fermeture correspondantes. Elle ne remplace pas la binarité de E par
l'intégralité seule : ici la diagonale du défaut est annulée grâce à
la binarité, AVANT d'invoquer les équations quadratiques sélectionnées.

Conséquences effectives : delta=0 donne au plus UNE complétion, même avec
un noyau non nul ; delta=1 donne au plus DEUX candidats ; en général au
plus2^delta affectations des arêtes libres. Le nombre d'équations
quadratiques nécessaires est delta, contre m(m-1)/2 précédemment.
Cela ne prouve pas que delta est petit pour tous les candidats C1.

Implémentation exacte : `coclique_affine_completion.py`. Elle calcule
l'espace affine, impose toutes les entrées binaires, puis seulement les
paires J ; tout témoin est contrôlé sur le polynôme complet. La recherche
du cas singulier, absente de V6, est ainsi implémentée sans paramétrer un
projecteur réel. Un délai expiré reste UNKNOWN, pas une exclusion.

## 37. Une fermeture quadratique se réduit réellement à une parité

Nouveaux contrôles du mécanisme, distincts des anciens audits :

* Grille3x3, bord formé d'une étoile fermée : h=1 mais delta=0,
  complétion binaire unique ; aucune équation quadratique restante.
* Petersen, même choix de bord : h=3, delta=3, trois arêtes libres x,y,z.
  Les HUIT choix binaires donnent des matrices d'adjacence satisfaisant
  toutes les équations linéaires, les degrés et les capacités D^tD+E<=mu.
  Les trois défauts sélectionnés sont exactement

      x-y-z+2yz,    y-x-z+2xz,    z-x-y+2xy.

  Leur annulation simultanée équivaut à UNE loi : x+y+z=0 modulo2.
  Quatre candidats passent, quatre échouent. Les trois choix individuels
  et toutes leurs paires se prolongent ; leur coexistence triple porte
  la seule obstruction. Cet exemple illustre une extraction complète,
  pas une exclusion d'une famille du problème à99.
* Paley13 et Paley17 : h=delta=0, complétions uniques retrouvées.

Les certificats rationnels sont dans `affine_completion_v7/`. Le contrôle
séparé `check_coclique_affine_completion.py` relit les données, vérifie les
dimensions, l'injectivité des coordonnées, la totalité des huit choix
Petersen et les équations complètes. Il ne réimporte pas le constructeur.

## 38. Exiger aussi la coexistence des colonnes pendant la construction

Le modèle V6 imposait surtout le bloc B-B. Des obligations nécessaires
supplémentaires peuvent être imposées AVANT d'obtenir un D complet :

    R=D^tD,     R_uv+E_uv<=2 pour u!=v,
    E1=14*1-D^t1,
    R_uv=2 => E_uw+E_vw<=1 pour tout w.                    (37)

La première interdit trois voisins communs déjà dans B et interdit une
arête lorsque deux voisins communs sont déjà présents. La troisième
interdit alors TOUT voisin commun supplémentaire dans le bloc manquant.
E est une seule matrice d'adjacence partagée, fournissant les degrés
restants ; les choix de partenaires ne sont pas indépendants par sommet.

Dans (0,2), E_ef=1. Pour chaque Z0, la loi des charges impose exactement
sum_(l dans L) D_lu - E_eu-E_fu=2. Le nouveau modèle impose aussi TOUTES
les équations mixtes pour les21 lignes de la coclique, avec le même E.
Il couvre toujours la famille entière sans fixer un noyau, une classe
de cycles ni epsilon. Il reste NÉCESSAIRE : un témoin doit être soumis
au critère exact des§36–37 avant d'être appelé graphe SRG.

Code `coclique_column_coexistence.py`, mesures de ressources intégrées.
Construction :128106 anciens produits plus96945 nouveaux, soit225051 ;
703 arêtes résiduelles,703 paires de colonnes. Un pilote de900s à huit
travailleurs est lancé dans `global_columns_v7/`. Lire son `result.json`
pour le verdict final ; une absence de fichier signifie qu'il n'est pas
encore enregistré. Les journaux V6 ne sont pas écrasés.

Le pilote `global_columns_v7` a terminé UNKNOWN901,503s : compteur de
réponse582416 conflits/1769420 branches, pas de D. Ces compteurs sont
ceux de la réponse d'un travailleur, PAS la somme du portefeuille.
Le journal conserve les statistiques de chacun : fs_random_no_lp925362
conflits, no_lp582416, quick_restart_no_lp158761. max_lp dépense son
temps sur597447 lignes/198344 colonnes, sans aucune résolution LP
OPTIMAL et avec392 conflits. Le pilote suivant conserve des moteurs LP
mais écarte max_lp. Aucun débit n'est un pourcentage de résolution.

## 39. Les arêtes résiduelles non couvertes doivent former des triangles

Pour une vraie complétion avec lambda1, poser

    U_uv = E_uv si (D^tD)_uv=0, et0 sinon.                 (38)

Toute arête de E a soit son unique triangle déjà complété dans B,
soit son unique triangle entièrement dans le bloc manquant. Dans le
second cas les trois arêtes du triangle appartiennent à U : une arête
ayant déjà un voisin commun dans B ne peut appartenir aussi à ce triangle.
Le graphe U possède donc une partition de ses arêtes en triangles, et
ceux-ci sont EXACTEMENT ses triangles. En particulier chaque degré de U
est pair et |E(U)| est divisible par3. La partition est imposée avec une
seule variable par triple, pas avec des choix indépendants par arête.

Le mode `--triangles` impose8436 variables de triangles pour les38
sommets, leur équivalence aux trois arêtes U et leur couverture unique.
Il ajoute les conséquences de parité et de divisibilité et étend les
paires saturées à R_uv+E_uv=2. Cela ferme exactement lambda1 pour toutes
les arêtes internes à E, et mu2 pour les non-arêtes avec R_uv=2. Les
autres non-arêtes et une partie des équations mixtes restent à fermer :
il s'agit encore d'un modèle nécessaire, pas d'une nouvelle équivalence.

Contrôle ciblé sur les anciens certificats, sans refaire leurs audits :
le bloc39 du BvLS donne69 arêtes U, exactement23 triangles qui partitionnent
ces arêtes, et tous les degrés pairs. Résultat sauvegardé dans
`affine_completion_v7/triangle_cover_check.json`.

Pilote `global_triangles_v7`,1800s,huit travailleurs, --no-max-lp, lancé
après le pilote précédent. Les deux sources de calcul sont copiées dans
leurs dossiers de sortie ; ressources et paramètres sont conservés.

## 40. Une grille3x3 impose une loi de défauts et interdit une fermeture de H

Cette conséquence est déduite des profils déjà établis, sans recherche
de rang ni hypothèse d'automorphisme. Soit R une grille3x3 induite (le
graphe des tours à9 sommets) dans un hypothétique graphe à99.

Fait de départ déjà utilisé dans les dossiers C2 : chaque sommet hors
de R a EXACTEMENT un voisin dans R. En effet, toutes les paires de R
ont déjà dans R leurs1 ou2 voisins communs autorisés ; un sommet externe
ne peut donc en toucher deux. Les9 sommets de R ont chacun10 voisins
externes, soit90 incidences pour90 sommets externes, d'où l'égalité partout.

Pour une coclique C de21 sommets, poser t=|C intersect R| et reprendre
q=4*1-(A+4I)1_C. Le comptage des incidences entre C et R donne

    sum_(r dans R) b_C(r) = 4t+(21-t)=21+3t,
    sum_(r dans R) q_r = 15-7t.                           (39)

Si C est maximale par inclusion, nos profils donnent a=n1<=1,
b=n2=6-3a-e et2<=e=n5<=6. Hors de C, les charges sont3 (a fois),
2 (b fois),1,0,-1. Sur NEUF sommets hors C leur somme est au plus
9+2a+b=15-a-e<=13. Ainsi t=0, qui exigerait15, est impossible.
Une grille rencontre donc toute coclique21 maximale. Comme t<=3,
les possibilités sont t=1 ou2 ; t=3 exige une somme-6 sur les six
sommets restants, donc tous les six sont négatifs. Cela force le profil
(0,6) et le graphe négatif induit C6 (complément d'une coclique maximale
dans la grille). Il ne s'agit pas d'exclure ce dernier profil.

APPLICATION À TOUT(0,2). Les quatre H ont charge2 et les quatre X,
uniques triangles des quatre arêtes de H, ont charge1. Si une grille
contient H, elle contient nécessairement aussi les quatre X et un
neuvième sommet v. La somme des charges y vaut12+q_v.

* Si v n'est pas dans C, t=0 et(39) exige q_v=3, absent du profil(0,2).
* Si v appartient à C, t=1 et(39) exige8, alors que la somme vaut12.

CONCLUSION : le C4 distingué H ne peut appartenir à AUCUNE grille3x3
induite. C'est une exclusion uniforme d'une extension de H, pas
l'exclusion de toute la famille(0,2).

Réinjection exacte. Noter X=(x0,x1,x2,x3) dans l'ordre cyclique des arêtes
de H. Si les deux arêtes opposées x0x2 et x1x3 sont présentes, un sommet
v adjacent aux quatre X compléterait cette grille. Il ne peut toucher H
car les arêtes H-X ont déjà leur unique voisin commun dans H. Les autres
arêtes entre X sont absentes car chacun a degré1 dans L. Donc, pour tous
les91 sommets v hors H union X,

    A_x0x2 + A_x1x3 + sum_(x dans X) A_vx <= 5.            (40)

Ces91 inégalités sont disponibles dans `coclique_column_coexistence.py`
avec --rook-cut. Elles valent sur les bords variables et ne fixent pas
les deux arêtes : avec au plus une d'entre elles, l'inégalité est triviale.
Les pilotes déjà lancés avant cette déduction ne les contiennent pas.

## 41. Extraction automatique de parités et références de comparaison

Le solveur affine construit les polynômes des défauts sélectionnés en
réduisant x_i²=x_i. Après élimination des dénominateurs et du facteur
commun entier, si tous les coefficients quadratiques sont pairs, il
extrait l'équation XOR linéaire nécessaire. Ces contraintes s'ajoutent
aux équations exactes ; elles ne les remplacent pas sans preuve de
suffisance. L'exemple Petersen extrait trois fois la même parité, qui
est dédupliquée. L'extraction facultative est bornée à delta<=24 ; le
système exact demeure appliqué au-delà. Un dépassement des coefficients
entiers supportés par CP-SAT est signalé explicitement, jamais UNSAT.

Consultation bibliographique ciblée du13 octobre, sans importer de
prétendue clôture :

* Petro et Phillips, On Clique Graphs and Clique Regular Graphs,
  https://arxiv.org/html/2502.17845v1 : référence pour le graphe des
  triangles et ses contraintes spectrales. Pas de conséquence nouvelle
  utilisée ici sans preuve.
* Keramatipour, Approaching the Conway-99 problem using SAT solvers,
  https://arxiv.org/html/2604.23037v2 : distingue l'interdiction d'un
  motif Paley9 universel de la conjecture d'absence de tout Paley9.
  Notre§40 n'utilise PAS cette conjecture ; son interdiction limitée à
  la grille contenant H est démontrée par le comptage(39).

La recherche porte encore sur l'existence d'un D admissible pour C1.
Le théorème affine, la loi(39), les coupes(40) et la décomposition(38)
complètent le critère global ; aucune impossibilité totale n'est annoncée.

## 42. Renforcement par la grille moins une arête, et propagation du centre

Lou et Murin, théorème2.1, prouvent qu'une grille3x3 privée d'UNE ARÊTE
ne peut être un sous-graphe induit de Conway99 :
https://math.mit.edu/research/highschool/primes/materials/2014/Lou-Murin.pdf
La preuve porte sur neuf sommets, pas huit ; on ne suppose aucune
complétion automatique d'une grille privée d'un sommet.

Avec le§40, cela renforce(40) en DEUX contraintes pour chaque v :

    A_x0x2 + sum_(x dans X) A_vx <= 4,
    A_x1x3 + sum_(x dans X) A_vx <= 4.                    (41)

Si une seule arête opposée était présente et v touchait les quatre X,
les neuf sommets formeraient exactement la grille moins l'autre arête.
Il n'y a pas d'arête supplémentaire cachée : les arêtes H-X saturées
interdisent v-H et les arêtes entre deux X consécutifs. Si les deux
opposées sont présentes, le§40 s'applique. Le mode --rook-cut impose
donc maintenant182 inégalités(41), qui impliquent les91 anciennes(40).
La nécessité de cette version renforcée cite expressément Lou-Murin.

Le contrôle `check_coclique_rook_balance.py` construit la grille dans
ses coordonnées naturelles, vérifie les identités et les sept profils,
les comptes impossibles du centre, et la conséquence C6 pour t=3.
Il ne prétend pas réauditer le théorème extérieur Lou-Murin. Son
certificat est `affine_completion_v7/rook_balance_certificate.json`.

La seule branche où un sommet v touche les quatre X a ainsi une structure
supplémentaire forcée :

1. v ne touche aucun H ; les quotas des étoiles excluent aussi Z_H.
   Un Y ne peut toucher les quatre X car son degré dans L est3. Donc
   v est dans C sans voisin H, ou dans Z0, et sa charge vaut0.
2. La loi Aq=3q+2 impose alors |N(v) intersect L|-|N(v) intersect{e,f}|=2.
   Comme les quatre X sont déjà présents, v touche exactement eux dans L
   et touche e et f. C'est donc l'UNIQUE voisin commun de e et f.
3. Les deux arêtes opposées de X sont absentes par(41). Dans le voisinage
   de v, l'arête ef forme déjà une paire. Chaque x_i doit former une
   autre paire avec un sommet w_i ; les quatre w_i sont distincts.
4. Chaque w_i touche exactement un X (x_i), ne touche ni e ni f, et
   appartient comme v à C sans voisin H ou à Z0. La loi des charges
   impose donc exactement UN voisin supplémentaire dans Y.

Ces quatre mates ne sont pas encore contradictoires ; ils constituent
une obligation commune précise pour la branche restante. L'absence de
contradiction à ce stade n'annule pas les exclusions(39)–(41).

Pilote dédié `global_center_v7`,600s,quatre travailleurs, avec
--triangles --no-max-lp --rook-cut --center-kind any. Il couvre TOUS
les centres possibles (13 dans C sans voisin H,36 dans Z0), sans en
fixer arbitrairement un malgré les ordres de signatures. La somme des
49 indicatrices de centre vaut1. Les équations de ses quatre mates
sont imposées conditionnellement ; aucune classe de cycles n'est fixée.
Ce pilote porte seulement sur la branche « un voisin commun aux quatre X ».
Il ne faut jamais attribuer son verdict éventuel à tout(0,2).

Si ce centre v est dans Z0, quatre de ses voisins sont dans C, quatre
dans X, deux sont e,f, et les quatre autres sont dans Z0 : les étoiles
de H saturées excluent tous les autres emplacements. Si p des quatre
mates w_i sont dans C, les quatre derniers voisins de v comprennent
4-p sommets de C et p sommets de Z0 et doivent former deux arêtes.
L'indépendance de C impose4-p<=p, donc p>=2. Si v est dans C, les
quatre w_i sont tous dans Z0. Ces conséquences sont démontrées ici ;
la borne p>=2 n'était pas ajoutée séparément au pilote déjà lancé.

## 43. La loi de défauts vaut pour tous les ensembles réguliers concernés

L'argument des grilles est un cas de la règle suivante. Si un ensemble
de sommets R vérifie A1_R=3*1_R+b*1, alors |R|=9b par sommation.
Pour toute coclique C de taille c, sans hypothèse c21/22, et
q=4*1-(A+4I)1_C, on a

    sum_(v dans R) q_v = b(36-c)-7|R intersect C|.         (42)

Preuve : (A+4I)1_R=7*1_R+b*1, puis prendre le produit avec1_C.
En notant delta=22-c, cela donne aussi

    sum_R q = b(14+delta)-7|R intersect C|,
    sum_R q = b*delta modulo7.

Une grille3x3 a b=1. Une union de b grilles disjointes a aussi ce
paramètre. À22, q=0 force exactement2b sommets de la coclique dans R ;
à21, les charges restantes imposent(39) et ses exclusions. L'existence
d'un tel R n'est PAS supposée pour tout Conway : la règle s'applique
chaque fois que cette structure est présente ou forcée.

## 44. Bilan des pilotes et poursuite intégrée

Les trois premiers pilotes V7 sont terminés, tous UNKNOWN :

| Modèle | Portée | Secondes | Pic mémoire observé |
| --- | --- | ---: | ---: |
| global_columns_v7 | Tout(0,2), colonnes et degrés partagés |901,503|4,35Gio|
| global_triangles_v7 | Tout(0,2), triangles résiduels ajoutés |1801,568|4,92Gio|
| global_center_v7 | Branche avec centre4X,49 positions possibles |601,439|2,94Gio|

Aucun n'a produit de D, et aucun n'exclut sa portée. Les mesures ont été
prises toutes les10s. Les statistiques par travailleur sont conservées :
sur le pilote triangulaire, fs_random_no_lp984221 conflits, no_lp883786,
quick_restart_no_lp213836. Les9511 conflits de la réponse finale ne sont
pas le total du portefeuille. Malgré l'exclusion de max_lp, CP-SAT avait
introduit probing_max_lp ; le nouveau réglage exclut explicitement les
deux, tout en conservant des moteurs à relaxation linéaire plus limitée.

Le pilote `global_integrated_v7` couvre à nouveau TOUT(0,2), avec toutes
les obligations nouvelles : triangles,182 inégalités de grilles, et
propagation CONDITIONNELLE des49 centres possibles. La somme des
indicatrices de centre est au plus1, PAS égale à1 ; aucun centre n'est
supposé. S'il existe, les mates, les quotas des voisins et la borne
p>=2 sont propagés. Le mode --center-kind conditional conserve donc la
famille entière. Budget3600s,huit travailleurs, observateur intégré.
Lire son result.json pour le résultat final ; le lancement ne vaut pas
verdict. Les sources exactes sont conservées dans chaque dossier.

Le manifeste `v7_run_manifest.json`, produit par `coclique_v7_snapshot.py`,
releve les portées, résultats, ressources et empreintes. Les preuves sont
aux§36–43. Les182 contraintes sont des instances de deux lois uniformes,
pas182 familles disjointes exclues. Les anciennes304 conditions V5 et
les anciens certificats sont conservés. Aucun classement des rangs
n'a été repris. C1 et la famille(0,2) restent ouverts.

## 45. V8 : un corps convexe dont les points entiers sont exactement les graphes

13 octobre2026. Recherche secondaire demandée pendant le calcul intégré V7.
Le rapprochement utile est avec le **fantope**, employé notamment pour
l'estimation de sous-espaces en statistique : l'enveloppe convexe des
projecteurs de rang fixé s'écrit 0<=Q<=I, trace Q fixée. Source primaire :
[Vu, Cho, Lei et Rohe, NeurIPS2013, section2](https://proceedings.neurips.cc/paper/2013/file/81e5f81db77c596492e6f1a5a792ed53-Paper.pdf).
Les inégalités de ce paragraphe sont dans l'ordre des matrices symétriques,
pas entrée par entrée. L'application à notre système est démontrée ici.

Conserver les hypothèses EXACTES du§32 : B et D binaires, B symétrique
à diagonale nulle, DD^t=12I+2J-B-B², les degrés, et une étoile complète
dans B. E0 et P sont ceux du§32. Définir le corps de complétion

    K(B,D) = { E=E^t : DE=F,
               E0+3P-E >= 0,   E-E0+4P >= 0 }.             (43)

Il est convexe et borné. Aucun nom de nouvelle théorie ni priorité
historique n'est revendiqué : c'est un objet de travail adapté au bord.

THÉORÈME. Les points ENTIERS de K(B,D) sont exactement les blocs E des
complétions SRG(99,14,1,2). Il n'est pas nécessaire de supposer à l'avance
leur diagonale nulle ou leurs entrées dans{0,1}.

Preuve. Une solution symétrique DE=F a E=E0+H avec H=PHP. Les deux
inégalités équivalent à -4P<=H<=3P. En posant

    Q=(3P-H)/7,

elles équivalent à 0<=Q<=P. En particulier PQ=Q. Le défaut du polynôme
complet A²+A-12I-2J est nul hors du bloc

    L = H²+H-12P = 49(Q²-Q) <= 0.                         (44)

La régularité A1=14*1 résulte déjà de la fermeture linéaire et de
l'étoile complète (§33), même avant d'imposer une diagonale nulle à E.
Pour chaque sommet, elle donne l'identité exacte

    (A²+A-12I-2J)_ii
       = A_ii² + sum_(j!=i) A_ij(A_ij-1).                 (45)

Si E est entière, tous les termes de droite sont des entiers positifs
ou nuls. La semi-définie négativité de(44) impose donc une diagonale
entièrement nulle. Une matrice semi-définie négative de trace nulle est
nulle. Ainsi L=0 et chaque terme de(45) vaut0 : diagonale A nulle,
coefficients hors diagonale0/1. Le graphe satisfait toutes les équations.
Réciproquement une vraie complétion fournit le projecteur Q du§32,
donc appartient à K(B,D).

Cette preuve remplace la contrainte non convexe Q²=Q par deux inégalités
convexes **en conservant l'intégralité**. Elle ne rend pas le problème
entier convexe, ne fournit pas D, et ne prouve pas K(B,D) vide pour C1.
Pour A²+A=(k-mu)I+mu J, la même preuve vaut avec les deux racines
r>s de t²+t-(k-mu), et les bornes sP<=H<=rP.

## 46. Identité de fractionnalité et version sur tout le graphe

Si E appartient à K(B,D), a diagonale nulle et des coefficients dans[0,1],
prendre la trace dans(44) donne

    sum_(u,v) E_uv(1-E_uv) = 49 trace(Q-Q²).                (46)

Le membre gauche compte les deux orientations de chaque arête. Les
deux membres sont positifs ou nuls ; ils s'annulent simultanément.
On obtient une identité quantitative entre le défaut de binarité des
arêtes et le défaut d'idempotence du projecteur. Avec trace E=0,
trace Q=(trace E0+3 dim ker D)/7 est fixée : la section de(43) est
une section affine d'un fantope sur ker D, si cette trace est admissible.
La constante49 devient(r-s)² pour les paramètres généraux.

Le même argument existe SANS bord fixé, SANS D et SANS coclique.
Pour une matrice entière symétrique A d'ordre99 telle que A1=14*1,
les deux conditions

    G_-(A)=A+4I-(2/11)J >= 0,
    G_+(A)=3I-A+(1/9)J >= 0                               (47)

sont équivalentes à A étant l'adjacence d'un SRG(99,14,1,2).
Preuve : elles annulent1 et enferment le spectre sur1-perp dans[-4,3].
Le défaut A²+A-12I-2J est alors semi-défini négatif, puis(45) l'annule.
Le sens réciproque découle directement des trois valeurs propres.

Pour tout vecteur entier z, (47) fournit des contraintes linéaires sur
les arêtes, valables uniformément pour TOUS les éventuels Conway :

    9 z^t A z <= 27 ||z||² + (sum z)²,
    11 z^t A z >= 2(sum z)² - 44 ||z||².                  (48)

Les supports de z peuvent être quelconques et ses signes mélangés.
Ce n'est pas une nouvelle classification des rangs. Une direction
négative trouvée dans un candidat fournit une coupe qui peut être
réutilisée même lorsque B et D changent. Vérifier seulement quelques
directions ne suffit pas ; vérifier les DEUX matrices complètes suffit.

## 47. Séparation exacte, arrondi entier et coexistence à trois coordonnées

`coclique_spectral_completion.py` implémente une seconde méthode exacte
pour un B,D fixé. Elle conserve l'espace affine V7 et impose la binarité
de toutes les entrées E. Le solveur propose un point ; on examine les
deux matrices de(43), comprimées sur une base rationnelle N de ker D.
Si elles sont positives, le théorème45 certifie la complétion ; sinon
un vecteur rationnel z prouve une forme quadratique strictement négative.

Ce vecteur donne une inégalité c+sum a_i x_i>=0, linéaire dans les
arêtes libres. Après suppression des dénominateurs, si g est le pgcd
des a_i, on peut renforcer l'inégalité en

    sum (a_i/g)x_i >= ceil(-c/g).                          (49)

Elle est valable pour TOUTE complétion du bord et rejette le candidat.
Le procédé termine en un nombre fini d'étapes sur l'ensemble binaire
si aucun budget n'est imposé ; aucune borne pratique favorable n'est
affirmée. Les délais et dépassements du domaine numérique implémenté
restent explicitement non concluants. Le prototype traite les racines
r,s rationnelles et refuse explicitement les autres paramètres.

Les témoins négatifs sont obtenus par élimination de Schur rationnelle,
avec traitement des pivots nuls. Une valeur propre flottante n'est
jamais utilisée comme certificat. Le module `global_separate` effectue
aussi la séparation de(47) sur le graphe complet, sans bord fixé.

Sur les HUIT points binaires linéaires de Petersen, cette méthode
retrouve les quatre complétions en ajoutant exactement quatre coupes :

    x<=y+z,    y<=x+z,    z<=x+y,    x+y+z<=2.              (50)

Exemple : le témoin du point100 donne d'abord
2-8x+8y+8z>=0 ; l'intégralité renforce cette coupe en x<=y+z.
Ces quatre inégalités équivalent à la parité paire sur{0,1}³.
Le solveur de ce contrôle ne contient AUCUN produit quadratique.

Plus précisément, avec le N sauvegardé dans le contrôle V7,

    N^t Q N = (2/3) [[1,1-2x,1-2y],
                     [1-2x,1,1-2z],
                     [1-2y,1-2z,1]].                     (51)

Tous les mineurs principaux d'ordre1 ou2 sont positifs ou nuls pour
les huit choix. Le déterminant est0 pour les quatre choix compatibles,
et -32/27 pour les quatre autres. La compatibilité de chaque paire ne
garantit donc pas celle des trois coordonnées. C'est un contrôle
explicite du mécanisme global, PAS une exclusion de C1.

Contre-exemple à une relaxation excessive : x=y=z=1/2 donne Q=P/3.
Les deux bornes convexes sont satisfaites, mais Q²!=Q et E est
fractionnaire. Une solution du seul système réel ne décide donc rien.

Nouveaux contrôles exacts, dans `spectral_completion_v8/` :

| Bord de contrôle | Libertés affines | Complétions | Coupes produites |
| --- | ---: | ---: | ---: |
| Grille3x3 |0|1|0|
| Petersen |3|4|4|
| Paley25 |2|1|0|
| Paley49 |5|1|0|

Dans les deux derniers cas, les contraintes de binarité de TOUT E
laissent déjà une seule complétion. Leur inclusion teste la nouvelle
procédure sur d'autres dimensions ; elle n'est pas présentée comme
une nouvelle classification. Le contrôle séparé relit les témoins,
les arrondis, les graphes complets, et les huit cas géométriques.

## 48. Extraire les parités de combinaisons d'équations

Le second rapprochement retenu concerne les systèmes booléens issus
notamment de la cryptographie. La réduction x_i²=x_i permet d'écrire
les équations comme des lignes de coefficients ; des combinaisons
éliminent les monômes de degré2. Ce principe d'algèbre linéaire est
documenté dans [Bardet, Faugère, Salvy et Spaenlehauer,
section2.1](https://arxiv.org/pdf/1112.6263).
Les fonctions booléennes et leur lien aux codes sont présentés par
[Carlet, sections2–3](https://www.math.univ-paris13.fr/~carlet/chap-fcts-Bool-corr.pdf).
Nous utilisons ici seulement des combinaisons constantes de lignes,
pas tout l'algorithme de ces références ni ses bornes de complexité.

Pour une présentation ENTIÈRE enregistrée f_j(x)=0, après réduction
booléenne et passage modulo2, définir l'espace de parités

    L(f) = span_F2{f_j} intersect {polynômes de degré<=1}.  (52)

Le code affine C(f) est l'ensemble des x annulant toutes les formes
de L(f). Toute vraie complétion y appartient. Une forme constante1
dans L(f) est un certificat d'impossibilité. L'élimination des colonnes
quadratiques, puis linéaires, calcule une base de L(f). Chaque ligne
porte la liste des équations initiales dont elle est le XOR.

`coclique_modular_coexistence.py` réalise cette extraction et le
rejeu exact des preuves. Elle contient celle de V7, qui ne conservait
que les équations dont la partie quadratique était déjà paire :
des parties quadratiques NON nulles peuvent maintenant s'annuler
entre plusieurs équations. L'espace(52) dépend de la présentation
entière enregistrée ; il n'est pas déclaré invariant sous toutes
les transformations rationnelles de générateurs.

Contrôle non artificiellement ajouté au problème de graphe : remplacer
les trois résidus Petersen f1,f2,f3 du§37 par le système équivalent
sur les rationnels g1=(f1+f2)/2, g2=(f1+f3)/2, g3=(f2+f3)/2. Alors

    g1=z(x+y-1),  g2=y(x+z-1),  g3=x(y+z-1).

Aucune de ces trois lignes ne fournit individuellement un XOR par
l'ancien critère. Leur SOMME modulo2 donne x+y+z=0. Le nouvel
extracteur retrouve ce certificat, vérifié sur les huit affectations.
Dans ce contrôle seulement, le code est aussi suffisant.

Limite prouvée : pour l'unique équation xy=0, L(f)={0} et le code
accepte aussi11, qui viole l'équation. En général ce code ne remplace
ni la binarité affine ni les équations de complétion restantes.

## 49. Portée pratique de cette recherche secondaire

Deux transferts ont produit des résultats précis : une section de
fantope dont les points entiers sont exactement les complétions, et
un espace calculable de parités prouvées par combinaisons d'équations.
Ce sont des adaptations démontrées d'outils existants ; aucune
revendication de nouveauté bibliographique générale n'est faite.

Le premier fournit un autre moteur de fermeture et des coupes valables
sur tout C1 via(48). Le second renforce l'extraction algébrique V7.
Les nouveaux contrôles passent, avec certificats rationnels et un
contre-exemple explicite à la suppression de l'intégralité.

Ces outils n'ont pas encore produit un D de C1 ni une exclusion
supplémentaire de(0,2). Le programme V7 déjà en cours n'a pas été
modifié ou arrêté pour cette exploration. À13h20UTC le13 octobre,
son observateur enregistrait encore huit cœurs environ, sans résultat
final. Lire son `result.json` et le manifeste daté pour l'état suivant.
Le temps passé et les exemples de contrôle ne constituent pas un
pourcentage de résolution de C1.

## 50. Fin du run intégré : ce que le calcul apprend réellement

13 octobre2026, vers15h44 heure de Paris : `global_integrated_v7`
termine UNKNOWN après3602,089498s, sans D et sans nouvelle exclusion.
Le processus23356 est terminé. Les quatre pilotes V7 sont maintenant
tous terminés UNKNOWN ; aucune continuation identique n'a été lancée.

À la question de l'utilisateur sur CaDiCaL : aucun CaDiCaL parallèle
n'a été lancé pour ce modèle. CP-SAT a lui-même appris et partagé des
clauses ENTRE ses travailleurs. Le programme ne sauvegarde pas leur
base interne et ne la réimporte pas au prochain run. Les journaux
conservent les compteurs, pas les clauses elles-mêmes. Un CaDiCaL
indépendant ne partagerait pas automatiquement son apprentissage
avec CP-SAT ; il faudrait un encodage et un échange explicitement conçus.

`coclique_solver_diagnostics.py` produit `v7_solver_diagnostics.json` :
portefeuille réellement choisi, compteurs par moteur, échanges de
clauses, dimensions LP, ressources et évolution du modèle toutes les
cinq minutes. Ce rapport est un diagnostic empirique, pas un certificat.

Résultats du run intégré :

* Somme des conflits rapportés par les moteurs :5698129. Les20378 de
  la réponse principale ne sont PAS ce total. Une même difficulté peut
  être rencontrée par plusieurs moteurs : pas5698129 cas disjoints exclus.
* fs_random_no_lp :2822978 conflits ; no_lp :2206321 ;
  quick_restart_no_lp :633009. Activité ne signifie pas efficacité
  comparative démontrée.
* Les compteurs d'exports de clauses totalisent306369 ; ces exports
  ne sont pas déclarés tous distincts. Ils sont internes à CE run.
* Dernière réduction du modèle enregistrée à3516,17s :213640 variables
  restantes sur216633 après présolve. Ce sont aussi des auxiliaires,
  pas une mesure du pourcentage de graphes exclus.
* Pic mémoire5680218112 octets ; activité CPU proche de huit cœurs.

Constat de réglage : exclure max_lp et probing_max_lp n'a pas éliminé
tous les moteurs de grande relaxation. Le portefeuille a introduit
**max_lp_sym**, avec623129 lignes et210770 colonnes LP. Il rapporte
zéro résolution LP de statut OPTIMAL,434 conflits,1959 exports de
clauses et25 améliorations de bornes partagées. Il a donc contribué,
mais ce comportement justifie de comparer un portefeuille fixé
explicitement. Il ne prouve pas à lui seul qu'enlever ce moteur accélère
l'ensemble. Les autres moteurs LP ont effectivement produit des coupes.

Pour une comparaison CP-SAT/CaDiCaL, il manque encore une traduction
CNF/PB contrôlée, les correspondances de variables et un protocole à
budget comparable. Aucun résultat de cette comparaison n'est inventé.
Pour capitaliser entre runs, conserver des lemmes/coupes certifiées ou
un état réutilisable explicite ; les seuls compteurs ne font pas cela.
La clôture exacte V7 et les nouveaux outils V8 restent disponibles.

## 51. Budgets de coexistence des colonnes : moments résiduels

13 octobre2026. À la demande de calibration courte, on distingue les
changements de moteur des renforcements mathématiques. Un renforcement
peu coûteux s'obtient en sommant les équations encore manquantes.

**Lemme.** Soit A=[[B,D],[D^t,E]] l'adjacence d'un graphe fortement
régulier avec lambda=mu-1. Posons m=|M|, r=E1 et R=D^t D. Pour tout
u dans M,

    sum_{v dans M, v!=u} R_uv + sum_{w dans M} E_uw r_w = mu(m-1).  (51)

Preuve : pour v!=u, R_uv+(E²)_uv+E_uv=mu. En sommant sur v!=u,
le terme E² donne (Er)_u-r_u, car (E²)_uu=r_u. La somme des E_uv
redonne r_u et ces deux termes s'annulent. Dans notre bord61/38,
le second membre vaut74. Tous les calculs sont entiers.

Il s'agit d'une obligation commune sur le MÊME E et ses degrés,
pas du choix indépendant d'un voisinage pour chaque colonne. Le terme
E_uw r_w se code par une variable entière y, avec y=r_w si E_uw=1
et y=0 sinon. On ajoute38 variables de degrés,1406 produits orientés
et38 budgets, sans développer tous les produits d'arêtes nécessaires
aux équations mixtes individuelles. Les bornes finales utilisées sont
1<=r_e,r_f<=6 et2<=r_z<=8 ; leur justification suit.

Précision sur la portée : avec R_total=A²+A-(k-mu)I-mu J et A régulier,
R_total*1=0. Si le bloc B-B est nul, (51) équivaut à la nullité des
SOMMES DE COLONNES du défaut mixte B-M. Elle ne force pas toutes ses
entrées à être nulles. Si toutes les équations mixtes sont déjà imposées,
ces budgets sont redondants. Leur gain sur V7 doit être mesuré ; aucune
preuve qu'ils renforcent strictement toute sa conjonction n'est supposée.

Leur SOMME est déjà nulle : le défaut total a des sommes de lignes
nulles ; son bloc B-B nul impose des sommes de lignes mixtes nulles,
et donc une somme totale nulle dans M-M. Les38 budgets ne sont ainsi
pas annoncés indépendants. Ils imposent la bonne répartition colonne
par colonne d'un total déjà correct. Le contrôle suivant conserve ce
total tout en donnant des budgets individuels non nuls.

Contrôle neuf de l'encodage, `check_coclique_residual_moments.py` :
on réutilise un graphe Paley25 sauvegardé et déplace deux sommets dans
le bord. Le bloc résiduel correct passe. Un échange de deux arêtes,
qui garde B, D et TOUS les degrés résiduels inchangés, donne le défaut
de moments (2,1,-1,-2,0,0,0,0,0,0) et est rejeté. Le certificat exact
figure dans `calibration_v9/moment_control.json`. Ce test distingue
la nouvelle obligation des seuls degrés ; ce n'est pas un témoin
satisfaisant toutes les autres contraintes V7 ni une exclusion C1.

**Quotas déduits des quatre étoiles complètes.** Notons C8 les huit
sommets de C adjacents à H, C13 les treize autres. Pour v hors H,
la somme des nombres de voisins communs de v avec les quatre h de H
donne

    d_C8(v)+2d_H(v)+2d_X(v)+d_Y(v)+d_ZH(v)=8-d_H(v).

En effet chaque h a deux voisins dans H, chaque X touche deux h,
chaque Y, C8 ou ZH touche un h, les autres sommets aucun. Cette égalité
est une combinaison d'équations DÉJÀ présentes, donc pas une exclusion
supplémentaire. Elle rend explicites des contraintes utiles au codage :

* pour x dans X : d_ZH(x)=1-d_X(x)-d_C8(x), donc d_Z0(x)>=7 ;
* pour y dans Y : d_ZH(y)=2-d_X(y)-d_C8(y), donc d_Z0(y)>=5 ;
* pour e ou f : d_ZH(e)=8-d_C8(e) et d_Z0(e)=d_C8(e),
  donc r_e=1+d_C8(e), avec1<=r_e<=6 ;
* pour z dans Z0 : d_ZH(z)=6-d_{e,f}(z)-d_X(z)-d_C8(z),
  donc r_z=2+d_X(z)+d_C8(z)>=2. Les quatre voisins de C et
  au moins deux voisins de L donnent aussi r_z<=8.

Ces identités expliquent pourquoi des choix qui conservent les degrés
peuvent encore modifier les budgets de voisins communs. L'encodage
des moments utilise les intervalles de r resserrés ci-dessus ; les
autres égalités restent ici des conséquences explicitées, pas des
équations ajoutées dans les comparaisons de moteurs.

## 52. Calibration V9 terminée : six essais de trois minutes

13 octobre2026, vers16h27 Paris. Campagne autorisée par l'utilisateur,
terminée sans D. Six recherches de180s, huit travailleurs chacune,
dans des processus successifs ; un septième contrôle s'arrête après
le présolve. Tous les verdicts sont UNKNOWN. Les secondes légèrement
supérieures à180 incluent la terminaison du solveur. Aucune recherche
longue supplémentaire n'est lancée automatiquement.

| Portefeuille / modèle | Graine | Présolve (s) | Pic observé (Gio) | Conflits sommés | Domaines d'arêtes réduits |
|---|---:|---:|---:|---:|---:|
| ancien V7 |1|36,48|4,912|278079|288|
| sans tous les max_lp |1|37,22|4,339|259327|288|
| sans LP |1|24,28|3,940|552959|288|
| ancien V7 |2|37,49|4,902|259726|290|
| sans LP |2|37,34|3,892|524147|290|
| sans LP + moments§51 |1|38,55|3,941|758547|290|

Le contrôle de présolve seul prend35,37s et réduit272 domaines d'arêtes.
Les trois runs de graine1 sur V7 ont EXACTEMENT les mêmes16 réductions
supplémentaires en sortie, pas seulement le même nombre. Les deux runs
de graine2 ont aussi les mêmes domaines entre eux. La variante moments
retrouve exactement les290 domaines de l'ancien modèle avec graine2.
Ses deux réductions supplémentaires par rapport à la graine1 V7 ne
sont donc pas présentées comme une nouvelle avancée de famille.

**Conclusion empirique mesurée.** Le portefeuille sans LP économise
environ20% de mémoire dans les deux comparaisons à graine égale. Son
gain initial de présolve ne se répète pas avec la seconde graine.
Les conflits augmentent, mais les domaines d'arêtes sont identiques
à graine égale : ni accélération du temps jusqu'à preuve, ni progression
mathématique supplémentaire démontrée. Le portefeuille intermédiaire
garde les petits moteurs LP et enlève max_lp_sym ; il économise environ
12% de mémoire sur l'unique graine essayée. Il reste une alternative
pour des recherches complémentaires, sans classement de puissance établi.

La variante moments ajoute1444 variables et2888 contraintes à246829
variables/766370 contraintes. Son pic mémoire reste voisin de3,94Gio.
Elle a donc un coût de stockage faible dans ce test ; l'amélioration du
temps jusqu'à solution reste inconnue. Les budgets sont démontrés,
mais ne suffisent pas à clore(0,2), a fortiori C1.

**Traçabilité et limites.** Les cinq comparaisons de moteur utilisent
le même export binaire SHA256
`5a29aa8518171c4eb2cb5f3fbe7e869f377a705436c5e640581dcde00bf801cc`.
L'export renforcé a le SHA256
`973c76b6d0c630573f5c685286a05f68d7a6201ac8a7e935804d778e49247516`.
Une lecture indépendante des protobufs vérifie que le préfixe des
variables et contraintes est strictement identique et que seuls les
ajouts annoncés apparaissent. Les snapshots de sources sont vérifiés
par leurs hashes, `artifact_check.json`. Contrôle d'encodage§51 PASS.

L'instrumentation conserve les ressources toutes les10s, les événements
de réduction, un résumé toutes les30s et les statistiques finales par
travailleur. Elle n'accède pas à une base persistante de clauses. Les
domaines resserrés sont DIAGNOSTIQUES : le présolve peut choisir des
représentants, puisque keep_all_feasible_solutions_in_presolve=false.
Ne pas combiner ces listes entre runs ni les promouvoir en propriétés
universelles de graphes. La documentation primaire précise ce point :
https://raw.githubusercontent.com/google/or-tools/v9.15/ortools/sat/cp_model.proto
(champ tightened_variables). Les portefeuilles sont définis dans
https://raw.githubusercontent.com/google/or-tools/v9.15/ortools/sat/cp_model_search.cc
et les paramètres sauvegardés dans chaque parameters.textproto.

Choix provisoire : portefeuille sans LP pour les prochains essais courts
à mémoire réduite ; conserver le portefeuille intermédiaire pour des
comparaisons avec LP. Tester les renforcements mathématiques à part.
Il n'existe ici aucune preuve de configuration optimale. On capitalise
sur les modèles, les preuves et le protocole, pas sur une reprise fictive
de l'apprentissage interne du run d'une heure. Détails et commandes :
`calibration_v9/protocol.json`, `report.json`, `recommendation.json`.

## 53. V10 : conservation et fermeture du bloc résiduel

13 octobre2026. Nouvelle étape demandée par l'utilisateur : utiliser les
réductions mathématiques pour structurer une recherche parallèle, sans
confondre puissance de calcul et preuve. Le système était déjà fini ;
l'objectif est de le rendre effectivement traitable.

**Lemme de fermeture par les plafonds.** Soit A une matrice d'adjacence
binaire symétrique, de diagonale nulle, k-régulière, sur n sommets. Supposons
k²+k=(k-mu)+mu*n. Posons T=A²+A-(k-mu)I-mu*J. Si le bloc T_BB est nul et
si T_uv<=0 pour toutes les paires distinctes u,v dans M, alors T_MM=0.

Preuve. T*1=0 par la relation sur les paramètres, et diag(T)=0 par les
degrés. Écrire T=[[0,G],[G^t,L]]. Les lignes du bord donnent G*1=0.
La somme des lignes de M donne 1^t*L*1=-1^t*G^t*1=0. Les termes de L
sont tous négatifs ou nuls et leur somme est nulle : chacun vaut zéro.
Il s'agit d'une contrainte de coexistence de TOUS les plafonds, pas d'une
vérification indépendante de chaque colonne. Les équations mixtes G=0
ne sont pas déduites de ce seul argument.

Application Conway : k=14,mu=2. Pour u!=v dans M, les plafonds sont

    (D^t*D)_uv + (E²)_uv + E_uv <= 2.

V10 impose directement les703 égalités correspondantes. Les anciennes
contraintes de saturation et de triangles ne contrôlaient pas tous les
nombres de voisins communs des paires NON adjacentes du bloc M. L'ajout
emploie25308 produits binaires, mutualisés entre ces équations. Les38
moments de§51 deviennent des conséquences des égalités individuelles et
ne sont donc pas ajoutés une deuxième fois dans cette variante.

Contrôle neuf : le Paley25 repartitionné de§51 satisfait aussi bien
l'encodage par plafonds que celui par égalités. Son échange d'arêtes à
degrés conservés, avec B,D inchangés, conserve la somme totale nulle du
défaut résiduel mais donne des entrées -1 et+1 : les deux encodages le
rejettent. Ce contrôle ne prétend pas exhiber un modèle V7 de C1.
Code : `coclique_residual_partition.py`, contrôle
`check_coclique_residual_partition.py` ; sortie
`partition_v10/mathematical_checks.json`.

## 54. V10 : partition exhaustive en61 branches intrinsèques

Notons e,f les deux sommets de charge négative, qui sont adjacents, et
r_e,r_f leurs degrés dans M={e,f}+Z0. Par§51,

    r_e=1+d_C8(e), r_f=1+d_C8(f), 1<=r_e,r_f<=6.

Leurs voisinages dans C ont chacun cinq sommets, donc
d_C13(e)=6-r_e et d_C13(f)=6-r_f. Ils ont un UNIQUE voisin commun t.
Les ensembles H et L sont anticomplets à e,f ; ainsi t appartient
exactement à l'une des quatre classes C8,C13,ZH,Z0.

Posons (a,b)=(min(r_e,r_f),max(r_e,r_f)). Leurs voisinages dans C8
ont tailles a-1,b-1, dans un ensemble de taille8, et leur intersection
a taille au plus1. Par conséquent a+b<=11. Le couple(6,6) est exclu.
Les autres conséquences utilisées sont :

* t dans C8 ou Z0 exige a>=2 ;
* t dans C13 exige b<=5 ;
* a+b=11 force t dans C8, par le même comptage d'intersection.

Il reste20 couples non ordonnés et61 triplets (a,b,classe(t)). Ce sont
des cas nécessaires, pas61 familles dont on affirme la réalisabilité.
Tout graphe de la famille(0,2) se trouve dans EXACTEMENT une branche.
Dans une branche a<b, l'encodage conserve les DEUX affectations
(r_e,r_f)=(a,b) et(b,a) ; aucune nouvelle hypothèse de symétrie e/f
n'est introduite dans les signatures ordonnées existantes.

Un centre adjacent aux quatre X, s'il existe, est t d'après§41. Ainsi
les branches t dans C8 ou ZH excluent tous ces centres ; dans les deux
autres classes, seuls les centres de la bonne classe sont possibles.
Ces conséquences sont ajoutées explicitement à la propagation.

Le dénombrement61 est contrôlé indépendamment par les contraintes
d'intersection d'ensembles de tailles(a-1,b-1) dans C8 et(6-a,6-b) dans
C13, avec les deux orientations de e,f. Cela vérifie la couverture du
découpage, sans remplacer sa preuve ci-dessus ni affirmer l'existence
d'un graphe dans une branche. Le couple(6,6) était déjà incompatible
avec les équations exactes sur e,f : on explicite une réduction utile,
on ne la présente pas comme une nouvelle exclusion indépendante de V7.

`coclique_partition_campaign.py` affecte ces branches à des processus
distincts, de1/2/4/8 travailleurs CP-SAT. Les clauses sont partagées
seulement à l'intérieur d'un processus. Les UNKNOWN restent ouverts ;
les journaux, empreintes de modèles, paramètres et sources permettent
de reprendre la campagne et de comparer des réglages sans prétendre
recharger les clauses internes. Un candidat doit encore satisfaire les
équations mixtes restantes ou passer la complétion exacte de V7.

## 55. Propagation du défaut mixte et contrôlabilité

Toujours sous les hypothèses de§53, avec les DEUX blocs diagonaux du
défaut T nuls, écrire T=[[0,G],[G^t,0]]. Puisque A est régulier, il
commute avec J, donc avec T. Le bloc mixte de AT=TA donne

    B*G=G*E.                                                    (55a)

Les sommes de lignes donnent G*1=0 et G^t*1=0. Par récurrence,

    G*E^j*1=0 pour tout j>=0.                                  (55b)

**Critère de fermeture.** Si W_E=[1,E1,...,E^(m-1)1] est inversible,
alors G=0 : les deux blocs diagonaux et les degrés suffisent déjà à
certifier le graphe complet. Il n'est PAS supposé que tout E admissible
satisfasse cette hypothèse. L'asymétrie seule ne l'implique pas.

Version utilisant les équations déjà imposées : si G a ses lignes S
nulles, alors G^t annule chaque B^j*e_s, s dans S, et chaque B^j*1.
Si ces vecteurs engendrent tout l'espace du bord, G=0. Dans V10,
S=C+H est connu, soit25 lignes exactes. Sinon, G est confiné aux
compléments de ces espaces ; il n'est pas déclaré nul par défaut.
Une propagation combinatoire possible : une ligne déjà nulle, dont
le sommet a exactement un voisin encore inconnu dans B, force cette
dernière ligne à zéro via(55a). C'est la règle usuelle de zero forcing.

Ces outils de marches/contrôlabilité sont classiques. La contribution
ici est leur application au défaut mixte de notre système, après la
fermeture du bloc résiduel. Références primaires consultées :
Chris Godsil, *Controllable Subsets in Graphs*, arXiv:1010.3231,
https://arxiv.org/abs/1010.3231 ; Burgarth et al., *Zero forcing, linear
and quantum controllability for systems evolving on networks*,
https://arxiv.org/abs/1111.1475. Aucun résultat de ces articles n'est
présenté comme une preuve de nonexistence de Conway.

Autre conséquence exacte : G non nul implique que B et E partagent
une valeur propre, puisque(55a) est une équation de Sylvester. Les
espaces de marches permettent d'écarter de ce défaut tous les modes
qu'ils engendrent. Ce critère sert à la complétion et à l'analyse de
candidats ; on ne lance pas un nouveau catalogue de rangs de Seidel.

**Contrôle positif et limite indispensable.** Le prisme pentagonal
A=[[C5,I],[I,C5]], régulier de degré3, satisfait les deux blocs
diagonaux de A²+A=2I+J mais pas le bloc mixte : G=2C5+I-J est non nul.
Sa matrice W_E a dimension1. Remplacer le deuxième C5 par son
complément donne Petersen, et deux lignes mixtes exactes (0,1)
engendrent ici tout le bord par B. Sur une partition explicite du
Paley25 sauvegardé, M=[1,2,5,7,10,11,15,16,20,22], on obtient
det(W_E)=18761760, donc une fermeture complète par(55b).
Calculs exacts : `coclique_mixed_closure.py`,
`check_coclique_mixed_closure.py`, `partition_v10/mixed_closure_checks.json`.
Ces nouveaux contrôles vérifient la portée du critère, pas C1.

## 56. Colonnes feuilles : renforcement ciblé sans fixer un bord

Dans les11 branches de§54 avec a=1, au moins un des deux sommets
négatifs est une feuille de E. Si c'est e, son seul voisin résiduel
est f (l'arête ef est obligatoire). Toutes les équations mixtes de la
colonne e se simplifient en

    (B+I)*D_e + D_f = 2*1.                                    (56a)

Cela détermine D_f à partir de B,D_e. Si les DEUX degrés valent1,
en posant s=D_e+D_f et d=D_e-D_f, les deux colonnes se ramènent à

    (B+2I)*s=4*1,   B*d=0.                                    (56b)

Autres contraintes immédiates dans ce double cas : D_e^t D_f=1,
D_Z0^t*d=0 et D_Z0^t*s=4*1. Les deux premières colonnes ont chacune
poids13, donc ||d||²=24 et ||s||²=28. Toutes sont des conséquences
exactes du même graphe, sans choisir indépendamment les voisinages.

L'option `--leaf-columns` ajoute(56a) conditionnellement pour CHACUN
des deux sommets, en gardant les deux orientations du découpage.
Les25 lignes C+H étaient déjà exactes ; on ajoute72 égalités
conditionnelles pour les36 autres lignes, avec des produits binaires
mutualisés. Ce renforcement est mesuré séparément des deux portefeuilles
sur V10 identique. Il ne suppose pas l'existence d'une feuille hors
des branches correspondantes et ne prétend pas déjà les exclure.

Un contrôle de ce NOUVEL encodage utilise la grille3x3 et un bloc M de
trois sommets dont deux feuilles adjacentes. Le bon graphe passe ;
l'échange de deux incidences B-M, conservant tous les degrés, est rejeté.
La sortie figure dans `mixed_closure_checks.json`, champ leaf_encoder.

## 57. Choix constructif des labels autour du triangle négatif

On peut réduire les étiquetages sans supposer A symétrique au sens
des automorphismes. Voici une procédure applicable à TOUT graphe(0,2).

1. Appeler e le négatif de plus petit degré résiduel et f l'autre.
   En cas d'égalité, garder une orientation arbitraire.
2. Si leur unique voisin commun t est dans C8 ou ZH, il a un unique
   voisin dans H. Choisir celui-ci comme h0 en tournant les labels du C4.
   Tourner simultanément X, les quatre paires Y, les paires C8 et les
   quatre groupes ZH, de façon à conserver toutes les incidences fixes.
3. Réordonner indépendamment chaque paire C8, le groupe C13, chaque
   groupe ZH et Z0 selon les signatures déjà utilisées. Ces groupes
   ne contiennent AUCUN sommet ancre H+L+{e,f}, donc leurs tris ne se
   perturbent pas mutuellement. Pour Z0, garder H+L comme clé principale
   et ajouter les deux bits e,f comme clé secondaire seulement.

Dans C8,C13 et ZH, les deux bits e,f sont les PLUS SIGNIFICATIFS de la
signature. Un sommet adjacent aux deux dépasse donc tout sommet qui
ne l'est pas. Comme t est unique, après le tri il est le dernier de
son groupe. D'où les représentants possibles, sans perte de graphes :

    r_e<=r_f ; t=1 si t dans C8 ; t=20 si t dans C13 ;
    t=44 si t dans ZH.

Le cas C13 était déjà une conséquence du tri précédent. Les deux
autres utilisent aussi le choix de h0. Pour Z0, aucun label unique de
t n'est imposé : les ancres H+L gardent la priorité. La clé secondaire
4*signature_HL+A_ze+2*A_zf respecte STRICTEMENT le tri précédent.

Cela ne dit PAS qu'échanger e,f ou tourner H soit un automorphisme
du graphe. La procédure produit un autre étiquetage du même graphe,
puis rétablit les conventions du modèle. Les61 branches de§54 restent
une couverture de tous les graphes ; on garde maintenant au moins un
représentant par graphe, et non tous ses étiquetages précédemment permis.

L'option `--canonical` ajoute seulement42 contraintes et aucune variable
auxiliaire : une orientation des degrés, six implications sur t, et35
tris secondaires. `coclique_triangle_canonical.py` contient aussi la
permutation constructive new-label -> old-label. Quatre contrôles sur
le squelette fixe vérifient les permutations, toutes les incidences
fixes et les représentants t, avec validation du modèle. Ils ne sont
pas des exemples de graphes C1 et ne remplacent pas la preuve ci-dessus.
La comparaison de domaines après cette réduction concerne des
représentants DIFFÉRENTS : ne pas en tirer des propriétés universelles.

## 58. Bilan V10 :255 recherches courtes sur AWS, toutes UNKNOWN

13 octobre2026, pilote borné à40minutes, région Stockholm, instance
c7a.32xlarge :128 cœurs physiques (un thread par cœur),256Gio de RAM.
L'instance a été lancée à15:13:40UTC ; terminaison demandée15:51:35UTC,
état terminé et nettoyage vérifiés15:53:16UTC. Les données ont été
récupérées et leurs empreintes vérifiées AVANT la terminaison.
Coût de calcul estimé jusqu'à la demande de terminaison :4,4441USD,
au tarif AWS vérifié de7,03232USD/h ; ce n'est pas une facture et les
petits frais EBS/IPv4 s'ajoutent. Aucun disque de l'expérience ne reste.

Chaque recherche avait un budget solveur de180s. Les campagnes étaient
successives pour séparer les mesures ; à l'intérieur d'une campagne,
la file distribuait des branches DISJOINTES à des processus séparés.

| Campagne | Cas | Processus × travailleurs | Temps total | CPU moyen échantillonné | Pic RSS cumulé estimé |
|---|---:|---:|---:|---:|---:|
| V10,3 moteurs principaux |61|32×4|375,09s|100,66 cœurs|101,55Gio|
| V10,6 moteurs principaux |61|16×8|750,31s|98,21 cœurs|79,08Gio|
| V10,4 moteurs principaux |61|32×4|375,35s|101,60 cœurs|109,99Gio|
| Colonnes feuilles§56 |11|11×8|188,10s|71,63 cœurs|52,58Gio|
| Labels canoniques§57 |61|32×4|376,03s|100,74 cœurs|110,37Gio|

TOUS les255 résultats sont UNKNOWN, sans candidat D ni exclusion de
branche. Ce sont255 recherches, PAS255 familles distinctes : plusieurs
réglages sont comparés sur les mêmes61 branches. Aucun pourcentage
d'exclusion n'est déduit de leurs compteurs. Le test local global V10
reste aussi UNKNOWN181,57s, pic4,64Gio et476260 conflits sommés.

Les valeurs CPU du tableau proviennent de mesures toutes les10s ; elles
sous-estiment les dernières secondes de chaque processus. L'instrument
amélioré des trois dernières campagnes mesure aussi le CPU en sortie
de solveur : moyennes respectives105,29,74,40 et104,58 cœurs. Les pics
RSS sont des estimations par agrégation temporelle, pas des mesures
exactes au même instant. Le prétraitement, la construction et la dernière
vague de29jobs expliquent une partie de l'écart à128 cœurs.

**Comparaison des moteurs.** Les61 empreintes de modèles correspondent
exactement entre les trois premières campagnes. Doubler les travailleurs
par branche double ici presque le coût total du passage, et augmente
l'activité de recherche ; aucun temps jusqu'à une preuve n'est mesuré.
Le quatrième moteur à4travailleurs augmente les conflits médians
(130744->233802) et la mémoire, mais ne produit aucun verdict. Ni les
conflits ni les domaines d'arêtes ne permettent de le déclarer optimal.
Le portefeuille4travailleurs initial n'avait que3moteurs principaux,
ce qui a motivé cette comparaison explicite plutôt qu'une extrapolation.

**Renforcements mathématiques.** Les colonnes feuilles ajoutent3192
produits et72 égalités conditionnelles. Sur les11 paires comparées à
8travailleurs, le nombre de domaines d'arêtes réduit varie de-8 à+10,
médiane+1 ; aucun gain jusqu'à preuve n'est établi. La concurrence
était11processus contre16 pour le passage de référence : ne pas traiter
leurs temps CPU comme une comparaison parfaitement isolée du modèle.
Les labels canoniques ajoutent42 contraintes et zéro variable auxiliaire.
La médiane de domaines réduits passe ici de314 à345, mais cela concerne
des représentants différents ; ce n'est pas une nouvelle propriété de
graphes ni une mesure du nombre de graphes exclus.

**Choix opérationnel.**32 processus de4travailleurs constituent un
point de départ mesuré pour une recherche par branches : un passage
de61 essais de3minutes en6min15, avec une marge mémoire importante.
Le réglage optimal pour une preuve reste inconnu. Le prochain calcul
doit viser une réduction mathématique nouvelle ou une branche précise,
pas une nouvelle série identique motivée par les seuls conflits.
Les clauses ne sont pas échangées entre processus, ni sauvegardées
comme un apprentissage réutilisable. Les255 recherches ne sont pas
une seule recherche continue de12h45 avec clauses cumulées.

Les critères de§53–57 restent acquis indépendamment de ces UNKNOWN :
plafonds collectifs, couverture61, propagation BG=GE, colonnes feuilles
et choix de représentants. La contrôlabilité est une condition de
complétion, pas une hypothèse imposée sans preuve au E recherché.
Conway, C1 et la famille(0,2) restent ouverts.

Artéfacts : `partition_v10/campaign_summary.json`, les trois rapports
`aws_comparison.json`, `aws_leaf_comparison.json`,
`aws_canonical_comparison.json`, et les255 dossiers de jobs sous
`aws_pilot/results/`. Le contrôle d'intégrité vérifie les trois archives,
les sources et tous les retours de jobs. L'ancien modèle V7 est un
préfixe EXACT de V10 :25395 variables et76900 contraintes ajoutées,
empreinte globale `5ef64ae6738739c13901aa3a3dba89b6b4009377c9bcd4a948cd312b5ee4267c`.
Les snapshots et données brutes sont conservés sans conversion des fins
de ligne. Aucun certificat UNSAT n'existe dans cette campagne.

## 59. V11 : une identité d'énergie pour chaque colonne du défaut

13 octobre2026. Reprise mathématique demandée par Dilan, sans nouveau
calcul AWS. Le pont avec Claude est rétabli, messages592–597. La question
est de comprendre ce qu'un défaut mixte non nul serait obligé de porter,
et de transformer cette obligation en contradiction.

On conserve les hypothèses de§55 : A binaire, symétrique, diagonale nulle,
k-régulier, mu entier, k²=mu(n-1), et les DEUX blocs diagonaux de
T=A²+A-(k-mu)I-mu J nuls. Ainsi T=[[0,G],[G^t,0]]. Aucune hypothèse de
rang, d'automorphisme ou de contrôlabilité n'est ajoutée.

**Identité d'énergie.** Pour chaque colonne g=G_u et d=D_u :

    ||g||² = d^t (2B+I) g.                                  (59a)

Preuve. L'équation définissant le bloc mixte est

    g=(B+I)d + sum_{v voisin de u dans E} D_v - mu*1.

Le produit scalaire avec g annule le dernier terme, car 1^t g=0. Par
D^tG=G^tD, on a D_v^t g=d^t G_v. Par BG=GE, leur somme vaut d^t B g.
Le premier terme contribue d^t(B+I)g, ce qui prouve(59a). C'est une
identité PAR COLONNE ; on n'affirme pas l'égalité matricielle obtenue en
enlevant les produits diagonaux, qui demanderait une commutation de plus.

**Lemme de fermeture entière.** Si Bg=0 ou Bg=-g, alors g=0.

En effet(59a) donne ||g||²=+/-d^t g. Mais g est entier, sa somme est nulle,
et d est binaire. Donc

    |d^t g| <= ||g||_1/2 <= ||g||²/2.                         (59b)

La première inégalité sépare les coordonnées positives et négatives de g,
de masses égales. La seconde utilise |a|<=a² pour a entier. Un g non nul
donnerait ||g||²<=||g||²/2, contradiction. Aucun calcul de voisins communs
supplémentaire n'est nécessaire. L'intégralité est essentielle :
g=(1/2,-1/2), d=(1,0) vérifie ||g||²=d^t g sans être nul.

Plus généralement, si une colonne entière NON NULLE est un vecteur propre
de B, sa valeur propre theta est rationnelle (lire une coordonnée non nulle),
donc entière puisque B est une matrice entière. On a |2theta+1|>=2.
En particulier theta=0 et theta=-1 sont impossibles.
Cela n'interdit PAS une composante propre0 ou-1 dans une colonne qui
mélange plusieurs modes. Le lemme porte bien sur une colonne entière.

**Deux corollaires uniformes.** Si E est une coclique, BG=0 ferme toutes
les colonnes. Si E est une clique, BG=G(J-I)=-G les ferme aussi. Les degrés
et les deux blocs diagonaux exacts suffisent donc à fermer le système
entier dans ces deux cas. Cela vaut pour tout paramètre lambda=mu-1
satisfaisant les hypothèses, pas seulement pour Conway. Le prisme
pentagonal de§55 reste un contre-exemple lorsque E est un cycle5.

Il s'agit d'un nouveau résultat dans cette campagne. Aucune priorité
bibliographique générale n'est revendiquée.

## 60. Conséquences pour les colonnes négatives de tout le profil(0,2)

Dans le modèle V10, les lignes mixtes C+H sont exactes. Puisque T commute
avec A, T*1=0 et T*1_C=0, le vecteur
q=4*1-(A+4I)*1_C satisfait aussi Tq=0. Or sa partie résiduelle vaut

    q_M=-(e_e+e_f), d'où G_e+G_f=0.                          (60a)

Une autre preuve utile passe par le transport des espaces de§61 :
G D_C^t=0, et D_C^t*1_C=4*1_M+e_e+e_f, car les colonnes négatives
ont cinq voisins dans C et les autres en ont quatre.

**Toutes les11 branches a=1.** Si e est une feuille de E, son seul voisin
résiduel est f. Donc BG_e=G_f=-G_e. Le lemme59 impose G_e=0, puis G_f=0.
Les DEUX colonnes négatives sont exactes, même si f n'est pas une feuille.
Les équations conditionnelles de§56 sont donc des conséquences de V10
avec ses deux blocs diagonaux exacts et ses lignes C exactes. Elles
peuvent accélérer la propagation d'un solveur ; elles ne suppriment pas
une solution de V10 qui aurait un défaut dans ces colonnes.

**Branche(2,2,Z0).** Les deux négatifs ont le même unique voisin z dans
Z0, troisième sommet du triangle ef. On a

    E(e_e+e_f)=e_e+e_f+2e_z.

Par(60a) et BG=GE, G_z=0. Ensuite BG_e=G_f+G_z=-G_e, donc G_e=G_f=0.
Trois colonnes sont automatiquement exactes dans cette douzième branche.

**Propagation supplémentaire dans(1,2).** Après G_e=G_f=0, l'unique
voisin z de f dans Z0 vérifie G_z=BG_f-G_e=0. Dans une branche(1,b)
quelconque, la somme des défauts des b-1 voisins Z0 de f est nulle ;
on ne conclut pas séparément si b-1>1 sans une autre contrainte.

Les12 branches mentionnées ne sont PAS exclues. Le résultat exclut un
type précis de défaut de coexistence qui semblait encore disponible.
Les colonnes restantes et l'existence du bord B,D restent à résoudre.

## 61. Propagation entre les deux blocs, puis fermeture entière

Maintenir deux espaces prouvés U inclus dans ker(G^t) et V inclus dans
ker(G). Les relations de commutation donnent quatre transports :

    B U inclus dans ker(G^t),   D V inclus dans ker(G^t),
    E V inclus dans ker(G),     D^t U inclus dans ker(G).       (61a)

Par exemple G D^t x=D G^t x=0 pour x dans U. Les espaces initiaux
contiennent1_B et1_M ; chaque ligne ou colonne mixte déjà exacte ajoute
le vecteur unité correspondant. Les lignes C exactes apportent ainsi
TOUS les vecteurs D_c^t au côté résiduel, pas seulement leur somme(60a).

Après saturation linéaire par(61a), ajouter la règle suivante :

    Si (E-theta I)e_u appartient à V pour theta=0 ou-1,
    alors e_u appartient à ker(G).                           (61b)

En effet BG_u=GE e_u=theta G_u, puis§59 ferme la colonne. La même règle
avec B et U ferme des lignes, en échangeant les deux blocs. Répéter
transport et fermeture jusqu'à stabilisation. Ce n'est pas simplement
une nouvelle écriture de l'espace de marches : l'intégralité permet
d'ajouter des vecteurs unités qui n'y appartenaient pas.

Une classe de vrais jumeaux dans E (clique avec même voisinage extérieur)
dont la somme des colonnes de G est nulle se ferme colonne par colonne :
la somme des équations BG_u annule la contribution extérieure commune,
puis BG_u=-G_u. Pour de faux jumeaux indépendants, on obtient BG_u=0.
Ce sont des jumeaux DANS LE BLOC E ; aucune symétrie du graphe99 entier
n'est supposée. Le cas(2,2,Z0) de§60 est une application à la paire e,f.

Code exact : `coclique_integral_defect_closure.py`. Les graines doivent
être justifiées par les hypothèses ; le propagateur n'utilise pas la
valeur calculée de G pour inventer des graines. Le mode `certify` vérifie
séparément les hypothèses et les conclusions sur un candidat concret.

**Contrôles nouveaux ciblés.** Le Paley25 sauvegardé, repartitionné avec
une paire adjacente dans M, donne des dimensions(U,V)=(1,1)->(2,1) par
le seul transport linéaire : les deux colonnes restent indissociables.
La règle entière ajoute les deux unités résiduelles, atteint V=R² et
ferme tout G. Sur la grille3x3 avec deux sommets indépendants dans M,
c'est le mode0 qui ferme les deux colonnes. Le prisme pentagonal conserve
ses dimensions(1,1), son défaut non nul et aucune fermeture indue.
Les85 vecteurs entiers de somme nulle dans[-2,2]^4 satisfont(59b) pour
les16 choix binaires de d ; ce dernier contrôle illustre l'inégalité,
dont la preuve pour toute dimension est donnée ci-dessus.

Sortie : `integral_closure_v11/integral_closure_checks.json`, PASS.
Aucun gros solveur, aucun nouveau candidat C1 et aucune branche C1
déclarée impossible dans ces contrôles.

## 62. Échange avec Claude : budgets de triangles et redondances identifiées

Messages593–596. Soit N l'incidence sommets/triangles, avec231 triangles,
sept par sommet. Alors NN^t=A+7I. Pour q de§2 avec delta=1, écrire
q_L=sum_{v dans L}q_v. On obtient exactement

    sum_L q_L=126,   sum_L q_L²=336.

Il y a147 triangles rencontrant C21 et84 entièrement hors C ; leurs
sommes de charges respectives sont42 et84. Le budget de variance240
proposé par Claude est une réécriture de ces identités. Il ne constitue
pas à lui seul une restriction nouvelle après la loi Aq=3q+2*1.

Pour préciser cette redondance dans(0,2), poser r=#triangles H-Y-Y et
b=#triangles entièrement dans L (donc dans Y, car chaque X a degré1
dans L). Le nombre de triangles par charge est nécessairement :

| Charge du triangle | Nombre |
|---|---:|
|5|4|
|4|r|
|3|8-2r+b|
|2|26-3b|
|1|44+2r+3b|
|0|136-r-b|
|-1|12|
|-2|1|

Preuve : les quatre arêtes H-H donnent les quatre triangles H-H-X.
Les vingt autres triangles contenant H se répartissent en r H-Y-Y,
8-2r H-Y-Z et12+r H-Z-Z, où Z signifie ici une charge nulle. L a14
arêtes ; après celles des r triangles H-Y-Y et des b triangles L-L-L,
il reste14-r-3b triangles L-L-Z. Compter les84 incidences de triangles
aux12 sommets L donne44+2r+3b triangles L-Z-Z. Le triangle ef a charge-2,
et les six autres triangles par négatif ont charge-1. Les moments126
et336 sont identiques pour tout r,b : compter ces types seuls ne les
renforce pas.

Claude a aussi étudié la Gram des droites associée au projecteur propre
-4 : diagonale4, entrée0 pour deux droites sécantes et1-j pour deux
droites disjointes reliées par j arêtes. Il a retiré explicitement en
message596 l'affirmation que sa borne supérieure fournirait une coupe
indépendante : elle se ramène aux coupes spectrales de sommets déjà
acquises et au comptage des triangles partiellement présents. Ne pas
réutiliser comme résultat acquis la proposition provisoire du message595.
La poursuite utile doit ajouter une obligation entière ou combinatoire,
ou exploiter ces relations sur un objet où elles ne sont pas déjà imposées.

## 63. V12 : quatre formes pour chaque voisinage complet de H

13 octobre2026, reprise après la configuration du téléphone, laissée en
attente. On conserve la recherche de coexistence déjà autorisée, sans
nouveau calcul AWS. L'identification des sommets par paires de voisins
autour de l'arête négative est déjà présente dans les notes163/177 : elle
n'est pas présentée comme une nouvelle réduction. Le gain effectif ici
porte sur les QUATRE voisinages complets de H dans le modèle global.

Fixons h_i. Deux triangles de N[h_i] sont déjà entièrement déterminés :

    (h_i,h_{i-1},X_{i-1}), (h_i,h_{i+1},X_i).

Après leurs quatre voisins, il reste dix voisins de h_i : les deux Y_i,
les deux C_i dans C, et les six Z_i de charge nulle hors C. Ils induisent
EXACTEMENT cinq arêtes disjointes. En effet, tout voisin de h_i possède
exactement un voisin dans N(h_i), puisque lambda=1. Les deux C_i ne sont
pas appariés entre eux, car C est indépendante.

Les permutations des deux Y_i, des deux C_i et des six Z_i préservent
toutes les données fixes du modèle. Elles donnent exactement quatre
formes, suivant l'existence de Y_0Y_1, sinon le nombre de paires Y-C :

| Forme | Cinq paires dans le voisinage restant |
|---|---|
| YY | Y0-Y1, C0-Z0, C1-Z1, Z2-Z3, Z4-Z5 |
| YC0 | Y0-Z0, Y1-Z1, C0-Z2, C1-Z3, Z4-Z5 |
| YC1 | Y0-C0, Y1-Z0, C1-Z1, Z2-Z3, Z4-Z5 |
| YC2 | Y0-C0, Y1-C1, Z0-Z1, Z2-Z3, Z4-Z5 |

**Preuve de couverture.** Si Y0 et Y1 sont appariés, les deux C doivent
être appariés à deux Z distincts ; les quatre Z restants forment deux
paires. Sinon, choisir les zero, une ou deux paires Y-C. Chaque Y ou C
encore libre est apparié à un Z distinct ; les Z restants sont appariés
entre eux. On nomme successivement les Y et C selon leur rôle, puis leurs
mates Z, puis les paires Z-Z. Cela produit exactement le tableau.

Les quatre ensembles de dix sommets sont disjoints. On peut donc faire
ces renommages simultanément, en transportant TOUTES les arêtes du
graphe, y compris celles vers les autres groupes et vers e,f. On ne
suppose aucun automorphisme du graphe99 et on ne choisit pas quatre
réalisations locales à recoller après coup.

Il y a 9!!-7!!=840 appariements étiquetés admissibles. Les tailles des
quatre orbites sont90,360,360,30. Un contrôle exhaustif distinct du
raisonnement engendre les840 appariements et les orbites sous
S2(Y) x S2(C) x S6(Z), puis vérifie leur égalité et leur disjonction.
Les quatre sélections du véritable encodeur sont aussi contrôlées.
Ce sont des contrôles de la NOUVELLE normalisation, pas une reprise
des anciens audits ni840 configurations globales de C1.

**Précaution nécessaire dans l'encodeur.** Les anciens ordres de
signatures sur C_i et Z_i ne sont pas imposés en plus de ces formes :
ils pourraient demander deux représentants incompatibles. Les ordres
sur C13 et Z0 subsistent. Dans chaque forme choisie, on ordonne seulement
les extrémités et les paires des arêtes Z-Z, par les permutations qui
préservent cette forme et fixent les ancres H,L,e,f. La combinaison
avec l'ancienne option de normalisation du triangle négatif est refusée
tant qu'une preuve de compatibilité n'est pas donnée.

## 64. Les quatre formes partagent le budget de l'arête négative

Pour tout sommet v de C8 ou ZH, sa charge est nulle et son unique voisin
dans H contribue2. La propagation des charges donne donc exactement

    d_L(v) = [v~e]+[v~f].                                  (64a)

Ainsi, une arête Y-C ou Y-Z dans un appariement de§63 impose que son
extrémité de charge nulle soit voisine de e ou de f. Les placements dans
les quatre étoiles utilisent ces mêmes deux sommets négatifs.

Notons kappa_i le nombre de paires Y-C de la forme choisie. Il vaut
respectivement0,0,1,2 pour YY,YC0,YC1,YC2. En sommant(64a) sur C8 et en
utilisant r_e=1+d_C8(e), r_f=1+d_C8(f), on obtient

    sum_i kappa_i <= r_e+r_f-2.                            (64b)

Les deux règles sont des conséquences des équations du modèle global,
rendues explicites sur les petits sélecteurs de formes ; elles ne sont
pas présentées comme de nouvelles exclusions indépendantes de V10.
Le nombre de quadruplets de formes autorisés par ce seul budget est
la somme des coefficients de (2+x+x²)^4 jusqu'au degré r_e+r_f-2 :

| Budget | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | au moins8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Quadruplets | 16 | 48 | 104 | 160 | 209 | 237 | 251 | 255 | 256 |

En particulier, dans les branches(1,1), chaque étoile est YY ou YC0.
Cela ne ferme aucune branche : les arêtes entre les groupes et la
factorisation binaire commune restent à construire.

## 65. Taille réelle et essai court de la réduction V12

`coclique_star_normal_form.py` impose quatre sélecteurs par étoile et
fixe les arêtes communes aux quatre formes AVANT la création des produits.
Sur132 entrées fixées dans les quatre étoiles, quatre étaient déjà les
paires C-C nulles ;128 variables d'arêtes supplémentaires disparaissent.
L'option `--canonical-stars` du moteur de partition est désactivée par
défaut. Le modèle de référence conserve exactement son ancienne empreinte
`5ef64ae6738739c13901aa3a3dba89b6b4009377c9bcd4a948cd312b5ee4267c`.

Deux essais SUCCESSIFS sur tout(0,2), graine1, huit travailleurs, plafond
60s, même portefeuille booléen, sans reprise de clauses :

| Mesure | V10 de référence | V12, formes des étoiles |
|---|---:|---:|
| Variables totales | 272224 | 258064 |
| Variables d'arêtes | 4231 | 4103 |
| Variables de produits | 257271 | 243223 |
| Contraintes | 843270 | 801267 |
| Octets du modèle sérialisé | 42437412 | 40335649 |
| Pic mémoire observé, Gio | 4,251 | 4,086 |
| Temps solveur, s | 61,414 | 61,124 |
| Verdict | UNKNOWN | UNKNOWN |

Le gain certain de représentation est de14160 variables (-5,20%) et
42003 contraintes. Le pic mémoire de CE passage baisse de3,88%.
Les deux temps proches du plafond ne mesurent pas le temps jusqu'à une
preuve. Aucun gain de ce dernier n'est établi. Les domaines resserrés
concernent des représentants différents et ne sont pas comparés comme
des exclusions de graphes. Pas de nouveau D, pas de contradiction C1.

Les sources, empreintes, contrôles et mesures sont conservés dans
`data/codex_coclique_defects/star_normal_form_v12/`. Les deux calculs
sont terminés ; aucun calcul AWS n'a été relancé. Cette normalisation
constitue une réduction modeste du coût du modèle, pas une résolution
du goulot mathématique de la factorisation binaire. La suite doit relier
les appariements des quatre étoiles aux mêmes cycles de ef et aux mêmes
21 sommets de C, au-delà de leurs seuls budgets ; pas une nouvelle série
identique de calibrations.

## 66. V13 : complétion exacte sur un bord quelconque avec régularité

13 octobre2026. L'échange609–611 avec Claude a identifié une hypothèse
indispensable de la formule V6 telle qu'elle était écrite : le voisinage
complet fournit la régularité du bloc extérieur. Sur un autre bord,
appliquer simplement D^+ au bloc mixte peut donner une matrice NON
symétrique. Voici l'extension, qui incorpore cette régularité au système
linéaire et supprime toute hypothèse de voisinage complet.

Soient n,m>0, v=n+m, des entiers k>=mu>0 avec k²=mu(v-1), et q=k-mu.
On suppose seulement B symétrique binaire de diagonale nulle, D binaire,
de tailles n x n et n x m, satisfaisant

    D1 = k1-B1,       DD^t = K = qI+mu J-B²-B.             (66a)

Les vecteurs1 et les matrices J ont les dimensions indiquées par les
produits. Posons

    b = D^t1,        rho = k1-b,
    F = mu J-(B+I)D,
    C = [ D  ],      R = [ F     ],
        [ 1^t]          [ rho^t ],
    E0 = C^+ R,      P = I-C^+ C.                         (66b)

Le symbole C désigne ici la matrice augmentée, pas une coclique.
Les identités suivantes sont AUTOMATIQUES sous(66a) :

    CE0=R,  E0=E0^t,  P=P^t=P²,  CP=0,  E0P=PE0=0,
    E0 1=rho,
    E0²+E0+D^tD = q(I-P)+mu J.                          (66c)

Si r,s sont les deux racines distinctes de x²+x-q, toutes les complétions
réelles symétriques régulières satisfaisant le polynôme SRG sont
EXACTEMENT

    E = E0+rP+(s-r)Q,   Q=Q^t=Q²,   PQ=QP=Q.             (66d)

Il existe une complétion SRG si et seulement si l'une de ces matrices E
est ENTIÈRE. L'intégralité seule impose alors la diagonale nulle et les
entrées0/1. Pour Conway, r=3,s=-4, donc E=E0+3P-7Q.
Le facteur binaire COMMUN D reste une hypothèse, jamais remplacée par
une collection de facteurs locaux ou par K positif.

**Preuve des identités linéaires.** Toutes les lignes de R appartiennent
à l'espace des lignes de C : cela se lit directement dans F et rho.
Ainsi RP=0. De plus,

    D F^t = F D^t,       D rho = F1.                     (66e)

La première identité résulte de K=qI+mu J-B²-B et D1=k1-B1 ; la seconde
utilise en plus k²=mu(v-1). Elles donnent CR^t=RC^t. Écrivons C^+ pour
la pseudo-inverse de Moore-Penrose. Puisque RP=0,

    R = R C^t(C^+)^t = C R^t(C^+)^t.

Les colonnes de R sont donc dans l'image de C et CC^+R=R. Enfin

    C^+R = C^+C R^t(C^+)^t = R^t(C^+)^t,

car les colonnes de R^t sont dans l'image de C^t. Cela prouve la symétrie
de E0 et CE0=R. La définition de P et RP=0 donnent les autres identités
linéaires, notamment P1=0 et E0 1=rho.

**Preuve du polynôme comprimé.** Posons

    L = E0²+E0+D^tD-qI-mu J.

En utilisant DE0=F, E0 1=rho et K, on obtient

    DL = mu 1 rho^t-BF+(K-qI)D-mu(D1)1^t
       = mu 1(rho+b)^t-mu(B1+D1)1^t = 0.

D'autre part E0 b=F^t1, donc

    L1 = (k+1)rho-F^t1+D^t(D1)-q1-mu m1
       = (k+1)(rho+b)-(mu v+q)1
       = [k²-mu(v-1)]1 = 0.

Ainsi CL=0. Par symétrie L=PLP ; mais LP=-qP, puisque E0P=DP=JP=0.
Par conséquent L=-qP, ce qui est(66c).

**Paramétrisation et intégralité.** Si E est symétrique et CE=R, alors
E=E0+T avec T=PTP. Son défaut polynomial vaut T²+T-qP. L'annulation
équivaut à ce que T ait seulement les valeurs propres r,s sur ker C,
d'où(66d), dans les deux sens. Pour E entière, la matrice complète
A=[[B,D],[D^t,E]] est entière, symétrique, k-régulière et vérifie le
polynôme. Soustraire la somme de sa ligne i de son équation diagonale :

    a_ii² + sum_(j!=i) a_ij(a_ij-1) = 0.                 (66f)

Chaque terme est un entier positif ou nul. Ainsi a_ii=0 et toutes les
autres entrées valent0 ou1. C'est la même fermeture entière qu'en V6,
désormais applicable à tout bord satisfaisant(66a).

Lorsque B contient un voisinage complet, 1^t est déjà dans l'espace
des lignes de D. L'augmentation ne change alors ni E0 ni P : V6 est
exactement retrouvée. Elle peut aussi être redondante sur d'autres
bords ; en général son gain de rang vaut0 ou1.

## 67. Les réductions affine et convexe survivent sur le bord augmenté

Pour étendre V7, il faut employer le BON noyau homogène :

    V_C = {T=T^t : diag T=0, DT=0, T1=0}.                (67a)

Prendre ker D seul après avoir corrigé E0 laisserait de nouveau varier
les degrés. Les complétions linéaires symétriques de diagonale nulle,
DE=F et E1=rho, forment un espace vide ou E_*+V_C.

Si h=dim ker C et N est une base colonne de ker C, alors

    delta = dim V_C
          = h(h+1)/2-rang[S -> diag(NSN^t)]
          <= h(h-1)/2.                                  (67b)

En effet, h lignes indépendantes de N donnent h formes quadratiques
indépendantes dans cette application diagonale, comme en V7. On choisit
delta paires dont l'évaluation est injective sur V_C ; les autres
entrées de E sont des fonctions affines rationnelles de ces arêtes.

Pour toute complétion linéaire BINAIRE de diagonale nulle, son défaut

    Delta = D^tD+E²+E-qI-mu J

appartient lui aussi à V_C. Les calculs DL=0 et L1=0 de§66 ne demandent
que CE=R et la symétrie ; ils restent valables pour E. La diagonale de
Delta est nulle par la binarité et les degrés. Il suffit donc d'annuler
les delta coefficients sélectionnés pour annuler TOUT Delta. Le critère
affine demeure exact, sans voisinage complet et sans projecteur continu.

V8 s'étend également : pour E symétrique et CE=R, les deux contraintes

    E0+rP-E >= 0,      E-E0-sP >= 0                     (67c)

dans l'ordre PSD placent le spectre de T=E-E0 dans[s,r]. Elles donnent
Delta=T²+T-qP <= 0. Si E est entière, chaque diagonale de Delta est la
somme positive(66f), donc vaut0. Une matrice négative PSD de diagonale
nulle est nulle : les points ENTIERS de ce corps convexe sont exactement
les complétions. La faisabilité réelle seule ne suffit toujours pas.

Implémentation : `coclique_regular_completion.py` calcule(66b) exactement.
`coclique_affine_completion.py` expose `regularity=True` dans `frame` et
`binary_completions`, et utilise alors ker C, y compris pour sa base
homogène. Le comportement par défaut de V6/V7 est conservé. Le transfert
convexe(67c) est prouvé ici ; aucune nouvelle option du solveur spectral
n'est annoncée comme implémentée.

## 68. Application uniforme au support régulier de18 sommets

Dans le cadre de norme18 discuté avec Claude, B est4-régulier sur18
sommets, D a81 colonnes et B,D doivent toujours satisfaire(66a). Les
colonnes touchent j sommets de chacune des deux parties, donc b=2j.
Les identités ci-dessous n'exigent aucun choix parmi les noyaux du pair.

    D1=10*1,      K1=28*1,
    sum b=180,    b^t b=504,
    w=1-(5/14)b,  Dw=0,
    1^t w=w^t w=117/7.                                  (68a)

La projection de1 sur l'espace des lignes de D est(5/14)b : en effet
D b=28*1. Ainsi w est exactement la composante de1 dans ker D. Sa norme
non nulle impose que l'ajout de la ligne1^t augmente le rang de1.

L'ancienne formule X=D^+[2J-(B+I)D] vérifie

    X-X^t = (b1^t-1b^t)/14 != 0.                         (68b)

Pour le voir, D^+=D^tK^+ et K commute avec B, car B est régulier. Donc

    X = b1^t/14-D^tK^+(B+I)D,

dont le second terme est symétrique. Le vecteur b ne peut être constant :
sinon b^t b=(sum b)²/81=400, contre504. Le transfert littéral de V6
échoue donc pour TOUT facteur de ce cadre, pas seulement pour un exemple.

La correction explicite donnée par§66 est

    E0 = X + w b^t/14 + (8/117)w w^t,
    P  = P_D-(7/117)w w^t,       P_D=I-D^+D.             (68c)

Pour vérifier la première formule, son ajout à X rétablit la symétrie
par(68b) ; D fois la correction est nul. De plus X1=rho-14w,
(w b^t/14)1=(90/7)w et ((8/117)w w^t)1=(8/7)w. Elle a donc la bonne
somme de lignes, et elle annule ker D intersect 1^perp. Cela caractérise
E0 de§66. La seconde formule est l'intersection orthogonale des noyaux.

On peut éviter les fractions dans le mode retiré :

    t=7*1-5j=7w,   t^t t=819,   P=P_D-t t^t/819.         (68d)

Pour les colonnes j=0,1,2,3 du cadre de Claude, t vaut respectivement
7,2,-3,-8. Ces valeurs ne constituent pas une preuve supplémentaire
de l'absence de j>=4 ;(68a–d) ne dépendent pas de cette exclusion.

Le plan engendré par b,w est forcé, avec

    E0 1=14*1-b,       E0 b=36*1-5b.

Dans la base(b,w), sa matrice est

    [55/7   117/98]
    [36       8/7],

de polynôme caractéristique x²-9x-34. Cela décrit un bloc du graphe
extérieur E, pas des valeurs propres nouvelles de la matrice A entière.
La correction enlève une direction de liberté artificielle ; elle ne
fabrique ni le facteur binaire D ni le projecteur entier de complétion.
Aucune campagne sur les26 noyaux n'est lancée.

## 69. Contrôles ciblés de V13 et portée restante

`check_coclique_regular_completion.py` contrôle la NOUVELLE extension
en arithmétique rationnelle, sur six bords sans voisinage complet :
un sommet de la grille3x3, une arête de cette grille, un bord irrégulier
de trois sommets, un bord injectif de cinq sommets, un sommet de Petersen
et une paire non adjacente de Petersen. Un septième cas, voisinage fermé
de la grille, vérifie seulement l'identité avec l'ancienne formule.

Sur les deux bords réduits à un sommet, l'ancienne formule est effectivement
non symétrique ; la correction explicite pour un bord régulier et son
projecteur sont contrôlés. Chaque bloc connu est reconstruit par(66d).

| Bord sans voisinage complet | h | delta | Affectations des arêtes libres | Candidats binaires linéaires | Complétions exactes |
|---|---:|---:|---:|---:|---:|
| Arête de la grille3x3 |4|3|8|8|4|
| Bord irrégulier de la grille |2|0|1|1|1|
| Bord injectif de la grille |0|0|1|1|1|
| Paire non adjacente de Petersen |5|7|128|24|12|

Pour chaque affectation binaire du cadre affine, on vérifie la régularité.
Pour chaque matrice binaire obtenue, le défaut appartient bien à V_C et
l'annulation sur les paires sélectionnées équivaut à son annulation
totale. Les résultats de l'encodeur coïncident exactement avec cette
énumération courte. Le verdict OPTIMAL de ces petits contrôles signifie
que leurs complétions sont toutes énumérées, pas une exclusion C1.

Les moments et la correction de§68 sont aussi contrôlés symboliquement
dans leur plan de dimension2 ; aucun facteur99 n'est supposé construit.
Résultats PASS dans `data/codex_coclique_defects/regular_completion_v13/`.
Pas de répétition de l'audit243, pas de nouveau calcul long ou AWS.

Le résultat nouveau est la suppression de l'hypothèse de voisinage complet
dans les critères exacts de complétion, avec implémentation de la version
affine. Il n'exclut aucune branche C1. Enfin, l'exclusion éventuelle des
cocliques22 et de tous les profils de cocliques21 maximales n'impliquerait
que alpha<=20 : aucune borne alpha>=21 n'est démontrée ici. Le critère
général(66) n'utilise précisément aucune de ces hypothèses de coclique.

## 70. V14 : une différence de rang deux est un échange de sommets

Suite structurelle de V13, 13 octobre2026. On cherche à distinguer une
ambiguïté de reconstruction d'une simple ambiguïté d'étiquettes. Le
résultat ci-dessous porte sur tous les graphes de paramètres Conway,
sans support de norme fixé et sans hypothèse sur une coclique.

**Théorème.** Soient A et A' deux matrices d'adjacence SRG(99,14,1,2)
sur le même ensemble étiqueté. Si rang(A'-A)=2, il existe une transposition
S de deux sommets telle que A'=SAS^t. La différence porte exactement sur
26 sommets et48 arêtes non orientées :24 ajoutées et24 retirées.

Cela ne dit pas que S est un automorphisme de A : lorsque A'!=A, S ne
fixe pas A. Il donne un isomorphisme entre les deux réalisations. Une
modification de rang deux ne peut donc produire un graphe non isomorphe
à un graphe de Conway donné. C'est un résultat conditionnel ; aucun
graphe de Conway n'est construit ou exclu.

**Forme générale d'une différence binaire de rang deux.** Posons T=A'-A.
La symétrie, le rang2 et la trace nulle donnent T=l(xx^t-yy^t), l>0,
avec x,y orthonormaux. La diagonale nulle impose x_i²=y_i². On partage
les lignes non nulles en U, où x_i=y_i, et V, où x_i=-y_i. T est nul à
l'intérieur de chaque partie, et toutes les entrées entre U et V sont
non nulles. Puisque ces entrées valent+1 ou-1, leurs valeurs absolues
imposent des amplitudes constantes sur chaque partie. On peut donc écrire

    T = u v^t+v u^t,                                    (70a)

où u,v ont des supports disjoints U,V et des coefficients non nuls+1/-1.
La régularité donne T1=0, donc sum u=sum v=0. Notons

    |U+|=|U-|=p,       |V+|=|V-|=q,       p,q>=1.

Sur U x V, la binarité des deux graphes force

    A_ij=(1-u_i v_j)/2,   A'_ij=(1+u_i v_j)/2.           (70b)

## 71. Le polynôme et les deux voisins communs ferment le rang deux

Soustraire les équations A²+A=12I+2J et A'²+A'=12I+2J donne

    AT+TA+T²+T=0.                                       (71a)

Pour z dans ker T, cela impose TAz=0. Ainsi A préserve ker T et,
par symétrie, son orthogonal im T=span(u,v). La formule(70b) donne alors

    Au=alpha*u-p*v,       Av=-q*u+beta*v,                 (71b)

avec alpha,beta ENTIERS : on lit les coefficients sur une ligne de U
ou V, où u_i ou v_i vaut+1/-1. Comme u et v sont orthogonaux à1,
la restriction de A à ce plan vérifie le polynôme x²+x-12. Ses termes
hors diagonale sont non nuls, d'où

    alpha+beta=-1,
    pq=12-alpha(alpha+1).                                (71c)

Si p>=2, deux sommets de U+ ont les q sommets de V- comme voisins
communs dans A. Ils ont au plus2 voisins communs, donc q<=2. De même,
q>=2 impose p<=2. Si p et q sont tous deux au moins2, ils valent donc
tous deux2. Mais(71c) demanderait alpha(alpha+1)=8, impossible dans Z.

On a donc p=1 ou q=1. Quitte à échanger les parties, p=1. Écrivons
U={a,b}, u=e_a-e_b et e=A_ab. Sur ces deux coordonnées, Au donne
alpha=-e, donc alpha appartient à{0,-1}. L'équation(71c) force q=12.
De plus(71b) impose A_za=A_zb pour tout z hors U union V. Échanger a,b
renverse exactement les arêtes de(70b), conserve l'arête ab et ne change
rien ailleurs : A'=SAS^t. Le support a2+24=26 sommets et la coupe
U x V comporte2*24=48 arêtes modifiées. Cela prouve§70.

La même analyse, pour des paramètres généraux(v,k,lambda,mu), donne

    alpha+beta=lambda-mu,
    pq=k-mu+(lambda-mu)alpha-alpha².                     (71d)

Cette identité montre où les paramètres interviennent. Le théorème de
rigidité n'est PAS étendu sans preuve à tous les graphes fortement réguliers.

## 72. Conséquence pour la reconstruction d'un bord fixé

Conservons B,D du théorème66 et C=[D;1^t]. Si E et E' sont deux
complétions, leur différence T vérifie CT=0 et est symétrique ; ainsi

    rang T <= dim ker C = h.

Une matrice symétrique non nulle de diagonale nulle ne peut avoir rang1.
Pour h<=2, toute différence non nulle a donc rang2. Les complétions de
paramètres Conway sont alors toutes isomorphes par une transposition
de deux sommets EXTÉRIEURS, fixant le bord point par point.

Cette transposition ne change pas D : les deux colonnes correspondantes
de D sont nécessairement identiques. En particulier :

* si h<=2 et toutes les colonnes de D sont distinctes, la complétion
  étiquetée est unique, lorsqu'elle existe ;
* pour h<=2, il y a au plus deux complétions étiquetées, puisque§67
  donne delta<=1 et que le coefficient libre peut être une arête binaire ;
* si le bloc extérieur compte au plus25 sommets et h<=2, la complétion
  étiquetée est unique, car la différence de§70 exige26 sommets.

Ces conséquences concernent la multiplicité des complétions d'un MÊME
facteur D. Elles ne construisent pas D et ne comparent pas deux facteurs
indépendants. Elles ne supposent pas non plus h<=2 dans le modèle99
actuel : cette condition doit être effectivement obtenue pour le bord
considéré. On ne retourne pas à une énumération des rangs de Seidel.

## 73. Le cas h=2 avec une colonne répétée se décide sans solveur

Voici une exploitation algorithmique, valable plus généralement pour
lambda=mu-1 et nu=k-mu>0, sous les hypothèses66. Supposons h=2 et
D_a=D_b. Alors u=e_a-e_b appartient à ker C. La droite de ker C
orthogonale à u est calculable AVANT toute complétion.

S'il existe une complétion E, écrivons e=E_ab dans{0,1}. Le noyau ker C
est invariant par E, car E=E0+PTP. Le vecteur

    v=-Eu-eu

est non nul, orthogonal à u, nul sur a,b, et a des coefficients0,+1,-1.
Il a une somme nulle. Le polynôme appliqué à u donne

    ||Eu||²+u^tEu=nu||u||²,
    ||v||²=2nu,
    Eu=-eu-v,          Ev=-nu*u+(e-1)v.                 (73a)

Ainsi la droite orthogonale doit admettre un générateur v nul sur a,b,
dont les coefficients non nuls ont tous la même amplitude ; une fois
normalisé à+1/-1, il doit avoir exactement nu signes+ et nu signes-.
Toute violation est un certificat d'impossibilité du facteur D.

Il reste seulement à calculer E0 de§66 et

    e=2(E0)_aa.                                         (73b)

Si e n'est pas0 ou1, il n'y a pas de complétion. Sinon les SEULES
matrices possibles sont

    E_± = E0-(e/2)u u^t+((e-1)/(2nu))v v^t
          ±(u v^t+v u^t)/2.                            (73c)

La formule résulte de(73a) dans la base orthogonale(u,v). Réciproquement,
ces deux matrices sont symétriques, ont les bons degrés et vérifient le
polynôme : sur ker C, leur matrice est [[-e,±nu],[±1,e-1]], dont le
carré plus elle-même vaut nu I. Sur l'orthogonal, c'est§66. Les deux
matrices sont échangées par la permutation de a,b, car E0u=0 et v_a=v_b=0.
Il suffit donc de vérifier l'INTÉGRALITÉ d'une seule d'entre elles.
Si elle est entière,§66 impose la diagonale nulle et la binarité ; sinon
aucune des deux ne convient. Pour Conway, v a12 signes+ et12 signes-.

`coclique_rank_two_rigidity.py` implémente ce critère exact dans
`complete_nullity_two_pair`. Il distingue explicitement un facteur
impossible d'un cas auquel le critère ne s'applique pas. Un appel hors
h=2 ou sans colonne répétée ne constitue jamais une exclusion.

Les contrôles nouveaux sont conservés dans `rank_two_rigidity_v14/` :

* trois échanges de sommets sur la grille3x3 et Petersen contrôlent
  la décomposition(70a) et les identités(71d) ;
* un bord de Petersen sans voisinage complet, avec h=2 et deux colonnes
  identiques, est reconstruit exactement par(73c), sans solveur : deux
  matrices étiquetées, un seul graphe à isomorphisme près ;
* un facteur3x6 pour un bord de la grille satisfait BIEN le Gram et les
  degrés, mais a deux paires de colonnes identiques. La droite orthogonale
  n'a que deux coordonnées non nulles, au lieu des quatre requises : le
  critère le rejette. C'est un exemple de contrôle, pas une branche C1 ;
* une modification de rang2 de la grille4x4 donne deux SRG(16,6,2,2)
  NON isomorphes, l'un avec huit cliques4 et l'autre sans clique4. Elle
  a p=q=2,alpha=beta=0 et satisfait(71d). Ce contre-exemple confirme
  que la conclusion de§70 dépend réellement des paramètres Conway.

Tous les contrôles exacts passent. Aucun audit243 ni catalogue de noyaux
n'est repris. Le résultat exploitable est une rigidité de reconstruction
et un test complet dans le cas singulier spécifié, pas une résolution
du problème d'existence C1.
