import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('pokemon.csv')
df = df.iloc[:, :24]
df = df.drop(columns=['german_name', 'japanese_name', 'type_number', 'type_2'])
df = df.rename(columns={'Unnamed: 0': 'csv_index'})
df = df.set_index('csv_index')

df['dup_count'] = df.groupby('pokedex_number').cumcount()

df['new_pokedex'] = df.apply(
    lambda row: (
        f"{str(row['pokedex_number']).zfill(3)}_f{row['dup_count']+1}"
        if row['dup_count'] > 0
        else str(row['pokedex_number']).zfill(3)
    ),
    axis=1
)

df['Pokemon'] = df.apply(
                    lambda row: f"{row['pokedex_number']:03d} - {row['name']}",
                    axis=1)


def get_pokemon_image_url(index):
    # Format index as a 3-digit string (e.g., 001, 025, 150)
    index_str = str(index).zfill(3)
    return (
        f"https://www.pokemon.com/static-assets/content-assets/"
        f"cms2/img/pokedex/full/{index_str}.png"
    )


st.title("Pokémon Image")

selected = st.selectbox("Choose Pokémon", df['Pokemon'])

image_index = df.loc[df['Pokemon'] == selected, 'new_pokedex'].values[0]

img_url = (
    f"https://www.pokemon.com/static-assets/content-assets/"
    f"cms2/img/pokedex/full/{image_index}.png"
)

st.image(img_url, caption=f"{selected}", use_container_width=True)


# Get user input
pokemon_name = df.loc[df['Pokemon'] == selected, 'name'].values[0]

# Filter to get the selected pokemon
matching_pokemon = df[df['name'] == pokemon_name]

# Store the details of the matched pokemon in a series
selected_pokemon = matching_pokemon.iloc[0]

# Get the name and height for the pokemon and store in a new DataFrame
main_pokemon_name = selected_pokemon['name'].strip()
# main_pokemon_weight = selected_pokemon['weight_kg']
# main_pokemon_dict = {
#     "name": main_pokemon_name,
#     "weight_kg": main_pokemon_weight
# }
# main_pokemon_df = pd.DataFrame([main_pokemon_dict])

# Choose a comparison metric
comparison_metric = st.selectbox(
    "Select metric to compare:",
    ["height_m", "weight_kg", "hp", "attack"]
)

# Get a random selection of other pokemon and store in a new DataFrame
# name_col = "name"
# weight_col = "weight_kg"

# # Drop any columns with missing name and height
# df_cleaned = df.dropna(subset=[name_col, weight_col])

# Set the number of randomly selected pokemon
num_selection = 5

# Select the pokemon from the dataframe
randomly_selected_df = df[
    df['name'] != main_pokemon_name
].sample(
    n=num_selection,
    random_state=5
)

# Combine both dataframes
# Convert the selected_pokemon series to a DataFrame
selected_pokemon_df = pd.DataFrame([selected_pokemon])
combined_df = pd.concat([
                    selected_pokemon_df,
                    randomly_selected_df],
                    ignore_index=True)

# Store the order of the pokemon names in a list
name_order = combined_df['name'].tolist()

# Format the text for every metric
suffix = {
            "height_m": "m",
            "weight_kg": "kg",
            "hp": " HP",
            "attack": " ATK"
        }[comparison_metric]

combined_df['metric_text'] = (
    combined_df[comparison_metric].astype(str) + suffix
)
st.write(combined_df)

# Plot the graph
fig = px.bar(combined_df,
             x=comparison_metric,
             y='name',
             title=(
                    f"Comparison of {main_pokemon_name}"
                    f"to Other Pokemon by {comparison_metric.capitalize()}"
                ),
             labels={
                        'name': 'Pokemon Name',
                        comparison_metric: comparison_metric.capitalize()
                    },
             text='metric_text',
             orientation='h',
             color='name'
             )
fig.update_layout(
    yaxis=dict(
        categoryorder='array',
        categoryarray=name_order[::-1]
    ),
    showlegend=False
)
st.plotly_chart(fig)
