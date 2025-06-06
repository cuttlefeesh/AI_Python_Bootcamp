import streamlit as st
import pandas as pd
import datetime
import torch
import librosa
# speech_recognition tidak diperlukan lagi untuk input mikrofon di Streamlit Cloud
# import speech_recognition as sr
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import os
from audio_recorder_streamlit import audio_recorder

# Menonaktifkan tokenizers parallelism untuk mencegah warning pada beberapa deployment environment
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# === Memuat model dan processor Whisper dari Hugging Face ===
@st.cache_resource
def load_whisper_model():
    """Memuat model dan processor Whisper dari Hugging Face."""
    try:
        processor = AutoProcessor.from_pretrained(
            "openai/whisper-small",
            cache_dir="./model_cache" # Cache model secara lokal
        )
        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            "openai/whisper-small",
            cache_dir="./model_cache",
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            low_cpu_mem_usage=True,
            use_safetensors=True
        )
        return processor, model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None, None

# Load model dan processor secara global saat aplikasi dimulai
processor, model = load_whisper_model()

# === Fungsi Pengenalan Suara Menggunakan Model Whisper yang Dimuat ===
def recognize_speech_from_whisper(audio_file_path):
    """
    Mengenali suara dari file audio menggunakan model Whisper yang sudah dimuat.
    Mengembalikan transkripsi teks.
    """
    try:
        if processor is None or model is None:
            return "Error: Model tidak dapat dimuat"

        # Load audio dan pastikan sample rate 16000 Hz
        try:
            audio_input, sample_rate = librosa.load(audio_file_path, sr=16000)
        except Exception as e:
            st.error(f"Error loading audio: {str(e)}")
            return "Error: Tidak dapat memproses file audio"

        # Proses audio menggunakan processor Whisper
        inputs = processor(audio_input, sampling_rate=16000, return_tensors="pt")

        # Pastikan input_features ada atau gunakan kunci pertama yang valid
        with torch.no_grad():
            if "input_features" in inputs:
                generated_ids = model.generate(
                    inputs["input_features"],
                    max_length=448, # Batasi panjang output untuk efisiensi
                    num_beams=1,
                    do_sample=False
                )
            else:
                first_key = list(inputs.keys())[0]
                generated_ids = model.generate(
                    inputs[first_key],
                    max_length=448,
                    num_beams=1,
                    do_sample=False
                )

        # Decode hasil transkripsi
        transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return transcription

    except Exception as e:
        st.error(f"Error in speech recognition: {str(e)}")
        return "Maaf, tidak dapat mengenali suara. Silakan coba lagi."

