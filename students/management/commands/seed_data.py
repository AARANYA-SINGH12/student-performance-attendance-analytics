from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from students.models import Student, Subject, Attendance, Marks
import random
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Seed database with sample data for demonstration'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')
        
        # Create subjects
        subjects_data = [
            ('S001', 'Data Structures', 'CS301', 3),
            ('S002', 'Database Management Systems', 'CS302', 3),
            ('S003', 'Operating Systems', 'CS303', 3),
            ('S004', 'Computer Networks', 'CS304', 3),
            ('S005', 'Python Programming', 'CS305', 3),
        ]
        subjects = []
        for sid, sname, scode, sem in subjects_data:
            subject, created = Subject.objects.get_or_create(
                subject_id=sid,
                defaults={'subject_name': sname, 'subject_code': scode, 'semester': sem}
            )
            subjects.append(subject)
        
        # Create students
        students_data = [
            ('ST001', 'Rahul Sharma', 'rahul@example.com', '9876543210', 'B.Tech CS', 3, 'A'),
            ('ST002', 'Priya Patel', 'priya@example.com', '9876543211', 'B.Tech CS', 3, 'A'),
            ('ST003', 'Amit Singh', 'amit@example.com', '9876543212', 'B.Tech CS', 3, 'A'),
            ('ST004', 'Neha Gupta', 'neha@example.com', '9876543213', 'B.Tech CS', 3, 'A'),
            ('ST005', 'Raj Kumar', 'raj@example.com', '9876543214', 'B.Tech CS', 3, 'A'),
            ('ST006', 'Anjali Verma', 'anjali@example.com', '9876543215', 'B.Tech CS', 3, 'A'),
            ('ST007', 'Vikram Joshi', 'vikram@example.com', '9876543216', 'B.Tech CS', 3, 'A'),
            ('ST008', 'Sneha Reddy', 'sneha@example.com', '9876543217', 'B.Tech CS', 3, 'A'),
            ('ST009', 'Karan Mehta', 'karan@example.com', '9876543218', 'B.Tech CS', 3, 'A'),
            ('ST010', 'Pooja Desai', 'pooja@example.com', '9876543219', 'B.Tech CS', 3, 'A'),
        ]
        students = []
        for stid, name, email, phone, course, sem, div in students_data:
            student, created = Student.objects.get_or_create(
                student_id=stid,
                defaults={
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'course': course,
                    'semester': sem,
                    'division': div
                }
            )
            students.append(student)
            # Link to user if not exists
            if not student.user:
                username = stid.lower()
                user, ucreated = User.objects.get_or_create(username=username)
                if ucreated:
                    user.set_password('student123')
                    user.first_name = name.split()[0]
                    user.last_name = name.split()[-1] if len(name.split()) > 1 else ''
                    user.email = email
                    user.save()
                student.user = user
                student.save()
        
        # Create attendance records (last 30 days)
        for student in students:
            for subject in subjects:
                for i in range(20):  # 20 classes per subject
                    attendance_date = date.today() - timedelta(days=random.randint(1, 30))
                    status = random.choice(['Present', 'Present', 'Present', 'Present', 'Absent'])
                    Attendance.objects.get_or_create(
                        student=student,
                        subject=subject,
                        date=attendance_date,
                        defaults={'status': status}
                    )
        
        # Create marks
        for student in students:
            for subject in subjects:
                internal = random.uniform(15, 25)  # out of 25 approx
                assignment = random.uniform(5, 10)
                practical = random.uniform(10, 20)
                external = random.uniform(30, 70)
                Marks.objects.get_or_create(
                    student=student,
                    subject=subject,
                    defaults={
                        'internal_marks': round(internal, 1),
                        'assignment_marks': round(assignment, 1),
                        'practical_marks': round(practical, 1),
                        'external_marks': round(external, 1),
                    }
                )
        
        # Create teacher user
        teacher, tcreated = User.objects.get_or_create(username='teacher')
        if tcreated:
            teacher.set_password('teacher123')
            teacher.is_staff = True
            teacher.is_superuser = True
            teacher.first_name = 'Teacher'
            teacher.last_name = 'Admin'
            teacher.email = 'teacher@example.com'
            teacher.save()
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
