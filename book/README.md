# Signals and Systems Workbook

*600 Practice Problems on Fourier, Laplace, and Z-Transform With Step-by-Step Solutions*
by Marcus J. Thornton Ph.D

## Finished files

- `output/Signals-and-Systems-Workbook.pdf`: print-ready interior, 6 × 9 in, one column, with cover as page 1
- `output/Signals-and-Systems-Workbook.epub`: EPUB 3 with MathML equations and embedded illustrations
- `output/cover.jpg`: front cover, 1800 × 2700 px

## Layout of the sources

- `text/`: hand-written prose (preface, part openers, chapter narratives, appendices)
- `gen/`: problem generators, one per chapter. Every answer is computed with exact SymPy arithmetic and self-checked
- `gen/textfigs.py`: illustrations for the chapter narratives
- `tools/`: LaTeX master, Pandoc filter, EPUB stylesheet, cover script and build script

## Rebuilding

Requires Python 3 with sympy, numpy, scipy and matplotlib; Pandoc 3; and XeLaTeX (TeX Live) with the Libertinus and Fira fonts.

    python3 gen/textfigs.py      # narrative illustrations
    python3 tools/cover.py       # cover image
    python3 tools/build.py       # PDF and EPUB into output/
