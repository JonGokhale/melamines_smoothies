import streamlit as st
from snowflake.snowpark.functions import col

# Title and description
st.title("Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Text input for the name on the order
name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be", name_on_order)

# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Retrieve the list of fruit options from the database
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).collect()
fruit_names = [row['FRUIT_NAME'] for row in my_dataframe]

# Multiselect widget for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_names,
    max_selections=5
)

# Display selected ingredients
if ingredients_list:
    st.write(ingredients_list)
    
    ingredients_string = ', '.join(ingredients_list)

    # Create the insert statement using parameterized queries
    my_insert_stmt = f"""INSERT INTO smoothies.public.orders (ingredients, name_on_order)
                         VALUES ('{ingredients_string}', '{name_on_order}')"""
    
    st.write(my_insert_stmt)

    # Button to submit the order
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered!", icon="✅")



#New section to displey fruityvice nutrition information
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response.json())
