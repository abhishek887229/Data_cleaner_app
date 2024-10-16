import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statistics as sts
from sklearn.impute import KNNImputer
from sklearn.preprocessing import LabelEncoder,OrdinalEncoder
import io 
uploaded_file = None
xyzabc="new"
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
st.write("# Data Cleaner App ")
st.write("Easily clean and explore your data with a simple, user-friendly interface.")

hr()
st.write("if things not work as ussual click on reset button")
if st.button("Reset"):
    st.session_state.clear()  # Clear all session state
uploaded_file = st.file_uploader("Upload your CSV or Excel file here", type=["csv", "xls"])
st.write(" ")
if uploaded_file:
    try:
        # Load the uploaded file as a DataFrame
        if "df" not in st.session_state:
            # Store the DataFrame in session_state to persist it across user interactions
            st.session_state.df = pd.read_csv(uploaded_file)
        df = st.session_state.df 
        df_copy=df.copy() # Use the DataFrame stored in session_state
        st.dataframe(df_copy, use_container_width=True)

        st.write("# Basic Info of Data")
        count_data = df.count()

        tab1, tab2, tab3 = st.tabs(["Overview of Data", "Explore Text Data", "Date Time Data"])

        # Overview Tab
        with tab1:
            st.subheader("Select a Column for Basic Statistics")
            all_num_cols = categorized_cols(df)[0]
            selected_column = st.selectbox("Select a column", all_num_cols)

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
                    fig, ax = plt.subplots(figsize=(6,4))
                    sns.boxplot(data=df, x=selected_column, ax=ax)
                    plt.xticks(rotation=90)
                    st.pyplot(fig)

                with coly:
                    st.write("Histogram")
                    fig, ax = plt.subplots(figsize=(6,4))
                    sns.histplot(data=df, x=selected_column, bins=30, kde=True)
                    plt.xticks(rotation=90)
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
                    fig, ax = plt.subplots(figsize=(6,4))
                    
                    value_counts = df[value_select].value_counts()
                    total = value_counts.sum()
                    labels = [f"{idx}: {count} ({count / total * 100:.2f}%)" for idx, count in zip(value_counts.index, value_counts)]
                    
                    plt.pie(value_counts, labels=labels, autopct='%1.1f%%')
                    plt.xticks(rotation=90)
                    st.pyplot(fig)

                with col_chart2:
                    st.write(f"Bar Chart for {value_select}")
                    fig, ax = plt.subplots(figsize=(6, 4))
                    ax.bar(value_counts.index, value_counts.values)
                    ax.set_xlabel("Categories")
                    ax.set_ylabel("Count")
                    ax.set_title(f"Distribution of {value_select}")
                    plt.xticks(rotation=90)  # Rotate labels for better visibility
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
                    # Check if the selected column is categorical or numerical
                    if df[null_column_select].dtype in ['object', 'category', 'string']:
                        imputer_value = st.selectbox("Select a category to impute", df[null_column_select].unique())
                    else:
                        imputer_value = st.number_input("Enter the imputer value", value=0.0)

                    if st.button("Apply Simple Imputation"):
                        try:
                            df[null_column_select].fillna(imputer_value, inplace=True)
                            st.session_state.df = df
                            st.success(f"Null values in '{null_column_select}' filled with {imputer_value}.")
                        except Exception as e:
                            st.error(f"Error during simple imputation: {e}")

                elif imputation_type == "Mean Imputation":
                    if st.button("Apply Mean Imputation"):
                        try:
                            df[null_column_select].fillna(df[null_column_select].mean(), inplace=True)
                            st.session_state.df = df
                            st.success(f"Null values in '{null_column_select}' filled with mean.")
                        except Exception as e:
                            st.error(f"Error during mean imputation: {e}")

                elif imputation_type == "Median Imputation":
                    if st.button("Apply Median Imputation"):
                        try:
                            df[null_column_select].fillna(df[null_column_select].median(), inplace=True)
                            st.session_state.df = df
                            st.success(f"Null values in '{null_column_select}' filled with median.")
                        except Exception as e:
                            st.error(f"Error during median imputation: {e}")

                elif imputation_type == "KNN Imputation":
                    knn_value = st.number_input("Number of Neighbors", value=5)
                    if st.button("Apply KNN Imputation"):
                        try:
                            imputer = KNNImputer(n_neighbors=knn_value)
                            df[null_column_select] = imputer.fit_transform(df[[null_column_select]])
                            st.session_state.df = df
                            st.success(f"KNN imputation applied to '{null_column_select}'.")
                        except Exception as e:
                            st.error(f"Error during KNN imputation: {e}")

        with col2:
            # Check if null_column_select is not None before displaying null values
            if null_column_select:
                null_value_count = df[null_column_select].isnull().sum()
                null_counts_df = pd.DataFrame({
                    'Column Name': [null_column_select],
                    'Null Count': [null_value_count]
                })
                st.write(null_counts_df)
        
        
        hr()
        st.write("# Data Transformation")
        st.write(" ")
        st.write(" ")
        col1_for_transformation,col2_for_transformation=st.columns(2)

        with col1_for_transformation:

            st.write("#### Normalization and Standardization for Data")
            
            Normal_or_standard=st.selectbox("select what kind of Transformation you want?",["Normalization","Standardization"])
            Normalization_select=st.selectbox("select a column for transformation",all_num_cols)
            new_cols=f"{Normalization_select}_Normalize"
            std_new_cols=f"{Normalization_select}_standardize"
            button_to_appply_transformation=st.button("Apply")
            try :
                if Normalization_select and Normal_or_standard=="Normalization" and button_to_appply_transformation:
                    df[new_cols]=(df[Normalization_select]-df[Normalization_select].min()/(df[Normalization_select].max()-df[Normalization_select].min()))
                    st.session_state.df=df
                elif Normalization_select and Normal_or_standard=="Standardization" and button_to_appply_transformation:
                    df[std_new_cols]=(df[Normalization_select]-df[Normalization_select].mean())/df[Normalization_select].std()
                    st.session_state.df=df
                else:
                    st.session_state.df=df

            except Exception as e:
                st.warning(e)



        with col2_for_transformation:
            st.write("#### Data Encoding for Categorical Data")
            encoder_type=st.selectbox("select method of encoding",["labelEncoder","Ordinal Encoder","One-hot-encoder"])
            columns_for_encoding=st.selectbox("select the column you want to apply encoding",columns_of_category)
            apply_change=st.button("apply Change")
            new_category_column_name=f"{columns_for_encoding}_{encoder_type}"
            if (encoder_type=="labelEncoder") and (apply_change):

                df["mid_process_encoder"]=pd.factorize(df[columns_for_encoding])[0]

                le=LabelEncoder()
                df[new_category_column_name]=le.fit_transform(df["mid_process_encoder"])
                #drop mid process encoder
                df.drop(columns=["mid_process_encoder"],inplace=True)
                st.session_state.df=df
                
            elif encoder_type == "One-hot-encoder" and (apply_change):
                try:
                    df = pd.get_dummies(df, columns=[columns_for_encoding], drop_first=True)  # Avoid dummy variable trap
                    st.session_state.df = df
                    st.success(f"One-Hot Encoding applied to '{columns_for_encoding}'.")
                except Exception as e:
                    st.error(f"Error during One-Hot Encoding: {e}")

            elif (encoder_type=="Ordinal Encoder") and (apply_change):

                st.write("will update soon")
            
        st.dataframe(st.session_state.df, use_container_width=True)
        st.write("### Visualization of Encoded Categories")
    
    # Check if any new columns were created for visual representation
        if encoder_type == "One-hot-encoder":
        # Show the names of the new one-hot encoded columns
            new_columns = [col for col in df.columns if columns_for_encoding in col]
            if new_columns:
                fig, ax = plt.subplots(figsize=(7,3))
                df[new_columns].sum().plot(kind='bar', ax=ax)
                ax.set_title(f"Sum of One-Hot Encoded Features for '{columns_for_encoding}'")
                ax.set_ylabel("Count")
                ax.set_xlabel("Encoded Categories")
                plt.xticks(rotation=90)
                st.pyplot(fig)
            else:
                pass
        else:
            pass



        hr()
        st.write("# Remove columns")

        # Select columns to drop
        columns = df.columns.tolist()
        select_columns = st.multiselect("Select columns to drop", columns)

        # Drop selected columns from the DataFrame
        if select_columns:
            df.drop(columns=select_columns, inplace=True)
            st.success(f"Dropped columns: {', '.join(select_columns)}")
            st.session_state.df=df
        else:
            st.session_state.df=df

        # Display the updated DataFrame
        st.dataframe(df.head())

            


        # Download button for modified CSV
        hr()
        st.write("### Download Your Cleaned Data")
        
        # Convert the modified DataFrame to CSV in memory buffer
        if "df" in st.session_state:
            csv_buffer = io.StringIO()
            st.session_state.df.to_csv(csv_buffer, index=False)  # Ensure this DataFrame is the one you want to export
            csv_data = csv_buffer.getvalue()

            st.download_button(
                label="Download Cleaned CSV",
                data=csv_data,
                file_name="cleaned_data.csv",
                mime="text/csv",
            )
        else:
            st.session_state.df=df
            st.experimental_rerun()
        



    except Exception as e:
        st.error(f"Error processing file: {e}")

else:
    st.warning("Please upload a CSV or Excel file to get started.") 
