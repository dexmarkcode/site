# Electric Circuits Workbook — Marcus J. Thornton, PhD

Finished files are in `output/`:

- `Electric_Circuits_Workbook_Marcus_J_Thornton.pdf`: print/ebook PDF, 7 × 10 in, single column, 541 pages
- `Electric_Circuits_Workbook_Marcus_J_Thornton.epub`: reflowable EPUB 3 with embedded fonts and 493 illustrations

## Rebuilding

    pip install weasyprint schemdraw matplotlib ebooklib markdown numpy
    python3 build.py

- `content/`: teaching text (Markdown), front and back matter
- `problems/`: the 800 problems; every answer is calculated in code, so solutions always match the questions
- `figs_text.py`: chapter illustrations; `lib.py`: circuit-diagram and formatting helpers
- `style/`: print, EPUB and cover stylesheets; `fonts/`: EB Garamond and Cormorant Garamond (SIL Open Font Licence)
