import streamlit as st
import pandas as pd
import statistics as sts

def categorized_cols(dataframe):
    num_cols=df.select_dtypes(include=["int32","int64","float32","float64"]).columns.tolist()
    categorical_col=df.select_dtypes(include=["object","category","string"]).columns.tolist()
    boolean_cols=df.select_dtypes(include=["bool"]).columns.tolist()
    date_time_cols=df.select_dtypes(include=["datetime64","datetime","timedelta","timedelta64"]).columns.tolist()

    return num_cols,categorical_col,boolean_cols,date_time_cols 


def hr():
    st.markdown("<hr>", unsafe_allow_html=True)

def check_duplicate(dataset):
    return dataset.duplicated().sum()

st.set_page_config(page_title="Data Cleaner App")

st.write("# Data Cleaner App")
st.write("A simple data cleaner app that can simplify the task of cleaning data.")

# Adding a horizontal line
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

        tab1, tab2, tab3 = st.tabs(["Over view of data", "Explore text Data", "Date time"])

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

        # with tab2:
        #     st.title("Select Columns You Want to Drop")

        #     # Select columns to drop
        #     columns = df.columns.tolist()
        #     select_columns = st.multiselect("Select columns to drop", columns)

        #     # Drop selected columns from the DataFrame
        #     if select_columns:
        #         df.drop(columns=select_columns, inplace=True)
        #         st.success(f"Dropped columns: {', '.join(select_columns)}")

        #     # Display the updated DataFrame
        #     st.dataframe(df.head())

        #     hr()

        #     st.title("# Change Your Data Type")

        #     col1, col2, col3 = st.columns([2, 1, 1])

        #     try:
        #         with col1:
        #             select_cols = st.selectbox("Select column", df.columns.tolist())
        #             st.write("Selected column:", select_cols)

        #         with col2:
        #             data_type = ['int64', 'float64', 'bool', 'object', 'string', 'datetime64[ns]', 'timedelta[ns]']
        #             select_datatype = st.selectbox("Select Data Type", data_type)
        #             st.write("Selected Data Type:", select_datatype)

        #         with col3:
        #             if st.button("Apply"):
        #                 try:
        #                     # Change the data type of the selected column
        #                     df[select_cols] = df[select_cols].astype(select_datatype)
        #                     st.success(f"Successfully converted '{select_cols}' to data type '{select_datatype}'")
        #                 except Exception as e:
        #                     st.error(f"Error converting '{select_cols}': {e}")
        #     except Exception:
        #         st.warning("Some invalid data type is present. Please remove it.")

        #     # Display updated data types
        #     st.write("Data Types of Each Column:")
        #     for col in df.columns:
        #         st.write(f"{col}: {df[col].dtype}")
        with tab2:
            columns_of_category=categorized_cols(df)[1]
            select_data=st.selectbox("select Category to analyze",columns_of_category)
            if select_data:
                
                st.write(f"total count {df[select_data].count()}")
            else:
                pass

        with tab3:
            st.write("Feature Engineering placeholder")

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
    
            else:
                pass

    except Exception as e:
        st.error(f"Error processing file: {e}")
    
    st.write("# handling Null Values:-")
    st.write(" ")
    tab1,tab2,tab3,tab4,tab5=st.tabs(["simple impute","mean imputation","median imputation","KNN imputation","regression Imptation"])

    with tab1:
        x=st.number_input("enter a number you want to replace Null values with")
        if x:
            df.fillna(x)
        else:
            pass

else:
    st.warning("Please upload a CSV file to get started.")
