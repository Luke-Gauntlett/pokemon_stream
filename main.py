import streamlit as st
import pandas as pd
import plotly.express as px


# Set the app title
st.title("Pokemon Streamlit Challenge")
# Load the Pokemon dataset
df = pd.read_csv("./pokemon.csv")
# # Test
# st.write(df.head(10))

# Get user input
pokedex_number = st.number_input(
                            "Enter a Pokedex number (e.g., 6 for Charizard),",
                            min_value=1,
                            step=1
                            )

# Filter to get the selected pokemon
matching_pokemon = df[df['pokedex_number'] == pokedex_number]

selected_pokemon = None

# Write an error is Pokemon isn't found
if matching_pokemon.empty:
    st.warning("No Pokemon found with that Pokemon number.")

elif len(matching_pokemon) == 1:
    selected_pokemon = matching_pokemon.iloc[0]

# Handle multiple matches (e.g., Charizard, Mega Charizard X, etc.)
else:
    form_options = matching_pokemon['name'].unique().tolist()
    selected_form = st.selectbox(
                            "Multiple Pokemon forms found. Please choose one:",
                            form_options
                            )
    selected_row = matching_pokemon[
                            matching_pokemon['name'] == selected_form]
    if not selected_row.empty:
        selected_pokemon = selected_row.iloc[0]
    else:
        st.error("Something went wrong selecting the form.")

if selected_pokemon is not None:
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
                                                        random_state=42
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
