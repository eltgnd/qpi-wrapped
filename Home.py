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
    df = full_df[['Subject Code', 'Units', 'Final Grade']]

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
    df['Units'] = pd.to_numeric(df['Units'], errors='coerce')
    df['Numerical Grade'] = df['Final Grade'].map(letters)
    total_units = df['Units'].sum()

    df['Weighted Grade'] = df['Units'] * df['Numerical Grade']
    weighted_grade = round(df['Weighted Grade'].sum() / total_units, 2)
    st.write("Weighted Average:", weighted_grade)
def save_edits():
    session_state.original_data = session_state.edited_data

if 'original_data' not in session_state:
    st.session_state.original_data = 'Empty'
if 'edited_data' not in st.session_state:
    session_state.edited_data = 'Empty'

def form_callable():
    try:
        df = get_table(text_input)
        session_state.original_data = df
    except:
        st.write('Error!')

# Form
with st.form(key='form'):
    text_input = st.text_area('Input your grades from AISIS', key='str')
    st.form_submit_button(label='Submit', on_click=form_callable)

st.write(session_state.original_data)

# if isinstance(df, pd.DataFrame):
#     # Session state
#     if "original_data" not in session_state:
#         st.session_state.original_data = df
#     if "edited_data" not in st.session_state:
#         session_state.edited_data = df.copy()

#     session_state.edited_data = st.data_editor(session_state.original_data, num_rows = 'dynamic')


#     st.header('Your QPI')
#     c = compute_qpi(session_state.edited_data)
#     st.title(c)


# Text processing
# if s and button:

#     edited_df = st.data_editor(df)

#     st.header('Your QPI')
#     c = compute_qpi(edited_df)
#     st.title(c)

# else:
#     error('Please input grades and press Submit.')

# col1, col2 = st.columns(2)
# # fig = px.bar(x=["a", "b", "c"], y=[1, 3, 2])
# with col1:
#     st.title('3.14')
#     st.bar_chart(pd.DataFrame({'a':[2], 'b':[4], 'c':[3]}))

#     st.text('Lorem ipsum dolor sit amet')
# with col2:
#     st.header('1.59')

#     st.line_chart(pd.DataFrame({'x':[2,4,6], 'y':[1,2,3]}))
    
#     st.text('Lorem ipsum dolor sit amet')