import streamlit as st
import pandas as pd
import statistics as sts

def hr():
    st.markdown("<hr>", unsafe_allow_html=True)

st.set_page_config(page_title="Data Cleaner App")

st.write("# Data Cleaner App")
st.write("A simple data cleaner app that can simplify the task of cleaning data.")

# Adding a horizontal line
hr()

# File uploader for CSV files
uploaded_file = st.file_uploader("Upload CSV file here", type=["csv", "xls"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.dataframe(df, use_container_width=True)

    hr()

    st.write("# Basic Info of Your Data")

    count_data = df.count()

    tab1, tab2, tab3 = st.tabs(["Overview of Your Data", "Feature Selection", "Feature Engineering"])

    with tab1:
        st.subheader("Select a Column for Basic Statistics")
        columns1 = df.columns.tolist()
        selected_column = st.selectbox("Select column", columns1)

        if selected_column:
            col1, col2, col3 = st.columns(3)

            with col1:
                st.subheader("Mean")
                st.write(df[selected_column].mean())

            with col2:
                st.subheader("Median")
                st.write(df[selected_column].median())

            with col3:
                st.subheader("Rows/Columns")
                st.write(f"{count_data[selected_column]}/{len(df.columns)}")

            col4, col5, col6 = st.columns(3)

            with col4:
                st.subheader("Unique Values")
                st.write(len(df[selected_column].unique()))

            with col5:
                st.subheader("Mode")
                try:
                    st.write(sts.mode(df[selected_column]))
                except Exception as e:
                    st.write("No mode found.")

    with tab2:
        st.title("Select Columns You Want to Drop")

        # Select columns to drop
        columns = df.columns.tolist()
        select_columns = st.multiselect("Select columns to drop", columns)

        # Drop selected columns from the DataFrame
        if select_columns:
            df.drop(columns=select_columns, inplace=True)
            st.success(f"Dropped columns: {', '.join(select_columns)}")

        # Display the updated DataFrame
        st.dataframe(df.head())

        st.markdown("<hr>", unsafe_allow_html=False)

        st.title("# Change Your Data Type")

        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            columns1 = df.columns.tolist()
            select_cols = st.selectbox("Select column", columns1)
            st.write("Selected column:", select_cols)

        with col2:
            data_type = ['int64', 'float64', 'bool', 'object', 'string', 'datetime64[ns]', 'timedelta[ns]']
            select_datatype = st.selectbox("Select Data Type", data_type)
            st.write("Selected Data Type:", select_datatype)

        with col3:
            if st.button("Apply"):
                try:
                    # Change the data type of the selected column
                    df[select_cols] = df[select_cols].astype(select_datatype)
                    st.success(f"Successfully converted '{select_cols}' to data type '{select_datatype}'")
                except Exception as e:
                    st.error(f"Error converting '{select_cols}': {e}")

        # Display updated data types
        st.write("Data Types of Each Column:")
        for i in df.columns:
            st.write(f"{i}: {df[i].dtype}")
else:
    st.warning("Please upload a CSV file to get started.")
