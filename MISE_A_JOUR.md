# 言葉 — guide de mise à jour

## Structure

```
index.html                l'appli
manifest.webmanifest      identité de l'appli (Android)
icon.png / icon-512.png   tes icônes
data/manifest.json        la carte : cours, séances, leçons, date de mise à jour
data/strokes.json         tracés des 166 kanji (KanjiVG) — ne pas modifier
data/components.json      composants et clés — ne pas modifier
data/cloze.json           exercices « kanji manquant » — régénérés, voir plus bas
data/readings.json        exercices « quelle lecture » — régénérés, voir plus bas
data/cles.json            les 214 clés — ne pas modifier
data/cours_cles.json      le cours sur les clés (séance 03)
data/kanji/S01…S10.json   une séance de kanji par fichier
data/grammaire/L00…L25.json  une leçon de grammaire par fichier
data/grammaire/_lexique.json verbes (forme en て) et adjectifs (contraires)
data/td/elements.json     phrases des leçons 1 à 4 découpées (contrôle de TD)
data/td/textes.json       petits textes du contrôle de TD
outils/importer_seance.py import automatique d'un PDF de séance
outils/corrections.json   coquilles corrigées, réappliquées après chaque import
outils/generer_exos.py    régénère cloze.json et readings.json
```

Les données et le code sont séparés : tu peux modifier n'importe quel fichier
de `data/` sans jamais casser l'appli. Si un fichier est mal formé, l'appli
ignore cette séance et continue.

La progression de chaque utilisateur est stockée sur son téléphone, jamais dans
ces fichiers. Mettre à jour les données ne l'efface pas.

---

## Chaque semaine — kanji

### Option A : automatique (recommandé)

1. Télécharge le PDF de la séance (`CM_Kanji_-_Se_ance_03_-_Cours_kanji.pdf`).
2. Dans le dossier de l'appli, lance :
   ```
   python outils/importer_seance.py "chemin/vers/CM_Kanji_-_Se_ance_03_-_Cours_kanji.pdf"
   ```
3. Le script trouve tout seul la bonne séance (S03), remplace les sens, lectures,
   traductions et étoiles, et date le manifeste. Il affiche un résumé.
   Il signale aussi les numéros hors de la plage de la séance et les kanji absents du PDF.
4. Régénère les exercices : `python outils/generer_exos.py`
5. Envoie `data/` sur GitHub.

Prérequis : Python 3 et pdftotext (voir en tête du script). Une seule
installation, ensuite c'est une commande par semaine.

### Option B : à la main

Ouvre `data/kanji/S03.json`. Chaque kanji a cette forme :

```json
{"n": 35, "k": "時", "fr": "le temps, l'heure", "on": ["ジ"], "kun": ["とき"],
 "strokes": 10, "src": "liste",
 "vocab": [
   {"w": "時間", "r": "じかん", "fr": "le temps, la durée", "star": true}
 ]}
```

- `star: true` = mot ★ (garanti à l'examen) · `false` = enrichissement · `null` = inconnu
- Quand la séance est complète, passe `"src": "liste"` en `"src": "cours"` dans
  le fichier ET dans `manifest.json` : l'étiquette « traductions provisoires » disparaît.
- Mets à jour `"maj"` dans `manifest.json` (date du jour).

Les séances 05 à 10 ont déjà les mots, lectures et traductions. Il manque
seulement les étoiles (`null`) — l'import automatique les ajoutera.

---

## Corriger une coquille du cours

Ne corrige pas directement `data/kanji/SXX.json` : un nouvel import écraserait
ta correction. Ajoute-la dans `outils/corrections.json`, par exemple :

```json
{"w": "天ぷら", "set": {"r": "てんぷら"}}
```

puis lance `python outils/importer_seance.py --corrections` et `python outils/generer_exos.py`.
Pour un kanji (lectures, lectures grisées) : `"68": {"on": ["セイ", "ショウ"]}` ou
`"64": {"pale": ["ケイ"]}` dans la partie `kanji`, par numéro.
Si la lecture d'un mot change, l'appli reporte automatiquement la progression.

## Contrôle de TD (Mme Rydzek)

- Date du contrôle : `data/manifest.json`, champ `cours.td.date` (ex. `"2026-10-22"`).
  Le compte à rebours s'affiche alors à l'accueil.
- Phrases à éléments : `data/td/elements.json`. Chaque phrase est une liste
  `[texte, rôle]` ; les rôles possibles sont définis en tête du fichier.
- Petits textes : `data/td/textes.json` (texte, version kana, traduction, questions ;
  `a` = numéro de la bonne réponse, en partant de 0).

## Le champ `kana` (triangle du prof)

Quand un mot est à connaître en kana seulement, ajoute `"kana": true` à son
entrée. L'appli continue de le montrer et de l'interroger sur le sens et la
lecture, mais ne demande jamais d'écrire ou de reconnaître son kanji.

## Chaque semaine — grammaire (normalement rien à faire)

Les 25 leçons sont déjà chargées avec leur vocabulaire, leurs verbes,
adjectifs et phrases-modèles. Elles n'ont pas de date : chacun les débloque
lui-même dans l'appli quand la leçon a été vue en cours (« Marquer comme
vue »). Si tu veux fixer une date pour tout le monde, ajoute `"date":
"2026-10-01"` dans le fichier de la leçon et dans `manifest.json`.

