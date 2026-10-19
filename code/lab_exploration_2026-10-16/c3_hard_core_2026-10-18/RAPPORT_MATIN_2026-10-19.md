# Rapport du matin, 19/10/2026 (LAB et Codex)

## En bref (05 h 05 UTC)

1. **La famille K3 universelle est FERMÉE.**
   - Les 2 742 342 bords sont exclus et 322 preuves RUP sont contrôlées. Statut : calcul exact, sous E3.
   - **Registre c = 3 : 1 163 → 902 ouverts** (sur 10 052). Commit main 404dc96b :
     https://github.com/amazing-source/conway99-c1/commit/404dc96b71f8bbc0f6fd92d4a305e3b6f89f3590
2. **La nouvelle famille 2K2 est FERMÉE** (365 ouverts après K3). Statut : calcul exact.
   - Étape 1 (sans Q12) et étape 2 (avec Q12, SAT exact) laissent 7 raccordements sur 5 bords, sur 12 569 bords.
   - Codex les réfute tous par ses coupes de continuation, avec preuves RUP vérifiées. Le dernier est contrôlé par
     drat-trim (s VERIFIED, aucun RAT). Commit Codex 44a95e8a.
   - Mon assembleur (`twostage_manifest.py`) donne `complete = true`.
   - **Registre c = 3 : 902 → 537 ouverts.** Commit main eb32ad91 :
     https://github.com/amazing-source/conway99-c1/commit/eb32ad9110db9deaadc6fa9675e8872562d75f90
   - **Relecture indépendante (agent adversarial, terminée) : aucun défaut de correction.**
     - Toutes mes exclusions sont refaites avec un code et un solveur différents (CryptoMiniSat), avec les mêmes résultats.
     - Les deux transports de Codex et le bord core51/b702 sont confirmés.
   - **Les coupes de Codex sont maintenant justifiées.** Les 4 raccordements concernés n'utilisent que deux lemmes de
     coupe.
     - Codex a écrit leur preuve complète à partir des axiomes SRG (`notes/PREUVE_COUPES_CONTINUATION_2026_10_19.txt`,
       main 798c7e20).
     - Contrôle positif sur 4 blocs de vrais srg(243) : les coupes préservent toujours la vraie complétion.
     - Il reste à faire relire cette preuve par un regard indépendant.
3. **Famille P3 (560 ouverts après K3) : production en cours.**
   - En local depuis 03 h 40 UTC : environ 180 tâches sur 1 233 sont faites (7 083 bords couverts sur 68 649), tout est
     exclu.
   - 3 bords étaient restés UNKNOWN au budget de 200 000 conflits (core0 b2373 et b2430, core1 b1161). Tous sont exclus
     par une seconde passe automatique à 3 millions de conflits.
   - Le reste part sur AWS dès ta reconnexion : environ 1 h sur 128 vCPU, quelques dollars.
   - Les vrais résidus éventuels (SAT ou UNKNOWN) iront aux coupes de Codex, comme pour 2K2.
4. **Nouvelle famille P3NB, en production locale depuis 05 h 50 UTC.**
   - Définition : paire partagée forcée, chemin de grilles Y, et une grille « B » par b et la droite libre ; Q_bc
     quelconque. La grille B est couplée parfaitement à une moitié du cœur et aux deux grilles Y.
   - Échantillon : 84 bords sur 84 exclus, environ 0,3 s par bord, soit environ 2 h sur 7 processus pour les 137 454
     bords.
   - Elle couvre **427 des 537 ouverts**, dont 160 hors de P3. Si P3NB tombe : 110 ouverts ; avec P3 et 2K2N : 64.
5. **Si P3 tombe aussi, il reste 250 ouverts en c = 3** (sans compter P3NB).
   - Piste suivante, déjà préparée : la famille 2K2N (même structure que 2K2, mais Q_bc quelconque). Elle couvre 92 de ces
     250.
   - Ses 737 bords survivants ont exactement 1 006 raccordements ouverts, tous des sélections SAT. Ce sont les cibles des
     coupes de Codex (commit 0ef28bf2). Coût probable : quelques heures à 1 jour CPU, moins avec ses réductions par
     symétrie.
   - Remarque de Codex : une fois K3 et 2K2 fermées, avec H01 = −H02 et Q12 grille, les grilles sur les quatre autres
     droites forment une étoile. P3 couvre l'étoile à au moins deux branches.
   - Plan pour ces 250 : `PLAN_250_2026-10-19.md`. Presque tous ont 3 à 5 grilles B/C (couplées parfaitement à une
     moitié du cœur) ; c'est le levier à exploiter.
6. **Plus tôt dans la nuit :** gz 5602 exclu, lemme C4 + C3 (29 ouverts), famille (2, 3) (24 ouverts).
7. **Rien n'est encore acquis sur c ≤ 2.**

