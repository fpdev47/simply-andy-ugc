# Simply Andy — Identidad visual

Sistema de identidad visual para Simply Andy (@__simplyandy), creadora de contenido UGC.

## Contenido

- `dist/simply-andy-identidad-completo.html` — vista consolidada con las 10 paletas, el laboratorio de logo/color y el laboratorio de tipografía interactivo.
- `dist/simply-andy-identidad-01-cuaderno.html` ... `10-bosque.html` — cada una de las 10 propuestas de paleta/tipografía como página independiente.
- `src/generate.py` — genera las 10 páginas individuales a partir de `base-template.html`.
- `src/generate_merged.py` — genera la vista consolidada (`dist/simply-andy-identidad-completo.html`).
- `src/base-template.html` — plantilla base con tokens `{{TOKEN}}` que `generate.py` reemplaza por paleta/tipografía.

## Regenerar

```bash
cd src
python3 generate.py          # regenera dist/simply-andy-identidad-*.html
python3 generate_merged.py   # regenera dist/simply-andy-identidad-completo.html
```
