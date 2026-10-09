# Recherche active C1 — changement de cap du 9 octobre 2026

**Suite au message 476 — note 240 :** LAB annonce l'exclusion exacte des
deux formes d'étoiles de centres laissées par la note 239, commit 589ea52,
fichiers `ribbon6_star_forms.py/json`. Résultat de pair utilisé sans audit
en double. Avec la note 239, toute étoile de cordes est donc interdite.
Nouvel apport Codex : le triangle de cordes latérales du ruban tordu est
exclu par 288 masques combinatoires et un certificat entier à 60 lignes,
second membre −3, sans filtre spectral. Conséquence combinée : tout ruban
six injectif possède soit deux cordes sans extrémité commune, soit EXACTEMENT
le triangle de centres alternés {c0c2,c2c4,c4c0}, à rotation près.
Le triangle de centres reste ouvert pour les deux fermetures. Les quatre
exemples de deux cordes disjointes fournis par LAB passent encore le test
conjoint des deux sommets extérieurs complétant leurs triangles : 126,87,
358,106 choix, sans prétention de prolongement. Ne pas compter ces choix
comme une exclusion et ne pas relancer le même pilote. Le vérificateur
nouveau `ribbon_six_matching.py` contrôle seulement notre classification
de triangles et notre certificat ; la dépendance LAB est explicite.

**Exploitation de la nouvelle preuve reçue — note 239 :** le texte fourni
par l'utilisateur exclut les rubans six nus et à une corde, via des
fonctions propres de valeur trois et une obstruction arithmétique au bord.
Son mécanisme est étendu aux ensembles de cordes ayant un sommet commun.
Une étoile de cordes centrée sur un sommet latéral est toujours impossible,
même avec plusieurs cordes. Si le sommet commun est un centre c_0, seules
deux formes restent nécessaires à symétrie près : {c_0a_4,c_0b_3} et
{c_0c_2,c_0c_4}, exactement deux cordes. Ces formes ne sont pas déclarées
réalisables. Preuve par une forme 2×2, les budgets locaux et des sommes
entières ; certificat standard-library dans `ribbon_six_star.py`.
Ce résultat suppose les dix-huit sommets distincts, ne force aucun ruban
six, et donne une nouvelle coupe conditionnelle : pour chaque sommet
latéral du ruban, au moins une corde ne lui est pas incidente. Ne pas
reprendre l'audit de la preuve reçue ; exploiter les répartitions de cordes
restantes. Le fichier `verify_ribbons.py` de l'autre session n'a pas été
fourni ni exécuté ici.

**Suite à la demande directe de poursuivre — note 238 :** chaque fenêtre
de huit centres avec rôles distincts impose au moins deux arêtes latérales
supplémentaires, même avec un graphe de centres arbitraire. Preuve locale
complète : deux types à six centres, un exclu par moments ; six types
nécessaires avec une seule arête latérale à sept centres ; leur recouvrement
laisse quatre supports à huit centres, tous exclus spectralement par
témoins entiers. Les 68 vecteurs de couverture et certificats sont archivés.
Une identification impose elle aussi au moins deux adjacences supplémentaires
entre rôles. Ainsi tout cycle de transport de longueur m≥10 a au moins
ceil(m/4) paires de rôles latérales supplémentaires dans ses fenêtres de
huit centres, identifications comprises. Ces paires ne sont pas autant
d'arêtes physiques distinctes de C1. Le raccord à une contrainte obligatoire
sur chaque cycle long est obtenu ; une borne supérieure contradictoire et
l'exclusion des assemblages restants manquent encore. Aucun rang ni noyau
global fermé. Ne pas refaire la classification : exploiter les types
restants à au moins deux écarts et leurs recouvrements.

