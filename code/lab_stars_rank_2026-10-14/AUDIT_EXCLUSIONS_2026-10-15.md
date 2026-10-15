# Audit des énoncés « qui excluraient Conway » (LAB, 15/10/2026, matin)

Demande de l'utilisateur (15/10, ~02:50 UTC) : refaire l'audit de toutes les conjectures et de tous les théorèmes
trouvés qui excluraient Conway, faire l'état des lieux, vérifier que rien n'a été manqué, en relisant tout ce qui a été
fait le 14/10 et la nuit ; ensuite continuer la piste vivante si elle le mérite.

## 0. Sources relues et re-vérifications faites ce matin
- Relu : NOTE_STARS_RANK.md, NOTE_PROOFS_1410.md (P1-P14, E1-E10, OPEN), N9_REDUCTION_2026-10-15.md,
  CONWAY_CONSTRAINTS.md (A1-G17), NOTE_ASYM_PALEY.md (sections 5, 9, 11), NOTE_ASYM_WINDOW.md (sections 4-8),
  NOTE_NIGHT.md (nuit du 13-14/10, en-têtes et énoncés), NOTE_LAMBDA1.md et SOLVER_CAMPAIGN_STATE.md, journal de Codex
  JOURNAL_C1_NUIT_2026_10_14.md (sections du 15/10, messages 764 à 778).
