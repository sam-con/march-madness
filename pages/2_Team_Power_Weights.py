import pandas as pd
import streamlit as st
from lib.storage import load_weights, save_weights

st.set_page_config(page_title="Team Power Weights", layout="wide")
st.title("⚙️ Team Power Weights")

uploaded = st.file_uploader("Upload the same teams CSV (team, power)", type=["csv"], key="weights_upload")
if uploaded is None:
    st.info("Upload teams CSV so we know which teams to show sliders for.")
    st.stop()

df = pd.read_csv(uploaded)
df.columns = [c.lower() for c in df.columns]
if "team" not in df.columns or "power" not in df.columns:
    st.error("CSV must include at least `team` and `power` columns.")
    st.stop()

saved = load_weights()

query = st.text_input("Search team", value="")
teams = df["team"].tolist()
if query.strip():
    teams = [t for t in teams if query.lower() in t.lower()]

st.caption("These sliders override the uploaded `power` values when generating a bracket.")

weights = {}
for team in teams:
    base = float(saved.get(team, float(df.loc[df["team"] == team, "power"].iloc[0])))
    weights[team] = st.slider(team, min_value=0.0, max_value=1.0, value=float(base), step=0.001)

c1, c2 = st.columns(2)
with c1:
    if st.button("💾 Save weights", type="primary"):
        save_weights(weights)
        st.success("Saved weights to data/weights.json")
with c2:
    if st.button("↩️ Reset to uploaded defaults"):
        save_weights({})
        st.success("Cleared saved weights.")
