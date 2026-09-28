# -*- coding: utf-8 -*-
"""
Consolida las 6 variantes de identidad de Simply Andy en un solo archivo
HTML con un selector arriba (cada variante vive en su propio iframe con
srcdoc, así que reutiliza 1:1 los archivos ya probados, sin riesgo de que
choquen ids/CSS/JS entre variantes) y agrega un panel nuevo "Logo y color"
para jugar con el logo real recoloreado contra toda la paleta.
"""
import os, re
from generate import COLORS, COMMON, VARIANTS, FONTS, render

OUT_DIR = '/mnt/user-data/outputs'
os.makedirs(OUT_DIR, exist_ok=True)

def esc_attr(s):
    # Escaping mínimo y válido para meter HTML completo adentro de un
    # atributo srcdoc="..." delimitado con comillas dobles.
    return s.replace('&', '&amp;').replace('"', '&quot;')

# ---------------------------------------------------------------- logoSVG
LOGO_SVG_JS = """
function logoSVG(w, ink, dot, cap){
  cap = cap || ink;
  const h = Math.round(w*76/256);
  return '<svg viewBox="0 0 256 76" width="'+w+'" height="'+h+'" xmlns="http://www.w3.org/2000/svg">'
    + '<text x="0" y="58" font-family="Archivo, Helvetica, Arial, sans-serif" font-weight="700" font-size="76" letter-spacing="-3.42" fill="'+ink+'">andy</text>'
    + '<circle cx="177" cy="29" r="7.5" fill="'+dot+'"></circle>'
    + '<text x="188" y="25.5" font-family="DM Mono, ui-monospace, monospace" font-size="11.5" letter-spacing="1.84" fill="'+cap+'">UGC</text>'
    + '<text x="188" y="42" font-family="DM Mono, ui-monospace, monospace" font-size="11.5" letter-spacing="1.84" fill="'+cap+'">CREATOR</text>'
    + '</svg>';
}
"""

# palette used everywhere in the shell (name -> hex)
PALETTE = [
    ('Eggshell',  COLORS['BG'][0]),
    ('Tinta',     COLORS['INK'][0]),
    ('Oliva',     COLORS['OLIVA'][0]),
    ('Cuero',     COLORS['CUERO'][0]),
    ('Índigo',    COLORS['INDIGO'][0]),
    ('Bordó',     COLORS['BORDO'][0]),
    ('Mostaza',   COLORS['MOSTAZA'][0]),
    ('Terracota', COLORS['TERRACOTA'][0]),
    ('Ciruela',   COLORS['CIRUELA'][0]),
    ('Bosque',    COLORS['BOSQUE'][0]),
    ('Blanco',    '#FFFFFF'),
]
PMAP = {n: h for n, h in PALETTE}

# (texto/ink, punto/dot, texto UGC Creator/cap, fondo/bg) — cap repite ink
# salvo que valga la pena mostrar una variación de esa etiqueta por separado.
COMBOS = [
    ('Tinta', 'Cuero', 'Tinta', 'Eggshell'),
    ('Eggshell', 'Cuero', 'Eggshell', 'Tinta'),
    ('Eggshell', 'Oliva', 'Eggshell', 'Bordó'),
    ('Eggshell', 'Bordó', 'Eggshell', 'Índigo'),
    ('Blanco', 'Cuero', 'Blanco', 'Oliva'),
    ('Eggshell', 'Índigo', 'Eggshell', 'Cuero'),
    ('Oliva', 'Bordó', 'Oliva', 'Eggshell'),
    ('Bordó', 'Oliva', 'Bordó', 'Eggshell'),
    ('Eggshell', 'Mostaza', 'Eggshell', 'Bordó'),
    ('Eggshell', 'Terracota', 'Eggshell', 'Índigo'),
    ('Blanco', 'Ciruela', 'Blanco', 'Mostaza'),
    ('Eggshell', 'Bosque', 'Eggshell', 'Terracota'),
]

TABS = [(v['n'], v['title'].split('—')[1].strip(), v['slug']) for v in VARIANTS]

# ---------------------------------------------------------------- fuentes
# una entrada por propuesta: nombre de variante + su pareja de fuentes real
FONT_PAIRS = [(v['n'], v['title'].split('—')[1].strip(), FONTS[v['n']]) for v in VARIANTS]
DISPLAY_FONTS = [(f['DISPLAY_NAME'], f['DISPLAY_FONT']) for _, _, f in FONT_PAIRS]
BODY_FONTS = [(f['BODY_NAME'], f['BODY_FONT']) for _, _, f in FONT_PAIRS]
# nombre -> valor CSS font-family, para título y texto por igual (no hay
# nombres repetidos entre las 10 propuestas, así que un solo mapa alcanza)
FONT_CSS_BY_NAME = {n: v for n, v in DISPLAY_FONTS + BODY_FONTS}