**Résultat de pair reçu au message 473, piste arithmétique distincte :**
LAP annonce, via LAB, `[M:Lambda_L]=3^(e3−1)` et
`M/Lambda_L ≅ F3^(e3−1)`, où Lambda_L est engendré par les 231 vecteurs
triangulaires et `e3=99−rang_F3(N)`, avec `1≤e3≤22`. Source annoncée :
`conway99-c2-aws`, commit `9ca72369f`, note mandat C §10 ; preuve à la main
rapportée, non auditée ici. Conséquence annoncée directement pertinente
au dossier : `2h_H=Σ huit w_T` entraîne `h_H∈Lambda_L`, car le quotient
n'a pas de torsion deux. Cela donne une combinaison entière de triangles
globaux ; aucune expression à coefficients bornés ni exclusion n'est fournie.
Ce résultat n'intervient pas dans la preuve de la note 237.

**Nouvelle exclusion de famille, note 237 :** un ruban fermé dont les
3m rôles sont distincts et dont les seules arêtes supplémentaires relient
des centres a nécessairement m≤8. Preuve théorique : les moments des deux
côtés donnent m≤15 ; pour 9≤m≤15, la positivité spectrale exige une
corrélation entre centres plus négative que ne l'autorisent leurs ensembles
de voisins indépendants dans le cycle des indices. Un polynôme à cinq
coefficients de Bernstein positifs certifie l'inégalité. Aucun balayage.
Cela traite tous les graphes d'arêtes entre centres, et prolonge la piste
LAB du message 472. Tout cycle de transport de longueur ≥9 doit donc
avoir une identification de rôles ou une arête supplémentaire touchant
un sommet a ou b. Les cycles comportant ces réparations restent ouverts ;
aucun cycle quatre n'est forcé et aucun rang global n'est exclu.

**Autres apports LAB au message 472 :** classifications annoncées des
fenêtres à cinq centres avec une seule relation supplémentaire ; cycles
6,7,8 nécessitant au moins deux relations. Résultats de pair conservés
avec leur portée, sans audit en double. Sa restriction calculée sur les
seules cordes de pas quatre est désormais couverte par la note 237.

**Exploitation concrète du dossier — note 236 :** les trois bords avec
exception donnent 95 étoiles de 24 sommets. Leurs moments restent tous
faisables. Deux choix entiers de bord du premier cas Cube sont en revanche
exclus par des certificats d'arêtes partagées : la même arête doit servir
aux deux extrémités. Ces certificats sont relevés en deux inégalités
linéaires exactes valables pour tous les choix de ce cas. Ce sont des
outils de réduction ; ni une étoile entière, ni un des cinq bords, ni un
rang n'est encore exclu. Ne pas relancer les 95 LP individuels. La cible
est une obstruction uniforme sur les arêtes, pas un compte d'affectations
rejetées. Aucun calcul Codex de cette étape ne reste en cours après son bilan.

**Transport, résultat de pair reçu au message 470 :** LAB annonce
l'exclusion des deux rubans fermés propres de longueur six par certificats
exacts (commit `da1282e`). Les longueurs propres fermées restent donc 3,4,5.
Il annonce aussi l'impossibilité d'un segment ouvert propre à cinq centres.
Ne pas refaire cet audit : les cycles longs comportant des identifications
ou arêtes supplémentaires restent à étudier, et aucun cycle quatre n'est
forcé dans tout C1.

**Dossier Convergences fourni directement par l'utilisateur — note 235 :**
le théorème extérieur de saturation par témoins de bord est exploité,
sans refaire ses campagnes. Il s'applique au motif obligatoire Makhnev
de six sommets (réseau primitif, projection totale, déterminant 3255,
orthogonal de rang 38). Il s'étend aussi à tout support induit
4-régulier sur douze sommets ; celui-ci ne peut avoir la valeur propre
trois. Enfin deux supports Cube/Wagner ayant le même vecteur h_H
ne peuvent se recouper qu'en au plus trois sommets, suivant quatre
formes explicites. La note et le petit calcul exact associé sont
enregistrés ; aucune exclusion de rang n'est annoncée. LAB explore
en parallèle les cycles longs du transport (message 466), sans audit
en double de nos conséquences.

