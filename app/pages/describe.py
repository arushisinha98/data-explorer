import streamlit as st
import pandas as pd
from streamlit.components.v1 import html
from streamlit_js_eval import streamlit_js_eval


def describe_data(N = 5):
    
    master_df = st.session_state["MASTER DATA"]
    
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
    
    N_UNIQUE = st.slider('Categorical Snippet Length', 5, 15, 5)
    describe_df = describe_data(N_UNIQUE)
    
    st.dataframe(describe_df)