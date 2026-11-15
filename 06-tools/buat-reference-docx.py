#!/usr/bin/env python3
"""Buat reference.docx bergaya skripsi (Times New Roman) untuk pandoc."""
import sys
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

out = sys.argv[1] if len(sys.argv) > 1 else "reference.docx"
d = Document()

# Ukuran kertas A4 + margin skripsi (kiri 4 cm, kanan 3 cm, atas-bawah 3 cm)
for s in d.sections:
    s.page_width, s.page_height = Cm(21), Cm(29.7)
    s.left_margin, s.right_margin = Cm(4), Cm(3)
    s.top_margin, s.bottom_margin = Cm(3), Cm(3)

st = d.styles["Normal"]
st.font.name = "Times New Roman"
st.font.size = Pt(12)
st.paragraph_format.line_spacing = 1.5
st.paragraph_format.space_after = Pt(6)

for name, size, align in [
    ("Heading 1", 14, WD_ALIGN_PARAGRAPH.CENTER),
    ("Heading 2", 12, WD_ALIGN_PARAGRAPH.LEFT),
    ("Heading 3", 12, WD_ALIGN_PARAGRAPH.LEFT),
]:
    h = d.styles[name]
    h.font.name = "Times New Roman"
    h.font.size = Pt(size)
    h.font.bold = True
    h.font.color.rgb = None
    try:
        h.font.color.theme_color = None
    except Exception:
        pass
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(6)
    h.paragraph_format.line_spacing = 1.5
    h.paragraph_format.alignment = align

for name in ("Title", "Author", "Date", "Caption", "Source Code"):
    try:
        s = d.styles[name]
        s.font.name = "Times New Roman"
        if name == "Caption":
            s.font.size = Pt(10)
            s.font.italic = False
    except KeyError:
        pass

# Gaya tabel rapi
try:
    t = d.styles["Table Grid"]
    t.font.name = "Times New Roman"
    t.font.size = Pt(10)
except KeyError:
    pass

d.save(out)
print("reference docx:", out)
