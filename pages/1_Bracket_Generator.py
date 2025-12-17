import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from lib.bracket import Team, generate_bracket
from lib.storage import load_weights
from lib.render import bracket_html

st.set_page_config(page_title="Bracket Generator", layout="wide")

st.title("🏀 March Madness Bracket Generator")

uploaded = st.file_uploader("Upload teams CSV (team, region, seed, power)", type=["csv"])
if uploaded is None:
    st.info("Upload a CSV to begin.")
    st.stop()

df = pd.read_csv(uploaded)
required = {"team","region","seed","power"}
missing = required - set(df.columns.str.lower())
# normalize columns
df.columns = [c.lower() for c in df.columns]
missing = required - set(df.columns)
if missing:
    st.error(f"Missing columns: {sorted(missing)}")
    st.stop()

teams = [Team(row.team, row.region, int(row.seed)) for row in df.itertuples(index=False)]
default_power = {row.team: float(row.power) for row in df.itertuples(index=False)}

saved = load_weights()
power = default_power | saved  # saved overrides defaults

col1, col2, col3 = st.columns([1,1,2])
with col1:
    use_seed = st.toggle("Use reproducible seed", value=True)
with col2:
    seed = st.number_input("Seed", min_value=0, max_value=10_000_000, value=12345, step=1, disabled=not use_seed)
with col3:
    st.caption("Weights used = uploaded `power`, overridden by any saved slider weights.")

if st.button("🎲 Generate randomized bracket", type="primary"):
    rounds = generate_bracket(teams, power, seed=int(seed) if use_seed else None)
    st.session_state["rounds"] = rounds

rounds = st.session_state.get("rounds")
if rounds:
    components.html(bracket_html(rounds), height=900, scrolling=True)
else:
    st.warning("Click **Generate** to populate the bracket.")
