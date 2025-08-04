import streamlit as st
import pandas as pd

def get_pokemon_image_url(index):
    # Format index as a 3-digit string (e.g., 001, 025, 150)
    index_str = str(index).zfill(3)
    return f"https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/{index_str}.png"

st.title("Pokémon Image")

index = st.number_input("Enter Pokémon Index Number", min_value=1, max_value=898, value=1)

img_url = get_pokemon_image_url(index)

st.image(img_url, caption=f"Pokémon #{str(index).zfill(3)}", use_column_width=True)

