# Articles prêts à relire (07/10/2026)

| dossier | article | état |
|---|---|---|
| `srg243_second/` | *A second strongly regular graph with parameters (243,22,1,2)* : nouveau graphe, non-unicité de BvLS, réfutation de la conjecture des hexagones de Reimbayev, rigidité de Godsil–McKay | texte complet ; fichiers annexes dans `anc/` (graphe, vérificateur, comptage d'hexagones) |
| `rank7/` | *On the 7-rank of a putative strongly regular graph with parameters (99,14,1,2)* : rang₇(A − 3I) impair, 23 ≤ rang₇ ≤ 43 (genre de Λ₋₄ + formule locale + étoiles), 25 avec un petit calcul | texte complet ; `verify_rank7.py` vérifie l'inverse du moulin, la formule locale mod 7, les rangs des 10 395 étoiles et l'arithmétique de genre |
| `s5_2adic/` | *A 2-adic nonexistence condition for strongly regular graphs* : critère S5, 35 « ? » de la table de Brouwer, famille NL_e(n), pg(14,14,4) | texte complet ; tableau régénéré et revérifié par `verify_s5.py` (0 écart) |

**Avant soumission.**
- Les PDF sont compilés (pdflatex, sans aucun avertissement) : `*/s5_2adic.pdf` et `*/srg243_second.pdf`.
- Relire en humain.
- Pour S5, demander l'avis d'A. E. Brouwer sur la nouveauté.
- Les remerciements mentionnent l'assistance de Claude (Anthropic). La version exacte du modèle n'est pas écrite
  dans le dépôt : l'auteur peut l'ajouter dans le .tex.

Non rédigé ici : l'article « automorphismes » (C2 + C3 + C7), en cours par l'autre équipe. Pour C1, restent
publiables plus tard : L16 (P ≤ 1151), L18, L8 (pas de point de Hamming), L25 (tissu de grilles ⟺ plan d'ordre 10).
