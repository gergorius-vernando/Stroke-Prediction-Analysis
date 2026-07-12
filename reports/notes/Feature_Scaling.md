# Feature Scaling — Alasan, Cara Kerja, dan Hasil

## Kenapa Diperlukan — Khusus untuk Logistic Regression

### Masalahnya: Fitur di Dataset Ini Punya Skala yang Sangat Berbeda

| Fitur | Rentang asli |
|---|---|
| `age` | 0 – 82 (tahun) |
| `avg_glucose_level` | 55 – 271 (mg/dL) |
| `bmi` | 10 – 97 |
| `hypertension`, `heart_disease` | 0 – 1 (biner) |

Kalau `age` (rentang puluhan) dan `hypertension` (cuma 0/1) dibiarkan apa adanya masuk ke Logistic Regression, model bisa salah "mengira" `age` jauh lebih berpengaruh, padahal itu cuma efek skala angka, bukan kekuatan hubungan sesungguhnya terhadap risiko stroke.

### Kenapa Random Forest Tidak Terpengaruh Masalah Ini

Random Forest membuat keputusan lewat pertanyaan ambang batas per fitur secara independen (*"age > 50?"*, *"glucose > 150?"*) — tiap fitur dievaluasi di skalanya masing-masing, tidak pernah dijumlahkan atau dibandingkan langsung antar fitur secara matematis. Itu sebabnya NB09 tidak memerlukan scaling sama sekali.

Logistic Regression sebaliknya menghitung kombinasi linear dari seluruh fitur sekaligus (`β₁×age + β₂×glucose + ...`) — proses ini sensitif terhadap skala, sehingga scaling menjadi wajib.

---

## Metode yang Digunakan: StandardScaler

### Rumus

```
nilai_baru = (nilai_asli − rata-rata) / standar_deviasi
```

Setiap nilai diterjemahkan ke satuan baru: *"seberapa jauh nilai ini dari rata-rata, diukur dalam satuan standar deviasi"* — bukan lagi satuan asli (tahun, mg/dL, dst).

**Contoh konkret (`age`, rata-rata ≈43, std ≈22,6):**
- Usia 82 tahun → (82−43)/22,6 = **+1,73** (1,73 std di atas rata-rata)
- Usia 43 tahun → **0** (persis di rata-rata)
- Usia 0 tahun → **−1,90** (1,90 std di bawah rata-rata)

Setelah diterjemahkan seperti ini, semua fitur — baik `age` maupun `hypertension` — punya "bahasa" yang sama dan bisa dibandingkan secara adil oleh model.

---

## Prinsip Krusial: Fit Hanya dari Data Training

```python
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)   # fit + transform
X_test_scaled = scaler.transform(X_test)          # transform SAJA, tanpa fit ulang
```

`X_test` **tidak boleh** ikut proses `fit()` — kalau ikut, itu termasuk *data leakage* (informasi dari data testing "bocor" ke tahap persiapan sebelum model dievaluasi secara jujur). Prinsip ini sama dengan yang diterapkan pada train-test split di NB08: data testing harus tetap "asing" bagi model sampai tahap evaluasi.

---

## Hasil Aktual — Sebelum vs Sesudah Scaling

| Fitur | Mean sebelum | Std sebelum | Mean sesudah | Std sesudah |
|---|---|---|---|---|
| age | 43,19 | 22,58 | ≈0 | 1,0 |
| avg_glucose_level | 105,89 | 44,96 | ≈0 | 1,0 |
| bmi | 28,85 | 7,66 | ≈0 | 1,0 |
| hypertension | 0,10 | 0,30 | ≈0 | 1,0 |
| heart_disease | 0,05 | 0,23 | ≈0 | 1,0 |
| smoking_status_formerly smoked | 0,17 | 0,37 | ≈0 | 1,0 |
| smoking_status_never smoked | 0,38 | 0,49 | ≈0 | 1,0 |
| smoking_status_smokes | 0,15 | 0,35 | ≈0 | 1,0 |

Seluruh fitur, tanpa terkecuali, berhasil diseragamkan menjadi mean ≈0 dan std =1 — membuktikan skala yang tadinya sangat berbeda (age puluhan vs hypertension 0/1) sekarang setara.

**Catatan kecil:** angka "−0,0" yang kadang muncul di output bukan berarti negatif — itu sekadar cara komputer menampilkan angka yang sangat mendekati nol (*floating-point rounding*), bukan indikasi kesalahan.

---

## Kenapa Ini Penting untuk Tahap Selanjutnya

Scaling ini menjadi prasyarat bagi **Section 8 (Interpretasi Koefisien)** — tanpa scaling, koefisien Logistic Regression tidak bisa dibandingkan besarannya secara adil antar fitur (koefisien `age` otomatis akan terlihat lebih besar hanya karena rentang aslinya lebih lebar, bukan karena pengaruhnya lebih kuat). Dengan seluruh fitur di skala yang sama, besar-kecilnya koefisien nanti benar-benar mencerminkan kekuatan hubungan masing-masing fitur terhadap risiko stroke.

---