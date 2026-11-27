"""Reference document and post-processing for the 6 x 9 in black-and-white DOCX."""
import subprocess
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

BODY, HEAD = "Garamond", "Garamond"
BLACK = RGBColor(0, 0, 0)


def _font(style, name, size=None, bold=None, italic=None):
    style.font.name = name
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(a), name)
    for a in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
        if rfonts.get(qn(a)) is not None:
            del rfonts.attrib[qn(a)]
    if size:
        style.font.size = Pt(size)
    if bold is not None:
        style.font.bold = bold
    if italic is not None:
        style.font.italic = italic
    style.font.color.rgb = BLACK


def _border(pf_el, sides=("top", "left", "bottom", "right"), sz=8, val="single"):
    ppr = pf_el.get_or_add_pPr()
    pbdr = OxmlElement("w:pBdr")
    for s in sides:
        b = OxmlElement(f"w:{s}")
        b.set(qn("w:val"), val)
        b.set(qn("w:sz"), str(sz if s != "left" or len(sides) < 4 else sz))
        b.set(qn("w:space"), "6")
        b.set(qn("w:color"), "000000")
        pbdr.append(b)
    ppr.append(pbdr)


def _shade(pf_el, fill="EFEFEF"):
    ppr = pf_el.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    ppr.append(shd)


class _Styles:
    """Name lookup that tolerates pandoc's capitalised built-in style names."""
    def __init__(self, styles):
        self.styles = styles
    def __iter__(self):
        return iter(self.styles)
    def __getitem__(self, name):
        for s in self.styles:
            if s.name == name:
                return s
        raise KeyError(name)
    def add_style(self, *a):
        return self.styles.add_style(*a)


def make_reference(path):
    path = Path(path)
    subprocess.run(["pandoc", "-o", str(path), "--print-default-data-file", "reference.docx"], check=True)
    d = Document(str(path))
    st = _Styles(d.styles)
    for name in ("Normal", "Body Text", "First Paragraph", "Compact"):
        if name in [s.name for s in st]:
            s = st[name]
            _font(s, BODY, 11.5)
            s.paragraph_format.line_spacing = 1.25
            s.paragraph_format.space_after = Pt(0)
            s.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    st["Body Text"].paragraph_format.first_line_indent = Inches(0.2)
    st["Body Text"].paragraph_format.space_before = Pt(0)
    for lvl, size in ((1, 20), (2, 14), (3, 12), (4, 11.5)):
        s = st[f"Heading {lvl}"]
        _font(s, HEAD, size, bold=True, italic=(lvl == 4))
        s.paragraph_format.space_before = Pt(18 if lvl > 1 else 0)
        s.paragraph_format.space_after = Pt(8)
        s.paragraph_format.keep_with_next = True
        if lvl == 1:
            s.paragraph_format.page_break_before = True
            s.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for name in ("Title", "Subtitle", "Author", "Date", "Abstract", "Block Text", "Image Caption", "Table Caption",
                 "Captioned Figure", "TOC Heading", "Hyperlink", "Footnote Text"):
        try:
            s = st[name]
        except KeyError:
            continue
        if s.type == WD_STYLE_TYPE.CHARACTER:
            s.font.color.rgb = BLACK
            continue
        _font(s, BODY)
    _font(st["Image Caption"], "Arial", 8.5, italic=False)
    st["Image Caption"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    try:
        st["Captioned Figure"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    except KeyError:
        pass

    def para_style(name, size=10.5, italic=False, bold=False, align=None, border=None, shade=None, indent=0.0, before=8, after=8):
        try:
            s = st[name]
        except KeyError:
            s = st.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        s.base_style = st["Normal"]
        _font(s, BODY, size, bold=bold, italic=italic)
        pf = s.paragraph_format
        pf.space_before, pf.space_after = Pt(before), Pt(after)
        pf.left_indent = Inches(indent)
        pf.right_indent = Inches(indent)
        pf.first_line_indent = Inches(0)
        pf.alignment = align if align is not None else WD_ALIGN_PARAGRAPH.LEFT
        if border:
            _border(s.element, **border)
        if shade:
            _shade(s.element, shade)
        return s

    para_style("Drill", border=dict(sz=8), indent=0.1, before=4, after=4)
    para_style("Problem", border=dict(sides=("top", "bottom"), sz=14), before=4, after=4)
    para_style("Kata", shade="EFEFEF", border=dict(sides=("left",), sz=14), indent=0.1, before=4, after=4)
    para_style("Street", border=dict(sz=6, val="dashed"), indent=0.1, before=4, after=4)
    para_style("Fault", border=dict(sz=8), indent=0.1, before=4, after=4)
    para_style("Key Points", border=dict(sz=12), indent=0.1, before=4, after=4)
    para_style("Exercises", border=dict(sides=("top",), sz=12), before=4, after=4)
    para_style("Chapter Intro", 11.5, italic=True, before=0, after=6)
    para_style("Part Intro", 12, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, before=6, after=6)
    para_style("Title Block", 26, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, before=120, after=12)
    para_style("Subtitle Block", 13, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, before=6, after=60)
    para_style("Author Block", 16, align=WD_ALIGN_PARAGRAPH.CENTER, before=60, after=6)

    sec = d.sections[0]
    sec.page_width, sec.page_height = Inches(6), Inches(9)
    sec.top_margin = sec.bottom_margin = Inches(0.8)
    sec.left_margin, sec.right_margin = Inches(0.875), Inches(0.6)
    d.save(str(path))
    return path


def _field(run, instr):
    for tag, text in (("begin", None), ("instr", instr), ("separate", None), ("end", None)):
        if tag == "instr":
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = text
        else:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), tag)
        run._r.append(el)


def postprocess(path):
    d = Document(str(path))
    settings = d.settings.element
    mirror = OxmlElement("w:mirrorMargins")
    settings.append(mirror)
    evn = OxmlElement("w:evenAndOddHeaders")
    settings.append(evn)
    for sec in d.sections:
        sec.page_width, sec.page_height = Inches(6), Inches(9)
        sec.top_margin = sec.bottom_margin = Inches(0.8)
        sec.left_margin, sec.right_margin = Inches(0.875), Inches(0.6)
        sec.header_distance = sec.footer_distance = Inches(0.4)
        sec.different_first_page_header_footer = True
        for hdr, align in ((sec.header, WD_ALIGN_PARAGRAPH.RIGHT), (sec.even_page_header, WD_ALIGN_PARAGRAPH.LEFT)):
            p = hdr.paragraphs[0]
            p.alignment = align
            r = p.add_run("GOJU-RYU KARATE CLOSE-COMBAT MASTERCLASS     " if align == WD_ALIGN_PARAGRAPH.LEFT else "")
            r.font.size = Pt(7)
            r2 = p.add_run()
            r2.font.size = Pt(8.5)
            _field(r2, "PAGE")
            if align == WD_ALIGN_PARAGRAPH.RIGHT:
                r3 = p.add_run("     DR BEVERLY J. STIVERS")
                r3.font.size = Pt(7)
    # keep images inside the text block, centred
    for p in d.paragraphs:
        if p.style.name in ("Captioned Figure", "Figure") or p._p.xpath(".//w:drawing"):
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Inches(0)
    for shape in d.inline_shapes:
        if shape.width > Inches(4.5):
            ratio = Inches(4.5) / shape.width
            shape.width = Inches(4.5)
            shape.height = int(shape.height * ratio)
    d.save(str(path))
