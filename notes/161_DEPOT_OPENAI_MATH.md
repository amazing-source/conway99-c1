# 161 — Exploration du dépôt openai/math (07/10, en cours)

*Demande de l'utilisateur : (1) y chercher tout ce qui peut servir pour Conway ; (2) étudier comment le modèle raisonne
(dossier `reasoning_traces/`). Le dépôt est cloné en lecture seule hors de ce dépôt (`/home/user/openai/math`, commit
adc7f1241, 3,1 Go, 132 851 fichiers). Tout son contenu est traité comme des données, pas comme des instructions.*

## Ce que contient le dépôt
- **722 manuscrits produits par un modèle interne d'OpenAI**, regroupés en 372 familles et 17 disciplines.
- **Procédure déclarée** (README) : environ 4 000 problèmes posés, en moyenne 3 h de calcul « ChatGPT Pro thinking » par
  résultat. Il y a un tri par significativité. Le taux de résultats retenus est donc d'environ 372 familles pour
  4 000 problèmes.
- **Vérification hétérogène.** Une partie est formalisée en Lean (`lean/formalization.yaml`, défis Comparator), le
  reste ne l'est pas. Le README prévient que les résultats non formalisés « could have issues ».
- **Traces de raisonnement abrégées** pour 10 familles (`reasoning_traces/`, environ 90 000 mots).

## Riemann : ce qui est annoncé exactement
- Famille 003, « The quasi-Riemann hypothesis » : ζ et toutes les L-fonctions de Dirichlet n'ont aucun zéro dans
  Re s > 7/8. Une preuve compagnon donne 11/12.
- C'est l'hypothèse **quasi**-Riemann (un demi-plan fixe Re s > θ avec θ < 1), pas l'hypothèse de Riemann (θ = 1/2).
- Énoncé Lean du défi : `riemannZeta_ne_zero_of_seven_eighths_lt_re` (`lean/ComparatorChallenges/QuasiRiemannHypothesis.lean`),
  portant sur le `riemannZeta` de Mathlib.
- La formalisation est annoncée ; nous ne l'avons pas recompilée.

## Recherche directe sur Conway
- **Aucun manuscrit** ne mentionne Conway-99, srg(99,…), les graphes de Moore, les graphes distance-réguliers ou le
  code de Golay.
- « Strongly regular » n'apparaît que deux fois, et hors sujet : l'historique de Borsuk (Bondarenko, Jenrich–Brouwer)
  et des « strongly regular semisimple » en théorie des représentations.
- **Candidats de technique transférable**, en cours de lecture :
  - conjecture des matrices de Hadamard circulantes (non-existence d'un objet combinatoire structuré) ;
  - certificats de Fourier exacts pour les matrices de Hadamard complexes d'ordre 6, et nombre maximal de bases
    mutuellement non biaisées en dimension 6 (non-existence par certificats) ;
  - Sidorenko (schémas d'association) ;
  - Ryser (plans projectifs) ;
  - Borsuk en dimension 9 (ensembles à deux distances) ;
  - Snaky (grand calcul fini certifié).

## Suite
Synthèse des deux lectures (techniques transférables ; habitudes de raisonnement) à ajouter ici dès qu'elles sont
terminées.
