# Packages
import time
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from shillelagh.backends.apsw.db import connect
from streamlit_extras.add_vertical_space import add_vertical_space

# Initialize
st.set_page_config(page_title='Your QPI Wrapped', page_icon='📉', layout="centered", initial_sidebar_state="auto", menu_items=None)
ss = st.session_state

# Imported files
from grades import Grades, honors_dict
from ui import *
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
    'Strong': (0.6, 0.79),
    'Very High': (0.8, 1.0)
}

donation_choices = {
    'PHP 50':'https://scontent.xx.fbcdn.net/v/t1.15752-9/413185299_313428951057664_6475839568897633274_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=510075&_nc_eui2=AeGWfR0iSFoIUR-gyr75FYQHIncde6cGYg0idx17pwZiDQ3VOIq8VZOJsgoH1TRb07DG4IMQ1LLcfEArjeWRzvlN&_nc_ohc=IVPDyqN5DD4AX8i948P&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&cb_e2o_trans=q&oh=03_AdRPKVGSmoV7ALd89jKwzIUnz7r160n_rxUxoqlmCxr79w&oe=65C4A98F',
    'PHP 100':'https://scontent.xx.fbcdn.net/v/t1.15752-9/413898045_1371548693482521_6834946516334489008_n.jpg?_nc_cat=105&ccb=1-7&_nc_sid=510075&_nc_eui2=AeEHibqWTLk5_3qwt2ffN_xJP7EQzTlPD6o_sRDNOU8PqlcAHvvZwCNj2Og7V5NJPgoIluUveEcrIuHwut6P04co&_nc_ohc=Fuy6MxZkXx4AX8bPjIh&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&cb_e2o_trans=q&oh=03_AdRot2gUXnxpNbtbOCD69nyF19KZqzfGlPn0BZhpt57uXw&oe=65C48885',
    'Other amount':'https://scontent.xx.fbcdn.net/v/t1.15752-9/414154292_331338256473546_3364700846078338076_n.jpg?_nc_cat=105&ccb=1-7&_nc_sid=510075&_nc_eui2=AeG9Ct9kEKIM5v-5B9DPDUyl46Z1FWeCfSfjpnUVZ4J9JzeQgAPFvjjshSPjWWMhZ4HQJZLw0QliXcd2Rkmt2uMT&_nc_ohc=hlUmFItLL9QAX9c5A1L&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&cb_e2o_trans=q&oh=03_AdQlaW47yGUt1lB5nIMarFVVbMHhh6cnf1OeEtg8CK_qMQ&oe=65C49F70'
}

ls_retainment = {
    1:['First Year', 1.80],
    2:['Sophomore Year', 1.90],
    3:['Junior Year', 2.00],
    4:['Senior Year', 2.00],
    5:['Senior Year', 2.00],
    6:['Senior Year', 2.00],
}

# Input variables
input_vars = {
    'grade_submit':False,
    'latin_honor_toast':False,
    'submit':False,
    }
for key,val in input_vars.items():
    if key not in ss:
        ss[key] = val
def grade_submit(grades):
    with st.spinner('Creating your QPI Wrapped...'):
        time.sleep(0)
    ss['grades'] = grades
    ss['grade_submit'] = True
    st.rerun()
def find_out_button():
    ss['find_out'] = True
def latin_honor_toast():
    ss['latin_honor_toast'] = True


# Header
st.sidebar.write('')
st.title('QPI Wrapped 📉')
add_vertical_space(1)

# Form
if not ss.grade_submit:
    st.write('Inspired by Spotify Wrapped and CompSAt\'s QPI Calculator, QPI Wrapped is a beautiful dashboard for your AISIS grades. To get started, paste your grades from AISIS.')
    st.info('**Privacy notice**: Your data is never saved.')
    add_vertical_space(1)
    ui_sidebar()

    # Tutorial
    ui_tutorial()

    # Input
    with st.container(border=True):
        s = st.text_area('Paste here')
        if s != '':
            try:
                grades = Grades(s)
            except IndexError:
                st.info('The pasted text does not seem to be in the correct format.', icon='🤔')

    col1, col2, col3 = st.columns([1,1,2.2])
    col1.button('Try Sample Grades', key='sample')

    try:
        if grades:
            ss.missing = grades.has_missing_data()
        if ss.missing:
            add_vertical_space(1)
            st.warning('Missing data detected! Please ensure all copied rows are complete.', icon='⚠️')
            st.dataframe(grades.get_missing_data(), hide_index=True, use_container_width=True)
        else:
            add_vertical_space(1)
            st.caption('DATA PREVIEW')
            st.dataframe(grades.df, hide_index=True, use_container_width=True) 
            col2.button('Analyze Grades', key='submit', type='primary')
    except:
        pass

    if ss.sample:
        grade_submit(Grades(sample_data))
    if ss.submit:
        grade_submit(grades)


else:
    grades = ss.grades

    # Sidebar
    with st.sidebar:
        st.caption('MORE TOOLS')
        # Latin honors
        st.write('**🎓 Latin Honor Eligibility**')
        st.number_input('How many computable units do you have left?', step=1, min_value=0, help='Computable units refer to units used in computing your cumulative QPI (e.g. PE is not included)', key='remaining_units')
        if st.session_state.remaining_units != 0:

            if not ss['latin_honor_toast']:
                st.toast('Scroll down to find the Latin Honor Eligibility section!', icon='👋')
            latin_honor_toast()

            st.selectbox('Check eligibility', honors_dict.keys(), index=3, key='check_eligibility')
        # Summarize course
        st.write('\n')
        st.write('**🤔 Grade Analysis by Course**')
        qpi_temp = grades.compute_qpi(grades.df)
        course_choices = grades.qpi_by_course(minimum_courses=1).sort_values(by='Subjects', ascending=False).reset_index()['Course']
        st.multiselect('Select at least one class code!', options=course_choices, key='courses', placeholder=course_choices[0])
        add_vertical_space(2)

        ui_sidebar()

    # Dashboard

    # Row 1
    st.caption('QPI AT A GLANCE')

    width = [0.3,0.3,0.4] if grades.dean_list() else [0.5,0.5,0.01]
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
    st.caption('QPI TREND')

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
    st.caption('QPI DISTRIBUTION')

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
                    height=380
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
            fig.update_polars(bgcolor='#FFFFFF', radialaxis=dict(visible=False, range=[0, 1]))
            fig.update_traces(fill='toself')
            fig.update_layout(margin=dict(l=35, r=35, t=50, b=20))
            st.plotly_chart(fig, use_container_width=True)
        with st.container(border=True):
            st.caption('**Disclaimer:** To avoid clutter, the radar chart only includes course codes with more than one subject.')
    
    add_vertical_space(1)

    # Row 4
    st.caption('LETTER GRADE TREND')
    df = grades.letter_trend(['A', 'B+'])
    semester_count = df['Semester'].nunique()
    with st.container(border=True):
        col1, col2 = st.columns([3,1])
        col1.multiselect('Select letter grade/s', grades_color_map.keys(), default=['A', 'B+', 'B'])
        col2.write('\n')
        stack = col2.toggle('Stack bars', value=semester_count>9)
    with st.container(border=True):
        fig = px.bar(df, x='Semester', y='Count',
            color='Final Grade',
            title='Letter Grade Trend',
            height=350,
            color_discrete_map=grades_color_map,
            barmode='stack' if stack else 'group')
        fig.update_layout(margin=dict(l=35, r=35, t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)

    add_vertical_space(1)

    # Row 5
    st.caption('QPI CORRELATION')
    col1, col2 = st.columns([0.65,0.35])
    if 'find_out' not in st.session_state:
        st.session_state.find_out = False

    with col1:
        with st.container(border=True):
            guess_options = [ "I\'m not sure 😴", "I think so👍", "I don't think so 👎"]
            st.radio('**Fun Question**: Based only on this data, do you think your QPI correlates with the number of units you take each semester?', guess_options, key='guess')
            add_vertical_space(1)
            find_out = st.button('I want to find out', type='primary', on_click=find_out_button)
    with col2:
        with st.container(border=True):      
            highest_qpi = grades.qpi_by_semester(True).sort_values(by='QPI', ascending=False).iloc[0]
            st.metric(label=f'Highest QPI *({highest_qpi.Semester})*', value=f'{highest_qpi.QPI}🪴')
        with st.container(border=True):     
            highest_units = grades.group_by_units().sort_values(by='Units', ascending=False).iloc[0]
            st.metric(label=f'Highest Units taken *({highest_units.Semester})*', value=f'{highest_units.Units} units 📋')

    if st.session_state.find_out:
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
                orig_corr = round(df['Units'].corr(df['QPI'], method='pearson'),2)
                corr = abs(round(df['Units'].corr(df['QPI'], method='pearson'),2))
                label = ''
                for val, scale in correlation_scales.items():
                    if scale[0] <= corr <= scale[1]:
                        label = val
                        break
                st.metric(label='Correlation\n\ncoefficient (r)', value=orig_corr, delta=label, delta_color='normal' if val != 'Moderate' else 'off')
            with st.container(border=True):
                st.write(f'What does *r* ({orig_corr}) mean?')
                st.caption("r quantifies the linear strength from -1 (inverse) to 1 (direct).")
            if corr >= correlation_scales['Strong'][0]:
                correct_guess = guess_options[1]
            elif corr <= correlation_scales['-Weak'][-1]:
                correct_guess = guess_options[2]
            else:
                correct_guess = 0
            if st.session_state.guess != guess_options[0]:
                text = 'right' if st.session_state.guess == correct_guess else 'wrong'
                st.toast(f"You got the fun question {text}!", icon='😳')

    add_vertical_space(1)

    # Row idk
    st.caption('QPI RETAINMENT')
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            year_level = grades.get_year_level()
            st.metric(f'Current yearly QPI', grades.yearly_qpi())
            add_vertical_space(1)
    with col2:
        with st.container(border=True):
            year_level = grades.get_year_level()
            st.metric(f'{ls_retainment[year_level][0]} Retainment', ls_retainment[year_level][1])
            add_vertical_space(1)
    with col3:
        with st.container(border=True):
            st.caption('RETAINMENT SOURCE')
            st.write('Data is based from the 2023 Student Handbook.')


    if st.session_state.remaining_units:
        remaining = st.session_state.remaining_units
        # Row 4
        st.caption('LATIN HONORS')

        col1, col2, col3 = st.columns([0.2, 0.45, 0.35])
        with col1:
            with st.container(border=True):
                st.metric(label='Completed Units', value=grades.completed_units(), delta=f'+{grades.completed_units_delta()} units')
            with st.container(border=True):
                st.metric(label='Remaining Units', value=remaining)
        with col2:
            with st.container(border=True):
                total = grades.completed_units() + remaining
                percent = round(grades.completed_units() * 100 / total,2)
                plot_gauge(percent, '#00BFFF', f'%', 'IPS Progress in Percent', 100)            
        with col3:
            with st.container(border=True):
                honor = st.session_state.check_eligibility
                highest_possible = grades.check_highest_possible(remaining, {'A':100}, by_percent=True)
                minimum_required = grades.check_minimum_required(remaining, honor)
                eligibility_text = 'Possible 🥳' if highest_possible >= honors_dict[honor][0] else 'Impossible' 

                st.metric(label=f'{st.session_state.check_eligibility} is...', value=eligibility_text, help="Highest attainable QPI assumes an **'A'** in all remaining courses.")
                if highest_possible >= honors_dict[honor][0]:
                    st.caption(f'To do this, get a minimum QPI of {minimum_required} on your remaining {remaining} units.')
                st.write(f'Highest attainable QPI: {highest_possible}\nHonor range: {honors_dict[honor][0]} to {honors_dict[honor][-1]}')

        add_vertical_space(1)

        # Row 5
        st.caption('ESTIMATING CHANCES')
        with st.expander('Realistically, it is hard to get *A*s on **all** remaining courses. Want to estimate your chances better?', expanded=False):
            st.write(':grey[Let\'s estimate your performance on your **remaining courses**. Choose between estimating by percentage (aproximate) or by number of units (precise).]')
            letters = ['A', 'B+', 'B', 'C+', 'C']
            tab1, tab2 = st.tabs(['Estimate approximately', 'Estimate precisely'])

            def row_5_execute(bool1, d, bool2):
                if bool1:
                    with st.container(border=True):
                        honor = st.session_state.check_eligibility
                        highest_possible = grades.check_highest_possible(remaining, d, by_percent=bool2)
                        eligibility_text = 'Possible 🥳' if highest_possible >= honors_dict[honor][0] else 'Impossible' 
                        st.metric(label=f'{st.session_state.check_eligibility} is...', value=eligibility_text)
                    n1, n2 = st.columns(2)
                    with n1:
                        with st.container(border=True):
                            st.metric(label='Estimated QPI', value=highest_possible)
                    with n2:
                        with st.container(border=True):
                            st.metric(label='Target QPI', value=honors_dict[honor][0])

            with tab1:
                col1, col2 = st.columns([0.5,0.5], gap='small')
                with col1:
                    percent_sum, percent_dict = 0,{}
                    for letter in letters:
                        st.number_input(f'How much of your remaining units will be :blue[**{letter}**]?', min_value=0, max_value=100, step=10, key=letter)
                        percent_sum += st.session_state[letter]
                        percent_dict[letter] = st.session_state[letter]
                with col2:
                    with st.container(border=True):
                        st.write('Percentage Sum')
                        if percent_sum > 100:
                            progress_text = f'Total: :red[{percent_sum}%]'
                            st.warning(f'Percent is currently at **{percent_sum}%**. Please set total to 100% only.', icon="⚠️")
                        else:
                            st.progress(percent_sum, text=f'{percent_sum}%')
                            if percent_sum == 100:
                                st.button('Estimate my chances', key='estimate_p')
                                row_5_execute(st.session_state.estimate_p, percent_dict, True)
                    

            with tab2:
                col1, col2 = st.columns([0.5,0.5], gap='small')
                with col1:
                    unit_sum, unit_dict = 0,{}
                    for letter in letters:
                        st.number_input(f'How many of your remaining units will be :blue[**{letter}**]?', min_value=0, max_value=remaining, step=1, key=f'{letter}_uc')
                        unit_sum += st.session_state[f'{letter}_uc']
                        unit_dict[letter] = st.session_state[f'{letter}_uc']
                with col2:
                    with st.container(border=True):
                        st.write(' Total Number of Units')
                        if unit_sum > remaining:
                            progress_text = f'Total: :red[{percent_sum}%]'
                            st.warning(f'Number of units is currently at **{unit_sum}%**. Please set total to {remaining} units only.', icon="⚠️")
                        else:
                            st.progress(unit_sum/remaining, text=f'{unit_sum}/{remaining}')
                            if unit_sum == remaining:
                                st.button('Estimate my chances', key='estimate_uc')
                                row_5_execute(st.session_state.estimate_uc, unit_dict, False)
        
        add_vertical_space(1)

    # No sidebar input
    else:
        add_vertical_space(1)
        st.info('Unlock more analysis by using the **MORE TOOLS** section on the sidebar!')

    # Row 6
    if st.session_state.courses:
        st.caption('QPI ANALYSIS')

        if 'show_qpi' not in st.session_state:
            st.session_state.show_qpi = False
        with st.container(border=True):
            qpi = (grades.analyze_courses_qpi(st.session_state.courses))
            df = grades.analyze_courses(st.session_state.courses).reset_index()
            fig = px.bar(df, x='Subject Code', y='Numerical Grade',
                color='Course',
                category_orders={'Subject Code':df['Subject Code']},
                title='Letter Grade by Specified Course Code',
                text='Final Grade',
                height=300,
            )
            if st.session_state.show_qpi:
                fig.add_hline(y=qpi, line_width=1, line_color='snow',
                    line_dash="dot",
                    annotation_text=f"Average Grade ({qpi})", 
                    annotation_position="top right",
                    annotation_font_size=13,
                    annotation_font_color="snow"
                )
            fig.update_layout(margin=dict(l=30, r=30, t=50, b=20))
            st.plotly_chart(fig, use_container_width=True)

            st.toggle(f"Show Weighted Average (for {', '.join(st.session_state.courses)})", key='show_qpi')

        add_vertical_space(1)