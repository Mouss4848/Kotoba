# -*- coding: utf-8 -*-
"""
Importe un PDF de séance du CM Kanji (M. Couteau) dans data/kanji/SXX.json.

Usage :  python outils/importer_seance.py "CM_Kanji_-_Se_ance_03_-_Cours_kanji.pdf"

Prérequis : Python 3 et l'outil pdftotext (paquet poppler).
  - Windows : winget install --id oschwartz10612.Poppler   (ou télécharger poppler et l'ajouter au PATH)
  - macOS   : brew install poppler
  - Linux   : sudo apt install poppler-utils

Autre usage :  python outils/importer_seance.py --corrections
  (réapplique outils/corrections.json à toutes les séances, sans PDF)

Le script remplace, pour chaque kanji de la séance : le sens, les lectures ON/kun,
le vocabulaire avec traductions et étoiles. Le reste du fichier (dates, titre) est conservé.
"""
import sys, json, os, re
sys.path.insert(0, os.path.dirname(__file__))
from parse_seance import parse

def apply_corrections(seance):
    """Applique outils/corrections.json à une séance (dict). Renvoie le nombre de corrections."""
    cpath = os.path.join(os.path.dirname(__file__), 'corrections.json')
    try:
        C = json.load(open(cpath, encoding='utf-8'))
    except Exception:
        return 0
    n = 0
    for k in seance['kanji']:
        fix = C.get('kanji', {}).get(str(k['n']))
        if fix:
            for key, val in fix.items(): k[key] = val
            n += 1
        k['fr'] = k.get('fr', '').replace('\u02bc', '\u2019')
        # lectures en double (ex. セイ セイ dans le PDF de 生)
        for key in ('on', 'kun'):
            seen = []
            for r in k.get(key, []):
                if r not in seen: seen.append(r)
            k[key] = seen
        for v in k['vocab']:
            v['fr'] = v.get('fr', '').replace('\u02bc', '\u2019')
            for c in C.get('vocab', []):
                if v['w'] == c['w'] and all(v.get(a) != b for a, b in c['set'].items()):
                    old = 'v:' + v['w'] + '/' + v['r']
                    v.update(c['set'])
                    new = 'v:' + v['w'] + '/' + v['r']
                    if new != old: v['prev'] = old      # l'appli reporte la progression
                    n += 1
    return n

if len(sys.argv) < 2:
    print(__doc__); sys.exit(1)
if sys.argv[1] == '--corrections':
    root = os.path.join(os.path.dirname(__file__), '..', 'data', 'kanji'); tot = 0
    for f in sorted(os.listdir(root)):
        if not re.match(r'S\d\d\.json$', f): continue
        path = os.path.join(root, f); s = json.load(open(path, encoding='utf-8'))
        n = apply_corrections(s); tot += n
        json.dump(s, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print("OK — corrections appliquées à toutes les séances (%d)." % tot); sys.exit(0)
pdf = sys.argv[1]
data = parse(pdf)
if not data:
    print("Aucun kanji trouvé dans ce PDF. Vérifie que pdftotext est installé et que c'est bien un PDF de séance."); sys.exit(1)

root = os.path.join(os.path.dirname(__file__), '..', 'data', 'kanji')
nums = [d['n'] for d in data]
target = None
for f in sorted(os.listdir(root)):
    if not re.match(r'S\d\d\.json$', f): continue
    s = json.load(open(os.path.join(root, f), encoding='utf-8'))
    if s['range'][0] <= min(nums) <= s['range'][1]:
        target = (f, s); break
if not target:
    print("Impossible de trouver la séance correspondant aux kanji n°%d–%d." % (min(nums), max(nums))); sys.exit(1)

fname, s = target
byn = {d['n']: d for d in data}
hors = [n for n in nums if not (s['range'][0] <= n <= s['range'][1])]
if hors: print("Attention : n°%s hors de la plage %s de %s — vérifie la numérotation officielle." % (hors, s['range'], fname))
manquants = [k['n'] for k in s['kanji'] if k['n'] not in byn]
if manquants: print("Attention : kanji n°%s absents du PDF — laissés tels quels." % manquants)
changed = 0
for k in s['kanji']:
    d = byn.get(k['n'])
    if not d: continue
    if d['k'] != k['k']:
        print("Attention : n°%d est %s dans le PDF mais %s dans la liste — ignoré." % (k['n'], d['k'], k['k'])); continue
    k['fr'] = d['fr']; k['on'] = d['on']; k['kun'] = d['kun']
    k['vocab'] = [{'w': v['w'], 'r': v['r'], 'fr': v['fr'], 'star': v['star']} for v in d['vocab']]
    k['src'] = 'cours'; changed += 1

apply_corrections(s)
json.dump(s, open(os.path.join(root, fname), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# manifeste : marquer la séance comme "cours"
mpath = os.path.join(root, '..', 'manifest.json')
m = json.load(open(mpath, encoding='utf-8'))
for se in m['cours']['kanji']['seances']:
    if se['id'] == s['id']: se['src'] = 'cours'
import datetime; m['maj'] = datetime.date.today().isoformat()
json.dump(m, open(mpath, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print("OK — %s : %d kanji mis à jour, %d mots, %d ★. Manifeste daté du %s." % (fname, changed, sum(len(d['vocab']) for d in data), sum(1 for d in data for v in d['vocab'] if v['star']), m['maj']))
