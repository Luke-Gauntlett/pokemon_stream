import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


# Title
st.title("Find Your Pokémon!")

# Load and clean data
df = pd.read_csv("pokemon.csv")
#df = df.iloc[:, :24]
df = df.drop(
    columns=['german_name', 'japanese_name', 'type_number', 'type_2'],
    errors='ignore'
)
df = df.rename(columns={'Unnamed: 0': '_'})
df = df.set_index('_')

# Handle duplicates
df['dup_count'] = df.groupby('pokedex_number').cumcount()
df['new_pokedex'] = df.apply(
    lambda row: (
        f"{str(row['pokedex_number']).zfill(3)}_f{row['dup_count']+1}"
        if row['dup_count'] > 0
        else str(row['pokedex_number']).zfill(3)
    ),
    axis=1
)


# Create display label
def format_pokemon_label(row):
    return f"{row['pokedex_number']:03d} - {row['name']}"


df['Pokemon'] = df.apply(format_pokemon_label, axis=1)

# Select Pokédex number
unique_numbers = sorted(df['pokedex_number'].unique())
selected_number = st.selectbox("Select Pokédex Number", unique_numbers)

# Select Pokémon name for that number
names_for_number = df[df['pokedex_number'] == selected_number]['name'].unique()
selected_name = st.selectbox("Select Pokémon Name", names_for_number)

# Get selected Pokémon row
selected_row = df[
    (df['pokedex_number'] == selected_number) &
    (df['name'] == selected_name)
].iloc[0]
selected_label = (
    f"{selected_row['pokedex_number']:03d} - {selected_row['name']}"
)
image_index = selected_row['new_pokedex']
img_url = (
    f"https://www.pokemon.com/static-assets/content-assets/cms2/"
    f"img/pokedex/full/{image_index}.png"
)

# Display image
st.image(img_url, caption=selected_label, use_container_width=True)

# Divider
st.markdown("---")

# Display basic info
select_columns = st.multiselect("What Attributes Would You Like To See? ",
options=df.columns.tolist(),
default=['name','height_m','weight_kg','type_1', 'ability_1', 'ability_2', 'ability_hidden']
)

user_result = df.loc[df['Pokemon'] == selected_label, select_columns]
st.subheader("Pokémon Info")
st.dataframe(user_result)

# Divider
st.markdown("---")
st.subheader("Pokémon Stats")

# Display stats chart
stats_cols = ["hp", "attack", "defense", "sp_attack", "sp_defense", "speed"]
pokemon_stats = selected_row[stats_cols]
min_stats = df[stats_cols].min()
max_stats = df[stats_cols].max()
normalized_stats = (
    (pokemon_stats - min_stats) / (max_stats - min_stats)
) * 100

# Display stats chart only
fig, ax = plt.subplots(figsize=(6, 3))
ax.bar(stats_cols, normalized_stats, width=0.4)
ax.set_ylim(0, 100)
ax.set_ylabel("Stat % (Min–Max)")
ax.set_title(f"{selected_name} Attack Stats")

for i, val in enumerate(normalized_stats):
    ax.text(i, val + 2, f"{val:.0f}%", ha="center")

st.pyplot(fig)

# Divider
st.markdown("---")

st.subheader("Pokémon Comparisons")
# Get the name for the selected Pokémon
main_pokemon_name = selected_name.strip()

# Choose a comparison metric
metric_options = {
    "Height (m)": "height_m",
    "Weight (kg)": "weight_kg",
    "Hit Points (HP)": "hp",
    "Attack (ATK)": "attack"
}
selected_display = st.selectbox(
    "Select metric to compare:",
    list(metric_options.keys())
)

# Get the actual column name
selected_column = metric_options[selected_display]

# Get a random selection of other Pokémon (excluding the selected one)
num_selection = 5
randomly_selected_df = df[df['name'] != main_pokemon_name].dropna(
    subset=[selected_column]
).sample(n=num_selection, random_state=42)

# Convert selected_row to DataFrame
selected_pokemon_df = pd.DataFrame([selected_row])

# Combine both DataFrames
combined_df = pd.concat(
    [selected_pokemon_df, randomly_selected_df],
    ignore_index=True
)

# Store the order of the Pokémon names
name_order = combined_df['name'].tolist()

# Format the metric text
suffix = {
    "height_m": "m",
    "weight_kg": "kg",
    "hp": " HP",
    "attack": " ATK"
}[selected_column]

combined_df['metric_text'] = (
    combined_df[selected_column].astype(str) + suffix
)

# Plot the graph
fig = px.bar(
    combined_df,
    x=selected_column,
    y='name',
    title=(
        f"Comparison of {main_pokemon_name} to Other Pokémon by "
        f"{selected_display}"
    ),
    labels={
        'name': 'Pokémon Name',
        selected_column: selected_display
    },
    text='metric_text',
    orientation='h',
    color='name'
)

fig.update_layout(
    yaxis=dict(categoryorder='array', categoryarray=name_order[::-1]),
    showlegend=False
)

st.plotly_chart(fig)


# Divider
st.markdown("---")

# Define type colors (you can expand this dictionary)
TYPE_COLORS = {
    "Normal": "#A8A77A", "Fire": "#EE8130", "Water": "#6390F0", "Electric": "#F7D02C",
    "Grass": "#7AC74C", "Ice": "#96D9D6", "Fighting": "#C22E28", "Poison": "#A33EA1",
    "Ground": "#E2BF65", "Flying": "#A98FF3", "Psychic": "#F95587", "Bug": "#A6B91A",
    "Rock": "#B6A136", "Ghost": "#735797", "Dragon": "#6F35FC", "Dark": "#705746",
    "Steel": "#B7B7CE", "Fairy": "#D685AD"
}

# Extract type effectiveness info from selected_row
general_info = selected_row.to_dict()
type_map = {
    col.replace("against_", "").capitalize(): val
    for col, val in general_info.items()
    if col.startswith("against_")
}

# Determine strengths and weaknesses
strong_types = [t for t, v in type_map.items() if v == 2.0]
weak_types = [t for t, v in type_map.items() if v < 1.0]

# Badge rendering function
def render_badges(types):
    badges = ""
    for t in types:
        color = TYPE_COLORS.get(t, "#999999")
        badges += (
            f'<span style="display:inline-block;background-color:{color};'
            f'color:white;font-weight:bold;padding:5px 12px;border-radius:12px;'
            f'margin:0 5px;font-size:16px;">{t}</span>'
        )
    return badges if badges else "<i>None</i>"

# Display Strong Against
st.markdown(
    f"""
    <div style='text-align:center; margin-top:20px;'>
        <h3 style='margin-bottom:10px;'>Strong Against</h3>
        {render_badges(strong_types)}
    </div>
    """,
    unsafe_allow_html=True
)

# Display Weak Against
st.markdown(
    f"""
    <div style='text-align:center; margin-top:20px;'>
        <h3 style='margin-bottom:10px;'>Weak Against</h3>
        {render_badges(weak_types)}
    </div>
    """,
    unsafe_allow_html=True
)
