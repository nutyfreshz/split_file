import subprocess
import streamlit as st
import pandas as pd
import os

# Function to split by rows
def split_csv_by_rows(df, output_prefix, rows_per_file):
    num_chunks = (len(df) + rows_per_file - 1) // rows_per_file  # Ceiling division
    output_files = []
    for i in range(num_chunks):
        start_row = i * rows_per_file
        end_row = start_row + rows_per_file
        chunk = df[start_row:end_row]
        output_file = f"{output_prefix}_rows_{i}.csv"
        chunk.to_csv(output_file, index=False)
        output_files.append(output_file)
    return output_files

# Function to split by group name
def split_csv_by_group_name(df, group_column, output_prefix):
    output_files = []
    for group_name in df[group_column].unique():
        group_data = df[df[group_column] == group_name]
        output_file = f"{output_prefix}_{group_name}.csv"
        group_data.to_csv(output_file, index=False)
        output_files.append(output_file)
    return output_files

# Streamlit App
st.title("CSV Splitter")

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file:
    # Read the uploaded file
    df = pd.read_csv(uploaded_file)
    st.write("Preview of the uploaded file:")
    st.write(df.head())

    st.subheader("1. Split by Number of Rows")
    rows_per_file = st.number_input("Enter number of rows per file:", min_value=1, value=1000, step=100)
    prefix_rows = st.text_input("Enter file prefix for split by rows:", value="output")
    
    if st.button("Split by Rows"):
        output_files = split_csv_by_rows(df, prefix_rows, rows_per_file)
        st.success("Files created:")
        for file in output_files:
            st.write(file)
            st.download_button(
                label=f"Download {file}",
                data=open(file, "rb").read(),
                file_name=file,
                mime="text/csv"
            )
        for file in output_files:
            os.remove(file)

    st.subheader("2. Split by Group Name")
    group_column = st.selectbox("Select column to split by group name:", df.columns)
    prefix_group = st.text_input("Enter file prefix for split by group name:", value="output")
    
    if st.button("Split by Group Name"):
        output_files = split_csv_by_group_name(df, group_column, prefix_group)
        st.success("Files created:")
        for file in output_files:
            st.write(file)
            st.download_button(
                label=f"Download {file}",
                data=open(file, "rb").read(),
                file_name=file,
                mime="text/csv"
            )
        for file in output_files:
            os.remove(file)
