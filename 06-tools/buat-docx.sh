#!/bin/sh
# Susun seluruh .md dalam satu folder menjadi satu docx bergaya skripsi.
# Pemakaian: buat-docx.sh <folder_dokumen> <keluaran.docx>
set -e
DIR="${1:?folder wajib diisi}"
OUT="${2:?keluaran wajib diisi}"
TOOLS="$(cd "$(dirname "$0")" && pwd)"
REF="$TOOLS/reference.docx"
[ -f "$REF" ] || python3 "$TOOLS/buat-reference-docx.py" "$REF" >/dev/null

cd "$DIR"
LIST=$(ls -1 [0-9]*.md 2>/dev/null | sort)
[ -n "$LIST" ] || { echo "tidak ada berkas .md di $DIR"; exit 1; }

# 1) pandoc: gambar tanpa lebar tetap, caption tidak ganda
pandoc $LIST --from=markdown-implicit_figures --reference-doc="$REF" \
  --resource-path="$DIR" --metadata title="" -o "$OUT"

# 2) pasca-proses: skala gambar muat ke lebar teks 14 cm dan tinggi maks 19 cm
python3 "$TOOLS/skala-gambar-docx.py" "$OUT"
python3 "$TOOLS/rapikan-tabel-docx.py" "$OUT"
python3 "$TOOLS/isi-toc.py" "$OUT"
echo "docx: $DIR/$OUT"
