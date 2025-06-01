🍔 Mc Ronald Drive-Thru - Aplikasi Pemesanan Suara
Aplikasi pemesanan makanan drive-thru dengan teknologi pengenalan suara menggunakan model Whisper AI. Pelanggan dapat memesan makanan dengan berbicara langsung ke sistem.
📋 Deskripsi
Mc Ronald Drive-Thru adalah aplikasi berbasis Streamlit yang memungkinkan pelanggan memesan makanan menggunakan perintah suara. Aplikasi ini menggunakan teknologi AI Whisper dari OpenAI untuk mengenali dan memproses ucapan pelanggan menjadi pesanan makanan.
✨ Fitur Utama

Pemesanan dengan Suara: Pelanggan dapat memesan dengan berbicara
Pengenalan Suara AI: Menggunakan model Whisper untuk akurasi tinggi
Manajemen Pesanan: Tambah, kurangi, atau hapus item pesanan
Sistem Pembayaran: Mendukung Cash, E-Wallet, dan Debit Card
Cetak Struk: Menghasilkan struk pembelian otomatis
Antarmuka Mudah: UI yang user-friendly dengan emoji dan warna

🍽️ Menu Tersedia
MenuHarga🍔 BurgerRp 25,000🍗 Ayam GorengRp 30,000🍟 Kentang GorengRp 15,000🌭 Hot DogRp 20,000🥤 ColaRp 10,000🥤 Mineral WaterRp 7,000🍦 Es KrimRp 12,000
🛠️ Persyaratan Sistem
Python Libraries
streamlit
pandas
torch
librosa
soundfile
speech_recognition
transformers
Hardware

Mikrofon untuk input suara
Speaker/headphone untuk feedback audio
Koneksi internet untuk download model Whisper

📦 Instalasi

Clone atau download file voice.py
Install dependencies:

bashpip install streamlit pandas torch librosa soundfile speechrecognition transformers

Install PyAudio untuk mikrofon (Windows):

bashpip install pyaudio
Untuk Linux/Mac:
bash# Ubuntu/Debian
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio

# MacOS
brew install portaudio
pip install pyaudio
🚀 Cara Menjalankan

Buka terminal/command prompt
Navigasi ke folder aplikasi:

bashcd path/to/your/app

Jalankan aplikasi:

bashstreamlit run voice.py

Buka browser dan akses http://localhost:8501

📱 Cara Penggunaan
1. Tahap Pemesanan

Lihat menu yang tersedia di bagian atas
Klik tombol 🎤 Mulai Bicara
Ucapkan pesanan Anda, contoh:

"Saya mau dua burger dan satu cola"
"Pesan tiga ayam goreng"
"Mau kentang goreng lima"


Sistem akan menampilkan hasil pengenalan suara
Pesanan akan otomatis ditambahkan ke keranjang

2. Mengelola Pesanan

Tambah jumlah: Klik tombol ➕
Kurangi jumlah: Klik tombol ➖
Edit langsung: Ubah angka di kolom Qty
Hapus item: Klik tombol 🗑️

3. Tahap Pembayaran

Klik 🛒 Lanjut ke Pembayaran
Pilih metode pembayaran:

Cash: Masukkan jumlah uang yang diterima
E-Wallet: Konfirmasi pembayaran digital
Debit Card: Konfirmasi pembayaran kartu


Sistem akan hitung kembalian (untuk Cash)

4. Cetak Struk

Klik 🖨️ Cetak Struk
Struk akan ditampilkan dengan detail:

Daftar pesanan dan harga
Total pembayaran
Metode pembayaran
Uang kembali (jika ada)
Tanggal dan waktu transaksi



🎤 Tips Penggunaan Suara
Format Ucapan yang Dikenali:

"Saya mau [jumlah] [nama menu]"

Contoh: "Saya mau dua burger"


"Pesan [jumlah] [nama menu]"

Contoh: "Pesan tiga ayam goreng"


"[Jumlah] [nama menu]"

Contoh: "Lima kentang goreng"



Nama Menu yang Dikenali:

Burger: "burger", "hamburger"
Ayam Goreng: "ayam goreng", "ayam", "fried chicken"
Kentang Goreng: "kentang goreng", "kentang", "french fries", "fries"
Hot Dog: "hot dog", "hotdog", "sosis"
Cola: "cola", "coke", "pepsi", "soda"
Air Mineral: "mineral water", "air mineral", "air", "water"
Es Krim: "es krim", "ice cream", "eskrim"

Angka yang Dikenali:

Bahasa Indonesia: satu, dua, tiga, empat, lima, dst.
Bahasa Inggris: one, two, three, four, five, dst.
Angka: 1, 2, 3, 4, 5, dst.

⚡ Tombol dan Fungsi
TombolFungsi🎤 Mulai BicaraMengaktifkan pengenalan suara➖Mengurangi jumlah item➕Menambah jumlah item🗑️Menghapus item dari pesanan🛒 Lanjut ke PembayaranPindah ke tahap pembayaran🗑️ Reset PesananMenghapus semua pesanan⬅️ Kembali ke PemesananKembali ke tahap pemesanan🖨️ Cetak StrukMenghasilkan struk pembelian🔄 Pesanan BaruMemulai transaksi baru
🔧 Troubleshooting
Masalah Umum:
1. Mikrofon tidak terdeteksi
Error: No microphone found

Pastikan mikrofon terhubung
Berikan izin akses mikrofon ke browser
Restart aplikasi

2. Model Whisper gagal download
Error loading model

Pastikan koneksi internet stabil
Coba restart aplikasi
Hapus cache Streamlit: streamlit cache clear

3. Suara tidak dikenali
Tidak ada item yang dikenali

Bicara lebih jelas dan pelan
Gunakan format ucapan yang benar
Pastikan tidak ada noise di sekitar
Coba gunakan nama menu dalam bahasa Indonesia

4. Aplikasi lambat
Loading model...

Model Whisper akan didownload saat pertama kali (±100MB)
Proses selanjutnya akan lebih cepat
Gunakan koneksi internet yang stabil