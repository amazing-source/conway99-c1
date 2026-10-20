# Ordre 2 en 7 sur l'étoile d'une droite : ce qui existe, et pourquoi presque rien n'agit avant 7 lointains

LAB, 20/10/2026, soir.

**Questions.**
1. Vérifier UᵀU ≡ 0 (mod 7) et écrire tout le système mod 49.
2. Surtout : trouver des conditions 7-adiques d'ordre ≥ 2 **locales**, sur l'étoile d'un proche x ou sur la double étoile
   (x, x̄).
3. Mesurer leur force sur les entrées star39 du rang 39.

**Statuts.**
- **P** : preuve écrite ici. Un agent l'a relue (lecture seule, §0.9), pas un humain.
- **A** : déjà dans l'archive (fichier:ligne).
- **E** : calcul exact ou mesure. Scripts et sorties dans `ordre2_2026-10-20/`.
- **H** : heuristique.
- **X** : ouvert.

**Cadre** (NOTE_OBSTRUCTION §1, NOTE_BOOST §2.3).
- Droite générique T : c = 1 et 7 ∤ τ. Rang r = 37 + ρ, avec ρ = 2k ∈ {0, 2, 4, 6}.
- H = 3I − R − EᵀZE + J/9 = 7Π_T (A).
- H ≡ −UDUᵀ (mod 7), avec les conventions du moteur : R = 4 − g + uᵀDu′ et, sur la diagonale, uᵀDu = g
  (A, star39_prep.py).
- Λ₋(T) est le réseau des vecteurs propres entiers de valeur −4 nuls hors de F. Il est de rang 8 (A, RD:14).

---

## 0. Réponse courte

### 0.1 UᵀU ≡ 0 (mod 7) est vrai, mais c'est de l'ordre 1 (P)
- C'est simplement H² ≡ 0 (mod 7).
- Il y a plus fort, toujours d'ordre 1 : les colonnes de U, prolongées par 0 sur N[T], sont dans ker M ∩ Im M. Autrement
  dit, EU ≡ 0, (R − 3I)U ≡ 0 et 𝟏ᵀU ≡ 0.
- C'est implicite dans RD §2 (A) : Im(H mod 7) est le radical de Λ₋(T)/7Λ₋(T).
- La seule partie locale est Σ_{a ∈ étoile(x)} u_a ≡ 0. Elle est automatique sur une étoile complète dès que
  rang U_S = ρ.

### 0.2 Système mod 49 complet (P, E)
- À l'ordre 49, H² = 7H équivaut à (M49). (M49) équivaut à (a) + (b), et l'ordre suivant donne (c) (§1.2).
- Ce n'est que la lecture mod 7 de la décomposition de Jordan Λ₋(T) ⊗ ℤ₇ ≅ U_{8−ρ} ⊥ 7U″_ρ (A, RD §2).
- Vérifié exactement sur des réseaux synthétiques : ρ = 2, 4, 6, deux relèvements, et un témoin négatif.

### 0.3 Contenu local exact (P)
- Soit X un ensemble de lointains. Tout ce que la structure 7-adique (à tous les ordres) peut dire de H_XX tient en une
  phrase : **H_XX est la Gram de |X| vecteurs du réseau M_T = U″_ρ ⊥ U_{8−ρ}(7)**.
- Constantes :
  - χ(det U″) = (−1)^{k+1}(τ|7) (A, RD:29-32) ;
  - **χ(det U_{8−ρ}) = (−1)^{k+1}** (P, déduit de det Λ₋(T) = 4·7^{2k}τ/(9j²), A, RD:21).
- Au rang 43, U₂ est donc un **plan anisotrope**.

### 0.4 Conséquence : la route « ordre 2 local » est close dans les cas génériques (P, E)
- **Cadre générique** : première couche pleine (rang₇ H_XX = ρ, de la bonne classe) et seconde couche s de corang ≤ 1.
  C'est là qu'est presque toute la masse des configurations.
- **Avant 7 lointains, dans ce cadre, à tous les rangs,** aucune condition d'ordre ≥ 2 n'agit (§2.3 (i) et (iii′)).
- **Hors de ce cadre, des conditions existent dès 6 lointains** (§2.3 (iv)). Leur classement reste ouvert (X).
  - Corang 2 de s à 6 lointains avec complément elliptique : rangs 37 à 41, probabilité de l'ordre de 7⁻³. C'est le
    contre-exemple du relecteur.
  - Première couche non pleine au rang 43, à 6 lointains : de l'ordre de 1 %.
- Tout cela vaut pour tout ensemble de lointains, donc aussi pour la double étoile (x, x̄) : les seuils ne dépendent pas
  de l'unité de recherche.
- **À 7 lointains, dans le cadre générique, une seule règle**, celle du corang 1 (§2.3 (iii), vérifiée sur réseaux
  synthétiques).
  - Si la seconde couche s est de corang 1 et si le plan complémentaire C est anisotrope, alors
    v₇(det H_XX) − (6 − ρ) est impair et ≥ 3.
  - Aux rangs 37, 39 et 41, elle ne joue que si s est de corang 1 (environ 1/6 des cas) et si C est anisotrope. Cela
    représente environ 7 % des configurations (H).
  - **Au rang 43, c'est la règle nouvelle (C43)** : C = U₂ est toujours anisotrope. Si rang₇ H_XX = 6 et det H_XX ≠ 0,
    alors **v₇(det H_XX) est impair**. Elle élimine 11 à 14 % des configurations de 7 lointains compatibles au premier
    ordre (E, six runs : graines 1, 2, 4, 5 et 6 avec x = 0, et graine 1 avec x = 2 ; positivité non imposée).
  - Ni l'une ni l'autre n'est dans l'archive (§2.6).
- **À 8 lointains, un seul bit.** C'est la partie en 7 de la condition de carré τ·det H₈₈ ∈ ℚ*², déjà connue (A).
  - Elle vient de LAP (TL:2338), confirmée par Codex (TL:2461-2463).
  - Elle est citée comme « Codex's note 217 » en NOTE_PROOFS_1410:257.
- **Autres premiers p ∤ 2·3·7·τ.** À 7 lointains, une règle de Legendre d'un bit par premier (§2.5, vérifiée), puis la
  classe carrée à 8 lointains (A).

### 0.5 Mesure (E) : sur ce qui a été parcouru, rien de ce qui agit à 6 lointains ou plus n'élague
- **Rang 37** : les recherches d'étoile meurent avec **au plus 3** lointains placés (3 entrées, arbres complets).
- **Rang 39** : elles meurent avec **au plus 5** lointains placés (5 entrées). Ce ne sont que des **préfixes** : 184 à 689
  branches de profondeur 1 sur 12 647 à 18 188, soit 1,0 à 5,4 % de chaque arbre.
- Le gain de toute condition d'ordre 2 est donc **nul sur ces préfixes**.
- La profondeur maximale des arbres complets du rang 39 n'est pas mesurée. Les runs complets du 20/10 n'ont atteint aucune
  feuille (NOTE_BOOST §5).

