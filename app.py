import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Virus Spread Simulation",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide default Streamlit elements
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    .stApp {
        background: #0a0e1a;
    }
</style>
""", unsafe_allow_html=True)

# Read and inject the simulation HTML
with open("simulation.html", "r") as f:
    html_content = f.read()

components.html(html_content, height=860, scrolling=False)
