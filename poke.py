import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

df = pd.read_csv("pokemon.csv")

# Create label like "001 - Bulbasaur for drop down"
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

# centered title
st.markdown("""<style> h1 {text-align: center;} </style>""", unsafe_allow_html=True)

# columns: Previous button | Title | Next button
prev_col, title_col, next_col = st.columns([2, 6, 2])

# Previous button
with prev_col:
    if st.button("Previous"):
        prev_index = (index - 2) % df["pokedex_number"].max() + 1
        prev_label = df.loc[df["pokedex_number"] == prev_index, "label"].values[0]
        st.session_state.current_pokemon = prev_label
        st.rerun()

# show title
with title_col:
    st.title(selected)

# Next button
with next_col:
    if st.button("Next"):
        next_index = (index % df["pokedex_number"].max()) + 1
        next_label = df.loc[df["pokedex_number"] == next_index, "label"].values[0]
        st.session_state.current_pokemon = next_label
        st.rerun()


url = f"https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/{index_str}.png"

# Get stats
stats_cols = ["hp", "attack", "defense", "sp_attack", "sp_defense", "speed"]
pokemon_stats = df.loc[df["pokedex_number"] == index, stats_cols].iloc[0]

# change stats to percentages
min_stats = df[stats_cols].min()
max_stats = df[stats_cols].max()
percentages = ((pokemon_stats - min_stats) / (max_stats - min_stats)) * 100

# Layout for image + stats
col1, col2 = st.columns([1, 2])

with col1:
    # show pokemon image
    st.image(url, width=220)

    # Get types
    type1 = df.loc[df["pokedex_number"] == index, "type_1"].values[0]
    type2 = (
        df.loc[df["pokedex_number"] == index, "type_2"].values[0]
        if "type_2" in df.columns and not pd.isna(df.loc[df["pokedex_number"] == index, "type_2"].values[0])
        else None
    )

    # show types with colour
    def badge_html(type_name):
        color = TYPE_COLORS.get(type_name, "#999999")
        return f'<span style="display:inline-block;background-color:{color};color:white;font-weight:bold;padding:5px 12px;border-radius:12px;margin:0 5px;font-size:16px;">{type_name}</span>'

    badges = badge_html(type1)
    if type2:
        badges += badge_html(type2)

    # badges under image
    st.markdown(f"<div style='text-align:center;margin-top:10px'>{badges}</div>", unsafe_allow_html=True)

with col2:
    # make graph type colour
    bar_color = TYPE_COLORS.get(type1, "#999999")

    # hide ugly bits and make others white
    fig, ax = plt.subplots(figsize=(9, 4))
    fig.patch.set_facecolor("#000000")
    ax.set_facecolor("#0e0000")
    ax.set_ylim(0, 100)
    ax.set_title("Stats", color="white", fontsize=20, pad=30)
    ax.tick_params(axis='x', colors='white')
    ax.bar(stats_cols, percentages, width=0.95, color=bar_color)
    
    #show graph
    st.pyplot(fig)

# divider
st.markdown("---")

pokemon_info = df.loc[df["pokedex_number"] == index].iloc[0]

egg_type = pokemon_info["egg_type_1"]
if not pd.isna(pokemon_info["egg_type_2"]):
    egg_type += f" / {pokemon_info['egg_type_2']}"

st.markdown(
    f"""
    <div style='text-align:center; font-size:18px;'>
        <b>Generation:</b> {pokemon_info['generation']} &nbsp;|&nbsp;
        <b>Height:</b> {pokemon_info['height_m']} m &nbsp;|&nbsp;
        <b>Weight:</b> {pokemon_info['weight_kg']} kg &nbsp;|&nbsp;
        <b>Catch Rate:</b> {pokemon_info['catch_rate']} &nbsp;|&nbsp;
        <b>Growth Rate:</b> {pokemon_info['growth_rate']} &nbsp;|&nbsp;
        <b>Egg Type:</b> {egg_type}
    </div>
    """,
    unsafe_allow_html=True
)

#divider
st.markdown("---")

# Map against_ columns to type names
type_map = {col.replace("against_", "").capitalize(): val for col, val in pokemon_info.items() if col.startswith("against_")}

# Strong = damage > 2.0, Weak = damage < 1.0
strong_types = [t for t, v in type_map.items() if v >= 2]
weak_types = [t for t, v in type_map.items() if v < 1]

def render_badges(types):
    badges = ""
    for type in types:
        color = TYPE_COLORS.get(type, "#999999")
        badges += f'<span style="display:inline-block;background-color:{color};color:white;font-weight:bold;padding:5px 12px;border-radius:12px;margin:0 5px;font-size:16px;">{type}</span>'
    return badges if badges else "<i>None</i>"

# Strong Against title
st.markdown(
    f"""
    <div style='text-align:center; margin-top:20px;'>
        <h3 style='margin-bottom:10px;'>Weak Against</h3>
        {render_badges(strong_types)}
    </div>
    """,
    unsafe_allow_html=True
)

# Weak Against title
st.markdown(
    f"""
    <div style='text-align:center; margin-top:20px;'>
        <h3 style='margin-bottom:10px;'>Strong Against</h3>
        {render_badges(weak_types)}
    </div>
    """,
    unsafe_allow_html=True
)





###################### experimental ########################################################

# --- Comparison Section ---
st.markdown("---")
st.header("Compare Pokémon")

# Multiselect for Pokémon (unlimited)
compare_pokemon = st.multiselect(
    "Select Pokémon to compare:",
    df["label"]
)

# Checkboxes for metrics
metrics = ["height_m", "weight_kg", "hp", "attack"]
metric_display_names = {
    "height_m": "Height (m)",
    "weight_kg": "Weight (kg)",
    "hp": "HP",
    "attack": "Attack"
}

# Show checkboxes
selected_metrics = []
cols = st.columns(4)  # One checkbox per metric
for i, metric in enumerate(metrics):
    if cols[i].checkbox(metric_display_names[metric], value=(metric in ["hp", "attack"])):
        selected_metrics.append(metric)

# Show comparison chart
if compare_pokemon and selected_metrics:
    compare_df = df[df["label"].isin(compare_pokemon)][["label"] + selected_metrics]

    # Create horizontal grouped bar chart
    fig, ax = plt.subplots(figsize=(10, 0.5 * len(compare_df)))  # Dynamic height
    y = range(len(compare_df))
    bar_height = 0.8 / len(selected_metrics)  # distribute bars evenly

    for i, metric in enumerate(selected_metrics):
        ax.barh(
            [p + i * bar_height for p in y],
            compare_df[metric],
            height=bar_height,
            label=metric_display_names[metric]
        )

    ax.set_yticks([p + bar_height * (len(selected_metrics) / 2) for p in y])
    ax.set_yticklabels(compare_df["label"])
    ax.invert_yaxis()  # Highest value at top
    ax.set_xlabel("Value")
    ax.set_title("Pokémon Comparison")
    ax.legend()

    st.pyplot(fig)