### 0.6 Sous-produit réel, valable à tout rang (P, E)
- Le second projecteur lointain, sur les vecteurs propres de valeur 3, est :

      7Π⁽³⁾ = H₃ = 4I + R − (2/35)J − Eᵀ(4I + G)⁻¹E ⪰ 0   (rang 18),        H + H₃ = 7(I − EᵀK⁺E).

- Contrôle positif, avec la formule générale pour k quelconque : sur deux srg(243,22,1,2) réels de l'archive, l'écart est
  ≤ 10⁻¹⁴.
- Le test « 7I − H ⪰ 0 » de star39 en découle. Constat empirique : il ne coupe **jamais**, 0 coupe sur les 10 runs où il
  est actif.
- H₃ ⪰ 0 coupe 5 229 fois, contre 85,7 M pour H ⪰ 0, soit −0,01 % de nœuds au rang 39. Il est inutile pour l'étoile.

### 0.7 Rangs 41 et 43
- Jusqu'à la profondeur ρ − 1, aucune condition arithmétique, ni en 7 ni ailleurs, ne peut agir (P, §5).
- À la profondeur ρ, seul agit le bit de classe de la première couche, et au rang 43 le cas dégénéré d'environ 1 %.
- Le haut de l'arbre n'est donc élagué que par la positivité et la combinatoire.
- L'ordre 2 n'y change rien d'utile : (C43) multiplie par 0,87 à la profondeur 7.

### 0.8 Prochaine étape (§6)
- Estimer par la méthode de Knuth la taille de l'arbre d'étoile « sans u » aux rangs 41 et 43, jusqu'à la profondeur
  ρ + 1, avec les filtres de cette note.
- Ce chiffre décide si une route droite par droite existe à ces rangs. Sinon, il faut un théorème global, une borne sur r.

### 0.9 Limites
- Les calculs ont été arrêtés à 16 h 33, quand l'utilisateur a repris le PC.
- La relecture adverse (agent) a rendu son avis après l'arrêt, sans rien exécuter.
  - Elle juge correctes les Prop. 1 et 2, le §2.2, le §2.3 (i) à (iii) avec (C43), le §2.5 et le §3.
  - Elle demandait trois corrections de portée et de mesure, et des corrections mineures. Toutes sont intégrées dans
    cette version.
- **Aucune preuve n'est relue par un humain.**
- La liste de ce qui n'a pas été vérifié est au §6 bis.

---

## 1. UᵀU ≡ 0 et le système mod 49

### 1.1 L'énoncé vérifié

**Proposition 1 (P).** Pour une droite générique, avec H ≡ −UDUᵀ (mod 7), U de rang ρ et D non dégénérée :
- (i) UᵀU ≡ 0 (mod 7) ;
- (ii) EU ≡ 0, (R − 3I)U ≡ 0 et 𝟏ᵀU ≡ 0 (mod 7).

De plus, (ii) et l'inclusion Ũ ⊂ Im M (étape 5) entraînent (i). (ii) seule ne suffit pas : ker M mod 7 n'est pas
totalement isotrope.

**Preuve.**
1. Π_T est le projecteur orthogonal sur W_T = {f : Ef = 0, Rf = −4f} (A, NOTE_BOOST §2.3).
   - Ses vecteurs sont orthogonaux aux lignes de E.
   - Ils sont orthogonaux à 𝟏, car 𝟏ᵀE = 6·𝟏ᵀ.
   - R agit par −4 sur W_T.
2. On a donc exactement HEᵀ = 0, (R + 4I)H = 0, H𝟏 = 0 et H² = 7H.
3. Mod 7, cela donne UD(UᵀEᵀ) ≡ 0, (R + 4I)U(DUᵀ) ≡ 0 et UD(Uᵀ𝟏) ≡ 0. Comme UD est injective et DUᵀ surjective, on
   obtient (ii), avec R + 4I ≡ R − 3I.
4. (ii) dit que les colonnes de Ũ (U prolongé par 0 sur N[T]) sont dans ker M, où M = A − 3I.
5. Elles sont aussi dans Im M.
   - Les colonnes de H sont dans 7Λ₋(T)^# ⊆ 7E₋^# = 7P₋(ℤ⁹⁹).
   - Or 7P₋ = M(A − 14I)/18, et 18 est une unité en 7. Donc Im(H mod 7) ⊆ Im(M mod 7). Cette justification est celle du
     relecteur.
   - C'est le sens combinatoire de ρ (A, NOTE_FUSION:69-70) : ρ(T) = dim(Im M ∩ {vecteurs nuls sur N[T]}).
6. Pour v = Mx et w ∈ ker M, on a v·w = xᵀMw = 0. D'où UᵀU = ŨᵀŨ ≡ 0. ∎

**Variante directe.** H² ≡ 0 entraîne UD(UᵀU)DUᵀ ≡ 0, donc UᵀU ≡ 0. Les deux arguments disent la même chose : Im(H mod 7)
est isotrope parce que c'est le radical de Λ₋(T)/7 (A, RD §2).

**Ce qui est local.** Soit S l'étoile de x. La ligne x de EU ≡ 0 donne Σ_{a∈S} u_a ≡ 0.
- Sur une étoile complète, H_SS𝟏 = 0 est automatique : marges et couplage, cf. l'en-tête de star39.cpp. Donc
  U_S D(Σ u_a) ≡ 0, et Σ u_a ≡ 0 dès que rang U_S = ρ (P).
- Les autres relations font toutes intervenir des lointains hors de l'étoile :
  - (R − 3I)U ≡ 0 en un lointain a ;
  - EU ≡ 0 en un proche v ≠ x ;
  - UᵀU ≡ 0.

### 1.2 Le système mod 49

**Notations.** On fixe des relèvements entiers U et D, et on pose :
- S = (H + UDUᵀ)/7, qui est 7-entière ;
- Q = UᵀU/7, entière par (i) ;
- K = {y : Uᵀy ≡ 0} = Im(U)^⊥, qui contient Im U ;
- C une matrice 60 × ρ telle que CᵀU ≡ I.

**Proposition 2 (P).**
1. À l'ordre 49, H² = 7H donne

       (M49)   UD(I + QD)Uᵀ ≡ UDUᵀS + SUDUᵀ   (mod 7).

2. (M49) équivaut à :
   - (a) UᵀSy ≡ 0 pour tout y ∈ K, c'est-à-dire S(K) ⊆ K ;
   - (b) N + Nᵀ ≡ Q + D⁻¹ (mod 7), où N = UᵀSCD⁻¹.
3. L'ordre suivant (mod 343) donne en particulier :
   - (c) yᵀ(S − S²)z ≡ 0 pour y, z ∈ K.
4. Ces énoncés ne dépendent pas du relèvement choisi.

**Preuve.**
1. On écrit H = −UDUᵀ + 7S, avec UᵀU = 7Q.
   - H² = 7UDQDUᵀ − 7(UDUᵀS + SUDUᵀ) + 49S², et 7H = −7UDUᵀ + 49S.
   - En divisant par 7 : UD(I + QD)Uᵀ − UDUᵀS − SUDUᵀ = 7(S − S²). Réduit mod 7, c'est (M49).
