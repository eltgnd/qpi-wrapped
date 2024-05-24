import streamlit as st
from ui import *
from streamlit_extras.add_vertical_space import add_vertical_space


# Initialize
st.set_page_config(page_title='About me', page_icon='🙋‍♂️', layout="centered", initial_sidebar_state="auto", menu_items=None)
ss = st.session_state
with st.sidebar:
    ui_sidebar()

# Header
# image here
col1, col2 = st.columns([0.46,0.55], gap='medium')
with col1:
    add_vertical_space(1)
    st.caption('ABOUT ME')
    st.title('Hi, I\'m Val! 👋')
    st.write('I\'m currently a junior at Ateneo de Manila University taking up Applied Mathematics with a specialization in Data Science. Funnily enough, I wrote a personal essay about QPI Wrapped, which got featured on Ateneo Gabay\'s Kwentong Scholar Zine. You can read it here: https://bit.ly/KSZine')
    st.write('**Please contact me at val.eltagonde@student.ateneo.edu for my resumé and work portfolio.**')
with col2:
    add_vertical_space(1)
    with st.container(border=True):
        st.image('images/photo.jpg')
