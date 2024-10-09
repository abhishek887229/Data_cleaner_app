import streamlit as st
import pandas as pd
import numpy as np 

def hr():
    st.markdown("<hr>", unsafe_allow_html=True)


st.set_page_config(page_title="Data Cleaner App")

st.write("# Data Cleaner App")
st.write("A simple data cleaner app that can simplify the task of cleaning data.")

# Adding a horizontal line
hr()

# upload=st.file_uploader("uplaod CSV file here",type=["csv","xls"])

df=pd.read_csv("/workspaces/streamlit_app/Customers.csv")

st.dataframe(df,use_container_width=True)

hr()

st.write("# basic info of your Data")

count_data=df.count()

tab1, tab2,tab3=st.tabs(["Baisc Info","Cleaning","Feature Engineering"])

with tab1:
    st.write(f"your data have {count_data[0]} rows and {len(df.columns)} columns")

print(count_data)