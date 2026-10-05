from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Count, Avg, Sum
from django.http import HttpResponse
from .models import Student, Subject, Attendance, Marks
from .forms import (
    StudentForm,
    SubjectForm,
    AttendanceForm,
    MarksForm,
    StudentRegistrationForm,
)
from .analytics import (
    get_attendance_dataframe,
    get_marks_dataframe,
    get_student_attendance_percentage,
    get_subject_attendance_percentage,
    get_students_below_attendance,
    calculate_attendance_statistics,
    calculate_marks_statistics,
    get_subject_wise_averages,
    rank_students_by_average,
)
from .charts import (
    plot_subject_wise_marks,
    plot_student_attendance,
    plot_subject_wise_attendance,
    plot_student_performance,
)


def is_teacher(user):
    return user.is_staff or user.is_superuser


def home(request):
    """Home page"""
    return render(request, 'students/home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if is_teacher(user):
                messages.success(request, 'Welcome, Teacher/Admin!')
                return redirect('teacher_dashboard')
            else:
                try:
                    student = user.student_profile
                    messages.success(request, 'Welcome, Student!')
                    return redirect('student_dashboard')
                except Student.DoesNotExist:
                    messages.warning(request, 'No student profile linked. Redirecting to teacher dashboard.')
                    return redirect('teacher_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'students/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('home')


@login_required
@user_passes_test(is_teacher, login_url='login')
def teacher_dashboard(request):
    total_students = Student.objects.count()
    total_subjects = Subject.objects.count()
    total_attendance = Attendance.objects.count()
    total_marks = Marks.objects.count()
    
    # Average class marks
    avg_marks = Marks.objects.aggregate(avg_total=Avg('total_marks'))['avg_total'] or 0
    
    # Students below 75% attendance
    below_75 = get_students_below_attendance(threshold=75)
    
    # Recent attendance
    recent_attendance = Attendance.objects.all()[:10]
    # Recent marks
    recent_marks = Marks.objects.all()[:10]
    
    context = {
        'total_students': total_students,
        'total_subjects': total_subjects,
        'total_attendance': total_attendance,
        'total_marks': total_marks,
        'avg_marks': round(avg_marks, 2),
        'below_75_count': len(below_75),
        'below_75': below_75,
        'recent_attendance': recent_attendance,
        'recent_marks': recent_marks,
    }
    return render(request, 'students/teacher_dashboard.html', context)


@login_required
def student_dashboard(request):
    try:
        if is_teacher(request.user):
            messages.info(request, 'Teacher view requested - redirecting to teacher dashboard.')
            return redirect('teacher_dashboard')
        student = get_object_or_404(Student, user=request.user)
    except:
        student = None
        if is_teacher(request.user):
            return redirect('teacher_dashboard')
        messages.error(request, 'Student profile not found.')
        return redirect('home')
    
    # Overall attendance
    overall_attendance = get_student_attendance_percentage(student)
    
    # Subject-wise attendance
    subject_attendance = []
    subjects = Subject.objects.filter(attendances__student=student).distinct()
    for subject in subjects:
        pct = get_subject_attendance_percentage(student, subject)
        subject_attendance.append({
            'subject': subject,
            'percentage': pct
        })
    
    # Marks
    marks_list = Marks.objects.filter(student=student)
    # Average marks
    avg_marks = sum(m.total_marks for m in marks_list) / len(marks_list) if marks_list else 0
    
    context = {
        'student': student,
        'overall_attendance': round(overall_attendance, 2),
        'subject_attendance': subject_attendance,
        'marks_list': marks_list,
        'avg_marks': round(avg_marks, 2),
    }
    return render(request, 'students/student_dashboard.html', context)


# Student CRUD views
@login_required
@user_passes_test(is_teacher, login_url='login')
def student_list(request):
    query = request.GET.get('q')
    students = Student.objects.all()
    if query:
        students = students.filter(
            Q(student_id__icontains=query) |
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(course__icontains=query)
        )
    context = {'students': students, 'query': query}
    return render(request, 'students/student_list.html', context)


@login_required
@user_passes_test(is_teacher, login_url='login')
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    marks_list = Marks.objects.filter(student=student)
    attendance_records = Attendance.objects.filter(student=student)[:20]
    overall_attendance = get_student_attendance_percentage(student)
    context = {
        'student': student,
        'marks_list': marks_list,
        'attendance_records': attendance_records,
        'overall_attendance': round(overall_attendance, 2)
    }
    return render(request, 'students/student_detail.html', context)


@login_required
@user_passes_test(is_teacher, login_url='login')
def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully.')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/student_add.html', {'form': form})


@login_required
@user_passes_test(is_teacher, login_url='login')
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully.')
            return redirect('student_detail', pk=pk)
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_edit.html', {'form': form, 'student': student})


@login_required
@user_passes_test(is_teacher, login_url='login')
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully.')
        return redirect('student_list')
    return render(request, 'students/student_delete.html', {'student': student})


# Subject CRUD
@login_required
@user_passes_test(is_teacher, login_url='login')
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'students/subject_list.html', {'subjects': subjects})


@login_required
@user_passes_test(is_teacher, login_url='login')
def subject_add(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject added successfully.')
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'students/subject_add.html', {'form': form})


@login_required
@user_passes_test(is_teacher, login_url='login')
def subject_edit(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject updated successfully.')
            return redirect('subject_list')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'students/subject_edit.html', {'form': form, 'subject': subject})


@login_required
@user_passes_test(is_teacher, login_url='login')
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted successfully.')
        return redirect('subject_list')
    return render(request, 'students/subject_delete.html', {'subject': subject})


