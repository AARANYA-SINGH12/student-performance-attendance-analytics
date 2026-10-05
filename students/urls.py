from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.student_register, name='student_register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    
    # Students
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_add, name='student_add'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    
    # Subjects
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/add/', views.subject_add, name='subject_add'),
    path('subjects/<int:pk>/edit/', views.subject_edit, name='subject_edit'),
    path('subjects/<int:pk>/delete/', views.subject_delete, name='subject_delete'),
    
    # Attendance
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/add/', views.attendance_add, name='attendance_add'),
    path('attendance/<int:pk>/edit/', views.attendance_edit, name='attendance_edit'),
    path('attendance/<int:pk>/delete/', views.attendance_delete, name='attendance_delete'),
    
    # Marks
    path('marks/', views.marks_list, name='marks_list'),
    path('marks/add/', views.marks_add, name='marks_add'),
    path('marks/<int:pk>/edit/', views.marks_edit, name='marks_edit'),
    path('marks/<int:pk>/delete/', views.marks_delete, name='marks_delete'),
    
    # Analytics
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('charts/', views.generate_charts, name='charts'),
]