# una sola hoja de Google Fonts con las 20 familias (10 de título + 10 de
# texto) usadas en el sistema, para que el laboratorio pueda cambiar entre
# ellas al instante sin pedir una hoja nueva por cada click
_seen_fams, FONT_FAMILY_SEGMENTS = set(), []
for _, _, f in FONT_PAIRS:
    for seg in re.findall(r'family=([^&]+)', f['FONT_URL']):
        if seg not in _seen_fams:
            _seen_fams.add(seg)
            FONT_FAMILY_SEGMENTS.append(seg)
FONT_LAB_FONTS_URL = ('https://fonts.googleapis.com/css2?'
                       + '&'.join(f'family={s}' for s in FONT_FAMILY_SEGMENTS)
                       + '&display=swap')

# ---------------------------------------------------------------- HEAD
HEAD = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Simply Andy — Sistema visual (10 paletas + logo + tipografía)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Archivo:wght@700&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<!--FONT_LAB_LINK-->
<style>
:root{--bg:#E9E2D0;--ink:#2A2620;--line:rgba(1,0,1,.12)}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font-family:'Poppins',system-ui,sans-serif;-webkit-font-smoothing:antialiased}
a{color:inherit}

.switcher{position:sticky;top:0;z-index:40;background:rgba(233,226,208,.94);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.switcher .row1{display:flex;align-items:center;gap:12px;padding:14px 20px 8px;flex-wrap:wrap}
.switcher .logo{display:flex;align-items:center;gap:10px}
.switcher .logo b{font-family:Poppins;font-weight:800;font-size:15px;letter-spacing:-.01em}
.switcher .sub{font-size:12.5px;color:#6b6355;margin-left:2px}
.switcher .row2{display:flex;gap:8px;padding:0 20px 14px;overflow-x:auto;flex-wrap:wrap;scrollbar-width:thin}
.tab{flex:none;font:600 13.5px Poppins,sans-serif;padding:9px 16px;border-radius:999px;border:1.5px solid var(--line);background:#fff;color:var(--ink);cursor:pointer;white-space:nowrap;transition:background .15s,color .15s,border-color .15s}
.tab:hover{border-color:rgba(1,0,1,.28)}
.tab.on{background:var(--ink);color:#fff;border-color:var(--ink)}
.tab.lab-tab{border-style:dashed}

main{display:block}
iframe.vpanel{width:100%;border:0;display:none;background:var(--bg)}
iframe.vpanel.show{display:block}
section.vpanel{display:none}
section.vpanel.show{display:block}

/* ---- Logo lab ---- */
.ll-wrap{max-width:1180px;margin:0 auto;padding:44px 22px 90px}
.ll-eyebrow{font:700 12px Poppins;letter-spacing:.14em;text-transform:uppercase;color:#8a6a3a}
.ll-h1{font-family:Archivo,Poppins,sans-serif;font-weight:700;font-size:clamp(30px,4vw,46px);margin:8px 0 10px;letter-spacing:-.01em}
.ll-lead{font-size:15.5px;line-height:1.6;color:#4a443c;max-width:640px;margin-bottom:34px}

.ll-stage{background:#fff;border:1px solid var(--line);border-radius:24px;padding:40px;display:flex;align-items:center;justify-content:center;min-height:240px;transition:background .25s}
.ll-stage svg{max-width:80%;height:auto}

.ll-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:22px}
.ll-panel{background:#fff;border:1px solid var(--line);border-radius:20px;padding:20px}
.ll-panel h4{font-family:Archivo,Poppins,sans-serif;font-size:15px;margin:0 0 4px}
.ll-panel .hint{font-size:12.5px;color:#7a7266;margin-bottom:14px}
.sw-picker{display:flex;flex-wrap:wrap;gap:8px}
.sw-dot{width:34px;height:34px;border-radius:50%;border:2px solid rgba(1,0,1,.12);cursor:pointer;position:relative;flex:none}
.sw-dot.on{border-color:var(--ink);box-shadow:0 0 0 2px #fff,0 0 0 4px var(--ink)}
.sw-dot span{position:absolute;inset:-20px -14px auto -14px;text-align:center;font-size:10.5px;font-weight:600;opacity:0;transition:opacity .15s;pointer-events:none}

.ll-combos{margin-top:26px}
.ll-combos h3{font-family:Archivo,Poppins,sans-serif;font-size:19px;margin-bottom:14px}
.combo-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.combo{background:#fff;border:1px solid var(--line);border-radius:18px;overflow:hidden;display:flex;flex-direction:column;cursor:pointer;transition:transform .15s,box-shadow .15s}
.combo:hover{transform:translateY(-3px);box-shadow:0 10px 24px rgba(1,0,1,.08)}
.combo .cstage{padding:22px 12px;display:flex;align-items:center;justify-content:center;min-height:80px}
.combo .cinfo{padding:10px 12px 14px;font-size:12px;line-height:1.5;color:#4a443c;border-top:1px solid var(--line)}
.combo .cinfo b{display:block;font-size:12.5px;color:var(--ink);margin-bottom:2px}

.ll-copybar{display:flex;align-items:center;gap:10px;margin-top:20px;flex-wrap:wrap}
.ll-copybar .chip{font:600 12.5px 'DM Mono',ui-monospace,monospace;background:#fff;border:1px solid var(--line);border-radius:999px;padding:7px 13px;cursor:pointer}
.ll-copybar .chip:hover{border-color:rgba(1,0,1,.3)}
.ll-btn{font:700 13.5px Poppins;padding:10px 18px;border-radius:999px;border:0;background:var(--ink);color:#fff;cursor:pointer}
.ll-btn:hover{opacity:.88}

.toast{opacity:0;position:fixed;left:50%;bottom:24px;transform:translate(-50%,120px);background:var(--ink);color:#fff;padding:10px 18px;border-radius:99px;font-weight:600;font-size:14px;transition:transform .3s;z-index:80}
.toast.show{transform:translate(-50%,0)}

/* ---- Font lab (comparte .ll-* y .sw-* con el logo lab) ----
   los prototipos a la izquierda y los controles (título / texto / fondo)
   compactos, ocupando el espacio libre a la derecha — todo entra junto en
   pantalla sin tener que scrollear para ver el resultado */
.ft-lab-layout{display:grid;grid-template-columns:1fr 300px;gap:22px;align-items:start}
.ft-protos{display:grid;grid-template-columns:repeat(2,1fr);gap:22px}
.ft-controls{display:flex;flex-direction:column;gap:12px}
.ft-controls .ll-panel{padding:14px 16px;border-radius:16px}
.ft-controls .ll-panel h4{font-size:13px;margin:0 0 2px}
.ft-controls .ll-panel .hint{font-size:11px;margin-bottom:9px}
.ft-controls .font-picker{gap:5px}
.ft-controls .font-chip{padding:5px 9px;font-size:11.5px;border-radius:8px}
.ft-controls .font-chip small{font-size:9px;margin-top:1px}
.ft-controls .sw-picker{gap:6px}
.ft-controls .sw-dot{width:24px;height:24px}
.ft-controls .ll-copybar{margin-top:2px;gap:6px}
.ft-controls .ll-copybar .chip{font-size:10.5px;padding:5px 10px}
.ft-controls .ll-btn{padding:9px 14px;font-size:12.5px}
.proto-label{font:700 10.5px 'DM Mono',ui-monospace,monospace;letter-spacing:.09em;text-transform:uppercase;color:#8a6a3a;margin-bottom:8px}

/* website hero */
.pw-frame{background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:0 10px 24px rgba(1,0,1,.07)}
.pw-bar{display:flex;align-items:center;gap:5px;padding:8px 10px;border-bottom:1px solid var(--line);background:#f4f0e6}
.pw-bar span{width:6px;height:6px;border-radius:50%;background:rgba(1,0,1,.16);flex:none}
.pw-url{margin-left:5px;font:500 9px Poppins,sans-serif;color:#8a8276;background:#fff;border-radius:5px;padding:2px 8px;flex:1;border:1px solid var(--line);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pw-hero{padding:20px 16px 22px;min-height:190px;transition:background .15s}
.pw-eyebrow{font:700 8.5px 'DM Mono',ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase;margin-bottom:9px;opacity:.75}
.pw-hero h3{margin:0 0 8px;font-size:21px;line-height:1.08;letter-spacing:-.01em;overflow-wrap:anywhere}
.pw-hero p{margin:0 0 13px;font-size:11.5px;line-height:1.5}
.pw-cta{display:inline-block;font:600 10.5px Poppins,sans-serif;padding:8px 14px;border-radius:999px}

/* social post: el texto de marca vive EN la imagen (pp-img, el gráfico
   diseñado); el header de arriba es UI nativa de la red y no cambia */
.pp-frame{background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:0 10px 24px rgba(1,0,1,.07)}
.pp-head{display:flex;align-items:center;gap:8px;padding:10px 12px}
.pp-avatar{width:23px;height:23px;border-radius:50%;background:#201c16;color:#fff;font:700 10px Poppins,sans-serif;display:flex;align-items:center;justify-content:center;flex:none}
.pp-handle{flex:1;font:600 11px Poppins,sans-serif;color:#201c16;line-height:1.25}
.pp-handle small{display:block;font:500 8.5px Poppins,sans-serif;color:#9a9184;font-weight:500}
.pp-img{position:relative;aspect-ratio:1/1;display:flex;align-items:center;justify-content:center;transition:background .15s}
.pp-overlay{padding:18px;width:100%;text-align:center}
.pp-overlay b{display:block;font-size:22px;line-height:1.12;margin-bottom:6px;overflow-wrap:anywhere}
.pp-overlay span{display:block;font-size:11px;line-height:1.4;opacity:.92}
.pp-actions{display:flex;gap:9px;padding:10px 12px 12px}
.pp-actions span{width:15px;height:15px;border:1.6px solid #201c16;opacity:.5;flex:none}
.pp-actions span:nth-child(1){border-radius:50% 50% 50% 2px;transform:rotate(-45deg)}
.pp-actions span:nth-child(2){border-radius:4px}
.pp-actions span:nth-child(3){border-radius:50%;clip-path:polygon(0 0,100% 50%,0 100%)}

.font-picker{display:flex;flex-wrap:wrap;gap:6px}
.font-chip{padding:8px 12px;border-radius:10px;border:1.5px solid var(--line);background:#fff;color:var(--ink);cursor:pointer;font-size:13px;line-height:1.15;text-align:left;white-space:nowrap;transition:border-color .15s,background .15s,color .15s}
.font-chip:hover{border-color:rgba(1,0,1,.3)}
.font-chip.on{border-color:var(--ink);background:var(--ink);color:#fff}
.font-chip small{display:block;font:600 10.5px Poppins,sans-serif;letter-spacing:.04em;opacity:.62;margin-top:2px}

.pair-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
.pair-card{background:#fff;border:1px solid var(--line);border-radius:18px;padding:20px 22px;cursor:pointer;transition:transform .15s,box-shadow .15s}
.pair-card:hover{transform:translateY(-3px);box-shadow:0 10px 24px rgba(1,0,1,.08)}
.pair-card .pc-sample{font-size:22px;line-height:1.15;margin-bottom:10px;overflow-wrap:anywhere}
.pair-card .pc-body{font-size:13px;line-height:1.5;color:#4a443c;margin-bottom:10px}
.pair-card .pc-info{font-size:11.5px;color:#7a7266;border-top:1px solid var(--line);padding-top:10px}
.pair-card .pc-info b{display:block;font-size:12.5px;color:var(--ink);margin-bottom:2px}

@media (max-width:1100px){.ll-grid{grid-template-columns:1fr 1fr}}
@media (max-width:900px){.combo-grid{grid-template-columns:1fr 1fr}.pair-grid{grid-template-columns:1fr}.ft-lab-layout{grid-template-columns:1fr}.ft-controls{flex-direction:row;flex-wrap:wrap}.ft-controls .ll-panel{flex:1 1 220px}.ft-controls .ll-copybar{flex:1 1 100%}}
@media (max-width:560px){.ll-grid{grid-template-columns:1fr}.combo-grid{grid-template-columns:1fr}.ft-protos{grid-template-columns:1fr;max-width:280px}.ft-controls{flex-direction:column}.ft-controls .ll-panel{flex:none}}
</style>
</head>
"""
HEAD = HEAD.replace('<!--FONT_LAB_LINK-->', f'<link href="{FONT_LAB_FONTS_URL}" rel="stylesheet">')

def logo_svg_py(w, ink, dot, cap=None):
    cap = cap or ink
    h = round(w * 76 / 256)
    return (f'<svg viewBox="0 0 256 76" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">'
            f'<text x="0" y="58" font-family="Archivo, Helvetica, Arial, sans-serif" font-weight="700" font-size="76" letter-spacing="-3.42" fill="{ink}">andy</text>'
            f'<circle cx="177" cy="29" r="7.5" fill="{dot}"></circle>'
            f'<text x="188" y="25.5" font-family="DM Mono, ui-monospace, monospace" font-size="11.5" letter-spacing="1.84" fill="{cap}">UGC</text>'
            f'<text x="188" y="42" font-family="DM Mono, ui-monospace, monospace" font-size="11.5" letter-spacing="1.84" fill="{cap}">CREATOR</text>'
            f'</svg>')

def build_body():
    parts = []
    parts.append('<body>\n')

    # ---- switcher bar ----
    parts.append('<div class="switcher">\n  <div class="row1">\n')
    parts.append('    <div class="logo">' + logo_svg_py(112, PMAP['Tinta'], PMAP['Cuero']) + '<b>Simply Andy</b></div>\n')
    parts.append('    <span class="sub">Sistema visual — 10 paletas + laboratorio de logo y tipografía</span>\n')
    parts.append('  </div>\n  <div class="row2" id="tabRow">\n')
    for n, name, slug in TABS:
        active = ' on' if n == 1 else ''
        parts.append(f'    <button type="button" class="tab{active}" data-target="vf{n}">{n:02d} · {name}</button>\n')
    parts.append('    <button type="button" class="tab lab-tab" data-target="fontlab">Aa Tipografía</button>\n')
    parts.append('    <button type="button" class="tab lab-tab" data-target="logolab">✷ Logo y color</button>\n')
    parts.append('  </div>\n</div>\n\n<main>\n')

    # ---- 6 iframes ----
    for v in VARIANTS:
        html = render(v)
        srcdoc = esc_attr(html)
        show = ' show' if v['n'] == 1 else ''
        parts.append(f'<iframe class="vpanel{show}" id="vf{v["n"]}" title="{v["title"]}" srcdoc="{srcdoc}"></iframe>\n')

    # ---- font lab panel ----
    parts.append(build_fontlab())

    # ---- logo lab panel ----
    parts.append(build_logolab())

    parts.append('</main>\n')
    parts.append('<div class="toast" id="toast"></div>\n')
    parts.append(build_script())
    parts.append('</body>\n</html>\n')
    return ''.join(parts)

FT_SAMPLE_BODY = ('Así se ve un párrafo completo con esta tipografía: legible a tamaño '
                   'chico, con buen espaciado entre líneas y personalidad propia en los títulos.')

# copy real de marca (mismas frases de la guía de voz de Andy), repartida
# entre los tres prototipos para que cada uno se sienta como una pieza real.
# La fuente de marca solo pisa texto DISEÑADO (hero del sitio, imagen del
# post, overlay del reel). La caption tipiada debajo del post es nativa de
# la red — siempre en la tipografía de la app — así que no cambia con el
# selector, tal como pasaría en Instagram/TikTok de verdad.
FT_WEB_TITLE = COMMON['HEADLINE']
FT_WEB_BODY = 'Historias reales, sin que se sienta a anuncio.'
FT_POST_OVERLAY_TITLE = 'No lo esperaba, pero funcionó.'
FT_POST_OVERLAY_SUB = 'Historia completa en el video.'

def build_fontlab():
    out = ['<section class="vpanel" id="fontlab">\n  <div class="ll-wrap">\n']
    out.append('    <div class="ll-eyebrow">Tipografía</div>\n')
    out.append('    <h1 class="ll-h1">Prueba las fuentes reales.</h1>\n')
    out.append('    <p class="ll-lead">Las 10 propuestas usan una fuente de título y una de texto '
                'distintas cada una. El cambio se aplica solo al texto diseñado (el hero del sitio y la '
                'imagen del post) — el header y los iconos son UI nativa de la red y no cambian, como en la '
                'vida real. Elegí una fuente y probá también otros fondos, todo sin perder de vista la vista previa.</p>\n')

    out.append('    <div class="ft-lab-layout">\n')

    out.append('      <div class="ft-protos">\n')

    # sitio web
    out.append('        <div class="proto proto-web">\n          <div class="proto-label">Sitio web</div>\n')
    out.append('          <div class="pw-frame">\n            <div class="pw-bar"><span></span><span></span><span></span>'
                f'<div class="pw-url">{COMMON["SITE_URL"]}</div></div>\n')
    out.append('            <div class="pw-hero" id="pwHero">\n              '
                f'<div class="pw-eyebrow">UGC · {COMMON["HANDLE"]}</div>\n'
                f'              <h3 class="ft-disp">{FT_WEB_TITLE}</h3>\n              <p class="ft-body">{FT_WEB_BODY}</p>\n'
                '              <span class="pw-cta">Ver el trabajo</span>\n            </div>\n          </div>\n        </div>\n')

    # post de redes — el header de arriba es nativo (fuente fija); la
    # fuente de marca solo vive en la imagen (pp-img); abajo solo quedan
    # los iconos, también nativos
    out.append('        <div class="proto proto-post">\n          <div class="proto-label">Post</div>\n')
    out.append('          <div class="pp-frame">\n            <div class="pp-head"><div class="pp-avatar">A</div>'
                f'<div class="pp-handle">{COMMON["HANDLE"]}<small>Colaboración pagada</small></div></div>\n')
    out.append('            <div class="pp-img" id="ppImg">\n              <div class="pp-overlay">\n                '
                f'<b class="ft-disp">{FT_POST_OVERLAY_TITLE}</b><span class="ft-body">{FT_POST_OVERLAY_SUB}</span>\n'
                '              </div>\n            </div>\n')
    out.append('            <div class="pp-actions"><span></span><span></span><span></span></div>\n')
    out.append('          </div>\n        </div>\n')

    out.append('      </div>\n')

    out.append('      <div class="ft-controls">\n')
    for label, key, opts in (('Título', 'display', DISPLAY_FONTS), ('Texto', 'body', BODY_FONTS)):
        out.append(f'        <div class="ll-panel">\n          <h4>{label}</h4>\n          <p class="hint">Toca una fuente para aplicarla.</p>\n          <div class="font-picker" data-role="{key}">\n')
        for name, cssval in opts:
            out.append(f'            <button type="button" class="font-chip" data-name="{name}" style="font-family:{cssval}">{name}</button>\n')
        out.append('          </div>\n        </div>\n')
    out.append('        <div class="ll-panel">\n          <h4>Fondo</h4>\n          <p class="hint">Toca un color para probarlo.</p>\n          <div class="sw-picker" data-role="ftbg">\n')
    for name, hexv in PALETTE:
        out.append(f'            <div class="sw-dot" data-hex="{hexv}" data-name="{name}" style="background:{hexv}" title="{name}"></div>\n')
    out.append('          </div>\n        </div>\n')
    out.append('        <div class="ll-copybar">\n')
    out.append('          <button type="button" class="ll-btn" id="ftCopyAll">Copiar combinación</button>\n')
    out.append('          <span class="chip" id="chipDisplay"></span><span class="chip" id="chipBody"></span><span class="chip" id="chipFtBg"></span>\n')
    out.append('        </div>\n')
    out.append('      </div>\n')

    out.append('    </div>\n')

    out.append('    <div class="ll-combos">\n      <h3>Parejas usadas en el sistema</h3>\n      <div class="pair-grid">\n')
    for n, name, f in FONT_PAIRS:
        out.append(f'        <div class="pair-card" data-display="{f["DISPLAY_NAME"]}" data-body="{f["BODY_NAME"]}">\n')
        out.append(f'          <div class="pc-sample" style="font-family:{f["DISPLAY_FONT"]}">{COMMON["HEADLINE"]}</div>\n')
        out.append(f'          <div class="pc-body" style="font-family:{f["BODY_FONT"]}">{FT_SAMPLE_BODY}</div>\n')
        out.append(f'          <div class="pc-info"><b>{n:02d} · {name}</b>Título {f["DISPLAY_NAME"]} · Texto {f["BODY_NAME"]}</div>\n')
        out.append('        </div>\n')
    out.append('      </div>\n    </div>\n')

    out.append('  </div>\n</section>\n')
    return ''.join(out)

def build_logolab():
    out = ['<section class="vpanel" id="logolab">\n  <div class="ll-wrap">\n']
    out.append('    <div class="ll-eyebrow">Logo y color</div>\n')
    out.append('    <h1 class="ll-h1">Prueba el logo real.</h1>\n')
    out.append('    <p class="ll-lead">El nombre y la forma del logo no cambian: lo único que se prueba aquí es qué colores de la paleta puede llevar. Elige texto, punto, la etiqueta "UGC Creator" y fondo por separado, o parte de una combinación ya revisada por contraste.</p>\n')

    out.append('    <div class="ll-stage" id="llStage"></div>\n')

    out.append('    <div class="ll-grid">\n')
    for label, key in (('Texto', 'ink'), ('Punto', 'dot'), ('UGC Creator', 'cap'), ('Fondo', 'bg')):
        out.append(f'      <div class="ll-panel">\n        <h4>{label}</h4>\n        <p class="hint">Toca un color para aplicarlo.</p>\n        <div class="sw-picker" data-role="{key}">\n')
        for name, hexv in PALETTE:
            out.append(f'          <div class="sw-dot" data-hex="{hexv}" data-name="{name}" style="background:{hexv}" title="{name}"></div>\n')
        out.append('        </div>\n      </div>\n')
    out.append('    </div>\n')

    out.append('    <div class="ll-copybar">\n')
    out.append('      <button type="button" class="ll-btn" id="llCopyAll">Copiar combinación</button>\n')
    out.append('      <span class="chip" id="chipInk"></span><span class="chip" id="chipDot"></span><span class="chip" id="chipCap"></span><span class="chip" id="chipBg"></span>\n')
    out.append('    </div>\n')

    out.append('    <div class="ll-combos">\n      <h3>Combinaciones ya revisadas</h3>\n      <div class="combo-grid">\n')
    for ink, dot, cap, bg in COMBOS:
        out.append(f'        <div class="combo" data-ink="{ink}" data-dot="{dot}" data-cap="{cap}" data-bg="{bg}">\n')
        out.append(f'          <div class="cstage" style="background:{PMAP[bg]}">' + logo_svg_py(120, PMAP[ink], PMAP[dot], PMAP[cap]) + '</div>\n')
        cap_line = f'UGC Creator {cap} · ' if cap != ink else ''
        out.append(f'          <div class="cinfo"><b>{ink} sobre {bg}</b>{cap_line}Punto {dot}</div>\n')
        out.append('        </div>\n')
    out.append('      </div>\n    </div>\n')

    out.append('  </div>\n</section>\n')
    return ''.join(out)

def build_script():
    return """<script>
""" + LOGO_SVG_JS + """
const toast = document.getElementById('toast');
function notify(t){toast.textContent=t;toast.classList.add('show');clearTimeout(notify.t);notify.t=setTimeout(()=>toast.classList.remove('show'),1400)}
function copy(txt,msg){
  (navigator.clipboard?navigator.clipboard.writeText(txt):Promise.reject()).then(()=>notify(msg),()=>{
    const ta=document.createElement('textarea');ta.value=txt;document.body.appendChild(ta);ta.select();
    try{document.execCommand('copy')}catch(e){} ta.remove();notify(msg);
  });
}

// ---- panel switching ----
const panels = Array.from(document.querySelectorAll('.vpanel'));
const tabs = Array.from(document.querySelectorAll('.tab'));
function fitIframe(ifr){
  try{
    const doc = ifr.contentDocument;
    if(!doc) return;
    const h = Math.max(doc.documentElement.scrollHeight, doc.body ? doc.body.scrollHeight : 0);
    if(h>0) ifr.style.height = h + 'px';
  }catch(e){}
}
function wireAnchors(ifr){
  try{
    const doc = ifr.contentDocument;
    doc.querySelectorAll('header nav a[href^="#"]').forEach(a=>{
      a.addEventListener('click', function(e){
        e.preventDefault();
        const id = a.getAttribute('href').slice(1);
        const target = doc.getElementById(id);
        if(!target) return;
        const rect = target.getBoundingClientRect();
        const ifrRect = ifr.getBoundingClientRect();
        const top = window.scrollY + ifrRect.top + rect.top - 96;
        window.scrollTo({top, behavior:'smooth'});
      });
    });
  }catch(e){}
}
panels.forEach(p=>{
  if(p.tagName==='IFRAME'){
    p.addEventListener('load', ()=>{ fitIframe(p); wireAnchors(p); });
  }
});
function showPanel(id){
  panels.forEach(p=>p.classList.toggle('show', p.id===id));
  tabs.forEach(t=>t.classList.toggle('on', t.dataset.target===id));
  const active = document.getElementById(id);
  if(active && active.tagName==='IFRAME'){ fitIframe(active); wireAnchors(active); }
  window.scrollTo({top:0, behavior:'instant' in document.documentElement.style ? 'instant' : 'auto'});
}
tabs.forEach(t=>t.addEventListener('click', ()=>showPanel(t.dataset.target)));
let resizeT;
window.addEventListener('resize', ()=>{
  clearTimeout(resizeT);
  resizeT = setTimeout(()=>{
    const active = panels.find(p=>p.classList.contains('show'));
    if(active && active.tagName==='IFRAME') fitIframe(active);
  }, 200);
});

// ---- logo lab ----
const ll = {ink:'""" + PMAP['Tinta'] + """', dot:'""" + PMAP['Cuero'] + """', cap:'""" + PMAP['Tinta'] + """', bg:'""" + PMAP['Eggshell'] + """'};
const llNames = {};
document.querySelectorAll('.sw-dot').forEach(el=>{ llNames[el.dataset.hex] = el.dataset.name; });
function llRender(){
  document.getElementById('llStage').style.background = ll.bg;
  document.getElementById('llStage').innerHTML = logoSVG(220, ll.ink, ll.dot, ll.cap);
  document.querySelectorAll('#logolab .sw-picker').forEach(p=>{
    const role = p.dataset.role;
    p.querySelectorAll('.sw-dot').forEach(d=>d.classList.toggle('on', d.dataset.hex.toLowerCase()===ll[role].toLowerCase()));
  });
  document.getElementById('chipInk').textContent = 'Texto ' + ll.ink;
  document.getElementById('chipDot').textContent = 'Punto ' + ll.dot;
  document.getElementById('chipCap').textContent = 'UGC Creator ' + ll.cap;
  document.getElementById('chipBg').textContent = 'Fondo ' + ll.bg;
}
document.querySelectorAll('#logolab .sw-picker').forEach(picker=>{
  const role = picker.dataset.role;
  picker.querySelectorAll('.sw-dot').forEach(dot=>{
    dot.addEventListener('click', ()=>{ ll[role] = dot.dataset.hex; llRender(); });
  });
});
document.getElementById('llCopyAll').addEventListener('click', ()=>{
  copy('Texto '+ll.ink+' / Punto '+ll.dot+' / UGC Creator '+ll.cap+' / Fondo '+ll.bg, 'Combinación copiada');
});
const hexByName = {};
""" + '\n'.join([f"hexByName['{n}']='{h}';" for n, h in PALETTE]) + """
document.querySelectorAll('.combo').forEach(c=>{
  c.addEventListener('click', ()=>{
    ll.ink = hexByName[c.dataset.ink];
    ll.dot = hexByName[c.dataset.dot];
    ll.cap = hexByName[c.dataset.cap];
    ll.bg = hexByName[c.dataset.bg];
    llRender();
    notify('Combinación aplicada');
  });
});
llRender();

// ---- font lab ----
const fontCssByName = {};
""" + '\n'.join([f"fontCssByName['{n}']={v!r};" for n, v in FONT_CSS_BY_NAME.items()]) + """
const ft = {display:'""" + FONT_PAIRS[0][2]['DISPLAY_NAME'] + """', body:'""" + FONT_PAIRS[0][2]['BODY_NAME'] + """', bg:'Cuero'};
function relLum(hex){
  const c = hex.replace('#','');
  const chan = v => { v = parseInt(v,16)/255; return v<=0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055,2.4); };
  return 0.2126*chan(c.slice(0,2)) + 0.7152*chan(c.slice(2,4)) + 0.0722*chan(c.slice(4,6));
}
function ftRender(){
  document.querySelectorAll('.ft-disp').forEach(el=>{ el.style.fontFamily = fontCssByName[ft.display]; });
  document.querySelectorAll('.ft-body').forEach(el=>{ el.style.fontFamily = fontCssByName[ft.body]; });
  document.querySelectorAll('.font-picker').forEach(p=>{
    const role = p.dataset.role === 'display' ? 'display' : 'body';
    p.querySelectorAll('.font-chip').forEach(c=>c.classList.toggle('on', c.dataset.name===ft[role]));
  });

  // fondo: sitio y post se tiñen claros/oscuros según el color elegido
  const bgHex = hexByName[ft.bg];
  const light = relLum(bgHex) > 0.42;
  const ink = light ? '#201c16' : '#fff';
  const pwHero = document.getElementById('pwHero');
  pwHero.style.background = bgHex;
  pwHero.style.color = ink;
  const cta = pwHero.querySelector('.pw-cta');
  cta.style.background = light ? '#201c16' : '#fff';
  cta.style.color = light ? '#fff' : '#201c16';
  const ppImg = document.getElementById('ppImg');
  ppImg.style.background = bgHex;
  ppImg.querySelector('.pp-overlay').style.color = ink;
  document.querySelectorAll('#fontlab .sw-picker').forEach(p=>{
    p.querySelectorAll('.sw-dot').forEach(d=>d.classList.toggle('on', d.dataset.hex.toLowerCase()===bgHex.toLowerCase()));
  });

  document.getElementById('chipDisplay').textContent = 'Título ' + ft.display;
  document.getElementById('chipBody').textContent = 'Texto ' + ft.body;
  document.getElementById('chipFtBg').textContent = 'Fondo ' + ft.bg;
}
document.querySelectorAll('.font-picker').forEach(picker=>{
  const role = picker.dataset.role === 'display' ? 'display' : 'body';
  picker.querySelectorAll('.font-chip').forEach(chip=>{
    chip.addEventListener('click', ()=>{ ft[role] = chip.dataset.name; ftRender(); });
  });
});
document.querySelectorAll('#fontlab .sw-picker[data-role="ftbg"] .sw-dot').forEach(dot=>{
  dot.addEventListener('click', ()=>{ ft.bg = dot.dataset.name; ftRender(); });
});
document.getElementById('ftCopyAll').addEventListener('click', ()=>{
  copy('Título '+ft.display+' / Texto '+ft.body+' / Fondo '+ft.bg, 'Combinación copiada');
});
document.querySelectorAll('.pair-card').forEach(c=>{
  c.addEventListener('click', ()=>{
    ft.display = c.dataset.display;
    ft.body = c.dataset.body;
    ftRender();
    notify('Pareja aplicada');
  });
});
ftRender();

// show first panel state (already marked via class in markup); make sure
// the visible iframe on first paint gets measured once fonts/layout settle.
window.addEventListener('load', ()=>{
  const active = panels.find(p=>p.classList.contains('show'));
  if(active && active.tagName==='IFRAME') setTimeout(()=>fitIframe(active), 250);
});
</script>
"""

def main():
    html = HEAD + build_body()
    path = os.path.join(OUT_DIR, 'simply-andy-identidad-completo.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('wrote', path, len(html))

if __name__ == '__main__':
    main()
