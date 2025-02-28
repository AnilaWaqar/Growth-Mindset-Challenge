import streamlit as st
import pandas as pd
import numpy as np
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout='wide')

# Custom CSS for dark theme
st.markdown(
    """
    <style>
        .stApp {
            background-color: black;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True
)

# Title and description
st.title("📀 Data Sweeper Sterling Integration by Anila Waqar")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization by creating a project in Q3.")

# File uploader
uploaded_files = st.file_uploader("Upload your files (accepts CSV or Excel):", 
                                  type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext in [".xlsx", ".xls"]:
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # File details
        st.write(f"🔍 Preview of {file.name}")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader("🛠️ Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates Removed!")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=[np.number]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing values have been filled")

        # Column selection
        st.subheader("🎯 Select Columns to Keep")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Visualization
        st.subheader("📉 Data Visualization")
        if st.checkbox(f"Show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include=[np.number]).iloc[:, :2])

        # Conversion Options
        st.subheader("🔄 Conversion Options")
        conversions_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=str(hash(file.name)))

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversions_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversions_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)  # Ensure file pointer is at the start

            st.download_button(
                label=f"Download {file.name} as {conversions_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("🚀 All files processed successfully!")
