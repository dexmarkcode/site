#!/usr/bin/env python3
"""Assemble the manuscript and build PDF and EPUB.

usage: python3 tools/build.py [--chapters 1,2] [--no-pdf] [--no-epub]
"""
import argparse
import importlib
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'gen'))
os.chdir(ROOT)

from core import LEVELS  # noqa: E402

PARTS = {
    1: ('part1', [1, 2, 3]),
    2: ('part2', [4, 5, 6]),
    3: ('part3', [7, 8, 9]),
    4: ('part4', [10, 11, 12]),
}


def read(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


def fig_md(fig, width='78%'):
    path, cap = fig
    return f'\n![{cap}]({path}){{width={width}}}\n'


FRAC = re.compile(r'(?<!\^\{)(?<!\^\{-)\\frac(?=\{)')


INLINE = re.compile(r'(?<![$\\])\$(?!\$)([^$]+?)\$(?!\$)')


def _promote(m):
    body = m.group(1)
    if len(body) > 55 and '\\frac' in body and '\\begin' not in body:
        return '$$' + body + '$$'
    return m.group(0)


def _dfrac_outer(txt):
    """Use \\dfrac only for fractions that are not nested in another fraction or an exponent."""
    out, i, depth = [], 0, 0
    fr = []          # stack of [arg_depth, groups_left, opened]
    sup = []         # brace depths that belong to superscripts
    n = len(txt)
    while i < n:
        if txt.startswith('\\frac', i) and not txt.startswith('\\fracc', i):
            nested = any(f[2] for f in fr) or bool(sup)
            out.append('\\frac' if nested else '\\dfrac')
            fr.append([depth, 2, False])
            i += 5
            continue
        if txt.startswith('\\dfrac', i):
            nested = any(f[2] for f in fr) or bool(sup)
            out.append('\\frac' if nested else '\\dfrac')
            fr.append([depth, 2, False])
            i += 6
            continue
        c = txt[i]
        if c == '^' and i + 1 < n and txt[i + 1] == '{':
            sup.append(depth)
        if c == '{':
            for f in fr:
                if f[0] == depth and f[1] > 0 and not f[2]:
                    f[2] = True
            depth += 1
        elif c == '}':
            depth -= 1
            if sup and sup[-1] == depth:
                sup.pop()
            for f in fr:
                if f[2] and f[0] == depth:
                    f[2] = False
                    f[1] -= 1
            fr = [f for f in fr if f[1] > 0]
        out.append(c)
        i += 1
    return ''.join(out)


def big(txt):
    """Display-size outer fractions in maths; long inline formulas become displays."""
    txt = INLINE.sub(_promote, txt)
    return _dfrac_outer(txt)


def problem_md(ch, i, p):
    out = [f'::: {{.problem num="{ch}.{i}" level="{LEVELS[p.level]}" topic="{p.topic}"}}', p.statement]
    if p.fig:
        out.append(fig_md(p.fig, '70%'))
    out.append(':::\n')
    return '\n'.join(out)


def solution_md(ch, i, p):
    out = [f':::: {{.solution num="{ch}.{i}" topic="{p.topic}"}}', '::: restate', p.statement, ':::', '']
    for k, (head, body) in enumerate(p.steps, 1):
        out.append(f'[Step {k}: {head}.]{{.step}} {body}\n')
    if p.sol_fig:
        out.append(fig_md(p.sol_fig, '70%'))
    out += ['::: answer', p.answer, ':::', '::::\n']
    return '\n'.join(out)


def chapter_md(ch):
    mod = importlib.import_module(f'ch{ch:02d}')
    probs = mod.generate()
    text = read(f'text/ch{ch:02d}.md').rstrip() + '\n\n'
    intro = getattr(mod, 'PROBLEM_INTRO', '')
    text += f'### Practice Problems\n\n{intro}\n\n'
    for lv in 'ABC':
        group = [(i, p) for i, p in enumerate(probs, 1) if p.level == lv]
        if not group:
            continue
        text += f'#### {LEVELS[lv]} problems {{.unnumbered}}\n\n'
        text += {'A': 'These check that the basic definitions are secure. Aim to finish each one in a few minutes.\n\n',
                 'B': 'The bread and butter of examinations. Each needs a clear method rather than a flash of insight.\n\n',
                 'C': 'Longer problems that combine several ideas. Take your time, sketch freely and check your answer by a second route where you can.\n\n'}[lv]
        for i, p in group:
            text += problem_md(ch, i, p) + '\n'
    text += '### Step-by-Step Solutions\n\n'
    text += ('Try each problem properly before reading its solution. When you do read one, read actively: '
             'cover the next step and ask yourself what you would do, then check.\n\n')
    for i, p in enumerate(probs, 1):
        text += solution_md(ch, i, p) + '\n'
    return big(text), probs


def assemble(chapters):
    body = []
    allp = {}
    for pn, (pfile, chs) in PARTS.items():
        sel = [c for c in chs if c in chapters]
        if not sel:
            continue
        body.append(read(f'text/{pfile}.md').rstrip() + '\n')
        for c in sel:
            t, probs = chapter_md(c)
            allp[c] = probs
            body.append(t)
    return '\n\n'.join(body), allp


def pandoc(src, dst, fmt, extra=()):
    cmd = ['pandoc', src, '-f', 'markdown+fenced_divs+bracketed_spans+tex_math_dollars+raw_attribute',
           '-t', fmt, '--lua-filter', 'tools/book.lua', '-o', dst] + list(extra)
    subprocess.run(cmd, check=True)


def build_pdf():
    for name in ('front', 'body', 'back'):
        pandoc(f'build/{name}.md', f'build/{name}.tex', 'latex', ['--top-level-division=part'])
    main = read('tools/main.tex')
    for name in ('front-pages', 'front', 'body', 'back'):
        main = main.replace('\\input{' + name + '.tex}', '\\input{build/' + name + '.tex}')
    shutil.copy('tools/front-pages.tex', 'build/front-pages.tex')
    with open('build/main.tex', 'w') as f:
        f.write(main)
    for run in range(2):
        r = subprocess.run(['xelatex', '-interaction=nonstopmode', '-halt-on-error', '-output-directory=build', 'build/main.tex'],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout[-4000:])
            raise SystemExit('xelatex failed')
    shutil.copy('build/main.pdf', 'output/Signals-and-Systems-Workbook.pdf')
    out = subprocess.run(['pdfinfo', 'output/Signals-and-Systems-Workbook.pdf'], capture_output=True, text=True).stdout
    print([l for l in out.splitlines() if l.startswith('Pages')])


def build_epub(front, body, back):
    def epubify(txt):
        return re.sub(r'```\{=latex\}.*?```', '', txt, flags=re.S)
    counter = iter(range(1, 100))
    body = re.sub(r'^## (?!.*unnumbered)(.+)$', lambda m: f'## Chapter {next(counter)}: {m.group(1)}', body, flags=re.M)
    letters = iter('ABCDEFGH')
    back = re.sub(r'^## (?!.*unnumbered)(.+)$', lambda m: f'## Appendix {next(letters)}: {m.group(1)}', back, flags=re.M)
    with open('build/epub.md', 'w') as f:
        f.write(epubify(front) + '\n\n' + body + '\n\n' + epubify(back))
    subprocess.run(['pandoc', 'build/epub.md', '-f', 'markdown+fenced_divs+bracketed_spans+tex_math_dollars+raw_attribute',
                    '-t', 'epub3', '--lua-filter', 'tools/book.lua', '--mathml', '--split-level=2',
                    '--toc', '--toc-depth=2', '--css', 'tools/epub.css', '--epub-cover-image=output/cover.jpg',
                    '--metadata-file', 'tools/metadata.yaml', '--default-image-extension=png',
                    '-o', 'output/Signals-and-Systems-Workbook.epub'], check=True)
    print('epub ok', os.path.getsize('output/Signals-and-Systems-Workbook.epub') // 1024, 'KB')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--chapters', default='1,2,3,4,5,6,7,8,9,10,11,12')
    ap.add_argument('--no-pdf', action='store_true')
    ap.add_argument('--no-epub', action='store_true')
    a = ap.parse_args()
    chapters = [int(c) for c in a.chapters.split(',')]
    os.makedirs('build', exist_ok=True)
    body, allp = assemble(chapters)
    front = read('text/front.md')
    back = read('text/back.md')
    for name, txt in (('front', front), ('body', body), ('back', back)):
        with open(f'build/{name}.md', 'w') as f:
            f.write(txt)
    words = len(re.findall(r'[A-Za-z]{2,}', front + body + back))
    print('chapters', chapters, 'problems', sum(len(v) for v in allp.values()), 'approx words', words)
    if not a.no_pdf:
        build_pdf()
    if not a.no_epub:
        build_epub(front, body, back)


if __name__ == '__main__':
    main()
