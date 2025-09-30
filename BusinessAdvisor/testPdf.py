from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "PT Example Tech Indonesia", ln=True, align="C")
        self.ln(8)

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.set_fill_color(220, 220, 220)  # abu-abu muda
        self.cell(0, 10, title, ln=True, align="L", fill=True)
        self.ln(4)

    def financial_table(self, header, data):
        col_widths = [70, 40, 40, 40]   # Lebar kolom
        row_height = 10                 # Tinggi baris seragam
        table_margin = 15               # Margin kiri tabel

        # Header tabel
        self.set_x(table_margin)
        self.set_font("Arial", "B", 11)
        self.set_fill_color(200, 200, 200)
        for i, col in enumerate(header):
            align = "C" if i == 0 else "R"
            self.cell(col_widths[i], row_height, col, border=1, align=align, fill=True)
        self.ln()

        # Isi tabel
        self.set_font("Arial", "", 11)
        for row in data:
            self.set_x(table_margin)
            for i, item in enumerate(row):
                align = "L" if i == 0 else "R"
                self.cell(col_widths[i], row_height, str(item), border=1, align=align)
            self.ln()

        self.ln(8)  # spasi antar tabel

pdf = PDF()
pdf.add_page()

# Income Statement
pdf.chapter_title("Income Statement (2021-2023)")
header = ["Item", "2021", "2022", "2023"]
data = [
    ["Revenue", "90,000,000", "110,000,000", "135,000,000"],
    ["Cost of Goods Sold", "50,000,000", "60,000,000", "70,000,000"],
    ["Operating Expenses", "15,000,000", "18,000,000", "22,000,000"],
    ["Net Profit", "25,000,000", "32,000,000", "43,000,000"]
]
pdf.financial_table(header, data)

# Balance Sheet
pdf.chapter_title("Balance Sheet (as of Dec 31, 2021-2023)")
data = [
    ["Cash", "10,000,000", "12,000,000", "15,000,000"],
    ["Accounts Receivable", "8,000,000", "9,000,000", "12,000,000"],
    ["Inventory", "20,000,000", "22,000,000", "27,000,000"],
    ["Total Assets", "38,000,000", "43,000,000", "54,000,000"],
    ["Accounts Payable", "6,000,000", "7,000,000", "8,000,000"],
    ["Bank Debt", "10,000,000", "11,000,000", "12,000,000"],
    ["Total Liabilities", "16,000,000", "18,000,000", "20,000,000"],
    ["Retained Earnings", "22,000,000", "25,000,000", "34,000,000"]
]
pdf.financial_table(header, data)

# Cash Flow Statement
pdf.chapter_title("Cash Flow Statement (2021-2023)")
data = [
    ["Operating Cash Flow", "28,000,000", "35,000,000", "45,000,000"],
    ["Investing Cash Flow", "-5,000,000", "-7,000,000", "-9,000,000"],
    ["Financing Cash Flow", "-10,000,000", "-12,000,000", "-14,000,000"],
    ["Net Cash Flow", "13,000,000", "16,000,000", "22,000,000"]
]
pdf.financial_table(header, data)

# Key Ratios
pdf.chapter_title("Key Ratios (2021-2023)")
data = [
    ["ROA (%)", "6.6%", "7.4%", "8.0%"],
    ["ROE (%)", "11.3%", "12.8%", "12.6%"],
    ["Debt-to-Equity Ratio", "0.73", "0.72", "0.59"],
    ["Current Ratio", "1.50", "1.60", "1.70"]
]
pdf.financial_table(header, data)

# Save PDF
pdf.output("sample_financial_report_full_EN_ratios_clean.pdf")
print("✅ File sample_financial_report_full_EN_ratios_clean.pdf berhasil dibuat!")
