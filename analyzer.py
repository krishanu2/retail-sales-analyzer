# analyzer.py (Level 2 – Emoji-free PDF Version)

import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
from prophet import Prophet
import warnings
import matplotlib
import re

matplotlib.use("Agg")
warnings.filterwarnings("ignore")

def strip_emojis(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

def run_analysis(df):
    output_paths = {}
    summary_points = []
    insights = []

    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    df.columns = df.columns.str.upper()
    df["DATE"] = pd.to_datetime(df[["YEAR", "MONTH"]].assign(DAY=1))

    # === TOP-SELLING ITEMS ===
    top_items = df.groupby("ITEM DESCRIPTION")["RETAIL SALES"].sum().sort_values(ascending=False).head(10).reset_index()
    output_paths["Top_Items.csv"] = os.path.join(output_dir, "top_items.csv")
    top_items.to_csv(output_paths["Top_Items.csv"], index=False)
    summary_points.append(f"Best-selling item: {top_items.iloc[0]['ITEM DESCRIPTION']} – ₹{top_items.iloc[0]['RETAIL SALES']:.2f}. Keep in stock!")

    # === LOW-SELLING ITEMS ===
    low_items = df.groupby("ITEM DESCRIPTION")["RETAIL SALES"].sum().sort_values().head(5).reset_index()
    output_paths["Low_Items.csv"] = os.path.join(output_dir, "low_selling.csv")
    low_items.to_csv(output_paths["Low_Items.csv"], index=False)
    summary_points.append(f"Lowest-selling item: {low_items.iloc[0]['ITEM DESCRIPTION']} – ₹{low_items.iloc[0]['RETAIL SALES']:.2f}. Consider phasing out.")

    # === SUPPLIER PERFORMANCE ===
    top_suppliers = df.groupby("SUPPLIER")["RETAIL SALES"].sum().sort_values(ascending=False).head(10).reset_index()
    output_paths["Top_Suppliers.csv"] = os.path.join(output_dir, "top_suppliers.csv")
    top_suppliers.to_csv(output_paths["Top_Suppliers.csv"], index=False)
    summary_points.append(f"Top supplier: {top_suppliers.iloc[0]['SUPPLIER']} – Reliable source of high-performing items.")

    # === MONTHLY SALES TREND ===
    monthly_sales = df.groupby("DATE")["RETAIL SALES"].sum().reset_index()
    plt.figure(figsize=(10, 5))
    plt.plot(monthly_sales["DATE"], monthly_sales["RETAIL SALES"], marker="o", color="royalblue")
    plt.title("Monthly Retail Sales Trend")
    plt.xlabel("Date")
    plt.ylabel("Retail Sales")
    plt.grid(True)
    plt.tight_layout()
    trend_path = os.path.join(output_dir, "sales_trend.png")
    plt.savefig(trend_path)
    output_paths["sales_trend.png"] = trend_path

    output_paths["Monthly_Trend.csv"] = os.path.join(output_dir, "monthly_sales_trend.csv")
    monthly_sales.to_csv(output_paths["Monthly_Trend.csv"], index=False)

    # === ITEM-WISE MONTHLY CSV ===
    item_monthly = df.groupby(["ITEM DESCRIPTION", "DATE"])["RETAIL SALES"].sum().reset_index()
    output_paths["Item_Monthly.csv"] = os.path.join(output_dir, "item_monthly_sales.csv")
    item_monthly.to_csv(output_paths["Item_Monthly.csv"], index=False)

    # === FORECAST WITH PROPHET ===
    forecast_df = pd.DataFrame()
    for item in top_items["ITEM DESCRIPTION"].head(3):
        item_data = df[df["ITEM DESCRIPTION"] == item].groupby("DATE")["RETAIL SALES"].sum().reset_index()
        item_data.columns = ["ds", "y"]
        if len(item_data) < 6:
            continue
        model = Prophet()
        model.fit(item_data)
        future = model.make_future_dataframe(periods=6, freq="MS")
        forecast = model.predict(future)
        forecast["ITEM"] = item
        forecast_df = pd.concat([forecast_df, forecast[["ds", "yhat", "ITEM"]]])

        # Plot
        fig = model.plot(forecast)
        plt.title(f"Forecast – {item}")
        fpath = os.path.join(output_dir, f"forecast_{item[:10].replace(' ', '_')}.png")
        fig.savefig(fpath)
        output_paths[f"forecast_{item}"] = fpath

        total_pred = forecast.tail(6)["yhat"].sum()
        summary_points.append(f"Upcoming 6-month projection for {item}: ₹{total_pred:.2f}. Stock up accordingly!")

    forecast_df = forecast_df.rename(columns={"ds": "Date", "yhat": "Predicted Sales"})
    output_paths["Forecast.csv"] = os.path.join(output_dir, "forecast.csv")
    forecast_df.to_csv(output_paths["Forecast.csv"], index=False)

    # === PROFITABILITY/LEAKAGE ===
    df["TOTAL SALES"] = df[["RETAIL SALES", "RETAIL TRANSFERS", "WAREHOUSE SALES"]].sum(axis=1)
    leakage = df[df["RETAIL SALES"] == 0].groupby("ITEM DESCRIPTION")["TOTAL SALES"].sum().sort_values(ascending=False).head(5)
    for i, (item, value) in enumerate(leakage.items(), start=1):
        insights.append(f"{i}. {item} shows sales via transfers/warehouse but not at retail: ₹{value:.2f}. Check for leakage or improper billing.")

    # === PDF REPORT ===
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Retail Sales Summary Report", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", size=11)
    intro = "Namaste! Here's a simple report to help manage your store better. We looked at your sales, slow/fast-moving items, and gave a peek into the future."
    pdf.multi_cell(0, 10, txt=strip_emojis(intro))
    pdf.ln(5)

    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Highlights", ln=True)
    for point in summary_points:
        clean = strip_emojis(point)
        pdf.multi_cell(0, 8, f"- {clean}")
    pdf.ln(4)

    if insights:
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt="Important Notes", ln=True)
        for obs in insights:
            clean = strip_emojis(obs)
            pdf.multi_cell(0, 8, f"- {clean}")

    pdf_path = os.path.join(output_dir, "Retail_Report.pdf")
    pdf.output(pdf_path)
    output_paths["Retail_Report.pdf"] = pdf_path

    return output_paths, summary_points + insights
