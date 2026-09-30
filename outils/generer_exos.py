# -*- coding: utf-8 -*-
"""Régénère data/cloze.json et data/readings.json depuis le vocabulaire des séances.
À lancer après chaque ajout de vocabulaire.  Usage :  python outils/generer_exos.py"""
import json,glob,re,random,os
BASE=os.path.join(os.path.dirname(__file__),'..')
K={};W=[]
for f in sorted(glob.glob(os.path.join(BASE,'data/kanji/S*.json'))):
    d=json.load(open(f,encoding='utf-8'))
    for k in d['kanji']:
        K[k['k']]={'n':k['n'],'seance':d['id']}
        for v in k['vocab']:
            if v.get('fr'): W.append({**v,'kanji':k['k'],'seance':d['id'],'n':k['n']})
KAN=re.compile(r'[\u4e00-\u9fff]')
cloze=[];seen=set()
for w in W:
    ks=[i for i,c in enumerate(w['w']) if KAN.match(c) and c in K]
    if len(w['w'])<2 or not ks or (w['w'],w['r']) in seen or w.get('kana'): continue
    seen.add((w['w'],w['r']))
    i=random.Random(sum(map(ord,w['w']))).choice(ks); hidden=w['w'][i]  # graine stable d'un lancement à l'autre
    pool=[c for c in K if c!=hidden and abs(K[c]['n']-K[hidden]['n'])<26]
    random.Random(w['w']).shuffle(pool)
    cloze.append({'id':'c:'+w['w'],'w':w['w'],'i':i,'k':hidden,'r':w['r'],'fr':w['fr'],'star':w['star'],
                  'seance':w['seance'],'n':max(K[c]['n'] for c in w['w'] if c in K),'d':pool[:6]})
json.dump(cloze,open(os.path.join(BASE,'data/cloze.json'),'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
byk={}
for w in W: byk.setdefault(w['kanji'],[]).append(w)
read=[]
for w in W:
    if not w['r'] or len(w['r'])<2: continue
    o=[x['r'] for x in byk.get(w['kanji'],[]) if x['r']!=w['r']]+[x['r'] for x in W if x['r'] and abs(x['n']-w['n'])<14 and x['r']!=w['r']]
    u=[]
    for r in o:
        if r not in u: u.append(r)
    if len(u)<3: continue
    read.append({'id':'r:'+w['w']+'/'+w['r'],'w':w['w'],'r':w['r'],'fr':w['fr'],'star':w['star'],'seance':w['seance'],'n':w['n'],'d':u[:6]})
json.dump(read,open(os.path.join(BASE,'data/readings.json'),'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
print("OK — %d exercices « kanji manquant », %d exercices « lecture »." % (len(cloze),len(read)))