**Correction de pair reçue au message 464 :** LAB retire sa loi générale
de parité d'holonomie (NOTE 17.85), réfutée par ses exemples de produits
cartésiens ; référence de la correction : commit LAB `9f0b149`, NOTE 17.86.
Ne pas utiliser cette loi. La formule locale `c(Q)=Σ_{e∈Q} c_e (mod 2)`
reste une conjecture selon LAB ; ses conséquences globales ne doivent pas
être présentées comme des théorèmes sur cette base. Les notes 232–234
n'utilisent aucune de ces assertions. Correction enregistrée sans
nouvelle campagne de vérification et sans réponse d'accusé aux pairs.

**Dernier lemme sans rang — note 234 :** autour de chaque quadrilatère,
chacun des deux graphes sur les vingt voisins simples des coins opposés
est connexe. Preuve par parité, déficits et moments entiers des degrés
extérieurs ; aucun solveur. Cette restriction locale ne ferme aucun rang
global ni C1. Le modèle des quarante voisins simples n'est 5-régulier
que si les quatre troisièmes points sont appariés par deux arêtes.
Voir `RECHERCHE_A_REDUCTION_STRUCTURELLE.md` pour la piste et ses limites.

**Reprise directe de la recherche par l'utilisateur, après le message 455 :**
« bah tente de la resoudre cette etape alors pourquoi t'arreter ».
La suspension conservatoire ci-dessous est donc historique. Continuer
sur le verrou binaire et les lemmes de reconstruction, sans reprendre
les anciens balayages par inertie. Fichier propre à cette piste :
`RECHERCHE_A_REDUCTION_STRUCTURELLE.md`.

**Résultats nouveaux, notes 232–233 :** à boule générique et 60 ombres
fixées, une complétion de rang 37 est unique parmi tous les rangs.
Deux complétions distinctes des mêmes ombres ont par ailleurs une
différence de rang au moins cinq sur F7 ; le cas (39,39) est donc
impossible lorsque le bloc proche est inversible. La première preuve
est théorique ; la seconde utilise une classification exacte de petites
différences et des certificats rationnels. Ces unicités ferment des
cas de coexistence, pas les rangs globaux 37 ou 39, ni les 174 noyaux.
Ne pas reprendre les résidus (37,41), (37,43) ou (39,39) à données
fixées comme des sous-problèmes encore ouverts dans ce cadre.

**État au 9 octobre, message LAB 450 (05:09 UTC) : nouveaux calculs
suspendus par précaution.** LAB rapporte avoir reçu directement de
l'utilisateur une demande d'arrêter les calculs et avoir arrêté ses
processus à 05:08 UTC ; il a transmis la demande à LAP. Ce message est
un relais de pair, pas une instruction reçue directement dans la session
Codex. Aucun calcul de recherche lancé par Codex ne reste actif. Conserver
les résultats et ne relancer aucun calcul sur une simple notification du
pont ; attendre une nouvelle instruction explicite de l'utilisateur.
Dernier état LAB rapporté : balayage principal (4,8) achevé ; torsion un
arrêtée à 2792 cas sur 15 462, tous exclus ; vérification complète des
isomorphismes non démarrée. Ce point partiel ne clôt pas la torsion un.

**Priorité explicite réaffirmée par l'utilisateur le 9 octobre : exploration,
nouveaux lemmes et théorèmes de réduction.** Alléger les vérifications et
cesser les audits en double. Appliquer `AGENTS.md` ; ne pas attendre une
nouvelle contre-vérification pour exploiter un résultat disponible. Cette
consigne est persistante et remplace les anciennes priorités de validation.

Demande de l'utilisateur : rechercher des voies vers C1 autres que
l'exclusion successive des rangs. Les anciennes campagnes de relecture
des quatre boules de calibration ne sont plus la priorité.

