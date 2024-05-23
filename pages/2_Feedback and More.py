import streamlit as st
from ui import *
from streamlit_extras.add_vertical_space import add_vertical_space

# Initialize
st.set_page_config(page_title='Feedback and more', page_icon='💙', layout="centered", initial_sidebar_state="auto", menu_items=None)
ss = st.session_state
with st.sidebar:
    ui_sidebar()

# Variables
input_vars = {
    'feedback':False
    }
for key,val in input_vars.items():
    if key not in ss:
        ss[key] = val
def feedback_pressed():
    ss['feedback'] = True

donation_choices = {
    'PHP 50':'https://scontent.xx.fbcdn.net/v/t1.15752-9/413185299_313428951057664_6475839568897633274_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=510075&_nc_eui2=AeGWfR0iSFoIUR-gyr75FYQHIncde6cGYg0idx17pwZiDQ3VOIq8VZOJsgoH1TRb07DG4IMQ1LLcfEArjeWRzvlN&_nc_ohc=IVPDyqN5DD4AX8i948P&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&cb_e2o_trans=q&oh=03_AdRPKVGSmoV7ALd89jKwzIUnz7r160n_rxUxoqlmCxr79w&oe=65C4A98F',
    'PHP 100':'https://scontent.xx.fbcdn.net/v/t1.15752-9/413898045_1371548693482521_6834946516334489008_n.jpg?_nc_cat=105&ccb=1-7&_nc_sid=510075&_nc_eui2=AeEHibqWTLk5_3qwt2ffN_xJP7EQzTlPD6o_sRDNOU8PqlcAHvvZwCNj2Og7V5NJPgoIluUveEcrIuHwut6P04co&_nc_ohc=Fuy6MxZkXx4AX8bPjIh&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&cb_e2o_trans=q&oh=03_AdRot2gUXnxpNbtbOCD69nyF19KZqzfGlPn0BZhpt57uXw&oe=65C48885',
    'Other amount':'https://scontent.xx.fbcdn.net/v/t1.15752-9/414154292_331338256473546_3364700846078338076_n.jpg?_nc_cat=105&ccb=1-7&_nc_sid=510075&_nc_eui2=AeG9Ct9kEKIM5v-5B9DPDUyl46Z1FWeCfSfjpnUVZ4J9JzeQgAPFvjjshSPjWWMhZ4HQJZLw0QliXcd2Rkmt2uMT&_nc_ohc=hlUmFItLL9QAX9c5A1L&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&cb_e2o_trans=q&oh=03_AdQlaW47yGUt1lB5nIMarFVVbMHhh6cnf1OeEtg8CK_qMQ&oe=65C49F70'
}

# Feedback form
if not ss.feedback:
    with st.container(border=True):
        st.subheader('Help me make QPI Wrapped better! 🤝')
        st.button('View Feedback Form', type='primary', key='feedback_pressed', on_click=feedback_pressed)
else:
    html_str = """
            <!DOCTYPE html> 
    <html> 
    <body> 
        <iframe src="https://docs.google.com/forms/d/e/1FAIpQLSdvKIGvBq-oqejFHxahYDHR0HSCwpULB4x6P4SG2BbHGWwvaQ/viewform?embedded=true" width="640" height="928" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>
    </body> 
    </html> 
    """
    st.markdown(html_str, unsafe_allow_html=True)
    st.link_button(label='Click here if you can\'t access the form above.', url='https://forms.gle/wdLjZdnYx3UHUukn7', type='primary')

st.divider()

# Announcement
st.header('QPI Wrapped will accomodate more universities soon. 🤓')
with st.container(border=True):
    st.write('What\'s next? 👀') 
    st.write('Right now, QPI Wrapped is only for AdMU students. To make the app more accessible, I\'m planning to expand it to accomodate other universities\' grades! If you\'re interested to include your school, please contact me at https://facebook.com/eltgnd!')

st.divider()

# Donate
st.header('Buy me iced coffee! ☕')

with st.container(border=True): 
    st.write('QPI Wrapped is free forever to use. If you\'d like to support my work, you can leave a tip via GCash!')
    choice = st.radio('Choose an amount', ['PHP 50', 'PHP 100', 'Other amount'])
    donate = st.button('Leave a tip')
if donate:
    st.balloons()
    st.toast('Thank you so much!', icon='💙')
    st.image(donation_choices[choice])

