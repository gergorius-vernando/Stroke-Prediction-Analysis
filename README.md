# Stroke Prediction Analysis

Proyek analisis dan preprocessing data kesehatan untuk memprediksi risiko stroke, menggunakan **Healthcare Stroke Prediction Dataset**. Proyek ini merupakan bagian dari tugas mata kuliah Preprocessing Data — mencakup analisis data, preprocessing lengkap dengan justifikasi metodologis, hingga pemodelan dan evaluasi menggunakan Random Forest dan Logistic Regression.

---

## Ringkasan Dataset

- **Sumber:** Healthcare Stroke Prediction Dataset
- **Ukuran:** 5.110 baris × 12 kolom
- **Target:** `stroke` (0 = tidak stroke, 1 = stroke) — **imbalanced** (95,1% vs 4,9%)
- **Fitur final digunakan (6):** `age`, `avg_glucose_level`, `bmi`, `hypertension`, `heart_disease`, `smoking_status`

---

## Struktur Project

```
Stroke-Prediction-Analysis/
├── data/
│   ├── raw/                  # Dataset asli, tidak pernah diubah
│   └── processed/            # Hasil tiap tahap preprocessing
├── notebooks/                # 11 notebook, urut dari 01-11
├── reports/
│   └── figures/              # Seluruh visualisasi & confusion matrix
├── notes/                    # Dokumentasi justifikasi tiap keputusan metodologis
├── models/                   # Model final tersimpan (.pkl) untuk demo
├── app.py                    # Demo interaktif (Streamlit)
└── requirements.txt
```

---

## Daftar Notebook

| # | Notebook | Isi |
|---|---|---|
| 01 | Data Understanding | Eksplorasi awal dataset asli (ground truth) |
| 02 | Data Corruption | Simulasi kerusakan data (duplikat, inkonsistensi, error nilai, missing value) |
| 03 | Data Cleaning | Penanganan duplikat, inkonsistensi, missing value, dan outlier |
| 04 | Imbalanced Data Check | Analisis distribusi target & implikasinya terhadap strategi evaluasi |
| 05 | Feature Selection | Seleksi fitur menggunakan filter method + embedded method |
| 06 | Dimensionality Reduction | Justifikasi keputusan untuk tidak menerapkan PCA |
| 07 | Data Visualization | Visualisasi pendukung untuk paper |
| 08 | Data Preparation for Modeling | Encoding, train-test split, perhitungan class weight |
| 09 | Modeling: Random Forest | Training, threshold tuning, eksperimen SMOTE |
| 10 | Modeling: Logistic Regression | VIF check, scaling, training, threshold tuning, interpretasi koefisien |
| 11 | Evaluation & Comparison | Perbandingan baseline vs model final, rekomendasi akhir |

---

## Keputusan Metodologis Utama

- **Outlier Detection:** Domain Knowledge-based (bukan IQR statistik murni) — divalidasi dengan referensi klinis ADA, karena distribusi `avg_glucose_level` bersifat bimodal.
- **Feature Selection:** Triangulasi Filter method (Chi-square, Mann-Whitney U, point-biserial correlation) + Embedded method (Random Forest Importance, Mutual Information). Wrapper method (RFE) sengaja tidak digunakan.
- **Imbalance Handling:** Cost-Sensitive Learning (`class_weight='balanced'`) + Threshold-Moving, dipilih berdasarkan validasi empiris dibanding SMOTE (lihat NB09/NB10, Section eksperimen SMOTE).
- **Dimensionality Reduction:** Tidak diterapkan — jumlah fitur sudah minim dan VIF/korelasi antar fitur rendah, sekaligus mempertahankan interpretability klinis.

Detail lengkap justifikasi tiap keputusan tersedia di folder [`notes/`](./notes).

---

## Hasil Akhir

| Model | Threshold | Recall | Precision | F1-Score |
|---|---|---|---|---|
| Random Forest | 0,2 | 63,27% | 17,42% | 0,2731 |
| **Logistic Regression** | 0,6 | **81,63%** | 17,54% | **0,2888** |

**Logistic Regression direkomendasikan sebagai model utama** — Recall tertinggi dengan interpretability lewat Odds Ratio.

### Pembuktian Dampak Preprocessing

Perbandingan dengan model baseline (data mentah, tanpa preprocessing, algoritma identik) pada NB11 membuktikan preprocessing meningkatkan **Recall dari 0% menjadi 63–82%** — mengonfirmasi bahwa preprocessing yang cermat adalah faktor penentu utama, bukan sekadar formalitas.

---

## Cara Menjalankan

### 1. Setup environment
```bash
python -m venv .venv
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

### 2. Jalankan notebook
Buka folder `notebooks/` di VS Code/Jupyter, jalankan urut dari `01_Data_Understanding.ipynb` sampai `11_Evaluation_Comparison.ipynb`.

### 3. Jalankan demo interaktif
```bash
python -m streamlit run app.py
```
Aplikasi akan terbuka di `localhost:8501` — pilih model, isi data pasien, dan lihat hasil prediksi risiko stroke secara langsung.

> Demo ini bersifat akademik, bukan alat diagnosis medis.

---

## Catatan

Proyek ini menekankan **argumentasi eksplisit** pada setiap keputusan preprocessing — termasuk keputusan untuk *tidak* menerapkan suatu teknik — sesuai arahan tugas. Setiap notebook menyertakan bagian *Tujuan* dan *Insight* pada tiap section untuk transparansi proses.