**Cible active : prolongements d'un motif obligatoire, sans rang modulo 7.**
Tout graphe de Conway contient deux triangles reliés par exactement
deux arêtes (Makhnev). Ce motif impose un noyau de 14 sommets.
La note 221 en donne une couverture exhaustive de 373 types enracinés,
dont 63 sont exclus par des certificats entiers de positivité réelle.
La note 222 impose ensuite les incidences simultanées des 85 sommets
extérieurs et exclut 136 noyaux supplémentaires, avec certificats entiers.
Il reste **174 noyaux**, admissibles aux seuls tests appliqués, pas des
graphes complets ni des instances à coût maîtrisé.

**Implication finale :** si aucun des 174 noyaux ne se prolonge en un
SRG(99,14,1,2), C1 est exclu, tous rangs confondus. Aucune hypothèse
de généricité, d'absence de prismes ou d'involution n'est utilisée.

**Nouveau lemme sans rang (note 225) :** les composantes visibles dans
chaque noyau imposent, par regroupement de leurs poids, les tailles
possibles des composantes autour de chacun des deux triangles. Cela
borne le nombre de grilles passant par ces triangles : 20 types imposent
zéro grille pour les deux, et 59 pour au moins l'un. Si tous les triangles
d'un candidat appartiennent à au moins q grilles, la couverture se réduit
à 115, 52, 11 ou 2 types pour q=1,2,3,4 ; q≥5 est impossible.
Ces réductions sont conditionnelles : les 174 types restent ouverts
sans hypothèse supplémentaire sur les grilles.

**Prochaine cible d'exploration :** tirer une obstruction des profils de
composantes imposés, ou des deux seuls noyaux du sous-cas où chaque
triangle appartient à au moins quatre grilles (identifiants 0 et 1).
Relier ces profils aux familles étudiées par LAP en gardant leurs
hypothèses de rang. Ne pas convertir cette piste en nouvelle mission
de reproduction des résultats précédents.

**Exploration complémentaire achevée (note 226, messages LAB 425–431) :**
les différences propres de masse neuf sont nécessairement binaires.
Dans la composante à neuf points et quatorze arêtes, les supports de
même projection sont disjoints et leurs classes ont taille au plus trois.
Une sous-collection de sommes 0,+3,−3 supprime les changements de somme ;
tous ses canaux restants sous P=0 sont maintenant majorés (masses 7,8,9).
Ces majorations sont trop larges pour déduire « rang 37 implique P>0 ».
Ne pas demander une certification supplémentaire des plafonds numériques
loin de la cible. L'obstacle est la fréquence des paires de supports de
même projection, pas un canal à ignorer ni un résultat ancien à réauditer.

**Obstacle franchi ensuite (LAB 433, note 227) :** deux moulins pondérés
distincts ne peuvent jamais avoir la même projection, sans hypothèse de
rang ou P=0. Codex en déduit des classes cubiques/moulins de taille au plus
quatre et une nouvelle forme C8 sans le terme constant de 8 981 280.
Utiliser désormais `data/codex_mass8_no_twin_mills.json`, qui remplace
la borne C8 de la note 226. Les canaux moulin–cubique restent comptés.

**Nouvelle réduction pour ces derniers (note 228) :** ils équivalent
à une relation positive de noyau de profil (2,1^16). Le support de
17 sommets force les profils et effectifs de ses 82 points extérieurs.
Sous P=0, il reste 359 types de supports nécessaires (29,122,208 selon
le cubique). Les premières contraintes spectrales n'en éliminent aucun.
Ce sont des types de relations moulin–cubique, pas une nouvelle liste
de candidats C1 remplaçant les 174 noyaux. Chercher une obstruction sur
les arêtes entre profils forcés, ou un théorème imposant une grille
dans le support positif ; ne pas relancer les mêmes tests spectraux.

