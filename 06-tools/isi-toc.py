#!/usr/bin/env python3
"""Isi penanda [[TOC]] pada docx dengan daftar isi berisi nomor halaman (field TOC dengan hasil
tersimpan), agar langsung tampil di Word/OnlyOffice. Nomor halaman dihitung dari render PDF
sementara; di OnlyOffice klik kanan daftar isi -> Refresh bila paginasinya sedikit bergeser."""
import os, re, shutil, subprocess, sys, tempfile
from docx import Document
from docx.shared import Cm, Pt
from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

berkas = os.path.abspath(sys.argv[1])
LEBAR_TEKS = Cm(15)


def judul_heading(d):
    hasil, pertama = [], True
    for p in d.paragraphs:
        n = p.style.name
        if n in ("Heading 1", "Heading 2") and p.text.strip():
            if pertama and n == "Heading 1":      # judul sampul
                pertama = False
                continue
            lv = 1 if n == "Heading 1" else 2
            if p.text.strip().lower().startswith("lampiran "):
                lv = 2
            hasil.append((lv, p.text.strip()))
    return hasil


def tulis_toc(d, entri, halaman):
    """Ganti paragraf [[TOC]] dengan entri; entri = [(level, teks)]; halaman = {indeks: no}."""
    target = next((p for p in d.paragraphs if p.text.strip() == "[[TOC]]"), None)
    if target is None:
        return False
    daftar = []
    for i, (lv, teks) in enumerate(entri):
        np_ = OxmlElement("w:p")
        target._p.addprevious(np_)
        from docx.text.paragraph import Paragraph
        par = Paragraph(np_, target._parent)
        pf = par.paragraph_format
        pf.line_spacing, pf.space_before, pf.space_after = 1.15, Pt(0), Pt(2)
        pf.left_indent = Cm(0.8 * (lv - 1))
        pf.tab_stops.add_tab_stop(LEBAR_TEKS, WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        r = par.add_run(f"{teks}\t{halaman.get(i, '00')}")
        r.font.size = Pt(10.5 if lv == 1 else 10)
        r.bold = lv == 1
        daftar.append(par)

    def fld(par, tipe, awal=False):
        r = OxmlElement("w:r")
        f = OxmlElement("w:fldChar"); f.set(qn("w:fldCharType"), tipe)
        r.append(f)
        if awal:
            par._p.insert(1 if par._p.pPr is not None else 0, r)
        else:
            par._p.append(r)
        return r

    # begin + instruksi + separate di paragraf pertama; end di paragraf terakhir
    p1, pn = daftar[0], daftar[-1]
    sisip = 1 if p1._p.pPr is not None else 0
    rb = OxmlElement("w:r"); fb = OxmlElement("w:fldChar"); fb.set(qn("w:fldCharType"), "begin"); rb.append(fb)
    ri = OxmlElement("w:r"); it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve")
    it.text = ' TOC \\o "1-2" \\h \\z \\u '; ri.append(it)
    rs = OxmlElement("w:r"); fs = OxmlElement("w:fldChar"); fs.set(qn("w:fldCharType"), "separate"); rs.append(fs)
    for k, rr in enumerate((rb, ri, rs)):
        p1._p.insert(sisip + k, rr)
    re_ = OxmlElement("w:r"); fe = OxmlElement("w:fldChar"); fe.set(qn("w:fldCharType"), "end"); re_.append(fe)
    pn._p.append(re_)
    target._p.getparent().remove(target._p)
    return True


def halaman_heading(pdf, entri):
    teks = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
    pages = teks.split("\f")
    toc_pages = {i for i, p in enumerate(pages)
                 if len(re.findall(r"\.{4,}\s*\d+\s*$", p, re.M)) >= 5
                 or len(re.findall(r"\s{2,}\d+\s*$", p, re.M)) >= 12 and "DAFTAR ISI" in p}
    norm = lambda x: re.sub(r"\s+", " ", x).strip().lower()
    hasil, mulai = {}, 0
    for i, (lv, t) in enumerate(entri):
        kunci = norm(t)
        if kunci == "daftar isi":                 # halaman pertama yang memuat daftar isi
            if toc_pages:
                hasil[i] = min(toc_pages) + 1
                mulai = max(mulai, min(toc_pages))
            continue
        # utamakan baris yang memang judul (bukan kalimat paragraf yang diawali teks judul,
        # mis. "BAB II Tinjauan Pustaka memuat ..." di Sistematika Penulisan)
        awal = kunci[:40]
        judul_baris = lambda p: any(norm(b).startswith(awal) and len(norm(b)) <= len(kunci) + 4
                                    for b in p.splitlines())
        for cocok in (judul_baris, lambda p: kunci in norm(p)):
            pg = next((pg for pg in range(mulai, len(pages))
                       if pg not in toc_pages and cocok(pages[pg])), None)
            if pg is not None:
                hasil[i] = pg + 1
                mulai = pg
                break
    return hasil


def render(docx_path, tmp):
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp, docx_path],
                   capture_output=True)
    return os.path.join(tmp, os.path.splitext(os.path.basename(docx_path))[0] + ".pdf")


asal = tempfile.mkdtemp()
shutil.copy(berkas, os.path.join(asal, "asal.docx"))
d0 = Document(os.path.join(asal, "asal.docx"))
entri = judul_heading(d0)
halaman = {}
for putaran in range(3):
    d = Document(os.path.join(asal, "asal.docx"))
    if not tulis_toc(d, entri, halaman):
        print("penanda [[TOC]] tidak ada; lewati"); sys.exit(0)
    sementara = os.path.join(asal, f"p{putaran}.docx")
    d.save(sementara)
    baru = halaman_heading(render(sementara, asal), entri)
    if baru == halaman:
        break
    halaman = baru
d = Document(os.path.join(asal, "asal.docx"))
tulis_toc(d, entri, halaman)
d.save(berkas)
print(f"daftar isi: {len(entri)} entri, {len(halaman)} bernomor halaman")
shutil.rmtree(asal, ignore_errors=True)
