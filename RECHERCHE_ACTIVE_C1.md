# Recherche active C1 — changement de cap du 9 octobre 2026

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
- `code/codex/twisted_prism_core.py` et
  `data/codex_twisted_prism_core.json` : catalogue et certificats initiaux ;
- `code/codex/twisted_prism_extension.py` et
  `data/codex_twisted_prism_extension.json` : prolongement et certificats.

Deux voies restent en réserve : les plans binaires à trois couches,
et un argument extrémal par transformations préservant le SRG.
La seconde n'a pas encore de mécanisme général démontré. La fenêtre
des rangs reste disponible comme outil secondaire, sans organiser
à elle seule la recherche.
