import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract
from transformers import pipeline
from collections import Counter
import plotly.express as px
import pandas as pd


st.markdown("""
    <style>
    /* Background utama */
    .stApp {
        background: linear-gradient(135deg, #0f172a, #1e293b, #0f2027);
        font-family: "Segoe UI", sans-serif;
        color: #e2e8f0;
    }

    /* Card form */
    .form-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 2rem;
        box-shadow: 0px 8px 25px rgba(0,0,0,0.6), inset 0px 0px 15px rgba(0,234,255,0.1);
        margin-top: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .form-card:hover {
        transform: translateY(-5px);
        box-shadow: 0px 12px 30px rgba(0,234,255,0.3), inset 0px 0px 20px rgba(0,234,255,0.15);
    }

    /* Title */
    .form-title {
        font-size: 24px;
        font-weight: 800;
        background: linear-gradient(90deg, #00eaff, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 18px;
        text-shadow: 0px 0px 8px rgba(0,234,255,0.6);
    }

    /* Input & textarea */
    .stTextInput input, .stTextArea textarea {
        background: rgba(15, 23, 42, 0.75) !important;
        border: 1px solid rgba(0,234,255,0.3) !important;
        border-radius: 12px !important;
        padding: 12px !important;
        color: #f1f5f9 !important;
        transition: all 0.3s ease;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #00eaff !important;
        box-shadow: 0px 0px 10px rgba(0,234,255,0.6);
    }
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: #94a3b8 !important;
    }

    /* Slider */
    .stSlider > div > div > div {
        color: #f8fafc !important;
    }

    }
    div.stButton > button:hover {
        transform: scale(1.07);
        box-shadow: 0px 8px 28px rgba(0,234,255,0.8);
    }

    /* Result box */
    .result-box {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(0,234,255,0.25);
        border-radius: 14px;
        padding: 1.5rem;
        margin-top: 20px;
        color: #e2e8f0;
        font-size: 15px;
        line-height: 1.6;
        box-shadow: inset 0px 0px 15px rgba(0,234,255,0.15);
    }
     /* === Fix Input Text Visibility === */
    .stTextInput input, .stTextArea textarea {
        background: rgba(15, 23, 42, 0.85) !important;
        border: 1px solid rgba(0,234,255,0.5) !important;
        border-radius: 12px !important;
        padding: 12px !important;
        color: #ffffff !important;     /* teks input putih */
        font-weight: 500 !important;
    }
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: #a0aec0 !important;     /* abu-abu terang */
        font-style: italic !important;
    }
    .stTextInput label, .stTextArea label, .stSlider label {
        color: #f8fafc !important;     /* label putih terang */
        font-weight: 600 !important;
    }

    /* === Slider Label & Value === */
    .stSlider label, .stSlider span {
        color: #f8fafc !important;
        font-weight: 600 !important;
    }
    /* === Judul Halaman (Markdown/Headers) === */
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2 {
        color: #ffffff !important;    /* Putih */
        font-weight: 800 !important;
        font-size: 28px !important;   /* Lebih besar */
    }

    /* === Label Input (Selectbox, TextInput, Slider) === */
    .stSelectbox label, .stTextInput label, .stTextArea label, .stSlider label {
        color: #ffffff !important;   /* Putih */
        font-weight: 600 !important;
        font-size: 15px !important;
    }

    .stFileUploader label {
        color: #ffffff !important;   /* Putih */
        font-weight: 600 !important;
        font-size: 15px !important;
    }
        /* === FILE UPLOADER CUSTOM === */
    .stFileUploader div[data-testid="stFileUploaderDropzone"] {
        background: rgba(15, 23, 42, 0.7) !important;   /* dark transparent */
        border: 2px dashed #00eaff !important;          /* neon border */
        border-radius: 12px !important;
        padding: 1.5rem !important;
        transition: all 0.3s ease-in-out;
        color: #f8fafc !important;                      /* text putih */
    }

    .stFileUploader div[data-testid="stFileUploaderDropzone"]:hover {
        background: rgba(0, 234, 255, 0.1) !important;
        border-color: #00bcd4 !important;
        box-shadow: 0px 0px 15px rgba(0,234,255,0.5);
    }

    /* === Text Drag & Drop === */
    .stFileUploader div[data-testid="stFileUploaderDropzone"] section div {
        color: #e2e8f0 !important;         /* putih */
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    /* === Browse Button === */
    .stFileUploader div[data-testid="stFileUploaderDropzone"] section button {
        background: linear-gradient(90deg, #00eaff, #0072ff) !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        border: none !important;
        font-size: 14px !important;
        box-shadow: 0px 4px 10px rgba(0,234,255,0.3) !important;
        transition: all 0.3s ease-in-out !important;
    }

    .stFileUploader div[data-testid="stFileUploaderDropzone"] section button:hover {
        transform: scale(1.05);
        box-shadow: 0px 6px 18px rgba(0,234,255,0.6) !important;
    }

    /* === File List (setelah upload) === */
    .stFileUploader ul {
        color: #f8fafc !important;   /* nama file putih */
        font-weight: 500 !important;
    }

            /* === FILE UPLOADER LIST === */
    .stFileUploader ul {
        margin-top: 10px !important;
    }

    .stFileUploader ul li {
        color: #ffffff !important;          /* teks nama file jadi putih */
        font-weight: 600 !important;        /* tebal */
        font-size: 14px !important;
        background: rgba(255,255,255,0.05); /* sedikit highlight */
        padding: 6px 10px;
        border-radius: 8px;
        margin-bottom: 6px;
    }

    /* Ikon file */
    .stFileUploader ul li span {
        color: #38bdf8 !important;  /* ikon biru muda */
    }

    /* Tombol X remove file */
    .stFileUploader ul li button {
        color: #f87171 !important;  /* merah */
        font-weight: bold;
    }
    .stFileUploader ul li button:hover {
        color: #ef4444 !important;
        transform: scale(1.2);
    }


    /* Kotak list file (full putih) */
    .stFileUploader div[data-testid="stFileUploaderFile"] {
        background: #ffffff !important;      /* Putih */
        border: 2px solid #00eaff !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        display: flex;
        align-items: center;
    }

    /* Nama file */
    .stFileUploader div[data-testid="stFileUploaderFile"] .uploadedFileName {
        color: #0f172a !important;   /* Hitam */
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    /* Ukuran file */
    .stFileUploader div[data-testid="stFileUploaderFile"] .uploadedFileSize {
        color: #334155 !important;   /* Abu gelap */
        font-size: 12px !important;
    }

    /* Ikon file */
    .stFileUploader div[data-testid="stFileUploaderFile"] svg {
        stroke: #0f172a !important;   /* Ikon hitam */
    }

    /* Tombol X hapus file */
    .stFileUploader div[data-testid="stFileUploaderFile"] button {
        color: #0f172a !important;    /* Hitam */
        font-weight: bold !important;
    }
    .stFileUploader div[data-testid="stFileUploaderFile"] button:hover {
        color: #1e293b !important;    /* Abu lebih gelap saat hover */
        transform: scale(1.1);
    }
            
    </style>
""", unsafe_allow_html=True)


