# Bilan de la nuit du 14 au 15/10 (LAB seul après 00:00 UTC, Codex hors usage)

Aucune exclusion. Tout ce qui suit est exact (arithmétique entière ou rationnelle), sauf mention « indice ».
Détails : NOTE_PROOFS_1410.md (entrées E1 à E10), N9_REDUCTION_2026-10-15.md, CONWAY_CONSTRAINTS.md (G12 à G17).
Tous les calculs sont arrêtés depuis 02:32 UTC.

## 1. Ce qui est établi
- Les objets à quatre étoiles (v, ses 14 voisins et les 44 labels de deux droites) peuvent satisfaire en même temps
  toutes les conditions locales spectrales connues : admissibilité, T et U semi-définies positives, rang exactement 30,
  et rang mod 7 au plus 28. J'en ai 331 distincts, tous vérifiés exactement (rank30_psd_objects_2026-10-15.json).
  Ces conditions ne peuvent donc pas exclure Conway à elles seules.
- Six lois que j'avais tirées des données sont fausses : (A4), « au plus 3 relations mixtes », (N9), (NOGRID), (R7)
  et (LOW). Elles venaient toutes de recherches parties de la même famille symétrique (G1). Dès qu'on en est sorti
  (d'abord le groupe à deux éléments h, puis Z5h, qui fait tourner les cinq autres droites), elles sont tombées,
  souvent en quelques minutes.
- Les 331 objets de rang 30 meurent tous au test du discriminant (exposants impairs en 3 et/ou 5). Les trois testés
  à l'extension meurent aussi : aucune des 40 étiquettes extérieures n'a de placement possible.
- Les 52 objets à trois étoiles connus qui contredisent (A) (une droite non spéciale, rang 30) n'ont aucune
  complétion de rang 30 à quatre étoiles : dès la première étiquette de la quatrième étoile, aucun profil ne convient.
- Le test du discriminant s'écrit simplement : dans un graphe de Conway, tout sous-graphe induit H à 45 sommets
  vérifie det(A_H - 3I) = 7^(30-k) n^2, donc c'est un carré parfait, divisible par 49 s'il est non nul. Pour
  55 sommets : det(A_H + 4I) = 2 7^(40-k) n^2. La preuve tient en cinq lignes (lemme : les mineurs principaux
  maximaux non nuls d'une matrice entière symétrique ont tous la même classe de carrés), plus L2 et L22 de Codex.
  J'ai revérifié les constantes à la main et testé le lemme sur Petersen, Paley 9 et 25, et sur un vrai
  srg(243,22,1,2). Le principe n'est pas nouveau : Codex l'utilise dans ses notes 205, 217, 231 et 247.

## 2. La seule piste encore vivante (non démontrée)
- (B') : aucun objet positif de rang 30 à quatre étoiles n'a de droite non spéciale (c = 1). Pour Conway, c'est
  équivalent à « toute droite est spéciale » (équivalence démontrée).
- Indices : sur les 331 objets de rang 30, le minimum de c est 2, atteint 182 fois. Les marches qui gardent une
  droite non spéciale (environ 20 000 visites positives) plafonnent à une nullité de 10, alors que Conway demande 14.
  ODD9 (les 10 vecteurs impairs ajoutent exactement 9 au rang) impliquerait (B') ; elle tient sur toutes les
  structures positives et sur l'analogue dans quatre vrais srg(243). Mais elle casse sans positivité : une preuve
  devra utiliser T ou U semi-définie positive.
- Prudence : la nuit a montré que ce genre de loi peut être un artefact de famille. Ici, trois familles symétriques
  et les marches qui en partent.
- Observation à tester (pas une loi) : les 331 objets ont tous la même classe de carrés, 2·3·5·7^e, alors que leurs
  sous-blocs à trois étoiles ont des classes dispersées. Une structure de rang 30 non positive a la classe -2, donc
  ce n'est pas une identité algébrique. Si « positif et rang 30 ⟹ classe 2·3·5·7^e » était vrai, aucun bloc à
  quatre étoiles d'un graphe de Conway ne pourrait être de rang 30. Deux lignées seulement : à tester d'abord dans
  des familles vraiment nouvelles.

## 3. Incident (ma faute)
Les marches ont écrit un fichier par visite positive : 477 579 fichiers (2,1 Go), ce qui ralentissait Python. Je les
ai déplacés, sans rien supprimer, dans visits_archive_2026-10-14_15/. Je ne les compresse ou ne les supprime que si
tu le demandes. Le code plafonne maintenant le nombre de fichiers écrits.

## 4. Commits
Branche lab/theta-lp-2026-10-08 du dépôt privé : f6ce63c, ce2c5b3, puis le commit final de la nuit.
