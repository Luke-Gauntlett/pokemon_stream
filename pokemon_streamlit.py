import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


# Title
st.title("Find Your Pokémon!")

# Load and clean data
df = pd.read_csv("pokemon.csv")
df = df.iloc[:, :24]
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

# Display basic info
info_cols = [
    'name', 'height_m', 'weight_kg', 'type_1',
    'ability_1', 'ability_2', 'ability_hidden'
]
st.subheader("Pokémon Info")
st.dataframe(df.loc[df['Pokemon'] == selected_label, info_cols])

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

st.subheader("Pokémon Comparisons")
# Get the name for the selected Pokémon
main_pokemon_name = selected_name.strip()

# Choose a comparison metric
comparison_metric = st.selectbox(
    "Select metric to compare:",
    ["height_m", "weight_kg", "hp", "attack"]
)

# Get a random selection of other Pokémon (excluding the selected one)
num_selection = 5
randomly_selected_df = df[df['name'] != main_pokemon_name].dropna(
    subset=[comparison_metric]
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
}[comparison_metric]

combined_df['metric_text'] = (
    combined_df[comparison_metric].astype(str) + suffix
)

# Plot the graph
fig = px.bar(
    combined_df,
    x=comparison_metric,
    y='name',
    title=(
        f"Comparison of {main_pokemon_name} to Other Pokémon by "
        f"{comparison_metric.capitalize()}"
    ),
    labels={
        'name': 'Pokémon Name',
        comparison_metric: comparison_metric.capitalize()
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
