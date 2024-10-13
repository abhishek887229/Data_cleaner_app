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

# Streamlit app configuration
st.set_page_config(page_title="Data Cleaner App", layout="wide")
st.write("# Data Cleaner App")
st.write("Easily clean and explore your data with a simple, user-friendly interface.")

hr()

# File uploader for CSV or Excel files
uploaded_file = st.file_uploader("Upload your CSV or Excel file here", type=["csv", "xls"])
hr()

if uploaded_file:
    try:
        # Load the uploaded file as a DataFrame
        if "df" not in st.session_state:
            # Store the DataFrame in session_state to persist it across user interactions
            st.session_state.df = pd.read_csv(uploaded_file)
        
        df = st.session_state.df  # Use the DataFrame stored in session_state
        st.dataframe(df, use_container_width=True)

        st.write("## Basic Info of Your Data")
        count_data = df.count()

        tab1, tab2, tab3 = st.tabs(["Overview of Data", "Explore Text Data", "Date Time Data"])

        # Overview Tab
        with tab1:
            st.subheader("Select a Column for Basic Statistics")
            columns1 = categorized_cols(df)[0]
            selected_column = st.selectbox("Select a column", columns1)

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
                
                # Chart for distribution
                colx, coly = st.columns(2)

                with colx:
                    st.write(f"Distribution Chart for {selected_column}")
                    fig, ax = plt.subplots(figsize=(4, 4))
                    sns.boxplot(data=df, x=selected_column, ax=ax)
                    st.pyplot(fig)

                with coly:
                    st.write("Histogram")
                    fig, ax = plt.subplots(figsize=(4, 4))
                    sns.histplot(data=df, x=selected_column, bins=30, kde=True)
                    st.pyplot(fig)

        # Explore Text Data Tab
        with tab2:
            st.subheader("Explore Text Data")
            columns_of_category = categorized_cols(df)[1]
            col1, col2, col3 = st.columns(3)
            value_select = st.selectbox("Select Categorical Column", columns_of_category)
            
            if value_select:
                with col1:
                    st.write("Value Count")
                    st.write(df[value_select].count())

                with col2:
                    st.write("Unique Values")
                    st.write(df[value_select].unique())

                with col3:
                    st.write("Value Frequency")
                    st.write(df[value_select].value_counts())

                # Charts for categorical data
                col_chart1, col_chart2 = st.columns(2)

                with col_chart1:
                    st.write(f"Pie Chart for {value_select}")
                    fig, ax = plt.subplots(figsize=(4, 4))
                    
                    value_counts = df[value_select].value_counts()
                    total = value_counts.sum()
                    labels = [f"{idx}: {count} ({count / total * 100:.2f}%)" for idx, count in zip(value_counts.index, value_counts)]
                    
                    plt.pie(value_counts, labels=labels, autopct='%1.1f%%')
                    st.pyplot(fig)

                with col_chart2:
                    st.write(f"Bar Chart for {value_select}")
                    fig, ax = plt.subplots(figsize=(4, 4))
                    ax.bar(value_counts.index, value_counts.values)
                    ax.set_xlabel("Categories")
                    ax.set_ylabel("Count")
                    ax.set_title(f"Distribution of {value_select}")
                    st.pyplot(fig)

        # Date Time Data Tab (To be implemented)
        with tab3:
            st.write("Date time handling will be updated soon.")

        hr()

        # Handle duplicates
        st.write("## Handle Duplicates")
        col1, col2 = st.columns(2)

        with col1:
            duplicated_count = check_duplicate(df)
            st.info(f"There are {duplicated_count} duplicate rows.")

        with col2:
            if st.button("Remove Duplicates"):
                df.drop_duplicates(inplace=True)
                st.session_state.df = df  # Update session state after removing duplicates
                duplicated_count = check_duplicate(df)  # Update duplicate count
                st.info(f"Duplicates removed! Now there are {duplicated_count} duplicate rows.")

        hr()

        # Handling null values
        st.write("## Handling Null Values")
        col1, col2 = st.columns(2)
        
        # Initialize null_column_select as None to avoid referencing before assignment
        null_column_select = None
        
        with col1:
            null_columns = null_column_finder(df)
            if null_columns:
                imputation_type = st.selectbox("Select Imputation Type", ["Simple Impute", "Mean Imputation", "Median Imputation", "KNN Imputation"])
                null_column_select = st.selectbox("Select Column", null_columns)

                if imputation_type == "Simple Impute":
                    imputer_value = st.number_input("Enter the imputer value", value=0)
                    if st.button("Apply Simple Imputation"):
                        df[null_column_select].fillna(imputer_value, inplace=True)
                        st.session_state.df = df
                        st.success(f"Null values in '{null_column_select}' filled with {imputer_value}.")
                
                elif imputation_type == "Mean Imputation":
                    if st.button("Apply Mean Imputation"):
                        df[null_column_select].fillna(df[null_column_select].mean(), inplace=True)
                        st.session_state.df = df

                elif imputation_type == "Median Imputation":
                    if st.button("Apply Median Imputation"):
                        df[null_column_select].fillna(df[null_column_select].median(), inplace=True)
                        st.session_state.df = df

                elif imputation_type == "KNN Imputation":
                    knn_value = st.number_input("Number of Neighbors", value=5)
                    if st.button("Apply KNN Imputation"):
                        imputer = KNNImputer(n_neighbors=knn_value)
                        df[null_column_select] = imputer.fit_transform(df[[null_column_select]])
                        st.session_state.df = df

        with col2:
            # Check if null_column_select is not None before displaying null values
            if null_column_select:
                null_value_count = df[null_column_select].isnull().sum()
                null_counts_df = pd.DataFrame({
                    'Column Name': [null_column_select],
                    'Null Count': [null_value_count]
                })
                st.write(null_counts_df)

    except Exception as e:
        st.error(f"Error processing file: {e}")

else:
    st.warning("Please upload a CSV or Excel file to get started.")
