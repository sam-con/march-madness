import streamlit as st

st.set_page_config(
    page_title="March Madness Bracket Generator",
    page_icon="🏀",
    layout="wide"
)

# ─────────────────────────────────────────────────────────────
# Initialize shared session state
# ─────────────────────────────────────────────────────────────
if "rounds" not in st.session_state:
    st.session_state["rounds"] = None

if "weights_loaded" not in st.session_state:
    st.session_state["weights_loaded"] = False

# ─────────────────────────────────────────────────────────────
# Landing page content
# ─────────────────────────────────────────────────────────────
st.title("🏀 March Madness Bracket Generator")

st.markdown(
    """
Welcome! This app generates a **fully feasible NCAA tournament bracket**
using **team strength weights** and controlled randomness.

### How it works
1. Each team has a *power rating* (Elite 8 odds or similar proxy)
2. Matchups are simulated using normalized probabilities  
3. Winners advance round-by-round until a champion is crowned

### Pages
- **Bracket Generator**
  - Upload teams
  - Generate a randomized bracket
  - View a full visual bracket

- **Team Power Weights**
  - Adjust team strengths using sliders
  - Save weights for reuse across sessions

Use the **sidebar** to navigate between pages.
"""
)

st.divider()

st.info(
    "Tip: Start on **Team Power Weights** if you want to tweak odds before generating a bracket."
)