# === Fungsi untuk memproses teks pesanan dan menambahkannya ke pesanan ===
def process_order_text(text):
    """
    Mengekstrak item dan jumlah dari teks pesanan.
    Mengembalikan dictionary dengan nama item sebagai kunci dan jumlah sebagai nilai.
    """
    import re

    # Dictionary untuk konversi angka dalam bahasa Indonesia/Inggris ke digit
    number_words = {
        'satu': 1, 'dua': 2, 'tiga': 3, 'empat': 4, 'lima': 5,
        'enam': 6, 'tujuh': 7, 'delapan': 8, 'sembilan': 9, 'sepuluh': 10,
        'sebelas': 11, 'dua belas': 12, 'tiga belas': 13, 'empat belas': 14, 'lima belas': 15,
        'enam belas': 16, 'tujuh belas': 17, 'delapan belas': 18, 'sembilan belas': 19, 'dua puluh': 20,
        'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
        'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15,
        'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20
    }

    def extract_quantity_and_item(text_segment, item_keywords):
        """Ekstrak jumlah dan item dari segmen teks."""
        text_segment = text_segment.lower()
        quantity = 0 # Default ke 0, akan diset ke 1 jika keyword ditemukan tanpa angka spesifik

        # Coba cocokkan keyword dan ekstrak angka di sekitarnya
        for keyword in item_keywords:
            # Pola: angka (digit atau kata) + item (contoh: "3 burger", "tiga burger")
            pattern1 = r'(\d+|' + '|'.join(number_words.keys()) + r')\s+(' + re.escape(keyword) + r')'
            match1 = re.search(pattern1, text_segment)

            # Pola: item + angka (contoh: "burger 3", "burger tiga")
            pattern2 = r'(' + re.escape(keyword) + r')\s+(\d+|' + '|'.join(number_words.keys()) + r')'
            match2 = re.search(pattern2, text_segment)

            # Pola: "mau 3 burger", "pesan satu cola"
            pattern3 = r'(?:mau|pesan|ingin|order)\s+(\d+|' + '|'.join(number_words.keys()) + r')?\s*(' + re.escape(keyword) + r')'
            match3 = re.search(pattern3, text_segment)
            
            # Pola: hanya item tanpa angka eksplisit (default quantity 1)
            pattern_only_item = r'\b' + re.escape(keyword) + r'\b'
            match_only_item = re.search(pattern_only_item, text_segment)

            if match1:
                qty_str = match1.group(1)
                if qty_str.isdigit():
                    quantity = int(qty_str)
                else:
                    quantity = number_words.get(qty_str, 1) # Fallback ke 1 jika kata angka tidak dikenal
                return max(1, quantity) # Minimal 1
            elif match2:
                qty_str = match2.group(2)
                if qty_str.isdigit():
                    quantity = int(qty_str)
                else:
                    quantity = number_words.get(qty_str, 1)
                return max(1, quantity)
            elif match3:
                qty_str = match3.group(1)
                if qty_str: # Jika angka ditemukan di pola ini
                    if qty_str.isdigit():
                        quantity = int(qty_str)
                    else:
                        quantity = number_words.get(qty_str, 1)
                else: # Jika tidak ada angka eksplisit, berarti default 1
                    quantity = 1
                return max(1, quantity)
            elif match_only_item:
                # Jika hanya itemnya yang disebut tanpa angka, default 1
                quantity = 1
                return max(1, quantity)
        return 0 # Item tidak ditemukan atau tidak ada kuantitas yang terdeteksi

    # Dictionary item dengan keywords yang mungkin diucapkan
    # Keywords harus dalam urutan spesifik ke umum atau diuji dengan hati-hati
    items_config = {
        "burger": ["burger", "hamburger"],
        "ayam goreng": ["ayam goreng", "ayam", "fried chicken"],
        "kentang goreng": ["kentang goreng", "kentang", "french fries", "fries"],
        "hot dog": ["hot dog", "hotdog", "sosis"],
        "cola": ["cola", "kola", "pepsi", "soda"],
        "mineral water": ["mineral water", "air mineral", "air", "water"],
        "es krim": ["es krim", "ice cream", "eskrim"]
    }

    found_items = {}
    remaining_text = text.lower()

    # Iterasi melalui setiap item yang mungkin dan ekstrak kuantitasnya
    for item_name, keywords in items_config.items():
        # Buat regex pattern untuk mencari item dan kuantitasnya secara berulang
        # Ini adalah tantangan karena satu baris teks bisa punya banyak item
        # Untuk simplicity, kita akan memproses seluruh teks untuk setiap item
        # dan memastikan kita tidak menghitung satu bagian teks berkali-kali.

        # Pendekatan yang lebih sederhana:
        # Coba ekstrak kuantitas untuk setiap item.
        # Jika satu item disebutkan beberapa kali (misal: "dua burger satu burger lagi"),
        # ini mungkin hanya menangkap yang pertama atau paling dominan.
        # Untuk penanganan yang lebih canggih, butuh stateful parsing atau NLU yang lebih kuat.
        quantity = extract_quantity_and_item(remaining_text, keywords)
        if quantity > 0:
            found_items[item_name] = found_items.get(item_name, 0) + quantity # Tambahkan jika sudah ada

            # (Opsional) Hapus bagian yang sudah dikenali dari teks untuk mencegah double counting
            # Ini akan menjadi kompleks jika ada banyak item di satu kalimat
            # Example: "saya mau dua burger dan satu cola"
            # Jika "burger" dikenali, bagian "dua burger" bisa dihapus agar "cola" bisa dikenali dengan baik
            # Tapi untuk kasus sederhana, mungkin tidak perlu terlalu kompleks.

    return found_items

