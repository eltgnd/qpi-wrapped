import streamlit as st
# import plotly.express as px
import pandas as pd

st.title('QPI Bot')
st.text('hi')
st.title('Test')

col1, col2 = st.columns(2)

# fig = px.bar(x=["a", "b", "c"], y=[1, 3, 2])
with col1:
    st.title('3.14')
    st.bar_chart(pd.DataFrame({'a':[2], 'b':[4], 'c':[3]}))

    st.text('Lorem ipsum dolor sit amet')
with col2:
    st.header('1.59')

    st.line_chart(pd.DataFrame({'x':[2,4,6], 'y':[1,2,3]}))
    
    st.text('Lorem ipsum dolor sit amet')