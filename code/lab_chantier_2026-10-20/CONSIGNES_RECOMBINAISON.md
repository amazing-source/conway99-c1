# Chantier du 20/10/2026 : consignes de la phase de recombinaison

**But.** Une exclusion du graphe de Conway srg(99,14,1,2), ou du seul cas asymétrique C1 (|Aut| = 1), peut se cacher dans
une combinaison de résultats épars, sans que personne ait relié les morceaux. Par exemple, une note dit « si X, alors pas de
Conway » et une autre prouve X. Cette phase cherche ces combinaisons dans tout le matériau consolidé, puis les vérifie de
façon adverse.

## Matériau d'entrée (lecture seule)

- `assemblage/MATERIAUX_BRUTS_*.md` : copie verbatim des sections « Matériaux pour la recombinaison » de chaque fiche. On y
  trouve les conditionnels, les bornes, les lemmes ouverts et les méthodes transférables. Chaque bloc indique
  `fiche:lignes`.
- `fiches/<lot>.jsonl` : tous les résultats, avec énoncé, statut, sources, dépendances et remarques. `fiches/<lot>.md`
  contient les tables, les routes fermées, les contradictions et la couverture de lecture.
- `assemblage/INDEX_RESULTATS.tsv` : index de tous les résultats (id, lot, statut, date, auteur, titre, première source).
- `assemblage/DOUBLONS_PROBABLES.tsv` : paires de résultats probablement identiques entre lots, avec leurs statuts.
- Les **sources originales** citées par les fiches (dépôts git, dossiers) peuvent être ouvertes pour vérifier un énoncé
  exact. Pour une note qui n'existe que dans une branche git : `git -C <dépôt> show <branche>:<chemin>`.
  - Les dépôts sont dans `C:/home/researcher/cw/` et `C:/home/researcher/Desktop/Recherche_Conway/`.
  - L'espace de travail est `C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/`.
- La copie des messages du pont LAB <-> Codex est dans `pont_codex/`. On cite un message par `pont:#N`.

## Pièges connus (à contrôler pour chaque combinaison)

1. **Conventions de rang.**
   - L'équipe note r = rang_7(A − 3I). La fenêtre certifiée est r ∈ {37, 39, 41, 43}.
   - Le dépôt externe conway-99-research note r_ext = rang_F7(2A − J + I).
   - Le dictionnaire r_équipe = r_ext + 1 a le statut H dans L03a-103 : à vérifier avant tout usage.
2. **Définitions.** Il faut vérifier que les deux énoncés parlent du même objet : P (prismes triangulaires induits), G
   (grilles), n3 externe, t (triangles transversaux d'une droite), c(l) (nombre de composantes du graphe cubique G_T d'une
   droite), m, ν, α, normes des vecteurs propres entiers de valeur −4 (normalisation !), « bord », « complétion »
   (étiquetée ou non), etc.
3. **Statuts.** Le statut de l'implication et celui de l'hypothèse sont distincts.
   - Un verdict CP-SAT antérieur au correctif du bug OR-Tools du 18/10 (domain[-1] renvoyait 0) est suspect, sauf s'il a
     été refait.
   - Un verdict S n'a pas de certificat.
   - Aucun humain n'a relu ces preuves. Ne jamais rehausser un statut.
4. **Portée.** Préciser ce que la combinaison couvre : C1 seul ou cas général, un rang précis, une plage de c(l), de
   nullité ou de t. Une réfutation ne touche que la version qu'elle vise.
5. **Redécouverte.** Avant de déclarer une combinaison nouvelle, chercher (grep) si une note l'a déjà faite. Si oui, la
   marquer « DÉJÀ CONNUE » avec la source et la date. Une combinaison déjà connue reste utile si elle s'applique aux
   survivants d'aujourd'hui.
6. **Analogie, non transposition.** Une méthode d'un autre cas (C2, C3, srg(243), Paley, rang 37) ne s'applique pas telle
   quelle. Il faut dire ce qui change dans l'objet et ce qu'il faudrait prouver de neuf.

## Format de sortie (dans `assemblage/`)

- `<agent>.jsonl` : une ligne par combinaison candidate, au format :
  `{"id": "<agent>-NN", "type": "COND×FAIT|BORNE×BORNE|LEMME×PREUVE|ANALOGIE|INCOHERENCE",
  "enonce_combine": "...", "ingredients": [{"ref": "Lxx-NN ou source", "role": "hypothese|fait|borne_sup|borne_inf|methode",
  "statut": "...", "enonce_exact": "..."}], "conclusion": "...", "portee": "...", "statut_combine": "le plus faible des
  ingrédients", "deja_connue": "non | oui : source, date", "points_a_verifier": ["définitions...", "conventions..."],
  "potentiel": "EXCLUSION_GRAPHE | EXCLUSION_C1 | EXCLUSION_RANG | EXCLUSION_CAS | REDUCTION | AUCUN", "remarques": "..."}`
- `<agent>.md`, en français :
  - le résumé ;
  - les candidats classés par potentiel ;
  - les **quasi-ratés**, c'est-à-dire les bornes qui se touchent presque, avec l'écart chiffré ;
  - les **incohérences** trouvées entre notes ;
  - ce qui n'a pas été examiné.

## Interdits

- Lecture seule partout. On n'écrit que ses propres fichiers dans `assemblage/`.
- Ne jamais ouvrir le dossier original `claude-codex-bridge` ; utiliser la copie `pont_codex/`.
- Ne jamais lire `C:\Users\RESEARCHER\Desktop\mdp.txt`, ni quoi que ce soit sous `~/.codex/`.
- Pas de commit ni de push, pas de mail, pas de cloud, pas d'installation.
- Pas de calcul lourd : au plus de petits scripts de vérification, un seul processus, moins de 5 minutes, peu de mémoire.
- Pas d'affirmation sans source.
