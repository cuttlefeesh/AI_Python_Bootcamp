# 🍔 Mc Ronald Drive-Thru - Aplikasi Pemesanan Suara

Aplikasi pemesanan makanan drive-thru dengan teknologi pengenalan suara menggunakan model Whisper AI. Pelanggan dapat memesan makanan dengan berbicara langsung ke sistem.

## 📋 Deskripsi

Mc Ronald Drive-Thru adalah aplikasi berbasis Streamlit yang memungkinkan pelanggan memesan makanan menggunakan perintah suara. Aplikasi ini akan merekam suara pengguna yang berisi menu yang akan dipesan menggunakan `streamlit-audiorec`. Kemudian, audio tersebut disimpan dalam format .wav dan diolah menggunakan teknologi `AI Whisper dari OpenAI` untuk mengenali dan memproses ucapan pelanggan menjadi pesanan makanan.

## ✨ Fitur Utama

- **Pemesanan dengan Suara**: Pelanggan dapat memesan dengan berbicara
- **Pengenalan Suara AI**: Menggunakan model Whisper untuk akurasi tinggi
- **Sistem Pembayaran**: Mendukung Cash, E-Wallet, dan Debit Card
- **Cetak Struk**: Menghasilkan struk pembelian otomatis
- **Antarmuka Mudah**: UI yang user-friendly dengan emoji dan warna

## 🍽️ Menu Tersedia

| Menu | Harga |
|------|-------|
| 🍔 Burger | Rp 25,000 |
| 🍗 Ayam Goreng | Rp 30,000 |
| 🍟 Kentang Goreng | Rp 15,000 |
| 🌭 Hot Dog | Rp 20,000 |
| 🥤 Cola | Rp 10,000 |
| 🥤 Mineral Water | Rp 7,000 |
| 🍦 Es Krim | Rp 12,000 |

## 🛠️ Persyaratan Sistem

### Python Libraries
```
streamlit
pandas
torch
librosa
speechrecognition
transformers
streamlit-audiorec
accelerate
```

### Hardware
- Mikrofon untuk input suara
- Speaker/headphone untuk feedback audio
- Koneksi internet untuk download model Whisper

## 📦 Instalasi

1. **Clone atau download file repository**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```


## 🚀 Cara Menjalankan di Localhost

1. **Buka VS Code**

2. **Navigasi ke folder aplikasi:**
```bash
cd "path/to/your/app"
```

3. **Jalankan aplikasi:**
```bash
streamlit run app.py
```


## 🚀 Cara Menjalankan di Streamlit Cloud
1. **Kunjungi link berikut `https://mcronald.streamlit.app/`**



## 📱 Cara Penggunaan

### 1. Tahap Pemesanan
- Lihat menu yang tersedia di bagian atas
- Klik tombol **Start Recording**
- Ucapkan pesanan Anda, contoh:
  - "Saya mau dua burger dan satu cola"
  - "Pesan tiga ayam goreng"
  - "Mau kentang goreng lima"
- Klik tombol **Stop** untuk menyudahi pesanan
- Sistem akan menampilkan hasil pengenalan suara
- Pesanan akan otomatis ditambahkan ke keranjang

### 2. Tahap Pembayaran
- Klik **🛒 Lanjut ke Pembayaran**
- Pilih metode pembayaran:
  - **Cash**: Masukkan jumlah uang yang diterima
  - **E-Wallet**: Konfirmasi pembayaran digital
  - **Debit Card**: Konfirmasi pembayaran kartu
- Sistem akan hitung kembalian (untuk Cash)

### 3. Mengelola Pesanan

- Tambah jumlah: Klik tombol ➕
- Kurangi jumlah: Klik tombol ➖
- Edit manual: Ubah angka di kolom jumlah
- Hapus item: Klik tombol 🗑️

### 4. Cetak Struk
- Klik **🖨️ Cetak Struk**
- Struk akan ditampilkan dengan detail:
  - Daftar pesanan dan harga
  - Total pembayaran
  - Metode pembayaran
  - Uang kembali (jika ada)
  - Tanggal dan waktu transaksi

## 🎤 Tips Penggunaan Suara

### Format Ucapan yang Dikenali:
- **"Saya mau [jumlah] [nama menu]"**
  - Contoh: "Saya mau dua burger"
- **"Pesan [jumlah] [nama menu]"**
  - Contoh: "Pesan tiga ayam goreng"
- **"[Jumlah] [nama menu]"**
  - Contoh: "Lima kentang goreng"

### Nama Menu yang Dikenali:
- **Burger**: "burger", "hamburger"
- **Ayam Goreng**: "ayam goreng", "ayam", "fried chicken"
- **Kentang Goreng**: "kentang goreng", "kentang", "french fries", "fries"
- **Hot Dog**: "hot dog", "hotdog", "sosis"
- **Cola**: "cola", "kola", "pepsi", "soda"
- **Air Mineral**: "mineral water", "air mineral", "air", "water"
- **Es Krim**: "es krim", "ice cream", "eskrim"

### Angka yang Dikenali (Maks sampai 20) :
- **Bahasa Indonesia**: satu, dua, tiga, empat, lima, dst.
- **Bahasa Inggris**: one, two, three, four, five, dst.
- **Angka**: 1, 2, 3, 4, 5, dst.

## ⚡ Tombol dan Fungsi

| Tombol | Fungsi |
|--------|--------|
| Start Recording | Merekam pesanan |
| Stop | Menghentikan rekaman dan disimpan dalam format .wav |
| Reset | Menghapus file audio .wav untuk mengulangi pesanan |
| Download | Mengunduh file audio.wav |
| 🛒 Lanjut ke Pembayaran | Pindah ke tahap pembayaran |
| 🗑️ Reset Pesanan | Menghapus semua pesanan yang telah tercatat |
| ⬅️ Kembali ke Pemesanan | Kembali ke tahap pemesanan |
| ➕ Tambah Jumlah | Menambah kuantitas item pesanan |
| ➖ Kurangi Jumlah | Mengurangi kuantitas item pesanan |
| 🗑️ Hapus Pesanan | Menghapus salah satu item pesanan |
| 🖨️ Cetak Struk | Menghasilkan struk pembelian |
| 🔄 Pesanan Baru | Memulai transaksi baru |

## 🔧 Troubleshooting

### Masalah Umum:

**1. Mikrofon tidak terdeteksi**
```
Error: No microphone found
```
- Pastikan mikrofon terhubung
- Berikan izin akses mikrofon ke browser
- Restart aplikasi

**2. Model Whisper gagal download**
```
Error loading model
```
- Pastikan koneksi internet stabil
- Coba restart aplikasi
- Hapus cache Streamlit: `streamlit cache clear`

**3. Suara tidak dikenali**
```
Tidak ada item yang dikenali
```
- Bicara lebih jelas dan pelan
- Gunakan format ucapan yang benar
- Pastikan tidak ada noise di sekitar
- Coba gunakan nama menu dalam bahasa Indonesia

**4. Aplikasi lambat**
```
Loading model...
```
- Model Whisper akan didownload saat pertama kali (±100MB)
- Proses selanjutnya akan lebih cepat
- Gunakan koneksi internet yang stabil

**Selamat menggunakan Mc Ronald Drive-Thru! 🍔🚗**
---
**Regards : Chandra and Mita**
