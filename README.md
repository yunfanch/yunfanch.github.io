# Yunfan Chen — academic website

Personal academic website hosted at https://yunfanch.github.io/ using GitHub Pages.

## Update content

Edit `content.json`, then run `python3 build.py` and commit the generated files. Changes pushed to `main` are published automatically by GitHub Pages.

- Research summaries, publication records, education, and contact information live in `content.json`.
- Layout and page copy are in `build.py`.
- Appearance is in `assets/styles.css`.
- The CV page supports printing and saving as PDF through the browser.
- Publication citations are generated as downloadable BibTeX files.

No dependencies, tracking, external fonts, or build service are required. All content and navigation remain accessible without JavaScript. JavaScript adds publication filtering and the CV print button.

## Preview

Run `python3 -m http.server 8000` in this folder and open http://localhost:8000.

The CV is a selected academic record. Publication status and opportunity availability should be updated as they change. The portrait is from the public University of Michigan profile. Publication metadata was checked against publisher records; ongoing research descriptions reflect the author's academic materials.
