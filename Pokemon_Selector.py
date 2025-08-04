import streamlit as st 
import pandas as pd 
import plotly.express as px 

st.title("Find your Pokemon")

df = pd.read_csv("pokemon.csv")
check1 = False
check2 = False
user_number = st.text_input("Please enter a number between 1 and 898")
print(f"User input is: {user_number}" )
if user_number.isnumeric():
    check1 = True
    print('That is a number')
    if int(user_number) < 1 or int(user_number) > 898:
        st.write("The number needs to be between 1 and 898 Try Again!")
    else:
        check2 = True
else:
    st.write("That was not a number please try again!")

  
if check1 == True and check2 == True:
    st.write("Here is the information about your pokemon:")
    user_result = df.loc[df['pokedex_number'] == int(user_number),['name','height_m','weight_kg','type_1','type_2','ability_1','ability_2','ability_hidden']]
    st.dataframe(user_result)