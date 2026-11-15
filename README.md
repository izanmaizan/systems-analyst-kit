# Systems Analyst Kit

Kerangka kerja dokumentasi Systems Analyst untuk proyek aplikasi pemerintahan dan rumah sakit. Berisi contoh nyata satu halaman per jenis dokumen, tangkapan halaman dokumen lengkap, checklist isi, standar format, dan sumber diagram.

Semua isi di repo ini sudah dianonimkan. Nama instansi, kota, provinsi, domain, dan alamat IP diganti dengan penanda contoh. Tidak ada data pasien, pegawai, kredensial, atau nilai anggaran.

## Isi repo

| Folder | Isi |
|---|---|
| `01-template/` | Contoh docx satu halaman untuk tiap jenis dokumen, sudah bergaya resmi (A4, Times New Roman 11, hitam-putih) |
| `02-contoh-halaman/` | Tangkapan halaman 1–3 dari dokumen versi lengkap, memperlihatkan hasil akhir tata letak |
| `03-checklist/` | Daftar bagian wajib per dokumen, dipakai saat menyusun dokumen baru |
| `04-format/` | Standar format penulisan dan `reference.docx` untuk pandoc |
| `05-diagram/` | 13 sumber diagram PlantUML (use case, class, activity, sequence, state, component, deployment, ERD, DFD level 0/1, flowchart) beserta hasil render PNG |
| `06-tools/` | Skrip pembentuk docx, render diagram, penyelarasan tabel dan gambar |
| `07-analisis-kapasitas/` | Kerangka dokumen analisis kapasitas server: susunan bab, metrik, perintah pengukuran |

## Paket dokumen

Pola nomor yang dipakai di lingkungan rumah sakit daerah:

| Nomor | Dokumen | Singkatan |
|---|---|---|
| 1 | Kerangka Acuan Kerja / Terms of Reference | KAK/TOR |
| 2 | Dokumen Desain Sistem | SDD |
| 3 | Dokumen Hasil Pengujian dan User Acceptance Test | UAT |
| 4 | Berita Acara Sosialisasi, Pelatihan, dan Serah Terima | BA |
| 5 | Panduan Pengguna | — |

## Alur pemakaian

1. Buka `01-template/` sesuai jenis dokumen. Salin isi dan strukturnya, jangan salin substansi proyek contoh.
2. Cek `03-checklist/` untuk memastikan tidak ada bagian yang tertinggal.
3. Ikuti `04-format/standar-format.md` agar tata letak seragam.
4. Untuk dokumen panjang, tulis markdown lalu gabungkan dengan `06-tools/buat-docx.sh`.
5. Untuk diagram, sunting `05-diagram/*.puml`, render dengan `06-tools/render.sh`.
6. Bagian UAT, tanda tangan, nama, dan NIP selalu dikosongkan untuk diisi unit pengguna.

## Aturan yang tidak boleh dilanggar

1. Hasil pengujian harus berasal dari pengujian yang benar-benar dijalankan. Yang tidak diuji ditulis "tidak dapat diuji" beserta alasannya.
2. Bagian UAT hanya diformat. Hasil, tanggal, nama, dan NIP dikosongkan.
3. Nama dan NIP penanda tangan tidak dikarang. Cukup jabatannya, sisanya titik-titik.
4. Kredensial, token, dan kunci API tidak boleh muncul di dokumen maupun tangkapan layar.
5. Data pasien dan pegawai tidak boleh masuk dokumen. Gunakan data agregat atau data contoh.
6. Nilai anggaran dan nomor dokumen dikosongkan.

## Membangun ulang

```bash
bash 06-tools/buat-docx.sh <folder-markdown> <keluaran.docx>
bash 06-tools/render.sh 05-diagram
```

Keduanya butuh `pandoc`, `python3`, dan `plantuml`. Untuk diagram `.dot` perlu `graphviz`.

## Lisensi

Contoh dokumen dilepas untuk keperluan pembelajaran penyusunan dokumen. Struktur dan tata letak boleh dipakai ulang. Substansi proyek contoh bukan acuan resmi instansi mana pun.
