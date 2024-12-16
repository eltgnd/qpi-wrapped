# Packages
import time
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from shillelagh.backends.apsw.db import connect
from streamlit_extras.add_vertical_space import add_vertical_space
# from st_pages import Page, show_pages

# Initialize
st.set_page_config(page_title='QPI Wrapped', page_icon='📉', layout="centered", initial_sidebar_state="auto", menu_items=None)
ss = st.session_state

# show_pages(
#     [
#         Page("Home.py", "Dashboard", ":house:"),
#         Page("pages/2_Feedback and More.py", "Feedback and More", ":blue_heart:"),
#         Page('pages/3_Update Log.py', 'Update Log', ':scroll:'),
#         Page('pages/4_About Me.py', 'About Me', ':boy:')
#     ]
# )

# Imported files
from grades import Grades, honors_dict
from ui import *
from sample_data import sample_data
from gauge import plot_gauge
from scholarship_retainment import scholarships

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
    'Very Weak': (0.0, 0.19),
    'Weak': (0.2, 0.39),
    'Moderate': (0.4, 0.59),
    'Strong': (0.6, 0.79),
    'Very High': (0.8, 1.0)
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
    'option':False,
    'grade_submit':False,
    'latin_honor_toast':False,
    'submit':False,
    'scholar':False,
    'duration':None,
    'scholarship_type':'Academic',
    'notification':False,
    'compare':False
    }

for key,val in input_vars.items():
    if key not in ss:
        ss[key] = val
def grade_submit(grades):
    with st.spinner('Creating your QPI Wrapped...'):
        time.sleep(3)
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

