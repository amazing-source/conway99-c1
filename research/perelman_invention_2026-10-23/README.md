# Perelman, l'invention mathématique et Conway-99

Dossier de recherche indépendant, créé les 23 et 24/10/2026 sur la branche `claude/perelman-invention-conway`, en
réponse au mandat « Perelman, l'invention mathématique et Conway-99 ». Il ne modifie aucune campagne de calcul en
cours. Il lit le dépôt (carte maîtresse, notes, données) sans rien y écrire.

## Les deux travaux

| dossier | contenu |
|---|---|
| `etude_perelman/` | **Premier travail.** L'invention chez Perelman : le mur avant 2002, la reconstruction des mécanismes avec les équations, treize fiches d'invention avec leur origine vérifiée, dix schémas testables (S1–S10) et cinq conditions de transfert vers un problème fini (T1–T5). Commencer par `00_INDEX.md` |
| `conway/` | **Second travail.** Les conditions T1–T5 testées une à une sur srg(99, 14, 1, 2), avec démonstrations, calculs et obstacles formulés exactement. Commencer par `00_INDEX.md` |
| `code/` | Les scripts des onze expériences, et leur mode d'emploi (`code/README.md`) |
| `data/` | Les sorties JSON de ces expériences |

## En une phrase

Pas de transfert qui fasse avancer l'exclusion de Conway. Aucune dynamique naturelle n'existe sur le graphe (démontré).
La topologie du complexe triangles-carrés structure la famille srg(v, k, 1, 2) (codes parfaits ; π₁ des huit srg(243)
connus), mais ne peut pas exclure Conway, car le type prédit est réalisé par de vrais graphes. Le reste (étalements,
« ingrédient manquant » d'ODD-PURE) redit des choses que l'équipe savait déjà.

## Conventions de statut

**[P]** démontré dans ces notes · **[L]** littérature · **[E]** calcul reproductible · **[S]** verdict de solveur ·
**[A]** analogie · **[C]** conjecture · **[O]** ouvert ou obstacle formulé. Les statuts des résultats de la campagne
sont repris de la carte maîtresse, sans nouvel audit, conformément à la consigne du 9 octobre (CLAUDE.md).

## Sources principales

- Perelman, arXiv:math/0211159, math/0303109, math/0307245, lus intégralement (sources LaTeX).
- Kleiner–Lott, arXiv:math/0605667 ; Morgan–Tian, arXiv:math/0607607 ; Tao, arXiv:math/0610903.
- Lin–Lu–Yau, Tohoku Math. J. 63 (2011) ; Ollivier, J. Funct. Anal. 256 (2009) ; Li–Liu, JUSTC 51 (2021) ; Huang–Liu–Xia,
  Combinatorica 44 (2024) ; Brouwer–Cohen–Neumaier, *Distance-regular graphs* (1989).
- Dépôt `amazing-source/conway99-c1` : `code/lab_chantier_2026-10-20/CARTE_MAITRESSE.md`, `notes/` (10, 20, 30, 159, 165,
  236–240), `code/lab_exploration_2026-10-16/EXPLORATION.md`, `code/lab_stars_rank_2026-10-14/N9NG_ATTACK_2026-10-15.md`,
  `code/lab_spreadfree_243_2026-10-12/`, `data/srg243/`, `data/t2_twisted.json`, `data/t3_twisted.json`.
