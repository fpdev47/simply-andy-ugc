# -*- coding: utf-8 -*-
import os, re

with open('/home/claude/build/base-template.html', encoding='utf-8') as f:
    BASE = f.read()

COLORS = {
    'BG':        ('#E9E2D0', 'Eggshell'),
    'INK':       ('#2A2620', 'Tinta'),
    'OLIVA':     ('#61603A', 'Oliva'),
    'CUERO':     ('#864C24', 'Cuero'),
    'INDIGO':    ('#1F2C44', 'Índigo'),
    'BORDO':     ('#51091B', 'Bordó'),
    'MOSTAZA':   ('#805613', 'Mostaza'),
    'TERRACOTA': ('#8F3F23', 'Terracota'),
    'CIRUELA':   ('#4B1E3D', 'Ciruela'),
    'BOSQUE':    ('#2E4636', 'Bosque'),
}
RGB = {
    'OLIVA':     '97,96,58',
    'CUERO':     '134,76,36',
    'INDIGO':    '31,44,68',
    'BORDO':     '81,9,27',
    'MOSTAZA':   '128,86,19',
    'TERRACOTA': '143,63,35',
    'CIRUELA':   '75,30,61',
    'BOSQUE':    '46,70,54',
}

COMMON = {
    'BRAND_NAME': 'Simply Andy',
    'HANDLE': '@__simplyandy',
    'SITE_URL': 'simplyandy.com',
    'HEADLINE': 'Contenido real, sin filtro.',
    'BG': COLORS['BG'][0], 'BG_NAME': COLORS['BG'][1],
    'INK': COLORS['INK'][0], 'INK_NAME': COLORS['INK'][1],
}

FONTS = {
    1: dict(DISPLAY_FONT="'Bevan'", DISPLAY_NAME='Bevan',
            BODY_FONT="'Nunito Sans'", BODY_NAME='Nunito Sans',
            FONT_URL='https://fonts.googleapis.com/css2?family=Bevan:ital@0;1&family=Nunito+Sans:wght@400;500;600;700&display=swap',
            DISPLAY_SPECIMEN='https://fonts.google.com/specimen/Bevan',
            BODY_SPECIMEN='https://fonts.google.com/specimen/Nunito+Sans'),
    2: dict(DISPLAY_FONT="'Space Grotesk'", DISPLAY_NAME='Space Grotesk',
            BODY_FONT="'Karla'", BODY_NAME='Karla',
            FONT_URL='https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Karla:wght@400;500;600;700&display=swap',
            DISPLAY_SPECIMEN='https://fonts.google.com/specimen/Space+Grotesk',
            BODY_SPECIMEN='https://fonts.google.com/specimen/Karla'),
    3: dict(DISPLAY_FONT="'Archivo'", DISPLAY_NAME='Archivo',
            BODY_FONT="'Onest'", BODY_NAME='Onest',
            FONT_URL='https://fonts.googleapis.com/css2?family=Archivo:wght@400;700;900&family=Onest:wght@400;500;600;700&display=swap',
            DISPLAY_SPECIMEN='https://fonts.google.com/specimen/Archivo',
            BODY_SPECIMEN='https://fonts.google.com/specimen/Onest'),
    4: dict(DISPLAY_FONT="'Unbounded'", DISPLAY_NAME='Unbounded',
            BODY_FONT="'Sora'", BODY_NAME='Sora',
            FONT_URL='https://fonts.googleapis.com/css2?family=Unbounded:wght@400;600;800&family=Sora:wght@400;500;600;700&display=swap',
            DISPLAY_SPECIMEN='https://fonts.google.com/specimen/Unbounded',
            BODY_SPECIMEN='https://fonts.google.com/specimen/Sora'),
    5: dict(DISPLAY_FONT="'Playfair Display'", DISPLAY_NAME='Playfair Display',
            BODY_FONT="'Manrope'", BODY_NAME='Manrope',
            FONT_URL='https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Manrope:wght@400;500;600;700&display=swap',
            DISPLAY_SPECIMEN='https://fonts.google.com/specimen/Playfair+Display',
            BODY_SPECIMEN='https://fonts.google.com/specimen/Manrope'),
    6: dict(DISPLAY_FONT="'Big Shoulders'", DISPLAY_NAME='Big Shoulders',
            BODY_FONT="'Work Sans'", BODY_NAME='Work Sans',
            FONT_URL='https://fonts.googleapis.com/css2?family=Big+Shoulders:wght@400;700;900&family=Work+Sans:wght@400;500;600;700&display=swap',
            DISPLAY_SPECIMEN='https://fonts.google.com/specimen/Big+Shoulders',
            BODY_SPECIMEN='https://fonts.google.com/specimen/Work+Sans'),
    7: dict(DISPLAY_FONT="'Titan One'", DISPLAY_NAME='Titan One',
            BODY_FONT="'Mulish'", BODY_NAME='Mulish',
            FONT_URL='https://fonts.googleapis.com/css2?family=Titan+One&family=Mulish:wght@400;500;600;700&display=swap',
            DISPLAY_SPECIMEN='https://fonts.google.com/specimen/Titan+One',
            BODY_SPECIMEN='https://fonts.google.com/specimen/Mulish'),
    8: dict(DISPLAY_FONT="'Bungee'", DISPLAY_NAME='Bungee',
            BODY_FONT="'Figtree'", BODY_NAME='Figtree',
            FONT_URL='https://fonts.googleapis.com/css2?family=Bungee&family=Figtree:wght@400;500;600;700&display=swap',
            DISPLAY_SPECIMEN='https://fonts.google.com/specimen/Bungee',
            BODY_SPECIMEN='https://fonts.google.com/specimen/Figtree'),
    9: dict(DISPLAY_FONT="'Fraunces'", DISPLAY_NAME='Fraunces',
            BODY_FONT="'Plus Jakarta Sans'", BODY_NAME='Plus Jakarta Sans',
            FONT_URL='https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,500;0,600;0,700;1,500&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap',
            DISPLAY_SPECIMEN='https://fonts.google.com/specimen/Fraunces',
            BODY_SPECIMEN='https://fonts.google.com/specimen/Plus+Jakarta+Sans'),
    10: dict(DISPLAY_FONT="'Righteous'", DISPLAY_NAME='Righteous',
            BODY_FONT="'Albert Sans'", BODY_NAME='Albert Sans',
            FONT_URL='https://fonts.googleapis.com/css2?family=Righteous&family=Albert+Sans:wght@400;500;600;700&display=swap',
            DISPLAY_SPECIMEN='https://fonts.google.com/specimen/Righteous',
            BODY_SPECIMEN='https://fonts.google.com/specimen/Albert+Sans'),
}

