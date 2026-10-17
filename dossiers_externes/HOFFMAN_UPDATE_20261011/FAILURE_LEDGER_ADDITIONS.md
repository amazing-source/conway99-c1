# Ajouts au registre d'échecs et de résultats

## HOF-001 — Bords C22 de la coclique de taille 22
Statut : CLOSED-SUBCLASS, preuve assistée par calcul reproductible.
Hypothèse : design 2-(22,4,2) invariant par une translation transitive sur 22 points.
Portée : toutes les complétions du graphe, même non invariantes.
Résultat : zéro complétion ; 72 designs normalisés après huit rejets locaux.
Réouverture : seulement erreur de preuve, d'énumération ou changement explicite de l'hypothèse de bord. Ne pas refaire un SAT à graphes cycliques pour les mêmes données.

## HOF-002 — Bords C7⋊C3, un point fixe et 21 points réguliers
Statut : CLOSED-SUBCLASS, preuve assistée par calcul reproductible.
Portée : idem, pas de symétrie imposée à D.
Résultat : 199 designs nécessaires réfutés, après 37 rejets locaux. Action C21 analogue déjà impossible pour des blocs distincts.
Réouverture : autres actions sur les points, ou erreur vérifiée. Le cas général des designs n'est pas fermé.

## HOF-003 — « Une structure extrémale de Hoffman empêche l'asymétrie »
Statut : INVALID-GENERAL-INFERENCE.
Contre-exemple : SRG asymétrique(25,12,5,6) avec trois cocliques de Hoffman. La transformation complémentaire conserve même tout un bord de Hoffman commun à Paley et au graphe asymétrique.
Information correcte : l'unicité d'une complétion force les symétries du design à se prolonger ; la présence du design ne le fait pas.

## HOF-004 — « Le design BvLS a une seule complétion, donc tous les SRG243 à coclique45 sont BvLS »
Statut : NON-DEMONSTRATED-GENERALIZATION.
Le calcul de Claude traite un design fixé. Une classification de tous les designs compatibles, ou un argument indépendant, serait nécessaire pour la conclusion générale.

## HOF-005 — Spectre extérieur et design de l'alpha22
Statut : ALREADY-KNOWN-IN-CORPUS.
Sources : note94 §3.2 et note104 annexe. YYᵀ=12I+2J, pas18I+2J. Le spectre extérieur n'est pas une nouveauté de ce dossier.

## HOF-006 — α22 général
Statut : OPEN / COMPUTE-UNDECIDED selon les journaux du dépôt lus ici.
Les classes de designs HOF-001 et HOF-002 sont exclues, mais rien ne force un design de bord arbitraire à leur appartenir. Pas de borne universelle α≤21 établie ici.
