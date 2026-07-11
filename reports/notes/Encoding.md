# Encoding Variabel Kategorikal

## Ringkasan Cepat

| Variabel | Perlu encoding? | Digunakan di | Jenis encoding |
|---|---|---|---|
| `smoking_status` | ✅ Ya | NB05 (analisis) | Label Encoding |
| `smoking_status` | ✅ Ya | NB08 (modeling) | **One-Hot Encoding** |
| `hypertension` | ❌ Tidak | — | Sudah numerik biner (0/1) |
| `heart_disease` | ❌ Tidak | — | Sudah numerik biner (0/1) |
| `age`, `avg_glucose_level`, `bmi` | ❌ Tidak | — | Sudah numerik kontinu |

Dari 6 fitur final hasil feature selection, **hanya `smoking_status`** yang berbentuk teks/kategori — 5 fitur lainnya sudah dalam bentuk angka sejak awal, sehingga tidak memerlukan proses encoding apapun.

---

## Kenapa `smoking_status` di-encode DUA KALI dengan metode berbeda?

Ini bukan pengulangan yang keliru — dua proses encoding ini punya **tujuan berbeda**, di tahap berbeda:

### 1. Label Encoding (NB05 — Feature Selection)

**Kapan dipakai:** Section 2 (Persiapan Encoding), khusus untuk keperluan analisis Random Forest Importance dan Mutual Information.

**Cara kerja:** 1 kolom, kategori diubah jadi angka urut — misal `never smoked=0`, `formerly smoked=1`, `smokes=2`, `Unknown=3`.

**Kenapa cukup Label Encoding di tahap ini:** Random Forest dan Mutual Information bekerja dengan cara "memecah" data berdasarkan **ambang/threshold**, bukan berdasarkan jarak/skala angka. Kedua metode ini tidak peduli apakah angka 0,1,2,3 punya urutan yang bermakna atau tidak — jadi Label Encoding aman dipakai murni untuk keperluan pengujian statistik, tanpa risiko menyesatkan hasil analisis.

### 2. One-Hot Encoding (NB08 — Data Preparation for Modeling)

**Kapan dipakai:** Section 2, sebagai persiapan final sebelum data masuk ke Random Forest (NB09) dan Logistic Regression (NB10).

**Cara kerja:** 1 kolom kategorikal dipecah jadi beberapa kolom biner terpisah. `smoking_status` (4 kategori) menjadi 3 kolom dummy (`smoking_status_formerly smoked`, `smoking_status_never smoked`, `smoking_status_smokes`) — 1 kategori (`Unknown`) sengaja dijadikan baseline implisit lewat parameter `drop_first=True`.

**Kenapa harus ganti ke One-Hot di tahap ini:**

`smoking_status` adalah data **nominal** (kategori tanpa urutan alami) — "smokes" secara konsep tidak "lebih besar" atau "lebih kecil" dari "never smoked". Masalahnya, kalau Label Encoding (0,1,2,3) tetap dipakai untuk modeling:

- **Logistic Regression** akan salah mengartikan urutan angka itu sebagai skala kuantitatif yang bermakna — model bisa menyimpulkan "smokes (kode 2) pengaruhnya 2x lebih besar dari formerly smoked (kode 1)", padahal itu cuma nomor urut sembarang hasil alfabetis, tidak merepresentasikan hubungan matematis apapun.
- **Random Forest** sebenarnya relatif aman dari masalah ini (karena cara kerjanya berbasis threshold, sama seperti alasan di NB05), tapi karena dataset yang sama dipakai untuk **dua model sekaligus** (RF dan LR), One-Hot Encoding dipilih sebagai pendekatan yang aman untuk keduanya — daripada membuat 2 versi encoding terpisah untuk 2 model yang berbeda.

### Kenapa `drop_first=True` (bukan bikin kolom untuk semua 4 kategori)

Ini mencegah **dummy variable trap** — kondisi di mana kolom-kolom dummy hasil one-hot saling collinear sempurna (kalau nilai 3 kolom sudah diketahui, kolom ke-4 otomatis bisa ditebak, karena totalnya harus salah satu kategori). Ini bisa membuat Logistic Regression error atau menghasilkan koefisien yang tidak stabil. Dengan `drop_first=True`, 1 kategori dijadikan baseline pembanding secara implisit, dan sisanya diinterpretasikan relatif terhadap baseline itu.

---

## Prinsip umum (untuk referensi ke depan)

| Situasi | Metode encoding yang tepat |
|---|---|
| Kategori tanpa urutan alami (nominal), untuk modeling — khususnya Logistic Regression / model linear | **One-Hot Encoding** |
| Kategori tanpa urutan alami, tapi cuma untuk model berbasis pohon (Random Forest, Decision Tree) atau uji statistik non-parametrik | Label Encoding cukup aman |
| Kategori dengan urutan alami (ordinal), misal "rendah/sedang/tinggi" | Ordinal Encoding (angka urut sesuai makna aslinya, bukan alfabetis) |