# role assignment: ACC1, ACC2, DEEP, SUPPORT <- keys into COLORS/RGB
VARIANTS = [
    dict(n=1, slug='01-cuaderno', title='Simply Andy — Cuaderno',  ACC1='CUERO',  ACC2='OLIVA',  DEEP='BORDO',  SUPPORT='INDIGO'),
    dict(n=2, slug='02-tierra',   title='Simply Andy — Tierra',    ACC1='OLIVA',  ACC2='CUERO',  DEEP='INDIGO', SUPPORT='BORDO'),
    dict(n=3, slug='03-nocturno', title='Simply Andy — Nocturno',  ACC1='INDIGO', ACC2='CUERO',  DEEP='BORDO',  SUPPORT='OLIVA'),
    dict(n=4, slug='04-bordo',    title='Simply Andy — Bordó',     ACC1='BORDO',  ACC2='OLIVA',  DEEP='INDIGO', SUPPORT='CUERO'),
    dict(n=5, slug='05-editorial',title='Simply Andy — Editorial', ACC1='CUERO',  ACC2='INDIGO', DEEP='OLIVA',  SUPPORT='BORDO'),
    dict(n=6, slug='06-impacto',  title='Simply Andy — Impacto',   ACC1='OLIVA',  ACC2='BORDO',  DEEP='CUERO',  SUPPORT='INDIGO'),
    dict(n=7,  slug='07-dorado',    title='Simply Andy — Dorado',    ACC1='MOSTAZA',   ACC2='BORDO',      DEEP='INDIGO',  SUPPORT='OLIVA'),
    dict(n=8,  slug='08-terracota', title='Simply Andy — Terracota', ACC1='TERRACOTA', ACC2='OLIVA',      DEEP='INDIGO',  SUPPORT='CUERO'),
    dict(n=9,  slug='09-ciruela',   title='Simply Andy — Ciruela',   ACC1='CIRUELA',   ACC2='MOSTAZA',    DEEP='BORDO',   SUPPORT='OLIVA'),
    dict(n=10, slug='10-bosque',    title='Simply Andy — Bosque',    ACC1='BOSQUE',    ACC2='TERRACOTA',  DEEP='CIRUELA', SUPPORT='CUERO'),
]

OUT_DIR = '/mnt/user-data/outputs'
os.makedirs(OUT_DIR, exist_ok=True)

def render(variant):
    tokens = dict(COMMON)
    tokens['TITLE'] = variant['title']
    tokens.update(FONTS[variant['n']])
    for role in ('ACC1', 'ACC2', 'DEEP', 'SUPPORT'):
        key = variant[role]
        hexv, name = COLORS[key]
        tokens[role] = hexv
        tokens[role + '_NAME'] = name
    tokens['ACC1_RGB'] = RGB[variant['ACC1']]

    out = BASE
    # replace longest keys first to avoid partial-name collisions (e.g. ACC1 vs ACC1_NAME vs ACC1_RGB)
    for key in sorted(tokens.keys(), key=len, reverse=True):
        out = out.replace('{{%s}}' % key, tokens[key])

    leftover = re.findall(r'\{\{[A-Z0-9_]+\}\}', out)
    if leftover:
        raise SystemExit(f"Leftover tokens in variant {variant['slug']}: {set(leftover)}")
    return out

if __name__ == '__main__':
    for v in VARIANTS:
        html = render(v)
        path = os.path.join(OUT_DIR, f"simply-andy-identidad-{v['slug']}.html")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print('wrote', path, len(html))
