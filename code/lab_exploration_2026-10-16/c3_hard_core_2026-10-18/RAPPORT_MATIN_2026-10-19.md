# Rapport du matin, 19/10/2026 (LAB et Codex) — brouillon mis à jour au fil de la nuit

## Faits vérifiés

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

## En cours

- **Famille universelle K3** (Codex) : paire partagée forcée, Q_bc grille, triangle de grilles. Elle contient **261 gabarits
  ouverts**, dont 74 durs.
- **Ensuite, la famille universelle P3** (deux grilles qui partagent une droite) : **821 gabarits ouverts**. Si elle tombe,
  c = 3 est presque vide.

## État à 03 h UTC

- **Famille K3 universelle.**
  - Codex a ajouté deux contradictions à la main sur les cœurs : les orbites 20 et 23 tombent par le lemme des 4 facteurs
    de Q12. J'ai vérifié ce lemme de mon côté, de façon indépendante.
  - L'énumération exacte à 24 sommets exclut tous les bords testés : les 2 000 premiers du cœur 0.
  - Le goulot est le temps CPU : 255 318 bords pour le seul cœur 0, sur un PC chargé par VALORANT et Medal laissés ouverts.
    La production complète demande plusieurs heures en local, mais quelques minutes sur AWS.
- **Front LAB des 17 gabarits sans paire.**
  - Les paires de grilles fermées donnent des égalités C2 exactes : 456 solutions par paire, 2 176 pour le triangle de 9302.
  - Pas encore de contradiction.

## À faire au réveil

- **Reconnexion AWS** (code du téléphone), puis `bash morning_sync.sh` dans le dossier aws_c1. Le script rapatrie les runs
  de la nuit et recalcule le registre.
- **Lancer la production K3 de Codex en Spot** (paquet en préparation, quelques minutes de calcul). Si la couverture est
  complète et le manifeste valide : créer `k3u_closed.json` (commit et manifeste) et relancer le registre, ce qui retire
  261 ouverts.
- Puis la famille P3 (821 ouverts) : les formes normales sont prêtes (`p3family_normal_forms.json`).
- **Coûts.** Octobre : 52 USD d'usage selon Cost Explorer, couverts par les crédits (avec un jour de retard).
  Consommation Spot de la nuit estimée entre 10 et 15 USD. Solde à vérifier dans la console.
