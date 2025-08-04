import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load Pokémon dataset
df = pd.read_csv("pokemon.csv")

# Create label column: "001 - Bulbasaur"
df["label"] = df["pokedex_number"].astype(str).str.zfill(3) + " - " + df["name"]

# Dropdown sorted by number
selected_label = st.selectbox("Search Pokémon by name or number:", df["label"])

# Extract number and name
index_str, pokemon_name = selected_label.split(" - ")
index = int(index_str)

# Image URL
url = f"https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/{index_str}.png"

# Stats to display
stats_cols = ["hp", "attack", "defense", "sp_attack", "sp_defense", "speed"]
pokemon_stats = df.loc[df["pokedex_number"] == index, stats_cols].iloc[0]

# Min and max for normalization
min_stats = df[stats_cols].min()
max_stats = df[stats_cols].max()

# Normalize to percentage (0–100%)
normalized_stats = ((pokemon_stats - min_stats) / (max_stats - min_stats)) * 100

# Centered title
st.markdown(f"<h1 style='text-align: center;'>{selected_label}</h1>", unsafe_allow_html=True)

# Layout: image and graph side-by-side
col1, col2 = st.columns([1, 2])

with col1:
    st.image(url, caption=f"{selected_label}", width=250)

with col2:
    fig, ax = plt.subplots(figsize=(6, 3))  # narrower figure
    ax.bar(stats_cols, normalized_stats, width=0.4)  # thinner bars
    ax.set_ylim(0, 100)
    ax.set_ylabel("Stat % (Min–Max)")
    ax.set_title(f"{pokemon_name} Attack Stats")

    # Make bars almost touch
    ax.margins(x=0.02)

    # Add value labels
    for i, val in enumerate(normalized_stats):
        ax.text(i, val + 2, f"{val:.0f}%", ha="center")

    st.pyplot(fig)
