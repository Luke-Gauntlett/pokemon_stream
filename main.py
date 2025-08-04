import streamlit as st
import pandas as pd

# Set the app title
st.title("Pokemon Streamlit Challenge")
# Load the Pokemon dataset
df = pd.read_csv("./pokemon.csv")
