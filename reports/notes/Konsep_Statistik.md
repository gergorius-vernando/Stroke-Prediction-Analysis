# Konsep Statistik — Proyek Stroke Prediction

Dua topik ini kelihatan mirip (sama-sama statistik) tapi dipakai untuk **tujuan berbeda**:
- **Feature Selection** (NB05) → mutusin fitur mana yang dipakai model
- **Evaluasi Model** (NB04, NB09-11) → mutusin apakah model-nya bagus atau nggak

---

## BAGIAN 1: Feature Selection

### p-value — "seberapa mungkin ini cuma kebetulan?"

> p-value = peluang pola yang kita lihat di data itu muncul **murni karena kebetulan**, KALAU seandainya sebenarnya tidak ada hubungan sama sekali.

**Aturan:** p < 0,05 → terlalu kecil buat dianggap kebetulan → **signifikan** (kemungkinan besar hubungannya nyata)

| Fitur | p-value | Artinya |
|---|---|---|
| `hypertension` | ≈0,000000 | Hampir mustahil ini kebetulan → **signifikan** |
| `gender` | 0,449 | Peluang kebetulan masih 44,9% → **tidak signifikan** |

### Chi-square & U-stat — cuma "bahan mentah" p-value

Dua angka ini **tidak perlu diartikan sendiri**. Fungsinya cuma jadi bahan hitung buat menghasilkan p-value.

**Aturan baca:** makin besar chi-square (atau makin jauh U-stat dari titik netralnya) → makin kecil p-value → makin kuat bukti hubungannya nyata. Tidak ada angka "besar" yang universal — tergantung ukuran data, jadi jangan dibandingkan mentah-mentah antar dataset lain.

### Proxy / Redundansi — kasus `ever_married`

Fitur bisa **signifikan secara statistik**, TAPI cuma karena "numpang" sinyal dari fitur lain yang lebih kuat.

**Bukti dari data kita:** 0 orang di bawah usia 18 tahun berstatus menikah. Begitu tau usianya di bawah 18, kita **udah pasti tau** `ever_married = "No"` tanpa perlu lihat kolom itu sama sekali — informasinya nyaris sepenuhnya sudah "kebaca" dari `age`.

**Keputusan:** dibuang meski p<0,05, karena informasi tambahannya di luar yang sudah dikasih `age` itu kecil.

---

## BAGIAN 2: Evaluasi Model

### Kenapa accuracy bisa menipu

> Accuracy = (jumlah tebakan benar) ÷ (total tebakan) — rumus ini menyamakan **semua jenis kesalahan**, padahal dampaknya beda jauh di dunia nyata.

**Akar masalahnya:** karena kelas mayoritas (tidak-stroke) = 4.848 dari 5.094 (95%), model yang cuma "jago" nebak kelas mayoritas otomatis dapat skor tinggi — nggak peduli separah apa performanya di kelas minoritas (stroke, cuma 246 orang). Kelas minoritas terlalu kecil buat "menarik turun" accuracy secara berarti.

**Buktinya:** model "malas" (selalu nebak "tidak stroke") dapat accuracy ~95% tanpa belajar apa pun, tapi gagal total (recall 0%) mendeteksi stroke.

### 4 metrik pengganti accuracy

| Metrik | Menjawab pertanyaan | Fokus ke |
|---|---|---|
| **Recall** | Dari semua yang BENERAN stroke, berapa % berhasil ketauan? | Kelas minoritas — paling penting untuk kasus medis |
| **Precision** | Dari semua yang DITEBAK stroke, berapa % beneran stroke? | Seberapa sering model "salah alarm" |
| **F1-Score** | Gabungan recall + precision | Biar model nggak asal nebak "stroke" semua demi kejar recall |
| **Confusion Matrix** | Breakdown lengkap: benar-stroke, benar-tidak, salah-stroke, salah-tidak | Gambaran utuh, nggak ketutupan 1 angka ringkasan |

---

## Kenapa 2 bagian ini penting dipisah

Bagian 1 (feature selection) itu soal **"apa yang dimasukkan ke model"**.
Bagian 2 (evaluasi) itu soal **"gimana cara menilai model setelah jadi"**.

Keduanya sama-sama merespons kondisi dasar dataset ini: **imbalanced** (stroke cuma ~4,8%) dan **butuh kehati-hatian ekstra** karena konteksnya medis — kesalahan Bagian 1 (masukin fitur yang salah) bisa bikin model bias, kesalahan Bagian 2 (salah baca performa) bisa bikin model yang jelek dikira bagus.