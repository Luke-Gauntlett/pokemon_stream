# Find your Pokémon!: A Streamlit Pokemon Application

Welcome to **Find Your Pokémon**, a Streamlit-powered app that lets you compare any Pokémon to others based on **Height**, **Weight**, **HP**, **Attack**, etc. Whether you're figuring out who's the tallest, tankiest, or strongest in the gym, we've got you covered.

---

## 🔍 Features

- 🧾 Search by **Pokédex number**
- 🔀 Handle multiple forms (Mega Evolutions, anyone?)
- 📊 Compare a selected Pokémon to 5 others
- 🏋️ Choose metrics: `Height`, `Weight`, `HP`, or `Attack`
- 🎨 Beautiful, interactive bar charts (Plotly FTW)
- 🤖 Dynamic labels (like "1.7m", "80kg", etc.)

---

## 🚀 How to Run It

1. **Clone this repo**:
```bash
git clone https://github.com/Luke-Gauntlett/pokemon_stream.git
cd pokemon_stream
```
2. **Set up virtual environment**
```bash
python3 -m venv .venv
```
- For Windows
```bash
source .venv/Scripts/activate
```
- For MacOS/Linux
```bash
source .venv/bin/activate
```
3. **Install the dependencies**:
```bash
pip install -r requirements.txt
```
4. **Run the Streamlit app**:
```bash
streamlit run pokemon_streamlit.py
```