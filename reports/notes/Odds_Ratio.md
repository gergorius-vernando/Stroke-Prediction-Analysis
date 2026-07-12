# Interpretasi Koefisien & Odds Ratio — Logistic Regression

## Kenapa Ini Kelebihan Khusus Logistic Regression

`feature_importances_` pada Random Forest (NB09) hanya bisa menjawab *"seberapa penting"* suatu fitur — tidak bisa menjawab *"menaikkan atau menurunkan risiko"*. Koefisien Logistic Regression bisa menjawab dua-duanya sekaligus: **arah** pengaruh (naik/turun) dan **kekuatan** pengaruh.

**Syarat agar interpretasi ini valid** (sudah dipenuhi di section sebelumnya):
1. Fitur sudah di-scaling (Section 3) — supaya besar-kecilnya koefisien bisa dibandingkan adil antar fitur.
2. VIF sudah dicek aman (Section 2) — supaya koefisien tidak terdistorsi oleh multikolinearitas.

---

## Apa itu Koefisien dan Odds Ratio

### Koefisien (angka mentah dari model)
- **Tanda (+/-)** = arah pengaruh. Positif → menaikkan risiko stroke. Negatif → menurunkan risiko.
- **Besar angka** = kekuatan pengaruh (semakin jauh dari 0, semakin kuat).

### Odds Ratio (OR) — transformasi koefisien agar lebih mudah dibaca
```
Odds Ratio = e^koefisien
```

**Cara baca:**
- OR > 1 → menaikkan risiko. Semakin jauh dari 1, semakin kuat efeknya.
- OR < 1 → menurunkan risiko.
- OR = 1 → tidak berpengaruh sama sekali.

**Karena fitur sudah di-scaling**, "kenaikan 1 unit" pada rumus OR berarti "kenaikan 1 standar deviasi" pada nilai asli fitur tersebut — bukan kenaikan 1 satuan asli (1 tahun, 1 mg/dL, dst).

---

## Hasil Aktual dari Model

| Fitur | Koefisien | Odds Ratio | Interpretasi |
|---|---|---|---|
| **age** | 1,6167 | **5,04** | Tiap naik ±22,6 tahun (1 std), odds stroke naik jadi 5,04x lipat — pengaruh paling dominan |
| smoking_status_never smoked | -0,1571 | 0,85 | Odds 15% lebih rendah (dibanding baseline, lihat catatan di bawah) |
| avg_glucose_level | 0,1546 | 1,17 | Tiap naik ±45 mg/dL (1 std), odds naik 17% |
| hypertension | 0,1516 | 1,16 | Odds naik 16% jika memiliki hipertensi |
| heart_disease | 0,0935 | 1,10 | Odds naik 10% jika memiliki penyakit jantung |
| bmi | 0,0925 | 1,10 | Tiap naik ±7,7 poin (1 std), odds naik 10% |
| smoking_status_smokes | 0,0529 | 1,05 | Odds naik 5% (efek kecil) |
| smoking_status_formerly smoked | -0,0224 | 0,98 | Nyaris tidak berpengaruh |

**Semua fitur klinis (avg_glucose_level, hypertension, heart_disease, bmi) menunjukkan arah yang sesuai literatur medis** — meningkatkan risiko stroke, memvalidasi model secara kualitatif.

---

## Catatan Khusus: Baseline `smoking_status`

Kategori `smoking_status` di-one-hot encoding dengan `drop_first=True` (NB08) — dari 4 kategori asli (Unknown, formerly smoked, never smoked, smokes), kategori **"Unknown"** yang dijadikan baseline/pembanding secara otomatis (alfabetis), sehingga tidak muncul sebagai baris terpisah di tabel.

**Cara kerja teknisnya:** "Unknown" direpresentasikan oleh kombinasi ketiga kolom dummy bernilai 0 sekaligus — bukan lewat kolom tersendiri. Karena tiap orang pasti masuk salah satu dari 4 kategori, begitu ketiga kolom dummy bernilai 0, itu otomatis berarti "Unknown" — informasinya tidak hilang, hanya direpresentasikan secara implisit.

**Implikasi:** seluruh Odds Ratio pada kategori `smoking_status` di atas merepresentasikan perbandingan terhadap kelompok "Unknown" — BUKAN terhadap "never smoked". Kalimat yang tepat: *"dibanding orang yang tidak mengungkapkan status merokoknya, orang berstatus 'never smoked' odds stroke-nya 15% lebih rendah"* — bukan "dibanding orang yang tidak pernah merokok".

Ini bukan kesalahan pemodelan, tapi keterbatasan interpretasi akibat pemilihan baseline otomatis (alfabetis) yang kurang intuitif dibanding jika baseline-nya sengaja diatur ke "never smoked".

---

## (Opsional) Menghitung Odds Ratio dari Sudut Pandang "Unknown"

Jika ingin tahu odds "Unknown" dibanding kategori lain (bukan sebaliknya), cukup dibalik (1 dibagi OR yang sudah ada) — tanpa perlu melatih ulang model:

```python
or_unknown_vs = 1 / coefficients.set_index('Fitur').loc[
    ['smoking_status_never smoked', 'smoking_status_formerly smoked', 'smoking_status_smokes'],
    'Odds_Ratio'
]
or_unknown_vs.index = ['vs never smoked', 'vs formerly smoked', 'vs smokes']
```

Hasil: OR "Unknown vs never smoked" ≈ **1,17** — mengindikasikan pasien yang tidak mengungkapkan status merokoknya justru punya odds stroke lebih tinggi dibanding yang mengaku "never smoked". Ini memberi bukti tambahan yang mendukung karakterisasi MNAR pada kategori "Unknown" sejak NB02/NB03 (kemungkinan pasien yang menyembunyikan status merokoknya justru memang perokok/mantan perokok).

---