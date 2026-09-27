# Threads Galigo Bot

Bot otomatis untuk mempublikasikan kisah epos **Sureq Galigo (La Galigo)** ke media sosial **Threads** secara berkala dan berurutan. Proyek ini dilengkapi kecerdasan buatan Gemini API, penundaan waktu acak (human jitter), dan penjadwalan GitHub Actions otomatis.

---

## Fitur Utama

1. **Narasi Berantai (Thread Series)**:
   - Episode dipecah menjadi 8 hingga 9 bagian (parts).
   - Part 1 berfungsi sebagai hook pembuka dengan petunjuk kelanjutan.
   - Part 2 s/d Part 8/9 diposting secara berurutan sebagai reply berantai di Threads.
   - Part terakhir dilengkapi Call to Action (CTA) interaktif untuk memicu diskusi pembaca.
   - Setiap part dijamin di bawah 450 karakter (batas aman Threads adalah 500 karakter).
   - Penulisan naskah bebas dari tanda em-dash dan kata klise AI, menjaga kewibawaan tutur lisan Bugis-Makassar.

2. **Human Jitter (0-9 Menit)**:
   - Sebelum posting dieksekusi, bot menunda waktu secara acak antara 0 hingga 540 detik (0 sampai 9 menit).
   - Menghindari kecurigaan algoritma spam dan bot karena jam posting selalu bervariasi (contoh: 07:02 hari ini, 07:08 esok hari).

3. **Penjadwalan Otomatis (GitHub Actions Cron)**:
   - Terjadwal otomatis 3 kali sehari pada waktu Indonesia Tengah (WITA / UTC+8):
     - Pagi: 07:00 WITA (23:00 UTC)
     - Siang: 12:00 WITA (04:00 UTC)
     - Malam: 20:00 WITA (12:00 UTC)
   - State pelacakan urutan (`state.json`) otomatis di-commit dan di-push kembali ke repositori sehingga urutan episode tidak pernah berulang atau terputus.

4. **Gemini API Integration**:
   - Menghasilkan episode baru otomatis jika stok cerita di `episodes.json` telah selesai diposting.

---

## Struktur Berkas

```
threads-galigo-bot/
├── .github/
│   └── workflows/
│       └── autopost.yml       # Jadwal cron GitHub Actions
├── bot.py                     # Skrip utama auto-post Threads + Gemini
├── episodes.json              # Bank naskah cerita Sureq Galigo (8-9 parts)
├── state.json                 # Penyimpan posisi episode terakhir
├── requirements.txt           # Dependensi Python
├── .env.example               # Contoh konfigurasi environment
└── README.md                  # Dokumentasi proyek
```

---

## Konfigurasi GitHub Secrets

Agar GitHub Actions dapat berjalan otomatis, tambahkan secrets berikut di menu repositori GitHub:
**Settings** > **Secrets and variables** > **Actions** > **New repository secret**:

1. `THREADS_USER_ID`: ID akun Threads pengguna Meta.
2. `THREADS_ACCESS_TOKEN`: Token akses panjang (Long-lived User Token) dari Threads API.
3. `GEMINI_API_KEY`: API Key dari Google AI Studio (opsional untuk auto-generate cerita baru).

Pastikan juga permission workflow diaktifkan untuk menulis repo:
**Settings** > **Actions** > **General** > **Workflow permissions** > pilih **Read and write permissions**.

---

## Uji Coba Lokal

1. Salin konfigurasi environment:
   ```bash
   cp .env.example .env
   ```

2. Jalankan simulasi (dry-run) tanpa mengirim ke Threads:
   ```bash
   python bot.py --dry-run --no-jitter
   ```

3. Jalankan posting episode tertentu:
   ```bash
   python bot.py --force-episode 1 --no-jitter
   ```