**Suite structurelle (LAB 437, note 229) :** le diagnostic couplé de LAB
confirme que les bornes de collisions restent trop larges. Ne pas relancer
une optimisation des seuls coefficients ni certifier ces plafonds éloignés.
L'anticomplétude de supports positifs propres de valeur trois impose déjà
leur projection normalisée ; leur antivoisinage Z a rayon spectral ≤3.
Les composantes cubiques de Z ont taille multiple de huit : 8 ou 16
pour un cubique huit, 8,16 ou 24 pour un moulin. Un partenaire moulin
force le profil extérieur (23,48,20) du cubique ; tout degré extérieur
≥3 interdit ce partenaire. Leur reste commun R a exactement seize points
et rayon spectral ≤3. La note 229 donne aussi des interdictions de degrés
et triangles dans Z. Ce sont des restrictions de partenaires, pas une
nouvelle exclusion de noyaux C1. Le pilote des nouvelles équations
d'arêtes entre cellules laisse ses cinq entrées ouvertes ; ne pas
l'étendre automatiquement ni le présenter comme une avancée d'exclusion.

Une autre piste porte sur les 33 sommets sans voisin dans le
motif initial et les six classes restantes (52 sommets au total),
avec les degrés et voisinages communs exacts de la note 221 §4.
Chercher une obstruction uniforme ou une réduction démontrée des
prolongements. Une liste de tests supplémentaires sur des exemples
déjà exclus ne remplit pas cette cible. Le premier modèle de multiplicités
est terminé sur les 310 entrées (22,4 secondes) ; ne pas le relancer comme
nouvelle avancée. Les premiers pilotes de fermeture et de paires de LAB
n'ont rien exclu de plus ; les 15 pilotes Codex avec multiplicités entières
et coexistence par paires ont tous un témoin nécessaire (note 223).
Ne pas approfondir automatiquement ces campagnes, ni retourner aux quatre
boules déjà exclues pour y compter des types sans théorème de couverture.

**Comptage global tenté :** compatibilité des noyaux autour de tous
les motifs S d'un même graphe. Le catalogue impose e(D(S))≤4 et
61≤e(C(S))≤65 pour chacun. LAB a incorporé les équations de types jusqu'à
l'ordre 10 à son recensement (message 416) : aucune exclusion supplémentaire
rapportée. Le comptage seul n'a donc pas clos la voie ; tout nouveau pilote
doit apporter une relation supplémentaire, pas répéter cette relaxation.

**Résultat disponible à exploiter :** LAP annonce l'exclusion de tous les
voisinages de droite déconnectés sans triangle ni carré au rang 37.
La note 224 valide la réduction algébrique, reproduit la classification
des composantes et les deux étapes finales du cas de torsion maximale.
Elle distingue les calculs indépendamment reproduits des grands balayages
encore repris des archives LAP. La contre-vérification supplémentaire du
témoin (0,0) a été annulée par message 420 suivant la nouvelle instruction
explicite de l'utilisateur. Ne pas la relancer. Exploiter le résultat de
LAP avec ses hypothèses et sa portée, et chercher les lemmes suivants.
Ce résultat annoncé ne ferme pas le rang 37 et ne réduit pas directement
les 174 noyaux. Il porte sur une famille distincte des quatre anciens exemples.

**Avancée rapportée ensuite par LAP (message LAB 442, 9 octobre, 01:03 UTC) :**
dans sa campagne au rang 37 sous P=0, le profil déconnecté (4,4,4),
soit trois composantes de douze sommets, est annoncé clos : 275
multi-ensembles traités, 275 exclus, aucun autre résultat. Source annoncée :
`amazing-source/conway99-c2-aws`, commit `784c31c98`, dossier
`c1_rank37_girth5_lines/`, journaux `sweep_222r.log`, `sweep_222r2.log`
et addendum 1 de `NOTE.md`. Statut : preuve assistée par ordinateur
rapportée par LAP ; pas de nouvel audit par Codex. Utiliser ce résultat
avec ces hypothèses, conformément à la priorité d'exploration.
Les profils (6,6) et (4,8), y compris leurs cas de torsion, sont encore
en traitement à cette date. L'énoncé « rang 37 et P=0 implique toute
droite connexe » reste une cible, pas une conclusion. Il n'interdirait
pas à lui seul les paires anticomplètes de cubiques huit du canal C8.
Ne pas relancer une reproduction des 275 recherches ni une campagne
de calcul supplémentaire sur la seule offre de processeur du message.

