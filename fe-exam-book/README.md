# Electrical Engineering FE Exam Prep 2026–2027

*The Complete Study Guide: 800 Practice Questions, Formulas, and Mock Exams to Pass First Time*, by Marcus J. Thornton, Ph.D.

## Final files (`output/`)

| File | Use |
|---|---|
| `Electrical-Engineering-FE-Exam-Prep-2026-2027_Marcus-J-Thornton.pdf` | 600-page print-quality interior, 7 × 10 in, single column, cover as page 1 |
| `Electrical-Engineering-FE-Exam-Prep-2026-2027_Marcus-J-Thornton.epub` | EPUB 3 with embedded fonts and MathML; passes EpubCheck with no errors |
| `Cover_1600x2286.png` | Front cover for store listings |

## Contents

- Front matter, 6 parts × 3 chapters (18 chapters), appendices, glossary
- 800 original questions with full worked solutions: a 20-question diagnostic, 14 chapter sets of 36, a 56-question timed drill and two 110-question mock exams with answer keys and scoring sheets
- About 60 chapter illustrations plus per-question circuit schematics

## Rebuilding

Requirements: Pandoc 3, XeLaTeX (TeX Live), TeX Gyre fonts, Python 3 with matplotlib and schemdraw.

```
python3 gen/figures.py          # chapter illustrations
python3 gen/cover.py            # cover
cd gen && python3 make_questions.py && cd ..   # all 800 questions (deterministic)
python3 build.py                # PDF and EPUB into build/
```

Prose lives in `src/`. Question templates live in `gen/t_*.py`, and the hand-written conceptual questions in `gen/concepts.py`.
