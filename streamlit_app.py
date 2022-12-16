import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title('Hi this is a title')

streamlit.header('Hello again, this is now a header')

streamlit.text('Ahoy from further down, this is some text')

# Creating a fruit list
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Banana'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)


def get_fruityvice_date(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized


# New Section to display API response
streamlit.header("Fruityvice Fruit Advice!")

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please select a fruit to get info')    
  else:
    streamlit.dataframe(get_fruityvice_date(fruit_choice))
except URLError as e:
    streamlit.error()

# New section
streamlit.header("The fruit load list contains:")

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()

if streamlit.button('Get Fruit Load list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  streamlit.dataframe(get_fruit_load_list())
  my_cnx.close()
 
# New section #2

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('" + new_fruit + "')")
    return "Thanks for adding the new fruit " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?','Jackfruit')
if streamlit.button('Add that fruit'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  res = insert_row_snowflake(add_my_fruit)
  streamlit.write(res)
  my_cnx.close()
  
# streamlit.stop()


