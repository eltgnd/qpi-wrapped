import streamlit as st
from ui import *

# Initialize
st.set_page_config(page_title='About me', page_icon='🙋‍♂️', layout="centered", initial_sidebar_state="auto", menu_items=None)
ss = st.session_state
with st.sidebar:
    ui_sidebar()