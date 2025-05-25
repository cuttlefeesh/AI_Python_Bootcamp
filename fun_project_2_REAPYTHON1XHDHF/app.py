import streamlit as st
import requests
import PyPDF2
from docx import Document 

# === Konfigurasi API ===
OPENROUTER_API_KEY = "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"  
MODEL = "openai/gpt-3.5-turbo"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}"
}

# === Judul Aplikasi ===
st.title("📄 AI Chatbot + File (.pdf / .docx)")
st.markdown("Unggah file PDF atau Word, lalu tanyakan apa saja berdasarkan isinya.")

# === Upload File ===
uploaded_file = st.file_uploader("Unggah file (.pdf atau .docx)", type=["pdf", "docx"])
file_text = ""

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        file_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(uploaded_file)
        file_text = "\n".join([para.text for para in doc.paragraphs if para.text.strip() != ""])

    if file_text.strip() == "":
        st.warning("❗ Tidak ada teks terbaca dari file.")
    else:
        st.success("✅ File berhasil dibaca!")
        with st.expander("🔍 Pratinjau isi file"):
            st.text_area("Isi file:", file_text[:3000], height=200)

# === Riwayat Chat ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# === Input dari Pengguna ===
prompt = st.chat_input("Tanyakan sesuatu ...")

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    # === Kirim permintaan ke OpenRouter ===
    context_message = f"Berikut adalah isi file yang diunggah:\n\n{file_text[:4000]}"
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": context_message},
        {"role": "user", "content": prompt}
    ]

    with st.spinner("Mengetik jawaban..."):
        response = requests.post(API_URL, headers=HEADERS, json={"model": MODEL, "messages": messages})

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
    else:
        reply = f"⚠️ Gagal mengambil respons. ({response.status_code}) {response.text}"

    st.chat_message("assistant").markdown(reply)
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
