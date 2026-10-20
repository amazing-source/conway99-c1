# Note ChatGPT du 20/10 : vecteurs propres entiers de valeur 3 de norme < 16. Relecture et contrôle de nouveauté

LAB, 20 octobre 2026. Texte transmis par l'utilisateur (sortie ChatGPT), reproduit sans modification en annexe.

## Verdict

**La preuve est correcte.** Je l'ai relue ligne à ligne, à la main, pour les sections 2 à 6 :
- (a) W ≥ 4a, donc ||f||² ≥ a² + 7a ≥ 18 dès que a ≥ 2 ;
- (b) le comptage des chemins de longueur deux donne 3d ≤ 2(p − 1) ;
- (c) pour p = 6, on obtient le prisme (K3,3 exclu par μ ≤ 2) ;
- (d) pour p = 7, l'égalité dans le comptage force B7, qui est unique ;
- (e) le raccord découle de (A − 3I)² = 21I − 7A + 2J.

J'ai aussi contrôlé à la main que B7 et H14 respectent λ ≤ 1 et μ ≤ 2.

**Le contenu figure déjà dans l'archive.** Références dans Desktop/Recherche_Conway/c1-main-codex/notes :
- **note 168 §2** (reprise dans 174 §3 et 247 §1) : borne S ≥ 4h, min(Z^99 ∩ V_3) ≥ 12, prismes anticomplets à la norme 12 ;
- **note 179** : prismes jumeaux (le nombre τ) ;
- **note 181 §1 et §3** (8/10) :
  - le graphe D est **exactement B7** : centre v, puis a, b, c, d, arêtes ab et cd, puis x, y avec xa, xc, yb, yd, xy ;
  - D est le seul type à sept sommets de degré minimum au moins trois, d'après le recensement machine de 208 types ;
  - entre les deux copies, il n'y a qu'une arête, celle qui relie les centres ;
  - on a Ω ≤ H ;
- **note 188** : collisions de masses six et sept, c'est-à-dire prismes jumeaux et paires de copies de D ;
- **le lemme de raccord** est la condition de jumeaux e(X) + e(Y) − e(X, Y) = 3m, en usage depuis le 08/10.

**Seul apport nouveau : une preuve à la main de l'unicité de D = B7.** Codex l'obtenait par recensement machine. Elle est utile pour une rédaction, mais sans effet sur la fenêtre des rangs.

**Section 7 (réseau lointain).** L'équivalence « min Λ_3(T) ≥ 16 ⟺ F ne contient ni H12 ni H14 induit » est correcte et immédiate. Elle ne rapproche pas d'une exclusion :
- **NOTE_RESEAUX_DE_DROITE.md §4** (LAB, 09/10) : Hermite–Blichfeldt donne, dans Λ_3(T), un vecteur de norme ≤ 30 au rang 37 (≤ 38, 48 et 60 aux rangs 39, 41 et 43). Une exclusion demande une minoration au-dessus de ces bornes, pas 16.
- **note 110** (25/09) : la route Minkowski est close. La paire de Petersen, vecteur ±1 de norme 20, passe tous les comptages, et les supports vont jusqu'à 36 sommets.
- **NOTE_MANDAT_REPRESENTATION_2026-10-19.md §7 (pont P2)** : sans hypothèse, le lemme de trou lointain est faux localement. Prenons une droite L en prisme avec T, contenue dans deux grilles L ∪ K et L ∪ K′ qui évitent T. Alors χ_K − χ_K′ appartient à Λ_3(T) et a la norme 12 : c'est un H12 dans F.

## Conséquence

Rien à relancer. Le palier de normes 16 à 30 reviendrait à recenser les supports spéciaux jusqu'à 15 sommets, avec des coefficients ±2 dès la norme 18. L'archive a poussé ce recensement jusqu'à l'ordre 10 (LAB, 08/10, census2.py) sans exclusion, et la route Minkowski est close depuis la note 110.

## Annexe : texte transmis (ChatGPT, 20/10/2026)

Conway-99 : les fonctions propres entières de valeur 3 et de norme carrée inférieure à 16

20 octobre 2026 — Déduction établie dans cette reprise de recherche.

Portée

