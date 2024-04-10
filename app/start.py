import streamlit as st
import datetime as datetime
import pandas as pd
import numpy as np
import os


DISPLAY_MAX_N = 50000
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
        
        if dtypes[col] == "string[python]" or dtypes[col] == "string":
            values = list(set(master_df[col].dropna()))
            show_values = ', '.join(values[:EXAMPLE_CATEGORIES])
            show_ellipse = [', ...' if len(values) > EXAMPLE_CATEGORIES else '']
            row.append(f"[{show_values}{show_ellipse[0]}], {len(values)} unique values")
            
        elif dtypes[col] == "boolean":
            row.append("TRUE (1) or FALSE (0)")
            
        else:
            row.append(f"{min(master_df[col].dropna())} to {np.nanmax(master_df[col].dropna())}")
            
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
            previous_cols += filter_column
            
            if col_type == "string[python]" or col_type == "string" or col_type == "boolean":
            
                # TODO: show bar chart
                filter_value = st.multiselect("↳ Select categories", list(set(df[filter_column])),
                                              key = f"filter_value_{n}")
                filtered_df = df.loc[df[filter_column].isin(filter_value)].reset_index(drop = True)
                
            else:
            
                # TODO: show distribution with labelled IQR
                min_value, max_value = min(df[filter_column].dropna()), max(df[filter_column].dropna())
                
                # TODO: add manual entry option for slider values
                if col_type == "Int64" or col_type == "Int32":
                    filter_value = st.slider("↳ Select range of values",
                                             int(min_value), int(max_value),
                                             value = (int(min_value), int(max_value)),
                                             key = f"filter_value_{n}")
                                             
                elif col_type == "datetime64[ns]":
                    df[filter_column] = pd.to_datetime(df[filter_column])
                    min_value, max_value = min(df[filter_column].dropna()).to_pydatetime(), max(df[filter_column].dropna()).to_pydatetime()
                    filter_value = st.slider("↳ Select range of values",
                                             min_value, max_value,
                                             format = "YYYY-MM-DD hh:mm",
                                             value = (min_value, max_value))
                
                else:
                    filter_value = st.slider("↳ Select range of values",
                                             np.floor(min_value), np.ceil(max_value),
                                             value = (min_value, max_value))
                
                filtered_df = df.loc[(df[filter_column] >= filter_value[0]) &
                                     (df[filter_column] <= filter_value[1])].reset_index(drop = True)
            
            add_filter = st.checkbox("Add Another Filter",
                                     key = f"add_filter_{n}")
                
            return recursive_filter(add_filter, filtered_df, previous_cols, n)
    
    
    
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
    
    if uploaded_file:
        df = load_data(uploaded_file)
        df = df.dropna(how = 'all', axis = 1) # drop empty columns
        df = df.convert_dtypes() # set best dtypes
        st.session_state["MASTER DATA"] = df
        
        master_df = st.session_state["MASTER DATA"]
        describe_df = describe_data(master_df)
        st.dataframe(describe_df, use_container_width = True)
        
        filter = st.checkbox("Apply Filters")
        filtered_df = recursive_filter(filter, master_df, [], n = 0)
        
        if filtered_df is not None:
            st.dataframe(sample_data(filtered_df))
            st.write(filtered_df.shape)
            if sample_data(filtered_df).shape[0] < filtered_df.shape[0]:
                st.write("*Unable to show all rows*")
            st.session_state["FILTERED DATA"] = filtered_df
        
    st.write("")
    st.write("**Do you have the artifacts of an existing transformation pipeline?**\
    Pipeline artifacts will allow you to apply a pre-defined series of transformations on the above dataset.")
    uploaded_artifacts = st.file_uploader(
        "(Optional) Upload Pipeline Artifacts",
        type = 'json',
        help = "Only JSON files that were previously created on and downloaded from this platform will be accepted."
    )
    
    #if uploaded_artifacts:
        # check if artifacts are valid
        
        # create mermaid diagram of pipeline
        
        # apply or confirm button
    
