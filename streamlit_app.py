import streamlit
import pandas as pd

streamlit.title('Hi this is a title')

streamlit.header('Hello again, this is now a header')

streamlit.text('Ahoy from further down, this is some text')

# Creating a fruit list
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)
