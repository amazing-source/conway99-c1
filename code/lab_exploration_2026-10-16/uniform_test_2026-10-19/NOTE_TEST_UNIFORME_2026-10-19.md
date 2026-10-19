# Test uniforme : note de départ (19/10/2026)

But fixé par l'utilisateur : une route se juge à son théorème. Il doit tuer 100 % des cas, et seule la difficulté de
certains cas peut ralentir. On cherche donc comment balayer c = 1, 2 et 3 d'un coup, par une liste finie d'objets et un
contrôle déterministe, à la manière des 156 réseaux de C2. À défaut, on accepte des solveurs, mais avec des preuves
vérifiées et un encodage « à la pointe ».

## 1. Définitions (à la racine r)

- 14 lettres, en 7 droites ; 84 étiquettes, chacune étant une paire de lettres de droites différentes.
- B est l'adjacence entre étiquettes : 12-régulière, B² + B = 12 I + 2 J − UᵀU, où U est l'incidence lettres/étiquettes.
- Quotas : une étiquette w a exactement 2 − [l ∈ w] − [l' ∈ w] voisins parmi les étiquettes qui contiennent la lettre l
  (l' est l'autre lettre de la droite de l).
- Rectangle F = Q_ab (4 étiquettes) : H_F = W_F − B g_F, avec W_F(w) = base(q(w), F).

## 2. Faits vérifiés ici (dérivés des seuls λ = 1, μ = 2 et des quotas)

1. **H_F est un vecteur propre pour −4.** B H_F = −4 H_F et U H_F = 0 ; prolongé par 0 sur la racine et les lettres,
   c'est un vecteur propre du graphe entier.
2. **Normes et produits.** ‖H_F‖² = 56 − 14 e_F ; ⟨H_F, H_G⟩ = 7 Σ_{w ∈ G} H_F(w).
3. **Le c d'une droite est un invariant d'arête.**
   - La droite a de r est l'arête opposée à r dans son triangle. Ses 24 étiquettes sont N(x) ∪ N(y) privé de {r, x, y}.
   - Elles forment un graphe 2-régulier : des cycles de longueur 4k qui alternent arêtes « même lettre » (droites par x
     ou par y) et arêtes « croisées ».
   - Chacune des 693 arêtes est la droite d'une seule racine, le troisième sommet de son triangle.
4. **Grille = sous-grille 3×3 de la géométrie PQ(2,6,2).** La somme sur les racines du nombre de rectangles grilles vaut
   9 G, où G est le nombre de sous-grilles. Les cycles de longueur 4 en une arête sont les prismes dont elle est un
   barreau.
5. **Étoile pleine.** Si les 6 rectangles d'une droite L sont des grilles à la racine r, c'est vrai aussi aux deux autres
   points de L. Les 36 voisins de L se répartissent alors en 12 droites parallèles (m_3(L) = 12).
6. **Décomposition des 12 voisins d'une étiquette.**
   - 2 à 4 voisins sont des arêtes « même lettre » ou « croisées » (structures de droites).
   - Les autres, 8 à 10, relient des rectangles disjoints.
   - Pour une grille F, ces arêtes forment un couplage parfait avec chaque rectangle disjoint de F.

## 3. Mécanismes candidats et premiers essais

- **Ordre 1 = ZC (Codex).**
  - Le catalogue exact des états z d'une étiquette est l'ensemble des solutions entières de C z = b_q, bornées.
  - Les multiplicités d'états doivent vérifier deux identités : K symétrique, et Zᵀ Z + K = D (λ et μ par paires de
    rectangles).
  - Le certificat de Farkas est relu en entiers, sans solveur.
  - Bilan : 7 361 des 10 052 gabarits c = 3.
