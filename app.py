import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="March Madness Bracket Generator",
    page_icon="🏀",
    layout="wide"
)

DATA_PATH = Path("data/teams_template.csv")

# ─────────────────────────────────────────────────────────────
# Initialize session state
# ─────────────────────────────────────────────────────────────
if "teams_df" not in st.session_state:
    if not DATA_PATH.exists():
        st.error(f"Expected CSV not found at {DATA_PATH.resolve()}")
        st.stop()

    df = pd.read_csv(DATA_PATH)
    df.columns = [c.lower() for c in df.columns]

    required = {"team", "region", "seed", "power"}
    missing = required - set(df.columns)
    if missing:
        st.error(f"CSV is missing required columns: {sorted(missing)}")
        st.stop()

    st.session_state["teams_df"] = df
    st.session_state["defaults"] = {
        row.team: float(row.power)
        for row in df.itertuples(index=False)
    }

if "weights" not in st.session_state:
    st.session_state["weights"] = {}

if "rounds" not in st.session_state:
    st.session_state["rounds"] = None

# ─────────────────────────────────────────────────────────────
# Landing page
# ─────────────────────────────────────────────────────────────
st.title("🏀 March Madness Bracket Generator")

st.markdown("""
This app generates a **feasible NCAA tournament bracket** using
team power weights and controlled randomness.

**Data source:**  
`data/teams_template.csv` (loaded automatically)

Use the sidebar to:
- Generate a randomized bracket
- Adjust team power weights (session-only)
""")

st.info("Edit `teams_template.csv` to update teams, regions, seeds, or baseline power.")
