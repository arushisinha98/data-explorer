import streamlit as st
import pandas as pd

st.set_page_config(
    page_title = "Describe",
    page_icon = "📈"
)

st.title("Describe Data")

file = st.file_uploader("upload file", type = {"csv", "txt"})
if file is not None:
    df = pd.read_csv(file)
st.write(df)