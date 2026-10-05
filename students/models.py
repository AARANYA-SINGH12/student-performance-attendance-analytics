from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Subject(models.Model):
    subject_id = models.CharField(max_length=20, unique=True, verbose_name="Subject ID")
    subject_name = models.CharField(max_length=100, verbose_name="Subject Name")
    subject_code = models.CharField(max_length=20, unique=True, verbose_name="Subject Code")
    semester = models.IntegerField(verbose_name="Semester", validators=[MinValueValidator(1), MaxValueValidator(8)])

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code})"

    class Meta:
        ordering = ['semester', 'subject_name']


class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True, verbose_name="Student ID")
    name = models.CharField(max_length=100, verbose_name="Full Name")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=15, verbose_name="Phone")
    course = models.CharField(max_length=100, verbose_name="Course")
    semester = models.IntegerField(verbose_name="Semester", validators=[MinValueValidator(1), MaxValueValidator(8)])
    division = models.CharField(max_length=10, verbose_name="Division")
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='student_profile')

    def __str__(self):
        return f"{self.name} - {self.student_id}"

    class Meta:
        ordering = ['name']


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(verbose_name="Date")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name="Status")

    def __str__(self):
        return f"{self.student.name} - {self.subject.subject_name} - {self.date} - {self.status}"

    class Meta:
        ordering = ['-date', 'student__name']
        unique_together = ['student', 'subject', 'date']


class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='marks')
    internal_marks = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    assignment_marks = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    practical_marks = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    external_marks = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    total_marks = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(400)])
    grade = models.CharField(max_length=3, default='F')

    def calculate_total(self):
        total = self.internal_marks + self.assignment_marks + self.practical_marks + self.external_marks
        return total

    def calculate_grade(self):
        total = self.calculate_total()
        if total >= 90:
            return 'A+'
        elif total >= 80:
            return 'A'
        elif total >= 70:
            return 'B+'
        elif total >= 60:
            return 'B'
        elif total >= 50:
            return 'C'
        elif total >= 40:
            return 'D'
        else:
            return 'F'

    def save(self, *args, **kwargs):
        self.total_marks = self.calculate_total()
        self.grade = self.calculate_grade()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.name} - {self.subject.subject_name} - {self.total_marks} ({self.grade})"

    class Meta:
        ordering = ['student__name', 'subject__subject_name']
        unique_together = ['student', 'subject']