# Notification
if not ss.notification:
    st.toast('Hey there! QPI Wrapped just got updated with new features!', icon='🥳')
    ss.notification = True

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
    ui_sidebar()

    ### Start of Dashboard

    options = ['SUMMARY', 'TRENDS', 'RETAINMENT', 'INVESTIGATE', 'LATIN HONORS', 'ANALYSIS', 'PREDICT']
    st.pills('', options, default='SUMMARY', key='tab')
    add_vertical_space(1)


    if ss.tab == 'SUMMARY':
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

        col1, col2, col3 = st.columns(3)
        with col1:
            with st.container(border=True):      
                highest_qpi = grades.qpi_by_semester(True).sort_values(by='QPI', ascending=False).iloc[0]
                st.metric(label=f'Maximum QPI *({highest_qpi.Semester})*', value=f'{highest_qpi.QPI}💪')
        with col2:
            with st.container(border=True):      
                lowest_qpi = grades.qpi_by_semester(True).sort_values(by='QPI', ascending=True).iloc[0]
                st.metric(label=f'Minimum QPI *({lowest_qpi.Semester})*', value=f'{lowest_qpi.QPI}🪴')
        with col3:
            with st.container(border=True):     
                highest_units = grades.group_by_units().sort_values(by='Units', ascending=False).iloc[0]
                st.metric(label=f'Max Units Taken *({highest_units.Semester})*', value=f'{highest_units.Units} units 📋')

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


    if ss.tab == 'TRENDS':
        # Row 2
        st.caption('QPI TREND')

        with st.container(border=True):
            sem,year = st.tabs(['By Semester', 'By School Year'])
            with sem:
                fig = px.line(grades.qpi_by_semester(ss.option), x='Semester', y='QPI', 
                    title='QPI by Semester',
                    markers=True,
                    text='QPI',
                    height=300)
                fig.update_traces(textposition="top center")
                fig.update_layout(margin=dict(l=30, r=30, t=50, b=20))
                st.plotly_chart(fig, use_container_width=True)
                st.toggle('Exclude Intersession QPI', key='option')
            with year:
                yearly_qpis = grades.all_yearly_qpi(return_as_df=True)
                fig = px.line(yearly_qpis,x='School Year', y='QPI', 
                    title='QPI by School Year',
                    markers=True,
                    text='QPI',
                    height=300)
                fig.update_traces(textposition="top center")
                fig.update_layout(margin=dict(l=30, r=30, t=50, b=20))
                st.plotly_chart(fig, use_container_width=True)

        add_vertical_space(1)

        # Row 4
        st.caption('LETTER GRADE TREND')
        with st.container(border=True):
            semester_count = grades.df['Semester'].nunique()
            col1, col2 = st.columns([3,1])
            letters = col1.multiselect('Select letter grade/s', grades_color_map.keys(), default=['A', 'B+', 'B'])
            col2.write('\n')
            stack = col2.toggle('Stack bars', value=semester_count>9)
        with st.container(border=True):
            df = grades.letter_trend(letters)
            fig = px.bar(df, x='Semester', y='Count',
                color='Final Grade',
                title='Letter Grade Trend',
                height=350,
                color_discrete_map=grades_color_map,
                barmode='stack' if stack else 'group')
            fig.update_layout(margin=dict(l=35, r=35, t=50, b=20))
            st.plotly_chart(fig, use_container_width=True)

        add_vertical_space(1)


    if ss.tab == 'INVESTIGATE':
        st.write('\n')
        st.caption('GRADE ANALYSIS')
        course_choices = grades.qpi_by_course(minimum_courses=1).sort_values(by='Subjects', ascending=False).reset_index()['Course']
        st.multiselect('Select at least one class code!', options=course_choices, key='courses', placeholder=course_choices[0])

        add_vertical_space(1)

        # Row 10
        if ss.courses:

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
                    fig.add_hline(y=qpi, line_width=2, line_color='darkblue',
                        line_dash="dot",
                        annotation_text=f"Weighted Average", 
                        annotation_position="bottom right",
                        annotation_font_size=13,
                        annotation_font_color="darkblue"
                    )
                fig.update_layout(margin=dict(l=30, r=30, t=50, b=20))
                st.plotly_chart(fig, use_container_width=True)

                st.write(f'**Weighted average of selected courses**: {qpi}')
                st.toggle(f"Show Weighted Average Line", key='show_qpi')

            add_vertical_space(1)

        # Row 11
        st.caption('COMPARE PERFORMANCE BETWEEN CLASS CODES')
        st.write('You can select more than one class code per group.')
        with st.container(border=True):
            group_num = st.slider('Number of groups', min_value=2, max_value=len(course_choices))

        with st.form(key='compare'):
            col1, col2 = st.columns(2)
            for i in range(group_num):
                col1.multiselect(f'Group {i+1}', options=course_choices, placeholder=course_choices[i], key=f'group_{i}')
            submit_compare = st.form_submit_button("Compare")

        if submit_compare:
            # Check if non-empty
            complete = True
            group_qpis = {}
            for i in range(group_num):
                if len(ss[f'group_{i}']) > 0:
                    group_qpis[f'Group {i+1}'] = (grades.analyze_courses_qpi(ss[f'group_{i}']))
                else:
                    st.warning('A group has no inputted course codes. Please try again!')
                    complete = False
                    break
            
            if complete:
                with st.container(border=True):
                    df = pd.DataFrame({'Group':group_qpis.keys(), 'Weighted Average':group_qpis.values()})
                    fig = px.bar(df, x='Weighted Average', y='Group',
                        title='Weighted Average Comparison',
                        height=332,
                        orientation='h'
                    )
                    st.plotly_chart(fig, use_container_width=True)


    if ss.tab == 'ANALYSIS':
        # Row 5
        st.caption('QPI CORRELATION')
        st.write('🤔 What\'s the correlation between your QPI and the number of units you\'ve taken?')
        col1, col2 = st.columns([0.8,0.2])
        with col1:
            with st.container(border=True):
                df = grades.qpi_vs_units()

                fig = go.Figure(layout_title_text="QPI vs Units")
                fig.add_trace(go.Scatter(x=df.Units, y=df.QPI, 
                    name='QPI vs Units',
                    text=df.QPI,
                    mode='markers+text',
                    marker=dict(color='royalblue', size=10)
                    )
                )

                # Linear regression
                model = np.polyfit(df.Units, df.QPI, 1)
                mn, mx = df.Units.min(), df.Units.max()
                x_line = [i for i in range(mn,mx+1,1)]
                y_line = [(model[0]*x + model[1]) for x in x_line]

                fig.add_trace(go.Scatter(x=x_line, y=y_line,
                    name='Best fit line',
                    line=dict(color='royalblue', width=1, dash='dot'),
                    mode='lines'
                    )
                )
                fig.update_traces(textposition="top center")
                fig.update_layout(legend=dict(
                    orientation='h',yanchor="top",y=-0.35,xanchor="left",x=-0.1), 
                    margin=dict(l=30, r=30, t=60, b=20),
                    height=310
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
                sign = 'inverse' if label in ['Weak', 'Very Weak'] else 'normal'
                st.metric(label='Correlation\n\ncoefficient (r)', value=orig_corr, delta=label, delta_color=sign if label != 'Moderate' else 'off')
            with st.container(border=True):
                st.write(f'What does *r* ({orig_corr}) mean?')
                st.caption("r quantifies the linear strength from -1 (inverse) to 1 (direct).")

        add_vertical_space(1)

        # Row 12
        st.caption('QPI INFERENCE')



    if ss.tab == 'RETAINMENT':
        # Row 6
        st.caption('YEARLY QPI RETAINMENT')
        col1, col2 = st.columns([2,4.5])
        year_level = grades.get_year_level()
        yearly_qpis = grades.all_yearly_qpi()
        with col1:
            val = '✔️' if grades.latest_yearly_qpi() >= ls_retainment[year_level][1] else '⚠️'
            with st.container(border=True):
                st.metric(f'{ls_retainment[year_level][0]} Retainment', float(ls_retainment[year_level][1]))
            with st.container(border=True):
                previous_school_year = None if year_level == 1 else grades.adjust_school_year(grades.last_sem[:-2], -1)
                yearly_delta = round(grades.latest_yearly_qpi() - grades.yearly_qpi(previous_school_year),3)
                st.metric(f'Current Yearly QPI', f'{grades.latest_yearly_qpi()}  {val}')
            with st.container(border=True):
                st.metric('Relative Percent', value=f'{round((grades.latest_yearly_qpi()/float(ls_retainment[year_level][1]))*100,2)}%', help='Your QPI is this percent higher than the required retainment grade.')

        with col2:
            with st.container(border=True):
                df = pd.DataFrame({
                    'School Year': yearly_qpis.keys(),
                    'Yearly QPI': yearly_qpis.values(),
                    'Retainment QPI': [ls_retainment[i][-1] for i in range(1,year_level+1)]
                })
                fig = px.bar(df, x='School Year', y=['Yearly QPI', 'Retainment QPI'],
                    title='Yearly QPI vs Retainment QPI per School Year',
                    height=320,
                    barmode='group')
                fig.update_layout(margin=dict(l=35, r=35, t=40, b=5))
                st.plotly_chart(fig, use_container_width=True)

        add_vertical_space(1)

        # Row 7
        st.caption("SCHOLARS' YEARLY QPI RETAINMENT")

        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.selectbox('Scholarship Type',scholarships.keys(), key='scholarship_type')
        with col2:
            with st.container(border=True):
                st.caption('Retainment data is based from the OAA Scholars\' Hub as of 12/16/2024.')
                add_vertical_space(1)

        # Yearly
        # Check if there is letter grade retainment requirement
        chosen_scholarship = scholarships[ss.scholarship_type]
        has_letter_grade_retainment = False
        if isinstance(chosen_scholarship[year_level]['Yearly'], list):
            has_letter_grade_retainment = True

        col1, col2 = st.columns([4, 1 if has_letter_grade_retainment else 0.001])
        with col1: 
            with st.container(border=True):
                retainment = [chosen_scholarship[year]['Yearly'] if isinstance(chosen_scholarship[year]['Yearly'], float) else chosen_scholarship[year]['Yearly'][-1] for year in range(1, year_level+1)]
                df = pd.DataFrame({
                    'School Year': yearly_qpis.keys(),
                    'Yearly QPI': yearly_qpis.values(),
                    'Retainment QPI': retainment
                })
                fig = px.bar(df, x='School Year', y=['Yearly QPI', 'Retainment QPI'],
                    title='Yearly QPI vs Scholar\'s Retainment QPI per School Year',
                    height=305,
                    barmode='group')
                fig.update_layout(margin=dict(l=35, r=35, t=40, b=10))
                st.plotly_chart(fig, use_container_width=True)

        if has_letter_grade_retainment:
            letters = chosen_scholarship[year_level]['Yearly'][0]
            with col2:
                for letter in letters.keys():
                    with st.container(border=True):
                        st.metric(f'Total **{letter}**s', grades.get_total_letters(letter))

        if ss.duration == 'Current Semester':
            st.info('Currently under development!')
            # render_semester_retainment(grades.last_sem[-1], ss.scholarship_type, year_level)


    if ss.tab == 'LATIN HONORS':

        st.write('**🎓 Latin Honor Eligibility**')
        st.number_input('How many computable units do you have left?', step=1, min_value=0, help='Computable units refer to units used in computing your cumulative QPI (e.g. PE is not included)', key='remaining_units')
        if st.session_state.remaining_units != 0:

            if not ss['latin_honor_toast']:
                st.toast('Scroll down to find the Latin Honor Eligibility section!', icon='👋')
            latin_honor_toast()

            st.selectbox('Check eligibility', honors_dict.keys(), index=3, key='check_eligibility')

        if st.session_state.remaining_units:
            remaining = st.session_state.remaining_units
            # Row 8
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
                        if minimum_required > 0:
                            st.caption(f'To do this, get a minimum QPI of {minimum_required} on your remaining {remaining} units.')
                with st.container(border=True):
                    st.metric('Highest attainable QPI', highest_possible)
                    # st.write(f'Highest attainable QPI: {highest_possible}\nHonor range: {honors_dict[honor][0]} to {honors_dict[honor][-1]}')

            add_vertical_space(1)

            # Row 9
            st.caption('ESTIMATING CHANCES')
            with st.expander('Realistically, it is hard to get *A*s on **all** remaining courses. Want to estimate your chances better?', expanded=True):
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