**Rectification LAP transmise par LAB 443 (03:40 UTC) :** l'annonce
de trois boules de torsion quatre exclues dans le profil (4,8) est
retirée. Des processus orphelins réécrivaient les fichiers d'instances
des nouveaux calculs, produisant de fausses sorties sans candidat.
LAP a jeté ses journaux agrégés de torsion trois et quatre et relancé
ces séries ; la correction de noms par PID est annoncée au commit
`8f6c57732`, avec `run_both` de `fastlib.py` encore signalé par LAB.
Ne pas compter ces résultats retirés comme acquis. Le profil (4,4,4)
reste annoncé clos ; (6,6) et (4,8) restent en cours. L'énoncé B local
« rang 37 et aucune arête de T dans un prisme implique G(T) connexe »
est encore une cible. L'offre de CPU et les vérifications annoncées
par les pairs ne déclenchent aucune nouvelle campagne Codex.

**Résultats rapportés par LAB 449 (04:53 UTC) :** le balayage principal
du profil (4,8), au rang 37 sous P=0, est terminé sur 97 896
représentants : 81 380 exclus sans torsion, 16 516 classés TORSION,
aucun autre résultat ni cas manquant annoncé. Ces derniers se répartissent
en 15 462 / 964 / 71 / 19 cas de torsion un / deux / trois / quatre.
Source annoncée : branche LAB, commit `d51ebbd`, dossier
`code/lab_theta_lp_2026-10-08/lap_sweep48/`. Statut : calcul assisté
par ordinateur rapporté par LAB, non reproduit par Codex.

LAP annonce ensuite la clôture de la **reprise propre** des 19 cas de
torsion quatre (19 exclus, commit `1b8b47967`). Ce résultat remplace
le statut ouvert de cette série ; il ne réhabilite pas les anciens
journaux retirés. Les torsions un, deux et trois restent partielles.
Les lignes COMB-ALIVE de torsion deux sont des survivants du seul test
combinatoire : elles attendent le test de rang résiduel, et ne sont pas
des témoins C1. Le profil (4,8) entier n'est donc pas encore clos.

Pour la droite dans six grilles, LAP rapporte une étoile satisfaisant
rang(Y)≤5 et les sommes de lignes nulles. Une étoile seule ne l'exclut
pas ; ce témoin nécessaire ne construit pas un SRG. Aucun nouveau
calcul Codex n'est lancé sur ce seul compte rendu.

**Piste de complétion connexe (note 230, message Codex 444) :** sous
rang₇(3I−G)=35, soixante ombres binaires de moments exacts K et de
produits de Green admissibles déterminent F. Son nombre d'arêtes vaut
240+7q, q≥0. Au seuil 240, toutes les équations SRG entières se ferment
automatiquement et le rang global est 37. Chercher une obstruction
binaire uniforme ou une borne de coût ≥247 dans les classes encore
ouvertes. Ne pas présenter cette équivalence comme une exclusion,
ni relancer les quatre boules anciennes pour la tester.

**Filtre acquis à réutiliser, pas résultat nouveau (LAB 445, Codex 446) :**
L23 de `notes/102_FORME_BETA_SIGNE.md`, écrit le 25 septembre, impose
au rang 37 sans torsion τ(G)∈{3,5,6} modulo sept. Les valeurs {1,2,4}
sont déjà exclues ; dans la formulation 230 elles imposent q≥1 et un
coût ≥247. Les écarter avant toute recherche de sélection. τ=0 sort
du modèle sans torsion. Ne pas annoncer comme nouvelle avancée le
critère retrouvé, ni un « facteur deux » global sur la foi d'échantillons.
Le lemme de discriminant proposé au message 445 correspond à la forme
globale déjà établie dans la note 102 ; ne pas relancer son audit.
Pour deux composantes sans torsion, la norme résiduelle a classe τ₁τ₂ :
une seule classe scalaire suffit dans un futur modèle, sans reprendre
les balayages historiques qui en traitaient deux.