# === OOP Menu Item ===
class MenuItem:
    """Representasi satu item menu."""
    def __init__(self, name, price):
        self.name = name
        self.price = price

# === OOP Order Logic ===
class Order:
    """Mengelola pesanan, termasuk menambah, menghapus, dan menghitung total."""
    def __init__(self):
        self.items = []
        self.payment_method = None

    def add_item(self, menu_item, quantity):
        """Menambahkan item ke pesanan atau memperbarui jumlahnya jika sudah ada."""
        if quantity > 0:
            for item in self.items:
                if item["Menu"] == menu_item.name:
                    item["Jumlah"] += quantity
                    item["Subtotal"] = item["Harga"] * item["Jumlah"]
                    return
            self.items.append({
                "Menu": menu_item.name,
                "Harga": menu_item.price,
                "Jumlah": quantity,
                "Subtotal": menu_item.price * quantity
            })

    def remove_item(self, index):
        """Hapus item berdasarkan index."""
        if 0 <= index < len(self.items):
            self.items.pop(index)

    def update_item_quantity(self, index, new_quantity):
        """Update jumlah item berdasarkan index."""
        if 0 <= index < len(self.items):
            if new_quantity <= 0:
                self.remove_item(index)
            else:
                self.items[index]["Jumlah"] = new_quantity
                self.items[index]["Subtotal"] = self.items[index]["Harga"] * new_quantity

    def clear_empty_items(self):
        """Hapus item dengan jumlah 0 (jika ada, meskipun update_item_quantity sudah menanganinya)."""
        self.items = [item for item in self.items if item["Jumlah"] > 0]

    def get_order_df(self):
        """Mengembalikan pesanan sebagai DataFrame Pandas."""
        return pd.DataFrame(self.items) if self.items else pd.DataFrame(columns=["Menu", "Harga", "Jumlah", "Subtotal"])

    def get_total(self):
        """Menghitung total harga pesanan."""
        return sum(item["Subtotal"] for item in self.items)

    def reset(self):
        """Mereset pesanan ke keadaan kosong."""
        self.items = []
        self.payment_method = None

    def set_payment_method(self, method):
        """Mengatur metode pembayaran."""
        self.payment_method = method

    def generate_receipt(self, uang_diterima=None):
        """Menghasilkan teks struk pembelian."""
        receipt = "=== STRUK PEMBELIAN ===\n"
        for item in self.items:
            receipt += f"{item['Menu']} x{item['Jumlah']} = Rp{item['Subtotal']:,.0f}\n"
        receipt += f"---------------------------\nTotal: Rp{self.get_total():,.0f}\n"
        receipt += f"Metode Bayar: {self.payment_method}\n"

        if uang_diterima is not None:
            if uang_diterima >= self.get_total():
                kembali = uang_diterima - self.get_total()
                receipt += f"Uang Diterima: Rp{uang_diterima:,.0f}\n"
                receipt += f"Uang Kembali: Rp{kembali:,.0f}\n"
            else:
                kekurangan = self.get_total() - uang_diterima
                receipt += f"Uang Diterima: Rp{uang_diterima:,.0f}\n"
                receipt += f"⚠️ Kekurangan: Rp{kekurangan:,.0f}\n"

        receipt += f"Waktu: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        receipt += "===========================\nTerima kasih! 🍽️"
        return receipt

