import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px 

#### Ruben's Branch
st.title("Find your Pokemon")

df = pd.read_csv("pokemon.csv")
check1 = False
check2 = False
user_number = st.text_input("Please enter a number between 1 and 898")
print(f"User input is: {user_number}" )
if user_number.isnumeric():
    check1 = True
    print('That is a number')
    if int(user_number) < 1 or int(user_number) > 898:
        st.write("The number needs to be between 1 and 898 Try Again!")
    else:
        check2 = True
else:
    st.write("That was not a number please try again!")

  
if check1 == True and check2 == True:
    st.write("Here is the information about your pokemon:")
    user_result = df.loc[df['pokedex_number'] == int(user_number),['name','height_m','weight_kg','type_1','type_2','ability_1','ability_2','ability_hidden']]
    st.dataframe(user_result)



#### Luke's Branch

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


#### Comfort's Branch
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

st.title("Pokémon Image")

selected = st.selectbox("Choose Pokémon", df['Pokemon'])

image_index = df.loc[df['Pokemon'] == selected, 'new_pokedex'].values[0]

img_url = f"https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/{image_index}.png"

st.image(img_url, caption=f"{selected}", use_container_width=True)


#### Ade's Branch
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
main_pokemon_weight = selected_pokemon['weight_kg']
main_pokemon_dict = {
    "name": main_pokemon_name,
    "weight_kg": main_pokemon_weight
}
main_pokemon_df = pd.DataFrame([main_pokemon_dict])

# Get a random selection of other pokemon and store in a new DataFrame
name_col = "name"
weight_col = "weight_kg"

# Drop any columns with missing name and height
df_cleaned = df.dropna(subset=[name_col, weight_col])

# Set the number of randomly selected pokemon
num_selection = 5

# Select the pokemon from the dataframe
randomly_selected_df = df_cleaned[[name_col, weight_col]].sample(
                                                    n=num_selection,
                                                    random_state=5
                                                )

# Combine both dataframes
combined_df = pd.concat([
                    main_pokemon_df,
                    randomly_selected_df],
                    ignore_index=True)
name_order = combined_df['name'].tolist()

# Create a new column to format height text
combined_df['weight_text'] = combined_df['weight_kg'].astype(str) + 'kg'

# Plot the graph
fig = px.bar(combined_df,
             x='weight_kg',
             y='name',
             title=(
                    f"Comparison of {main_pokemon_name}'s Weight "
                    "to Other Pokemon"
                ),
             labels={
                        'name': 'Pokemon Name',
                        'weight_kg': 'Pokemon Weight (kg)'
                    },
             text='weight_text',
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