Cette note ne démontre ni la non-existence de Conway-99, ni l'exclusion d'une branche c_min.
Elle donne une classification humaine des supports des fonctions propres entières de valeur 3 dont la norme carrée est strictement inférieure à 16.
La géométrie des deux prismes anticomplets est déjà étudiée dans les notes 179 et 194 du dépôt. Elle n'est pas revendiquée comme nouvelle. Le palier 14 et le raccord ci-dessous sont démontrés ici ; leur nouveauté vis-à-vis de toute l'archive et de la littérature n'est pas établie.

Source de coordination consultée : amazing-source/conway99-c1, commit 23f8bde77d17d0a301b1a57cf90fabbf7a1d6acb. Les arguments de cette note n'utilisent aucun verdict de solveur, aucune fenêtre de rang modulo 7 et aucune exclusion d'automorphisme.

1. Théorème

Soit A l'adjacence d'un hypothétique srg(99,14,1,2), et soit f un vecteur entier non nul vérifiant Af=3f. Si ||f||²<16, alors f ne prend que les valeurs 0,+1,-1 et l'un des deux cas suivants se produit.

Norme carrée 12. Les supports positif et négatif ont chacun six sommets. Chacun induit un prisme triangulaire K3 carré K2. Ils sont disjoints et anticomplets. On appelle H12 leur réunion disjointe.

Norme carrée 14. Les supports positif et négatif ont chacun sept sommets. Chacun induit le graphe B7 suivant :

• sommets 0,1,2,3,4,5,6 ;
• arêtes 01,02,03,04,12,34,15,35,26,46,56.

Le sommet 0 est son unique sommet de degré quatre ; les six autres ont degré trois. Les deux copies de B7 sont reliées par exactement une arête, joignant leurs sommets de degré quatre. On appelle H14 ce graphe à quatorze sommets.

Réciproquement, toute copie induite de H12 ou H14 dans le graphe hypothétique produit une fonction propre entière de valeur 3 : +1 sur une copie, -1 sur l'autre, zéro ailleurs.

2. Réduction aux coefficients 0,+1,-1

La régularité donne 14 sum(f)=sum(Af)=3 sum(f), donc sum(f)=0.
Soit W la somme des coefficients positifs, égale à la somme des valeurs absolues des coefficients négatifs.

Supposons qu'un coefficient ait valeur absolue a>=2. Quitte à remplacer f par -f, on choisit v avec f(v)=a. L'équation en v implique

3a = sum_{u~v} f(u) <= W-a,

puisque les contributions négatives ne peuvent qu'abaisser la somme et que v n'est pas son propre voisin. Donc W>=4a.

Pour tout entier t>=0, t²>=t. Sur le côté positif, le coefficient a ajoute en outre a²-a. Ainsi

||f||² >= (W+a²-a)+W >= a²+7a >=18.

Cela contredit ||f||²<16. On a donc f dans {0,+1,-1}^99. Par sum(f)=0, ses supports P et Q ont même taille p, et ||f||²=2p.

3. Une borne de degré pour les petits supports

Pour v dans P, l'équation propre s'écrit

d_P(v)-d_Q(v)=3.

Le graphe induit sur P a donc degré minimum au moins trois, et de même pour Q.

Soit H un sous-graphe induit sur p sommets, de degré minimum au moins trois, respectant les bornes de voisins communs lambda<=1 et mu<=2. Pour v de degré d dans H, on compte les chemins de longueur deux issus de v, sans retour à v :

sum_{u~_H v}(d_H(u)-1) >=2d.

En les comptant par extrémité, il y en a au plus un pour chacun des d voisins de v et au plus deux pour chacun de ses p-1-d non-voisins. Donc

2d <= d+2(p-1-d),  soit  3d<=2(p-1).             (1)

Si p<=5, (1) contredit d>=3. Ainsi p>=6. Comme 2p<16, il reste seulement p=6 ou p=7.

4. Le cas p=6

L'inégalité (1) impose d<=3. H est donc cubique. Son complément sur six sommets est 2-régulier et simple : c'est C6 ou la réunion de deux triangles. H est respectivement le prisme triangulaire ou K3,3.

K3,3 est interdit : deux sommets d'une même part ont trois voisins communs. H est donc le prisme triangulaire.

Pour tout v dans P, d_P(v)=3 impose d_Q(v)=0. Les deux prismes sont anticomplets. Cela donne H12.

5. Le cas p=7 : unicité de B7

