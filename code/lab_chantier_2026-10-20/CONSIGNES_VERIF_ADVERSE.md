# Vérification adverse d'une combinaison candidate (chantier du 20/10/2026)

Tu reçois une combinaison candidate issue de la recombinaison (agents R1, R2 ou R3). Elle prétend qu'en reliant des
résultats épars, on obtient une exclusion, une réduction ou un fait nouveau sur le graphe de Conway srg(99,14,1,2).

**Ton rôle est de la casser.** Une combinaison n'est retenue que si elle résiste à tous les contrôles ci-dessous.

## Contrôles obligatoires

1. **Énoncés exacts.**
   - Ouvre chaque ingrédient à sa source **d'origine**, pas seulement dans sa fiche, et recopie l'énoncé exact avec sa
     ligne.
   - Pour une note qui n'existe que dans une branche git : `git -C <dépôt> show <branche>:<chemin>`.
   - Les dépôts sont dans `C:/home/researcher/cw/` et `C:/home/researcher/Desktop/Recherche_Conway/`. L'espace de travail est
     `C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/`.
2. **Définitions et normalisations.**
   - Vérifie que les objets coïncident : P, G, n3, t, c(l), m, ν, normes de vecteurs, bord, complétion, rang.
   - Conventions de rang :
     - r = rang_7(A − 3I) chez l'équipe ;
     - r_ext = rang_F7(2A − J + I) dans le dépôt externe ;
     - r = r_ext + 1, prouvé dans `chantier_2026-10-20/CARTE_MAITRESSE.md` §1.6.
3. **Hypothèses.** Chaque hypothèse de chaque ingrédient doit être satisfaite dans la portée de la combinaison. Les
   hypothèses cachées comptent : rang fixé, c(l), t ≤ 7, positivité stricte, absence de grille, etc.
4. **Statuts.**
   - Le statut de la combinaison est celui de son ingrédient le plus faible.
   - Un verdict CP-SAT antérieur au correctif du 18/10 (bug OR-Tools 9.15, domain[-1] = 0) est retiré, sauf s'il a été
     refait.
   - Un verdict S n'a pas de certificat.
5. **Logique.** L'implication doit s'emboîter exactement. Méfie-toi :
   - des quantificateurs : « il existe une droite » n'est pas « toute droite » ;
   - des cas d'égalité ;
   - des bornes entières contre réelles ;
   - des arrondis.
6. **Redécouverte.** Cherche (grep dans `work/`, les dépôts et `chantier_2026-10-20/fiches/`) si la combinaison a déjà été
   faite, puis donne la source et la date.
7. **Contrôle numérique.** Si un nombre est en jeu, refais le calcul avec un petit script (un processus, moins de
   5 minutes).

## Verdict

Écris `chantier_2026-10-20/assemblage/VERIF_<id>.md`, en français, avec :
- **Verdict** : TIENT, TIENT AVEC RÉSERVES (lesquelles), CASSÉE (où exactement) ou DÉJÀ CONNUE (source).
- La chaîne complète réécrite proprement, chaque maillon accompagné de sa source exacte et de son statut.
- Ce qui manquerait pour que la combinaison soit une preuve complète.

## Interdits

- Lecture seule partout, sauf ton fichier VERIF.
- Ne pas ouvrir le dossier original `claude-codex-bridge` ; sa copie est dans `chantier_2026-10-20/pont_codex/`.
- Ne pas lire `C:\Users\RESEARCHER\Desktop\mdp.txt`, ni rien sous `~/.codex/`.
- Pas de commit, de mail, de cloud ni de calcul lourd.
