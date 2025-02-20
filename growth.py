import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Load data
st.set_page_config(page_title= "Data Sweeper,", layout="wide")

# custom css
st.markdown(
    """
    <style>
    startApp{
        background-color-black;
        color: white;
        }
     </style>
      """,
      unsafe_allow_html=True
)       

#tilte and description
st.title("Data Sweeper By M.S.Shah")
st.write("This is a data cleaning tool that helps you clean your data in a few clicks.")

#upload file
uploaded_file = st.file_uploader("Upload your input CSV file", type=["csv", "xlsx"], accept_multiple_files=true)

if uploaded_files:
    for file in uploaded_files:
      file_extension = os.path.splitext(file.name)[-1].lower()

      if file_extension == ".csv":
          df = pd.read_csv(file)
        elif file_extension == ".xlsx":
          df = pd.read_excel(file)
          else:
                st:error("This file format is not supported"): {file_extension}
                containue

                #file details
                st.write(" Preveiw the hand of the Dataframe") 
                st.Dataframe(df.head()) 

                #data cleaning options
                st.subheader("Data Cleaning Options")
                if st.checkox(f"Clean data for {file.name}"):
                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button(f"Remove duplicates from the file: {file.name}"):
                            df.drop_duplicates(inplace=True)
                            st.write("Duplicates removed successfully") 

                            with col2:
                                if st.button(f"Remove missing values from the file: {file.name}"):
                                    df.dropna(inplace=True)
                                    st.write("Missing values removed successfully") 

                                    #download cleaned data
                                    st.button(f"Fill missing values for 
                                    {file.name}"):
                                      numeric_cols = df.select_dtypes(include=["numbers"]).columns
                                        df[numeric_cols] = df[numeric_cols].fillna df.mean(df[numeric_cols].mean())
                                        st.write("Missing values have been filled successfully!")

                               st.subheader("Select Colums to keep")
                               columnns = st.multiselect(f"Select the columns for" {file.name} , df.columns, default=df.columns) 
                                 df = df[columnns]  

                                 #data visualization
                                 st.subheader("Data Visualization")
                                 if st.checkbox(f"Show visualizations for 
                                 {file.name}"):
                                     st.bar_chart(df.select_dtypes (include="number").ioloc[:, :2])

      #Converstion to Options

      st.subheader(" Conversion Options")
      converion_type = st.radio(f"Convert {file.name} to:", ["csv", "xlsx"], key=file.name)    
      if st.button(f"Convert{file.name}"):
          buffer = BytesIO()
          if conversion_type == "csv":
              df.to_csv(buffer, index=False)
              file_name = file.name.replace(file_extension, ".csv")
              mime_type = "text/csv"

           elsis conversion_type == "Excel":
               df.to_excel(buffer, index=False)
               file_name = file.name.replace(file_extension, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
           buffer.seek(0)
           st.download_button(
               label=f"Click here to download {file_name} as {conversion_type}",
               data=buffer,
               file_name=file_name,
               mime=mime_type,
           )     

st.success("All operations have been completed successfully!")           
