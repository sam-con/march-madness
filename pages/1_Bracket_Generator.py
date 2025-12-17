import streamlit as st
import streamlit.components.v1 as components

from lib.bracket import Team, generate_bracket
from lib.render import bracket_html

st.set_page_config(page_title="Bracket Generator", layout="wide")
st.title("🏀 Bracket Generator")

df = st.session_state["teams_df"]

teams = [
    Team(row.team, row.region, int(row.seed))
    for row in df.itertuples(index=False)
]

# Merge defaults + session overrides
default_power = st.session_state["defaults"]
weights = st.session_state["weights"]
power = default_power | weights

col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
with col1:
    use_seed = st.toggle("Use reproducible seed", value=False)
with col2:
    seed = st.number_input(
        "Seed",
        min_value=0,
        max_value=10_000_000,
        value=12345,
        step=1,
        disabled=not use_seed
    )
with col3:
    show_debug = st.toggle("Show debug", value=False)
with col4:
    st.caption("Power = CSV defaults overridden by in-session sliders")

c1, c2, c3 = st.columns([1, 1, 2])
with c1:
    if st.button("🎲 Generate randomized bracket", type="primary"):
        st.session_state["rounds"] = generate_bracket(
            teams,
            power,
            seed=int(seed) if use_seed else None
        )

with c2:
    if st.button("🧹 Clear bracket"):
        st.session_state["rounds"] = None

with c3:
    if st.button("↩️ Reset weights to CSV defaults"):
        st.session_state["weights"] = {}
        st.success("All overrides cleared (session only).")

rounds = st.session_state.get("rounds")
if rounds:
    components.html(bracket_html(rounds), height=1000, scrolling=True)

    if show_debug:
        st.subheader("Debug")
        st.write("Champion:", rounds["CHAMP"].name)
        st.write("Final Four:", [t.name for t in rounds["F4"]])
else:
    st.info("Click **Generate randomized bracket** to populate the bracket.")
