import os
import streamlit as st
import pdfplumber
import plotly.express as px
import pandas as pd
import re
import requests
from io import BytesIO
from fpdf import FPDF
import tempfile
import plotly.io as pio


def save_figures_to_images(figures):
"""Simpan semua figure ke file PNG sementara"""
image_paths = []
for i, fig in enumerate(figures):
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    fig.write_image(tmp_file.name)
    image_paths.append(tmp_file.name)
return image_paths

# ===================== 🔍 Extract Text from PDF =====================
def extract_text_from_pdf(pdf_file):
text = ""
with pdfplumber.open(pdf_file) as pdf:
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
return text


# ===================== 📊 Parse Financial Data =====================
def parse_financials_dynamic(text):
"""Parse data keuangan dari laporan PDF, bisa tahunan atau bulanan."""
years = re.findall(r"\b(20\d{2})\b", text)
months = re.findall(
    r"(Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember)",
    text, flags=re.IGNORECASE
)

def extract_value(pattern):
    match = re.search(pattern + r".*?([\d.,]+)", text, flags=re.IGNORECASE)
    if match:
        try:
            # Ambil grup ke-2, karena grup ke-1 berisi kata "Pendapatan"
            value = match.group(2) if match.lastindex >= 2 else match.group(1)
            return float(value.replace(".", "").replace(",", ""))
        except Exception:
            return 0
    return 0


# Ambil data utama
revenue = extract_value(r"(Pendapatan|Penjualan|Revenue)")
cost = extract_value(r"(Beban|Cost|Pengeluaran)")
profit = extract_value(r"(Laba|Profit|Rugi)")
debt = extract_value(r"(Utang|Liabilitas|Debt)")

    # Tentukan mode waktu
if len(set(years)) > 1:
    time_mode = "year"
    labels = sorted(set(years))
elif months:
    time_mode = "month"
    labels = [m.capitalize() for m in months]
else:
    time_mode = "single"
    labels = [years[0] if years else "Unknown"]

# Buat DataFrame agar tetap tampil di grafik
df = pd.DataFrame({
    "Period": labels,
    "Revenue": [revenue] * len(labels),
    "Cost": [cost] * len(labels),
    "Profit": [profit] * len(labels),
    "Debt": [debt] * len(labels),
})

return df, time_mode


# ===================== 🧠 Query AI =====================
def query_hf_api(api_key, prompt, temperature=0.7, max_tokens=1200):
if not api_key:
    st.error("Please enter your API key first.")
    return None

try:
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        json={
            "model": "meta-llama/Llama-3.3-70B-Instruct",
            "messages": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
        },
        timeout=30,
    )
    if response.status_code != 200:
        st.error(f"Model Error {response.status_code}: {response.text}")
        return None

    return response.json()["choices"][0]["message"]["content"]

except Exception as e:
    st.error(f"Request Error: {e}")
    return None


