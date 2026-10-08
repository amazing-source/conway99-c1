# Recherche active C1 — changement de cap du 9 octobre 2026

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

Le prochain travail porte sur les 33 sommets sans voisin dans le
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

**Cible théorique suivante :** compatibilité des noyaux autour de tous
les motifs S d'un même graphe. Le catalogue impose e(D(S))≤4 et
61≤e(C(S))≤65 pour chacun. Chercher un double comptage de la somme des
e(D(S)) ou des types, avec une relation supplémentaire propre aux paramètres
de 99. Ce sous-problème est proposé à LAB ; aucune contradiction par ce
comptage n'est acquise. La route reste révisable selon les résultats.

Sources de travail :

- `notes/220_CODEX_ROUTES_HORS_RANGS.md` : comparaison des routes A/B/C
  de C2, alternatives pour C1 et raisons du choix ;
- `notes/221_CODEX_NOYAU_PRISME_DEFECTUEUX.md` : couverture, preuves,
  portée exacte et équations de prolongement ;
- `notes/222_CODEX_PROLONGEMENT_PRISME_MASQUES.md` : 136 exclusions
  supplémentaires par les incidences des sommets extérieurs ;
- `notes/223_CODEX_LIMITE_DES_PREMIERS_PROLONGEMENTS.md` : pilotes sans
  exclusion supplémentaire, témoins exacts, limite et cible suivante ;
- `code/codex/twisted_prism_core.py` et
  `data/codex_twisted_prism_core.json` : catalogue et certificats initiaux ;
- `code/codex/twisted_prism_extension.py` et
  `data/codex_twisted_prism_extension.json` : prolongement et certificats.

Deux voies restent en réserve : les plans binaires à trois couches,
et un argument extrémal par transformations préservant le SRG.
La seconde n'a pas encore de mécanisme général démontré. La fenêtre
des rangs reste disponible comme outil secondaire, sans organiser
à elle seule la recherche.