# === Daftar Menu ===
menu_items = [
    MenuItem("🍔 Burger", 25000),
    MenuItem("🍗 Ayam Goreng", 30000),
    MenuItem("🍟 Kentang Goreng", 15000),
    MenuItem("🌭 Hot Dog", 20000),
    MenuItem("🥤 Cola", 10000),
    MenuItem("🥤 Mineral Water", 7000),
    MenuItem("🍦 Es Krim", 12000),
]

# === Streamlit UI ===
st.title("🍔 Mc Ronald Drive-Thru 🍔")

# Inisialisasi session state
if "order" not in st.session_state:
    st.session_state.order = Order()
if "stage" not in st.session_state:
    st.session_state.stage = "ordering"  # ordering, payment, completed
if "last_transcription" not in st.session_state:
    st.session_state.last_transcription = ""
if "uang_diterima_payment_stage" not in st.session_state:
    st.session_state.uang_diterima_payment_stage = 0

# Menampilkan menu dan harga
st.subheader("Menu Mc Ronald")
menu_df = pd.DataFrame([(item.name, f"Rp{item.price:,.0f}") for item in menu_items], columns=["Menu", "Harga"])
st.dataframe(menu_df, use_container_width=True, hide_index=True)

# Sidebar untuk kategori menu
with st.sidebar:
    st.image("https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExdmF6aGw2YWN6am1zZgo4M2RvOHl2bWZlbXRkbTNjcjAzbzgzOHhkYSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/12OoIZRC435JrcFV6z/giphy.gif", caption="Fast Food Logo", width=300)
    st.title("Menu Ingredient")
    category = st.radio("Pilih kategori:", ["Burger", "Ayam Goreng", "Kentang Goreng", "Hotdog", "Cola", "Mineral Water", "Es Krim"])

    # Tambahkan tombol deskripsi di bawah menu ingredient
    category_descriptions = {
        "Burger": "Burger lezat dengan daging sapi pilihan dan sayuran segar.",
        "Ayam Goreng": "Ayam goreng renyah dengan bumbu khas.",
        "Kentang Goreng": "Kentang goreng gurih dan renyah, cocok untuk camilan.",
        "Hotdog": "Hotdog dengan sosis premium dan saus spesial.",
        "Cola": "Minuman cola dingin yang menyegarkan.",
        "Mineral Water": "Air mineral murni untuk melepas dahaga.",
        "Es Krim": "Es krim manis dan dingin membuat fun."
    }

    if st.button("Tampilkan Deskripsi"):
        st.write(f"**Deskripsi:** {category_descriptions[category]}")

