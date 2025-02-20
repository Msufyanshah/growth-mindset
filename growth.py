import streamlit as st
import pandas as pd
import os
import io
from io import BytesIO
import chardet  # Ensure this is correctly indented

# Load data
st.set_page_config(page_title="Data Sweeper", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    body {
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Description
st.title("Data Sweeper By M.S. Shah")
st.write("This is a data cleaning tool that helps you clean your data in a few clicks.")

# Upload File
uploaded_files = st.file_uploader("Upload your input CSV/XLSX file", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()  # Get file extension

        # Read the file correctly
        if file_ext == ".csv":
            try:
                raw_data = file.getvalue()
                detected_encoding = chardet.detect(raw_data)["encoding"]  # Auto-detect encoding
                df = pd.read_csv(io.StringIO(raw_data.decode(detected_encoding)), errors="replace")
            except UnicodeDecodeError:
                st.error("Error reading CSV file. Unsupported encoding format.")
                continue
        elif file_ext == ".xlsx":
            df = pd.read_excel(io.BytesIO(file.getvalue()), engine="openpyxl")
        else:
            st.error(f"Unsupported file format: {file_ext}")
            continue  # Skip invalid file formats

        # File Preview
        st.subheader(f"Preview of {file.name}")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("Duplicates removed successfully!")

            with col2:
                if st.button(f"Remove missing values from {file.name}"):
                    df.dropna(inplace=True)
                    st.success("Missing values removed successfully!")

            # Fill Missing Values
            if st.button(f"Fill missing values for {file.name}"):
                numeric_cols = df.select_dtypes(include=["number"]).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.success("Missing values filled successfully!")

        # Select Columns to Keep
        st.subheader("Select Columns to Keep")
        columns = st.multiselect(f"Select columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show visualizations for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # Conversion Options
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine="openpyxl")
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)
            st.download_button(
                label=f"Click to download {file_name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type,
            )

st.success("All operations have been completed successfully!")
