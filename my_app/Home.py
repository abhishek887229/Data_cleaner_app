import streamlit as st
import pandas as pd
import numpy as np
import math as mt
import statistics as sts

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

st.write("#")

st.write("# basic info of your Data")

count_data=df.count()

tab1, tab2,tab3=st.tabs(["Over view of your data","Cleaning","Feature Engineering"])

with tab1:

    col1,col2,col3 =st.columns(3)

    with col1:
        st.subheader("mean")
        st.write(df['Age'].mean())

    with col2:
        st.subheader("median")
        st.write(df['Age'].median())

    with col3:
        st.subheader("Rows/Columns")
        st.write(f"{count_data[0]}/{len(df.columns)}")
        
    col4,col5,col6=st.columns(3)

    with col4:
        st.subheader("unique values")
        st.write(len(df['Age'].unique()))

    with col5:
        st.subheader("median")
        st.write(df['Age'].median())

    with col6:
        st.subheader("mode")
        st.write(sts.mode(df['Age']))
        
    