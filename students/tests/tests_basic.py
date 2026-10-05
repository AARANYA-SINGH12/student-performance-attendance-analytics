from django.test import TestCase
from django.contrib.auth.models import User
from students.models import Student, Subject, Attendance, Marks


class StudentModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            student_id='ST001',
            name='Test Student',
            email='test@example.com',
            phone='1234567890',
            course='B.Tech',
            semester=3,
            division='A'
        )

    def test_student_creation(self):
        self.assertEqual(self.student.name, 'Test Student')
        self.assertEqual(self.student.student_id, 'ST001')
        self.assertTrue(isinstance(self.student, Student))

    def test_student_update(self):
        self.student.name = 'Updated Student'
        self.student.save()
        self.assertEqual(self.student.name, 'Updated Student')


class AttendanceCalculationTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            student_id='ST001',
            name='Test Student',
            email='test@example.com',
            phone='1234567890',
            course='B.Tech',
            semester=3,
            division='A'
        )
        self.subject = Subject.objects.create(
            subject_id='SUB001',
            subject_name='Test Subject',
            subject_code='T101',
            semester=3
        )
        # Create attendance records
        Attendance.objects.create(student=self.student, subject=self.subject, date='2024-01-01', status='Present')
        Attendance.objects.create(student=self.student, subject=self.subject, date='2024-01-02', status='Present')
        Attendance.objects.create(student=self.student, subject=self.subject, date='2024-01-03', status='Absent')

    def test_attendance_percentage_calculation(self):
        total = Attendance.objects.filter(student=self.student).count()
        present = Attendance.objects.filter(student=self.student, status='Present').count()
        percentage = (present / total) * 100
        self.assertEqual(total, 3)
        self.assertEqual(present, 2)
        self.assertEqual(percentage, 66.66666666666666)


class MarksCalculationTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            student_id='ST001',
            name='Test Student',
            email='test@example.com',
            phone='1234567890',
            course='B.Tech',
            semester=3,
            division='A'
        )
        self.subject = Subject.objects.create(
            subject_id='SUB001',
            subject_name='Test Subject',
            subject_code='T101',
            semester=3
        )

    def test_total_marks_calculation(self):
        marks = Marks.objects.create(
            student=self.student,
            subject=self.subject,
            internal_marks=20,
            assignment_marks=10,
            practical_marks=15,
            external_marks=50
        )
        self.assertEqual(marks.total_marks, 95)

    def test_grade_calculation(self):
        marks = Marks.objects.create(
            student=self.student,
            subject=self.subject,
            internal_marks=25,
            assignment_marks=10,
            practical_marks=20,
            external_marks=45  # Total 100, A+
        )
        self.assertEqual(marks.grade, 'A+')
        marks2 = Marks.objects.create(
            student=Student.objects.create(
                student_id='ST002', name='S2', email='s2@test.com',
                phone='123', course='B.Tech', semester=3, division='A'
            ),
            subject=self.subject,
            internal_marks=10,
            assignment_marks=5,
            practical_marks=10,
            external_marks=10  # Total 35, F
        )
        self.assertEqual(marks2.grade, 'F')
