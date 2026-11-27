# Goju-Ryu Karate Kyohan — manuscript and build

*Illustrated Textbook With 1200 Line Drawings Showing Sanchin Tension, Rooting, Iron Body Methods, and Internal Energy Training Explained Step by Step*, by Dr Beverly J. Stivers.

## Finished files (`output/`)

- `Goju-Ryu-Karate-Kyohan_Dr-Beverly-J-Stivers.pdf` — print-ready KDP interior: 6 × 9 in trim, no bleed, single column, black and white, 393 pages, all fonts embedded, mirrored margins (0.85 in gutter, 0.6 in outside).
- `Goju-Ryu-Karate-Kyohan_Dr-Beverly-J-Stivers.epub` — EPUB 3 with greyscale images, for Google Play Books / Kindle.
- `Goju-Ryu-Karate-Kyohan_Dr-Beverly-J-Stivers.docx` — editable Word manuscript, 6 × 9 page setup, all plates embedded.
- `Goju-Ryu-Karate-Kyohan_Cover.jpg` — black-and-white front cover, 1800 × 2700 px.

## Structure

Five parts of three chapters each (15 chapters, about 54,000 words), plus safety notes, preface, list of plates, answers to review questions, training log appendix, glossary, further reading and About the Author. 173 plates containing 1,208 individual line drawings.

## Rebuilding

```
pip install weasyprint matplotlib python-docx pymupdf
cd figs && for f in ch*.py parts.py cover.py; do python3 $f; done && cd ..
python3 build.py all
```

- `figs/body.py` — the posable 3D line-drawing figure; `figs/diag.py` — footprints, hands, equipment, charts.
- Plates are numbered automatically in order of appearance; `build_counts.json` records drawings per plate.
