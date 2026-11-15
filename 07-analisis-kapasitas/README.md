# Kerangka Analisis Kapasitas Server

Susunan bab untuk dokumen analisis kapasitas dan penggunaan sumber daya. Isi angka diambil dari pengukuran nyata, bukan perkiraan.

## Susunan dokumen

| Bab | Isi |
|---|---|
| 1 | Pendahuluan: latar belakang, ruang lingkup, tujuan, pemisahan tugas |
| 2 | Metode dan sumber data: perintah pengukuran, waktu pengambilan, keterbatasan |
| 3 | Peta layanan pada peladen: daftar aplikasi, port, basis data, konsumen |
| 4 | Analisis penggunaan sumber daya per aplikasi: komposisi data, alokasi memori terhadap RAM, pertumbuhan data |
| 5 | Analisis beban lintas layanan pada satu host: total permintaan, puncak, waktu lambat |
| 6 | Perbandingan ukuran data antar sistem |
| 7 | Catatan insiden kapasitas: waktu, gejala, penyebab, durasi |
| 8 | Temuan dan risiko, termasuk risiko yang belum terukur |
| 9 | Rekomendasi: parameter, penjadwalan, penambahan sumber daya |
| 10 | Batasan dan rencana pengukuran lanjutan |

## Metrik minimum

- RAM total, terpakai, tersedia, swap, dan `zram` bila ada.
- Beban CPU 1/5/15 menit dan proses teratas.
- Disk: kapasitas, sisa, laju pertumbuhan per bulan.
- Ukuran basis data per tabel terbesar dan jumlah baris.
- Jumlah dan ukuran berkas log, lama retensi.
- Jumlah permintaan per jam, puncak, dan waktu respons.
- Uptime proses dan riwayat restart.

## Perintah pengukuran yang lazim

```bash
free -m
vmstat 1 5
ps -eo pid,ppid,%cpu,%mem,rss,comm --sort=-rss | head -20
df -h
du -sh /var/log/* | sort -h | tail -20
docker stats --no-stream
```

Basis data:

```sql
SELECT table_schema, table_name,
       ROUND((data_length + index_length) / 1024 / 1024, 1) AS mb,
       table_rows
FROM information_schema.tables
ORDER BY data_length + index_length DESC
LIMIT 20;
```

## Aturan penulisan

- Setiap angka disertai waktu pengambilan dan perintahnya.
- Bedakan beban puncak dan beban rata-rata.
- Jangan menyimpulkan kapasitas dari satu kali pengukuran.
- Cantumkan batasan: apa yang tidak terukur dan mengapa.
- Rekomendasi harus bisa diuji: parameter apa, nilainya berapa, dampaknya apa.
- Dokumen bersifat internal: klasifikasi ditulis di halaman judul, bukan di badan teks.
