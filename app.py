import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="GuruIbu - Asisten Belajar",
    page_icon="👩‍🏫",
    layout="centered"
)

# --- JUDUL & TAMPILAN ---
st.title("👩‍🏫 GuruIbu AI")
st.write("Foto soal PR anak, Bunda dapat penjelasannya + cara ngajarinnya!")
st.write("---")

# --- SETUP API KEY (RAHASIA) ---
# Kita mengambil kunci dari brankas rahasia Streamlit
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("Kunci API belum disetting! Harap masukkan API Key di Streamlit Secrets.")
    st.stop()

# --- FUNGSI GEMINI ---
def tanya_guruibu(image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = """
    Kamu adalah 'GuruIbu', asisten belajar cerdas khusus untuk membantu Ibu-ibu.
    Persona: Sabar, suportif, ceria, dan jago membuat analogi sederhana.

    Tugasmu dari gambar soal ini:
    1. Analisa Soal: Ini materi apa?
    2. Penjelasan untuk Ibu: Jelaskan konsepnya simpel saja.
    3. SKRIP AJAR (Penting): Buatkan kalimat langsung (dialog) yang bisa dibacakan Ibu ke anaknya. Gunakan analogi benda sehari-hari (buah, mainan, kue).
    4. Kunci Jawaban: Berikan jawaban benar di akhir.

    Format output gunakan Markdown yang rapi. Pakai emoji biar seru.
    """
    
    with st.spinner("Sebentar Bun, GuruIbu lagi baca soalnya... 🧐"):
        response = model.generate_content([prompt, image])
        return response.text

# --- BAGIAN UPLOAD FOTO ---
uploaded_file = st.file_uploader("Upload Foto Soal di sini (Jepret yang jelas ya Bun)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Tampilkan gambar yang diupload
    image = Image.open(uploaded_file)
    st.image(image, caption="Soal yang diupload", use_container_width=True)

    # Tombol Aksi
    if st.button("Bantu Saya Jelaskan, GuruIbu! ✨"):
        try:
            # Kirim ke AI
            hasil = tanya_guruibu(image)
            
            # Tampilkan Hasil
            st.success("Selesai! Ini contekannya buat Bunda:")
            st.markdown(hasil)
            
            st.info("💡 Tips: Kalau anak masih bingung, coba minta GuruIbu cari analogi lain.")
            
        except Exception as e:
            st.error(f"Waduh, ada masalah teknis: {e}")