L'inégalité (1) impose d<=4. Un graphe 3-régulier sur sept sommets est impossible par parité de la somme des degrés. Il existe donc un sommet v de degré quatre.

Pour ce sommet, les deux bornes du comptage précédent valent exactement huit. L'égalité force simultanément :

• les quatre voisins de v ont degré trois ;
• chacun de ces voisins a exactement un voisin parmi les quatre ; ils induisent donc deux arêtes disjointes ;
• chacun des deux non-voisins de v a exactement deux voisins parmi les quatre.

Notons les voisins 1,2,3,4, avec les arêtes 12 et 34 ; notons les deux non-voisins 5 et 6. Les sommets 5 et 6 doivent être adjacents, car ils ont déjà deux voisins parmi les quatre et doivent avoir degré au moins trois. Leur degré est alors exactement trois.

Chaque sommet de {1,2,3,4}, déjà adjacent à v et à son partenaire, doit être adjacent à exactement un des deux sommets 5,6. Les deux voisins de 5 ne peuvent former l'une des arêtes 12 ou 34 : cette arête aurait v et 5 comme voisins communs. Ils prennent donc un sommet dans chaque paire. A relabellisation près, 5 voit 1,3 et 6 voit 2,4.

Le graphe est exactement B7, avec v=0. Tous les autres sommets ont degré trois, donc v est l'unique sommet de degré quatre.

Appliqué à P et Q, cela montre que seuls leurs sommets de degré quatre peuvent avoir un voisin dans l'autre support. Chacun doit en avoir exactement un. L'unique arête entre les deux supports relie donc ces deux sommets. Cela donne H14.

6. Le raccord global est automatique

Voici un principe utile qui n'exige aucune vérification des sommets extérieurs au support.

Lemme. Soit S un ensemble de sommets, H=A[S,S], et z un vecteur réel indexé par S tel que Hz=3z et sum(z)=0. Alors son prolongement f par zéro est un vecteur propre de A de valeur 3.

Preuve. L'identité SRG donne

(A-3I)² = 21I-7A+2J.

Par suite,

||(A-3I)f||²
  =21||f||²-7 f^T A f+2(sum(f))²
  =21||z||²-7 z^T H z
  =0.

Donc (A-3I)f=0. Cette preuve utilise la symétrie matricielle de A, pas un automorphisme du graphe.

Pour H12 et H14, prendre z égal à +1 sur le premier support et -1 sur le second vérifie exactement les deux hypothèses. Cela démontre les réciproques du théorème.

Le mot « induite » est indispensable : des arêtes supplémentaires entre ou dans les deux supports modifieraient Hz.

7. Application exacte à la piste des réseaux lointains

Pour une droite T, soit F l'ensemble des soixante sommets sans voisin dans T. Posons

Lambda_3(T)={f dans Z^99 : Af=3f et f=0 hors de F}.

Alors :

• Lambda_3(T) contient un vecteur de norme carrée 12 si et seulement si A[F,F] contient H12 comme sous-graphe induit ;
• Lambda_3(T) contient un vecteur de norme carrée 14 si et seulement si A[F,F] contient H14 comme sous-graphe induit ;
• son minimum est au moins 16 si et seulement si A[F,F] ne contient aucun de ces deux graphes induits.

L'équivalence ne suppose ni c(T)=1, ni une coclique de Hoffman, ni un automorphisme. Elle vaut pour toute droite du graphe hypothétique.

Cela transforme complètement le premier palier de la recherche d'un « trou de normes » en deux configurations combinatoires précises. Cela ne démontre pas que ces configurations sont impossibles. La borne d'Hermite envisagée dans l'archive allant jusqu'à 30, il faudrait encore traiter les normes 16 à 30, ou trouver une autre façon de neutraliser les vecteurs admissibles. Les normes annoncées « typiques » dans l'archive ne sont pas des bornes uniformes sans contrôle supplémentaire.

8. Statut et contrôle

La preuve des sections 2 à 6 est entièrement à la main. verify.py contrôle exactement les deux graphes explicites, les bornes de voisins communs, les fonctions signées et le second moment du bord qu'exigerait une complétion. Il ne vérifie pas l'existence d'une complétion ; les graphes supports ne sont pas des contre-exemples au problème de Conway.

python3 verify.py

Le résultat est une classification de supports, pas une exclusion de H12 ou de H14. Il n'a pas été relu indépendamment par un mathématicien ni formalisé.
