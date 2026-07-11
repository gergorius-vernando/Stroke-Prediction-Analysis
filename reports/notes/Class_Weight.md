# `class_weight='balanced'` — Cara Kerja & Dampaknya

## Analogi Dasar: Asisten yang Dibayar per Tebakan Benar

Bayangin asisten yang tugasnya nebak "orang ini bakal stroke apa nggak" dari 100 orang, di mana cuma 5 yang beneran stroke, 95 tidak.

**Tanpa aturan khusus**, asisten nemu cara "curang": jawab **"TIDAK STROKE" ke SEMUA orang**. Hasilnya tetap benar 95 dari 100 kali (95% akurat!) — padahal dia nggak belajar pola apapun, cuma jawab sama rata. Masalahnya, tugas paling penting justru nyari yang 5 orang itu — bukan sekadar benerin tebakan ke 95 orang sisanya.

---

## Bagaimana `class_weight='balanced'` Mengatasi Ini

Aturan diubah: **"Kalau kamu salah nebak orang yang KENA stroke, dendanya jauh lebih berat dibanding salah nebak orang yang tidak stroke."**

### Rumus & Angka Konkret (dari data project ini)

```
weight = n_total / (n_classes × n_samples_kelas_itu)
```

| Kelas | Jumlah di training set | Bobot |
|---|---|---|
| 0 (Tidak Stroke) | 3.878 | 0,5254 |
| 1 (Stroke) | 197 | **10,3426** |

**Rasio: 10,3426 / 0,5254 ≈ 19,69x** — sebanding dengan rasio jumlah data (3.878/197 ≈ 19,69). Artinya: **1 kesalahan pada kasus stroke "dihitung" setara dengan ±20 kesalahan pada kasus tidak-stroke** saat model dilatih.

**Penting:** ini bukan proses menambah/mengubah data (beda dari SMOTE). `class_weight` cuma mengubah cara model "dihukum" saat belajar — `X_train`/`y_train` tetap 100% data asli.

---

## Dampak Konkret ke Perilaku Model

### Sebelum kena hukuman (tanpa class_weight)
Model aman-aman aja jawab "tidak stroke" ke semua orang yang meragukan — toh dendanya sama rata, dan strategi ini jarang salah (95% orang emang tidak stroke).

### Setelah kena hukuman (dengan class_weight)
Untuk kasus yang meragukan (misal usia tua + glucose agak tinggi, tapi belum jelas-jelas ekstrem), model jadi lebih "waspada" — logikanya berubah jadi: *"Kalau aku salah dan ternyata dia stroke, dendanya besar. Mending jawab 'stroke' untuk jaga-jaga."*

### Trade-off yang terjadi (2 sisi mata uang)

| Efek | Penjelasan |
|---|---|
| ✅ **Recall naik** | Model lebih sering menangkap kasus stroke yang beneran — lebih waspada, tidak gampang bilang "aman" |
| ⚠️ **Precision turun** | Model juga jadi lebih sering "salah alarm" ke orang sehat — menebak "stroke" padahal orangnya baik-baik saja |
| ⚠️ **Accuracy total bisa turun** | Karena salah alarm ke populasi sehat (yang jumlahnya besar, 95%) jadi lebih sering, angka accuracy keseluruhan bisa sedikit menurun dibanding strategi "jawab tidak-stroke semua" |

---

## Kenapa Trade-off Ini Dianggap Berhasil, Bukan Gagal

Dalam konteks medis, dua jenis kesalahan itu **tidak setara dampaknya**:
- **False Alarm** (dikira stroke, ternyata sehat) → konsekuensinya: pasien disuruh cek lebih lanjut, biaya & waktu terbuang, tapi relatif aman.
- **Kelewatan** (dikira sehat, ternyata stroke) → konsekuensinya: pasien tidak mendapat penanganan tepat waktu, risiko fatal.

Karena kelewatan jauh lebih berbahaya daripada false alarm, **menurunkan precision demi menaikkan recall adalah trade-off yang disengaja dan diinginkan** — bukan kegagalan model. Ini alasan utama kenapa evaluasi model nanti (NB11) tidak boleh hanya bergantung pada accuracy, sejalan dengan kesimpulan accuracy paradox di NB04.

---

## Ringkasan

1. `class_weight='balanced'` memberi penalti lebih berat pada kesalahan di kelas minoritas (stroke), sebanding dengan rasio imbalance data.
2. Tidak mengubah data sama sekali — murni mengubah cara model dihukum saat training.
3. Efeknya: recall naik (lebih baik), tapi precision & accuracy bisa turun — trade-off yang disengaja karena konteks medis memprioritaskan tidak melewatkan kasus berisiko dibanding menghindari salah alarm.