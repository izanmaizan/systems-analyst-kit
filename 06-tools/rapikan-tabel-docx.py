#!/usr/bin/env python3
"""Rapikan tabel docx hasil pandoc: border, spasi tunggal, font kecil, header tebal berlatar,
lebar kolom otomatis, baris tidak terpotong antar halaman, header berulang."""
import sys
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH

d = Document(sys.argv[1])


URUTAN_TBLPR = ["tblStyle", "tblpPr", "tblOverlap", "bidiVisual", "tblStyleRowBandSize",
                "tblStyleColBandSize", "tblW", "jc", "tblCellSpacing", "tblInd",
                "tblBorders", "shd", "tblLayout", "tblCellMar", "tblLook",
                "tblCaption", "tblDescription"]
URUTAN_TCPR = ["cnfStyle", "tcW", "gridSpan", "hMerge", "vMerge", "tcBorders", "shd",
               "noWrap", "tcMar", "textDirection", "tcFitText", "vAlign", "hideMark"]


def urutkan(parent, urutan):
    def kunci(e):
        nama = e.tag.split("}")[1]
        return urutan.index(nama) if nama in urutan else len(urutan)
    anak = sorted(list(parent), key=kunci)
    for a in list(parent):
        parent.remove(a)
    for a in anak:
        parent.append(a)


def border(tbl):
    tblPr = tbl._tbl.tblPr
    for t in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(t)
    b = OxmlElement("w:tblBorders")
    for sisi in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{sisi}")
        e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "4")
        e.set(qn("w:space"), "0"); e.set(qn("w:color"), "808080")
        b.append(e)
    tblPr.append(b)
    for t in tblPr.findall(qn("w:tblLayout")):
        tblPr.remove(t)
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "autofit"); tblPr.append(lay)
    for t in tblPr.findall(qn("w:tblW")):
        tblPr.remove(t)
    w = OxmlElement("w:tblW"); w.set(qn("w:w"), "5000"); w.set(qn("w:type"), "pct"); tblPr.append(w)


def latar(cell, hex_):
    tcPr = cell._tc.get_or_add_tcPr()
    for t in tcPr.findall(qn("w:shd")):
        tcPr.remove(t)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), hex_)
    tcPr.append(shd)


def atur_lebar(tbl):
    """Lebar kolom proporsional terhadap panjang isi (min 6 %, maks 46 %)."""
    n = len(tbl.columns)
    if n == 0:
        return
    skor = [0.0] * n
    for row in tbl.rows:
        for j, cell in enumerate(row.cells[:n]):
            teks = cell.text.strip()
            # kata terpanjang menentukan lebar minimum; panjang total menentukan bobot
            kata = max((len(w) for w in teks.split()), default=1)
            skor[j] = max(skor[j], min(0.55 * len(teks), 60) + kata * 1.6 + 4)
    tot = sum(skor) or 1
    persen = [min(0.46, max(0.08, x / tot)) for x in skor]
    t2 = sum(persen)
    persen = [x / t2 for x in persen]
    tblPr = tbl._tbl.tblPr
    for g in tbl._tbl.findall(qn("w:tblGrid")):
        for gc, pr in zip(g.findall(qn("w:gridCol")), persen):
            gc.set(qn("w:w"), str(int(9000 * pr)))
    for row in tbl.rows:
        for cell, pr in zip(row.cells[:n], persen):
            tcPr = cell._tc.get_or_add_tcPr()
            for w in tcPr.findall(qn("w:tcW")):
                tcPr.remove(w)
            tw = OxmlElement("w:tcW")
            tw.set(qn("w:w"), str(int(5000 * pr))); tw.set(qn("w:type"), "pct")
            tcPr.append(tw)


def cantik(tbl):
    border(tbl)
    atur_lebar(tbl)
    for i, row in enumerate(tbl.rows):
        trPr = row._tr.get_or_add_trPr()
        for e in list(trPr):
            trPr.remove(e)
        trPr.append(OxmlElement("w:cantSplit"))
        if i == 0:
            trPr.append(OxmlElement("w:tblHeader"))
        for cell in row.cells:
            if i == 0:
                latar(cell, "D9D9D9")
            for p in cell.paragraphs:
                pf = p.paragraph_format
                pf.line_spacing, pf.space_before, pf.space_after = 1.0, Pt(1), Pt(1)
                pf.keep_together = True
                for r in p.runs:
                    r.font.size = Pt(9)
                    r.font.name = "Times New Roman"
                    if i == 0:
                        r.font.bold = True


n = 0
for t in d.tables:
    cantik(t)
    urutkan(t._tbl.tblPr, URUTAN_TBLPR)
    for tc in t._tbl.iter(qn("w:tc")):
        tcPr = tc.find(qn("w:tcPr"))
        if tcPr is not None:
            urutkan(tcPr, URUTAN_TCPR)
    n += 1

# blok kode: font mono kecil, spasi tunggal
for p in d.paragraphs:
    if p.style.name in ("Source Code", "Verbatim Char", "Preformatted Text"):
        p.paragraph_format.line_spacing = 1.0
        for r in p.runs:
            r.font.size = Pt(8)
d.save(sys.argv[1])
print("tabel dirapikan:", n)

# ── pindahkan blok daftar isi otomatis ke setelah halaman pengesahan dan beri page break ──
from docx import Document as _D
from docx.oxml import OxmlElement as _E
_d = _D(sys.argv[1])
_body = _d.element.body
_sdt = _body.find(qn("w:sdt"))
if _sdt is not None:
    # cari heading pertama setelah blok judul: "KATA PENGANTAR" bila ada; jika tidak, biarkan
    target = None
    for p in _d.paragraphs:
        if p.text.strip().upper().startswith("KATA PENGANTAR"):
            target = p._p; break
    if target is not None:
        _body.remove(_sdt)
        target.addprevious(_sdt)
        br = _E("w:p"); r = _E("w:r"); b = _E("w:br"); b.set(qn("w:type"), "page")
        r.append(b); br.append(r); target.addprevious(br)
_d.save(sys.argv[1])


