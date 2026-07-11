# Threshold Tuning & Alasan Pemilihan Threshold 0,2

## Kenapa Threshold Tuning Diperlukan

Model Random Forest sudah dilatih dengan `class_weight='balanced'` (Cost-Sensitive Learning) untuk mengatasi imbalance kelas. Namun, evaluasi pada threshold default (0,5) tetap menghasilkan recall yang sangat rendah:

| Metrik | Threshold default (0,5) |
|---|---|
| Recall | 12,24% |
| Precision | 24,00% |
| FN (kasus stroke kelewatan) | 43 dari 49 |

**Penyebabnya:** `class_weight` hanya memengaruhi proses *training* (bagaimana pohon keputusan menghitung kemurnian split), TAPI saat `.predict()` dipanggil, sklearn tetap memakai ambang keputusan default 0,5 (probabilitas ≥50% baru ditebak "stroke"). Banyak kasus stroke yang probabilitas prediksinya naik karena class_weight, tapi belum cukup tinggi untuk melewati ambang 0,5 — sehingga tetap ditebak "tidak stroke".

---

## Apa itu Threshold Tuning

Alih-alih pakai `.predict()` (langsung memberi tebakan final 0/1 dengan ambang tetap 0,5), dipakai `.predict_proba()` yang memberi **probabilitas mentah** (0,0–1,0) — lalu ambang keputusan digeser manual untuk mencari titik yang lebih sesuai kebutuhan.

```python
y_proba = rf_model.predict_proba(X_test)[:, 1]
y_pred_custom = (y_proba >= threshold).astype(int)
```

**Catatan penting:** menurunkan threshold **pasti** meningkatkan jumlah salah alarm (False Positive) — bukan solusi gratis. Trade-off ini diterima karena dalam konteks medis, kelewatan mendeteksi pasien berisiko (False Negative) memiliki konsekuensi jauh lebih berbahaya dibanding salah alarm.

---

## Hasil Eksperimen — 6 Titik Threshold

| Threshold | Recall | Precision | F1 | FN | FP |
|---|---|---|---|---|---|
| 0,5 | 12,2% | 24,0% | 0,162 | 43 | 19 |
| 0,4 | 20,4% | 20,4% | 0,204 | 39 | 39 |
| 0,3 | 42,9% | 21,2% | 0,284 | 28 | 78 |
| 0,2 | 63,3% | 17,4% | 0,273 | 18 | 147 |
| 0,15 | 75,5% | 16,2% | 0,267 | 12 | 192 |
| 0,1 | 81,6% | 13,7% | 0,235 | 9 | 253 |

**Pola yang teramati:** semakin threshold diturunkan, recall naik namun FP juga bertambah — trade-off klasik. Ada titik *diminishing returns* di sekitar 0,15 ke bawah: dari 0,15→0,1, recall cuma naik 6,1 poin (+3 kasus terselamatkan) tapi FP melonjak 61 kasus — "harga" tambahan recall jadi jauh lebih mahal.

---

## Keputusan Final: Threshold 0,2

Dipilih sebagai **titik tengah** antara F1-optimal (0,3) dan F2-optimal (0,15), dengan pertimbangan:

1. **F1 (0,3) kurang cocok** dipakai sebagai patokan utama karena mengasumsikan precision & recall sama penting — tidak sesuai prioritas medis proyek ini.
2. **F2-optimal (0,15) menghasilkan FP yang cukup tinggi** (192, ~19,8% dari populasi sehat) — dan F2-nya sendiri hanya beda tipis dari 0,2 (0,436 vs 0,414), sehingga tambahan alarm palsu yang signifikan tidak sebanding dengan sedikit peningkatan F2.
3. **Threshold 0,2 memberi lompatan recall yang paling signifikan secara proporsional** (12,2%→63,3%) sambil FP (147, ~15,2%) masih berada di rentang yang dapat diterima untuk konteks skrining awal (bukan diagnosis final).

### Dampak Konkret: Threshold 0,5 → Threshold 0,2

| Metrik | Threshold 0,5 | Threshold 0,2 | Perubahan |
|---|---|---|---|
| Recall | 12,2% | **63,3%** | +51,1 poin |
| Precision | 24,0% | 17,4% | -6,6 poin |
| F1-Score | 0,162 | 0,273 | +0,111 |
| Kasus stroke terdeteksi (TP) | 6 dari 49 | **31 dari 49** | +25 kasus |
| Kasus stroke kelewatan (FN) | 43 dari 49 | **18 dari 49** | -25 kasus |
| Alarm palsu (FP) | 19 dari 970 | 147 dari 970 | +128 kasus |

---

## Keterbatasan yang Perlu Diakui

Precision pada threshold final (17,4%) tergolong rendah — dari setiap ~6 pasien yang di-flag model sebagai berisiko, hanya ±1 yang benar-benar mengalami stroke. Ini trade-off yang **disengaja** demi memaksimalkan deteksi kasus berisiko, dan perlu ditulis eksplisit sebagai keterbatasan model dalam paper — bukan disembunyikan.

## Klasifikasi Metode (untuk referensi metodologi)

Pendekatan ini menggabungkan dua kategori resmi dalam literatur *imbalanced learning*:
1. **Cost-Sensitive Learning** — via `class_weight='balanced'` (algoritma diberi bobot penalti berbeda per kelas saat training)
2. **Threshold-Moving** — via threshold tuning pasca-training (menggeser ambang keputusan dari default 0,5)

Berbeda dari pendekatan **Resampling** (SMOTE, dll) yang bekerja di level data — kombinasi ini tidak mengubah data training sama sekali.