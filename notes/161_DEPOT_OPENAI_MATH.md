# 161 — Exploration du dépôt openai/math (07/10)

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

## Bilan (lectures terminées : notes 161b et 161c)
- **Rien sur Conway-99**, ni directement ni indirectement. Pas de DRAT, nauty, Terwilliger, star complement ni switching
  de Seidel dans toute la collection.
- **Une seule technique mathématique transposable** : la hiérarchie de moments injectifs exacts de l'article sur les
  matrices de Hadamard complexes d'ordre 6. Pour nous, cela donne :
  - des densités de motifs induits à t ≤ 6 ou 7 sommets ;
  - des relations de contraction exactes en n = 99 ;
  - des matrices de Gram enracinées ⪰ 0 avec un sommet partagé ;
  - un certificat rationnel revérifié exactement.
  Les conditions à 3 points (Krein : −28 ≤ 153, 42 ≤ 160 ; bornes absolues 1034 et 1539) ont beaucoup de marge.
  Un certificat de bas degré est donc improbable. Le gain réaliste, ce sont des égalités forcées (directions nulles du
  dual) à injecter dans CP-SAT.
- **Méthodes de certification** reprenables : Snaky (règle de composition prouvée une fois + données vérifiées par
  `decide +kernel` en Lean) et Ramsey cycle–clique (journal de propagation en JSONL, double vérificateur). Ce dernier est
  utile pour CP-SAT, qui n'émet pas de DRAT.
- **Non transférables** :
  - descente de corps (Hadamard circulante : elle exige une action régulière abélienne, exclue à 99) ;
  - recouvrements binary64 (MUB 6 : code de vérification absent du dépôt) ;
  - certificats de Fourier à deux points (la représentation euclidienne est un 2-design qui sature Delsarte à
    2 points) ;
  - « Fano » et « abélien » désignent ici des variétés algébriques.
- **Habitudes de raisonnement** (161b) : reformulations vérifiées, test de Liouville, objets extrêmes comme bancs
  d'essai, budgets chiffrés, bascule quand une obstruction revient, alternance preuve/réfutation. Faiblesses :
  surrevendication, auto-audit en boucle, aucun calcul visible.
