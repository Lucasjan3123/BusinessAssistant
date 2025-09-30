import streamlit as st
import pdfplumber
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import re
import requests
from fpdf import FPDF
import tempfile
import os


st.markdown("# Financial Advisor Page  💰")
st.sidebar.markdown("# Financial Advisor Page  💰")
st.sidebar.text_input("Enter your OpenRouter API Key:", type="password", key="api_key")
# Hugging Face API Key
API_KEY = st.session_state.get("api_key", "")

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
            return "⚠️ AI unable to generate response"

        data = response.json()
        answer = data["choices"][0]["message"]["content"]
        return answer

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

    uploaded_file = st.file_uploader("Upload laporan keuangan perusahaan (PDF)", type=["pdf"])
    goal = st.text_input("Apa tujuan perusahaan? (ekspansi, efisiensi, cari investor, dll)")

    if uploaded_file is not None and goal:
        st.info("📑 Membaca laporan keuangan...")
        report_text = extract_text_from_pdf(uploaded_file)

        if not report_text.strip():
            st.error("Tidak bisa membaca isi PDF. Pastikan file berisi teks, bukan scan gambar.")
            return

        st.subheader("📄 Cuplikan Laporan Keuangan")
        st.text(report_text[:800])

        parsed = parse_financials(report_text)
        st.write("📊 Data terdeteksi:", parsed)

        years = [2019, 2020, 2021, 2022, 2023]

        if parsed:
            revenue = [parsed.get("Revenue", 100000)] + list(np.random.randint(80, 150, size=4))
            cost = [parsed.get("Cost", 50000)] + list(np.random.randint(40, 100, size=4))
            profit = [parsed.get("Profit", revenue[0] - cost[0])] + list(np.random.randint(20, 80, size=4))
            debt = [parsed.get("Debt", 20000)] + list(np.random.randint(10, 60, size=4))
        else:
            revenue = np.random.randint(80, 150, size=5)
            cost = np.random.randint(40, 100, size=5)
            profit = revenue - cost
            debt = np.random.randint(20, 60, size=5)

        df = pd.DataFrame({
            "Year": years,
            "Revenue": revenue,
            "Cost": cost,
            "Profit": profit,
            "Debt": debt
        })

        # Grafik
        st.subheader("📊 Visualisasi Keuangan")
        fig1 = px.bar(df, x="Year", y=["Revenue", "Cost"], barmode="group", title="Revenue vs Cost")
        st.plotly_chart(fig1, use_container_width=True)
        fig2 = px.line(df, x="Year", y="Profit", markers=True, title="Profit Trend")
        st.plotly_chart(fig2, use_container_width=True)
        fig3 = px.area(df, x="Year", y="Debt", title="Debt Trend", color_discrete_sequence=["red"])
        st.plotly_chart(fig3, use_container_width=True)
        latest = df.iloc[-1]
        fig4 = px.pie(
            names=["Revenue", "Cost", "Profit"],
            values=[latest["Revenue"], latest["Cost"], latest["Profit"]],
            title=f"Komposisi Keuangan {latest['Year']}"
        )
        st.plotly_chart(fig4, use_container_width=True)

        # Financial Health Score
        st.subheader("📈 Financial Health Score")
        profit_margin = latest["Profit"] / latest["Revenue"] if latest["Revenue"] else 0
        debt_ratio = latest["Debt"] / latest["Revenue"] if latest["Revenue"] else 0
        score = (profit_margin * 100) - (debt_ratio * 50)
        score = max(0, min(100, score))
        if score > 70:
            label = "Sangat Sehat 👍"
        elif score > 40:
            label = "Cukup Sehat 🙂"
        else:
            label = "Kurang Sehat ⚠️"
        st.write(f"**Profit Margin:** {profit_margin:.2%}")
        st.write(f"**Debt Ratio:** {debt_ratio:.2%}")
        st.write(f"**Health Score:** {score:.0f} → {label}")

        fig5 = go.Figure(
            go.Indicator(
                mode="gauge+number+delta",
                value=score,
                delta={'reference': 70},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 40], 'color': "red"},
                        {'range': [40, 70], 'color': "yellow"},
                        {'range': [70, 100], 'color': "green"}
                    ],
                },
                title={'text': "Financial Health Gauge"}
            )
        )
        st.plotly_chart(fig5, use_container_width=True)

               # Analisis AI
        st.subheader("🤖 Analisis & Saran AI")
        result = None
        if API_KEY:
            prompt = [
            {"role": "system", "content": "You are a world-renowned financial and business expert, ranked among the top in the world with decades of proven experience in corporate finance, business strategy, and investment advisory."},
            {"role": "user", "content": f"""
            Analyze the following company's financial report with the highest level of expertise 
            and provide clear, actionable recommendations.

            Company's financial report:

            {report_text}

            Company's goal: {goal}

            Please deliver a professional analysis covering revenue, costs, profit, and debt. 
            Identify financial strengths, weaknesses, opportunities, and risks. 
            Finally, provide strategic business recommendations tailored to the company's stated goal.
            """}
        ]


            result = query_hf_api(API_KEY, prompt, temperature=0.7, max_tokens=1200)
            if result:
                st.success(result)
        else:
            st.warning("❌ Hugging Face API Key belum diset.")

        # ✅ Download Report PDF dengan grafik (di luar if API_KEY)
        if result:
            if st.button("📥 Download Report (PDF dengan Grafik)"):
                figures = [fig1, fig2, fig3, fig4, fig5]
                image_paths = save_figures_to_images(figures)

                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", "B", 16)
                pdf.cell(200, 10, "Financial Advisor Report", ln=True, align="C")

                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, f"Business Goal: {goal}\n")
                pdf.multi_cell(0, 10, f"Health Score: {score:.0f} → {label}\n")
                pdf.multi_cell(0, 10, "AI Advice:\n")
                pdf.multi_cell(0, 10, result)

                pdf.set_font("Arial", "B", 14)
                pdf.cell(200, 10, "Financial Charts", ln=True, align="L")

                for img_path in image_paths:
                    pdf.image(img_path, w=180)
                    pdf.ln(5)

                tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                pdf.output(tmp_file.name)

                with open(tmp_file.name, "rb") as f:
                    st.download_button(
                        label="⬇️ Klik untuk Download PDF Lengkap",
                        data=f,
                        file_name="Financial_Advisor_Report.pdf",
                        mime="application/pdf"
                    )

                for path in image_paths:
                    os.unlink(path)
                os.unlink(tmp_file.name)

run_financial_advisor()       

