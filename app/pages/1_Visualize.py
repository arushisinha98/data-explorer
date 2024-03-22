import streamlit as st
import pandas as pd
import numpy as np
import os


if __name__ == "__main__":

    st.set_page_config(
        page_title = "Visualize",
    )
    
    if "MASTER DATA" not in st.session_state:
        st.session_state["MASTER DATA"] = pd.DataFrame()
    if "FILTERED DATA" not in st.session_state:
        st.session_state["FILTERED DATA"] = pd.DataFrame()
    
    
    data_subset = st.radio(label = "Select subset of data to be visualized.",
                           options = ("All Data", "Filtered Data"))
    
    if data_subset == "All Data":
        visualize_df = st.session_state["MASTER DATA"]
    else:
        visualize_df = st.session_state["FILTERED DATA"]
    
    st.write(f"Shape of selected data: {visualize_df.shape[0]} rows, {visualize_df.shape[1]} columns")
