import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Type colors for badges ---
TYPE_COLORS = {
    "Normal": "#A8A77A",
    "Fire": "#EE8130",
    "Water": "#6390F0",
    "Electric": "#F7D02C",
    "Grass": "#7AC74C",
    "Ice": "#96D9D6",
    "Fighting": "#C22E28",
    "Poison": "#A33EA1",
    "Ground": "#E2BF65",
    "Flying": "#A98FF3",
    "Psychic": "#F95587",
    "Bug": "#A6B91A",
    "Rock": "#B6A136",
    "Ghost": "#735797",
    "Dragon": "#6F35FC",
    "Dark": "#705746",
    "Steel": "#B7B7CE",
    "Fairy": "#D685AD"
}

# Load Pokémon data
df = pd.read_csv("pokemon.csv")

# Create label like "001 - Bulbasaur"
df["label"] = df["pokedex_number"].astype(str).str.zfill(3) + " - " + df["name"]

# Initialize session state
if "current_pokemon" not in st.session_state:
    st.session_state.current_pokemon = df["label"].iloc[0]

# Dropdown selector
selected = st.selectbox(
    "Search Pokémon by number or name:",
    df["label"],
    index=int(df[df["label"] == st.session_state.current_pokemon].index[0])
)

# Update current Pokémon
st.session_state.current_pokemon = selected

# Extract number and name
index_str, pokemon_name = selected.split(" - ")
index = int(index_str)

# Styling for centered title
st.markdown("""<style> h1 {text-align: center;} </style>""", unsafe_allow_html=True)

# Layout: Previous button | Title | Next button
prev_col, title_col, next_col = st.columns([2, 6, 2])

# Previous button
with prev_col:
    if st.button("Previous"):
        prev_index = (index - 2) % df["pokedex_number"].max() + 1
        prev_label = df.loc[df["pokedex_number"] == prev_index, "label"].values[0]
        st.session_state.current_pokemon = prev_label
        st.rerun()

# Title
with title_col:
    st.title(selected)

# Next button
with next_col:
    if st.button("Next"):
        next_index = (index % df["pokedex_number"].max()) + 1
        next_label = df.loc[df["pokedex_number"] == next_index, "label"].values[0]
        st.session_state.current_pokemon = next_label
        st.rerun()

# Image URL
url = f"https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/{index_str}.png"

# Get stats
stats_cols = ["hp", "attack", "defense", "sp_attack", "sp_defense", "speed"]
pokemon_stats = df.loc[df["pokedex_number"] == index, stats_cols].iloc[0]

# Normalize stats to percentages
min_stats = df[stats_cols].min()
max_stats = df[stats_cols].max()
percentages = ((pokemon_stats - min_stats) / (max_stats - min_stats)) * 100

# Layout for image + stats
col1, col2 = st.columns([1, 2])

with col1:
    # Pokémon image
    st.image(url, width=220)

    # Get Pokémon types
    type1 = df.loc[df["pokedex_number"] == index, "type_1"].values[0]
    type2 = (
        df.loc[df["pokedex_number"] == index, "type_2"].values[0]
        if "type_2" in df.columns and not pd.isna(df.loc[df["pokedex_number"] == index, "type_2"].values[0])
        else None
    )

    # Badge rendering (single-line HTML to avoid escaping)
    def badge_html(type_name):
        color = TYPE_COLORS.get(type_name, "#999999")
        return f'<span style="display:inline-block;background-color:{color};color:white;font-weight:bold;padding:5px 12px;border-radius:12px;margin:0 5px;font-size:16px;">{type_name}</span>'

    badges = badge_html(type1)
    if type2:
        badges += badge_html(type2)

    # Center badges under image
    st.markdown(f"<div style='text-align:center;margin-top:10px'>{badges}</div>", unsafe_allow_html=True)

with col2:
    # Single-color bars (primary type)
    bar_color = TYPE_COLORS.get(type1, "#999999")

    fig, ax = plt.subplots(figsize=(9, 4))
    fig.patch.set_facecolor("#000000")
    ax.set_facecolor("#0e0000")
    ax.set_ylim(0, 100)
    ax.set_title("Stats", color="white", fontsize=20, pad=30)
    ax.tick_params(axis='x', colors='white')

    ax.bar(stats_cols, percentages, width=0.95, color=bar_color)
    st.pyplot(fig)