## Ce qu'il faut de toi

- **Le code AWS du compte « frere »** : je lance `aws_login_remote_frere.py`, tu colles le code reçu sur le téléphone.
  Ensuite :
  - P3 tourne déjà **en local** depuis 03 h 40 UTC (6 processus à basse priorité). J'arrête ces runs et j'envoie le reste
    en Spot : `remaining_manifest.py`, paquet `p3prod` (tar d350262e), puis `launch_spot_region.sh`.
  - Puis `morning_sync.sh`, qui rapatrie les runs AWS de la nuit et recalcule le registre.
- **Rien d'autre.**

## Faits vérifiés (début de nuit)

1. **gz 5602, dimension 7, exclu par un calcul fini exact**, sans Gram, sans solveur SAT, sous E3. Statut : calcul exact.
   - Preuve de Codex (main cebb050b, `notes/COEUR_HUIT_SOMMETS_5602_2026_10_19.txt`).
   - **Cœur.** Les relations d'étoile donnent H03 = −H12. Les 8 étiquettes Q03 ∪ Q12 induisent alors un graphe cubique, et
     e = 2 est forcé.
   - **Énumération.** On obtient 304 cœurs étiquetés, puis 1 328 bords à 20 sommets.
   - **Jointure à 36.** 888 bords sont exclus par jointure exhaustive et 437 par marges entières ; il reste 3 bords.
   - **Frontière.** Ces 3 bords ont 58 réalisations, toutes tuées : une étiquette manquante n'y a plus aucun voisinage
     possible.
   - **Contre-vérifications LAB.**
     - Cœur 8 refait avec du code indépendant : 304 cœurs exactement.
     - Jointure rejouée sur AWS : mêmes 1 325 exclusions et mêmes 3 survivants.
     - Frontière rejouée en local : les 58 réalisations sont exclues.
