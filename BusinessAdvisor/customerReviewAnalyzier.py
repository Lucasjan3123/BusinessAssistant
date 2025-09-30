import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract
from transformers import pipeline
from collections import Counter
import plotly.express as px
import pandas as pd


st.markdown("# Customer Review Analyzer Page ⭐")
st.sidebar.markdown("# Customer Review Analyzer Page ⭐")

# Load sentiment model (1–5 stars, multi-language)
@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

sentiment_model = load_model()

# Ekstraksi teks dari link
def extract_text_from_link(url):
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        texts = [p.get_text() for p in soup.find_all("p")]
        return " ".join(texts)
    except Exception as e:
        return f"Gagal ambil teks dari link: {e}"

# Ekstraksi teks dari gambar dengan OCR
def extract_text_from_image(image_file):
    try:
        img = Image.open(image_file)
        text = pytesseract.image_to_string(img, lang="ind")  # OCR Bahasa Indonesia
        return text
    except Exception as e:
        return f"Gagal baca teks dari gambar: {e}"


st.header("📝 Customer Review Analyzer")

# Pilihan input dengan selectbox
option = st.selectbox(
    "Pilih sumber review:",
    ["Pilih...", "Link", "Foto"]
)

review_text = ""

if option == "Link":
    st.subheader("Input Review dari Link")
    url = st.text_input("Masukkan URL review:")
    if st.button("Analisis Review dari Link") and url:
        st.info("Mengambil teks dari link...")
        review_text = extract_text_from_link(url)

elif option == "Foto":
    st.subheader("Input Review dari Foto")
    uploaded_file = st.file_uploader(
        "Upload screenshot review (JPG/PNG)",
        type=["jpg", "png"],
        accept_multiple_files=True
    )
    if st.button("Analisis Review dari Foto") and uploaded_file:
        all_texts = []
    for img_file in uploaded_file:  # tidak ada batasan
        st.info(f"Membaca teks dari gambar: {img_file.name} ...")
        text = extract_text_from_image(img_file)
        all_texts.append(text)

        review_text = " ".join(all_texts)

else:
    st.info("Silakan pilih sumber review di atas")

# ✅ Analisis Sentimen dipindahkan ke luar else
if review_text and review_text.strip():
    st.subheader("📄 Teks Review yang Diekstrak")
    st.write(review_text[:800])  # tampilkan cuplikan teks

    st.subheader("🤖 Analisis Sentimen")
    try:
        sentences = review_text.split(".")[:5]
        results = sentiment_model(sentences)

        # Tampilkan hasil tabel
        for sent, res in zip(sentences, results):
            st.write(f"**Kalimat:** {sent.strip()}")
            st.write(f"Sentimen: {res['label']} (score={res['score']:.2f})")
            st.write("---")

        # Grafik distribusi sentimen
        labels = [res["label"] for res in results]
        counts = Counter(labels)
        df_plot = pd.DataFrame({"Sentimen": list(counts.keys()), "Jumlah": list(counts.values())})

        # Plot pakai Plotly
        fig = px.bar(
            df_plot,
            x="Sentimen",
            y="Jumlah",
            color="Sentimen",          # warna tiap kategori
            barmode="group",
            text="Jumlah",             # tampilkan nilai di atas bar
            title="Distribusi Sentimen Review"
        )
        fig.update_layout(
            xaxis_title="Kategori Sentimen",
            yaxis_title="Jumlah Review",
            legend_title="Sentimen"
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Gagal analisis sentimen: {e}")
