import streamlit as st
import pandas as pd
import numpy as np
#from streamlit.components.v1 import html
#from streamlit_js_eval import streamlit_js_eval
import random

import sys
sys.path.append('../src/')
from PipelineClass import Pipeline, valid_dtypes


def recursive_transform(add_step, pipeline, n):
    
    if not add_step:
        return pipeline
        
    n += 1
    step_n = st.selectbox(label = "Select transformation step to be added to the pre-processing pipeline",
                      options = pipeline.listFunctions(),
                      key = f"Transformation_{n}")
    
    # get user inputs for each transformation
    if step_n:
        dtypes = dict(pipeline.data.dtypes)
        
        if step_n == "DropColumns":
            # multiselect columns to drop
            drop_cols = st.multiselect("↳ Select columns",
                                       pipeline.data.columns,
                                       key = f"{n}-DropColumns")
            if drop_cols:
                pipeline.DropColumns(drop_cols)
                
        elif step_n == "FilterColumnByStd":
            # select column; multiselect group_by; select params
            col = st.selectbox("↳ Select column",
                               [col for col in pipeline.data.columns if dtypes[col] == "Float64"],
                               key = f"{n}-FilterColumnByStd-Column")
            group_by = st.multiselect("↳ (Optional) Select column(s) to group by",
                                      [col for col in pipeline.data.columns if dtypes[col] != "Float64"],
                                      key = f"{n}-FilterColumnByStd-GroupBy")
            n_std = st.slider("↳ Select `N` standard deviations",
                              1, 5, 3,
                              key = f"{n}-FilterColumnByStd-n")
            fill = st.text_input("↳ Input fill value",
                                 placeholder = "Can be a numeric value, or 'mean', 'median', or 'NA'",
                                 key = f"{n}-FilterColumnByStd-Fill")
            
            if col and n_std and fill:
                pipeline.FilterColumnByStd(col, group_by, n_std, fill)
                
        elif step_n == "FilterColumnByValue":
            # select column; multiselect group_by; select params
            col = st.selectbox("↳ Select column",
                               [col for col in pipeline.data.columns if dtypes[col] == "Float64" or dtypes[col] == "Int64" or dtypes[col] == "boolean"],
                               key = f"{n}-FilterColumnByValue-Column")
            group_by = st.multiselect("↳ (Optional) Select column(s) to group by",
                                      [col for col in pipeline.data.columns if dtypes[col] != "Float64"],
                                      key = f"{n}-FilterColumnByValue-GroupBy")
            display1, display2 = st.columns([1,5])
            direction = display1.selectbox("↳ Specify filter",
                                           [">","<",">=","<="],
                                           key = f"{n}-FilterColumnByValue-direction")
            bound = display2.text_input("",
                                      key = f"{n}-FilterColumnByValue-bound")
            fill = st.text_input("↳ Input fill value",
                                 placeholder = "Can be a numeric value, or 'mean', 'median', or 'NA'",
                                 key = f"{n}-FilterColumnByValue-Fill")
            
            min_b, max_b = min(pipeline.data[col]), max(pipeline.data[col])
            if col and direction and bound:
                if bound > max_b or bound < min_b:
                    st.write("Filter value is beyond the minimum/maximum bounds of the column.")
                else:
                    pipeline.FilterColumnByValue(col, bound, dir, group_by, fill)
            
        elif step_n == "ImputeWithKNN":
            # select column and KNN params
            col = st.selectbox("↳ Select column",
                               [col for col in pipeline.data.columns if dtypes[col] == "Float64"],
                               key = f"{n}-ImputeWithKNN-Column")
            # TODO: suggest best N?
            n = st.slider("↳ Select `N` neighboring samples",
                          2, 20, 5,
                          key = f"{n}-ImputeWithKNN-n")
            
            if col and n:
                pipeline.ImputeWithKNN(col, n_neighbors = n)
            
        elif step_n == "RecodeColumnTypes":
            # select column and dtype
            col = st.selectbox("↳ Select column",
                               [col for col in pipeline.data.columns],
                               key = f"{n}-RecodeColumnTypes-Column")
            # TODO: select from allowable list of recodes
            dtype = st.selectbox("↳ Select dtype",
                                 valid_dtypes,
                                 key = f"{n}-RecodeColumnTypes-dtype")
            if col and dtype:
                pipeline.RecodeColumnTypes({col: dtype})
                
        elif step_n == "RecodeColumnValues":
            # select column and fill recode dataframe
            col = st.selectbox("↳ Select column",
                               [col for col in pipeline.data.columns if dtypes[col] == 'string[python]' or dtypes[col] == 'string'],
                               key = f"{n}-RecodeColumnValues-Column")
            df = pd.DataFrame(data = np.unique(pipeline.data[col]),
                              columns = ["Original Value"])
            df["New Value"] = ""
            recode_editor = st.data_editor(df,
                                           column_config = {
        "New Value": st.column_config.TextColumn(required = True)},
                                           key = f"{n}-RecodeColumnValues")
            apply = st.toggle("Apply", key = f"{n}-Recode")
            if apply:
                df = recode_editor.set_index("Original Value")
                st.write(df["New Value"].to_dict())
        
        #elif step_n == "RenameColumns":
            # select column and type name (fill dataframe?)
        #elif step_n == "SumColumnValues":
        
        
        add_step = st.checkbox("Add Another Transformation",
                               key = f"add_step_{n}")
        
        return recursive_transform(add_step, pipeline, n)


if __name__ == "__main__":

    st.set_page_config(
        page_title = "Transform"
    )
    
    if "MASTER DATA" not in st.session_state:
        st.session_state["MASTER DATA"] = pd.DataFrame()
    if "FILTERED DATA" not in st.session_state:
        st.session_state["FILTERED DATA"] = pd.DataFrame()
    
    data_subset = st.radio(label = "Select subset of data to be transformed.",
                           options = ("All Data", "Filtered Data"))
    
    if data_subset == "All Data":
        transform_df = st.session_state["MASTER DATA"]
    else:
        transform_df = st.session_state["FILTERED DATA"]
    
    st.write(f"Shape of selected data: {transform_df.shape[0]} rows, {transform_df.shape[1]} columns")
    
    pipeline = Pipeline(input_df = transform_df)
    
    with st.expander("View Data"):
        st.dataframe(transform_df)
    
    if transform_df.shape[0] > 0:
        transform = st.checkbox("Apply Transformation")
        steps = recursive_transform(transform, pipeline, n = 0)
