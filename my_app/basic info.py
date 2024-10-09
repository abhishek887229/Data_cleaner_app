import streamlit as st
import pandas as pd
import numpy as np 

st.set_page_config(page_title="Basic Statistics")

st.write("# Data Cleaner App")
st.write("A simple data cleaner app that can simplify the task of cleaning data.")

# Adding a horizontal line
st.markdown("<hr>", unsafe_allow_html=True)

upload=st.file_uploader("uplaod CSV file here",type=["csv","xls"])

df=pd.read_csv(upload)

st.dataframe(df,use_container_width=True)