# ===================== 🎨 Streamlit UI =====================
def run_financial_advisor():
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

    /* ==== FILE UPLOADER ==== */
    .stFileUploader label {
        color: #ffffff !important;       /* Label "Upload file" putih */
        font-weight: 600 !important;
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

    </style>
    """, unsafe_allow_html=True)
     
st.header("💰 Financial Advisor (Dynamic & AI-Powered)")
st.sidebar.text_input("Enter your OpenRouter API Key:", type="password", key="api_key")
API_KEY = st.session_state.get("api_key", "")

uploaded_file = st.file_uploader("📑 Upload company financial report (PDF)", type=["pdf"])
goal = st.text_input("🎯 What is the company's goal? (expansion, efficiency, attract investors, etc.)")

if uploaded_file and goal:
    st.info("🔎 Reading and analyzing financial data...")
    report_text = extract_text_from_pdf(uploaded_file)
    df, mode = parse_financials_dynamic(report_text)

    st.write(f"📅 **Detected mode:** {'Yearly' if mode=='year' else 'Monthly'}")
    st.dataframe(df)

    # === 1️⃣ Bar Chart: Summary ===
    st.subheader("📊 Overall Financial Summary")
    summary_df = df[["Revenue", "Cost", "Profit", "Debt"]].sum().reset_index()
    summary_df.columns = ["Metric", "Value"]
    fig1 = px.bar(summary_df, x="Metric", y="Value", title="Total Financial Performance", color="Metric")
    st.plotly_chart(fig1, use_container_width=True)

    # === 2️⃣ Line Chart: Profit Trend ===
    st.subheader("📈 Profit Trend Over Time")
    fig2 = px.line(df, x="Period", y="Profit", markers=True, title="Profit Trend", color_discrete_sequence=["#00BFFF"])
    st.plotly_chart(fig2, use_container_width=True)

    # === 3️⃣ Grouped Bar Chart: Revenue vs Cost ===
    st.subheader("📊 Revenue vs Cost Comparison")
    fig3 = px.bar(df, x="Period", y=["Revenue", "Cost"], barmode="group", title="Revenue vs Cost (Dynamic)", color_discrete_sequence=px.colors.qualitative.Set1)
    st.plotly_chart(fig3, use_container_width=True)

    # === 4️⃣ Pie Chart: Composition ===
    st.subheader("🥧 Financial Composition")
    comp_data = {
        "Revenue": df["Revenue"].sum(),
        "Cost": df["Cost"].sum(),
        "Profit": df["Profit"].sum(),
        "Debt": df["Debt"].sum(),
    }
    fig4 = px.pie(values=comp_data.values(), names=comp_data.keys(), title="Financial Composition")
    st.plotly_chart(fig4, use_container_width=True)

    # === 🧠 AI Analysis ===
    st.subheader("🤖 AI Strategic Recommendation")
    prompt = [
        {"role": "system", "content": """
    You are a world-class financial analyst and corporate strategist. 
    Your job is to analyze company financial reports and generate insights, risk evaluations, and strategic recommendations.
    Always consider both numerical data and written financial context.
    """},
        {"role": "user", "content": f"""
    Below is the raw extracted financial text from the company's PDF report:
    --------------------
    {report_text[:4000]}  # Limit supaya tidak overload token
    --------------------

    Below is the structured numerical data parsed from the report:
    {df.to_string(index=False)}

    The company's stated goal is: "{goal}"

    Your tasks:
    1. Analyze the financial performance — profitability, efficiency, and debt management.
    2. Identify trends and anomalies using both the numeric data and textual report.
    3. Classify the company's financial health as 'Excellent', 'Moderate', or 'Poor'.
    4. Provide detailed, actionable recommendations to achieve the company's goal.
    5. Summarize your findings clearly and concisely.
    Output your analysis in well-structured paragraphs.
    """}
    ]
    ai_result = query_hf_api(API_KEY, prompt)
    if ai_result:
        st.markdown(f'<div class="result-box">{ai_result}</div>', unsafe_allow_html=True)

            # === PDF Download with Charts ===
    if st.button("📥 Download Full Financial Report (PDF)"):

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "Financial Advisor Report", ln=True, align="C")

        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, f"Company Goal: {goal}\n\nAI Analysis:\n{ai_result}\n")

        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Financial Charts", ln=True, align="L")

        # ✅ Simpan figure langsung ke file sementara tanpa kaleido
        figures = [fig1, fig2, fig3, fig4]
        image_paths = []

        for i, fig in enumerate(figures):
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")

            # ⚡ gunakan full-color export tanpa kaleido
            img_bytes = pio.to_image(fig, format="png", engine="json")  # JSON engine tidak butuh chrome
            with open(tmp_file.name, "wb") as f:
                f.write(img_bytes)
            image_paths.append(tmp_file.name)

            pdf.image(tmp_file.name, w=180)
            pdf.ln(5)

        # ✅ Simpan hasil PDF ke memori
        pdf_buffer = BytesIO()
        pdf.output(pdf_buffer)
        pdf_buffer.seek(0)

        # ✅ Tombol Download PDF
        st.download_button(
            label="⬇️ Download Full PDF Report (Colored)",
            data=pdf_buffer,
            file_name="Financial_Advisor_Report.pdf",
            mime="application/pdf"
        )

        # Hapus file sementara
        for path in image_paths:
            os.unlink(path)


run_financial_advisor()