2. On décompose 𝔽₇⁶⁰ = K ⊕ Im C et on lit (M49) bloc par bloc.
   - Sur K × K, les deux membres sont nuls.
   - Sur K × Im C, il reste yᵀSUDb ≡ 0 pour tout b, c'est-à-dire (a).
   - Sur Im C × Im C, on encadre par Cᵀ et C, puis on multiplie par D⁻¹ des deux côtés : D⁻¹ + Q ≡ N + Nᵀ, c'est-à-dire (b).
3. Sur K × K, le membre de gauche de l'égalité exacte est divisible par 49, puisque yᵀU ≡ 0, zᵀU ≡ 0 et yᵀSU ≡ 0 par
   (a). Donc yᵀ(S − S²)z ≡ 0.
4. **Changement de relèvement.**
   - U → U′ = U + 7Y. On a C′ ≡ C, et :
     - S′ = S + YDUᵀ + UDYᵀ + 7YDYᵀ ;
     - Q′ ≡ Q + UᵀY + YᵀU.
   - Sur K, U′ᵀS′y ≡ UᵀSy, car UᵀU ≡ 0 et Uᵀy ≡ 0 : (a) est inchangé.
   - N′ ≡ N + UᵀY(DUᵀC)D⁻¹ = N + UᵀY. Les deux membres de (b) bougent donc de UᵀY + YᵀU : (b) est inchangé.
   - D → D + 7D′ change S de UD′Uᵀ et laisse Q et D⁻¹ mod 7 fixes. N bouge de UᵀUD′UᵀCD⁻¹ ≡ 0.
   - (c) est inchangé grâce à (a) et à UᵀU ≡ 0.
   - Cette vérification à la main est confirmée par le relecteur, et numériquement en §1.3. ∎

**Lecture en réseau.** On prend une base B = [B₀ | B₁] de Λ₋(T) ⊗ ℤ₇ adaptée à U ⊥ 7U″, avec B₀ᵀB₁ = 0, B₀ᵀB₀ = G₀
et B₁ᵀB₁ = 7G₁. Alors

    H = 7B₀G₀⁻¹B₀ᵀ + B₁G₁⁻¹B₁ᵀ.

- Avec U = B₁ et D = −G₁⁻¹, on obtient Q = G₁ et S = B₀G₀⁻¹B₀ᵀ.
- (a), (b) et (c) deviennent alors des identités.
- Le système mod 49 n'apporte donc **rien de plus** que la décomposition de Jordan (A, RD §2). La seule question
  nouvelle est ce qu'il en reste sur une étoile (§2).

### 1.3 Vérification (E)
Script `o2_m49_synth.py`.
- Réseau synthétique de rang 8 dans ℤ⁶⁰, de type U_{8−ρ} ⊥ 7U″_ρ, sans aucune hypothèse srg.
- H = 7·projecteur, en arithmétique exacte (sympy).

| ρ | graines | H² = 7H, rang₇ H = ρ | (i), (M49), (a), (b), (c), relèvement 1 | idem avec U + 7Y, D + 7D′ | témoin H + 7(E_ab + E_ba) |
|---|---|---|---|---|---|
| 2 | 1, 4 | oui | tout vrai | tout vrai | (M49), (a), (c) faux |
| 4 | 2 | oui | tout vrai | tout vrai | (M49), (a), (b), (c) faux |
| 6 | 3 | oui | tout vrai | tout vrai | (M49), (a), (b), (c) faux |

---

## 2. Ce que l'ordre 2 et au-delà peut dire d'une étoile

### 2.1 Le principe (P)
- Les vecteurs Π_T e_a, pour a ∈ F, sont dans le dual Λ₋(T)^#, et H_ab = 7·(Π_T e_a · Π_T e_b).
- Pour X ⊂ F, H_XX est donc la Gram de |X| vecteurs de M_T := Λ₋(T)^#(7) ≅ U″_ρ ⊥ U_{8−ρ}(7).
- C'est la condition 7-adique locale la plus forte, tous ordres confondus : toute condition sur H_XX qui ne dépend que de
  la classe de Λ₋(T) ⊗ ℤ₇ en découle.
- La première couche (H_XX mod 7 de rang ≤ ρ, forme de classe fixée) est celle que le moteur impose déjà, par u et D.
- **Pas de colle en 7 (P).** On pourrait craindre que la configuration entière N[T] ∪ X, vue dans E₋^#(7), en dise plus que
  sa partie lointaine.
  - Ce n'est pas le cas : pour une droite générique, le Gram proche, ramené à l'échelle (3I − G + J/9), a pour
    déterminant 144τ, qui est une unité en 7 (RD:23-24).
  - Le réseau proche se détache donc de E₋^#(7) : E₋^#(7) = N_proche ⊥ M_T.
  - Les composantes proches des lointains sont fixées par les noms et entières.
  - La représentabilité de 7P sur N[T] ∪ X se ramène ainsi exactement à celle de H_XX par M_T.
- **Ce que la règle couvre.** Elle vaut pour tout X ⊂ F : étoile, double étoile (x, x̄), droite complète.
  - Vue depuis la droite latérale T_x, la double étoile est le même ensemble de sommets N[T_x] ∪ F′.
  - La droite latérale n'apporte donc aucune condition 7-adique locale supplémentaire (P, même argument).

### 2.2 Les constantes

| rang | ρ | couche 1 : U″_ρ, χ(det) | couche 2 : U_{8−ρ}, χ(det) | indice de Witt de U_{8−ρ} mod 7 |
|---|---|---|---|---|
| 37 | 0 | — | U₈ : −1 | 3 |
| 39 | 2 | (τ\|7) (A, RD:31) | U₆ : +1 | 2 |
| 41 | 4 | −(τ\|7) | U₄ : −1 | 1 |
| 43 | 6 | (τ\|7) | U₂ : +1 | 0 : **plan anisotrope** |

**Preuve de la colonne 4 (P).**
- 7Π_T est 7-entière. Λ₋(T) ⊗ ℤ₇ n'a donc que les échelles 1 et 7 (A, RD §2).
- On en tire det Λ₋(T) = det U · 7^{2k} · det U″, à un carré d'unité près.
- RD:21 (A) donne det Λ₋(T) = 4·7^{2k}τ/(9j²). Comme la valuation en 7 vaut exactement 2k, 7 ∤ j.
- Donc χ(det U)·χ(det U″) = χ(τ), puis χ(det U) = (−1)^{k+1}.

**Indice de Witt.** Sur 𝔽₇, une forme non dégénérée de dimension 2n est hyperbolique si et seulement si (−1)ⁿ·det est un
carré, et −1 n'est pas un carré mod 7. Cela donne la dernière colonne.

**Cohérence.** Au rang 37, on retrouve par une autre voie l'énoncé « Σ/7 mod 7 est la Gram de vecteurs d'un espace de
dimension 8 de discriminant non résidu » (A, TL:3604-3607, session portable).

