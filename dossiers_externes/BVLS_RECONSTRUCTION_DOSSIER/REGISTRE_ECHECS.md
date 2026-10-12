# Registre de cette campagne — pas de réouverture implicite des anciens calculs

## B0 — région lointaine de ligne : contrôle, pas nouveauté
La note 165, §7, et le manuscrit du deuxième BvLS traitaient déjà la reconstruction sur 180 sommets. Reproduite : 2 domaines par ligne, 2 complétions exactes. Utilisée pour reconstruire le jumeau et valider le moteur.

## B1 — transposition Paley avec le bord d'une arête : explosion des domaines
Région libre de 200 sommets, bord de 43 sommets. Pour les deux premières lignes, la génération atteint chacune un million de candidats avant épuisement; pour la troisième, elle est interrompue à 20 s après 134 784 candidats. Ces nombres ne sont pas des totaux. La recherche de complétion n'a pas été lancée avec ces domaines incomplets.

Réouvrir seulement avec génération conditionnelle, compression justifiée des domaines ou un autre bord. Ne pas présenter le seuil approximatif de 2 000 candidats d'un ancien pilote comme un plafond exhaustif pour ce problème.

## B2 — libérer un prisme en plus du lointain : CLASSIFIED
BvLS, 186 sommets libres, 16 matrices, exactement BvLS et jumeau à renommage près. Gamma3 au triangle indiqué : 8 matrices, une seule classe Gamma3. Les isomorphismes sont explicitement vérifiés. Ne pas relancer les mêmes instances pour y chercher un nouveau graphe.

## B3 — libérer deux prismes en plus du lointain : CLASSIFIED
192 sommets libres, 27 648 matrices, 2 classes. Couverture de tous les choix équivalents dans BvLS par transports explicites. La génération brute des 192 domaines a été remplacée par celle de 5 représentants puis transport exact; aucun ancien compte interrompu n'est utilisé comme total.

## B4 — libérer 3 paires mates dans une seule couche : CLASSIFIED
186 sommets libres, 2 matrices exactement. Cela ne traite pas trois prismes complets. Les positions libérées importent autant que leur nombre.

## B5 — trois prismes complets : OPEN, diagnostic de premier niveau seulement
Région libre de 198 sommets. Le premier domaine, quotienté uniquement pour cette première décision par les permutations des profils identiques, a 3 645 représentants; l'énumération de cette seule ligne est terminée. Un autre domaine de ligne a 1 895 candidats. Aucune classification de la complétion à 243 sommets n'en découle. Ni SAT global ni UNSAT global n'est revendiqué.

## Hors périmètre
La parité S3, les nouveaux squelettes latins, le recollement sur K_{9,9,9} et le modèle Conway/K11 continuent d'appartenir à l'autre session. Pas de duplication ici. Les notes 169–170 sur la balance ont été consultées pour coordination, pas reprises comme hypothèses de ce constructeur.
