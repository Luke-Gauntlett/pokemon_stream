import streamlit as st
import pandas as pd
import plotly.express as px


# Set the app title
st.title("Pokemon Streamlit Challenge")
# Load the Pokemon dataset
df = pd.read_csv("./pokemon.csv")
# Test
st.write(df.head(6))

# Get user input
pokedex_number = st.number_input(
                            "Enter a Pokedex number (e.g., 6 for Charizard),",
                            min_value=1,
                            step=1
                            )

# Filter to get the selected pokemon
selected_pokemon = df[df['pokedex_number'] == pokedex_number]

# Write an error is Pokemon isn't found
if selected_pokemon.empty:
    st.warning("No Pokemon found with that Pokemon number.")
else:
    # Get the name and height for the pokemon and store in a new DataFrame
    main_pokemon_name = selected_pokemon['name'].values[0].strip()
    main_pokemon_height = selected_pokemon['height_m'].values[0]
    main_pokemon_dict = {
        "name": main_pokemon_name,
        "height_m": main_pokemon_height
    }
    main_pokemon_df = pd.DataFrame([main_pokemon_dict])

    # Get a random selection of other pokemon and store in a new DataFrame
    name_col = "name"
    height_col = "height_m"
    # Drop any columns with missing name and height
    df_cleaned = df.dropna(subset=[name_col, height_col])
    # Set the number of randomly selected pokemon
    num_selection = 5
    # Select the pokemon from the dataframe
    randomly_selected_df = df_cleaned[[name_col, height_col]].sample(
                                                        n=num_selection,
                                                        random_state=42
                                                    )

    # Combine both dataframes
    combined_df = pd.concat([
                        main_pokemon_df,
                        randomly_selected_df],
                        ignore_index=True)
    name_order = combined_df['name'].tolist()

    # Create a new column to format height text
    combined_df['height_text'] = combined_df['height_m'].astype(str) + 'm'

    # Plot the graph
    fig = px.bar(combined_df,
                 x='height_m',
                 y='name',
                 title=(
                     f"Comparison of {main_pokemon_name}'s Height "
                     "to Other Pokemon"
                 ),
                 labels={
                            'name': 'Pokemon Name',
                            'height_m': 'Pokemon Height (m)'
                        },
                 text='height_text',
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