**Dépendances.** La colonne 4, et donc (C43), repose sur deux énoncés de l'archive.
- **χ(det U″) = (−1)^{k+1}(τ|7)** (RD:31, A non relu). C'est aussi la règle de δ qu'utilise star39_prep.
- **La partie unité de det Λ₋(T) est ≡ τ.**
  - Je la redérive ainsi : d(W_T) ≡ d(V₋)·d(P(ℚ^N)) modulo les carrés.
  - On a d(V₋) = det E₋ = 9·7^{r−1}, qui est un carré (A, RD:9 et CX).
  - On a d(P(ℚ^N)) ≡ 144τ/7³⁶ ≡ τ (Gram des projections proches, RD:23-24).

Si la première est fausse, U₂ peut être hyperbolique au rang 43, et (C43) tombe. La règle du corang 1 resterait vraie, avec
la classe corrigée.

**Deux appuis indépendants pour la classe de U_{8−ρ}.** Aucun n'est relu par un humain.
1. **Pas de colle en 7** (§2.1). Le réseau proche se détache de E₋^#(7). La partie unimodulaire de E₋ ⊗ ℤ₇, notée U_E, de
   rang 45 − r, est donc isométrique à U_{8−ρ}. Or RD:62 (session portable) dit qu'au rang 43, U_E est le plan anisotrope.
   Cela confirme U₂ anisotrope sans passer par RD:31.
2. **La dérivation du relecteur** (agent, 20/10, non revérifiée par moi). Elle part de RD:9-10 seuls :
   - c₂(V₋) = −1, car E₋ est pair de déterminant ≡ 1 mod 8 ;
   - c₃ = 1, car la partie en 3 du groupe discriminant est cyclique ;
   - la formule du produit donne alors c₇(V₋) = −1, en accord avec RD:36 ;
   - et c₇(V₋) = (−1)^k χ(det U_E).

   On en tire χ(det U_{8−ρ}) = (−1)^{k+1}, puis RD:31.

### 2.3 Le théorème de non-existence (P)

**Notation.** Dans ce paragraphe, m = |X| est le nombre de lointains. La lettre k garde le sens ρ = 2k.

**Théorème.** Soit X un ensemble de m lointains, avec rang₇ H_XX = ρ (première couche pleine, de la bonne classe) et H_XX
de rang réel m. Soit s la forme H_XX/7, restreinte à K_X = ker(H_XX mod 7), qui est de dimension m − ρ.
- **(i)** Si s est non dégénérée et m ≤ 7, H_XX est représentée par M_T : **aucune condition d'ordre ≥ 2**.
- **(ii)** Si s est non dégénérée et m = 8, la seule condition est χ(det s) = χ(det U_{8−ρ}) = (−1)^{ρ/2+1}. C'est la
  partie en 7 de τ·det H₈₈ ∈ ℚ*² (A).
- **(iii′) Corang 1, m ≤ 6 : aucune condition.**
  - Le complément de s₀ dans U_{8−ρ} est de rang 9 − m ≥ 3, donc isotrope.
  - Le vecteur radical peut s'envoyer sur un vecteur isotrope non nul, ce qui laisse e′ libre.
- **(iii) Règle du corang 1, à m = 7.** On suppose que s est de corang 1. Soit s₀ sa partie non dégénérée, de dimension
  6 − ρ, et C le plan complémentaire de s₀ dans U_{8−ρ}, avec det C ≡ det U_{8−ρ} · det s₀.
  - Si C est anisotrope, c'est-à-dire χ(−det C) = −1, alors v₇(det H_XX) − (6 − ρ) est **impair et ≥ 3**.
  - Si C est hyperbolique, il n'y a aucune condition.
  - **(C43).** Au rang 43 (ρ = 6), s₀ est vide et C = U₂ est toujours anisotrope. Avec le cas s ≢ 0, où v₇ = 1, on
    obtient : H_XX est représentée si et seulement si **v₇(det H_XX) est impair**.
