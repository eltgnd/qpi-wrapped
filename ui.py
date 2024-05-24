# Packages
import time
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from shillelagh.backends.apsw.db import connect
from streamlit_extras.add_vertical_space import add_vertical_space

# Imported files
from scholarship_retainment import scholarships

def ui_tutorial():
    with st.expander('How to copy-paste grades', expanded=False):
        st.write('''1. Visit AISIS and go to `MY GRADES`.
            \n2. Select `ALL GRADES` from the dropdown and click the `DISPLAY GRADES` button.
            \n3. Copy the big table and paste it here!
        ''')
        add_vertical_space(1)
        st.success('Copying the data should include all rows and columns of the table! (See image below)', icon='✅')
        st.image('images/copy-paste-tutorial.png')

def ui_sidebar():
    with st.sidebar:
        st.caption('Developed by Val Eltagonde. @eltgnd_v')
        col1, col2, col3, col4 = st.columns([0.05,0.05,0.05,0.15])
        with col1:
            st.markdown("""<a href="https://github.com/eltgnd">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Octicons-mark-github.svg/1200px-Octicons-mark-github.svg.png?20180806170715" 
                width="30" height="30"></a>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""<a href="https://www.linkedin.com/in/val-eltagonde-8b6282141/">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/LinkedIn_icon.svg/2048px-LinkedIn_icon.svg.png" 
                width="30" height="30"></a>""", unsafe_allow_html=True)
        with col3:
            st.markdown("""<a href="https://www.instagram.com/eltgnd_v/">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Instagram_logo_2016.svg/2048px-Instagram_logo_2016.svg.png" 
                width="30" height="30"></a>""", unsafe_allow_html=True)

def render_semester_retainment(semester, chosen, year_level):
    # Intersession
    if semester == '0':
        retainment = scholarships[chosen][year_level]['Intersession']
        if isinstance(retainment, float):
            pass