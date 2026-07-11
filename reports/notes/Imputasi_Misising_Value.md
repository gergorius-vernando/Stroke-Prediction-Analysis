# Dasar Pemilihan Metode Imputasi Missing Value

## `bmi`: Median (bukan Mean)

**Data:** 201 baris missing (~3,9%)

**Bukti dari data:**
| | Nilai |
|---|---|
| Skewness | **1,055** (right-skewed / condong ke kanan) |
| Mean | 28,89 |
| Median | 28,1 |

**Kenapa median dipilih, bukan mean:**

Skewness 1,055 menandakan distribusi tidak simetris — ada sejumlah nilai BMI ekstrem tinggi (representasi obesitas berat) yang "menarik" mean ke atas. Terbukti mean (28,89) lebih tinggi dari median (28,1) — pola khas distribusi right-skewed.

**Analogi:** bayangin di satu ruangan ada 9 orang bergaji 5 juta dan 1 orang bergaji 500 juta. Rata-rata (mean) gaji jadi ~54 juta — angka ini tidak mewakili siapapun di ruangan itu, karena tertarik jauh oleh 1 nilai ekstrem. Median (5 juta) jauh lebih representatif buat "orang tipikal" di data itu.

Kalau mean dipakai buat imputasi, nilai yang diisikan ke 201 baris kosong itu akan **lebih tinggi dari kondisi tipikal pasien sebenarnya** — bias ke atas akibat pengaruh outlier obesitas berat. Median tidak terpengaruh besaran nilai ekstrem (cuma soal urutan/posisi tengah), jadi lebih representatif buat mengisi nilai yang hilang.

---

## `smoking_status`: Mode, dihitung khusus (exclude kategori "Unknown")

**Data:** 173 baris NaN (hasil injeksi simulasi corruption, bersifat **MCAR** — Missing Completely At Random)

**Kenapa Mode (bukan mean/median):**

`smoking_status` itu data kategorikal/nominal (teks: "never smoked", "formerly smoked", dst) — bukan angka. Mean dan median tidak punya makna untuk data seperti ini (tidak ada "rata-rata kategori"). Mode — kategori yang paling sering muncul — satu-satunya ukuran "pusat" yang valid untuk data kategorikal.

**Kenapa mode dihitung dengan MENGECUALIKAN kategori "Unknown":**

Kolom ini punya 2 bentuk "tidak diketahui" yang mekanismenya beda:
- **"Unknown"** (1.544 baris) → **MNAR**, bawaan data asli. Pasien yang *sengaja* tidak mau mengungkapkan status merokoknya.
- **NaN** (173 baris) → **MCAR**, hasil simulasi corruption. Representasi kegagalan sistem/human error saat pencatatan — bukan keputusan pasien.

Kalau mode dihitung dari **seluruh** kolom (termasuk "Unknown"), ada risiko konseptual: NaN (MCAR) bisa keliru terisi jadi "Unknown" — padahal dua kondisi ini sengaja dibedakan sejak NB02 justru karena mekanismenya berbeda. Mengisi NaN dengan "Unknown" berarti mencampur kembali dua jenis missing value yang seharusnya dipisah, dan secara konsep tidak menyelesaikan apa-apa (masih sama-sama "tidak diketahui").

Dengan mengecualikan "Unknown", mode dipaksa jatuh ke salah satu kategori **konkret** (never smoked / formerly smoked / smokes) — sesuai tujuan imputasi MCAR: mengisi dengan tebakan terbaik yang valid, bukan sekadar "tidak diketahui" lagi.

**Hasil:** mode (exclude "Unknown") = **"never smoked"** (1.892 dari 3.566 baris non-Unknown, ±53%)

> **Catatan transparansi:** di dataset ini, "never smoked" (1.892) kebetulan **sudah lebih banyak** dari "Unknown" (1.544) bahkan tanpa exclude — jadi hasil akhirnya sama saja secara kebetulan. Tapi exclude tetap dilakukan sebagai **prinsip metodologis**, bukan bergantung pada kebetulan angka di dataset ini — supaya logikanya tetap benar seandainya di dataset lain "Unknown" yang justru lebih dominan.

---

## Ringkasan prinsip umum (buat referensi ke depan)

| Tipe data | Distribusi | Metode imputasi |
|---|---|---|
| Numerik | Simetris/normal | Mean |
| Numerik | Skewed (miring) | **Median** ← kasus `bmi` |
| Kategorikal | — | **Mode** ← kasus `smoking_status`, dengan pengecualian kategori yang punya makna "tidak diketahui" lain |