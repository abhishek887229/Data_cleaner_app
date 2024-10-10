# import streamlit as st
# import pandas as pd

# df=pd.read_csv("/workspaces/streamlit_app/Customers.csv")

# st.dataframe(df,use_container_width=True)

# for i in df.columns:
#     st.write(i)

import streamlit as st

st.title('Streamlit Multiselect Example')

# Define options for multiselect
options = ['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry', 'Fig', 'Grape']

# Create a multiselect widget
selected_fruits = st.multiselect('Select your favorite fruits:', options)

# Display the selected fruits
if selected_fruits:
    st.write('You selected:', ', '.join(selected_fruits))
else:
    st.write('No fruits selected.')

st.write(selected_fruits)
