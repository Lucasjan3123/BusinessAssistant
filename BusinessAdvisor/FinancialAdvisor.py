import streamlit as st
import pdfplumber
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import re
import requests
import json
from fpdf import FPDF
import tempfile
import os
from io import BytesIO



def save_figures_to_images(figures):
    """Simpan semua figure ke file PNG sementara"""
    image_paths = []
    for i, fig in enumerate(figures):
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        fig.write_image(tmp_file.name)
        image_paths.append(tmp_file.name)
    return image_paths

def query_hf_api(api_key, prompt, temperature=0.7, max_tokens=1200):
    if not api_key:
        st.error("Please enter your API key first.")
        return None

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "model": "meta-llama/Llama-3.3-70B-Instruct",
                "messages": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature,
            },
            timeout=30
        )

        if response.status_code != 200:
            try:
                error_msg = response.json().get("error", {}).get("message", response.text)
            except:
                error_msg = response.text
            st.error(f"⚠️ Model Error ({response.status_code}): {error_msg}")
            return None

        data = response.json()
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        st.error(f"⚠️ Request Error: {e}")
        return None

    except requests.exceptions.Timeout:
        st.error("⚠️ Request timeout. Try again.")
        return "⚠️ Request timeout. Try again."

    except requests.exceptions.ConnectionError:
        st.error("⚠️ Unable to connect to the model server. Please check your internet connection.")
        return "⚠️ Unable to connect to the model server. Please check your internet connection."

    except Exception:
        return "⚠️ AI unable to generate response"

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def parse_financials(text):
    patterns = {
        "Revenue": r"(Revenue|Pendapatan|Penjualan)\D+([\d,\.]+)",
        "Cost": r"(Cost|Beban|Pengeluaran)\D+([\d,\.]+)",
        "Profit": r"(Profit|Laba)\D+([\d,\.]+)",
        "Debt": r"(Debt|Utang)\D+([\d,\.]+)"
    }
    data = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                value = float(match.group(2).replace(",", "").replace(".", ""))
                data[key] = value
            except:
                pass
    return data

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

        st.header("💰 Financial Advisor Page")
        st.sidebar.markdown("# Financial Advisor Page 💰")
        st.sidebar.text_input("Enter your OpenRouter API Key:", type="password", key="api_key")

        API_KEY = st.session_state.get("api_key", "")
        uploaded_file = st.file_uploader("📑 Upload company financial report (PDF)", type=["pdf"])
        goal = st.text_input("🎯 What is the company's goal? (expansion, efficiency, attract investors, etc.)")

        if uploaded_file is not None and goal:
            st.info("🔎 Reading financial report...")
            report_text = extract_text_from_pdf(uploaded_file)

            if not report_text.strip():
                st.error("⚠️ Unable to read PDF content. Make sure the file contains text, not just scanned images.")
                return

            st.subheader("📄 Financial Report Preview")
            st.write(report_text[:800] + "...")

            parsed = parse_financials(report_text)
            st.write("📊 Extracted Data:", parsed)

            if not parsed:
                st.error("⚠️ No Revenue/Cost/Profit/Debt data found in report.")
                return

            # ✅ Build AI Prompt
            prompt = [
                {"role": "system", "content": "You are a financial analyst and strategist."},
                {"role": "user", "content": f"""
                Based on this company's extracted financial data:

                Revenue: {parsed.get("Revenue", 0)}
                Cost: {parsed.get("Cost", 0)}
                Profit: {parsed.get("Profit", 0)}
                Debt: {parsed.get("Debt", 0)}

                Company's goal: {goal}

                Task:
                1. Use these numbers as 'scores'.
                2. Build a JSON response with:
                    - scores (Revenue, Cost, Profit, Debt)
                    - trend (2019-2023 profit trend)
                    - comparison (2019-2023 revenue vs cost)
                    - composition (Strengths, Weaknesses, Risks, Opportunities as integer values)
                    - recommendation (strategic text advice)

                Return ONLY JSON in this format:
                {{
                "scores": {{"Revenue": int, "Cost": int, "Profit": int, "Debt": int}},
                "trend": {{
                    "Year": [2019, 2020, 2021, 2022, 2023],
                    "ProfitTrend": [int, int, int, int, int]
                }},
                "comparison": {{
                    "Year": [2019, 2020, 2021, 2022, 2023],
                    "Revenue": [int, int, int, int, int],
                    "Cost": [int, int, int, int, int]
                }},
                "composition": {{
                    "Strengths": int,
                    "Weaknesses": int,
                    "Risks": int,
                    "Opportunities": int
                }},
                "recommendation": "text"
                }}
                """}
            ]

            result = query_hf_api(API_KEY, prompt)

            if result:
                try:
                    # 🔹 Bersihkan jika AI balikin dengan ```json ... ```
                    clean_result = re.sub(r"^```(json)?", "", result.strip(), flags=re.MULTILINE)
                    clean_result = re.sub(r"```$", "", clean_result.strip(), flags=re.MULTILINE)
                    clean_result = clean_result.strip()

                    # 🔹 Parse ke JSON
                    data_json = json.loads(clean_result)

                    st.success("✅ JSON parsed successfully!")

                    # === Grafik 1: Scores (Bar Chart) ===
                    st.subheader("📊 Financial Scores")
                    df_scores = pd.DataFrame(list(data_json["scores"].items()), columns=["Metric", "Value"])
                    fig1 = px.bar(df_scores, x="Metric", y="Value", title="Financial Scores",color_discrete_sequence=px.colors.qualitative.Set2)
                    st.plotly_chart(fig1, use_container_width=True)

                    # === Grafik 2: Profit Trend (Line Chart) ===
                    st.subheader("📈 Profit Trend (2019-2023)")
                    df_trend = pd.DataFrame(data_json["trend"])
                    fig2 = px.line(df_trend, x="Year", y="ProfitTrend", markers=True, title="Profit Trend",color_discrete_sequence=["#00BFFF"])
                    st.plotly_chart(fig2, use_container_width=True)

                    # === Grafik 3: Revenue vs Cost (Grouped Bar Chart) ===
                    st.subheader("📊 Revenue vs Cost Comparison")
                    df_comp = pd.DataFrame(data_json["comparison"])
                    fig3 = px.bar(df_comp, x="Year", y=["Revenue", "Cost"], barmode="group", title="Revenue vs Cost", color_discrete_sequence=px.colors.qualitative.Set1)
                    st.plotly_chart(fig3, use_container_width=True)

                    # === Grafik 4: SWOT Composition (Pie Chart) ===
                    st.subheader("📊 SWOT Composition")
                    df_swot = pd.DataFrame(list(data_json["composition"].items()), columns=["Category", "Value"])
                    fig4 = px.pie(df_swot, names="Category",values="Value", title="SWOT Composition", color_discrete_sequence=px.colors.qualitative.Pastel)
                    st.plotly_chart(fig4, use_container_width=True)

                    # === Recommendation ===
                    st.subheader("🤖 AI Strategic Recommendation")
                    recommendation = data_json["recommendation"]
                    st.markdown(f'<div class="result-box">{recommendation}</div>', unsafe_allow_html=True)

                    if st.button("📥 Download Report (PDF with Charts)"):

                        figures = [fig1, fig2,fig3,fig4]  # tambahkan fig lain kalau ada
                        image_paths = save_figures_to_images(figures)

                        pdf = FPDF()
                        pdf.add_page()
                        pdf.set_font("Arial", "B", 16)
                        pdf.cell(200, 10, "Financial Advisor Report", ln=True, align="C")

                        pdf.set_font("Arial", size=12)
                        pdf.multi_cell(0, 10, f"Business Goal: {goal}\n")
                        pdf.multi_cell(0, 10, f"Scores: {data_json['scores']}\n")

                        pdf.set_font("Arial", "B", 14)
                        pdf.cell(200, 10, "AI Strategic Recommendation", ln=True, align="L")

                        # ✅ Wrap teks supaya aman
                        import textwrap
                        recommendation_text = data_json["recommendation"]
                        wrapped_recommendation = "\n".join(textwrap.wrap(recommendation_text, width=90))
                        pdf.set_font("Arial", size=12)
                        pdf.multi_cell(0, 10, wrapped_recommendation)

                        # Tambahkan grafik
                        pdf.set_font("Arial", "B", 14)
                        pdf.cell(200, 10, "Financial Charts", ln=True, align="L")
                        for img_path in image_paths:
                            pdf.image(img_path, w=180)
                            pdf.ln(5)

                        pdf_buffer = BytesIO()
                        pdf.output(pdf_buffer)
                        pdf_buffer.seek(0)

                        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                        pdf.output(tmp_file.name)

                        with open(tmp_file.name, "rb") as f:
                            st.download_button(
                                label="⬇️ Download Full PDF Report (Colored)",
                                data=f,
                                file_name="Financial_Advisor_Report.pdf",
                                mime="application/pdf"
                            )


                        for path in image_paths:
                            os.unlink(path)

                except Exception as e:
                    st.error(f"⚠️ JSON Parsing Error: {e}")
                    st.text("Raw AI output:\n" + result)


def save_figures_to_images(figures):
    image_paths = []
    for i, fig in enumerate(figures):
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        fig.write_image(tmp_file.name, format="png", scale=2)  # ✅ PNG berwarna
        image_paths.append(tmp_file.name)
    return image_paths


run_financial_advisor()       

