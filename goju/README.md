# Goju-Ryu Karate Close-Combat Masterclass — manuscript and build

*Diagrams for Trapping, Elbows, Knees, Throws, Joint Controls, and Counter-Attacks for Sparring and Real-World Encounters*, by Dr Beverly J. Stivers.

## Finished files (`output/`)

- `...pdf`: print-ready interior, 6 × 9 in trim, single column, black and white, 335 pages, fonts embedded, mirrored KDP margins (0.875 in gutter)
- `...epub`: EPUB 3 with all 58 diagrams, embedded fonts and cover
- `...docx`: editable Word file, 6 × 9 in pages, mirrored margins, all diagrams (update the table of contents field in Word on first open)
- `..._Front-Cover.jpg`: black-and-white front cover, 1800 × 2700 px (6 × 9 in at 300 dpi)

## Structure

Six parts of three chapters each (18 chapters, every chapter over 3,000 words), plus preface, How to Use This Book, introduction, a twelve-week programme, kata application map, FAQ, glossary, closing letter and About the Author. About 74,000 words and 58 diagrams.

## Rebuilding

```
pip install weasyprint matplotlib python-docx pillow
cd figs && for f in ch*.py cover.py; do python3 $f; done && cd ..
python3 build.py all
```
