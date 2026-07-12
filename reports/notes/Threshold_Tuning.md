# Threshold Tuning & Alasan Pemilihan Threshold

## Kenapa Threshold Tuning Diperlukan

Model dilatih dengan `class_weight='balanced'` (Cost-Sensitive Learning) untuk mengatasi imbalance kelas. Namun, `class_weight` hanya memengaruhi proses *training*, sementara `.predict()` tetap memakai ambang keputusan default 0,5. Threshold tuning diperlukan untuk mengecek apakah 0,5 itu benar-benar titik terbaik, atau ada titik lain yang menghasilkan keseimbangan recall-precision yang lebih sesuai konteks medis.

**Catatan penting:** menggeser threshold selalu berupa trade-off — bukan solusi "gratis". Trade-off ini diterima karena dalam konteks medis, kelewatan mendeteksi pasien berisiko (False Negative) memiliki konsekuensi jauh lebih berbahaya dibanding salah alarm (False Positive).

## Cara Kerja (kode yang dipakai di NB09 & NB10)

```python
y_proba = model.predict_proba(X_test)[:, 1]  # probabilitas mentah, bukan tebakan final
for t in thresholds:
    y_pred_t = (y_proba >= t).astype(int)
    r = recall_score(y_test, y_pred_t)
    p = precision_score(y_test, y_pred_t, zero_division=0)
    f1 = f1_score(y_test, y_pred_t)
    f2 = (5 * p * r) / (4 * p + r) if (4*p + r) > 0 else 0
```

`predict_proba()` memberi probabilitas (0,0–1,0), bukan tebakan final 0/1 — dari situ ambang keputusan bisa digeser manual, bukan pasrah pakai default sklearn.

---

## Bagian 1: Random Forest (NB09)

### Hasil Eksperimen — 6 Titik Threshold

| Threshold | Recall | Precision | F1 | F2 | FN | FP |
|---|---|---|---|---|---|---|
| 0,5 | 12,2% | 24,0% | 0,162 | 0,135 | 43 | 19 |
| 0,4 | 20,4% | 20,4% | 0,204 | 0,204 | 39 | 39 |
| **0,3** | 42,9% | 21,2% | **0,284 (F1 tertinggi)** | 0,356 | 28 | 78 |
| 0,2 | 63,3% | 17,4% | 0,273 | 0,414 | 18 | 147 |
| **0,15** | 75,5% | 16,2% | 0,267 | **0,436 (F2 tertinggi)** | 12 | 192 |
| 0,1 | 81,6% | 13,7% | 0,235 | 0,410 | 9 | 253 |

**Threshold dieksplorasi menurun (0,5→0,1)** karena RF di default terlalu "pelit" memprediksi stroke (recall sangat rendah).

### Keputusan: Threshold 0,2

Dipilih sebagai titik tengah antara F1-optimal (0,3) dan F2-optimal (0,15) — recall naik signifikan (12,2%→63,3%, FN turun 43→18), dengan kenaikan FP (19→147) yang masih dapat diterima untuk skrining awal.

---

## Bagian 2: Logistic Regression (NB10)

### Karakteristik Berbeda dari Random Forest

`class_weight` bekerja lebih langsung di Logistic Regression — ia mengubah fungsi kerugian (*loss function*) yang secara langsung menggeser *decision boundary*, berbeda dari Random Forest yang efeknya teredam oleh proses voting antar pohon. Akibatnya, LR pada threshold default (0,5) sudah **terlalu sering** memprediksi stroke (314 dari 1.019, dibanding 49 kasus asli) — kebalikan dari masalah RF.

### Hasil Eksperimen — 6 Titik Threshold

| Threshold | Recall | Precision | F1 | F2 | FN | FP |
|---|---|---|---|---|---|---|
| **0,7** | 69,4% | 19,8% | **0,308 (F1 tertinggi)** | 0,462 | 15 | 138 |
| **0,6** | 81,6% | 17,5% | 0,289 | **0,471 (F2 tertinggi)** | 9 | 188 |
| 0,5 (default) | 85,7% | 13,4% | 0,231 | 0,412 | 7 | 272 |
| 0,4 | 89,8% | 11,2% | 0,200 | 0,374 | 5 | 348 |
| 0,3 | 91,8% | 9,7% | 0,176 | 0,341 | 4 | 418 |
| 0,2 | 95,9% | 8,3% | 0,152 | 0,308 | 2 | 522 |

**Threshold dieksplorasi ke DUA arah (naik ke 0,7 dan turun ke 0,2)** — berbeda dari RF — karena LR di default sudah terlalu sensitif, sehingga perlu dicek apakah menaikkan ambang (bukan menurunkan) yang justru memperbaiki keseimbangan.

### Keputusan: Threshold 0,6

Dipilih karena F2-nya tertinggi (0,471) — paling sesuai prioritas medis (recall diutamakan) — dengan recall tetap tinggi (81,6%, hanya 9 dari 49 kasus kelewatan) dan FP jauh lebih terkendali dibanding default (188 vs 272).

---

## Bagian 3: Formula F1 dan F2 — Referensi

### Rumus

```
F1 = 2 · (precision × recall) / (precision + recall)
F2 = 5 · (precision × recall) / (4 × precision + recall)
```

### Kenapa F1 Saja Tidak Cukup

F1 menganggap recall dan precision **sama penting** (bobot seimbang). Namun karena disepakati bahwa recall lebih diprioritaskan dalam konteks medis, F2 dipakai sebagai pelengkap — memberi bobot lebih besar pada recall.

### Proporsi Bobot Precision vs Recall (koreksi penting)

F-beta score secara matematis setara dengan *weighted harmonic mean*, dengan bobot:
```
bobot precision = 1 / (1 + β²)
bobot recall     = β² / (1 + β²)
```

| Metrik | β | Bobot Precision | Bobot Recall |
|---|---|---|---|
| F1 | 1 | 50% | 50% |
| F2 | 2 | **20%** | **80%** |

**Catatan:** F2 sering disalahpahami sebagai "recall dibobot 2x" (rasio 67:33 atau 70:30) — padahal karena β dikuadratkan (β²=4) dalam rumus, proporsi sebenarnya jauh lebih miring ke recall, yaitu **80:20**.

---

## Ringkasan Perbandingan Kedua Model

| | Random Forest | Logistic Regression |
|---|---|---|
| Arah eksplorasi threshold | Turun (0,5→0,1) | Naik-turun (0,7→0,2) |
| Masalah di threshold default | Recall terlalu rendah | Recall tinggi, tapi precision sangat rendah |
| Threshold final | 0,2 | 0,6 |
| Dasar pemilihan | Titik tengah F1 (0,3) & F2 (0,15) | F2-optimal |
| Recall di threshold final | 63,3% | 81,6% |
| Precision di threshold final | 17,4% | 17,5% |

## Klasifikasi Metode (untuk referensi metodologi)

Pendekatan ini menggabungkan dua kategori resmi dalam literatur *imbalanced learning*:
1. **Cost-Sensitive Learning** — via `class_weight='balanced'` (algoritma diberi bobot penalti berbeda per kelas saat training)
2. **Threshold-Moving** — via threshold tuning pasca-training (menggeser ambang keputusan dari default 0,5), dengan arah eksplorasi yang disesuaikan karakteristik masing-masing algoritma

Berbeda dari pendekatan **Resampling** (SMOTE, dll) yang bekerja di level data.