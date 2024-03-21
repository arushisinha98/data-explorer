import streamlit as st
import pandas as pd


def describe_data(master_df, n_categorical = 5):
    data = []
    dtypes = dict(master_df.dtypes)
    
    for col in list(master_df.columns):
        row = []
        row.append(dtypes[col])
        row.append(master_df[col].isnull().mean())
        
        if dtypes[col] == "string[python]":
            row.append("")
            values = list(set(master_df[col].dropna()))
            show_values = ', '.join(values[:n_unique])
            show_ellipse = [', ...' if len(values) > n_unique else '']
            row.append(f"[{show_values}{show_ellipse[0]}], {len(values)} unique values")
            
        elif dtypes[col] == "boolean":
            row.append("TRUE (1) or FALSE (0)")
            row.append("")
            
        else:
            row.append(f"{min(master_df[col].dropna())} to {max(master_df[col].dropna())}")
            row.append("")
            
        data.append(row)
            
    describe_df = pd.DataFrame(index = list(dtypes.keys()),
                               columns = ["dtype", "% Missing",
                                          "Numerical Range",
                                          "Categorical Snippet"],
                               data = data)
    return describe_df



if __name__ == "__main__":

    st.set_page_config(
        page_title = "Describe",
        page_icon = "📝"
    )

    st.title("Describe")
    master_df = st.session_state["MASTER DATA"]
    
    n_categorical = st.slider('Categorical Snippet Length', 5, 15, 5)
    describe_df = describe_data(master_df, n_categorical)
    
    st.dataframe(describe_df)
    
    with st.expander("View Details"):
        modify = st.checkbox("Filter by Column Value")
        if modify:
            dtypes = dict(master_df.dtypes)
            categoricals = [dtypes[col] for col, dtype in dtypes.items() if dtype == "string[python]" or dtype == "boolean"]
            filter_column = st.selectbox(categoricals,
                                         label_visibility = 'collapsed'
                                         index = None,
                                         placeholder = "Select a categorical column to filter by ...")
            if filter_column:
                filter_value = st.multiselect("↳ Select categories", list(set(master_df[filter_column])))
                st.dataframe(master_df.loc[df[filter_column].isin(filter_value)].reset_index(drop = True))
        else:
            st.dataframe(master_df)
    
    