import pandas as pd
import numpy as np
from django.db.models import Count, Avg, Q
from .models import Student, Subject, Attendance, Marks


def get_attendance_dataframe():
    """Convert attendance data into Pandas DataFrame"""
    attendances = Attendance.objects.all().values(
        'student__name', 'student__student_id', 'subject__subject_name',
        'date', 'status'
    )
    if not attendances:
        return pd.DataFrame()
    df = pd.DataFrame(attendances)
    return df


def get_marks_dataframe():
    """Convert marks data into Pandas DataFrame"""
    marks = Marks.objects.all().values(
        'student__name', 'student__student_id', 'subject__subject_name',
        'internal_marks', 'assignment_marks', 'practical_marks',
        'external_marks', 'total_marks', 'grade'
    )
    if not marks:
        return pd.DataFrame()
    df = pd.DataFrame(marks)
    return df


def get_student_attendance_percentage(student):
    """Calculate attendance percentage for a specific student"""
    total_classes = Attendance.objects.filter(student=student).count()
    if total_classes == 0:
        return 0
    present_classes = Attendance.objects.filter(student=student, status='Present').count()
    percentage = (present_classes / total_classes) * 100
    return percentage


def get_subject_attendance_percentage(student, subject):
    """Calculate subject-wise attendance percentage"""
    total_classes = Attendance.objects.filter(student=student, subject=subject).count()
    if total_classes == 0:
        return 0
    present_classes = Attendance.objects.filter(student=student, subject=subject, status='Present').count()
    percentage = (present_classes / total_classes) * 100
    return percentage


def get_students_below_attendance(threshold=75):
    """Identify students with attendance below threshold"""
    students = Student.objects.all()
    below_list = []
    for student in students:
        pct = get_student_attendance_percentage(student)
        if pct < threshold and pct >= 0:
            below_list.append({
                'student': student,
                'attendance_percentage': round(pct, 2)
            })
    return below_list


def calculate_attendance_statistics():
    """Calculate attendance statistics using Pandas and NumPy"""
    df = get_attendance_dataframe()
    if df.empty:
        return {
            'total_records': 0,
            'present_count': 0,
            'absent_count': 0,
            'attendance_rate': 0
        }
    total_records = len(df)
    present_count = len(df[df['status'] == 'Present'])
    absent_count = len(df[df['status'] == 'Absent'])
    attendance_rate = (present_count / total_records * 100) if total_records > 0 else 0
    
    return {
        'total_records': total_records,
        'present_count': present_count,
        'absent_count': absent_count,
        'attendance_rate': round(attendance_rate, 2)
    }


def calculate_marks_statistics():
    """Calculate mean, min, max marks using Pandas and NumPy"""
    df = get_marks_dataframe()
    if df.empty:
        return {
            'total_marks_records': 0,
            'mean_marks': 0,
            'min_marks': 0,
            'max_marks': 0,
            'median_marks': 0,
            'std_dev': 0
        }
    mean_marks = df['total_marks'].mean()
    min_marks = df['total_marks'].min()
    max_marks = df['total_marks'].max()
    median_marks = df['total_marks'].median()
    std_dev = df['total_marks'].std()
    
    return {
        'total_marks_records': len(df),
        'mean_marks': round(float(mean_marks), 2),
        'min_marks': float(min_marks),
        'max_marks': float(max_marks),
        'median_marks': round(float(median_marks), 2),
        'std_dev': round(float(std_dev), 2) if not np.isnan(std_dev) else 0
    }


def get_subject_wise_averages():
    """Calculate subject-wise average marks"""
    df = get_marks_dataframe()
    if df.empty:
        return []
    subject_avg = df.groupby('subject__subject_name')['total_marks'].mean().reset_index()
    subject_avg = subject_avg.sort_values('subject__subject_name')
    result = []
    for _, row in subject_avg.iterrows():
        result.append({
            'subject_name': row['subject__subject_name'],
            'average_marks': round(float(row['total_marks']), 2)
        })
    return result


def rank_students_by_average():
    """Rank students based on average marks"""
    df = get_marks_dataframe()
    if df.empty:
        return []
    student_avg = df.groupby(['student__name', 'student__student_id'])['total_marks'].mean().reset_index()
    student_avg['rank'] = student_avg['total_marks'].rank(method='min', ascending=False)
    student_avg = student_avg.sort_values('total_marks', ascending=False)
    result = []
    for idx, row in student_avg.iterrows():
        result.append({
            'student_name': row['student__name'],
            'student_id': row['student__student_id'],
            'average_marks': round(float(row['total_marks']), 2),
            'rank': int(row['rank'])
        })
    return result
