import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Title and description
st.title("Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Text input for the name on the order
name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be", name_on_order)

# Snowflake connection
# Ensure your Snowflake credentials are correctly set up in the .streamlit/secrets.toml
cnx = st.connection("snowflake")
session = cnx.session()

# Retrieve the list of fruit options from the database
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()

# Multiselect for choosing fruits
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    pd_df['FRUIT_NAME'],
    max_selections=5
)

if ingredients_list:
    st.write("You have selected:", ingredients_list)
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write(f'The search value for {fruit_chosen} is {search_on}.')

        # Fetching and displaying nutrition information
        try:
            fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_chosen.lower()}")
            if fruityvice_response.status_code == 200:
                fv_data = fruityvice_response.json()
                fv_df = pd.DataFrame([fv_data])
                st.subheader(f'{fruit_chosen} Nutrition Information')
                st.dataframe(fv_df)
      

    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success("Your Smoothie is ordered!", icon="✅")
    """

    st.write(my_insert_stmt)
    if st.button('Submit Order'):
        try:
            session.sql(my_insert_stmt).collect()
            st.success("Your Smoothie is ordered!", icon="✅")



