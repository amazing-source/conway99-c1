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

La plupart ((A4), les plafonds de relations mixtes, (N9), (NOGRID), (LOW), (R7)) venaient de recherches parties de la
famille G1 ou de graines qui en descendaient, et sont tombées dès qu'une famille indépendante a été essayée ; (H3), (H4)
et (A) avaient d'autres origines (données Z5, premières recherches). Remarque (relecture indépendante) : (H3) ne
portait que sur le rang exactement 30, alors qu'un bloc à trois étoiles de Conway a le rang 30 - delta' <= 30 ; même
vraie, (H3) + L8 n'aurait donc pas suffi à exclure Conway.

### 1.2 Encore ouverts, compatibles avec toutes les données
| # | énoncé (local, sur les structures admissibles avec T, U >= 0) | ce qu'il donnerait | données |
|---|---|---|---|
| O1 | (B') nullité >= 14 => aucune droite avec c = 1 | toute droite de Conway est spéciale. N'EXCLUT PAS SEUL : il faut aussi (C) | 331/331 objets de rang 30 ont min c >= 2, mais 329 ont la grille sur (l, m), qui force c >= 2 à elle seule : seuls les 2 objets c55 testent vraiment (B') ; avec une droite c = 1 la nullité vue ne dépasse pas 10 (280 424 visites positives avec c = 1), et UNE seule lignée a visité c = 1 (voir 3.8) |
| O2 | ODD9 : les 10 vecteurs impairs ajoutent exactement 9 au rang | implique (B') et nullité <= 12 + min(c) | exact sur tout objet positif testé ; sans positivité, quasi-échecs (écart 2e-5) mais aucun échec exact enregistré |
| O3 | (T8) pont des transversales : nullité >= 14 => t(l) >= 8 et t(m) >= 8 (variante : t(l) + t(m) >= 15) | P >= 924 (variante : P >= 867), contre P <= 852 (certificat exact de Codex, ordre 9) : PAS DE CONWAY | 331/331 : t = (12,12) dans 329 cas, (8,8) dans 2 ; FRAGILE : avec t <= 7 la nullité vue atteint 13 (voir 3.8) |
| O4 | (K22) nullité >= 14 => rang_7(8T_S4) >= 23 | k >= 24, donc r = 37 exclu ; avec >= 25 : r = 37 et 39 exclus | rang_7 = 25, 29 ou 30 sur les 331 |
| O5 | (SQ30) rang 30 => classe de carrés de det(8T_I) = 2*3*5*7^e | aucun bloc de Conway de rang 30, donc delta >= 1 à toute paire | 331/331 (+ sc_7_null14) ; un objet NON positif de rang 30 a la classe -2 |
| O6 | (N15) aucun objet positif de nullité >= 15 | avec O5 : PAS DE CONWAY (tout bloc aurait rang 30, donc devrait passer DISC) | jamais vue : ~288 000 visites positives à nullité 14 dans les journaux, aucune à 15 ou plus ; sc_2_null14 (T seule positive, U non) atteint 16 |
| O7 | H4' : pas de droite c = 1 des deux côtés à nullité >= 14 | cas particulier de O1 | max nullité 10 en c = (1,1) |
| O8 | (C) toute Conway a une droite non spéciale | avec O1 ou O2 : PAS DE CONWAY | aucune idée de preuve ; le cas « toute droite non connexe » est aussi un verrou du programme 7-adique de Codex (note 127, verrou 3) |

### 1.3 Autres voies d'exclusion de la journée (asymétrie, solveur, Codex)
- Principe de symétrie forcée (prouvé, modulo Aut = 1, qui utilise C3, en relecture externe) : une pièce forcée qui a plus de symétries que de complétions exclut C1. La
  fenêtre est fermée aux ordres 1 et 2 (flips, théorème de majorité de Codex) : aucune pièce forcée symétrique connue.
  Reste « l'abondance » : il faudrait une borne supérieure sur le nombre de solutions ; aucune méthode.
- Conjecture (P) de Codex (toute arête est dans un prisme) : P >= 231 ; n'exclut que le profil sans prisme.
- Campagne solveur enracinée (14/10, calibrée sur srg(57,14,1,4) et srg(51,10,1,2), UNSAT sans certificat DRAT) :
  Conway arrêté sans verdict, campagne mise en pause par l'utilisateur ; rien ne tourne.
- Théorèmes de rang de la nuit du 13-14/10 (rang_F7(A + 4I) >= 33) : redécouverte, plus faible que la fenêtre
  {37, 39, 41, 43} déjà connue.
- Cibles de la nuit du 13-14/10 (NOTE_NIGHT, section 2) : T1 (pas de sommet localement affine) = L8, prouvé ; T2 (aucune
  grille 3 x 3) n'exclurait pas Conway seul ; T3 (borne sur le nombre de prismes p(l) d'une droite, 0 <= p(l) <= 12 par
  F3) : une borne inférieure p(l) >= 8 pour toute droite serait décisive avec P <= 852 ; c'est exactement le pont (T8).
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

## 5. Boucle de tests après l'audit (15/10, à partir de 03:00 UTC ; l'utilisateur dort, « continue en loop »)
Journal des résultats, au fil de l'eau (heures UTC).
- 03:01-03:12 : quatre groupes n'admettent AUCUNE structure admissible à quatre étoiles (SAT) :
  <(4 6)(5 7), (8 10)(9 11), h>, <h, (4 6)(5 7)>, <h, (4 5)>, et (déjà connu) <(4 6 8)(5 7 9)>.
- 03:05 : les familles contenant Z5 imposent la grille sur (l, m) (un label fixe ne peut pas être apparié à une
  5-orbite) : 276 des 331 objets sont Z5-invariants, et 329/331 ont la grille ; l'absence de c = 1 y est automatique.
- 03:10 : mécanisme des relations dans les objets Z5h de rang 30 : 9 relations mixtes de la forme
  (combinaison l-paire sur X_l) + 5 (1_{2y} + 1_{3y}), une par lettre extérieure y : les vecteurs pairs de m sont
  absorbés par X_l ; chaque relation vit sur la boule de l plus la droite {y, z_2y, z_3y} (prisme avec m).
- 03:13 : interdire la grille sur (l, m) près de ces objets (NOSQUARE) fait perdre la positivité (lambda_min vers
  -0,3 après 6000 pas) : la grille est essentielle à ces objets de rang 30.
- 03:20 : énumérations EXHAUSTIVES (enum_group.py : modèle SAT de sym4g.py, blocage sur les représentants d'orbites,
  terminé quand le solveur dit UNSAT) : <Z5, h, M> (ordre 20) : 64 structures admissibles, aucune positive ;
  <Z5, (0 1)M, (2 3)M> (ordre 20) : 4, aucune positive ; <Z5, h, (0 2)(1 3)> (ordre 20) : 90, aucune positive.
  Z5h (ordre 10) : 6177 structures en 240 s sans finir (13 positives : nullité 14 seulement avec t = (12,12) et la
  grille ; dans Z5h, t vaut 2, 7 ou 12 par orbites) ; énumération complète lancée (limite 2 h).
- 03:20 : les marches « oddgap » longues dans h retrouvent des quasi-échecs d'ODD9 (troisième valeur propre impaire
  0,007 en quelques minutes) : ODD9 reste fragile.
- 03:24 : relecture des journaux par transversales des DEUX droites (t_scan2.py, ~830 000 visites positives) :
  quand les deux droites ont au plus 7 transversales (le régime typique d'un Conway, où la moyenne de t est <= 7,38
  par le certificat de Codex), la nullité vue ne dépasse pas 12 (t = (6,6) et (7,7), lignée c55) ; avec
  t(l) + t(m) <= 14 elle atteint 13 une fois (t = (12,2), Z5h). Les variantes du pont : « t(l), t(m) >= 8 »
  (P >= 924) et « t(l) + t(m) >= 15 » (P >= 867) sont donc compatibles avec tout ce qui a été vu, à une relation près ;
  « au moins une droite avec t >= 8 » (P >= 792) n'exclurait rien.
- 03:30 : MÉCANISME transversales <-> nullité (even_explained.py, even_bound_scan.py). Avec ODD9, la nullité vaut
  12 + c(l) - (gain pair), où le gain pair est celui des 10 vecteurs m-pairs g_y = 1_{2y} + 1_{3y} au-delà de
  X_l + (vecteurs impairs). Nullité 14 exige donc gain pair = c(l) - 2 : pour c(l) = 2, TOUS les g_y doivent être
  absorbés. Or la norme de g_y vaut 5/2 si y est une transversale de m, 9/2 sinon, et sur 6000 structures positives
  tirées des archives (toutes familles, les deux sens l/m) la part « expliquée » d'un g_y non transversal ne dépasse
  jamais 4,2516 < 4,5 : un g_y non transversal n'est jamais absorbé, un g_y transversal peut l'être (2,5 atteint).
  Si cette borne était un théorème : nullité 14 avec c(l) = 2 forcerait les 10 transversales extérieures de m
  (t(m) >= 10), exactement ce que montrent les 182 objets (2,2). C'est une explication du pont (T8), pas une preuve ;
  pour c(l) >= 3 l'absorption partielle ne force rien lettre par lettre.
- 03:33 : bilan intermédiaire des recherches lancées à 03:00 : aucune cible atteinte. Pas de structure positive de
  nullité 15 (n15_Z5h, ~30 000 pas) ; pas de nullité 14 avec t <= 7 (t8_*) ; pas de droite c = 1 à nullité >= 11
  (c1_*, dont G1 où c = 1 est permis) ; sans grille sur (l, m) près des amas connus, pas de positivité (nosq_*).
  32 objets de rang 30 réellement nouveaux, tous dans les deux lignées connues (t = (12,12) avec grille et classe
  2*3*5*7, ou c55 avec t = (8,8), sans grille et classe 2*3*5) : aucun ne passe DISC, tous satisfont ODD9.
- 03:36 : vérification de la formule « nullité = 12 + c(l) - gain pair » sur les 331 objets : gain pair = c(l) - 2
  pour TOUS (227 objets avec c(l) = 2 et gain 0, 24 avec c(l) = 3 et gain 1, 12 avec 4 et 2, 10 avec c(l) = 5 et 3 (dont les 2 c55), 58 avec 6
  et 4 ; ce n'est pas une vérification indépendante : rang 30 + ODD9 + P3 imposent cette identité) ; les 10 lettres extérieures de m sont des transversales partout sauf dans la lignée c55 (8). Lecture : un
  contre-exemple à (B') demande un gain total <= 8 au-delà de X_l, donc un échec d'ODD9 (gain impair <= 8) ; si le gain
  impair vaut exactement 8, il faut EN PLUS l'absorption complète des vecteurs pairs (donc 10 transversales sur m) ;
  la lignée c = 1 connue a 4 à 6 transversales.
- 03:50 : où mènerait la piste si les deux lois locales étaient prouvées (programme, rien de prouvé) :
  (i) ODD9 (gain impair 9) et (ii) la borne d'absorption (un g_y non transversal n'est jamais absorbé). Dans un
  Conway, un bloc de rang 30 (delta = 0) a P_V(B) de dimension 32 - c(l) ; pour c(l) = 2 c'est tout V, donc tous les
  g_y sont absorbés, ce que (ii) interdit sauf si les 10 lettres extérieures sont des transversales de m. Donc :
  (i) => toute droite a c >= 2 ; (i)+(ii) => toute droite l avec c(l) = 2 force t >= 10 sur les 18 droites qui la
  coupent (avec ODD9, c(l) = 2 force d'ailleurs delta = 0 à toutes les paires de l). Avec P <= 852 (moyenne de t <= 7,38), il y a au plus 170 droites avec t >= 10 ;
  cela contraint les voisines des droites avec c = 2 sans dire que ces droites sont rares, et les autres droites
  auraient c >= 3 (au moins trois parts : grilles ou
  configurations fermées de taille 2 ou 3). Ce n'est pas encore une exclusion : il faudrait un comptage de plus
  (census des configurations fermées). Je le note comme programme, pas comme résultat.
- 04:05 : fin de la deuxième vague (2700 s chacune). Depuis les objets (2,2) de rang 30, deux marches qui cherchaient
  N'IMPORTE QUELLE structure positive avec une droite c = 1 (groupe identité : 39 995 visites positives ; groupe h :
  30 624) n'en ont trouvé AUCUNE, même à basse nullité : autour de l'amas Z5h, la positivité garde la grille sur (l, m),
  donc c >= 2 ; et sans grille la positivité tombe (nosq). L'amas à haute nullité et la lignée c = 1 (nullité <= 10)
  sont deux régions séparées de l'espace positif. Pas de nullité 15 (n15_Z5h, 31 524 visites), pas de t <= 7 à
  nullité 14 (t8, 77 939 visites), pas de nouvelle lignée (nl_Z5M plafonne à 13).
- 04:08 : troisième vague terminée sans cible : les marches « oddgap » dans h descendent à 0,007 (troisième valeur
  propre impaire), sans échec exact d'ODD9 ; dans G1 (où c = 1 est permis), ~7 800 visites positives depuis c55 et
  depuis psd4_candidate : aucune avec c = 1 ; sans grille près de l'amas Z5h : aucune structure positive en 3000 s.
  Lancé : énumérations exhaustives de Z5 x (0 1)M et de Z5 x (0 2)(1 3) (2 h chacune), deux familles nouvelles
  <h, (4 7)(5 6)> et <(0 1)(4 5)>, recherche ciblée b1x dans h depuis c31.
- 04:20 : RELECTURE INDÉPENDANTE de cet audit (agent « adversarial reviewer », lecture seule) : aucune réfutation
  fausse, aucune implication fausse dans les tableaux 1.1 et 1.2. Corrigé suite à ses remarques : (1) « ODD9 faux sans
  positivité » n'est pas établi (quasi-échecs 2e-5, aucun échec exact) ; (2) l'« équivalence » (B') <=> « toute
  droite spéciale » et « ODD9 <=> c >= 2 + delta » étaient fausses comme équivalences : seules les implications sont
  vraies (corrigé dans NOTE_PROOFS, CONWAY_CONSTRAINTS G17, BILAN) ; (3) (A) et (H4) marqués réfutés dans la liste OPEN
  du carnet ; (4) le témoignage pour (B') est presque vide : 329/331 objets ont la grille, qui force c >= 2, seuls les 2
  c55 testent (B') ; (5) comptes corrigés (275 objets atteignent la borne, 10 objets avec c(l) = 5, 280 424 visites
  avec une droite c = 1) ; (6) sc_7_null14 n'est pas un objet admissible positif (U non positif) ; (7) la
  re-vérification exacte des 52 objets (A) est maintenant consignée : verify_A52_2026-10-15.log (52/52) ; (8) G5 : les
  52 meurent tous à l'étiquette {3,4} de la quatrième étoile (ext3), {4,6} n'avait été testée que sur l'objet 38.
