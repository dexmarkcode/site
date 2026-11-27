"""Create the Word reference document (styles) and post-process the pandoc DOCX:
6 x 9 in page, mirrored KDP margins, Garamond type, black-and-white boxes, page numbers."""
import subprocess
from pathlib import Path

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

SERIF = "Garamond"
SANS = "Gill Sans MT"
BLACK = RGBColor(0, 0, 0)


def _font(style, name=SERIF, size=11, bold=None, italic=None, caps=None, small_caps=None):
    f = style.font
    f.name, f.size, f.color.rgb = name, Pt(size), BLACK
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts"); rpr.append(rfonts)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(a), name)
    for k in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
        if rfonts.get(qn(k)) is not None:
            del rfonts.attrib[qn(k)]
    if bold is not None: f.bold = bold
    if italic is not None: f.italic = italic
    if caps is not None: f.all_caps = caps
    if small_caps is not None: f.small_caps = small_caps


def _para(style, align=None, before=0, after=0, line=1.15, indent=None, keep=False, page_break=False, left=None, right=None):
    pf = style.paragraph_format
    if align is not None: pf.alignment = align
    pf.space_before, pf.space_after, pf.line_spacing = Pt(before), Pt(after), line
    if indent is not None: pf.first_line_indent = Inches(indent)
    if left is not None: pf.left_indent = Inches(left)
    if right is not None: pf.right_indent = Inches(right)
    pf.keep_with_next = keep
    pf.page_break_before = page_break
    pf.widow_control = True


def _border(style, sides=("top", "bottom", "left", "right"), sz=6, val="single", shade=None, space=6):
    ppr = style.element.get_or_add_pPr()
    old = ppr.find(qn("w:pBdr"))
    if old is not None: ppr.remove(old)
    bdr = OxmlElement("w:pBdr")
    for s in ("top", "left", "bottom", "right"):
        if s in sides:
            e = OxmlElement(f"w:{s}")
            e.set(qn("w:val"), val); e.set(qn("w:sz"), str(sz if not isinstance(sz, dict) else sz.get(s, 6)))
            e.set(qn("w:space"), str(space)); e.set(qn("w:color"), "000000")
            bdr.append(e)
    ppr.append(bdr)
    if shade:
        shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), shade)
        ppr.append(shd)


def _get(doc, name, kind=WD_STYLE_TYPE.PARAGRAPH, base="Normal"):
    try:
        return doc.styles[name]
    except KeyError:
        s = doc.styles.add_style(name, kind)
        if kind == WD_STYLE_TYPE.PARAGRAPH:
            s.base_style = doc.styles[base]
        return s


