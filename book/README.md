# Electric Vehicle Engineering — manuscript and build

*A Modern Textbook on EV Powertrains, Batteries, Motors, Charging, and Power Electronics*, by Marcus J. Thornton, Ph.D.

## Finished files (`output/`)

- `Electric-Vehicle-Engineering_Marcus-J-Thornton.pdf`: print-ready interior, 6 × 9 in trim, single column, 335 pages
- `Electric-Vehicle-Engineering_Marcus-J-Thornton.epub`: EPUB 3, passes EPUBCheck with no errors or warnings
- `Electric-Vehicle-Engineering_Cover.jpg`: front cover, 1800 × 2700 px (6 × 9 in at 300 dpi)

## Structure

Five parts of three chapters each (15 chapters), plus a preface, How to Use This Book, Appendix A (answers), Appendix B (data and formulae), a glossary, further reading and About the Author.

## Rebuilding

```
pip install weasyprint matplotlib schemdraw ebooklib
cd figs && for f in ch*.py cover.py; do python3 $f; done && cd ..
python3 build.py all
```

- `manuscript/`: chapter text in Markdown (British English). Display equations use `$$ LaTeX $$ {number}`.
- `figs/`: Python scripts that draw every illustration into `figures/`.
- `style/`: print (WeasyPrint) and EPUB stylesheets.
- `book_meta.py`: title, author, part titles and introductions, and chapter order.
