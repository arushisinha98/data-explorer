import streamlit as st
import pandas as pd
import numpy as np

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
        valid_user_input = False
        
        if step_n == "DropColumns":
            # multiselect columns to drop
            drop_cols = st.multiselect("↳ Select columns to drop",
                                       pipeline.data.columns,
                                       key = f"{n}-DropColumns")
            if drop_cols:
                pipeline.DropColumns(drop_cols)
                valid_user_input = True
        
        elif step_n == "DropRows":
            # multiselect mandatory columns
            mandatory_cols = st.multiselect("↳ Select mandatory columns",
                                            pipeline.data.columns,
                                            key = f"{n}-DropRows")
            if mandatory_cols:
                pipeline.DropRows(mandatory_cols)
                valid_user_input = True
                
        elif step_n == "RenameColumns":
            # select column and fill rename dataframe
            df = pd.DataFrame(data = pipeline.data.columns,
                              columns = ["Original Name"])
            df["New Name"] = pipeline.data.columns
            recode_editor = st.data_editor(df,
                                           column_config = {"New Name": st.column_config.TextColumn(required = True),
                                                            "Original Name": st.column_config.TextColumn(disabled = True)},
                                           key = f"{n}-RenameColumns")
            df = recode_editor.set_index("Original Name")
            pipeline.RenameColumns(df["New Name"].to_dict())
            valid_user_input = True
                
        elif step_n == "RecodeColumnTypes":
            # select column and dtype
            display1, display2 = st.columns([1,1])
            col = display1.selectbox("↳ Select column",
                                     [col for col in pipeline.data.columns],
                                     key = f"{n}-RecodeColumnTypes-Column")
            dtype = display2.selectbox("↳ Select dtype",
                                       valid_dtypes,
                                       key = f"{n}-RecodeColumnTypes-dtype")
            if col and dtype:
                pipeline.RecodeColumnTypes({col: dtype})
        
        elif step_n == "ReplaceByValue":
            # select column; multiselect group_by; select params
            display1, display2 = st.columns([1,1])
            col = display1.selectbox("↳ Select column to be affected",
                                     [col for col in pipeline.data.columns if dtypes[col] == "Float64" or dtypes[col] == "Int64"],
                                     key = f"{n}-ReplaceByValue-Column")
            group_by = display2.multiselect("↳ (Optional) Select column(s) to group by",
                                            [col for col in pipeline.data.columns if dtypes[col] != "Float64" and dtypes[col] != "datetime64[ns]"],
                                            key = f"{n}-ReplaceByValue-GroupBy")
            display3, display4 = st.columns([1,5])
            direction = display3.selectbox("↳ Specify criteria",
                                           [">","<",">=","<=","==","!="],
                                           key = f"{n}-ReplaceByValue-direction")
            bound = display4.text_input("(i.e. values to replace)",
                                        key = f"{n}-ReplaceByValue-bound")
            fill = st.text_input("↳ Input fill value for filtered cells",
                                 placeholder = "Can be a numeric value, or 'mean', 'median', or 'NA'",
                                 key = f"{n}-ReplaceByValue-Fill")
            
            min_b, max_b = min(pipeline.data[col].dropna()), max(pipeline.data[col].dropna())
            if col and direction and bound:
                bound = float(bound)
                if bound > max_b or bound < min_b:
                    st.write("Criteria defies the minimum/maximum values of the column.")
                else:
                    pipeline.ReplaceByValue(col, bound, direction, group_by, fill)
        
        elif step_n == "ReplaceByStd":
            # select column; multiselect group_by; select params
            display1, display2 = st.columns([1,1])
            col = display1.selectbox("↳ Select column to be affected",
                                     [col for col in pipeline.data.columns if dtypes[col] == "Float64"],
                                     key = f"{n}-ReplaceByStd-Column")
            group_by = display2.multiselect("↳ (Optional) Select column(s) to group by",
                                [col for col in pipeline.data.columns if dtypes[col] != "Float64"],
                                key = f"{n}-ReplaceByStd-GroupBy")
            n_std = st.slider("↳ Select `N` standard deviations",
                              1, 5, 3,
                              key = f"{n}-ReplaceByStd-n")
            fill = st.text_input("↳ Input fill value for filtered cells",
                                 placeholder = "Can be a numeric value, or 'mean', 'median', or 'NA'",
                                 key = f"{n}-ReplaceByStd-Fill")
            
            if col and n_std and fill:
                pipeline.FilterColumnByStd(col, group_by, n_std, fill)
        
        
        elif step_n == "ImputeWithKNN":
            # select column and KNN params
            col = st.selectbox("↳ Select column",
                               [col for col in pipeline.data.columns if dtypes[col] == "Float64" and pipeline.data[col].isnull().values.any()],
                               key = f"{n}-ImputeWithKNN-Column")
            # TODO: suggest best N?
            knn = st.slider("↳ Select `N` neighboring samples whose mean value to impute with",
                            2, 20, 5,
                            key = f"{n}-ImputeWithKNN-knn")
            
            if col and knn:
                pipeline.ImputeWithKNN(col, n_neighbors = knn)
        
        
        elif step_n == "ImputeWithRegression":
            # select column; select dependent variables (columns) and input coefficients
            col = st.selectbox("↳ Select column (Independent Variable)",
                               [col for col in pipeline.data.columns if dtypes[col] == "Float64" or dtypes[col] == "Int64" or dtypes[col] == "boolean" and pipeline.data[col].isnull().values.any()],
                               key = f"{n}-ImputeWithRegression-Column")
                               
            df = pd.DataFrame(data = [c for c in pipeline.data.columns if dtypes[c] == "Float64" or dtypes[c] == "Int64" or dtypes[c] == "boolean"],
                              columns = ["Dependent Variable"])
            df["Coefficient"] = ""
            recode_editor = st.data_editor(df,
                                           column_config = {"Coefficient": st.column_config.NumberColumn(required = False)},
                                           key = f"{n}-ImputeWithRegression")
            apply = st.toggle("Calculate", key = f"{n}-Recode")
            if apply:
                df = recode_editor.set_index("Dependent Variable")["Coefficient"].to_dict()
                eqn_str = f"[{col}] ="
                Xs, coeffs = [], []
                for X, beta in df.items():
                    if beta:
                        Xs.append(X)
                        coeffs.append(beta)
                        if eqn_str[-1] == "=":
                            eqn_str += f" {beta} x [{X}]"
                        else:
                            eqn_str += f" + {beta} x [{X}]"
                st.write(f"**{eqn_str}**")
                pipeline.ImputeWithRegression(col, Xs, coeffs)
        
        
        elif step_n == "RecodeColumnValues":
            # select column and fill recode dataframe
            col = st.selectbox("↳ Select column",
                               [col for col in pipeline.data.columns if dtypes[col] == "string" or dtypes[col] == "boolean" or dtypes[col] == "Int64"],
                               key = f"{n}-RecodeColumnValues-Column")
            df = pd.DataFrame(data = np.unique(pipeline.data[col]),
                              columns = ["Original Value"])
            df["New Value"] = ""
            recode_editor = st.data_editor(df,
                                           column_config = {"New Value": st.column_config.TextColumn(required = True)},
                                           key = f"{n}-RecodeColumnValues")
            apply = st.toggle("Apply", key = f"{n}-Recode")
            if apply:
                df = recode_editor.set_index("Original Value")
                pipeline.RecodeColumnValues(col, df["New Value"].to_dict())
        
        else:
            st.write("[Work in Progress] This transformation is available in `src/PipelineClass.py` but still requires a frontend configuration to work on this Streamlit app. Please edit `app/pages/2_Transform.py` accordingly.")
        
        add_step = st.checkbox("Add Another Transformation",
                               key = f"add_step_{n}")
        
        return recursive_transform(add_step, pipeline, n)
