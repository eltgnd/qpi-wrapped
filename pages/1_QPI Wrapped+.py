# Packages
import streamlit as st

# Imported files
from ui import *

# Initialize
st.set_page_config(page_title='QPI Wrapped+', page_icon='💻', layout="centered", initial_sidebar_state="auto", menu_items=None)
ss = st.session_state
with st.sidebar:
    ui_sidebar()