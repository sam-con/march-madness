import streamlit as st

st.set_page_config(page_title="Team Power Weights", layout="wide")
st.title("⚙️ Team Power Weights (Session Only)")

df = st.session_state.get("teams_df")
defaults = st.session_state.get("defaults", {})
weights = st.session_state.get("weights", {})

if df is None:
    st.info("Go to **Bracket Generator** and upload your teams CSV first.")
    st.stop()

query = st.text_input("Search team", value="")
teams = df["team"].tolist()
if query.strip():
    teams = [t for t in teams if query.lower() in t.lower()]

st.caption("Slider values override the uploaded `power` values for this session only.")

# A nice UX pattern: update weights live as sliders move
for team in teams:
    base = float(weights.get(team, defaults.get(team, 0.5)))
    new_val = st.slider(team, min_value=0.0, max_value=1.0, value=float(base), step=0.001)
    weights[team] = float(new_val)

st.session_state["weights"] = weights

c1, c2, c3 = st.columns([1, 1, 2])
with c1:
    if st.button("↩️ Reset ALL to uploaded defaults"):
        st.session_state["weights"] = {}
        st.success("All overrides cleared (session).")

with c2:
    if st.button("🧹 Clear bracket (if generated)"):
        st.session_state["rounds"] = None
        st.success("Bracket cleared. Generate again to apply weights.")

with c3:
    st.caption(f"Overrides currently set: {sum(1 for t in weights if t in defaults and weights[t] != defaults[t])}")
