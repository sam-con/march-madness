import streamlit as st

st.set_page_config(page_title="Team Power Weights", layout="wide")
st.title("⚙️ Team Power Weights (Session Only)")

df = st.session_state["teams_df"]
defaults = st.session_state["defaults"]
weights = st.session_state["weights"]

query = st.text_input("Search team", value="")
teams = df["team"].tolist()
if query.strip():
    teams = [t for t in teams if query.lower() in t.lower()]

st.caption("Sliders override the CSV `power` column for this session only.")

for team in teams:
    base = float(weights.get(team, defaults.get(team, 0.5)))
    weights[team] = st.slider(
        team,
        min_value=0.0,
        max_value=1.0,
        value=base,
        step=0.001
    )

st.session_state["weights"] = weights

c1, c2, c3 = st.columns([1, 1, 2])
with c1:
    if st.button("↩️ Reset ALL to CSV defaults"):
        st.session_state["weights"] = {}
        st.success("All overrides cleared.")

with c2:
    if st.button("🧹 Clear bracket"):
        st.session_state["rounds"] = None
        st.success("Bracket cleared.")

with c3:
    st.caption(
        f"Overrides active: "
        f"{sum(weights[t] != defaults[t] for t in weights if t in defaults)}"
    )
