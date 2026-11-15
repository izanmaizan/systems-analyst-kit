# Checklist Dokumen Desain Sistem (SDD)

## Pendahuluan
- [ ] Maksud dan tujuan dokumen
- [ ] Ruang lingkup sistem (termasuk batas sistem)
- [ ] Prinsip desain
- [ ] Daftar istilah

## Arsitektur
- [ ] Arsitektur berlapis: presentasi, aplikasi, data, integrasi
- [ ] Statistik kode (jumlah baris, berkas, modul)
- [ ] Struktur modul dan berkas program
- [ ] Lingkungan penerapan dan alur CI/CD
- [ ] Strategi perenderan dan cache

## Desain basis data
- [ ] Daftar tabel dan fungsi
- [ ] Kolom per tabel: nama, tipe, kunci, wajib, keterangan
- [ ] Relasi antartabel dan kardinalitas
- [ ] Indeks dan aturan hapus data

## Integrasi eksternal
- [ ] Daftar sistem eksternal
- [ ] Protokol, format data, autentikasi
- [ ] Penanganan kegagalan dan percobaan ulang

## Pemodelan UML
- [ ] Use case diagram
- [ ] Class diagram
- [ ] Minimal 3 activity diagram untuk alur penting
- [ ] Sequence diagram untuk alur utama
- [ ] State diagram untuk objek berstatus

## Antarmuka dan keamanan
- [ ] Identitas visual
- [ ] Rancangan tiap halaman utama
- [ ] Matriks hak akses per peran
- [ ] Rancangan keamanan: autentikasi, otorisasi, validasi masukan, perlindungan data

## Penutup
- [ ] Catatan teknis untuk pengembangan lanjutan
- [ ] Lembar pengesahan
