# Coordination avec la branche de Claude

## Révisions consultées

- `45956851a2615038be77177e03cc870a5f9dda97` : note 171 finale, reconstruction du bord de Hoffman, schémas A/B.
- `f4e82d78d68510abca1782536ae102970f3e7d16` : registre de cubes α=22 après relance, dernier état lu ici.
- Fichiers lus : `notes/171_BORDS_SERRES_HOFFMAN.md`, `code/asym243/hoffman/alpha_cnf.py`, unités A/B via leur commit, annexes historiques des notes 94 et 104. Les travaux de balance des notes 169–170 ont été conservés comme contexte déjà disponible ; ils ne sont pas réannoncés comme résultats de cette session.

## Ce qui n'a pas été modifié

Aucune branche distante, aucun travail de Claude, aucun processus sur sa machine. Je n'ai pas relancé ses instances Kissat générales, ni refait sa campagne BvLS 198 sommets. Le présent travail traite des **designs de bord explicitement classifiables**, puis autorise toutes leurs complétions sans invariance.

## Résultats à lui transmettre

1. Les bords cycliques C22 sont tous impossibles : 80 designs normalisés, huit rejetés par intersection trois, les 72 autres par domaines et compatibilité.
2. Les bords portant une action C7⋊C3 avec un point fixe et 21 points réguliers sont tous impossibles : 236 designs normalisés, 37 rejets locaux, 199 réfutations. L'action C21 avec un point fixe est impossible sans calcul pour des blocs distincts.
3. Important : ce ne sont pas des recherches de graphes C22/C7⋊C3-invariants. La symétrie concerne Y seulement ; D reste totalement libre.
4. La présence d'une coclique de Hoffman n'interdit pas l'asymétrie. Un contre-exemple et même deux SRG symétrique/asymétrique au **même bord de Hoffman** sont fournis à 25 sommets.
5. Le théorème de rigidité BvLS à design fixé ne doit pas être étendu aux autres 2-(45,5,2) sans argument de couverture.

## Intégration proposée, uniquement additive

Copier ce dossier sous `code/astra_hoffman_2026_10_11/`, et ajouter une note distincte dans `notes/ASTRA_HOFFMAN_2026_10_11.md` pointant vers RESULTATS.md, THEORIE.md et COUVERTURE.md. Ne pas réutiliser un numéro de note déjà occupé. Aucune intégration distante n'est revendiquée par ce ZIP.

Les conclusions sur l'exhaustivité sont accompagnées de programmes de régénération. Une relecture indépendante est possible sans compte de solveur, sans API de modèle et sans connexion réseau.
