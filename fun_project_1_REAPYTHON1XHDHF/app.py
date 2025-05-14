import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Tes Kepribadian", page_icon="🧠")
st.title("🔍 Tes Kepribadian: Introvert, Ekstrovert, atau Ambivert?")
st.write("Jawab 6 pertanyaan berikut untuk mengetahui kecenderungan kepribadianmu!")

# Input nama pengguna
user_name = st.text_input("Masukkan nama kamu terlebih dahulu untuk memulai:")

if user_name:
    # Inisialisasi skor
    scores = {
        "Introvert": 0,
        "Ekstrovert": 0,
        "Ambivert": 0
    }

    # Pertanyaan dan opsi jawaban
    questions = [
        {
            "question": "Apa yang kamu lakukan saat akhir pekan?",
            "options": {
                "Menghabiskan waktu sendirian atau bersama keluarga dekat": "Introvert",
                "Hangout dengan banyak teman": "Ekstrovert",
                "Kadang menyendiri, kadang nongkrong": "Ambivert"
            }
        },
        {
            "question": "Bagaimana kamu mengisi energi?",
            "options": {
                "Dengan menyendiri atau melakukan hobi sendiri": "Introvert",
                "Dengan bertemu banyak orang": "Ekstrovert",
                "Tergantung situasi": "Ambivert"
            }
        },
        {
            "question": "Dalam diskusi kelompok, kamu lebih suka:",
            "options": {
                "Mendengarkan dan bicara jika perlu": "Introvert",
                "Aktif menyampaikan ide-ide": "Ekstrovert",
                "Berbicara jika ada hal penting, tapi juga suka mendengar": "Ambivert"
            }
        },
        {
            "question": "Saat bertemu orang baru:",
            "options": {
                "Canggung dan butuh waktu untuk nyaman": "Introvert",
                "Langsung akrab dan mudah membuka pembicaraan": "Ekstrovert",
                "Tergantung mood dan konteksnya": "Ambivert"
            }
        },
        {
            "question": "Kamu lebih nyaman bekerja:",
            "options": {
                "Sendirian atau dengan sedikit orang": "Introvert",
                "Dalam tim besar yang dinamis": "Ekstrovert",
                "Dalam tim kecil tapi tetap terbuka berdiskusi": "Ambivert"
            }
        },
        {
            "question": "Pilih aktivitas favorit:",
            "options": {
                "Membaca buku atau menonton sendiri": "Introvert",
                "Pergi ke konser atau pesta": "Ekstrovert",
                "Nonton bareng teman dekat atau jalan santai": "Ambivert"
            }
        }
    ]

    # List untuk menyimpan jawaban pengguna
    answers = []

    # Form untuk menjawab pertanyaan
    with st.form("quiz_form"):
        for idx, q in enumerate(questions):
            answer = st.radio(f"{idx+1}. {q['question']}", list(q["options"].keys()), key=idx)
            answers.append(q["options"][answer])
        
        submitted = st.form_submit_button("Lihat Hasil")

    if submitted:
        for result in answers:
            scores[result] += 1

        # Perhitungan skor kepribadian
        skor_tertinggi = max(scores.values())
        kandidat_teratas = [tipe for tipe, skor in scores.items() if skor == skor_tertinggi]

        st.subheader(f"🧠 Hasil Kepribadian {user_name}:")
        # Jika skor di 3 kepribadian sama rata
        if len(kandidat_teratas) == 3:
            st.warning(f"Wah {user_name}, nilai kamu imbang di tiga kepribadian! Coba tes lagi dengan lebih spontan.")
            st.image("https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExMGhkd2xsa2lzdTc5ZTAzenBxY3drYndzOHQ1b3R2NXdxOGZxZjlpbSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/RMZBsdFnax7mo/giphy.gif", width=300)

        # Jika skor di 2 kepribadian sama rata
        elif len(kandidat_teratas) == 2:
            st.warning(f"Wah {user_name}, nilai kamu imbang di dua kepribadian! Coba tes lagi dengan lebih spontan.")
            st.image("https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExMGhkd2xsa2lzdTc5ZTAzenBxY3drYndzOHQ1b3R2NXdxOGZxZjlpbSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/RMZBsdFnax7mo/giphy.gif", width=300)

        # Jika hanya satu kepribadian yang terpilih
        else:
            tipe_terpilih = kandidat_teratas[0]
            if tipe_terpilih == "Introvert":
                st.image("https://media.giphy.com/media/l41lVsYDBC0UVQJCE/giphy.gif", width=300)
                st.success(f"{user_name}, kamu cenderung **Introvert**. Kamu menikmati waktu sendiri dan berpikir mendalam.")

            elif tipe_terpilih == "Ekstrovert":
                st.image("https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif", width=300)
                st.success(f"{user_name}, kamu cenderung **Ekstrovert**. Kamu berenergi di sekitar orang lain dan suka berbicara.")

            elif tipe_terpilih == "Ambivert":
                st.image("https://media.giphy.com/media/uVd5gVHAq63SjtjAOe/giphy.gif", width=300)
                st.success(f"{user_name}, kamu adalah seorang **Ambivert**. Kamu fleksibel dan bisa menyesuaikan diri dengan situasi.")

            # Menampilkan proporsi kepribadian
            if len(kandidat_teratas) == 1:
                st.subheader("📊 Proporsi Kepribadian:")
                labels = ['Introvert', 'Ekstrovert', 'Ambivert']
                sizes = [scores['Introvert'], scores['Ekstrovert'], scores['Ambivert']]

                # Memfilter label kepribadian yang memiliki skor 0
                # Jika ada kepribadian yang distribusinya 0.0%, jangan tampilkan text jenis kepribadian dan distribusinya
                filtered_labels = [label for label, size in zip(labels, sizes) if size > 0]
                filtered_sizes = [size for size in sizes if size > 0]

                if filtered_sizes:  # Only plot if there are non-zero values
                    fig, ax = plt.subplots(figsize=(3, 3))
                    ax.pie(filtered_sizes, labels=filtered_labels, autopct='%1.1f%%', startangle=90, colors=['#FF9999','#66B2FF','#99FF99'])
                    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                    st.pyplot(fig)
else:
    st.info("Silakan masukkan nama terlebih dahulu untuk memulai kuis.")
