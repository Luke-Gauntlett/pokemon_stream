import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load Pokémon dataset
df = pd.read_csv("pokemon.csv")

# Sort by Pokédex number numerically
df = df.sort_values("pokedex_number").reset_index(drop=True)

# Create label without leading zeros
df["label"] = df["pokedex_number"].astype(str) + " - " + df["name"]

# Search box
search_input = st.text_input("Search Pokémon by name or number:")

# Filter results
if search_input:
    if search_input.isdigit():
        num = int(search_input)
        # Exact match first
        exact = df[df["pokedex_number"] == num]
        # Then numbers starting with input
        starts_with = df[
            df["pokedex_number"].astype(str).str.startswith(search_input)
            & (df["pokedex_number"] != num)
        ]
        # Then names containing input
        name_matches = df[df["name"].str.contains(search_input, case=False, na=False)]
        filtered_df = pd.concat([exact, starts_with, name_matches]).drop_duplicates(
            subset=["pokedex_number", "name"]
        )
    else:
        filtered_df = df[df["name"].str.contains(search_input, case=False, na=False)]
else:
    filtered_df = df

# Style for results container
st.markdown(
    """
    <style>
    .result-item {
        padding: 4px;
        border-bottom: 1px solid #ddd;
        cursor: pointer;
    }
    .result-item:hover {
        background-color: #f0f0f0;
    }
    .results-box {
        max-height: 250px;
        overflow-y: auto;
        border: 1px solid #ccc;
        border-radius: 4px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

selected_pokemon = None

# Display filtered results as clickable list
st.markdown('<div class="results-box">', unsafe_allow_html=True)
for _, row in filtered_df.iterrows():
    label = f"{row['pokedex_number']} - {row['name']}"
    if st.button(label, key=f"{row['pokedex_number']}-{row['name']}"):
        selected_pokemon = row
st.markdown('</div>', unsafe_allow_html=True)

# Show Pokémon details when selected
if selected_pokemon is not None:
    index = selected_pokemon["pokedex_number"]
    pokemon_name = selected_pokemon["name"]

    # Image URL (zero-padded for official images)
    image_index_str = str(index).zfill(3)
    url = f"https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/{image_index_str}.png"

    # Stats
    stats_cols = ["hp", "attack", "defense", "sp_attack", "sp_defense", "speed"]
    pokemon_stats = df.loc[
        (df["pokedex_number"] == index) & (df["name"] == pokemon_name),
        stats_cols
    ].iloc[0]

    # Normalize stats
    min_stats = df[stats_cols].min()
    max_stats = df[stats_cols].max()
    normalized_stats = ((pokemon_stats - min_stats) / (max_stats - min_stats)) * 100

    # Centered title
    st.markdown(f"<h1 style='text-align: center;'>{index} - {pokemon_name}</h1>", unsafe_allow_html=True)

    # Layout: image and graph
    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(url, caption=f"{index} - {pokemon_name}", width=200)

    with col2:
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.bar(stats_cols, normalized_stats, width=0.4)
        ax.set_ylim(0, 100)
        ax.set_ylabel("Stat % (Min–Max)")
        ax.set_title(f"{pokemon_name} Attack Stats")
        ax.margins(x=0.02)

        for i, val in enumerate(normalized_stats):
            ax.text(i, val + 2, f"{val:.0f}%", ha="center")

        st.pyplot(fig)
