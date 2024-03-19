import streamlit as st
import datetime as datetime
import pandas as pd
import numpy as np
import os
#import openpyxl

#from PipelineClass import Pipeline

file_formats = {'csv': pd.read_csv,
                'xls': pd.read_excel,
                'xlsx': pd.read_excel,
                'xlsm': pd.read_excel,
                'xlsb': pd.read_excel
}

@st.cache_data(ttl = "2h") # cache data for 2 hours
def load_data(uploaded_file):
    try:
        ext = os.path.splitext(uploaded_file.name)[1][1:].lower()
    except:
        ext = uploaded_file.split(".")[-1]
    if ext in list(file_formats.keys()):
        return file_formats[ext](uploaded_file)
    else:
        st.error(f"Unsupported file format: {ext}")
        return None




if __name__ == "__main__":

    st.set_page_config(
        page_title = "Start",
        page_icon = "🚀",
    )
    
    st.title("Start")
    
    
    uploaded_file = st.file_uploader(
        "Upload Data",
        type = list(file_formats.keys()),
        help = "Excel and CSV file formats and their variations are supported."
    )
    
    if uploaded_file:
        df = load_data(uploaded_file)
        st.dataframe(df)
