import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from lib.bracket import Team, generate_bracket
from lib.render import bracket_html

st.set_page_config(page_title="Bracket Generator", layout="wide")
st.title("🏀 Bracket Generator")

uploaded = st.file_uploader("Upload teams CSV (team, region, seed, power)", type=["csv"])

if uploaded is not None:
    df = pd.read_csv(uploaded)
    df.columns = [c.lower() for c in df.columns]

    required = {"team", "region", "seed", "power"}
    missing = required - set(df.columns)
    if missing:
        st.error(f"Missing columns: {sorted(missing)}")
        st.stop()

    # Store uploaded data in session so Weights page can use it without re-upload
    st.session_state["teams_df"] = df.copy()

    # Store defaults (from upload) in session
    st.session_state["defaults"] = {row.team: float(row.power) for row in df.itertuples(index=False)}

    st.success("Teams loaded into session. You can now adjust weights on the Team Power Weights page.")

df = st.session_state.get("teams_df")
if df is None:
    st.info("Upload your teams CSV to begin.")
    st.stop()

# Build team objects
teams = [Team(row.team, row.region, int(row.seed)) for row in df.itertuples(index=False)]

# Merge power: defaults overridden by session weights
default_power = st.session_state.get("defaults", {})
weights = st.session_state.get("weights", {})
power = default_power | weights

col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
with col1:
    use_seed = st.toggle("Use reproducible seed", value=True)
with col2:
    seed = st.number_input("Seed", min_value=0, max_value=10_000_000, value=12345, step=1, disabled=not use_seed)
with col3:
    show_debug = st.toggle("Show debug", value=False)
with col4:
    st.caption("Power used = uploaded defaults overridden by any in-session slider weights.")

cA, cB, cC = st.columns([1, 1, 2])
with cA:
    if st.button("🎲 Generate randomized bracket", type="primary"):
        rounds = generate_bracket(teams, power, seed=int(seed) if use_seed else None)
        st.session_state["rounds"] = rounds

with cB:
    if st.button("🧹 Clear bracket"):
        st.session_state["rounds"] = None

with cC:
    if st.button("↩️ Reset weights to uploaded defaults"):
        st.session_state["weights"] = {}
        st.success("Cleared in-session weight overrides.")

rounds = st.session_state.get("rounds")
if rounds:
    components.html(bracket_html(rounds), height=900, scrolling=True)

    if show_debug:
        st.subheader("Debug")
        st.write("Champion:", rounds["CHAMP"].name)
        st.write("Finalists:", [t.name for t in rounds["F2"]])
else:
    st.warning("Click **Generate randomized bracket** to populate the bracket.")
