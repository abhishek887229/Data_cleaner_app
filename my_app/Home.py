import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statistics as sts

def categorized_cols(dataframe):
    num_cols = df.select_dtypes(include=["int32", "int64", "float32", "float64"]).columns.tolist()
    categorical_col = df.select_dtypes(include=["object", "category", "string"]).columns.tolist()
    boolean_cols = df.select_dtypes(include=["bool"]).columns.tolist()
    date_time_cols = df.select_dtypes(include=["datetime64", "datetime", "timedelta", "timedelta64"]).columns.tolist()

    return num_cols, categorical_col, boolean_cols, date_time_cols


def hr():
    st.markdown("<hr>", unsafe_allow_html=True)


def check_duplicate(dataset):
    return dataset.duplicated().sum()
global null_columns
null_columns=[]
def find_null_cols(data):
    for i in data.columns:
        if data[i].isnull().sum()>0:
            null_columns.append(i)


    
    # Select box for columns with null values
    return 


st.set_page_config(page_title="Data Cleaner App")

st.write("# Data Cleaner App")
st.write("A simple data cleaner app that can simplify the task of cleaning data.")

hr()

# File uploader for CSV files
uploaded_file = st.file_uploader("Upload CSV file here", type=["csv", "xls"])
hr()

if uploaded_file:
    try:
        # Load the uploaded file as a DataFrame
        df = pd.read_csv(uploaded_file)
        st.dataframe(df, use_container_width=True)

        st.write("# Basic Info of Your Data")
        count_data = df.count()

        tab1, tab2, tab3 = st.tabs(["Overview of data", "Explore text Data", "Date time"])

        with tab1:
            st.subheader("Select a Column for Basic Statistics")
            columns1 = categorized_cols(df)[0]
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
                    except Exception:
                        st.write("No mode found or error in calculating mode.")

        with tab2:
            columns_of_category = categorized_cols(df)[1]
            select_data = st.selectbox("Select Category to analyze", columns_of_category)
            if select_data:
                st.write(f"Total count: {df[select_data].count()}")

        with tab3:
            st.write("Feature Engineering placeholder")

        st.write("Chart to show distribution")
        sns.boxplot(df[selected_column])
        plt.show()

        hr()

        # Handle duplicates
        st.write("# Handle Duplicate")
        col1, col2 = st.columns(2)

        with col1:
            try:
                duplicated_count = check_duplicate(df)
                st.info(f"There are {duplicated_count} duplicate rows.")
            except Exception as e:
                st.warning("Could not check duplicates: " + str(e))

        with col2:
            if st.button("Remove Duplicates"):
                df.drop_duplicates(inplace=True)
                duplicated_count = check_duplicate(df)  # Update duplicate count

    except Exception as e:
        st.error(f"Error processing file: {e}")

    st.write("# Handling Null Values:")
    st.write(" ")

    # Tabs for different types of imputations
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Simple Impute", "Mean Imputation", "Median Imputation", "KNN Imputation", "Regression Imputation"])

    # Code to find columns with null values
    null_columns_list = [col for col in df.columns if df[col].isnull().sum() > 0]

    # ... (existing code)

    with tab1:
            col1, col2 = st.columns(2)
            with col1:
                imputation_methods = ["Simple Imputation", "Mean Imputation", "Median Imputation", "KNN Imputation", "Regression Imputation"]

                if imputation_methods==imputation_methods[0]:
                    pass
                else:
                    pass


else:
    st.warning("Please upload a CSV file to get started.")
