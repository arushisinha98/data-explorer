import streamlit as st
import datetime as datetime


st.title("TR2.0 Data Guide")
st.caption("A data visualization and experimentation tracking aid for TR2.0 and TR Integration.")

"""
st.header("1. Data Selection")
selection_type = st.radio("a. Type of Selection.",
                          ("**Continuous** to select all data collected during a continuous period.",
                           "**Discrete** to specify select years from the available data."))

if selection_type == "Continuous":
    YEAR_START, YEAR_END = st.slider("Select a continuous time period", 2016, 2023, (2016, 2016))
"""