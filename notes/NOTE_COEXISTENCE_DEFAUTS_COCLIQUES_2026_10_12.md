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
