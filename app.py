import streamlit as st

st.set_page_config(
    page_title="March Madness Bracket Generator",
    page_icon="🏀",
    layout="wide"
)

# Session-only storage
if "weights" not in st.session_state:
    st.session_state["weights"] = {}   # team -> float override
if "defaults" not in st.session_state:
    st.session_state["defaults"] = {}  # team -> float from upload
if "teams_df" not in st.session_state:
    st.session_state["teams_df"] = None
if "rounds" not in st.session_state:
    st.session_state["rounds"] = None

st.title("🏀 March Madness Bracket Generator (Session Only)")

st.markdown("""
Use the sidebar to navigate:

- **Bracket Generator**: upload teams, generate bracket, view bracket
- **Team Power Weights**: adjust team strengths with sliders (saved in-session)
""")
