# 📘 Business Assistant AI  

## 📌 Deskripsi Singkat  
Project ini merupakan aplikasi **Business Assistant berbasis AI** yang dibuat menggunakan **Streamlit, Python, dan OpenRouter API (Llama 3.3)**.  
Aplikasi ini dirancang untuk membantu user dalam berbagai kebutuhan bisnis seperti:  
- Menghasilkan ide bisnis baru.  
- Menganalisis strategi pemasaran.  
- Melakukan analisis review pelanggan.  
- Memberikan rekomendasi finansial berbasis laporan keuangan perusahaan.  

Tujuannya adalah menyediakan sebuah **AI Business Consultant** yang interaktif, mudah digunakan, dan dapat diakses siapa saja secara online.  

---

## ✨ Fitur-Fitur Utama  
- **💡 Business Idea Generator** → Membuat ide bisnis berdasarkan industri, target audience, lokasi, budget, dan goals.  
- **📊 Marketing Strategy Generator** → Menyusun strategi pemasaran sesuai kebutuhan audiens.  
- **📝 Customer Review Analyzer** → Analisis sentimen review pelanggan dari link atau gambar (OCR).  
- **💰 Financial Advisor** →  
  - Membaca laporan keuangan (PDF).  
  - Mengekstrak data Revenue, Cost, Profit, Debt.  
  - Memberikan analisis keuangan berbasis AI.  
  - Menampilkan hasil dalam 4 grafik (Bar, Line, Grouped Bar, Pie).  
  - Menyediakan **strategic recommendation**.  
  - Download laporan lengkap dalam bentuk **PDF dengan grafik berwarna**.  

---

## ⚙️ Cara Menjalankan di Lokal  

1. **Clone Repository**
   ```bash
   git clone https://github.com/username/business-assistant-ai.git
   cd business-assistant-ai
2. **Buat Virtual Environment (opsional tapi direkomendasikan)**
   ```bash
  python -m venv venv
source venv/bin/activate  # untuk Mac/Linux
venv\Scripts\activate
3. **Install Dependencies**
   ```bash
 pip install -r requirements.txt
4. **Jalankan Aplikasi**
   ```bash
 streamlit run mainApps.py
