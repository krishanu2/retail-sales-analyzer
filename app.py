import streamlit as st
import pandas as pd
import os
import base64
from analyzer import run_analysis

st.set_page_config(page_title="Retail Analyzer", layout="wide")
st.title("🛍️ Retail Sales Analyzer")

uploaded_file = st.file_uploader("Upload your sales data CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")

        if st.button("Run Analysis"):
            with st.spinner("Analyzing data and generating reports..."):
                output_paths, summary = run_analysis(df)

            st.success("✅ Analysis Complete!")

            # Display summary points
            st.subheader("📌 Summary Insights")
            for point in summary:
                st.markdown(f"- {point}")

            # Tabs for results
            tab1, tab2, tab3, tab4 = st.tabs(["Top Items", "Top Suppliers", "Trends", "Forecast"])

            with tab1:
                st.subheader("🏆 Top-Selling Items")
                st.dataframe(pd.read_csv(output_paths["Top_Items.csv"]))
                st.download_button("Download CSV", data=open(output_paths["Top_Items.csv"], "rb"), file_name="top_items.csv")

            with tab2:
                st.subheader("🚚 Top Suppliers")
                st.dataframe(pd.read_csv(output_paths["Top_Suppliers.csv"]))
                st.download_button("Download CSV", data=open(output_paths["Top_Suppliers.csv"], "rb"), file_name="top_suppliers.csv")

            with tab3:
                st.subheader("📈 Monthly Sales Trend")
                st.image(output_paths["sales_trend.png"])
                st.download_button("Download CSV", data=open(output_paths["Monthly_Trend.csv"], "rb"), file_name="monthly_sales_trend.csv")

            with tab4:
                st.subheader("🔮 Forecasts (Next 6 Months)")
                forecast_df = pd.read_csv(output_paths["Forecast.csv"])
                st.dataframe(forecast_df)
                st.download_button("Download Forecast CSV", data=open(output_paths["Forecast.csv"], "rb"), file_name="forecast.csv")

                for key in output_paths:
                    if key.startswith("forecast_") and key.endswith(".png"):
                        st.image(output_paths[key])

            # Report download
            st.markdown("---")
            st.subheader("📝 Download Full Report")
            with open(output_paths["Retail_Report.pdf"], "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                href = f'<a href="data:application/pdf;base64,{b64}" download="Retail_Report.pdf">📥 Download PDF Report</a>'
                st.markdown(href, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Failed to process file: {e}")