# Tambahkan CSS untuk mempercantik aplikasi
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #fffbe7 0%, #ffe5b4 40%, #f6d365 70%, #fda085 100%);
        background-attachment: fixed;
        min-height: 100vh;
    }
    .stTitle, .stHeader, .stSubheader, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #8B4513 !important;
        text-shadow: 2px 2px 8px #ffd70099, 0 2px 8px #fda08566;
    }
    .stButton>button {
        background: linear-gradient(90deg, #ffd700 0%, #f7971e 100%);
        color: #8B4513;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        box-shadow: 0 2px 8px #fda08533;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #f7971e 0%, #ffd700 100%);
    }
    .stSidebar {
        background: #fffbe7;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Tambahkan header dengan gaya khusus
st.markdown('<h1 style="text-align:center; font-size:2rem; font-family:Comic Sans MS, Comic Sans, cursive; color:#8B4513; font-weight:bold; letter-spacing:2px; margin-bottom:0.5em; text-shadow:2px 2px 8px #ffd70099,0 2px 8px #fda08566;">🍔PAYMENT🍔</h1>', unsafe_allow_html=True)

# ---
## Tahap Pemesanan
#---
if st.session_state.stage == "ordering":
    st.subheader("🎤 Pemesanan Suara")

    # Tampilkan pesanan saat ini jika ada
    if st.session_state.order.items:
        st.subheader("Pesanan Saat Ini:")

        # Tampilkan setiap item dengan tombol hapus dan edit
        for idx, item in enumerate(st.session_state.order.items):
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])

            with col1:
                st.write(f"**{item['Menu']}** - Rp{item['Harga']:,.0f} x {item['Jumlah']} = Rp{item['Subtotal']:,.0f}")

            with col2:
                # Tombol kurangi jumlah
                if st.button("➖", key=f"decrease_{idx}", help="Kurangi 1"):
                    if item['Jumlah'] > 1:
                        item['Jumlah'] -= 1
                        item['Subtotal'] = item['Harga'] * item['Jumlah']
                    else:
                        st.session_state.order.items.pop(idx) # Hapus jika jumlah jadi 0
                    st.rerun()

            with col3:
                # Input jumlah langsung
                new_qty = st.number_input(
                    label="",
                    min_value=0,
                    value=item['Jumlah'],
                    key=f"qty_{idx}",
                    label_visibility="collapsed"
                )
                if new_qty != item['Jumlah']:
                    if new_qty == 0:
                        st.session_state.order.items.pop(idx)
                    else:
                        item['Jumlah'] = new_qty
                        item['Subtotal'] = item['Harga'] * item['Jumlah']
                    st.rerun()

            with col4:
                # Tombol tambah jumlah
                if st.button("➕", key=f"increase_{idx}", help="Tambah 1"):
                    item['Jumlah'] += 1
                    item['Subtotal'] = item['Harga'] * item['Jumlah']
                    st.rerun()

            with col5:
                # Tombol hapus item
                if st.button("🗑️", key=f"delete_{idx}", help="Hapus item"):
                    st.session_state.order.items.pop(idx)
                    st.rerun()

        st.divider()
        st.write(f"### **Total: Rp{st.session_state.order.get_total():,.0f}**")

    # Input audio menggunakan st.audio_recorder
    st.info("Tekan tombol 'Rekam Audio' untuk memulai perekaman pesanan Anda.")
    audio_bytes = audio_recorder(
        text="Rekam Audio",
        sampling_rate=16000, # Penting: Whisper butuh 16kHz
        # Pengaturan lain bisa ditambahkan, misal: icon="mic"
    )

    if audio_bytes:
        with st.spinner("🎤 Memproses pesanan dari audio..."):
            try:
                # Simpan audio_bytes ke file sementara
                temp_audio_file = "temp_audio.wav"
                with open(temp_audio_file, "wb") as f:
                    f.write(audio_bytes)

                # Mengenali suara dengan model Whisper
                transcription = recognize_speech_from_whisper(temp_audio_file)
                st.session_state.last_transcription = transcription

                # Hapus file sementara setelah diproses
                if os.path.exists(temp_audio_file):
                    os.remove(temp_audio_file)

                st.success(f"Pesanan yang dikenali: {transcription}")

                # Proses transkripsi untuk menambah item ke pesanan
                items_recognized = process_order_text(transcription)
                if items_recognized:
                    for item_key, qty in items_recognized.items():
                        # Cari item menu yang cocok berdasarkan keywords
                        found_match = False
                        for menu_item in menu_items:
                            # Gunakan item_key yang sudah dinormalisasi dari process_order_text
                            # Jika item_key adalah nama menu yang tepat
                            if item_key.lower() == menu_item.name.replace("🍔 ", "").replace("🍗 ", "").replace("🍟 ", "").replace("🌭 ", "").replace("🥤 ", "").replace("🍦 ", "").lower():
                                st.session_state.order.add_item(menu_item, qty)
                                st.success(f"✅ Menambahkan {qty} x {menu_item.name}")
                                found_match = True
                                break
                        if not found_match:
                            st.warning(f"Item '{item_key}' tidak dikenali dalam menu.")
                else:
                    st.warning("Tidak ada item yang dikenali dari rekaman suara. Silakan coba lagi dengan lebih jelas.")

            except Exception as e:
                st.error(f"Error saat memproses rekaman suara: {str(e)}")


    # Tombol aksi di bawah
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🛒 Lanjut ke Pembayaran", key="payment_button"):
            if st.session_state.order.items:
                st.session_state.stage = "payment"
                st.rerun()
            else:
                st.warning("Pesanan masih kosong! Silakan pesan terlebih dahulu.")

    with col2:
        if st.button("🗑️ Reset Pesanan", key="reset_button"):
            st.session_state.order.reset()
            st.session_state.last_transcription = ""
            st.success("Pesanan direset!")
            st.rerun()

