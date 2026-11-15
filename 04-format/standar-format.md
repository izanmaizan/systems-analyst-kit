# Standar Format Dokumen

## Halaman
- Ukuran A4 (21 x 29,7 cm), orientasi tegak.
- Margin: atas 2,2 cm, bawah 2,2 cm, kiri 2,5 cm, kanan 2,2 cm.
- Hitam-putih seluruhnya. Tidak ada warna selain abu muda pada kepala tabel.

## Teks
- Times New Roman 11 pt.
- Spasi baris 1,15, jarak antarparagraf 6 pt.
- Rata kanan-kiri (justify) untuk badan teks.
- Judul bab: tebal, 14 pt, rata tengah, `keep_with_next`.
- Subjudul: tebal, 11–12 pt, rata kiri.

## Tabel
- Kepala tabel abu muda `#D9D9D9` dengan teks hitam tebal.
- `w:tblLayout=fixed` dengan `w:gridCol` terisi agar lebar kolom stabil.
- Baris kepala diulang di halaman berikutnya (`w:tblHeader`).
- Baris tidak terpotong antar halaman (`w:cantSplit`).
- Nomor tabel dan judul di atas tabel, rata tengah.

## Gambar
- Gambar tidak terpisah dari keterangannya.
- Keterangan di bawah gambar, rata tengah, miring: `Gambar 4.1 — Judul`.
- Lebar maksimum mengikuti lebar teks (14 cm), tinggi maksimum 19 cm.
- Tangkapan layar wajib disensor jika memuat nama, NIP, nomor rekam medis, atau sandi.

## Penomoran
- Angka Arab bertingkat: `1.`, `1.1.`, `1.1.1.`
- Nomor halaman di bawah tengah, kecuali halaman judul.
- Nomor dokumen, tanggal, nama, dan NIP ditulis titik-titik untuk diisi manual.

## Blok tanda tangan
- Tidak terpisah dari judulnya (`keep_with_next`).
- Tiga kolom sejajar untuk berita acara: Yang Menyerahkan, Yang Menerima, Mengetahui.
- Jabatan terisi, nama dan NIP titik-titik.

## Bagian UAT
- Hanya kerangka. Baris hasil, tanggal, nama penguji, dan NIP dikosongkan.

## Berkas pendukung
- `reference.docx` dipakai pandoc sebagai acuan gaya.
- Skrip `06-tools/buat-docx.sh` menggabungkan markdown menjadi docx, menyelaraskan tabel, dan menyesuaikan ukuran gambar.
