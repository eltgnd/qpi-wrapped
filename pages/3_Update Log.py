import streamlit as st
from ui import ui_sidebar

# Initialize
st.set_page_config(page_title='Update Log', page_icon='📋', layout="centered", initial_sidebar_state="auto", menu_items=None)
ss = st.session_state
with st.sidebar:
    ui_sidebar()

# Header
st.caption('UPDATE LOG')

# First Update
st.subheader('1️⃣ QPI Wrapped 1.0')
st.write('*January 8, 2024*\n\n- Created the first working version of QPI Wrapped.')

st.divider()

# Second Update
st.subheader('2️⃣ QPI Wrapped 1.1')
st.write('*May 25, 2024*')
st.write("""
- Fixed clunky user input. Proper reference of session states
- Disable analyze grades button when missing data is detected
- Added a 'By School Year' tab on QPI Trend section
- Added a 'Letter Grade Trend' section, automatically stacks bars when grades have too many semesters
- Added a 'Yearly QPI Retainment' section
- Added a 'Yearly QPI Retainment' section for scholars. Still under development for 'Current Semester' option
- Updated feedback form to be more concise
- Updated About me page
- Created an Update Log page
""")

