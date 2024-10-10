import streamlit as st

# Create columns with specified width ratios
col1, col2, col3 = st.columns([1, 2, 2])  # 1:2:1 ratio

# Add content to the first column
with col1:
    st.header("Column 1")
    st.button("Button 1")

# Add content to the second column
with col2:
    st.header("Column 2")
    st.text_input("Input here")

# Add content to the third column
with col3:
    st.header("Column 3")
    st.checkbox("Check me!")

# You can also add more elements below the columns if needed
st.write("This is below the columns.")
