import os
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from django.conf import settings
from django.db.models import Count, Avg
from .models import Student, Subject, Attendance, Marks

# Ensure media directory exists
os.makedirs(settings.MEDIA_ROOT, exist_ok=True)


def plot_subject_wise_marks():
    """Generate subject-wise average marks bar chart"""
    subjects = Subject.objects.all()
    if not subjects:
        return None
    data = []
    labels = []
    for subject in subjects:
        avg = Marks.objects.filter(subject=subject).aggregate(avg=Avg('total_marks'))['avg'] or 0
        data.append(round(avg, 2))
        labels.append(subject.subject_code)
    
    plt.figure(figsize=(10, 6))
    plt.bar(labels, data, color='skyblue')
    plt.title('Subject-wise Average Marks')
    plt.xlabel('Subjects')
    plt.ylabel('Average Marks')
    plt.tight_layout()
    
    filename = 'subject_wise_marks.png'
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    plt.savefig(filepath)
    plt.close()
    return filename


def plot_student_attendance():
    """Generate student attendance percentage chart (top 10 students)"""
    students = Student.objects.all()[:10]
    if not students:
        return None
    data = []
    labels = []
    for student in students:
        total = Attendance.objects.filter(student=student).count()
        present = Attendance.objects.filter(student=student, status='Present').count()
        pct = (present / total * 100) if total > 0 else 0
        data.append(round(pct, 2))
        labels.append(student.student_id)
    
    plt.figure(figsize=(10, 6))
    plt.bar(labels, data, color='lightgreen')
    plt.title('Student Attendance Percentage (Top 10)')
    plt.xlabel('Student ID')
    plt.ylabel('Attendance %')
    plt.tight_layout()
    
    filename = 'student_attendance.png'
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    plt.savefig(filepath)
    plt.close()
    return filename


def plot_subject_wise_attendance():
    """Generate subject-wise attendance chart"""
    subjects = Subject.objects.all()
    if not subjects:
        return None
    data = []
    labels = []
    for subject in subjects:
        total = Attendance.objects.filter(subject=subject).count()
        present = Attendance.objects.filter(subject=subject, status='Present').count()
        pct = (present / total * 100) if total > 0 else 0
        data.append(round(pct, 2))
        labels.append(subject.subject_code)
    
    plt.figure(figsize=(10, 6))
    plt.bar(labels, data, color='orange')
    plt.title('Subject-wise Attendance Percentage')
    plt.xlabel('Subjects')
    plt.ylabel('Attendance %')
    plt.tight_layout()
    
    filename = 'subject_wise_attendance.png'
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    plt.savefig(filepath)
    plt.close()
    return filename


def plot_student_performance():
    """Generate student performance chart based on average marks (top 10)"""
    students = Student.objects.all()
    if not students:
        return None
    performance = []
    for student in students:
        marks = Marks.objects.filter(student=student)
        avg = sum(m.total_marks for m in marks) / len(marks) if marks else 0
        performance.append((student.student_id, round(avg, 2)))
    performance.sort(key=lambda x: x[1], reverse=True)
    performance = performance[:10]
    
    labels = [p[0] for p in performance]
    data = [p[1] for p in performance]
    
    plt.figure(figsize=(10, 6))
    plt.bar(labels, data, color='coral')
    plt.title('Student Performance - Average Marks (Top 10)')
    plt.xlabel('Student ID')
    plt.ylabel('Average Marks')
    plt.tight_layout()
    
    filename = 'student_performance.png'
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    plt.savefig(filepath)
    plt.close()
    return filename