2. **Lemme de fermeture C4 + C3, vrai en tout sommet d'un Conway.**
   - Énoncé : si le graphe des grilles contient un C4 sur 4 droites et un C3 sur les 3 autres, les deux diagonales du C4
     sont des grilles.
   - Preuve : les relations universelles Σ_{b≠a} H_ab = 0 donnent H_d1 = −H_d2 ; l'énumération de 5602 n'utilise que le cœur
     et ces 7 grilles.
   - Effet : **29 gabarits c3 ouverts tués** (134 dans le catalogue gz, dont 105 déjà exclus par d'autres méthodes).
3. **Famille (2, 3) exclue : 24 gabarits ouverts.** Statut : calcul exact de Codex (main 7d95ad5e).
   - Structure : paire opposée disjointe, 3 grilles Y, 2 grilles X adjacentes, 2 rectangles X non grille qui se touchent.
   - Calcul : 5 312 positions sans UNKNOWN. 1 748 sont exclues par marges, 3 564 par jointure ; les 18 graphes à 36 sommets
     restants ont tous une frontière vide.
   - Le détecteur LAB retrouve exactement ces 24 gabarits ouverts.
4. **Registre c = 3 : 1 163 ouverts sur 10 052**, contre 1 285 hier à 23 h.
   - Ce chiffre ne compte pas encore les runs AWS de la nuit (c3l2, c3p5, P4E, z_joint complet). Ils sont bloqués par
     l'expiration de la session AWS.

## Ce qui a été compris (la structure commune des survivants)

- **La dimension décide de la survie** : en dimension 6, 93 % des gabarits restent ouverts ; en dimension 4, 3 %.
- **Pourquoi** : les couvertures de Gram explosent avec la dimension. Médiane de 4 Gram en dimension 4, 70 en dimension 5,
  34 688 en dimension 6.
- **Le levier commun, ce sont les colonnes opposées forcées H_A = −H_B.**
  - Elles sont présentes dans presque tous les gabarits ouverts, souvent en plusieurs exemplaires.
  - Chacune impose une structure locale rigide : un cœur cubique si la paire est disjointe, un cœur 2-régulier C8 ou 2C4 si
    elle est partagée.
  - Elle impose aussi des comptes exacts de voisins pour toutes les étiquettes.
  - Les grilles autour du cœur le rendent rigide, et l'énumération exacte conclut.
- **Les gabarits durs (300) sont surtout de type paire partagée.**
  - Le cœur est alors la partie étiquettes d'une composante de taille 2 de G_{l_a}.
  - Catalogue LAB de ces cœurs : 114 cœurs étiquetés, 23 orbites.

## Historique : état à 00 h 45 UTC (02 h 45 locale)

- **Famille K3 universelle.**
  - Codex a ajouté deux contradictions à la main sur les cœurs : les orbites 20 et 23 tombent par le lemme des 4 facteurs
    de Q12. J'ai vérifié ce lemme de mon côté, de façon indépendante.
  - L'énumération exacte à 24 sommets exclut tous les bords testés : les 2 000 premiers du cœur 0.
  - Le goulot est le temps CPU : 255 318 bords pour le seul cœur 0, sur un PC chargé par VALORANT et Medal laissés ouverts.
    La production complète demande plusieurs heures en local, mais quelques minutes sur AWS.
- **Front LAB des 17 gabarits sans paire.**
  - Les paires de grilles fermées donnent des égalités C2 exactes : 456 solutions par paire, 2 176 pour le triangle de 9302.
  - Pas encore de contradiction.

## Détail à 03 h 45 UTC (05 h 45 locale) : K3 fermée, P3 prêt pour AWS, 2K2 presque fermée

- **K3 universelle : FERMÉE (261 gabarits ouverts retirés).** Statut : calcul exact, sous E3 (comme 5602 et T23).
  - Les 2 742 342 bords sont couverts et tous exclus : `family_excluded = true`, 322 preuves RUP contrôlées.
  - Manifeste : l'assembleur de Codex, sans `--allow-partial`.
  - Calcul : 56 tranches de Codex, plus 504 tranches calculées en local cette nuit avec son code 587f1fdd inchangé.
    Mes plages et les siennes forment une partition exacte, vérifiée avant le lancement.
  - **Registre c = 3 : 1 163 → 902 ouverts** (règle K3U activée par `k3u_closed.json`).
- **Nouvelle famille 2K2 (548 ouverts, dont 365 hors K3) : pas encore fermée, résidu très petit.**
  - Définition : une paire partagée forcée H_ab = −H_ac, Q_bc grille, et deux grilles disjointes sur les quatre autres
    droites.
  - Fait utilisé : deux grilles disjointes sont reliées par un couplage parfait. Ce fait est déjà dans l'archive (commit
    hc7 du 18/10) ; la nouveauté est son emploi ici. Le couplage crée un troisième voisin commun interdit pour des paires
    (cœur, grille).
  - **Étape 1, sans Q12 (complète).** Elle exclut 11 832 des 12 569 bords, sans SAT pour l'essentiel.
  - **Étape 2, avec Q12 et SAT exact** (accélérée par un cache exact des raccordements en double).
    - Résidu final : 5 bords et 7 raccordements (core6 b547 : 2 ; core51 b476 : 1, b702 : 1 en UNKNOWN ; core75 b355 : 1 ;
      core88 b618 : 2). Core8 b235 est exclu à la relance complète.
    - Le cœur 6, bord 547, a une sélection de profils satisfiable : la sélection seule ne suffit pas.
    - Mais les **coupes de continuation de Codex** excluent ce raccordement pour tous ses profils (9 clauses, preuve RUP,
      main d8ba1ce0).
  - Suite : Codex applique ses coupes aux 6 raccordements restants. L'assembleur (`twostage_manifest.py --residual
    --certificates`) ne ferme un bord que si chaque raccordement ouvert a un certificat exact.
- **P3 universelle (821 ouverts, dont les 261 K3).**
  - Tous les bords échantillonnés sont exclus par une sélection exacte de profils (SAT avec preuve RUP vérifiée).
  - Coût : environ 105 h CPU avec le cache. Le paquet AWS est prêt pour le réveil : 1 233 tâches, environ 1 h sur
    128 vCPU.
- **Effet attendu sur le registre c = 3.**
  - 1 163 → 902 ouverts : fait (K3).
  - → 342 si P3 se ferme (AWS). P3 est fermé à 100 % sur l'échantillon, mais 2K2 montre que de rares bords
    satisfiables peuvent exister ; seule la production complète tranchera.
  - Rien n'est compté avant les manifestes de couverture complète.
- **Négatif, utile.** Sans Q12 grille (P3N), ou avec une seule grille Y (K2), la sélection de profils devient
  satisfiable sur certains bords. Ces deux hypothèses sont donc nécessaires à la méthode.

## À faire au réveil

- **Reconnexion AWS** (code du téléphone), puis `bash morning_sync.sh` dans le dossier aws_c1. Le script rapatrie les runs
  de la nuit et recalcule le registre.
- **Lancer la production P3 en Spot** : paquet `p3prod` (1 233 tâches, environ 1 h sur 128 vCPU, quelques dollars), puis
  `p3_manifest.py` et la règle P3U du registre.
- **Assembler 2K2** quand les certificats de Codex arrivent, puis la règle 2K2 du registre.
- **Coûts.** Octobre : 52 USD d'usage selon Cost Explorer, couverts par les crédits (avec un jour de retard).
  Consommation Spot de la nuit estimée entre 10 et 15 USD. Solde à vérifier dans la console.
