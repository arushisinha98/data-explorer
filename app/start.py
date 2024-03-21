import streamlit as st
import datetime as datetime
import pandas as pd
import numpy as np
import os


DISPLAY_MAX_N = 60000

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
    empty_df = pd.DataFrame()
    
    if "MASTER DATA" not in st.session_state:
        st.session_state["MASTER DATA"] = empty_df
    if "DISPLAY DATA" not in st.session_state:
        st.session_state["DISPLAY DATA"] = empty_df
    
    uploaded_file = st.file_uploader(
        "Upload Data",
        type = list(file_formats.keys()),
        help = "Most variations of Excel and CSV file formats are supported."
    )
    
    if uploaded_file:
        df = load_data(uploaded_file)
        df = df.convert_dtypes() # convert to columns to best dtypes
        st.session_state["MASTER DATA"] = df
        
        if df.shape[0] > DISPLAY_MAX_N:
            st.session_state["DISPLAY DATA"] = df.sample(n = DISPLAY_MAX_N,
                                                         replace = False, 
                                                         random_state = 1)
        else:
            st.session_state["DISPLAY DATA"] = df
            
        
        st.dataframe(st.session_state["DISPLAY DATA"])