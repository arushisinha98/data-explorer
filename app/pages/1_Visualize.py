import streamlit as st
import pandas as pd
import numpy as np
import os
from Start import describe_data

import sys
sys.path.append('../src/')
from visualizations import *


def unique_groups(df, group_by):
    permutations = 1
    for col in group_by:
        permutations *= len(set(df[col]))
    return permutations


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
    
    st.write(f"Shape of selected data: `{visualize_df.shape}`")
    
    with st.expander("Describe Data Columns"):
        st.dataframe(describe_data(visualize_df))
    
    OneD, TwoD = st.tabs([" 1D  ","  2D  "])
    dtypes = dict(visualize_df.dtypes)
    
    with OneD:
        # select x-axis
        x_axis = st.selectbox(label = "Select x-axis",
                              options = list(visualize_df.columns),
                              index = None,
                              key = "1D_x_axis")
        group_by = False
        if x_axis:
            if dtypes[x_axis] != "datetime64[ns]":
                # select group_by (must be categorical)
                group_by = st.multiselect("Select Column(s) to Group By",
                                          options = [col for col in visualize_df.columns if col not in x_axis and dtypes[col] == "string" or dtypes[col] == "boolean"],
                                          key = "1D_group")
            
            # plot bar chart if x-axis is string/boolean
            if dtypes[x_axis] == "string" or dtypes[x_axis] == "boolean":
                chart = PlotBar(visualize_df, x_axis, group_by)
                st.altair_chart(chart, use_container_width = True)
            
            # plot density o/w (i.e. x-axis is float/int/datetime)
            else:
                chart = PlotDensity(visualize_df, x_axis, group_by)
                st.altair_chart(chart, use_container_width = True)
                
    with TwoD:
        # select x-axis
        x_axis = st.selectbox(label = "Select x-axis",
                              options = [col for col in visualize_df.columns],
                              index = None,
                              key = "2D_x_axis")
        group_by = False
        if x_axis:
            # if x-axis is categorical and y-axis is numeric, create vertical boxplots
            
            # if x-axis is categorical and y-axis is categorical, create heatmap
            
            # if x-axis is numeric and y-axis is categorical, create horizontal boxplots
            
            # if x-axis is numeric and y-axis is numeric, create scatter plot with coalescing bubbles (option to group by)
            
            # select y-axis
            y_axis = st.selectbox(label = "Select y-axis",
                                  options = [col for col in visualize_df.columns if col not in x_axis and dtypes[col] != "datetime64[ns]"],
                                  index = None,
                                  key = "2D_y_axis")
            if y_axis:
                # select group_by (must be categorical)
                group_by = st.multiselect("Select Column(s) to Group By",
                                          options = [col for col in visualize_df.columns if col not in x_axis and col not in y_axis and dtypes[col] == "string" or dtypes[col] == "boolean"],
                                          key = "2D_group")
                chart = PlotScatter(visualize_df, x_axis, y_axis, group_by)
                st.altair_chart(chart, use_container_width = True)
                
