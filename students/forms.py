from django import forms
from django.contrib.auth.models import User
from .models import Student, Subject, Attendance, Marks


class StudentRegistrationForm(forms.Form):
    full_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    student_id = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    course = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    semester = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    division = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if Student.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError("Student ID already exists.")
        if User.objects.filter(username=student_id.lower()).exists():
            raise forms.ValidationError("Username already exists.")
        return student_id

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Student.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'name', 'email', 'phone', 'course', 'semester', 'division']
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.TextInput(attrs={'class': 'form-control'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control'}),
            'division': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject_id', 'subject_name', 'subject_code', 'semester']
        widgets = {
            'subject_id': forms.TextInput(attrs={'class': 'form-control'}),
            'subject_name': forms.TextInput(attrs={'class': 'form-control'}),
            'subject_code': forms.TextInput(attrs={'class': 'form-control'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'subject', 'date', 'status']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class MarksForm(forms.ModelForm):
    class Meta:
        model = Marks
        fields = ['student', 'subject', 'internal_marks', 'assignment_marks', 'practical_marks', 'external_marks']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'internal_marks': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'assignment_marks': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'practical_marks': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'external_marks': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }
