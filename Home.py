# Packages
import time
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Imported files
from grades import Grades, honors_dict
from streamlit_extras.add_vertical_space import add_vertical_space
from sample_data import sample_data
from gauge import plot_gauge

# Variables
grades_color_map = {
    'A': '#4169E1',  # Royal Blue
    'B+': '#00BFFF', # Deep Sky Blue
    'B': '#87CEEB',  # Sky Blue
    'C+': '#FFD700', # Gold
    'C': '#FFA500',  # Orange
    'D': '#FF6347',  # Tomato
    'F': '#FF0000',  # Red
}
correlation_scales = {
    '-Very Weak': (0.0, 0.19),
    '-Weak': (0.2, 0.39),
    'Moderate': (0.4, 0.59),
    '+Strong': (0.6, 0.79),
    '+Very High': (0.8, 1.0)
}

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

# Logo
def logo():
    st.title('Hi')

# Header
st.sidebar.write('')
st.title('🦅📘 QPI Wrapped')
add_vertical_space(1)
st.write('Inspired by CompSAt\'s QPI Calculator, QPI Wrapped calculates your QPI and visualizes your grades for fun! To get started, input your grades from AISIS. **Disclaimer: Your data is not saved.**')
add_vertical_space(1)
# Tutorial
with st.expander('See how to copy paste grades', expanded=False):
    st.write('''1. Visit AISIS and go to `MY GRADES`.
        \n2. Select `ALL GRADES` from the dropdown and click the `DISPLAY GRADES` button.
        \n3. Copy the big table and paste it here!
    ''')
    st.image('https://scontent.xx.fbcdn.net/v/t1.15752-9/407088558_396969352731566_5235174993494823881_n.png?_nc_cat=103&ccb=1-7&_nc_sid=510075&_nc_eui2=AeEQIolU45pnuLrvVhT_5LSwec86j5goO6Z5zzqPmCg7phHZHCRq6OFBIoNhpqC9a8BaiRfCC9v85kGaHo8pE0rm&_nc_ohc=IstVxbAedXAAX8a7j5p&_nc_oc=AQl5EUZMveKZqWo7wmXntup_DCNDeTubAVcOc9HsZVOQ9HPt_LboQgk4DTkpOfE-w_No6XORLqAQycrq-ywacCBh&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&cb_e2o_trans=q&oh=03_AdRg16NwA4mvNFXObHeOIn1vO_SxvkiwgnFMllnoYWvZdA&oe=65BCE003')

# if submit:
#     with st.form(key='df'):
#         df = get_table(s)
#         st.data_editor(df, hide_index=True, use_container_width=True)
#         update = st.form_submit_button(label='Update table')

# with open('sample_data.txt', 'r') as file:
#     s = file.read()

if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Form
with st.container(border=True):
    user_input = st.text_area('Input your grades from AISIS', 
        placeholder=sample_data,
        disabled=st.session_state.submitted,
        key='str'
    )
    col1, col2 = st.columns([0.5,3.5], gap='small')
    with col1:
        submit = st.button(label='Submit', type='primary')
    with col2:
        sample = st.button(label='Try sample data')

if sample:
    if 'data' not in st.session_state:
        st.session_state.data = sample_data
        st.session_state.submitted = True
if submit:
    if 'data' not in st.session_state:
        st.session_state.data = user_input
        st.session_state.submitted = True

try:
    s = st.session_state.data
    grades = Grades(s)

    # Wait
    if 'waited' not in st.session_state:
        st.session_state.waited = True  
        add_vertical_space(1)
        with st.spinner('Analyzing your grades...'):
            time.sleep(3)
        st.toast('Done analyzing!', icon='🥳')

    # Table
    with st.expander('View Table', expanded=False):
        st.dataframe(grades.df, hide_index=True, use_container_width=True)

    # Sidebar
    with st.sidebar:
        st.divider()

        # Latin honors
        st.write('**🤔 Latin Honor Eligibility**')
        st.number_input('How many are your computable units left?', step=1, min_value=0, help='Computable units refer to units used in computing your cumulative QPI (e.g. PE is not included)', key='remaining_units')
        if st.session_state.remaining_units != 0:
            st.radio('Check eligibility', honors_dict.keys(), index=3, key='check_eligibility')
    
        st.divider()

        # Summarize course
        qpi_temp = grades.compute_qpi(grades.df)
        course_choices = grades.qpi_by_course(minimum_courses=1).sort_values(by='Subjects', ascending=False).reset_index()['Course']
        st.multiselect('Analyze courses based on course code', options=course_choices, key='courses', placeholder=course_choices[0])
        if st.session_state.courses:
            with st.expander('View selected courses'):
                st.dataframe(grades.analyze_courses(st.session_state.courses)[['Subject Code', 'Units', 'Final Grade']], hide_index=True)

        st.divider()

        # About
        st.caption('Developed by Val Eltagonde. @eltgnd_v')
        col1, col2 = st.columns([0.05,0.45])
        with col1:
            st.markdown("""<a href="https://www.linkedin.com/in/val-eltagonde-8b6282141/">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/LinkedIn_icon.svg/2048px-LinkedIn_icon.svg.png" 
                width="25" height="25"></a>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""<a href="https://www.instagram.com/eltgnd_v/">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Instagram_logo_2016.svg/2048px-Instagram_logo_2016.svg.png" 
                width="25" height="25"></a>""", unsafe_allow_html=True)
    
    add_vertical_space(1)

    # Row 1
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

    # Row 2
    with st.container(border=True):
        option = st.toggle('Exclude Intersession QPI')
        fig = px.line(grades.qpi_by_semester(option), x='Semester', y='QPI', 
            title='QPI by Semester',
            markers=True,
            text='QPI',
            height=300)
        fig.update_traces(textposition="top center")
        fig.update_layout(margin=dict(l=30, r=30, t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)

    add_vertical_space(1)

    # Row 3
    col1, col2 = st.columns([0.5,0.5])
    with col1:
        with st.container(border=True):
            pie, bar = st.tabs(['Pie Chart', 'Bar Chart'])
            with pie:
                if 'curr_sem1' not in st.session_state:
                    st.session_state.curr_sem1 = False
                fig = px.pie(grades.letter_frequency(st.session_state.curr_sem1), names='Final Grade', values='Subject Code',
                    title='Current Semester Letter Grade Frequency' if st.session_state.curr_sem1 else 'Cumulative Letter Grade Frequency',
                    height=380,
                    hole=0.6,
                    color='Final Grade',
                    color_discrete_map=grades_color_map
                )
                fig.update_layout(legend=dict(
                    orientation='h',yanchor="top",y=0.1,xanchor="center",x=0.5),
                    margin=dict(l=20, r=20, t=30, b=0),
                    title=dict(x=0, y=0.95)
                )
                st.plotly_chart(fig, use_container_width=True)
                st.toggle('Current Semester Only', key='curr_sem1')
            with bar:
                if 'curr_sem2' not in st.session_state:
                    st.session_state.curr_sem2 = False
                fig = px.bar(grades.letter_frequency(st.session_state.curr_sem2), x='Final Grade', y='Subject Code',
                    title='Current Semester Letter Grade Frequency' if st.session_state.curr_sem2 else 'Cumulative Letter Grade Frequency',
                    height=380,
                    # color='group',
                    # color_discrete_map=grades_color_map
                )
                fig.update_layout(legend=dict(
                    orientation='h',yanchor="top",y=0.9,xanchor="center",x=0.5),
                    margin=dict(l=20, r=20, t=50, b=0),
                    title=dict(x=0, y=0.95),
                    xaxis_title='Letter Grade',
                    yaxis_title='Frequency'
                )
                st.plotly_chart(fig, use_container_width=True)
                st.toggle('Current Semester Only', key='curr_sem2')

    with col2:
        with st.container(border=True):
            # Scale
            df = grades.qpi_by_course()
            df['Scaled'] = df[0]/4
            fig = px.line_polar(df, r='Scaled', theta='Course', 
                title='Overall Performance by Course',
                height=386,
                line_close=True)
            fig.update_polars(bgcolor='#0F1116', radialaxis=dict(visible=False, range=[0, 1]))
            fig.update_traces(fill='toself')
            fig.update_layout(margin=dict(l=35, r=35, t=50, b=20))
            st.plotly_chart(fig, use_container_width=True)

        with st.container(border=True):
            st.caption('**Disclaimer:** To avoid clutter, the radar chart above only includes courses with more than two subjects.')
    
    add_vertical_space(1)

    if st.session_state.remaining_units:
        # Row 4
        col1, col2, col3 = st.columns([0.2, 0.45, 0.35])
        with col1:
            with st.container(border=True):
                st.metric(label='Completed Units', value=grades.completed_units(), delta=f'{grades.completed_units_delta()} units')
            with st.container(border=True):
                st.metric(label='Remaining Units', value=st.session_state.remaining_units)
        with col2:
            with st.container(border=True):
                total = grades.completed_units() + st.session_state.remaining_units
                percent = round(grades.completed_units() * 100 / total,2)
                plot_gauge(percent, '#00BFFF', f'%', 'IPS Progress in Percent', 100)            
        with col3:
            with st.container(border=True):
                honor = st.session_state.check_eligibility
                highest_possible = grades.check_highest_possible(st.session_state.remaining_units, honor, 0)
                eligibility_text = 'Possible 🥳' if highest_possible >= honors_dict[honor][0] else 'Impossible' 

                st.metric(label=f'{st.session_state.check_eligibility} is...', value=eligibility_text)

                st.write(f'Highest attainable QPI: {highest_possible}\nHonor range: {honors_dict[honor][0]} to {honors_dict[honor][-1]}')
                st.caption("Highest attainable QPI assumes an **'A'** in all remaining courses.")

        # Row 5
        # mathematically, itis possible but for many of us, it is hard to get an A. Let's try to estimate your chances better
        with st.expander('Realistically, it is hard to get *A*s on **all** remaining courses. Want to estimate your chances better?', expanded=False):
            st.write(':grey[Let\'s assume all your remaining courses all weigh 3 units.]')
            col1, col2, col3 = st.columns([0.4,0.2,0.3], gap='small')
            with col1:
                with st.container(border=True):
                    st.slider('What percent of your remaining courses do you estimate to get B+ on?', min_value=0, max_value=100, step=10, format=f'%f%%', key='ratio')
            with col2:
                with st.container(border=True):
                    ratio = st.session_state.ratio
                    st.caption('Your estimation')
                    summary = (f'{100-ratio}% A and {ratio}% B+')
                    st.markdown(f'''<span style="  font-size:22px ; font-weight:light ; ">{summary}</span>''', unsafe_allow_html=True)
            with col3:
                with st.container(border=True):  
                    honor = st.session_state.check_eligibility
                    highest_possible = grades.check_highest_possible(st.session_state.remaining_units, honor, st.session_state.ratio)
                    eligibility_text = 'possible 👍' if highest_possible >= honors_dict[honor][0] else 'impossible 😟' 

                    st.markdown(f'<span style=" font-size:22px ">{st.session_state.check_eligibility} is {eligibility_text}</span>', unsafe_allow_html=True)
                    st.caption(f'Highest attainable QPI: {highest_possible}')

        add_vertical_space(1)

    # Row 6
    if st.session_state.courses:
        with st.container(border=True):
            df = grades.analyze_courses(st.session_state.courses).reset_index()
            fig = px.bar(df, x='Subject Code', y='Numerical Grade',
                color='Course',
                category_orders={'Subject Code':df['Subject Code']},
                title='Letter Grade by Specified Course Code',
                text='Final Grade',
                height=300,
            )

            fig.update_layout(margin=dict(l=30, r=30, t=50, b=20))
            st.plotly_chart(fig, use_container_width=True)

        add_vertical_space(1)

    # Row 7
    col1, col2 = st.columns([0.65,0.35])
    with col1:
        with st.container(border=True):
            st.radio('**Fun Question**: Based only on your data, do you think your QPI correlates with the number of units you take each semester?', [ 'I\'m not sure 😴', 'I think yes 👍', 'I don\'t think so 🥱'])
            add_vertical_space(1)
            find_out = st.button('I want to find out')
    with col2:
        with st.container(border=True):      
            st.metric(label='hi', value=5) # highest qpi and ilang units
        with st.container(border=True):      
            st.metric(label='hi', value=5) # highes units ilan qpi
    if find_out:
        col1, col2 = st.columns([0.8,0.2])
        with col1:
            with st.container(border=True):
                df = grades.qpi_vs_units()

                fig = go.Figure(layout_title_text="QPI vs Units")
                fig.add_trace(go.Scatter(x=df.Units, y=df.QPI, 
                    name='QPI vs Units',
                    text=df.QPI,
                    mode='markers+text',
                    marker=dict(color='skyblue', size=10)
                    )
                )

                # Linear regression
                model = np.polyfit(df.Units, df.QPI, 1)
                mn, mx = df.Units.min(), df.Units.max()
                x_line = [i for i in range(mn,mx+1,1)]
                y_line = [(model[0]*x + model[1]) for x in x_line]

                fig.add_trace(go.Scatter(x=x_line, y=y_line,
                    name='Best fit line',
                    line=dict(color='skyblue', width=1, dash='dot'),
                    mode='lines'
                    )
                )
                fig.update_traces(textposition="top center")
                fig.update_layout(legend=dict(
                    orientation='h',yanchor="top",y=-0.35,xanchor="left",x=-0.1), 
                    margin=dict(l=30, r=30, t=60, b=20),
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
        with col2:
            with st.container(border=True):
                corr = abs(round(df['Units'].corr(df['QPI'], method='pearson'),2))
                label = ''
                for val, scale in correlation_scales.items():
                    if scale[0] <= corr <= scale[1]:
                        label = val
                        break
                st.metric(label='Correlation\n\ncoefficient (r)', value=corr, delta=label, delta_color='normal' if val != 'Moderate' else 'off')
            with st.container(border=True):
                st.write(f'What does *r* ({corr}) mean?')
                st.caption("r quantifies the strength of a linear relationship!")

except Exception as e:
    st.info('Waiting for input... 😴')
    st.write(e)



# add one more chart in 'Fun questiom' -- divide into 2 columns (wip)

# one time lang "I want to find out"
# toast when same guess with correlation coefficient
# best fit line button
# remove + sign from metric delta

# add bridging courses
# add feedback form
# update sample data
# download results