- **(iv) Hors du cadre : corang ≥ 2, ou première couche non pleine.** Des conditions apparaissent dès que le complément
  disponible manque d'isotropie, **à partir de 6 lointains**.
  - **Contre-exemple du relecteur (P, relecteur, non revérifié par moi).**
    - On se place au rang 41 (ρ = 4, U₄ elliptique, d'indice de Witt 1) avec m = 6, et s ≡ 0 sur K_X, de dimension 2.
    - On suppose B = (N′, H/49) unimodulaire et anisotrope.
    - Une représentation de B(7) dans U₄ se réduit mod 7 à un sous-espace totalement isotrope de dimension ≤ 1. Un y
      primitif devrait donc vérifier v₇(yᵀHy) ≥ 3, alors que tous valent 2.
    - H_XX n'est donc pas représentée.
    - Le même mécanisme vaut aux rangs 37 et 39 : corang 2 à 6 lointains, avec un complément de rang 4 elliptique.
    - Probabilité de l'ordre de 7⁻³.
  - **Exemple au rang 43 : 6 lointains avec rang₇ H = 5 et v₇(det H) = 2.**
    - Le complément de la première couche est alors ⟨c⟩ ⊥ U₂(7), et l'on doit avoir χ(det H/49) = χ(det U″).
    - Probabilité de l'ordre de 1 % (P, esquisse non vérifiée).
  - **Le classement complet de ces cas reste à faire (X).** Ils sont rares, mais ils ne sont pas couverts par (i) à (iii).

**Preuve de (i), (ii) et (iii)** ; celle de (iii′) est dans l'énoncé.
- **Lemme A : on détache la première couche.** Comme p est impair, ℤ₇^X = N₀ ⊥ N′, avec N₀ unimodulaire de rang ρ et
  H(N′, N′) ⊂ 7ℤ₇.
  - Une représentation φ envoie N₀ sur un sous-réseau unimodulaire, d'où M_T = φ(N₀) ⊥ M′.
  - Pour p impair, les rangs et les classes de déterminant de chaque composante de Jordan sont des invariants. Ils
    imposent N₀ ≅ U″ (c'est la condition de première couche) et M′ ≅ U_{8−ρ}(7).
  - Donc H_XX est représentée ⟺ (N′, H/7) est représenté par U_{8−ρ}. La réduction mod 7 de (N′, H/7) est s.
- **(i) et (ii).** Si s est non dégénérée, (N′, H/7) est unimodulaire de rang m − ρ.
  - Pour m − ρ < 8 − ρ, il se plonge dans U_{8−ρ} : le complément, de rang ≥ 1 et de classe imposée, existe toujours.
  - Pour m = 8, il faut (N′, H/7) ≅ U_{8−ρ}, c'est-à-dire l'égalité des classes de déterminant.
- **(iii).** On écrit N′ ≅ N′₀(7) ⊥ ⟨y⟩, où N′₀ correspond à s₀ et y engendre le radical de s. Alors
  e′ := v₇(yᵀHy) = v₇(det H_XX) − (6 − ρ) ≥ 2.
  - φ(y) est orthogonal à φ(N₀), donc φ(y) = β ∈ M′ ≅ U_{8−ρ}(7). Il est orthogonal aux images de N′₀, et sa
    réduction β̄ est isotrope. On a donc β̄ ∈ C.
  - Si C est anisotrope, β̄ = 0, donc β = 7β′ avec β′ ∈ C exactement, d'où yᵀHy = 7³·N(β′). Une norme du plan
    anisotrope a une valuation paire, donc e′ = 3 + pair.
  - Si C est hyperbolique, β̄ peut être un vecteur isotrope non nul, et e′ est libre.
  - **Cas ρ = 6.** N′ = ⟨7^e u⟩ avec e = v₇(det H_XX) ≥ 1. Il faut que U₂ représente 7^{e−1}u. Or U₂ anisotrope est la
    forme norme de l'extension quadratique non ramifiée : elle représente exactement 0 et les éléments 7^{2j}·(unité).
    Donc e − 1 est pair. ∎

### 2.4 Tests (E)

**Le pas de représentation, sur réseaux synthétiques** (`o2_parity.py`). On tire des blocs principaux de 7Π d'un réseau de
type donné, avec première couche pleine.

| modèle | m = \|X\| | v₇(det) observé |
|---|---|---|
| ρ = 6, U₂ anisotrope (graines 1 et 3) | 7 | {1 : 772, 3 : 16} : **toujours impair** (788 sur 788) |
| ρ = 6, U₂ hyperbolique (graine 2) | 7 | {1 : 296, 2 : 76, 3 : 11, 4 : 4} : 21 % pairs |
| ρ = 4 (graine 4) | 5 | {1 : 323, 2 : 57, 3 : 10, 4 : 2} : 15 % pairs |
| ρ = 2 (graine 5) | 3 | {1 : 335, 2 : 54, 3 : 5} : 14 % pairs |
| les cinq modèles | 8 | χ(det/7^{8−ρ}) constant : (ii), 327 à 336 tirages par modèle |

**Règle du corang 1, sur réseaux synthétiques** (`o2_corank.py`, 1 500 tirages de 7 coordonnées par modèle). On donne
l'histogramme de v₇(det H_XX) − (6 − ρ) sur les cas où s est de corang 1.

| modèle | cas de corang 1 | C anisotrope (prédit : impair ≥ 3) | C hyperbolique |
|---|---|---|---|
| ρ = 2 (graine 11) | 248 | {3 : 15, 5 : 1} | {2 : 180, 3 : 42, 4 : 8, 5 : 1, 6 : 1} |
| ρ = 4 (graine 12) | 261 | {3 : 6} | {2 : 194, 3 : 42, 4 : 18, 5 : 1} |
| ρ = 6, U₂ anisotrope (graine 13) | 26 | {3 : 26} | — |
| ρ = 0, χ(det L) = +1 (graine 21, `o2_corank0.py`, 2 000 tirages) | 352 | {3 : 12, 5 : 2} | {2 : 259, 3 : 60, 4 : 13, 5 : 5, 6 : 1} |
| ρ = 0, χ(det L) = −1, la classe de Conway au rang 37 (graine 22) | 324 | {3 : 14} | {2 : 242, 3 : 53, 4 : 13, 5 : 2} |

- Dans un vrai réseau, le cas « C anisotrope » est rare, puisqu'il exige e′ ≥ 3.
- Pour une configuration qui ne vient pas d'un réseau, il survient avec la probabilité P(corang 1) ≈ 1/6, et C y est
  anisotrope une fois sur deux. La règle y élimine donc environ 1/6 × 1/2 × 0,85 ≈ 7 % (H).

**(C43) sur des étoiles réalistes** (`o2_c43_rate.py`).
- On part des vrais candidats de l'étoile de x = 0, avec les filtres de star39_prep.
- On tire 7 valeurs de y distinctes, avec des paires q et s distinctes, un recouvrement ≤ 2, et pour R un couplage
  partiel aléatoire.
- H est calculé exactement, en entiers : on multiplie par 9·det L, qui est premier à 7.
- On garde les configurations avec rang₇ H₇₇ = 6. La positivité n'est pas imposée : un bloc 7 × 7 de candidats aléatoires
  est semi-défini positif avec une probabilité d'environ 10⁻⁴.

| graine | configurations de rang₇ 6 | histogramme de v₇(det) | passent (C43) |
|---|---|---|---|
| 1 | 2 586 | {1 : 2 190, 2 : 347, 3 : 43, 4 : 4, 5 : 2} | 86,4 % |
| 2 | 1 833 | {1 : 1 589, 2 : 199, 3 : 44, 4 : 1} | 89,1 % |
| 4 | 2 461 | {1 : 2 123, 2 : 282, 3 : 48, 4 : 7, 5 : 1} | 88,3 % |
| 5 | 2 077 | {1 : 1 797, 2 : 234, 3 : 43, 4 : 3} | 88,6 % |
| 6 | 1 427 | {1 : 1 223, 2 : 175, 3 : 26, 4 : 2, 5 : 1} | 87,6 % |
| 1, avec x = 2 | 1 884 | {1 : 1 619, 2 : 227, 3 : 35, 4 : 3} | 87,8 % |

Sur ces six runs, (C43) élimine 11 à 14 % des configurations (graines 1, 2 et 4 : 400 000 tirages ; les autres :
300 000).

### 2.5 Les autres premiers (P, E)

**Énoncé.** Soit p ∤ 2·3·7·τ.
- Λ₋(T) ⊗ ℤ_p est unimodulaire, de déterminant ≡ τ modulo les carrés. En effet, par RD:21, j² divise 4·7^{2k}τ/9, donc
  p ∤ j.
- Π_XX est la Gram de vecteurs de ce réseau, et le lemme A s'applique encore :
  - **jusqu'à 6 lointains**, rien ne se passe dans les cas génériques ;
  - **à 7 lointains**, si Π_XX mod p est de rang 6 et si e = v_p(det Π_XX) est impair, alors **(−τ·d₀ | p) = +1**. Ici
    d₀ est le discriminant de la forme Π_XX mod p, c'est-à-dire le déterminant d'un mineur principal 6 × 6 non singulier.
    Raison : le complément de N₀ est un plan unimodulaire de déterminant τ/d₀. Il doit représenter p^e·(unité), donc être
    isotrope ;
  - **à 8 lointains**, on retrouve la classe carrée (A).

**Contrôle** (`o2_hasse7.py`, réseaux synthétiques unimodulaires en p).
- La règle est vraie dans 3 726 cas sur 3 726.
- Le signe opposé n'est vrai que dans 44 % des cas.

**Correction en cours de route.** Ma première version remplaçait d₀ par la partie p-unité de det Π_XX. Elle n'était vraie
qu'à 52 % : elle était fausse. Elle a été corrigée avant tout usage. La trace est dans `engine_runs_2026-10-20.log` §7, et
le script imprime encore l'ancienne version.

**Le cas p | τ (P, esquisse non vérifiée).**
- E₋ ⊗ ℤ_p est unimodulaire (p ∤ 63), mais le réseau proche ne l'est pas : son déterminant 144τ contient p. Il y a donc
  une colle en p entre le réseau proche et Λ₋(T).
- Elle fixe la classe de chaque Π_T e_a dans le groupe discriminant de Λ₋(T) en p comme fonction des noms de a. C'est la
  partie polaire de rang 1 de Z = (3I − G + J)⁻¹ en p, cohérente par construction.
- La première couche en p est donc automatique. La suite (seconde couche unimodulaire de rang 8 − v_p(τ)) n'agit qu'à
  partir de 8 lointains, sauf cas dégénérés.

### 2.6 Nouveauté

**Déjà dans l'archive (A).**
- La classe carrée à 8 lointains :
  - LAP (TL:2338) ;
  - confirmée par Codex (TL:2461-2463) ;
  - citée comme « Codex's note 217 » en NOTE_PROOFS_1410:257.
- Au rang 37, le constat qu'aucune relation collective n'agit avant 8 membres (TL:3597 et 3604-3608, sans preuve
  générale, avec H⁺ mod 49).
- Les déterminants et les classes de Λ₋(T) (RD §1-2).
- DISC et (SQ3) pour les blocs de rang plein (NOTE_PROOFS_1410:332-349).

**Non trouvé dans `work/`.** Recherche par grep sur « anisotrop », « valuation impaire », « odd valuation », « v₇(det »,
« Hasse », « Pi' », « 138/35 », « 4I+G ».
- La règle du corang 1 à 7 lointains, et son cas du rang 43, (C43).
  - Elle **complète** TL:3597 (« none acts before eight members ») à une précision plus fine. Ce n'est pas une correction.
    - TL travaille avec H⁺ mod 49 (TL:3608).
    - La règle du corang 1 doit distinguer e′ = 2 de e′ ≥ 3, ce qui demande H mod 7³.
    - À 7 membres, elle agit dans environ 7 % des cas au rang 37.
  - La preuve est la même avec ρ = 0, vérifiée sur réseaux synthétiques : `o2_corank0.py`, 28 cas « C anisotrope » sur 28,
    dont 14 avec la classe de Conway.
- La règle de Legendre à 7 lointains.
- Le théorème §2.3 en général.
- L'usage de Π⁽³⁾ comme filtre.

**(C43) n'est pas une conséquence de (SQ3).** Pour 7 lointains, le bloc A − 3I sur N[T] ∪ X est de rang ≤ 44 < 45.

---

## 3. Le second projecteur réel Π⁽³⁾ (P, E)

### 3.1 Formules
On se place dans un srg(v, k, 1, 2) de valeurs propres r > s, avec n = k − 2 et f_a = e_a − (2/n)𝟏. Ici e_a est la
colonne a de E, l'indicatrice des noms de a. Soit Π^(θ) le projecteur sur les vecteurs propres de valeur θ nuls hors de F.
Alors :

    (r − s) Π^(r)_ab = R_ab − sδ_ab − 2/(n−2) − 2(r−3)/(n(n−2)) − f_aᵀ(G − sI)⁻¹f_b,
    (r − s) Π^(s)_ab = rδ_ab − R_ab + 2/(n−2) − 2(r+4)/(n(n−2)) − f_aᵀ(rI − G)⁺f_b.

**Preuve.**
- R préserve ker E, et y vérifie R² + R − (k − 2) = 0. Cela vient des identités ER = 2J − E − GE et
  R² + R + EᵀE = (k − 2)I + 2J.
- Donc Π^(r) = (R − sI)P_{ker E}/(r − s) et Π^(s) = (rI − R)P_{ker E}/(r − s), avec P_{ker E} = I − EᵀK⁺E.
- On calcule K⁺ sur la décomposition « classes ⊕ Z » de NOTE_OBSTRUCTION §1.1.
- Les f_a sont dans Z ; quand c ≥ 2, L4 les rend orthogonaux au noyau.

**Pour Conway** (k = 14, r = 3, s = −4) :
- 7Π^(−4) = H = 3I − R + J/9 − Eᵀ(3I − G + J)⁻¹E (A) ;
- **7Π^(3) = H₃ = 4I + R − (2/35)J − Eᵀ(4I + G)⁻¹E**, de rang 18 pour c = 1 ;
- **H + H₃ = 7(I − EᵀK⁺E)**.

La diagonale de H₃ est la formule « n_fᵀ(4I+G)⁻¹n_f = 138/35 − 7Π′_ff » de TL:2335 (A, identité de LAP). Elle n'était pas
utilisée comme filtre.

### 3.2 Contrôles (E)

**Contrôle positif** (`o2_srg243_control.py`), sur deux srg(243,22,1,2) réels de l'archive : bvls243, avec une droite à
c = 10, et new243_trade_aut162, avec une droite à c = 5.
- On compare les formules locales aux vrais projecteurs, obtenus par complément de Schur du projecteur global. L'écart
  est ≤ 9·10⁻¹⁵.
- Les valeurs propres sont dans {0, 1}, et les rangs valent 72 et 50.
- Les blocs d'étoile (18 lointains) sont semi-définis positifs, et 𝟏_S est dans le noyau des deux.
- **Écart :** au premier essai, j'ai pris le pseudo-inverse de numpy avec la tolérance par défaut sur le bloc proche
  singulier. On obtenait 10⁻³ d'écart et des valeurs propres hors de {0, 1}. C'est un artefact du côté « vérité », corrigé
  avec rcond = 10⁻⁹.

**Identité de Conway** (`o2_p3stats.py`) : sur 300 tirages, l'écart vaut 7·10⁻¹⁵.

### 3.3 Le test « 7I − H ⪰ 0 » : impliqué par H₃ ⪰ 0, vide en petite taille, jamais actif en pratique
- **Impliqué (P).** 7I − H = H₃ + 7EᵀK⁺E. Il découle donc de H₃ ⪰ 0.
- **Vide sur la diagonale (P).** H_aa = 37/12 − f_aᵀΓ_R f_a ≤ 37/12 < 7.
- **Vide sur les blocs de taille 2 dès que H ⪰ 0** (relecteur, P). Les valeurs propres sont ≤ tr ≤ 37/6 < 7.
- **Jamais actif (E, constat empirique).** Le moteur n'imposait pas H₃ ⪰ 0, et ce test ne coupe rien : 0 coupe sur les 10
  runs où il est actif (h7_cuts = 0, rangs 37 et 39). Ce n'est pas un théorème pour les blocs de taille ≥ 3.

### 3.4 Force de H₃ ⪰ 0 (E)

| mesure | H seul (moteur actuel) | H et H₃ |
|---|---|---|
| unaire, graine 1 (25 581 triplets) | 3 618 coupés | 0 de plus |
| blocs aléatoires de k candidats semi-définis positifs, k = 5 | 1,87 % | 1,80 % |
| idem, k = 6 | 0,20 % | 0,13 % |
| moteur, rang 39, graine 4, les 400 premières branches | 2 060 617 nœuds | 2 060 411 nœuds (5 229 coupes, contre 85,7 M pour H) |

L'espace de valeur 3 est de dimension 18. Il ne contraint que des blocs de taille au moins 10 environ (double étoile,
droite complète), et pas l'étoile.

### 3.5 Complétude (P)
Le contenu réel de second ordre (matrices de Gram) de X = N[T] ∪ S est exactement :
- Π⁽⁻⁴⁾_SS ⪰ 0, de rang ≤ 8 ;
- Π⁽³⁾_SS ⪰ 0, de rang ≤ 18.

Le reste est automatique.
- Les blocs proches P_θ,NN sont semi-définis positifs pour tout G cubique.
- Les conditions d'image sont vraies dès que chaque lointain a deux noms par classe et aucun dans T.
  - Le noyau de P₋₄ sur N[T] (bloc 39 × 39) est engendré par les vecteurs
    κ_t = e_t + (5/18)𝟏_{C_t} − (1/18)(𝟏_{C_t′} + 𝟏_{C_t″}) (RD:24).
  - Le bloc 36 × 36 sur N(T), lui, est inversible : son déterminant vaut 144τ/7³⁶.
  - Pour tout triplet W, Σ_{v∈W} κ_v = 1/3 = Σκ/9.
- Vérification (E, `o2_nearblocks.py`, graines 1 à 5).
  - Les deux blocs proches sont semi-définis positifs, et tous deux de rang 36.
  - Les κ_t annulent P₋₄,NN à 2·10⁻¹⁶ près.
  - Les noyaux des deux blocs annulent les colonnes de 200 lointains admissibles tirés au hasard, à 5·10⁻¹⁶ près.

Aucune condition réelle de Gram ne reste donc à ajouter sur l'étoile.

---

## 4. Profondeurs atteintes (E)

`star39o2.cpp` est une copie instrumentée de star39.cpp.
- Avec les options par défaut, elle donne les mêmes nœuds et les mêmes coupes que l'original (3 entrées, journal §1).
- Le tableau donne le nombre de nœuds selon le nombre de lointains déjà placés.

| entrée | rang | δ | branches parcourues | 0 | 1 | 2 | 3 | 4 | 5 | ≥ 6 |
|---|---|---|---|---|---|---|---|---|---|---|
| star37 s1, s10, s12 | 37 | — | toutes | 1 | 354-371 | 2 156-2 572 | 0-1 | 0 | 0 | 0 |
| star39 s4 | 39 | 3 | 689 / 12 647 | 1 | 113 | 64 651 | 3 319 474 | 305 231 | 2 | 0 |
| star39 s1 | 39 | 3 | 184 / 18 188 | 1 | 31 | 24 031 | 1 681 027 | 335 730 | 12 | 0 |
| star39 s2 | 39 | 3 | 215 / 14 124 | 1 | 36 | 26 729 | 1 892 293 | 317 352 | 5 | 0 |
| star39 s3 | 39 | 1 | 341 / 14 736 | 1 | 47 | 33 653 | 2 043 128 | 215 903 | 4 | 0 |
| star39 s6 | 39 | 3 | 351 / 16 354 | 1 | 58 | 37 065 | 2 104 592 | 164 332 | 0 | 0 |

**Conséquence.**
- Aux rangs 37 et 39, aucune branche échantillonnée ne place plus de 5 lointains.
- Les conditions qui n'agissent qu'à 7 ou 8 lointains ont donc un pouvoir d'élagage **nul** sur ces tests : la règle du
  corang 1, (C43), la règle de Legendre, la classe carrée, le rang exact à 9 (STAR_R9).
- Le moteur sait les appliquer (STAR_R9, STAR_DUMP8), mais aucun nœud de profondeur 8 n'a été produit (dump8 = 0).
- Ce sont des préfixes de 1 à 5 % de l'arbre : la profondeur maximale des runs complets n'est pas mesurée. Les runs
  complets du 20/10 n'ont atteint aucune feuille (NOTE_BOOST §5).

---

## 5. Rangs 41 et 43 (P, H)

**Le haut de l'arbre est hors de portée de l'arithmétique (P).**
- Jusqu'à la profondeur ρ − 1, la première couche est vide : toute forme de dimension < ρ se plonge dans U″_ρ.
- À la profondeur ρ, il n'y a qu'un bit, la classe de la forme.
- Avant 7 lointains, dans le cadre générique (corang ≤ 1), l'ordre ≥ 2 n'agit pas (théorème §2.3). Hors de ce cadre, il
  existe des cas dégénérés dès 6 lointains : de l'ordre de 1 % au rang 43, de l'ordre de 7⁻³ ailleurs, non classés (X).
- Les autres premiers n'agissent pas non plus avant 7 lointains (§2.5).
- Le haut de l'arbre (4 à 5 lointains au rang 41, 6 au rang 43) n'est donc élagué que par la positivité (H et H₃) et par
  la combinatoire.
- **(H)** Le théorème montre seulement que rien d'arithmétique n'agit avant 7 lointains dans les cas génériques. Que les
  règles des profondeurs 7 et 8 réduisent ou non l'estimation d'environ 10¹⁵ nœuds par droite au rang 41 (SYNTHESE §8,
  A ; non relu ici) dépend du profil de profondeur de l'arbre. C'est la mesure proposée au §6.

**Remarque sur le tableau de SYNTHESE §3.5 (H).**
- Au rang 43, les espérances « avec le filtre réel » (environ 10⁸, « l'étoile survit ») comptent la positivité.
- Elles ne comptent ni le rang réel ≤ 8 de l'étoile complète, qui est une équation exacte (le déterminant 9 × 9 est nul),
  ni la classe carrée à 8 lointains (A).
- Avec ces deux conditions, l'espérance heuristique d'étoiles complètes devient négligeable à tout rang, sauf annulation
  structurelle que l'on ne connaît pas.
- L'obstacle aux rangs 41 et 43 est donc la **taille de l'arbre** au-dessus de 7 lointains, plutôt que la
  satisfaisabilité.

---

## 6. Prochaine étape concrète

1. **Fermer l'item 3 du plan pour les cas génériques** (SYNTHESE §8, « conditions 7-adiques d'ordre 2 locales »), avec
   le théorème §2.3.
   - Les seules règles nouvelles y sont à 7 lointains : la règle du corang 1, environ ×0,93 aux rangs 37 à 41, et (C43),
     environ ×0,87 au rang 43.
   - Les cas dégénérés de §2.3 (iv) restent ouverts (X), mais leur probabilité est de 1 % au plus.
2. **Faire la mesure décisive pour les rangs 41 et 43.** Écrire un moteur d'étoile **sans u** :
   - la première couche devient un test de rang incrémental mod 7 sur H_XX, sans énumérer F₇^ρ, ce qui évite les
     environ 7⁵ vecteurs u par triplet au rang 43 ;
   - le bit de classe à la profondeur ρ ;
   - (C43) et la règle de Legendre à 7 lointains ;
   - la classe carrée et le rang exact à 8 et 9 lointains ;
   - la positivité de H et de H₃ ;
   - et un estimateur de Knuth des nœuds aux profondeurs ρ, ρ + 1 et 8.

   Coût : environ une journée de code, moins d'une heure de CPU, un seul processus.

   **Critère de décision.**
   - Si l'estimation dépasse environ 10¹² nœuds par droite au rang 41, la route droite par droite est close aux rangs 41
     et 43. Seul un théorème global pourra finir (r ≤ 39, ou r = 37).
   - Si elle reste sous 10⁹, un pilote sur quelques droites devient possible.
3. **Hygiène des moteurs (gratuit).**
   - Remplacer « 7I − H » par H₃ : même coût, strictement plus fort, valable à tout rang.
   - Ajouter R9, le rang exact à 9 lointains, dans les unités plus grandes (double étoile, droite complète), où
     apparaissent des blocs de taille ≥ 9.
   - Gain mesuré nul pour l'étoile aux rangs 37 et 39.

---

## 6 bis. Ce qui n'a pas été vérifié

Les calculs ont été arrêtés à 16 h 33 : l'utilisateur reprenait le PC, et tous les processus ont été suspendus. La note
est finie avec ce qui était acquis.

**Relecture.**
- Une relecture adverse indépendante (agent) des §1 à §3 a été lancée à 16 h 25. On lui a demandé d'arrêter tout calcul.
- Elle a rendu son avis par lecture seule, sans exécuter aucun script. Son verdict : mathématiques correctes.
- Elle demandait trois corrections, toutes intégrées ici :
  - la portée du « avant 7 lointains » (le cas de corang 2 à 6 lointains) ;
  - le signe et la notation de (ii) ;
  - la portée des mesures (préfixes) et du §5.
- **Aucune preuve n'est relue par un humain.** Tout ce qui est marqué P reste « P, non relu ».
- Ce qui vient du relecteur est marqué tel : le contre-exemple de (iv), la dérivation de Hasse en §2.2, la justification de
  l'étape 5. Je ne l'ai pas revérifié.

**Constantes de l'archive.**
- χ(det U″) = (−1)^{k+1}(τ|7) et det Λ₋(T) = 4·7^{2k}τ/(9j²) sont pris dans RD (A, « non relu par un tiers » selon RD
  lui-même).
- (C43) en dépend. La partie unité de det Λ₋(T) est redérivée en §2.2 ; la classe de U″ ne l'est pas.

**Ce qui n'a pas été testé.**
- **§2.3 (iv)** : rien n'y est testé, et le classement complet reste ouvert.
  - Le cas dégénéré du rang 43 à 6 lointains (rang₇ H = 5, v₇ = 2) est une esquisse.
  - Le contre-exemple de corang 2 à 6 lointains est un raisonnement du relecteur.
- **§2.3 (iii′)** : « corang 1 à m ≤ 6 : libre » est prouvé en une ligne. Les tests synthétiques portent sur m = 7
  seulement.
- **§2.5** : le cas p | τ est une esquisse. La règle de Legendre n'est testée que sur réseaux synthétiques, pas sur des
  étoiles de Conway. Il faudrait factoriser det Π₇₇ pour trouver les premiers actifs.
- **(C43) et la règle du corang 1 sur de vraies étoiles** :
  - (C43) est mesurée sur des configurations réalistes de 7 lointains (six runs), mais sans la positivité. Aucun nœud de
    profondeur 7 n'existe dans les recherches réelles aux rangs 37 et 39, et il n'existe pas d'entrée au rang 43.
  - La règle du corang 1 n'est mesurée que sur réseaux synthétiques. Son taux d'environ 7 % est une heuristique (H).

**Ce qui n'est pas exhaustif.**
- Les histogrammes de profondeur du rang 39 sont des préfixes : 184 à 689 branches de profondeur 1 sur 12 647 à 18 188,
  soit 1 à 5 % de l'arbre. Une branche plus profonde ailleurs dans l'arbre n'est pas exclue. Les runs complets du 20/10
  n'ont atteint aucune feuille.
- La comparaison H₃ et sans 7I − H porte sur un seul préfixe de 400 branches (graine 4).

**Ce qui n'a pas été fait.**
- Le moteur « sans u » et l'estimateur de Knuth du §6.
- Le coût annoncé, une journée de code, est une estimation.

**Contrôles qui ont échoué puis ont été corrigés** (journal §6 à §8).
- Le pseudo-inverse dans le contrôle srg(243).
- La première version de la règle de Legendre.
- La première estimation des cas dégénérés de §2.3 (iv).

---

## 7. Fichiers

Tout se trouve dans `merge_2026-10-19/ordre2_2026-10-20/`.

**Scripts.**
- `o2_srg243_control.py` : contrôle positif des deux projecteurs sur un srg(243,22,1,2) réel.
- `o2_p3stats.py` : identité H + H₃, force unaire et par blocs de H₃ (Conway, graine 1).
- `o2_nearblocks.py` : blocs proches des deux projecteurs, rangs, noyaux et conditions d'image (§3.5).
- `star39o2.cpp` : moteur instrumenté (STAR_P3, STAR_NO7, STAR_R9, STAR_D1MAX, STAR_DUMP8 ; histogramme des profondeurs).
- `o2_m49_synth.py` : système mod 49 (§1.3).
- `o2_parity.py` : (C43) et (ii) sur réseaux synthétiques.
- `o2_corank.py` : règle du corang 1 sur réseaux synthétiques (ρ = 2, 4, 6).
- `o2_corank0.py` : la même règle pour ρ = 0 (rang 37).
- `o2_c43_rate.py` : taux de (C43) sur des étoiles réalistes.
- `o2_hasse7.py` : règle de Legendre à 7 lointains.

**Sorties.**
- `engine_runs_2026-10-20.log` : sorties brutes des moteurs, des contrôles, et la trace de l'erreur corrigée.
- `REVUE_AGENT_2026-10-20.md` : l'avis du relecteur adverse (agent, lecture seule), condensé, et ses corrections, toutes
  intégrées.
- `hist39_*.json`, `m49_*.json`, `parity_*.json`, `corank_*.json`, `corank0_*.json`, `c43_s*_big.json`,
  `c43_s*_x*_more.json`, `hasse7_s*.json`.

**Reproduction.** Interpréteur `C:/home/researcher/conway99-env/.venv/Scripts/python.exe -I`, un processus, chaque commande en
moins de 5 minutes. Les entrées .bin sont dans le scratchpad (`boost/runs/`, `real/`).

    python o2_srg243_control.py <work>/stars_rank_2026-10-14/kreps_check/bvls243.edges 0 0
    python o2_srg243_control.py <work>/spreadfree_243_2026-10-12/new243_trade_aut162.edges 5 7
    python o2_p3stats.py 1 0 1500
    python o2_nearblocks.py 1 2 3 4 5
    g++ -O2 -o star39o2.exe star39o2.cpp
    STAR_D1MAX=400 [STAR_P3=1] [STAR_NO7=1] ./star39o2.exe star39_s4_x0.bin 250
    python o2_m49_synth.py 1 2        (et 2 4, 3 6, 4 2)
    python o2_parity.py 1 6 aniso 400 (et 2 6 hyper, 3 6 aniso, 4 4 any, 5 2 any)
    python o2_corank.py 11 2 1500     (et 12 4 1500, 13 6 1500 aniso)
    python o2_corank0.py 21 2000      (et 22 2000 -1)
    python o2_c43_rate.py 1 0 400000  (graines 1, 2, 4 ; puis 5 0, 6 0, 1 2 avec 300000)
    python o2_hasse7.py 1 800 3000    (graines 1, 2, 3)
