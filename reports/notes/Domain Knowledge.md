# Dasar Pemilihan Batas Domain Knowledge — Outlier Data Cleaning

Dokumen ini menjelaskan asal-usul angka batas yang dipakai di NB03 (Data Cleaning), khususnya bagaimana angka **0–300** untuk `avg_glucose_level` didapat — karena angka ini melalui beberapa kali koreksi, bukan langsung ditentukan sekali jadi.

---

## `avg_glucose_level`: 0 – 300 mg/dL

### Kenapa tidak pakai IQR (metode statistik biasa)

Distribusi `avg_glucose_level` bersifat **bimodal** — ada dua gerombolan terpisah: kelompok non-diabetes (~55–120) dan kelompok diabetes (~185–270). IQR mengasumsikan distribusi unimodal, sehingga akan salah mendeteksi seluruh sub-populasi diabetes sebagai outlier, padahal itu sinyal klinis valid. Simulasi menunjukkan IQR blanket akan membuang 33,7% kasus stroke asli (84 dari 249) kalau tetap dipaksakan.

### Bagaimana angka 300 didapat — dua jalur bukti yang bertemu

**Jalur 1 — Gap statistik alami**

Setelah dataset sengaja "dikotori" (NB02, simulasi human-error berupa nilai ×5), dicek posisi nilai asli vs nilai hasil corruption:
- Nilai maksimum alami di data asli: **271,74**
- Nilai terendah dari hasil corruption (×5): **341,75**

Ada gap kosong di rentang **272–341** — tidak ada satupun data asli yang jatuh di situ. Angka **300** dipilih karena duduk tepat di tengah gap ini, memberi margin aman ke kedua sisi.

**Jalur 2 — Referensi klinis (ADA)**

Protokol uji klinis mendefinisikan **hiperglikemia akut/berat** pada glukosa plasma puasa di atas **270 mg/dL** — kondisi yang sudah dianggap serius secara medis. Angka 300 sejalan dengan ambang ini, bukan kebetulan statistik semata.

**Kedua jalur bertemu di titik yang sama** — itu yang membuat angka 300 defensible secara ganda (statistik + klinis), bukan cuma pilihan sembarang.

### Kenapa batas BAWAH bukan 70 (meski itu ambang resmi hipoglikemia ADA)

Ini bagian yang sempat salah dan perlu dikoreksi selama proses diskusi:

1. ADA mendefinisikan **hipoglikemia** sebagai glukosa darah **< 70 mg/dL** — angka ini sempat mau dipakai juga sebagai batas bawah outlier.
2. Tapi setelah dicek ke data asli: ada **754 baris data ASLI** (bukan hasil corruption) di rentang 55–70 mg/dL, termasuk **27 kasus stroke asli**. Nilai serendah ini bukan error — itu representasi kondisi hipoglikemia ringan yang nyata secara klinis.
3. Kalau 70 dipakai sebagai batas bawah **outlier removal**, 754 pasien valid akan ikut terhapus secara keliru — mengulang kesalahan yang sama seperti isu IQR di awal (membuang sinyal klinis asli, bukan error).

**Penting dibedakan:** angka 70 tetap dipakai, tapi HANYA di NB02 (Data Corruption) sebagai syarat baris mana yang **boleh dipilih untuk disimulasikan rusak** — bukan sebagai batas penghapusan data. Dua fungsi ini berbeda meski angkanya sama:

| | Fungsi | Efeknya ke data |
|---|---|---|
| **70 di NB02** | Syarat baris boleh dipilih untuk corruption | Tidak menghapus data apapun |
| **70 (dibatalkan) di NB03** | Batas bawah outlier | Akan menghapus 754 data valid — dibatalkan |

### Kesimpulan akhir

```
avg_glucose_level: lebih dari 0 (sanity check implausibilitas) DAN kurang dari sama dengan 300 (ambang hiperglikemia akut, sekaligus batas statistik hasil corruption)
```

Tanpa batas bawah klinis yang ketat — nilai rendah yang genuinely rendah (hipoglikemia) dipertahankan sebagai data valid.

---

## `bmi`: 10 – 110 (safety net, bukan angka WHO resmi)

WHO mengklasifikasikan BMI resmi hanya sampai **"Obese Class III: ≥40"**, tanpa batas atas baku setelah itu. Jadi 10 dan 110 **bukan** angka rujukan WHO — keduanya murni *sanity check* implausibilitas biologis:
- Rentang alami data: 10,3–97,6 → batas 10–110 tidak memotong data valid apapun, murni jaring pengaman.

## `age`: ≤ 100

Batas realistis usia manusia untuk data populasi umum, bukan hasil kajian klinis spesifik. Tidak memotong data apapun (usia maksimum asli hanya 82 tahun).

---

## Pelajaran dari proses penentuan batas ini

1. **Satu angka bisa punya dua fungsi berbeda** (seleksi vs penghapusan) — jangan disamaratakan hanya karena nilainya sama.
2. **Angka yang "kedengaran benar secara klinis" tetap wajib dicek ke data sebenarnya** sebelum dipakai — 70 itu benar sebagai ambang hipoglikemia, tapi salah kalau dipakai untuk menghapus data.
3. **Bukti ganda (statistik + klinis) lebih kuat daripada satu jenis bukti saja** — itu sebabnya angka 300 lebih defensible dibanding 70 untuk kasus penghapusan outlier.