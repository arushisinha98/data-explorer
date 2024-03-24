import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.figure_factory as ff


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
    
    with st.expander("View Data"):
        st.dataframe(visualize_df)
    
    OneD, TwoD, ThreeD = st.tabs(["  1D  ","  2D  ","  3D  "])
    dtypes = dict(visualize_df.dtypes)
    
    with OneD:
        # select x-axis
        x_axis = st.selectbox(label = "Select x-axis",
                              options = list(visualize_df.columns),
                              index = None,
                              key = "1D_x_axis")
        
        # select group_by (must be categorical)
        group_by = st.multiselect("Select Column(s) to Group By",
                                  options = [col for col in visualize_df.columns if col not in x_axis])
        
        if x_axis:
            if dtypes[x_axis] == "string[python]" or dtypes[x_axis] == "boolean":
                st.write("INSERT BAR CHART")
            else:
                st.write("INSERT HISTOGRAM")
                
    with TwoD:
        # select x-axis (must be numeric)
        x_axis = st.selectbox(label = "Select x-axis",
                              options = list(visualize_df.columns),
                              index = None,
                              key = "2D_x_axis")
                              
        # select y-axis (must be numeric)
        y_axis = st.selectbox(label = "Select y-axis",
                              options = [col for col in visualize_df.columns if col not in x_axis],
                              index = None,
                              key = "2D_y_axis")
        
        # select group_by (must be categorical)
        group_by = st.multiselect("Select Column(s) to Group By",
                                  options = [col for col in visualize_df.columns if col not in x_axis and col not in y_axis])
        
        # if x_axis and y_axis:
    
    with ThreeD:
        # select x-axis (must be numeric)
        
        # select y-axis (must be numeric)
        
        # select z-axis
        
        # select group_by (must be categorical)
        
        # if x_axis and y_axis and z_axis:
        