# ---
## Tahap Pembayaran
#---
elif st.session_state.stage == "payment":
    st.subheader("💳 Pembayaran")

    # Tampilkan ringkasan pesanan
    st.subheader("Ringkasan Pesanan:")
    order_df = st.session_state.order.get_order_df()
    st.dataframe(order_df, use_container_width=True, hide_index=True)

    total = st.session_state.order.get_total()
    st.write(f"### **Total: Rp{total:,.0f}**")

    # Input metode pembayaran
    payment_method = st.selectbox("Pilih Metode Pembayaran:", ["Cash", "E-Wallet", "Debit Card"], key="payment_method")
    st.session_state.order.set_payment_method(payment_method)

    # Input jumlah uang yang diterima (hanya untuk Cash)
    if payment_method == "Cash":
        uang_diterima = st.number_input(
            "💵 Masukkan uang diterima (Rp):",
            min_value=0,
            step=1000,
            value=st.session_state.uang_diterima_payment_stage, # Pertahankan nilai dari session state
            key="uang_diterima_input"
        )
        st.session_state.uang_diterima_payment_stage = uang_diterima # Simpan ke session state

        if uang_diterima > 0:
            if uang_diterima >= total:
                kembalian = uang_diterima - total
                st.success(f"✅ Uang kembali: Rp{kembalian:,.0f}")
                payment_complete = True
            else:
                kekurangan = total - uang_diterima
                st.error(f"⚠️ Uang kurang: Rp{kekurangan:,.0f}")
                payment_complete = False
        else:
            payment_complete = False
    else:
        # Untuk E-Wallet dan Debit Card, tidak perlu input uang
        st.info(f"Silakan lakukan pembayaran melalui {payment_method}")
        uang_diterima = total  # Set equal to total for non-cash payments
        st.session_state.uang_diterima_payment_stage = total # Simpan ke session state
        payment_complete = True

    # Tombol aksi
    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Kembali ke Pemesanan", key="back_to_order"):
            st.session_state.stage = "ordering"
            st.rerun()

    with col2:
        if payment_complete and st.button("🖨️ Cetak Struk", key="print_receipt"):
            st.session_state.stage = "completed"
            st.rerun()

# ---
## Tahap Selesai
#---
elif st.session_state.stage == "completed":
    st.subheader("🎉 Pembayaran Berhasil!")

    # Generate dan tampilkan struk
    # Gunakan uang_diterima yang disimpan di session state
    receipt = st.session_state.order.generate_receipt(st.session_state.uang_diterima_payment_stage)
    st.code(receipt, language="text")

    # Tombol untuk pesanan baru
    if st.button("🔄 Pesanan Baru", key="new_order"):
        st.session_state.order.reset()
        st.session_state.stage = "ordering"
        st.session_state.last_transcription = ""
        # Reset uang_diterima_payment_stage
        st.session_state.uang_diterima_payment_stage = 0
        st.rerun()

# Tampilkan transkripsi terakhir jika ada di tahap ordering
if st.session_state.last_transcription and st.session_state.stage == "ordering":
    st.info(f"Transkripsi terakhir: {st.session_state.last_transcription}")