def build(path):
    path = Path(path)
    default = path.with_name("pandoc-default.docx")
    with open(default, "wb") as fh:
        subprocess.run(["pandoc", "--print-default-data-file", "reference.docx"], stdout=fh, check=True)
    doc = Document(default)
    J, C, L = WD_ALIGN_PARAGRAPH.JUSTIFY, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT

    n = _get(doc, "Normal"); _font(n, size=11); _para(n, line=1.2)
    for nm, ind in (("Body Text", 0.25), ("First Paragraph", 0), ("Compact", 0)):
        s = _get(doc, nm); _font(s, size=11); _para(s, align=J, line=1.25, indent=ind, after=0)
    h1 = _get(doc, "Heading 1"); _font(h1, size=22, bold=False, caps=True); _para(h1, align=C, before=150, after=24, page_break=True, keep=True)
    h2 = _get(doc, "Heading 2"); _font(h2, size=19, bold=True); _para(h2, align=C, before=70, after=20, page_break=True, keep=True)
    h3 = _get(doc, "Heading 3"); _font(h3, size=13, bold=True, small_caps=True); _para(h3, align=L, before=18, after=6, keep=True)
    h4 = _get(doc, "Heading 4"); _font(h4, size=11.5, bold=True, italic=True); _para(h4, align=L, before=12, after=4, keep=True)
    h5 = _get(doc, "Heading 5"); _font(h5, name=SANS, size=9, bold=True, caps=True); _para(h5, align=L, before=10, after=3, keep=True)
    for nm in ("Title", "Subtitle", "Author", "Date", "Abstract"):
        s = _get(doc, nm); _font(s, size=12)
    t = _get(doc, "Title"); _font(t, size=26, bold=True, caps=True); _para(t, align=C, before=40, after=12)
    st = _get(doc, "Subtitle"); _font(st, size=13, italic=True); _para(st, align=C, after=12)
    for nm in ("Image Caption", "Caption", "Table Caption"):
        s = _get(doc, nm); _font(s, name=SANS, size=8.5, italic=False); _para(s, align=L, before=4, after=12, line=1.1)
    cap = _get(doc, "Captioned Figure"); _para(cap, align=C, before=8, after=0, keep=True)
    fig = _get(doc, "Figure"); _para(fig, align=C, before=8, after=0, keep=True)
    toc = _get(doc, "TOC Heading"); _font(toc, size=19, caps=True); _para(toc, align=C, before=60, after=20)
    bt = _get(doc, "Block Text"); _font(bt, size=11, italic=True); _para(bt, left=0.35, right=0.35, before=6, after=6)

    boxes = {
        "Drill Box": dict(sides=("top", "bottom", "left", "right"), sz={"top": 24, "left": 6, "right": 6, "bottom": 6}),
        "Fault Box": dict(sides=("left",), sz=24, shade="EFEFEF"),
        "Note Box": dict(sides=("top", "bottom"), sz=6),
        "Test Box": dict(sides=("top", "bottom", "left", "right"), sz=6, val="dashed"),
        "Summary Box": dict(sides=("top", "bottom", "left", "right"), sz=18, val="double"),
        "Practice Box": dict(sides=("top",), sz=12),
    }
    for nm, kw in boxes.items():
        s = _get(doc, nm); _font(s, size=10); _para(s, align=L, before=0, after=4, line=1.2, left=0.12, right=0.12)
        _border(s, **kw)
    ci = _get(doc, "Chapter Intro"); _font(ci, size=11, italic=True); _para(ci, align=C, after=14, left=0.2, right=0.2)
    pi = _get(doc, "Part Intro"); _font(pi, size=11, italic=True); _para(pi, align=J, after=8, left=0.2, right=0.2)
    b1 = _get(doc, "Book Title"); _font(b1, size=28, bold=True, caps=True); _para(b1, align=C, before=60, after=14)
    b2 = _get(doc, "Book Subtitle"); _font(b2, size=13, italic=True); _para(b2, align=C, after=18)
    b3 = _get(doc, "Book Author"); _font(b3, size=14, bold=True, caps=True); _para(b3, align=C, before=24)
    cp = _get(doc, "Copyright"); _font(cp, size=8.5); _para(cp, align=L, after=5)
    de = _get(doc, "Dedication"); _font(de, size=12, italic=True); _para(de, align=C, before=160)
    for nm in ("Hyperlink",):
        try:
            hl = doc.styles[nm]; hl.font.color.rgb = BLACK; hl.font.underline = False
        except KeyError:
            pass
    doc.save(path)
    return path


def _page_field(par):
    run = par.add_run()
    for tag, txt in (("begin", None), (None, "PAGE"), ("end", None)):
        if tag:
            e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), tag); run._r.append(e)
        else:
            it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = txt; run._r.append(it)
    run.font.name, run.font.size = SERIF, Pt(9)


def postprocess(path):
    doc = Document(path)
    for sec in doc.sections:
        sec.page_width, sec.page_height = Inches(6), Inches(9)
        sec.top_margin, sec.bottom_margin = Inches(0.8), Inches(0.8)
        sec.left_margin, sec.right_margin = Inches(0.85), Inches(0.6)   # inside / outside with mirror margins
        sec.gutter = Inches(0)
        sec.header_distance, sec.footer_distance = Inches(0.4), Inches(0.4)
        fp = sec.footer.paragraphs[0] if sec.footer.paragraphs else sec.footer.add_paragraph()
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _page_field(fp)
    settings = doc.settings.element
    if settings.find(qn("w:mirrorMargins")) is None:
        settings.insert(0, OxmlElement("w:mirrorMargins"))
    # keep pictures inside the text block
    from docx.shared import Emu
    maxw = Inches(4.5)
    for shape in doc.inline_shapes:
        if shape.width > maxw:
            ratio = maxw / shape.width
            shape.width, shape.height = Emu(int(maxw)), Emu(int(shape.height * ratio))
    doc.save(path)