# Attendance
@login_required
@user_passes_test(is_teacher, login_url='login')
def attendance_list(request):
    attendances = Attendance.objects.all()[:200]
    return render(request, 'students/attendance_list.html', {'attendances': attendances})


@login_required
@user_passes_test(is_teacher, login_url='login')
def attendance_add(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Attendance recorded successfully.')
                return redirect('attendance_list')
            except Exception as e:
                messages.error(request, f'Error saving attendance: {str(e)}')
    else:
        form = AttendanceForm()
    return render(request, 'students/attendance_add.html', {'form': form})


@login_required
@user_passes_test(is_teacher, login_url='login')
def attendance_edit(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Attendance updated successfully.')
                return redirect('attendance_list')
            except Exception as e:
                messages.error(request, f'Error updating attendance: {str(e)}')
    else:
        form = AttendanceForm(instance=attendance)
    return render(request, 'students/attendance_edit.html', {'form': form, 'attendance': attendance})


@login_required
@user_passes_test(is_teacher, login_url='login')
def attendance_delete(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        attendance.delete()
        messages.success(request, 'Attendance deleted successfully.')
        return redirect('attendance_list')
    return render(request, 'students/attendance_delete.html', {'attendance': attendance})


# Marks
@login_required
@user_passes_test(is_teacher, login_url='login')
def marks_list(request):
    marks = Marks.objects.all()
    return render(request, 'students/marks_list.html', {'marks': marks})


@login_required
@user_passes_test(is_teacher, login_url='login')
def marks_add(request):
    if request.method == 'POST':
        form = MarksForm(request.POST)
        if form.is_valid():
            try:
                mark = form.save(commit=False)
                mark.total_marks = mark.calculate_total()
                mark.grade = mark.calculate_grade()
                mark.save()
                messages.success(request, 'Marks added successfully.')
                return redirect('marks_list')
            except Exception as e:
                messages.error(request, f'Error saving marks: {str(e)}')
    else:
        form = MarksForm()
    return render(request, 'students/marks_add.html', {'form': form})


@login_required
@user_passes_test(is_teacher, login_url='login')
def marks_edit(request, pk):
    mark = get_object_or_404(Marks, pk=pk)
    if request.method == 'POST':
        form = MarksForm(request.POST, instance=mark)
        if form.is_valid():
            try:
                mark = form.save(commit=False)
                mark.total_marks = mark.calculate_total()
                mark.grade = mark.calculate_grade()
                mark.save()
                messages.success(request, 'Marks updated successfully.')
                return redirect('marks_list')
            except Exception as e:
                messages.error(request, f'Error updating marks: {str(e)}')
    else:
        form = MarksForm(instance=mark)
    return render(request, 'students/marks_edit.html', {'form': form, 'mark': mark})


@login_required
@user_passes_test(is_teacher, login_url='login')
def marks_delete(request, pk):
    mark = get_object_or_404(Marks, pk=pk)
    if request.method == 'POST':
        mark.delete()
        messages.success(request, 'Marks deleted successfully.')
        return redirect('marks_list')
    return render(request, 'students/marks_delete.html', {'mark': mark})


# Analytics views
@login_required
@user_passes_test(is_teacher, login_url='login')
def analytics_dashboard(request):
    # Get dataframes for analysis
    attendance_df = get_attendance_dataframe()
    marks_df = get_marks_dataframe()
    
    # Attendance statistics
    att_stats = calculate_attendance_statistics()
    
    # Marks statistics
    marks_stats = calculate_marks_statistics()
    
    # Subject-wise averages
    subject_averages = get_subject_wise_averages()
    
    # Ranked students
    ranked_students = rank_students_by_average()
    
    # Students below 75% attendance
    below_75 = get_students_below_attendance(threshold=75)
    
    context = {
        'attendance_stats': att_stats,
        'marks_stats': marks_stats,
        'subject_averages': subject_averages,
        'ranked_students': ranked_students,
        'below_75': below_75,
    }
    return render(request, 'students/analytics_dashboard.html', context)


@login_required
@user_passes_test(is_teacher, login_url='login')
def generate_charts(request):
    # Generate charts and save to media/static
    try:
        subject_marks_img = plot_subject_wise_marks()
        student_att_img = plot_student_attendance()
        subject_att_img = plot_subject_wise_attendance()
        student_perf_img = plot_student_performance()
        messages.success(request, 'Charts generated successfully.')
        context = {
            'charts': {
                'subject_marks': subject_marks_img,
                'student_attendance': student_att_img,
                'subject_attendance': subject_att_img,
                'student_performance': student_perf_img,
            }
        }
    except Exception as e:
        messages.error(request, f'Error generating charts: {str(e)}')
        context = {'error': str(e)}
    
    return render(request, 'students/charts.html', context)


def student_register(request):
    if request.user.is_authenticated:
        if is_teacher(request.user):
            return redirect('teacher_dashboard')
        try:
            return redirect('student_dashboard')
        except Exception:
            pass

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            # Create user
            username = cleaned['student_id'].lower()
            user = User.objects.create_user(
                username=username,
                email=cleaned['email'],
                password=cleaned['password'],
                first_name=cleaned['full_name'].split()[0] if cleaned['full_name'] else '',
                last_name=' '.join(cleaned['full_name'].split()[1:]) if len(cleaned['full_name'].split()) > 1 else ''
            )
            # Create student profile
            Student.objects.create(
                student_id=cleaned['student_id'],
                name=cleaned['full_name'],
                email=cleaned['email'],
                phone=cleaned['phone'],
                course=cleaned['course'],
                semester=cleaned['semester'],
                division=cleaned['division'],
                user=user
            )
            # Log user in
            login(request, user)
            messages.success(request, 'Registration successful. Welcome to Student Dashboard!')
            return redirect('student_dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'students/student_register.html', {'form': form})
