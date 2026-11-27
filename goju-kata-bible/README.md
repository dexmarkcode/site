# Goju-Ryu Karate Kata Bible — manuscript and build

*Illustrated Textbook With Full Diagram Sequences for Gekisai, Saifa, Seiyunchin, Shisochin, Seisan, Seipai, Kururunfa, and Suparinpei With Grading Notes*, by Dr Beverly J. Stivers.

## Finished files (`output/`)

- `…Stivers.pdf`: print-ready interior, 6 × 9 in trim, single column, black and white, 309 pages (cover not included, as KDP requires)
- `…Stivers.epub`: EPUB 3 with embedded fonts and all illustrations
- `…Stivers.docx`: editable Word manuscript, 6 × 9 in page, Garamond, all illustrations (update the contents field in Word: right-click > Update Field)
- `…Front-Cover_6x9.png`: black-and-white front cover, 1800 × 2700 px (6 × 9 in at 300 dpi)

## Structure

Four parts of three chapters each: Foundations (history, stances and breathing, reading kata and grading), the Gateway Kata (Gekisai Dai Ichi and Dai Ni, Saifa, Seiyunchin), the Middle Kaishu Kata (Shisochin, Seisan, Seipai) and the Senior Kata (Kururunfa, Suparinpei, the grading floor). Back matter: grading checklists, a twelve-week programme and log, Kata at a Glance, glossary, further reading, About the Author.

## Rebuilding

```
pip install weasyprint matplotlib python-docx pymupdf
cd figs && python3 make_theory.py && python3 make_kata.py && cd ..
python3 build.py all
```

- `figs/kata_data.py` holds every count of every kata; it drives the sequence panels, the embusen maps and the count-sheet tables, so they always agree. Edit a count there and rebuild.
- `figs/lib.py` is the black-and-white figure engine (mannequin, footprints, maps).
- `manuscript/` is the chapter text (British English). `{{SEQ:key}}` and `{{MAP:key}}` insert the generated sequences and maps.
