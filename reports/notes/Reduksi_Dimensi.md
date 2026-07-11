Kenapa Reduksi Dimensi (PCA) Tidak Diterapkan

## Konteks singkat

PCA (Principal Component Analysis) dan metode reduksi dimensi lain pada dasarnya memadatkan banyak fitur jadi lebih sedikit "komponen" gabungan, biasanya dipakai kalau jumlah fitur terlalu banyak dan/atau saling tumpang tindih (redundan). Keputusan di project ini: **tidak diterapkan**, dengan 3 alasan berikut.

---

## Alasan 1 — Jumlah fitur sudah minim

Dataset final hasil feature selection (NB05) cuma punya **6 fitur** (`age`, `avg_glucose_level`, `bmi`, `hypertension`, `heart_disease`, `smoking_status`). PCA umumnya baru terasa manfaatnya pada dataset dengan puluhan–ratusan fitur, di mana kompleksitas komputasi dan *curse of dimensionality* jadi masalah nyata. Dengan 6 fitur, kondisi itu tidak berlaku.

## Alasan 2 — Tidak ditemukan multikolinearitas signifikan (dibuktikan, bukan diasumsikan)

Salah satu alasan utama orang pakai PCA adalah untuk mengatasi fitur-fitur yang saling redundan. Ini dicek langsung lewat correlation matrix ke-6 fitur final (NB06):

| Pasangan fitur | Korelasi |
|---|---|
| `age` – `bmi` | ~0,32 (tertinggi) |
| Pasangan lainnya | ~0,04 – 0,28 |

**Ambang batas yang umum dianggap "multikolinearitas mengkhawatirkan": >0,7–0,8.** Korelasi tertinggi di data kita (0,32) jauh di bawah itu — artinya fitur-fitur final relatif independen satu sama lain, tidak ada informasi yang "dobel dihitung". Ini bukti empiris, bukan cuma asumsi, bahwa PCA tidak dibutuhkan untuk mengurangi redundansi.

## Alasan 3 — PCA mengorbankan interpretability klinis

PCA mengubah fitur asli jadi kombinasi linear abstrak (komponen utama) yang kehilangan makna aslinya — misalnya, "Komponen 1" hasil PCA bisa jadi campuran 0,4×age + 0,3×bmi + 0,2×glucose, dan tidak lagi bisa langsung diartikan sebagai "usia pasien".

Dalam konteks penelitian kesehatan, kemampuan menjelaskan **fitur spesifik mana** yang berkontribusi terhadap risiko stroke (misal untuk komunikasi ke tenaga medis atau pembahasan klinis) jauh lebih bernilai dibanding sedikit efisiensi komputasi yang ditawarkan PCA — apalagi dengan fitur yang sudah sangat sedikit, efisiensi tersebut nyaris tidak terasa.

---

## Kapan PCA sebenarnya akan relevan (untuk konteks pembanding)

Supaya argumen "tidak perlu" ini kuat, penting juga menyebutkan kapan PCA *akan* jadi pilihan tepat — sebagai pembanding:
- Jumlah fitur sangat banyak (puluhan–ratusan), misalnya data genomik, citra, atau sensor dengan ribuan kolom.
- Ditemukan multikolinearitas tinggi antar banyak fitur (korelasi >0,7–0,8) yang mengganggu stabilitas model seperti Logistic Regression.
- Interpretability bukan prioritas utama (misal untuk sistem rekomendasi umum, bukan riset medis).

Ketiga kondisi ini **tidak berlaku** di project ini, memperkuat keputusan untuk melewati tahap reduksi dimensi.

---

## Kalimat siap pakai untuk paper

```markdown
Reduksi dimensi (PCA) tidak diterapkan pada penelitian ini dengan tiga pertimbangan utama. Pertama, jumlah fitur final setelah proses feature selection hanya enam fitur, sehingga kompleksitas komputasi yang menjadi motivasi utama PCA tidak relevan. Kedua, pengecekan correlation matrix menunjukkan tidak adanya multikolinearitas signifikan antar fitur (korelasi tertinggi 0,32, jauh di bawah ambang batas 0,7-0,8), sehingga tidak ditemukan redundansi informasi yang perlu direduksi. Ketiga, PCA mengubah fitur asli menjadi kombinasi linear yang kehilangan interpretasi klinis langsung, sementara kemampuan menjelaskan kontribusi tiap fitur secara eksplisit merupakan aspek penting dalam penelitian di bidang kesehatan.
```
