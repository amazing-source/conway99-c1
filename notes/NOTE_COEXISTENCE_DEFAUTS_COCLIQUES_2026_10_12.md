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
