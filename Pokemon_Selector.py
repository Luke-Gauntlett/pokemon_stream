import streamlit as st 
import pandas as pd 
import plotly.express as px 

st.title("Find your Pokemon")

df = pd.read_csv("pokemon.csv")

df['dup_count'] = df.groupby('pokedex_number').cumcount()

df['new_pokedex'] = df.apply(
    lambda row: f"{str(row['pokedex_number']).zfill(3)}_f{row['dup_count']+1}" if row['dup_count'] > 0 else str(row['pokedex_number']).zfill(3),
    axis=1
)

df['Pokemon'] = df.apply(lambda row: f"{row['pokedex_number']:03d} - {row['name']}", axis=1)

st.title("Pokémon Image")

selected = st.selectbox("Choose the name of your Pokémon", df['Pokemon'])
name = selected.split(" - ")[1]
user_result = df.loc[df['name'] == name,['name','height_m','weight_kg','type_1','type_2','ability_1','ability_2','ability_hidden']]

select_columns = st.multiselect(
    "What Attributes Would you like to see:",
    options = df.columns.tolist(),
    default=['name','height_m','weight_kg','type_1','type_2','ability_1','ability_2','ability_hidden']
)
user_result = df.loc[df['name'] == name, select_columns]

st.dataframe(user_result)