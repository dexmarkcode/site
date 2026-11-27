# Goju-Ryu Karate Sanchin Masterclass — manuscript and build

*Illustrated Textbook With Frame-by-Frame Diagrams, Testing Drills, Posture Corrections, and Strength Progressions for the Foundational Form*, by Dr Beverly J. Stivers.

## Finished files (`output/`)

- `…pdf` — print-ready interior, 6 × 9 in trim (Amazon KDP), single column, black and white, fonts embedded
- `…epub` — EPUB 3 with black-and-white cover
- `…docx` — editable Word manuscript, 6 × 9 in page, mirrored margins (right-click the Contents block and choose Update Field)

## Structure

Nine parts of three chapters each (27 chapters), preface, safety notes, How to Use This Book, three appendices (kata at a glance, testing scorecards and logs, assessment record and 12-week planner), glossary, further reading and About the Author. About 94,000 words and 100 black-and-white illustrations.

## Rebuilding

```
pip install weasyprint matplotlib python-docx
cd figs && for f in ch*.py parts.py cover.py; do python3 $f; done && cd ..
python3 build.py all
```

- `manuscript/` — chapter text in Markdown (British English)
- `figs/` — Python scripts that draw every illustration into `figures/` (`common.py` holds the 3D mannequin)
- `style/` — print (WeasyPrint) and EPUB stylesheets; `make_reference.py` styles the DOCX
- `book_meta.py` — title, author, part titles and introductions, chapter order
