import streamlit as st
import datetime as datetime
import pandas as pd
import numpy as np
import json
import os

import sys
sys.path.append('../src/')
from visualizations import PlotStrip, PlotDensity, PlotBox
from PipelineClass import Pipeline, valid_dtypes

DISPLAY_MAX_N = 5000
EXAMPLE_CATEGORIES = 3

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


def describe_data(master_df):
    data = []
    dtypes = dict(master_df.dtypes)
    
    for col in list(master_df.columns):
        row = []
        row.append(dtypes[col])
        row.append(np.round(master_df[col].isnull().mean()*100,2))
        
        if dtypes[col] == "string":
            values = list(set(master_df[col].dropna()))
            show_values = ', '.join(values[:EXAMPLE_CATEGORIES])
            show_ellipse = [', ...' if len(values) > EXAMPLE_CATEGORIES else '']
            row.append(f"[{show_values}{show_ellipse[0]}], {len(values)} unique values")
            
        elif dtypes[col] == "boolean":
            row.append("True (1), False (0)")
            
        elif dtypes[col] == "datetime64[ns]":
            row.append(f"{pd.to_datetime(master_df[col].dropna().min().round('s'))} to {pd.to_datetime(master_df[col].dropna().max().round('s'))}")
        else:
            row.append(f"{round(master_df[col].dropna().min(), 4)} to {round(master_df[col].dropna().max(), 4)}")
            
        data.append(row)
            
    describe_df = pd.DataFrame(index = list(dtypes.keys()),
                               columns = ["dtype", "% Missing",
                                          "Values"],
                               data = data)
    return describe_df
    
    
def sample_data(df):
    if df.shape[0] > DISPLAY_MAX_N:
        return df.sample(n = DISPLAY_MAX_N,
                         replace = False,
                         random_state = 1)
    return df


def recursive_filter(add_filter, df, previous_cols, n):
    
    if not add_filter or df.empty or df.shape[0] == 0:
        return df
    
    n += 1
    dtypes = dict(df.dtypes)
    col_type = st.radio(label = "Select type of column to be filtered",
                        options = list(set(dtypes.values())),
                        key = f"col_type_{n}")
    
    if col_type:
        col_options = [col for col, dtype in dtypes.items() if dtype == col_type and col not in previous_cols]
        filter_column = st.selectbox(label = "Select column to filter by",
                                     options = col_options,
                                     index = None,
                                     key = f"filter_column_{n}")
        
        if filter_column:
            previous_cols += [filter_column]
            
            if col_type == "string" or col_type == "boolean":
                # inludes <NA> in selections
                filter_value = st.multiselect("↳ Select categories", list(set(df[filter_column])),
                                              key = f"filter_value_{n}")
                filtered_df = df.loc[df[filter_column].isin(filter_value)].reset_index(drop = True)
                
            else:
                min_value, max_value = min(df[filter_column].dropna()), max(df[filter_column].dropna())
                
                if col_type == "Int64":
                    chart = PlotBox(df, filter_column, width = 600, height = 60)
                    st.altair_chart(chart, use_container_width = True)
                    
                    filter_value = st.slider("↳ Select range of values",
                                             int(min_value), int(max_value),
                                             value = (int(min_value), int(max_value)),
                                             key = f"filter_value_{n}")
                    # toggle option to include <NA>
                    include_na = st.toggle("Include missing?", key = f"inlcude_na_{n}")
                                             
                elif col_type == "datetime64[ns]":
                    df[filter_column] = pd.to_datetime(df[filter_column])
                    min_value, max_value = min(df[filter_column].dropna()).to_pydatetime(), max(df[filter_column].dropna()).to_pydatetime()
                    filter_value = st.slider("↳ Select range of values",
                                             min_value, max_value,
                                             format = "YYYY-MM-DD hh:mm",
                                             value = (min_value, max_value),
                                             key = f"filter_value_{n}")
                    # toggle option to include <NA>
                    include_na = st.toggle("Include missing?", key = f"inlcude_na_{n}")
                
                else:
                    chart = PlotBox(df, filter_column, width = 600, height = 60)
                    st.altair_chart(chart, use_container_width = True)
                    filter_value = st.slider("↳ Select range of values",
                                             np.floor(min_value), np.ceil(max_value),
                                             value = (min_value, max_value),
                                             key = f"filter_value_{n}")
                    # toggle option to include <NA>
                    include_na = st.toggle("Include missing?", key = f"inlcude_na_{n}")
                
                filtered_df = df[(df[filter_column].between(filter_value[0], filter_value[1], inclusive = 'both'))]
                
                if include_na:
                    filtered_df = df[(df[filter_column].between(filter_value[0], filter_value[1], inclusive = 'both')) | df[filter_column].isna()]
            
            add_filter = st.checkbox("Add Another Filter",
                                     key = f"add_filter_{n}")
                
            return recursive_filter(add_filter, filtered_df, previous_cols, n)
    
    
def check_artifacts(json_data):
    # check that the artifacts have steps 1, 2, ... N
    keys = list(json_data.keys())
    steps = list(np.array(keys, dtype = int))
    if steps != list(np.array(range(1,len(steps)+1))):
        return False
    
    pipeline = Pipeline(pd.DataFrame())
    # check that the transformations are valid functions
    for key in keys:
        for function, params in json_data[key].items():
            if function not in pipeline.listFunctions:
                return False
    
    # check that each transformation has valid params
    return True
    

if __name__ == "__main__":

    st.set_page_config(
        page_title = "Explore My Data",
        page_icon = "🚀",
    )
    
    if "MASTER DATA" not in st.session_state:
        st.session_state["MASTER DATA"] = pd.DataFrame()
    if "FILTERED DATA" not in st.session_state:
        st.session_state["FILTERED DATA"] = pd.DataFrame()
    
    uploaded_file = st.file_uploader(
        "(Required) Upload Data",
        type = list(file_formats.keys()),
        help = "Most variations of Excel and CSV file formats are supported."
    )
    # upload data widget
    if uploaded_file:
        df = load_data(uploaded_file)
        # initialize pipeline object
        pipeline = Pipeline(input_df = df)
        df = pipeline.data # address edge-case dtype conversions
        
        st.session_state["MASTER DATA"] = df
        
        # show column descriptions
        master_df = st.session_state["MASTER DATA"]
        describe_df = describe_data(master_df)
        st.dataframe(describe_df, use_container_width = True)
        
        # optionally, apply recursive filtering
        filter = st.checkbox("Apply Filters")
        filtered_df = recursive_filter(filter, master_df, [], n = 0)
        
        if filtered_df is not None:
            st.dataframe(sample_data(filtered_df))
            st.write(filtered_df.shape)
            if sample_data(filtered_df).shape[0] < filtered_df.shape[0]:
                st.write("*Only showing a sample of {DISPLAY_MAX_N} rows*")
            st.session_state["FILTERED DATA"] = filtered_df
            
    
    # upload artifacts widget
    st.markdown("***")
    st.write("**Do you have the artifacts of an existing transformation pipeline?**\
    Pipeline artifacts will allow you to apply a pre-defined series of transformations on your uploaded dataset.")
    uploaded_artifacts = st.file_uploader(
        "(Optional) Upload Pipeline Artifacts",
        type = 'json',
        help = "Only JSON files that were previously created on and downloaded from this platform will be accepted."
    )
    
    # check valid artifacts, illustrate, and apply
    if uploaded_artifacts:
        artifacts = json.loads(uploaded_artifacts.read())
        if check_artifacts:
            st.write(artifacts)
            # apply or confirm button
            
            if uploaded_file:
                st.button("Apply")
    
