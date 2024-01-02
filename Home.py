import streamlit as st
import plotly.express as px
import pandas as pd
from grades import Grades
from streamlit_extras.add_vertical_space import add_vertical_space

# Settings
# st.set_page_config(layout='wide')

# Variables
session_state = st.session_state

# Layout
st.title('🤖 QPI Bot')
st.text('description')

# Functions
def error(message):
    st.write(message)
def save_edits():
    session_state.original_data = session_state.edited_data
def form_callable():
    try:
        df = get_table(session_state.str)
        session_state.original_data = df
    except:
        st.write('Error!')

# Form
# with st.form(key='form'):
#     s = st.text_area('Input your grades from AISIS', key='str')
#     submit = st.form_submit_button(label='Submit')

# if submit:
#     with st.form(key='df'):
#         df = get_table(s)
#         st.data_editor(df, hide_index=True, use_container_width=True)
#         update = st.form_submit_button(label='Update table')

# if submit:
with open('sample_data.txt', 'r') as file:
    s = file.read()

grades = Grades(s)
st.dataframe(grades.df, hide_index=True, use_container_width=True)

add_vertical_space(1)

width = [0.3,0.3,0.4] if grades.dean_list() else [0.5,0.5,0]
col1, col2, col3 = st.columns(width)
with col1:
    with st.container(border=True):
        cumulative_qpi_delta = round(grades.cumulative_qpi() - grades.cumulative_qpi_delta(), 2)
        st.metric(label="Cumulative QPI 🎯", value=grades.cumulative_qpi(), delta=f'{cumulative_qpi_delta} points')
with col2:
    with st.container(border=True):
        latest_qpi_delta = round(grades.latest_qpi() - grades.latest_qpi_delta(), 2)
        st.metric(label='Semestral QPI 🪴', value=grades.latest_qpi(), delta=f'{latest_qpi_delta} points')
with col3:
    if grades.dean_list():
        with st.container(border=True):
            st.metric(label='Dean\'s Lister Award 🎉', value=grades.dean_list(), delta='Congratulations!', delta_color='normal')

add_vertical_space(1)


# Graph
col1, col2 = st.columns([0.8,0.2])
with col1:
    with st.container(border=True):
        fig = px.line(grades.qpi_by_semester(), x='Semester', y='QPI', 
            title='QPI by Semester',
            markers=True,
            height=300)
        st.plotly_chart(fig, use_container_width=True)
with col2:
    st.write('hi')