import streamlit as st
import pandas as pd
import numpy as np
import os
from Start import describe_data

import sys
sys.path.append('../src/')
from visualizations import *


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
        # select x-axis (non-datetime only)
        x_axis = st.selectbox(label = "Select x-axis",
                              options = visualize_df.columns,
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
            
            # plot density o/w (i.e. x-axis is float/int)
            else:
                chart = PlotDensity(visualize_df, x_axis, group_by)
                st.altair_chart(chart, use_container_width = True)
                
    with TwoD:
        # select x-axis
        x_axis = st.selectbox(label = "Select x-axis",
                              options = visualize_df.columns,
                              index = None,
                              key = "2D_x_axis")
        group_by = False
        if x_axis:
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
                
                # if x-axis is datetime
                if dtypes[x_axis] == "datetime64[ns]":
                    # if y-axis is numeric, create time series
                    if dtypes[y_axis] != "boolean" and dtypes[y_axis] != "string":
                        chart = PlotTimeseries(visualize_df, x_axis, y_axis, group_by)
                        st.altair_chart(chart, use_container_width = True)
                    else: # if y-axis is categorical, create bubble chart
                        chart = PlotStrip(visualize_df, x_axis, y_axis, group_by)
                        st.altair_chart(chart, use_container_width = True)
                
                # if x-axis is categorical
                elif dtypes[x_axis] == "boolean" or dtypes[x_axis] == "string":
                    # if y-axis is numeric, create vertical boxplots
                    if dtypes[y_axis] != "boolean" and dtypes[y_axis] != "string":
                        #chart =
                        print('continue')
                    else: # if y-axis is categorical, create heatmap
                        #chart =
                        x, y, df = x_axis, y_axis, visualize_df
                        df_filtered = df.copy()
                        df_filtered = df_filtered.dropna(subset=[x,y])
                        df_filtered['Group'] = df_filtered[group_by].astype(str).agg(', '.join, axis=1)
                        chart = alt.Chart(df_filtered).mark_rect().encode(
                            alt.X(f'{x}:N'),
                            alt.Y(f'{y}:N'),
                            alt.Color('count():Q', scale=alt.Scale(scheme="lightgreyred"))
                        )
                        st.altair_chart(chart, use_container_width = True)
                
                # if x-axis is numeric
                else:
                    # if y-axis is numeric, create scatter plot with coalescing bubbles
                    if dtypes[y_axis] != "boolean" and dtypes[y_axis] != "string":
                        bin = st.toggle("Bin axes")
                        chart = PlotScatter(visualize_df, x_axis, y_axis, bin, group_by)
                        st.altair_chart(chart, use_container_width = True)
                    else: # if y-axis is categorical, create horizontal boxplots
                        #chart =
                        print('continue')
                
