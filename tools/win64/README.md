# Outils DRAT pour Windows x64 (sans Docker, sans WSL)

*27/09, C1. Pour le PC du labo, qui n'a pas de compilateur : la route SAT des 79 types a besoin de preuves DRAT vérifiées.*

| fichier | contenu | SHA-256 |
|---|---|---|
| `cadical.exe` | CaDiCaL 3.0.1, statique | d0650d6acfed7156fbb850b6964420542f825792a5ea5260e6a5d26dc31c3047 |
| `drat-trim.exe` | drat-trim (master), statique, patché | 2474cb831f89f06181667c711a9c3438e1b825fd02250555770b1bbd29634ea6 |
| `drat-trim-win.patch` | le patch appliqué à drat-trim.c | |

- **Sources** : les archives du « proofbox » de C3 (c3_recherche_annexe/docker/proofbox).
  - cadical.tar.gz, SHA-256 2327ac9b54e4b75e0a817507e56d43af370a66ac232c27c966174313edd5fc13 ;
  - drat-trim.tar.gz, SHA-256 334099b54c2ac9c5a38a6509c705b4fca1f98ebfcba99c2f49366281a16d6186.
- **Compilateur** : MinGW-w64 UCRT (WinLibs, gcc et g++ 16.1.0).
  - Seules dépendances : KERNEL32 et l'UCRT de Windows 10/11 (api-ms-win-crt-*). Pas de DLL à copier.

## Construction
- **CaDiCaL** : `CXX=g++ ./configure -static -lpsapi && mingw32-make cadical`. Configure choisit tout seul `-DNUNLOCKED -DNCLOSEFROM`.
  - CaDiCaL ouvre ses fichiers de preuve en `"wb"` : le DRAT binaire est sûr sous Windows.
- **drat-trim** : `gcc -O2 -static -Dgetc_unlocked=_getc_nolock -o drat-trim.exe drat-trim-win.c`, avec deux corrections :
  - **tous les `fopen` en mode binaire** (`"rb"`, `"wb"`). C'est OBLIGATOIRE : en mode texte, Windows corrompt les preuves DRAT
    binaires (la sortie par défaut de CaDiCaL). Sans le patch, l'exemple R_4_4_18 d'origine (DRAT binaire) donne NOT VERIFIED ;
    avec, VERIFIED ;
  - `getc_unlocked` n'existe pas sous MinGW, d'où le `-D`.

## Tests (portable C1, 27/09)
- **Positifs** : chaque instance est UNSAT pour CaDiCaL et VERIFIED par drat-trim, en DRAT binaire comme en texte
  (`--binary=false`) :
  - le pigeonnier PHP(8,7) ;
  - un 3-SAT aléatoire, n = 200 et m = 1200 ;
  - R_4_4_18 avec la preuve binaire fournie par drat-trim.
- **Négatifs**, tous NOT VERIFIED :
  - une preuve tronquée de moitié ;
  - une preuve réduite à la clause vide, sur une formule satisfiable ;
  - la preuve de PHP(8,7) vérifiée contre PHP(8,7) privé d'une clause, que CaDiCaL trouve SAT.

## Usage
```
cadical.exe -q type_XXXX.cnf type_XXXX.drat          # exit 20 = UNSAT, 10 = SAT
drat-trim.exe type_XXXX.cnf type_XXXX.drat -t 200000  # "s VERIFIED" ; le -t par défaut est de 40 000 s
```
- **DIMACS** : `code/sat_local_batch.py TYPES.json I0 I1 0 --dimacs OUTDIR`, ou l'export des encodages de « structures ».
- **Temps** : la vérification peut prendre plus longtemps que la résolution, avec une mémoire de l'ordre de la taille de la
  preuve. Laisser de la marge au garde-fou RAM.
- **Dépendances de la preuve** : une preuve DRAT couvre la CNF telle qu'elle est écrite. Les clauses lex-leader et les coupes
  (--cuts, --digon) restent des dépendances à citer : le lemme de symétrie et NOTE_S29 §9.