- **Ordre 2 (sonde `z2_probe.py`).**
  - Il ajoute les nombres d'arêtes M entre types, et l'équation propre de chaque H_F sommée sur chaque type. C'est λ/μ
    raffiné type par type, et cela implique les identités de ZC.
  - L'option `--corners` ajoute une distribution par coin, le graphe interne de chaque rectangle avec E3, et les sommes
    de h par lettre (U H = 0).
  - Contrôles :
    - le cas « tout-grille » est faisable ;
    - gz 5128 (certificat ZC) est infaisable ;
    - gz 10006 reste faisable même avec les coins.
  - Le témoin de 10006 est fractionnaire à 97 % : 190 types sur 196. **L'écart restant vient de l'intégralité.**
- Pistes suivantes, toutes à preuve vérifiable :
  - coupes entières explicites ;
  - certificats modulaires : une fonctionnelle φ et un module m tels que Σ_w φ(état_w) ≢ cible (mod m) ;
  - programmation linéaire en nombres entiers avec certificat d'arbre (VIPR) ;
  - choix de la racine : maximiser c_min ou le nombre de grilles sur les 99 racines d'un éventuel graphe.
- **Calibration en cours** : 40 gabarits exclus sans ZC et les 40 ouverts. Elle mesure le gain de l'ordre 2 sur l'ordre 1.

## 4. Résultats du 19/10 (après-midi)

### Certificats

- **Outillage.**
  - `z2lib.py` construit le système entier et trouve un certificat de Farkas (programme linéaire élastique, arrondi
    rationnel, réparation par les bornes).
  - `z2_verify.py` est un vérificateur indépendant, en bibliothèque standard seulement : il refait son propre catalogue
    d'états et calcule les coefficients colonne par colonne.
- **Relecture adversariale : saine, sous E3.** Retirer les lignes E3 rend tous les programmes linéaires faisables.
  - B H_F = −4 H_F a été redérivé autrement.
  - Les états ont été comptés par trois énumérations indépendantes, identiques.
  - Les certificats volontairement faussés sont tous rejetés.
- **Certificats valides.**
  - gz 5986 et 5984 : **nouvelles fermetures**.
  - gz 9748 : deuxième preuve. Codex l'avait déjà fermé le 18/10 (84373a67, borne d'histogramme S_F ≤ 24), et le
    registre l'avait manqué.
  - gz 9997 et 5128 : calibration.
- **Registre c = 3 : 40 → 37 ouverts.** Règles Z2C et CXC, fichiers `z2_certified.json` et `codex_extra_closures.json`.

### Passe unique, sans certificat (demandée par l'utilisateur)

`z2_sweep.py` a tourné sur AWS Spot (c7a.32xlarge, 17 min). Sur 9 752 des 10 052 gabarits ; les 300 plus gros sont en
cours :

| Résultat | Gabarits |
|---|---:|
| Infaisables | 7 354 (75 %) |
| Faisables | 1 649 |
| Non tranchés (points intérieurs, à reprendre au simplexe) | 749 |

Croisement avec les méthodes du registre :

| Groupe | Tués par l'ordre 2 |
|---|---:|
| Déjà exclus sans solveur (ZC, etc.) | 6 428 (737 non tranchés) |
| Exclus seulement par SAT + RUP | **913** sur 2 436 |
| Exclus seulement par un verdict de solveur | **10** sur 30 |
| Ouverts | 3 sur 34 |

Couverture sans solveur dans la preuve, une fois les certificats faits : **8 395 gabarits** (au lieu de 7 469).

### Couches essayées sans gain en programme linéaire

- Coins, lettres et graphe interne : 29 ouverts sur 29 restent faisables.
- Triangles (λ = 1 exact par étiquette, cohérence des motifs) : 4 sur 4.
- Filtre d'états exact par sommet (`state_filter.py`) : aucun état retiré sur 9748 ni sur 10006.
- **Diagnostic.** L'obstruction des survivants est globale et tient à l'intégralité : le témoin de 10006 est
  fractionnaire à 97 %, et un MILP sur n entiers n'a pas conclu en 500 s.
- **Pistes.**
  - Les bornes d'histogrammes de Codex (S_F ≤ 24, « colonnes courtes »), qui ne sont pas encore dans l'ordre 2.
  - Des découpages en cas exacts, avec un certificat à chaque feuille.
  - Le choix de la racine.
