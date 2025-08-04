import streamlit as st
import pandas as pd

df = pd.read_csv('pokemon.csv')
df = df.iloc[:, :24]
df = df.drop(columns=['german_name', 'japanese_name', 'type_number', 'type_2'])
df = df.rename(columns={'Unnamed: 0': 'csv_index'})
df = df.set_index('csv_index')

df['dup_count'] = df.groupby('pokedex_number').cumcount()

df['new_pokedex'] = df.apply(
    lambda row: f"{str(row['pokedex_number']).zfill(3)}_f{row['dup_count']+1}" if row['dup_count'] > 0 else str(row['pokedex_number']).zfill(3),
    axis=1
)

df['Pokemon'] = df.apply(lambda row: f"{row['pokedex_number']:03d} - {row['name']}", axis=1)

def get_pokemon_image_url(index):
    # Format index as a 3-digit string (e.g., 001, 025, 150)
    index_str = str(index).zfill(3)
    return f"https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/{index_str}.png"

st.title("Pokémon Image")

selected = st.selectbox("Choose Pokémon", df['Pokemon'])

image_index = df.loc[df['Pokemon'] == selected, 'new_pokedex'].values[0]

img_url = f"https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/{image_index}.png"

st.image(img_url, caption=f"{selected}", use_column_width=True)

