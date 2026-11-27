# Goju-Ryu Karate Kyohan, Volume Two — manuscript and build

*Illustrated Textbook With 800 Line Drawings for Kaishu Kata, Tension Drills, and Classical Applications Beyond the First Textbook*, by Dr Beverly J. Stivers.

## Finished files (`output/`)

- `…Stivers.pdf`: print interior, 6 × 9 in trim, single column, black and white, 337 pages
- `…Stivers.epub`: EPUB 3 with embedded fonts and cover
- `…Stivers.docx`: Word manuscript, 6 × 9 in page size (open in Word and update the table of contents field)

## Structure

Six parts of three chapters each (18 chapters), preface, How to Use This Book, Appendix A (kata reference cards), Appendix B (training plans), Appendix C (troubleshooting index), glossary, further reading and About the Author. 857 numbered line drawings across 116 figure plates.

## Rebuilding

```
pip install weasyprint matplotlib shapely ebooklib python-docx
cd figs && for f in ch*.py extras.py cover.py; do python3 $f; done && cd ..
python3 build.py all
```

- `manuscript/`: chapter text in Markdown (British English)
- `figs/goju.py`: the line-drawing engine; `figs/chNN.py` draw each chapter's plates into `figures/`
- `style/`: print (WeasyPrint) and EPUB stylesheets
- `book_meta.py`: title, author, part titles and chapter order
