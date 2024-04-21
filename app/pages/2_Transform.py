import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import json

import sys
sys.path.append('../src/')
from PipelineClass import Pipeline, valid_dtypes
from transformations import recursive_transform


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
    
    st.write(f"Shape of selected data: `{transform_df.shape}`")
    
    # initialize pipeline object
    pipeline = Pipeline(input_df = transform_df)
    
    with st.expander("View Data"):
        st.dataframe(transform_df)
    
    if transform_df.shape[0] > 0:
        transform = st.checkbox("Apply Transformation")
        steps = recursive_transform(transform, pipeline, n = 0)
        
        export = st.button("Export Pipeline", disabled = not transform)
        if export:
            transform_df = pipeline.data
            st.write("Metadata:")
            st.write(pipeline.metadata)
            st.write("Artifacts:")
            st.write(pipeline.artifacts)
            
            creation_date = datetime.now().strftime('%Y%m%d')
            # download artifacts as json file and save in /data
            with open(f'../data/{creation_date}_artifacts.json', "w") as json_file:
                json.dump(pipeline.artifacts, json_file, indent=4)
        
        with st.expander("View Transformed Data"):
            st.dataframe(pipeline.data)
