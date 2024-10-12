import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statistics as sts
from sklearn.impute import KNNImputer

# Function to categorize DataFrame columns
def categorized_cols(df):
    """Categorize the columns into different types."""
    num_cols = df.select_dtypes(include=["int32", "int64", "float32", "float64"]).columns.tolist()
    categorical_col = df.select_dtypes(include=["object", "category", "string"]).columns.tolist()
    boolean_cols = df.select_dtypes(include=["bool"]).columns.tolist()
    date_time_cols = df.select_dtypes(include=["datetime64", "datetime", "timedelta", "timedelta64"]).columns.tolist()
    
    return num_cols, categorical_col, boolean_cols, date_time_cols

# Function to create a horizontal rule for visual separation
def hr():
    """Horizontal rule for separation."""
    st.markdown("<hr>", unsafe_allow_html=True)

# Function to check for duplicate rows
def check_duplicate(dataset):
    """Check for duplicate rows."""
    return dataset.duplicated().sum()

# Function to find columns containing null values
def null_column_finder(df):
    """Find and return a list of columns containing null values."""
    return [col for col in df.columns if df[col].isnull().sum() > 0]

# Streamlit configuration
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
        if "df" not in st.session_state:
            # Store the DataFrame in session_state to persist it across user interactions
            st.session_state.df = pd.read_csv(uploaded_file)
        
        df = st.session_state.df  # Use the DataFrame stored in session_state
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

        col1, col2 = st.columns(2)

        with col1:
            st.write("Chart to show distribution")
            fig, ax = plt.subplots(figsize=(4, 4))
            sns.boxplot(data=df, x=selected_column, ax=ax)
            st.pyplot(fig)

        with col2:
            st.write("Chart to show distribution")
            fig, ax = plt.subplots(figsize=(4, 4))
            sns.histplot(data=df, x=selected_column, bins=30, kde=True)
            st.pyplot(fig)

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
                st.session_state.df = df  # Update session state after removing duplicates
                duplicated_count = check_duplicate(df)  # Update duplicate count
                st.info(f"Duplicates removed! Now there are {duplicated_count} duplicate rows.")

    except Exception as e:
        st.error(f"Error processing file: {e}")

    st.write("# Handling Null Values:")
    st.write(" ")

    col1, col2 = st.columns(2)
    
    with col1:
        try:
            # Finding columns with null values
            null_columns = null_column_finder(df)
            imputation_type = st.selectbox("Select an imputation type", ["Simple Impute", "Mean Imputation", "Median Imputation", "KNN Imputation"])
            null_column_select = st.selectbox("Select column containing null values", null_columns)

            if imputation_type == "Simple Impute":
                imputer_value = st.number_input("Enter the imputer value", value=0)

                if st.button("Apply Imputation"):
                    df[null_column_select].fillna(imputer_value, inplace=True)
                    st.session_state.df = df  # Update the session state DataFrame
                    st.success(f"Null values in '{null_column_select}' have been filled with {imputer_value}.")
                    
                    # Update the null column list dynamically after imputation
                    null_columns = null_column_finder(df)
                    st.session_state.null_columns = null_columns  # Update session state

            elif imputation_type == "Mean Imputation":
                if st.button("Apply Imputation"):
                    df[null_column_select].fillna(df[null_column_select].mean(), inplace=True)
                    st.session_state.df = df  # Update the session state DataFrame

            elif imputation_type == "Median Imputation":
                if st.button("Apply Imputation"):
                    df[null_column_select].fillna(df[null_column_select].median(), inplace=True)
                    st.session_state.df = df  # Update the session state DataFrame

            elif imputation_type == "KNN Imputation":
                knn_value = st.number_input("Select the number of neighbors", value=5)
                
                if st.button("Apply Imputation"):
                    imputer = KNNImputer(n_neighbors=knn_value)
                    # Apply KNN imputation
                    df[null_column_select] = imputer.fit_transform(df[[null_column_select]])
                    st.session_state.df = df  # Update the session state DataFrame
          


        except Exception as e:
            st.info("No null values to handle or error in processing: " + str(e))

    with col2:
        # Display null counts for the selected column
        if null_column_select:
            null_value_count = df[null_column_select].isnull().sum()
            null_counts_df = pd.DataFrame({
                'Column Name': [null_column_select],
                'Null Count': [null_value_count]
            })
            st.write(null_counts_df)
        else:
            st.info("No null values to show.")

else:
    st.warning("Please upload a CSV file to get started.")
