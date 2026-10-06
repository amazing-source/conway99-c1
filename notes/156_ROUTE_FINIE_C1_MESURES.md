# 156 — Une « route (C) » pour C1 ? Mesures (06/10, soir)

*Question de l'utilisateur : peut-on, comme pour C2 (route (C) : 156 réseaux, ~9 000 h CPU sur AWS), ramener C1 à un calcul
fini de coût maîtrisé ? Réponse courte : **pas par les voies mesurées ici**. Code : `code/b18/`.*

## 1. Pourquoi la route (C) existe pour C2
- L'involution coupe l'espace propre −4 en deux.
- On obtient un repère de 51 vecteurs dans un réseau unimodulaire impair **de rang 24**, de minimum ≥ 2.
- En rang 24, tout est classifié : la table de Borcherds donne **156 réseaux**.
- Il reste à épuiser le repère dans chacun (frame_dfs + étage h), d'où ~9 000 h CPU.

## 2. L'analogue direct est impossible pour C1
Sans symétrie, le réseau naturel a un rang de 44 à 48 :
- T, de rang 44 et de déterminant 441, porteur de 99 marques formant un repère tendu Σ(u, w_x)² = 7|u|² ;
- ou M, unimodulaire pair de rang 48 (passation §7).

Masse de Smith–Minkowski–Siegel des réseaux unimodulaires pairs (calcul exact) :

| rang | 24 | 32 | 40 | 48 |
|---|---|---|---|---|
| masse | 7,9·10⁻¹⁵ | 4,0·10⁷ | 4,4·10⁵¹ | **1,5·10¹²¹** |

En rang 48, il y a donc plus de 10¹²¹ classes. Énumérer les « enveloppes » est hors de question, quelle que soit la
puissance de calcul. Le genre de T en rang 44 est du même ordre.

## 3. Candidat combinatoire : la branche 18 par complément étoilé (valeur propre 3)
**L'idée.**
- Le noyau H = support (18) ∪ X = E₂ (18) ∪ T = E₀ (9) a 45 sommets.
- Il porte f = 3s + 1_X − 1_T, avec Af = 3f + 7·1 et Σf = 63 ≠ 0.
- Si K_H est de rang 44, H est un complément étoilé de la valeur propre 3. Les 54 sommets de S sont alors reconstruits
  par colonnes, et leurs adjacences mutuelles sont forcées.

**Niveau 0 : les supports (`supports.py`, `genbg` de nauty).**
- Il y a 26 classes colorées, **25 à transposition près**, comme dans la passation.
- Tous les supports sont connexes : l'isomorphisme non coloré correspond donc bien à l'échange des signes.

**Niveau 1 : les configurations X (`xcount.c`, `xlevel.py`).**
- **Données forcées.** La paire positive {p, p'} apparaît avec la multiplicité 2 − |ligne_p ∩ ligne_p'|, et la paire
  négative de même : il y a 18 emplacements de chaque côté. X est donc une bijection entre ces emplacements.
- **Contraintes exactes.**
  - λ sur les arêtes u–p et u–v : |ν ∩ ligne_p| ≤ 1 et |π ∩ colonne_v| ≤ 1 ;
  - x(p, v) ≤ 2 − D[p][v] ;
  - |π ∩ π'| + |ν ∩ ν'| ≤ 2.
- **Comptes.** Estimateur de Knuth sur 2·10⁵ chemins par support, écart-type relatif ≈ 3 % :
  - de **2,5·10⁷ à 3,0·10⁹ configurations étiquetées** par support, **2,75·10¹⁰ au total** ;
  - |Aut(D)| va de 1 à 72, donc il reste **~8,4·10⁹ configurations à symétrie près**.
- **L'estimateur est validé.** Le comptage exact du support 24 donne 25 548 884 configurations (1 min 45 s), contre
  2,54·10⁷ ± 1,6·10⁶ estimés.
- L'énumération brute coûte ~4 µs par configuration, soit déjà ~30 h CPU pour le seul niveau 1.
- **Aucun test bon marché ne tue au niveau 1.** Sans arête X–X, λ_min(K) sur support ∪ X a une médiane de −1,2 et vaut
  −3,3 au pire, sur 1 000 échantillons. Les arêtes X–X forment une forêt d'au plus 9 arêtes, de norme spectrale ≤ 2 :
  elles peuvent déplacer λ_min jusqu'à 18. Rien n'est donc exclu.

**Niveau 2, non énuméré.**
- Il faut encore choisir les arêtes internes de X (e ≤ 9), les 9 sommets T et leurs arêtes internes, puis les 36 + 2e
  arêtes X–T, sous les contraintes d_T = d_X + 2 sur X et d_X = d_T + 4 sur T.
- Chaque configuration X se multiplie donc encore par un facteur très grand.

**Coût.** Même à 1 s par configuration X pour tout le reste, ce qui est optimiste, la branche 18 seule demanderait
**8·10⁹ s ≈ 2,3·10⁶ h CPU, soit ~250 fois la route (C)**. Les branches 26 et 37 restent en dehors de ce chiffre.

## 4. Conséquences
- Il n'existe pas, dans l'état actuel, de route finie pour C1 d'un coût comparable à la route (C) de C2.
- La raison est structurelle. C2 bénéficie d'une réduction de dimension (l'involution) et d'une classification (rang 24).
  C1 n'a ni l'une ni l'autre.
- Les germes combinatoires naturels explosent dès le premier niveau sans test qui tue (branche 18 ici, V7 en note 155).
- **Ce qu'il faudrait pour en obtenir une**, au choix :
  - un théorème forçant beaucoup plus de structure au niveau 1, par exemple fixant les arêtes internes de X et T à partir
    du support ;
  - un germe dont le comptage tombe vers 10⁶ ;
  - une réduction à un réseau de rang ≤ 24, ce qui demande une idée qui manque pour l'instant.
- Le test de classe de la note 155 reste l'élagage le plus fort trouvé. Il ne devient décisif que sur des germes de plus
  de 30 sommets, dont le nombre est justement ce qui explose.

## 5. Fichiers (`code/b18/`)
- **Supports** : `supports.py` (générateur Python, abandonné au profit de genbg) ; `supports18.json` (les 25) ;
  `bip_raw.g6`, `bip_keep.g6`.
- **Niveau 1** : `xlevel.py` (référence Python) ; `xcount.c` (comptage exact, `dump`, estimateur `knuth N graine`) ;
  `run_xcount.py`.
- **Test de positivité** : `xsample.py`.
