# SalesTrack website

Official website for **SalesTrack**: Lead. Connect. Grow.
Live domain: https://www.salestrack.co.in

A fast, static website (HTML, CSS and JavaScript only, no frameworks) with four pages: Home, Services, About and Contact.

## Folder structure

| Path | What it is |
|---|---|
| `dist/` | **The finished website.** Upload the contents of this folder to your web host. |
| `src/assets/` | Stylesheets, JavaScript, fonts, logo images and licence texts |
| `build.py` | Generates every page in `dist/` from shared header, footer and section components |
| `LICENCES.md` | Third-party licences, originality record and pre-launch checklist |

## Editing the site

1. Edit page content in `build.py`, or styles and scripts in `src/assets/`.
2. Rebuild: `python3 build.py`
3. Upload the new `dist/` folder.

To preview locally: `cd dist && python3 -m http.server 8000`, then open http://localhost:8000

## Licences

The code was written for SalesTrack. Fonts (SIL OFL 1.1) and adapted icon outlines (Feather MIT / Lucide ISC) are credited in `LICENCES.md`, with full licence texts in `src/assets/licences/`.