Pour corriger ou compléter une leçon : ouvre `data/grammaire/LXX.json`.
Chaque phrase a un champ `tok`, la découpe utilisée par « construire la
phrase » — garde les particules collées au mot (`わたしは`, `車の`).

## Anciennes instructions grammaire (si tu ajoutes une leçon hors Noda)

1. Copie `data/grammaire/_MODELE.json` en `L03.json`, remplis-le.
2. Chaque phrase d'exemple a un champ `tok` : la phrase découpée en blocs.
   C'est ce que l'appli mélange dans « construire la phrase ».
   Découpe par groupe de sens : `["ミラーさんは", "会社員", "です"]`.
   Garde les particules collées au mot : `わたしは`, `車の`.
3. Ajoute la leçon dans `manifest.json` :
   ```json
   {"id": "L03", "titre": "Leçon 3 — …", "date": "2026-09-24"}
   ```
4. Envoie sur GitHub.

Le `vocab` de la leçon (liste de paires `[mot, sens]`) entre automatiquement
dans le flux ★.

---

## Déploiement

Nouveau dépôt GitHub (public ou privé avec accès à tes camarades), puis
Settings → Pages → branche `main`. Tu envoies : `index.html`, `icon.png`,
tout le dossier `data/`. Le dossier `outils/` et ce fichier peuvent rester
sur ton PC ou aller sur GitHub, peu importe.

Pour une mise à jour : remplace les fichiers modifiés dans le dépôt, commit.
L'appli se recharge au prochain lancement sur chaque téléphone.

Sur iPhone : Safari → Partager → Sur l'écran d'accueil.
Sur Android : Chrome → ⋮ → Ajouter à l'écran d'accueil.

---

## Dates importantes déjà dans l'appli

- Séances kanji 01 → 10 : du 3 sept. au 12 nov. (les séances futures
  apparaissent grisées et n'entrent pas dans la révision avant leur date)
- Examen kanji : 19 novembre 2026

## Coquilles corrigées par rapport au polycopié

一週間 (pas 一周間) · 空気 = くうき · 土石 = どせき · 晩年 = ばんねん


---

## Régénérer les exercices

Les fichiers `cloze.json` (kanji manquant) et `readings.json` (lectures) sont
**calculés** à partir du vocabulaire des séances. Après tout ajout ou
correction de vocabulaire, lance :

```
python outils/generer_exos.py
```

Ça reconstruit les deux fichiers. Sans ça, les nouveaux mots n'apparaissent
pas dans ces exercices (le reste de l'appli les voit quand même).

## Mode examen — ajuster le format

Les proportions de chaque type de question sont dans `index.html`, fonction
`buildExam` : 30 % lectures, 20 % sens, 20 % kanji manquant, 15 % ordre des
traits, 5 % nombre de traits, 10 % thème. Quand tu connaîtras le format réel
de l'épreuve, dis-le-moi et on cale les proportions dessus.
