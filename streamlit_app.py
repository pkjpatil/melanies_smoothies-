# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)

#option = st.selectbox('What is your favorite fruit?', 
#                     ('Banana', 'Strawberries', 'Peaches'))
#st.write('Your favorite fruit is ', option)

name_on_smoothie = st.text_input('Name on Smoothie:')
st.write('Name on the smoothie will be: ', name_on_smoothie)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('search_on'))
#st.dataframe(data=my_dataframe, use_container_width=True)

#Convert to pandas dataframe
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)

ingredients_list = st.multiselect('Choose upto 5 ingredients', my_dataframe, max_selections=5)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen, ' is ', search_on, '.')
        
        # URL_string = 'https://fruityvice.com/api/fruit/'+fruit_chosen
        st.subheader=(fruit_chosen + ' Nutrition information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+search_on)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_smoothie+"""')"""
    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+name_on_smoothie+'!', icon="✅")


#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response.json())
#fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    
