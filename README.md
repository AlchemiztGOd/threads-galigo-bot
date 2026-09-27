# Threads Galigo Bot: Serial Lengkap Epos Sureq Galigo

Bot otomatis untuk mempublikasikan **Seluruh Siklus Wiracarita Sureq Galigo (La Galigo)** ke **Threads** secara kronologis, lengkap dari awal penciptaan jagat raya hingga pamitnya para dewata.

Setiap postingan dikemas sebagai satu episode berseri terpadu dengan **gambar ilustrasi artistik klasik**, **penanda pergantian Arc/Babak**, dan narasi bersambung yang mengaitkan jam tayang (Pagi, Siang, Malam).

---

## Struktur 7 Arc Utama Sureq Galigo (28 Episode Lengkap)

Serial ini merangkum naskah asli 300.000 larik daun lontar Bugis kuno ke dalam 7 Arc besar selama 10 hari tayang beruntun:

### 1. Arc 1: Asal-Usul Dewata dan Berdirinya Luwu (Episode 1 - 4)
- **Tanda Arc**: `[ARC 1: ASAL DEWATA]`
- **Jadwal**: Hari 1 Pagi s/d Hari 2 Pagi
- **Sinopsis**: Musyawarah Boting Langiq & Uriq Liu, turunnya Batara Guru beralaskan bambu gading ke Luwu, munculnya We Nyiliq Timo dari buih ombak emas, hingga penegakan hukum adat dan pernikahan agung.

### 2. Arc 2: Kutukan Kembar Emas dan Takdir Terlarang (Episode 5 - 8)
- **Tanda Arc**: `[ARC 2: KUTUKAN KEMBAR EMAS]`
- **Jadwal**: Hari 2 Siang s/d Hari 3 Siang
- **Sinopsis**: Lahirnya kembar emas Sawerigading & We Tenriabeng, ramalan petaka kosmis para Bissu, pemisahan sejak bayi, hingga terbukanya tirai sutra emas di istana Luwu.

### 3. Arc 3: Penebangan Pohon Keramat dan Bahtera Maut (Episode 9 - 13)
- **Tanda Arc**: `[ARC 3: BAHARU & SAMUDRA]`
- **Jadwal**: Hari 3 Malam s/d Hari 5 Pagi
- **Sinopsis**: Siasat We Tenriabeng menunjuk Tana Kelling, penebangan pohon purba Welenrengnge, pecahnya telur garuda dan air bah, pembuatan bahtera Wakka Pasompe, serta sumpah pantang kembali ke tanah Luwu.

### 4. Arc 4: Samudra Berdarah dan Penaklukan Tana Kelling (Episode 14 - 17)
- **Tanda Arc**: `[ARC 4: PERANG DI KELLING]`
- **Jadwal**: Hari 5 Siang s/d Hari 6 Siang
- **Sinopsis**: Menembus kabut beracun dan melawan monster laut, pendaratan armada Luwu di pesisir Kelling, duel ksatria dengan pendekar We Cudai, hingga lahirnya I La Galigo.

### 5. Arc 5: Petualangan Liar Sang Pewaris I La Galigo (Episode 18 - 21)
- **Tanda Arc**: `[ARC 5: SANG PEWARIS GALIGO]`
- **Jadwal**: Hari 6 Malam s/d Hari 7 Malam
- **Sinopsis**: Jiwa merdeka dan pembangkang I La Galigo, arena sabung ayam legendaris di Sunra & Wajo dengan ayam jago Bakka Lolona, penjelajahan asmara, penulisan syair lontar, dan kelahiran sang cucu La Tenritatta.

### 6. Arc 6: Perjalanan Terakhir dan Tenggelamnya Bahtera (Episode 22 - 25)
- **Tanda Arc**: `[ARC 6: SAMUDRA TERAKHIR]`
- **Jadwal**: Hari 8 Pagi s/d Hari 9 Pagi
- **Sinopsis**: Kerinduan tua Sawerigading menatap bukit Luwu, pertemuan rahasia di atas teluk Bone tanpa menginjak daratan, bangkitnya badai kosmis, dan tenggelamnya Wakka Pasompe ke dasar samudra Uriq Liu.

### 7. Arc 7: Kembalinya Para Dewata dan Penutupan Epos (Episode 26 - 28)
- **Tanda Arc**: `[ARC 7: AKHIR ZAMAN DEWATA]`
- **Jadwal**: Hari 9 Siang s/d Hari 10 Pagi
- **Sinopsis**: Takhta abadi Sawerigading di dasar laut dan We Tenriabeng di puncak langit, penobatan raja manusia La Tenritatta di Ale Lino, pamitnya keturunan dewa, serta penutupan epos terpanjang dunia dengan ajakan diskusi publik.

---

## Jadwal Penyiaran Otomatis (WITA / UTC+8)

Cron GitHub Actions terpasang pada jam:
- **Pagi: 07:00 WITA** (23:00 UTC)
- **Siang: 12:00 WITA** (04:00 UTC)
- **Malam: 20:00 WITA** (12:00 UTC)

### Human Jitter (0-9 Menit)
Di setiap jadwal cron, `bot.py` otomatis menunda pengunggahan antara 0 hingga 540 detik secara acak agar waktu posting tidak statis dan tidak terbaca oleh sistem deteksi bot.

---

## Kepatuhan Aturan Penulisan (Antislop Standar)
1. **Batas Karakter**: Seluruh teks episode berada di kisaran 310 hingga 380 karakter (sangat aman di bawah batas 450 karakter).
2. **Bebas Em-Dash**: Nol em-dash (`—` atau `--`) di seluruh narasi, kode, dan dokumentasi.
3. **Tone Otentik**: Menjunjung kearifan budaya Bugis kuno (*siriq na pesse*, *Dewata Sewwae*, *Bissu*, *Wakka Pasompe*).

---

## Uji Coba Pratinjau Lokal

```bash
# Uji coba mode simulasi tanpa mengunggah
python bot.py --dry-run --no-jitter

# Uji coba episode tertentu (contoh: Episode 5 awal Arc 2)
python bot.py --force-episode 5 --dry-run --no-jitter
```
