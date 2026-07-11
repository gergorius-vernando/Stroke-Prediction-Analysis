Feature Selection — Metode & Alasan Keputusan

## 1. Kenapa Filter + Embedded (bukan Wrapper)?

Ada 3 keluarga metode feature selection: **Filter** (cek tiap fitur sendiri-sendiri, murah & cepat), **Wrapper** (uji kombinasi fitur, mahal secara komputasi), **Embedded** (nempel otomatis saat training model).

**Wrapper (RFE) sengaja tidak dipakai** karena:
- Jumlah fitur kandidat kecil (~10 kolom) — hasil Filter + Embedded sudah saling mengonfirmasi (triangulasi), RFE kemungkinan besar cuma mengulang kesimpulan yang sama dengan biaya komputasi lebih besar.
- Sesuai instruksi tugas: *"tidak semua metode preprocessing harus digunakan, pilih yang diperlukan dengan argumen jelas."*

---

## 2. Filter Method — cek tiap fitur SENDIRIAN vs target

| Metode | Dipakai untuk | Menjawab pertanyaan |
|---|---|---|
| **Chi-square** | Fitur kategorikal/biner (gender, hypertension, dll) | Apakah proporsi stroke beda signifikan antar kategori? |
| **Mann-Whitney U** | Fitur numerik (age, glucose, bmi) | Apakah sebaran nilai beda signifikan antara grup stroke vs tidak? |
| **Point-biserial correlation (r)** | Fitur numerik | Seberapa kuat & searah hubungannya (skala -1 sampai +1)? |

**Cara baca p-value** (dipakai chi-square maupun Mann-Whitney): peluang pola yang muncul itu murni kebetulan, KALAU seandainya sebenarnya tidak ada hubungan. **p < 0,05 = signifikan** (kemungkinan besar bukan kebetulan).

**Penting:** p-value cuma jawab "ADA hubungan atau tidak" — BUKAN "seberapa besar pengaruhnya". Itu tugas r (korelasi) atau importance (lihat Bagian 3). Dengan sampel besar, hubungan yang kecil pun bisa lolos jadi "signifikan" (kasus `bmi`: p=0,0003 tapi r cuma 0,037).

**Keterbatasan Filter:** cuma lihat 1 fitur vs target secara **terpisah** — tidak tahu kalau suatu fitur ternyata cuma "numpang" sinyal dari fitur lain (lihat kasus `ever_married` di Bagian 5).

---

## 3. Embedded Method — cek fitur BARENGAN, termasuk pola non-linear

| Metode | Cara kerja | Kelebihan dibanding r/point-biserial |
|---|---|---|
| **Random Forest Importance** | Ukur seberapa sering & efektif fitur dipakai buat "memecah" data di 300 pohon keputusan sekaligus | Bisa nangkep pola non-linear + mempertimbangkan interaksi antar fitur |
| **Mutual Information** | Ukur seberapa besar suatu fitur "bikin yakin" nebak stroke, tanpa peduli bentuk hubungannya | Bisa nangkep pola non-linear, cocok jadi cross-check RF |

**Kenapa perlu, padahal udah ada Filter:** r (korelasi) cuma bisa nangkep pola **garis lurus**. Kalau hubungannya melengkung (misal risiko cuma melonjak di atas ambang tertentu, bukan naik pelan-pelan), r bisa "buta" walau hubungannya beneran kuat — persis kasus `bmi` (r=0,037 tapi RF importance 0,182, peringkat ke-3 tertinggi).

**Cara baca:** kedua angka ini **tidak** punya patokan universal kayak p-value (tidak ada "0,05" versi RF/MI) — cuma bisa dibandingkan **rangking relatifnya** dalam 1 analisis yang sama.

---

## 4. Tabel Hasil Lengkap (hasil aktual dari notebook)

| Fitur | Chi2 / U-stat | p-value | r / — | RF Importance | Mutual Info |
|---|---|---|---|---|---|
| `age` | — | <0,001 | 0,244 | **0,386** | **0,036** |
| `avg_glucose_level` | — | <0,001 | 0,132 | 0,205 | 0,006 |
| `bmi` | — | 0,0003 | 0,037 | 0,182 | 0,010 |
| `smoking_status` | 26,34 | <0,001 | — | 0,051 | 0,004 |
| `work_type` | 47,29 | <0,001 | — | 0,048 | 0,004 |
| `ever_married` | 57,40 | <0,001 | — | 0,034 | 0,010 |
| `hypertension` | 79,90 | <0,001 | — | 0,030 | 0,012 |
| `gender` | 0,57 | 0,449 | — | 0,023 | **0,000** |
| `Residence_type` | 1,47 | 0,225 | — | 0,022 | 0,003 |
| `heart_disease` | 92,30 | <0,001 | — | 0,020 | 0,010 |

---

## 5. Keputusan Final per Fitur

### ✅ Dipertahankan (6 fitur) — konsisten kuat di semua metode + masuk akal medis

| Fitur | Alasan |
|---|---|
| `age`, `avg_glucose_level`, `bmi` | Signifikan + RF importance tertinggi (termasuk `bmi` yang ternyata kuat lewat pola non-linear) |
| `hypertension`, `heart_disease`, `smoking_status` | Signifikan + risk factor stroke yang diakui langsung secara medis, walau RF importance-nya moderat/rendah (kemungkinan overlap sama `age`) |

### ❌ Dibuang — gagal semua uji statistik

| Fitur | Alasan |
|---|---|
| `gender` | p=0,449 (jauh di atas 0,05), Mutual Information **persis 0** — bukti paling final, secara harfiah tidak ada informasi apapun yang membantu nebak stroke |
| `Residence_type` | p=0,225, konsisten lemah di semua metode (importance & MI terendah) |

### ⚠️ Dibuang — signifikan secara statistik, TAPI proxy dari `age`

| Fitur | Alasan |
|---|---|
| `ever_married`, `work_type` | p<0,05 dan RF importance lumayan, TAPI: 0 orang di bawah 18 tahun yang berstatus menikah — usia sendirian sudah hampir cukup buat nebak status ini. Informasinya sebagian besar tumpang tindih dengan `age`, sehingga kontribusi tambahannya kecil dan berisiko menyebabkan multikolinearitas di Logistic Regression |

---

## 6. Ringkasan Alur Keputusan (per fitur)

```
1. Uji statistik (Chi-square / Mann-Whitney) → hasilkan p-value
2. p < 0,05?
   TIDAK → dibuang  (gender, Residence_type)
   YA    → lanjut ke langkah 3
3. Cek kekuatan hubungan (r, RF importance, Mutual Information)
4. Cek akal sehat domain: apakah hubungan ini masuk akal secara medis,
   atau cuma numpang sinyal dari fitur lain (proxy)?
   Proxy/meragukan → dibuang dengan catatan (ever_married, work_type)
   Jelas & langsung  → PERTAHANKAN (age, glucose, bmi, hypertension,
                        heart_disease, smoking_status)
```

**Intinya:** tidak ada satupun metode yang dipakai sendirian untuk memutuskan — keputusan akhir selalu hasil **triangulasi** (bukti statistik + bukti model + akal sehat domain), supaya tidak salah kaprah seperti kasus `ever_married` yang "kelihatan penting" secara angka tapi sebenarnya cuma bayangan dari `age`.