# 🛍️ Retail Sales Analyzer for Local Stores

A smart, lightweight app that helps small Kirana and clothing stores understand their **sales**, **inventory trends**, and make **better stocking decisions** — without needing tech skills.

---

## 💡 Features

✅ Upload your monthly sales + inventory CSV  
✅ Get insights like:
- 🥇 Best & worst-selling items
- 📦 Inventory shrinkage/loss
- 📈 Monthly trends
- 🔮 Sales forecast for upcoming months  
✅ Download clean and simple **PDF reports**
✅ Built with a **minimal, modern UI** using Streamlit

---

## 📂 Files Generated

- `top_items.csv` → Top-performing products  
- `low_items.csv` → Poor-selling products  
- `top_suppliers.csv` → Most active suppliers  
- `monthly_sales_trend.csv` → Trends over time  
- `Retail_Report.pdf` → Automatically generated report with insights

---

## 🛠️ Tech Stack

- **Python** 🐍  
- **Streamlit** for UI  
- **Pandas** & **Matplotlib** for data analysis + plots  
- **FPDF** for PDF generation  
- **Prophet** for forecasting

---

## 🚀 How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/krishanu2/retail-sales-analyzer.git
cd retail-sales-analyzer

2. Install dependencies

pip install -r requirements.txt

Or install individually:

pip install streamlit pandas matplotlib fpdf scikit-learn prophet


3. Run the app
python -m streamlit run app.py
Open the app in your browser at: http://localhost:8501



📄 Sample Report Section
The generated PDF includes:

📌 Best-selling products you should restock

⚠️ Low-selling items you can remove or discount

📈 Forecast of next month's sales

✅ Actionable points in simple shopkeeper-friendly language

🙌 Made By
Krishanu Mahapatra