**Suite théorique (LAB 447, Codex 448, note 231) :** la complétion de
Witt fixe le discriminant résiduel à partir de M₀ et de la dimension
des relations vraies. Au rang 37, si d=dim ker M₀ et b=dim Tr, le
résidu a dimension 2b−d et discriminant de classe 3d₀(−1)^(d−b).
Un mauvais signe en dimension zéro élimine tous les Tr de cette
dimension ; en dimension positive, une seule classe de forme reste
possible. Aucun nouveau décompte de boules exclues n'est annoncé.
Dans le modèle sans torsion de la note 230, l'identité de déterminants
χ_(NᵀM⁻¹N)=x²⁶(x−6)χ_(H|E) montre que toutes les identités de traces
sont déjà conséquences de NNᵀ=K. Ne pas calculer les moments suivants
comme des contraintes nouvelles pour cette sélection complète.
Les 150 exemples connexes annoncés morts par LAP sont un échantillon,
pas une couverture. Pour l'avancement des séries relancées de torsion,
utiliser la mise à jour LAB 449 ci-dessus.

Sources de travail :

- `notes/220_CODEX_ROUTES_HORS_RANGS.md` : comparaison des routes A/B/C
  de C2, alternatives pour C1 et raisons du choix ;
- `notes/221_CODEX_NOYAU_PRISME_DEFECTUEUX.md` : couverture, preuves,
  portée exacte et équations de prolongement ;
- `notes/222_CODEX_PROLONGEMENT_PRISME_MASQUES.md` : 136 exclusions
  supplémentaires par les incidences des sommets extérieurs ;
- `notes/223_CODEX_LIMITE_DES_PREMIERS_PROLONGEMENTS.md` : pilotes sans
  exclusion supplémentaire, témoins exacts, limite et cible suivante ;
- `notes/224_CODEX_AUDIT_LAP_RANG37_MAILLE5.md` : réduction algébrique
  et contrôles indépendants du nouveau sous-cas annoncé par LAP ;
- `notes/225_CODEX_NOYAUX_COMPOSANTES_ET_GRILLES.md` : nouveau lemme
  de regroupement et réductions conditionnelles sans rang ;
- `data/codex_core_component_profiles.json` : profils des deux triangles
  et listes de noyaux pour chaque sous-cas de couverture par des grilles ;
- `notes/226_CODEX_MASSES789_SANS_PRISME.md` : lemme de masse neuf,
  nouveaux canaux et limite des premières majorations complètes sous P=0 ;
- `notes/227_CODEX_C8_SANS_DOUBLES_MOULINS.md` : lemme de LAB et
  amélioration effective de C8 par Codex, sans coût forfaitaire des moulins ;
- `notes/228_CODEX_MOULIN_CUBIQUE_NOYAU17.md` : réduction positive
  et 359 types nécessaires avec profils extérieurs forcés ;
- `notes/229_CODEX_PARTENAIRES_ET_ANTIVOISINAGES.md` : confinement
  spectral, divisibilité des partenaires, profil mixte forcé et pilote
  d'arêtes sans exclusion supplémentaire ;
- `notes/230_CODEX_COMPLETION_BINAIRE_SEUIL240.md` : critère suffisant
  de complétion par soixante ombres binaires et seuil exact d'arêtes ;
- `notes/231_CODEX_SIGNE_RESIDUEL_ET_TRACES.md` : filtre des formes
  résiduelles et dépendance de toutes les traces aux moments d'incidence ;
- `code/codex/twisted_prism_core.py` et
  `data/codex_twisted_prism_core.json` : catalogue et certificats initiaux ;
- `code/codex/twisted_prism_extension.py` et
  `data/codex_twisted_prism_extension.json` : prolongement et certificats.

Deux voies restent en réserve : les plans binaires à trois couches,
et un argument extrémal par transformations préservant le SRG.
La seconde n'a pas encore de mécanisme général démontré. La fenêtre
des rangs reste disponible comme outil secondaire, sans organiser
à elle seule la recherche.
