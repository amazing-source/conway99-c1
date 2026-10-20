# Dissection du graphe S3 : d'où viennent ses 6 automorphismes (20/10/2026)

**Objet.** Le srg(378,52,1,8) de la graine 1. Il provient d'un hémisystème du quadrangle généralisé FTWKB(5), d'ordre
(25,5), construit le 14/10 (`ftwkb5_data/`, NOTE_LAMBDA1 §2).

**Question de l'utilisateur.** Comment atteint-on exactement |Aut| = 6, et peut-on descendre plus bas ?

**Scripts.** `s3_dissection/dissect_s3.py`, `dissect_more.py`, `dissect3.py`. Ce sont trois calculs d'environ 70 s
chacun, un seul processus.
- Le groupe est recalculé exactement avec le pipeline de `srg_group3.py`.
- Chaque automorphisme est vérifié arête par arête.
- Chaque automorphisme est relevé au quadrangle. Un point du quadrangle correspond à un triangle du graphe, puisque ses
  3 droites d'hémisystème se coupent deux à deux en ce point.
- On vérifie que chaque relèvement envoie les 756 droites du quadrangle sur des droites. Ce sont donc des
  collinéations.

## Résultats (exacts)

1. **Le groupe.** Aut = S3 : trois involutions et deux éléments d'ordre 3. Les orbites de sommets ont pour tailles
   1, 2 (quatre fois), 3 (cinq fois) et 6 (59 fois).
2. **Chaque involution fixe une grille 6 × 6.** C'est un sous-quadrangle d'ordre (5,1) : 36 points et 12 droites,
   6 points par droite, 2 droites par point.
   - Une classe de parallélisme de la grille est **entièrement dans l'hémisystème** : 6 droites, soit les 6 sommets
     fixés du graphe.
   - L'autre classe est **entièrement hors de l'hémisystème**.
   - Les trois grilles partagent la droite 751, qui est dans H, et la droite 226, qui n'y est pas.
3. **Chaque élément d'ordre 3 fixe un triade régulier et son orthogonal.**
   - Le triade est T = {3170, 3213, 3230} : trois points deux à deux non alignés, dont les 6 droites sont toutes fixes.
   - Son orthogonal est T^⊥ = {849, 3275, 99, 799, 1024, 1074} : les 6 points alignés avec les trois.
   - Cela fait 9 points fixes et 18 droites fixes, chaque droite fixe joignant un point de T à un point de T^⊥. Sur
     ces 18 droites, 9 sont dans H : 9 sommets fixés.
4. **Le groupe entier fixe le chemin a — b — c.**
   - a = 849 et c = 3275 ne sont pas alignés, et b = 3170 appartient à {a, c}^⊥.
   - La droite bc est la droite 751, dans H : c'est le sommet fixé par tout le groupe.

## Pourquoi 6, et pourquoi pas moins dans ce monde

- **La borne par rareté.** Le groupe de FTWKB(5) est d'ordre 9 000 000. D'après la classification de
  Bamberg–Giudici–Royle (arXiv 1012.3819, Thm 1.1), il y a N = 3 180 000 hémisystèmes. Une orbite a donc au plus N
  éléments, et chaque stabilisateur est d'ordre au moins 9·10⁶ / N > 2,8, donc au moins 3.
  - C'est rigoureux, une fois N connu par la classification.
- **Le minimum effectif est 6 (S3).** La classification le dit, et la dissection montre sa forme : les symétries sont
  des collinéations du quadrangle qui fixent des sous-structures classiques (grilles, triades réguliers).
- **Pour descendre sous 6, il faut sortir des hémisystèmes des deux quadrangles connus d'ordre (25,5).** Deux voies
  seulement :
  - un nouveau quadrangle de cet ordre, ce qui serait un résultat majeur de géométrie finie ;
  - un srg(378,52,1,8) qui ne vient pas d'un hémisystème. On ne sait ni s'il en existe un, ni si tous en viennent.

## Ce que cela dit de l'idée « λ = 1 force la symétrie »

- Dans les exemples connus, **les symétries viennent de la géométrie ambiante**, le quadrangle et son groupe, et non de
  λ = 1 lui-même. La rareté rend la symétrie inévitable *dans un hôte donné*.
- **Contraste avec Conway.** Dans le graphe S3, une involution fixe 6 sommets et une grille entière. Dans un Conway, les
  paramètres forcent une involution à fixer **un seul sommet**, ce qui ne donne aucune structure fixe riche. C'est
  exactement ce que la route C de C2 a exploité pour exclure l'ordre 2.
- **Version Conway de l'argument de rareté.** L'hôte canonique est le cadre d'un sommet, de groupe d'ordre 645 120. Il
  faudrait montrer que le nombre N de complétions étiquetées du cadre est inférieur à 645 120. Personne ne sait borner
  N sans résoudre le problème.
- **Ce qui manque donc à cette voie** : un hôte pour Conway où l'on sache compter les solutions. Aucun n'est connu (voir
  CARTE_MAITRESSE §4.H et R2-12).
