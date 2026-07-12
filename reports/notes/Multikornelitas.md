# Notes: Kenapa Multikolinearitas Perlu Dicek untuk Logistic Regression, Tidak untuk Random Forest

## Apa itu Multikolinearitas

Kondisi di mana satu fitur bisa "ditebak" dari kombinasi fitur lain — artinya fitur-fitur tersebut membawa informasi yang tumpang tindih (redundan), bukan masing-masing membawa informasi unik.

---

## Kenapa Logistic Regression Sensitif terhadap Ini

Logistic Regression bekerja dengan memberi **satu koefisien pasti** untuk tiap fitur, dengan asumsi *"seandainya semua fitur lain tetap/konstan, seberapa besar pengaruh fitur ini?"*.

**Analogi:** bayangin mau ngukur pengaruh "jam belajar" dan "jumlah halaman dibaca" terhadap nilai ujian — tapi dua hal ini **selalu bergerak bareng** (makin lama belajar, makin banyak halaman dibaca). Model jadi bingung: apakah nilai naik karena jam belajarnya, atau karena halaman yang dibaca? Karena keduanya nggak pernah "terpisah" di data, model **tidak bisa membedakan** kontribusi masing-masing secara meyakinkan.

**Konsekuensi konkret kalau tetap dipaksakan:**
- Koefisien jadi tidak stabil — bisa berubah drastis (bahkan berbalik tanda, dari positif jadi negatif) hanya karena sedikit perubahan data.
- Standard error koefisien membesar, membuat kesimpulan "signifikan/tidak signifikan" jadi tidak dapat dipercaya.
- Interpretasi seperti *"tiap kenaikan 1 unit BMI meningkatkan risiko stroke sebesar X"* jadi tidak valid, karena X yang dihasilkan bisa sangat menyesatkan.

Ini alasan kenapa Section 8 NB10 (Interpretasi Koefisien) baru bisa dipercaya **setelah** dipastikan tidak ada multikolinearitas signifikan — kalau tidak dicek dulu, interpretasi koefisien berisiko keliru.

---

## Kenapa Random Forest TIDAK Memerlukan Pengecekan Ini

Random Forest bekerja dengan cara yang fundamental berbeda — dia tidak pernah mencoba memberi "satu angka pengaruh pasti" untuk tiap fitur secara simultan.

**Analogi:** RF itu kayak serangkaian pertanyaan ya/tidak berurutan — *"Umur di atas 50? → cek glukosa dulu → di atas 150? → ..."*. Di tiap titik keputusan (split), pohon cuma **memilih fitur mana yang paling berguna saat itu**, tanpa perlu tahu "seberapa besar pengaruh murni" fitur itu sambil menganggap fitur lain konstan. Kalau ada 2 fitur yang mirip informasinya, pohon cukup pakai salah satunya di satu titik, dan mungkin pakai yang lain di titik berbeda — tidak ada proses "isolasi pengaruh" yang bisa rusak akibat korelasi antar fitur.

**Kesimpulan:** RF secara struktural kebal terhadap multikolinearitas — prediksi dan feature importance-nya tetap valid meski ada fitur yang saling berkorelasi tinggi. Ini sebabnya NB09 tidak memerlukan tahap pengecekan VIF, sementara NB10 memerlukannya.

---

## VIF (Variance Inflation Factor) — Cara Kerja & Interpretasi

VIF mengukur: *"seberapa bisa fitur ini ditebak dari KOMBINASI seluruh fitur lain sekaligus"* — berbeda dari correlation matrix (NB06) yang cuma bisa melihat hubungan 2 fitur pada satu waktu.

### Skala Interpretasi

| VIF | Artinya |
|---|---|
| ~1 | Nyaris tidak ada korelasi dengan fitur lain |
| 1–5 | Korelasi moderat, umumnya masih aman |
| 5–10 | Mulai mengkhawatirkan |
| >10 | Multikolinearitas parah, bermasalah |

### Hasil Aktual (NB10, Section 2)

| Fitur | VIF | Kategori |
|---|---|---|
| smoking_status_never smoked | 1,58 | Aman |
| smoking_status_formerly smoked | 1,51 | Aman |
| age | 1,44 | Aman |
| smoking_status_smokes | 1,38 | Aman |
| bmi | 1,16 | Aman |
| hypertension | 1,10 | Aman |
| heart_disease | 1,10 | Aman |
| avg_glucose_level | 1,09 | Aman |

Seluruh nilai berada di rentang 1,09–1,58 — jauh di bawah ambang batas 5. Hasil ini konsisten dengan correlation matrix pada NB06 (korelasi tertinggi hanya ~0,32), dan sekaligus memvalidasi ulang keputusan NB05 untuk membuang `ever_married` dan `work_type` karena berpotensi menjadi proxy dari `age` — terbukti VIF `age` tetap rendah (1,44) setelah kedua fitur tersebut dihilangkan.

---