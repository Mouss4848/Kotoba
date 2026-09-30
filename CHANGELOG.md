# 言葉 — versions

## v4.0 — 1er octobre 2026

**Interface**
- Barre d'onglets en bas : Aujourd'hui, Kanji, Grammaire, S'entraîner. Elle disparaît pendant les exercices pour laisser toute la place à la carte.
- Accueil allégé : Réviser, Nouveaux et Enrichir, compte à rebours, semaine, phrase du jour. Les cours et les jeux ont leur propre onglet.
- Les emojis sont remplacés par des kanji (見 découvrir, 書 tracer, 試 examen…) dans des cases de papier d'exercice.
- Nouvelle palette (encre indigo, corrections au vermillon) et thème nuit assorti.
- Police japonaise Klee One (style manuscrit scolaire), la même sur iPhone et Android. Si elle ne charge pas (hors ligne), l'appli reprend la police du téléphone.
- Cartes de révision : la question en haut, les réponses toujours au même endroit en bas.
- Grille des kanji : le niveau est indiqué par un point de couleur.
- Animations de page dans le sens de la navigation (on avance, on revient).

**Contrôle de TD (Mme Rydzek, leçons 1 à 4 et kana)**
- Nouvelle section dans l'onglet Grammaire, et examen blanc dans l'onglet S'entraîner.
- Nouveaux exercices : lire les kanji des leçons, transcrire en kana, identifier les éléments d'une phrase (toucher l'élément demandé, donner son rôle, retrouver la particule), traduire une phrase, comprendre un petit texte.
- 36 phrases des leçons 1 à 4 découpées en éléments (`data/td/elements.json`) et 6 petits textes originaux avec questions (`data/td/textes.json`).
- La date du contrôle se renseigne dans `data/manifest.json` (`cours.td.date`) : le compte à rebours s'affiche alors à l'accueil.

**Corrections**
- Saisie au clavier plus tolérante : katakana et hiragana équivalents, variantes acceptées (あした・あす), sans tenir compte de ～ ni des espaces.
- Quiz multi-angles et Survie : une carte « écrire la lecture » d'un exercice de lecture faisait planter l'écran. Corrigé.
- Construire la phrase : deux morceaux identiques (deux « です ») sont maintenant interchangeables.
- Plus de quiz « quel trait ? » sur un kanji d'un seul trait.
- Grammaire : 33 mots dont les colonnes étaient fusionnées (九 et きゅう・く dans le même champ) sont séparés ; 17 phrases mal découpées (« ブラジル人ですマリアさんも… », « a) ») corrigées ; 5 points sans titre renommés. La progression sur ces mots est reportée automatiquement.
- Kanji : lecture de 三千六百九十五 corrigée (espace parasite) ; apostrophes uniformisées.
- Le générateur d'exercices donne toujours le même résultat d'un lancement à l'autre.

**Séance 04**
- Importée du PDF de cours : 17 kanji, 87 mots, 48 ★.
- Coquilles corrigées : てんぷら, « dans le ciel », « topographiques » ; 生 = セイ・ショウ (le PDF écrivait セイ deux fois).
- Lectures grisées dans le cours (ケイ pour 京, キョウ pour 校) affichées en gris dans la fiche. Elles restent interrogées.

**Outils**
- `importer_seance.py` : les lectures kun terminées par un tiret (あか- あき- あ-) ne sont plus collées entre elles ; une ligne de suite contenant des parenthèses n'est plus prise pour un nouveau mot.
- Nouveau fichier `outils/corrections.json` : les coquilles corrigées y sont listées et l'importeur les réapplique après chaque import. `python outils/importer_seance.py --corrections` les réapplique à toutes les séances sans PDF.

## v3.0 — 18 septembre 2026

**Corrections**
- Quiz « trait n°N » : les quatre réponses sont désormais quatre tracés (le trait candidat en rouge sur le kanji en gris), plus des numéros écrits. Idem dans l'examen.
- 日本人 (le Japonais) était noté 日本. Corrigé, et contrôle de cohérence passé sur tout le vocabulaire.
- Un rappel différé ne peut plus s'afficher par-dessus un autre écran si tu changes de page pendant l'animation.

**Contenu**
- Séance 03 importée du cours : 17 kanji, 101 mots, 83 ★.
- Cours « La composition des kanji : les clés » (séance 03) : notions, dix familles d'exemples, sept positions avec schémas.
- Les 214 clés : table complète, recherche, nom japonais des clés courantes (さんずい, にんべん, しんにょう…). Chaque kanji est relié à sa clé officielle.
- Grammaire : les 25 leçons de Mme Noda, 675 mots classés par leçon, 374 phrases-modèles traduites et découpées, 96 verbes avec forme en て, 75 adjectifs avec leurs contraires.
- Les leçons et séances non encore vues sont grisées mais consultables, et chacun peut les débloquer lui-même (« Marquer comme vue en cours »).

**Audio**
- Prononciation par la voix japonaise du téléphone, à partir de la lecture en kana (jamais du kanji, pour éviter les erreurs de lecture). Boutons sur les mots, les lectures, les phrases.
- Option « prononcer automatiquement » à chaque carte.
- Deux nouveaux exercices : compréhension orale (écoute → sens, écoute → écriture) et dictée.

**Exercices**
- Forme en て, contraires, lecture → mot (あお → 青), clé d'un kanji, sens d'une clé.
- Écriture au clavier étendue à la forme en て.
- Champ `kana` pour les mots à connaître en kana seulement : l'appli ne demande alors jamais d'écrire le kanji.

**Jeux**
- Quiz multi-angles : chaque élément est interrogé sous un angle différent à chaque passage (sens, lecture, trait, clé, écoute, clavier…), en insistant sur les faibles.
- Duel de séances : dix questions sur chacune, verdict, révision de la plus faible.
- Survie : trois vies, quatre paliers de difficulté croissante, record par séance.
- Case « les jeux comptent dans ma progression » (poids réduit).

**Exercices libres** : n'importe quel type sur n'importe quelle portée, sans rien enregistrer.

**Examen blanc** : clés, forme en て et contraires ajoutés ; portée étendue aux leçons de grammaire.

## v2.0 — 14 septembre 2026
Découverte guidée, examen blanc, textes à trous, lectures, réseau de kanji, composants.

## v1.0 — 14 septembre 2026
Séances kanji, fiches, tracé vérifié, révision espacée, leçons de grammaire, construction de phrases.
