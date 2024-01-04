import pandas as pd

letters = {'A':4.00, 'B+':3.50, 'B':3.00, 'C+':2.50, 'C':2.00, 'D':1.00, 'F':0.00, 'W':0.00}
honors_dict = {
    "Summa Cum Laude": [3.87, 4.00],
    "Magna Cum Laude": [3.70, 3.86],
    "Cum Laude": [3.50, 3.69],
    "Honorable Mention": [3.35, 3.49]
}

def correct_format(grade):
    return True
def get_table(s, part_of_qpi_only=True):
    columns = 'School Year	Sem	Course	Subject Code	Course Title	Units	Final Grade'.split('	')

    grades = s.split('\n')
    grades = grades[1:] if grades[0][:6] == 'School' else grades

    if part_of_qpi_only:
        data = [grade.split('	') for grade in grades if correct_format(grade) and part_of_qpi(grade)]
    else:
        data = [grade.split('	') for grade in grades if correct_format(grade)]
    full_df = pd.DataFrame(data, columns=columns)
    
    full_df['Semester'] = full_df['School Year'] + '-' + full_df['Sem']
    df = full_df[['Semester', 'Subject Code', 'Units', 'Final Grade']]

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

class Grades:
    def __init__(self, s):
        self.df = get_table(s)
        self.df_full = get_table(s, False)
        self.last_sem = self.df.iloc[-1]['Semester']
        self.num_sem = self.df['Semester'].nunique()
        if self.num_sem < 2:
            self.df_delta = self.df.copy()
        else:
            self.df_delta = self.df[self.df['Semester'] != self.last_sem].copy()

    def compute_qpi(self, df):
        df['Units'] = pd.to_numeric(df['Units'], errors='coerce')
        df['Numerical Grade'] = df['Final Grade'].map(letters)
        total_units = df['Units'].sum()

        df['Weighted Grade'] = df['Units'] * df['Numerical Grade']
        weighted_grade = round(df['Weighted Grade'].sum() / total_units, 2)
        return weighted_grade

    def cumulative_qpi(self):
        return self.compute_qpi(self.df)

    def cumulative_qpi_delta(self):
        return self.compute_qpi(self.df_delta)
    
    def semester_qpi(self, sem):
        df = self.df
        new_df = df[df['Semester'] == sem].copy()
        return self.compute_qpi(new_df)    

    def latest_qpi(self):
        return self.semester_qpi(self.last_sem)

    def latest_qpi_delta(self):
        df = self.df_delta
        previous_sem = df.iloc[-1]['Semester']
        return self.semester_qpi(previous_sem)

    def dean_list(self):
        second_honor = 3.35
        first_honor = 3.7
        if self.latest_qpi() < second_honor:
            return False
        if second_honor <= self.latest_qpi() < first_honor:
            return 'Second Honors'
        else:
            return 'First Honors'
    
    def qpi_by_semester(self,exclude_intersession):
        semesters = self.df['Semester'].unique()
        if exclude_intersession:
            semesters = [sem for sem in semesters if sem[-1] != '0']
        qpi_lst = []
        for s in semesters:
            qpi_lst.append(self.semester_qpi(s))
        new_df = pd.DataFrame(data={'Semester':semesters, 'QPI':qpi_lst})
        return new_df
    
    def letter_frequency(self, option):
        df = self.df
        if option:
            df = df[df['Semester'] == self.last_sem].copy()
        return df.groupby('Final Grade')['Subject Code'].count().reset_index()

    def qpi_by_course(self, minimum_courses=2):
        df = self.df
        df['Units'] = pd.to_numeric(df['Units'], errors='coerce')
        df['Course'] = df['Subject Code'].str.split().str.get(0)
        new_df = df.groupby('Course').apply(lambda x: x['Weighted Grade'].sum() / x['Units'].sum()).reset_index()
        new_df['Subjects'] = df.groupby('Course')['Subject Code'].count().reset_index()['Subject Code']
        return new_df[new_df['Subjects'] >= minimum_courses]
        
    def completed_units(self):
        df = self.df
        df['Units'] = pd.to_numeric(df['Units'], errors='coerce')
        return df['Units'].sum()
    
    def completed_units_delta(self):
        df = self.df
        df = df[df['Semester'] == self.last_sem].copy()
        df['Units'] = pd.to_numeric(df['Units'], errors='coerce')
        return df['Units'].sum()
    
    def check_highest_possible(self, remaining_units, honor, b_plus_percent):
        df = self.df
        df['Units'] = pd.to_numeric(df['Units'], errors='coerce')
        b_plus_percent /= 100
        a_percent = 1-b_plus_percent

        total_weighted = df['Weighted Grade'].sum() + (4 * (a_percent*remaining_units)) + (3 * (b_plus_percent*remaining_units))
        total_units = df['Units'].sum() + remaining_units
        highest_possible = round(total_weighted / total_units, 2)

        return highest_possible

    def analyze_courses(self, courses):
        df = self.df
        filtered_df = df.query('Course in @courses')
        return filtered_df

    def qpi_vs_units(self):
        df = self.df
        qpi_sem_df = self.qpi_by_semester(exclude_intersession=True)
        grouped_df = df.groupby('Semester')['Units'].sum().reset_index()
        return pd.merge(qpi_sem_df, grouped_df, on='Semester')