from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from students.models import Student


class StudentRegistrationTest(TestCase):
    def test_successful_registration(self):
        response = self.client.post(reverse('student_register'), {
            'full_name': 'John Doe',
            'student_id': 'ST1001',
            'email': 'john.doe@example.com',
            'phone': '9876543210',
            'course': 'B.Tech CS',
            'semester': 3,
            'division': 'A',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
        })
        self.assertTrue(User.objects.filter(username='st1001').exists())
        self.assertTrue(Student.objects.filter(student_id='ST1001').exists())
        self.assertEqual(response.status_code, 302)

    def test_duplicate_student_id(self):
        Student.objects.create(
            student_id='ST2001',
            name='Existing',
            email='existing@example.com',
            phone='1234567890',
            course='B.Tech',
            semester=3,
            division='A'
        )
        response = self.client.post(reverse('student_register'), {
            'full_name': 'New User',
            'student_id': 'ST2001',
            'email': 'new@example.com',
            'phone': '9876543211',
            'course': 'B.Tech CS',
            'semester': 3,
            'division': 'B',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Student ID already exists')

    def test_duplicate_email(self):
        Student.objects.create(
            student_id='ST3001',
            name='Existing',
            email='dup@example.com',
            phone='1234567890',
            course='B.Tech',
            semester=3,
            division='A'
        )
        response = self.client.post(reverse('student_register'), {
            'full_name': 'New User',
            'student_id': 'ST3002',
            'email': 'dup@example.com',
            'phone': '9876543211',
            'course': 'B.Tech CS',
            'semester': 3,
            'division': 'B',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email already registered')

    def test_password_mismatch(self):
        response = self.client.post(reverse('student_register'), {
            'full_name': 'Test User',
            'student_id': 'ST4001',
            'email': 'test4@example.com',
            'phone': '9876543210',
            'course': 'B.Tech',
            'semester': 3,
            'division': 'A',
            'password': 'pass123',
            'confirm_password': 'pass456',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Passwords do not match')