- Re-vérifié exactement (verify_counterexample.py, arithmétique exacte, sans code de recherche) : les 11 témoins à quatre
  étoiles (night_urep_PSD_100, c31_mix4, c21_mix4, c11_mix6, asym_c31, asym_c21, grid_Z5h_c22, grid_Z5h_c62, r7_25_Z5h,
  rank30_c33_h, psd4_candidate_1) : admissibles, T et U semi-définies positives, rangs et c conformes aux notes.
  Les 52 objets à trois étoiles de counterexamples_A_all.json : les 52 sont des contre-exemples exacts à (A) (jusqu'ici
  seul l'objet 38 était vérifié exactement). z2b.json : rang 30, c(l) = 2, sans grille (réfute (H3)).
- Recalculé : transversales t(l), t(m) des 331 objets de rang 30 (audit_transversals.py) ; classes de carrés complètes.

## 1. Énoncés conditionnels d'exclusion (« si X est vrai, Conway n'existe pas »)

### 1.1 Réfutés (témoins exacts, tous re-vérifiés ce matin)
| # | énoncé | conséquence visée | réfuté par |
|---|---|---|---|
| R1 | (H3) trois étoiles, positivité, rang 30 => grille sur (l, m) | avec L8 : pas de Conway | z2b.json (rang 30, sans grille), 14/10 |
| R2 | (H4) aucun objet à quatre étoiles n'est positif | pas de Conway | psd4_candidate_1.json, 14/10 ~21:12 UTC |
| R3 | (A) trois étoiles, positivité, c(l) = 1 => rang 31 | avec (C) : pas de Conway | 52 objets exacts, 14/10 ~20:55 UTC |
| R4 | (A4) positivité à quatre étoiles => c(l), c(m) >= 2 | toute droite spéciale | fourstar_psd_c31_mix4.json (c(m) = 1) |
| R5 | au plus 2 relations mixtes | rho >= 198 > 191 (borne prouvée) | E4 (4 mixtes) |
| R6 | au plus 3 relations mixtes | rho >= 154 > 126 (certificat de Codex) | E4, E5 (4 et 6 mixtes) |
| R7 | (N9) nullité <= 9 + min(c) | c >= 5 partout, rho >= 154 > 126 | E6 (c62 : nullité 14 > 11) |
| R8 | (NOGRID) pas de grille sur (l, m) + (LOW) nullité <= 13 si c <= 3 | pas de Conway (sans census) | E6 (grille), E8 (c = (3,3), nullité 14) |
| R9 | (R7) rang_7(8T_S4) >= 29 | contradiction avec k <= 28 (L22) | E7 (rang_7 = 25) |
| R10 | au plus 6 relations mixtes (idée de la nuit, jamais écrite comme conjecture) | - | E8 (7 mixtes) |

Toutes ces lois venaient de recherches parties de la famille G1 (ou de graines qui en descendaient) ; chacune est tombée
dès qu'une famille indépendante a été essayée.

### 1.2 Encore ouverts, compatibles avec toutes les données
| # | énoncé (local, sur les structures admissibles avec T, U >= 0) | ce qu'il donnerait | données |
|---|---|---|---|
| O1 | (B') nullité >= 14 => aucune droite avec c = 1 | toute droite de Conway est spéciale. N'EXCLUT PAS SEUL : il faut aussi (C) | 331/331 objets de rang 30 ont min c >= 2 ; avec une droite c = 1 la nullité vue ne dépasse pas 10 (800 408 visites), mais UNE seule lignée a visité c = 1 (voir 3.8) |
| O2 | ODD9 : les 10 vecteurs impairs ajoutent exactement 9 au rang | implique (B') et nullité <= 12 + min(c) | exact sur tout objet positif testé ; FAUX sans positivité |
| O3 | (T8) pont des transversales : nullité >= 14 => t(l) >= 8 et t(m) >= 8 (variante : t(l) + t(m) >= 15) | P >= 924 (variante : P >= 867), contre P <= 852 (certificat exact de Codex, ordre 9) : PAS DE CONWAY | 331/331 : t = (12,12) dans 329 cas, (8,8) dans 2 ; FRAGILE : avec t <= 7 la nullité vue atteint 13 (voir 3.8) |
| O4 | (K22) nullité >= 14 => rang_7(8T_S4) >= 23 | k >= 24, donc r = 37 exclu ; avec >= 25 : r = 37 et 39 exclus | rang_7 = 25, 29 ou 30 sur les 331 |
| O5 | (SQ30) rang 30 => classe de carrés de det(8T_I) = 2*3*5*7^e | aucun bloc de Conway de rang 30, donc delta >= 1 à toute paire | 331/331 (+ sc_7_null14) ; un objet NON positif de rang 30 a la classe -2 |
| O6 | (N15) aucun objet positif de nullité >= 15 | avec O5 : PAS DE CONWAY (tout bloc aurait rang 30, donc devrait passer DISC) | aucune donnée : jamais cherché avant ce matin |
| O7 | H4' : pas de droite c = 1 des deux côtés à nullité >= 14 | cas particulier de O1 | max nullité 10 en c = (1,1) |
| O8 | (C) toute Conway a une droite non spéciale | avec O1 ou O2 : PAS DE CONWAY | aucune idée de preuve ; le cas « toute droite non connexe » est aussi un verrou du programme 7-adique de Codex (note 127, verrou 3) |

### 1.3 Autres voies d'exclusion de la journée (asymétrie, solveur, Codex)
- Principe de symétrie forcée (prouvé) : une pièce forcée qui a plus de symétries que de complétions exclut C1. La
  fenêtre est fermée aux ordres 1 et 2 (flips, théorème de majorité de Codex) : aucune pièce forcée symétrique connue.
  Reste « l'abondance » : il faudrait une borne supérieure sur le nombre de solutions ; aucune méthode.
- Conjecture (P) de Codex (toute arête est dans un prisme) : P >= 231 ; n'exclut que le profil sans prisme.
- Campagne solveur enracinée (14/10, calibrée sur srg(57,14,1,4) et srg(51,10,1,2), UNSAT sans certificat DRAT) :
  Conway arrêté sans verdict, campagne mise en pause par l'utilisateur ; rien ne tourne.
- Théorèmes de rang de la nuit du 13-14/10 (rang_F7(A + 4I) >= 33) : redécouverte, plus faible que la fenêtre
  {37, 39, 41, 43} déjà connue.
- Codex, 15/10 : la famille G1 c55 sans grille est exclue par F7 (théorème) ; au moins 336 des 2079 drapeaux ont au
  moins 4 relations mixtes (prouvé, utilise rho <= 126) ; budgets de comptage du second ordre (nécessaires, pas des
  bornes sur P) ; le census d'ordre 9 admet P = 0 en relaxation réelle (pas de borne inférieure sur P par cette voie).

## 2. Théorèmes utilisés, re-vérifiés
- P1 (T^2 = 7T), P3 (rang T_X = 23 - c, preuve de Codex), P6 (relations mixtes >= 12 - c_l - c_m + [grille]), G9
  (rang T_S4 = 30 - delta, delta = multiplicité de -4 sur les 40 labels extérieurs) : relus, corrects.
- Tests d'extension (Tr) et (Tn) : nécessaires pour TOUTE complétion de rang 30, positive ou non (si rang(bloc entier) =
  rang(sous-bloc), les colonnes nouvelles sont dans l'image et le complément de Schur est nul). La note E9 disait
  « aucune complétion de rang 30 » : c'est bien correct, même sans positivité.
- DISC = (SQ3) : lemme de classe de carrés (prouvé, testé sur Petersen, Paley 9 et 25, un vrai srg(243,22,1,2)) +
  L2/L22 de Codex ; partie robuste (premiers autres que 2 et 7 à exposant pair) sans aucun lemme de Codex.
- ODD9 => c(l) >= 2 + delta : 23 - c + 9 <= rang T_S4 = 30 - delta. Correct.
- Entrées acceptées sans re-dérivation : L2, L22 (Codex) ; P <= 852 et rho <= 126 (certificats exacts de Codex, census
  d'ordre 9) ; P <= 1151 (Codex, preuve cubique).

## 3. Ce que j'avais manqué ou mal dit
1. Le pont des transversales (O3) était la cible du 14/10 au soir (CONWAY_CONSTRAINTS G11). Je ne l'ai pas re-testé
   cette nuit alors que c'est le seul des énoncés ouverts qui donnerait une exclusion à lui seul (modulo le certificat
   P <= 852 de Codex). Les 331 objets de rang 30 le satisfont tous, largement.
2. (B') n'exclut pas Conway à lui seul : il donne « toute droite est spéciale ». Il faut en plus (C). Le bilan de nuit
   aurait dû le dire explicitement. Le mot « équivalent » y était trop large : (B') implique « toute droite spéciale » ;
   la réciproque ne vaut que pour les blocs qui apparaissent vraiment dans un Conway.
3. Biais d'échantillon fondamental : les 331 objets échouent tous au test du discriminant, donc AUCUN n'est un bloc de
   Conway. Si Conway existe, ses blocs sont soit de rang 30 et passent DISC (jamais vu), soit de nullité >= 15 (jamais
   vu). Les lois O1-O5 sont observées sur une population qui ne contient pas les blocs de Conway. Un contre-exemple
   les réfuterait quand même ; mais leur validation sur ces objets prouve peu.
4. Deux lignées seulement (G1-c55 et Z5h). Dans une lignée, c varie mais la classe de carrés, rang_7 et les
   transversales restent fixes : c'est l'amas qui décide, pas c.
5. Combinaison nouvelle : O5 + O6 exclurait Conway, et delta = 0 est le cas générique (rien n'oblige les 40 labels
   extérieurs à porter un vecteur propre -4). O6 n'avait jamais été cherché.
6. Le catalogue CONWAY_CONSTRAINTS G8 était périmé (« tout objet positif trouvé a c >= 3 ») et G11 sans les données.
7. La note E9 n'avait vérifié exactement qu'un des 52 objets (A) : les 52 le sont maintenant.
8. Relecture de TOUS les journaux de marche (audit_logs_nt.py : 800 408 visites positives, toutes familles) :
   - avec une droite c = 1, la nullité ne dépasse jamais 10 (= 9 + 1, la valeur de (N9) en c = 1) ; avec c >= 2 elle
     atteint 14. Mais toutes les visites c = 1 viennent de la même lignée (graines c11, c21, c31, asym, issues de G1/h) :
     les marches Z5h et c55, les seules qui atteignent la nullité 14, n'ont JAMAIS visité de structure positive avec
     c = 1. L'écart de 4 en faveur de (B') est donc mesuré dans une seule lignée.
   - pour (T8), l'écart est minuscule : avec une droite portant au plus 7 transversales, la nullité atteint 13
     (t = 2 dans Z5h, t = 6 dans la lignée c55). Il suffirait d'une relation de plus pour réfuter (T8). Je le classe
     donc comme fragile, malgré les 331/331.

## 4. Suite
Toutes les pistes ouvertes reposent sur les mêmes 331 objets. L'étape la plus informative est donc d'obtenir des objets
de nullité >= 14 dans des familles vraiment nouvelles, et de tester O1 à O6 dessus en une fois. Lancé à 03:00 UTC :
six familles nouvelles (Z5 x (0 1)M, Klein extérieur x h, cycle (0 2 1 3) x Klein, Z5 x échange des droites,
Z5 x hM, Klein extérieur x échange), deux recherches de nullité 15 (O6) et deux recherches de rang 30 avec t <= 7 (O3).
Le groupe <(4 6)(5 7), (8 10)(9 11), h> n'admet aucune structure admissible (SAT). Ajouté à 03:01 UTC : deux
recherches qui imposent une droite c = 1 dans les lignées à haute nullité (Z5h à froid, et h depuis c55), pour tester
(B') là où il n'a jamais été testé.
