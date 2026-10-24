# Premier travail — L'invention mathématique chez Perelman

Étude rédigée le 23–24/10/2026 pour la campagne « Perelman, l'invention mathématique et Conway-99 ».

## Ce que contient ce dossier

| fichier | contenu |
|---|---|
| `01_LE_MUR_AVANT_PERELMAN.md` | Partie I. Sources et statuts ; état du programme de Hamilton ; les six murs (M1)–(M6) formulés exactement ; ce qui était accessible et ce qui demandait une idée |
| `02_RECONSTRUCTION_DES_MECANISMES.md` | Partie II. Reconstruction, avec les équations, de tous les mécanismes décisifs de [I], [II], [III] : $\mathcal F$, $\mathcal W$, non-effondrement, géométrie $\mathcal L$ et volume réduit, Harnack adjointe, pseudolocalité, $\kappa$-solutions, voisinages canoniques, solution standard, $\delta$-coupure, hypothèses a priori, temps long, $\lambda$, extinction |
| `03_LES_INVENTIONS.md` | Partie III. Treize fiches « obstacle → idée → définition → propriété → conséquence → rôle », avec l'origine vérifiée et la nature de l'apport ; ce qui est devenu démontrable ; pourquoi ces objets |
| `04_PRINCIPES_TESTABLES.md` | Parties IV et V. Dix schémas abstraits (S1–S10), chacun tiré d'un argument précis, avec ses hypothèses, son protocole de test et ses transferts déjà réussis ; ce qui est propre au flot de Ricci ; cinq conditions de transfert (T1–T5) pour un problème fini |

## Lecture rapide (une page)

**Le mur.** Le programme de Hamilton butait sur une estimée a priori, le non-effondrement (« Little Loop Lemma »). Sans
elle, pas de limites d'éclatement, et des modèles effondrés (cigare × droite) qu'aucune chirurgie n'enlève. Venaient
ensuite trois manques : une classification grossière des limites, un contrôle *uniforme* de la région de haute courbure
autour de points non maximaux, et la survie de ces estimées à la chirurgie.

**Les inventions décisives.**
1. Une **entropie à échelle** ($\mathcal W$) dont la dissipation est exactement le carré du défaut de soliton.
2. Le **volume réduit**, géométrie de comparaison en espace-temps : monotone, rigide dans le cas d'égalité, et surtout
   localisable, donc robuste à la chirurgie.
3. L'**écrasement des solutions anciennes vers un soliton**, par « monotonie bornée + rigidité de l'égalité ».
4. La **compacité des modèles**, avec une classification seulement grossière.
5. Les **voisinages canoniques** obtenus par un choix extrémal qui transforme la conclusion aux échelles fines en
   hypothèse, avec l'exclusion des cônes par le principe du maximum fort (géométrie d'Alexandrov).
6. La **chirurgie à deux échelles** ($h \ll r$) autour d'un modèle standard universel, avec une ressource qui décroît.
7. Pour l'extinction, un **min-max sur une classe d'homotopie non triviale** muni d'une dérive négative universelle
   (Gauss–Bonnet).

**Ce qui est propre au flot.** Une déformation canonique existe à partir de toute donnée ; principes du maximum ;
symétries de jauge et d'échelle ; compacité ; spécificités de la dimension 3.

**Ce qui est transférable.** L'architecture logique S1–S10 : dissipation carrée, sonde locale d'une quantité globale,
rigidité de l'égalité, induction sur les échelles par choix extrémal, classification réduite à ce que l'aval consomme,
séparation hiérarchique des paramètres, min-max topologique, et le méta-principe de l'**énoncé intermédiaire unique**.

**Pour un problème fini**, cinq conditions de transfert (T1–T5) sont dégagées en fin de partie V. Le second travail
(`../conway/`) les teste une à une sur Conway-99.

## Sources

- Perelman, arXiv:math/0211159, math/0303109, math/0307245 : lus intégralement (sources LaTeX).
- Kleiner–Lott, arXiv:math/0605667 ; Morgan–Tian, arXiv:math/0607607 ; Tao, arXiv:math/0610903 ; Cao–Zhu,
  arXiv:math/0612069 : consultés aux passages cités.
- Les citations de Hamilton, Ivey, Li–Yau, Huisken, Ecker, Gross, Bakry–Émery, Chow–Chu, Altschuler–Grayson,
  Meeks–Yau, Colding–Minicozzi, Shioya–Yamaguchi, Anderson, Brendle sont faites d'après les renvois de Perelman et des
  reconstructions. Leurs articles n'ont pas été relus ici.
