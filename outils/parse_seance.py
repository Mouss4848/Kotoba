# -*- coding: utf-8 -*-
"""Parseur d'un PDF de séance du CM Kanji (M. Couteau).

v4 : les lectures sont lues en mode « layout » de pdftotext (le mode brut colle
les lectures kun terminées par un tiret : あか- あき- あ- devenait あかあきあ-).
Le vocabulaire reste lu en mode brut. Une ligne de suite qui contient des
parenthèses n'est plus prise pour un nouveau mot (bug de 風土 en S04).
"""
import re, sys, json, unicodedata, subprocess

def norm(s):
    s = unicodedata.normalize('NFKC', s)
    return s.replace('\u02bc', '\u2019')          # ʼ → ’ (apostrophe du PDF)

JP = re.compile(r'[\u3040-\u30ff\u3400-\u9fff々〆ヶ]')
ENTRY = re.compile(r'^(.+?)[（(]([^）)]+)[）)]\s*(.*)$')
KANA_READING = re.compile(r'^[\u3040-\u30ffー・\-]+$')

def is_entry(line):
    m = ENTRY.match(line)
    if not m: return None
    w, r, _ = m.groups()
    # un vrai mot : du japonais avant la parenthèse, du kana dedans, pas de lettres latines
    if not JP.search(w) or re.search(r'[A-Za-zÀ-ÿ]', w): return None
    if not re.fullmatch(r'[\u3040-\u30ffー・ 　]+', r.strip()): return None
    return m

def pdf_pages(pdf, layout=False):
    cmd = ['pdftotext'] + (['-layout'] if layout else []) + [pdf, '-']
    txt = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8').stdout
    return [norm(p) for p in txt.split('\f')]

def readings_from_layout(page):
    """Lit ON / kun dans la colonne de gauche de la page en mode layout."""
    on, kun, mode = [], [], None
    lines = page.split('\n')
    try:
        start = next(i for i, l in enumerate(lines) if l.strip().startswith('Lectures'))
    except StopIteration:
        return None
    for l in lines[start + 1:]:
        left = re.split(r'\s{3,}', l.strip())[0].strip() if l.strip() else ''
        if left.startswith('・ON'):
            mode = 'on'; left = left.split(':', 1)[1].strip() if ':' in left else ''
        elif left.startswith('・kun'):
            mode = 'kun'; left = left.split(':', 1)[1].strip() if ':' in left else ''
        if not mode or not left or left == '-': continue
        for tok in left.split():
            if KANA_READING.match(tok) and tok != '-':
                (on if mode == 'on' else kun).append(tok)
    return on, kun

def parse(pdf):
    raw, lay = pdf_pages(pdf), pdf_pages(pdf, layout=True)
    out = []
    for pi, pg in enumerate(raw):
        lines = [l.strip() for l in pg.split('\n') if l.strip()]
        m = next((i for i, l in enumerate(lines) if re.match(r'^\d{3}\.$', l)), None)
        if m is None: continue
        num = int(lines[m][:-1]); meaning = lines[m + 1]; kanji = lines[m + 2].split()[0]
        rd = readings_from_layout(lay[pi]) if pi < len(lay) else None
        if rd is None:                                  # repli : ancienne méthode
            on, kun, mode = [], [], None
            j = lines.index('Lectures')
            vi = lines.index('Vocabulaire') if 'Vocabulaire' in lines else len(lines)
            for l in lines[j + 1:vi]:
                if l.startswith('・ON'): mode = 'on'; l = l.split(':', 1)[1].strip()
                elif l.startswith('・kun'): mode = 'kun'; l = l.split(':', 1)[1].strip()
                if l and l != '-' and mode: (on if mode == 'on' else kun).extend(l.split())
        else:
            on, kun = rd
        vi = lines.index('Vocabulaire') if 'Vocabulaire' in lines else len(lines)
        merged = []
        for l in lines[vi + 1:]:
            if is_entry(l) or not merged: merged.append(l)
            else: merged[-1] += ' ' + l
        vocab = []
        for l in merged:
            mm = is_entry(l)
            if not mm: continue
            w, r, t = mm.groups(); star = '★' in t
            t = re.sub(r'\s+', ' ', t.replace('★', '').replace('"', '')).strip()
            vocab.append({'w': w.strip(), 'r': re.sub(r'\s', '', r), 'fr': t, 'star': star})
        out.append({'n': num, 'k': kanji, 'fr': meaning, 'on': on, 'kun': kun, 'vocab': vocab})
    return out

if __name__ == '__main__':
    data = parse(sys.argv[1])
    for d in data: print(d['n'], d['k'], d['on'], d['kun'], len(d['vocab']))
    print('TOTAL kanji:', len(data), '| vocab:', sum(len(d['vocab']) for d in data),
          '| ★:', sum(1 for d in data for v in d['vocab'] if v['star']))
    bad = [v for d in data for v in d['vocab'] if not v['fr']]
    print('sans traduction:', len(bad), [v['w'] for v in bad][:10])
