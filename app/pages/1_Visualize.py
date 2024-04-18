import streamlit as st
import pandas as pd
import numpy as np
import os


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
    
    st.write(f"Shape of selected data: {visualize_df.shape[0]} rows, {visualize_df.shape[1]} columns")
    
    with st.expander("View Data"):
        st.dataframe(visualize_df)
    
    OneD, TwoD = st.tabs(["  1D  ","  2D  "])
    dtypes = dict(visualize_df.dtypes)
    
    with OneD:
        # select x-axis
        x_axis = st.selectbox(label = "Select x-axis",
                              options = list(visualize_df.columns),
                              index = None,
                              key = "1D_x_axis")
        if x_axis:
            # select group_by (must be categorical)
            group_by = st.multiselect("Select Column(s) to Group By",
                                      options = [col for col in visualize_df.columns if col not in x_axis and dtypes[col] == "string" or dtypes[col] == "boolean"],
                                      key = "1D_group")
            # plot histogram if x-axis is string/boolean
            if dtypes[x_axis] == "string" or dtypes[x_axis] == "boolean":
                chart = PlotHistogram(visualize_df, x_axis)
                if group_by:
                    chart = PlotHistogram(visualize_df, x_axis, group_by)
                st.altair_chart(chart, use_container_width = True)
            # plot density o/w (i.e. x-axis is float, int, datetime)
            else:
                chart = PlotDensity(visualize_df, x_axis)
                if group_by:
                    chart = PlotDensity(visualize_df, x_axis, group_by)
                st.altair_chart(chart, use_container_width = True)
                
    with TwoD:
        # select x-axis
        x_axis = st.selectbox(label = "Select x-axis",
                              options = [col for col in visualize_df.columns if dtypes[col] != "string" and dtypes[col] != "boolean"],
                              index = None,
                              key = "2D_x_axis")
        if x_axis:
            # select y-axis
            y_axis = st.selectbox(label = "Select y-axis",
                                  options = [col for col in visualize_df.columns if col not in x_axis and dtypes[col] != "string" and dtypes[col] != "boolean" and dtypes[col] != "datetime64[ns]"],
                                  index = None,
                                  key = "2D_y_axis")
            if y_axis:
                # select group_by (must be categorical)
                group_by = st.multiselect("Select Column(s) to Group By",
                                          options = [col for col in visualize_df.columns if col not in x_axis and col not in y_axis and dtypes[col] == "string" or dtypes[col] == "boolean"],
                                          key = "2D_group")
                
                chart = PlotScatter(visualize_df, x_axis, y_axis)
                if group_by:
                    chart = PlotScatter(visualize_df, x_axis, y_axis, group_by)
                st.altair_chart(chart, use_container_width = True)
                
                # TODO: if categorical x or y, scatter by size