st.header("⭐ Customer Review Analyzer Page")
st.sidebar.markdown("# Customer Review Analyzer Page ⭐")

# Load sentiment model (1–5 stars, multi-language)
@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

sentiment_model = load_model()

# Extract text from link
def extract_text_from_link(url):
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        texts = [p.get_text() for p in soup.find_all("p")]
        return " ".join(texts)
    except Exception as e:
        return f"⚠️ Failed to fetch text from link: {e}"

# Extract text from image with OCR
def extract_text_from_image(image_file):
    try:
        img = Image.open(image_file)
        text = pytesseract.image_to_string(img, lang="eng")  # OCR English
        return text
    except Exception as e:
        return f"⚠️ Failed to read text from image: {e}"

st.markdown('<div class="form-card">', unsafe_allow_html=True)
st.markdown('<div class="form-title">📝 Customer Review Analyzer</div>', unsafe_allow_html=True)

option = st.selectbox(
    "Select review source:",
    ["Choose...", "Link", "Image"]
)

review_text = ""

if option == "Link":
    url = st.text_input("🌐 Enter review URL:")
    if st.button("🔍 Analyze Review from Link", key="analyze_link"):
        st.info("Fetching text from link...")
        review_text = extract_text_from_link(url)

elif option == "Image":
    uploaded_file = st.file_uploader(
        "📷 Upload review screenshot (JPG/PNG)",
        type=["jpg", "png"],
        accept_multiple_files=True
    )
    if st.button("🔍 Analyze Review from Image", key="analyze_photo") and uploaded_file:
        all_texts = []
        for img_file in uploaded_file:
            st.info(f"Reading text from image: {img_file.name} ...")
            text = extract_text_from_image(img_file)
            all_texts.append(text)
        review_text = " ".join(all_texts)

else:
    st.warning("⚠️ Please select a review source above")

st.markdown('</div>', unsafe_allow_html=True)  # close form-card


# ✅ Sentiment Analysis
if review_text and review_text.strip():
    st.subheader("📄 Extracted Review Text")
    st.write(review_text[:800])  # show preview

    st.subheader("🤖 Sentiment Analysis")
    try:
        sentences = review_text.split(".")[:5]
        results = sentiment_model(sentences)

        # Show result per sentence
        for sent, res in zip(sentences, results):
            st.write(f"**Sentence:** {sent.strip()}")
            st.write(f"Sentiment: {res['label']} (score={res['score']:.2f})")
            st.write("---")

        # Sentiment distribution chart
        labels = [res["label"] for res in results]
        counts = Counter(labels)
        df_plot = pd.DataFrame({"Sentiment": list(counts.keys()), "Count": list(counts.values())})

        fig = px.bar(
            df_plot,
            x="Sentiment",
            y="Count",
            color="Sentiment",
            barmode="group",
            text="Count",
            title="Sentiment Distribution"
        )
        fig.update_layout(
            xaxis_title="Sentiment Category",
            yaxis_title="Number of Reviews",
            legend_title="Sentiment"
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"⚠️ Failed to analyze sentiment: {e}")
