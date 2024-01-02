import streamlit as st
# import plotly.express as px
import pandas as pd

# Settings
# st.set_page_config(layout='wide')

# Variables
letters = {'A':4.00, 'B+':3.50, 'B':3.00, 'C+':2.50, 'C':2.00, 'D':1.00, 'F':0.00, 'W':0.00}
session_state = st.session_state

# Layout
st.title('🤖 QPI Bot')
st.text('description')

# Functions
def error(message):
    st.write(message)
def correct_format(grade):
    return True
def get_table(s):
    columns = 'School Year	Sem	Course	Subject Code	Course Title	Units	Final Grade'.split('	')

    grades = s.split('\n')
    data = [grade.split('	') for grade in grades if correct_format(grade) and part_of_qpi(grade)]

    full_df = pd.DataFrame(data, columns=columns)
    df = full_df[['School Year', 'Sem', 'Subject Code', 'Units', 'Final Grade']]

    return df
def part_of_qpi(grade):
    d = grade.split('	')

    subj_conditions = ['PHYED', 'NSTP']
    for s in subj_conditions:
        l = len(s)
        if d[3][:l] == s:
            return False

    grade_conditions = ['WP', 'S']
    for c in grade_conditions:
        if c in d:
            return False        
    return True
def compute_qpi(df):
    # if df == None:
    #     return ''
    # else:
    df['Units'] = pd.to_numeric(df['Units'], errors='coerce')
    df['Numerical Grade'] = df['Final Grade'].map(letters)
    total_units = df['Units'].sum()

    df['Weighted Grade'] = df['Units'] * df['Numerical Grade']
    weighted_grade = round(df['Weighted Grade'].sum() / total_units, 2)
    return weighted_grade
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

df = get_table(s)
st.dataframe(df, hide_index=True, use_container_width=True)

col1, col2 = st.columns([0.2,0.8])
with col1:
    with st.container(border=True):
        qpi = compute_qpi(df)
        st.caption('Cumulative QPI')
        st.header(qpi)
        st.write('')
with col2:
    pass 
