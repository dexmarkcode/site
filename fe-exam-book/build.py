#!/usr/bin/env python3
"""Assemble the manuscript and export PDF (XeLaTeX) and EPUB 3."""
import glob
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(ROOT, "build")
QD = os.path.join(B, "q")
TITLE = "Electrical Engineering FE Exam Prep 2026-2027"
SUBTITLE = "The Complete Study Guide - 800 Practice Questions, Formulas, and Mock Exams to Pass First Time"
AUTHOR = "Marcus J. Thornton, Ph.D."
OUTNAME = "Electrical-Engineering-FE-Exam-Prep-2026-2027_Marcus-J-Thornton"


def assemble():
    parts = []
    for f in sorted(glob.glob(os.path.join(ROOT, "src", "*.md"))):
        parts.append(open(f, encoding="utf-8").read())
    text = "\n\n".join(parts)

    def sub(m):
        kind, name = m.group(1), m.group(2)
        suffix = {"QUESTIONS": "_q", "ANSWERS": "_a", "KEY": "_key", "SHEET": "_sheet"}[kind]
        return open(os.path.join(QD, name + suffix + ".md"), encoding="utf-8").read()

    text = re.sub(r"\{\{(QUESTIONS|ANSWERS|KEY|SHEET):(\w+)\}\}", sub, text)
    out = os.path.join(B, "book.md")
    open(out, "w", encoding="utf-8").write(text)
    words = len(text.split())
    print(f"assembled book.md: ~{words:,} words")
    return out


COMMON = ["--from", "markdown+fancy_lists+fenced_divs+bracketed_spans+implicit_figures", "--lua-filter", "filters/book.lua",
          "--top-level-division=chapter", "--resource-path", ".:build"]


def pdf(md):
    tex = os.path.join(B, OUTNAME + ".tex")
    cmd = ["pandoc", md, "-s", "-o", tex, *COMMON, "--toc", "--toc-depth=1",
           "-V", "documentclass=book", "-V", "classoption=openright", "-V", "fontsize=11pt",
           "-V", "geometry:paperwidth=7in", "-V", "geometry:paperheight=10in", "-V", "geometry:inner=0.92in",
           "-V", "geometry:outer=0.78in", "-V", "geometry:top=0.9in", "-V", "geometry:bottom=0.95in",
           "-V", "geometry:headsep=0.3in", "-V", "geometry:footskip=0.45in",
           "-V", "mainfont=TeX Gyre Pagella", "-V", "mathfont=TeX Gyre Pagella Math", "-V", "lang=en-GB",
           "-V", "linestretch=1.1", "-V", "colorlinks=true", "-V", "linkcolor=black", "-V", "urlcolor=black", "-V", "toccolor=black",
           "-H", "tex/preamble.tex", "-B", "tex/titlepages.tex",
           "-M", f"pagetitle={TITLE}"]
    subprocess.run(cmd, check=True, cwd=ROOT)
    for i in range(3):
        r = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", "-output-directory", B, tex],
                           cwd=ROOT, capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout[-4000:])
            sys.exit("xelatex failed")
    print("PDF ok")


def epub(md):
    fonts = [f"--epub-embed-font={p}" for p in glob.glob("/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyrepagella-*.otf")]
    cmd = ["pandoc", md, "-o", os.path.join(B, OUTNAME + ".epub"), *COMMON, "--to", "epub3", "--toc", "--toc-depth=1",
           "--split-level=1", "--css", "epub/epub.css", "--epub-cover-image", "figures/cover.png", "--mathml", *fonts,
           "-M", f"title={TITLE}", "-M", f"subtitle={SUBTITLE}", "-M", f"author={AUTHOR}", "-M", "lang=en-GB",
           "-M", "rights=Copyright © 2026 Marcus J. Thornton, Ph.D. All rights reserved.",
           "-M", "publisher=Marcus J. Thornton", "-M", "date=2026",
           "-M", "description=A complete, problem-solving study guide for the FE Electrical and Computer exam, with 800 worked practice questions, two full mock exams and every formula you need."]
    subprocess.run(cmd, check=True, cwd=ROOT)
    print("EPUB ok")


if __name__ == "__main__":
    md = assemble()
    which = sys.argv[1:] or ["pdf", "epub"]
    if "pdf" in which:
        pdf(md)
    if "epub" in which:
        epub(md)
