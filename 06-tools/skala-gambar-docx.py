#!/usr/bin/env python3
"""Skala semua gambar inline docx agar muat di area teks (lebar maks 14 cm, tinggi maks 19 cm),
mempertahankan rasio. Dipakai setelah pandoc."""
import sys
from docx import Document
from docx.shared import Cm
from docx.oxml.ns import qn

MAKS_W, MAKS_H = Cm(15.0), Cm(20.5)
d = Document(sys.argv[1])
n = 0
for shape in d.inline_shapes:
    w, h = shape.width, shape.height
    if not w or not h:
        continue
    faktor = min(MAKS_W / w, MAKS_H / h, 1.0 if w <= MAKS_W and h <= MAKS_H else 9)
    faktor = min(MAKS_W / w, MAKS_H / h)
    shape.width, shape.height = int(w * faktor), int(h * faktor)
    n += 1
from docx.enum.text import WD_ALIGN_PARAGRAPH
paras = d.paragraphs
for i, p in enumerate(paras):
    if p._p.xpath(".//w:drawing"):
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.space_after = 0
        if i + 1 < len(paras) and paras[i + 1].text.strip().startswith("Gambar "):
            c = paras[i + 1]
            c.alignment = WD_ALIGN_PARAGRAPH.CENTER
            c.paragraph_format.space_before = 0
# judul sampul tidak dipisah halaman agar tetap bersama kop surat
for p_ in d.paragraphs:
    if p_.style.name == "Heading 1":
        p_.paragraph_format.page_break_before = False
        break
d.save(sys.argv[1])
print(f"gambar diskala: {n}")
