# Student Performance & Attendance Analytics System

A complete beginner-friendly Django web application for managing students, subjects, attendance, and marks with basic academic analytics and data visualization. This project is designed for college academic use and is easy to understand and explain during a viva.

## Features

### 1. Student Management (CRUD)
- Add, view, edit, and delete students
- Search students by ID, name, email, or course
- View individual student details

### 2. Subject Management (CRUD)
- Manage subjects with ID, name, code, and semester

### 3. Attendance Management
- Record attendance for students per subject with date
- View, edit, and delete attendance records
- Calculate attendance percentage for each student
- Calculate subject-wise attendance
- Highlight students with attendance below 75%

### 4. Marks Management
- Add/edit marks for internal, assignment, practical, and external exams
- Automatic total calculation
- Automatic grade calculation (A+, A, B+, B, C, D, F)
- View marks with average calculations

### 5. Student Dashboard
- View personal information
- Overall attendance percentage
- Subject-wise attendance
- Subject-wise marks
- Average marks and grades
- Performance summary

### 6. Teacher/Admin Dashboard
- Overview statistics (total students, subjects, attendance, marks)
- Average class marks
- Students below 75% attendance
- Recent attendance and marks records

### 7. Data Analytics (Using Pandas & NumPy)
- Convert data to Pandas DataFrames
- Calculate mean, min, max, median, standard deviation of marks
- Attendance statistics
- Subject-wise average marks
- Student ranking based on average marks
- Identification of students with low attendance

### 8. Data Visualization (Using Matplotlib)
- Subject-wise average marks bar chart
- Student attendance percentage chart
- Subject-wise attendance chart
- Student performance chart (Top 10 students)

### 9. Authentication
- Django built-in authentication system
- Login/Logout functionality
- Role-based dashboards (Teacher/Admin and Student)

### 10. Sample Data
- Management command to seed 10-15 students, 5 subjects, attendance, and marks

## Technologies Used

- Python 3.x
- Django 4.2.7
- MySQL 8.0 / MariaDB
- HTML5, CSS3, Bootstrap 5 (CDN)
- Pandas 2.1.3
- NumPy 1.26.2
- Matplotlib 3.8.2
- Django ORM

## Project Structure

```
student_performance_system/
├── manage.py
├── student_performance_system/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── students/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── analytics.py
│   ├── charts.py
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py
│   ├── tests/
│   │   ├── __init__.py
│   │   └── tests_basic.py
│   ├── templates/
│   │   └── students/
│   └── static/
│       └── students/
├── analytics/ (if needed)
├── templates/
├── static/
├── media/
├── requirements.txt
├── README.md
├── .gitignore
└── .env.example
```

## Installation Instructions

1. Clone/download the project
2. Navigate to project directory:
   ```bash
   cd student_performance_system
   ```

3. Create and activate virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## MySQL Database Setup

1. Open MySQL command line or MySQL Workbench
2. Create the database:
   ```sql
   CREATE DATABASE student_performance_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. Create a MySQL user (optional but recommended):
   ```sql
   CREATE USER 'student_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON student_performance_db.* TO 'student_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

## Environment Variable Setup

1. Create a `.env` file in the project root (same level as manage.py):
   ```bash
   cp .env.example .env
   ```

2. Update the `.env` file with your MySQL credentials:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   DB_NAME=student_performance_db
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_HOST=localhost
   DB_PORT=3306
   ```

## Migration Commands

Run the following commands in order:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Creating a Superuser

Create a superuser for admin access:

```bash
python manage.py createsuperuser
```

Follow the prompts to set username, email, and password.

## Seeding Sample Data

Populate the database with sample data for demonstration:

```bash
python manage.py seed_data
```

This will create:
- 10-15 sample students
- 5 sample subjects
- Attendance records (20 classes per student-subject combination)
- Marks records
- A teacher admin account (username: teacher, password: teacher123)

## Running the Development Server

```bash
python manage.py runserver
```

Open your browser and navigate to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## How to Use the Application

### For Teacher/Admin
1. Go to http://127.0.0.1:8000/login/
2. Login with superuser credentials or teacher account (teacher/teacher123)
3. Access Teacher Dashboard - manage students, subjects, attendance, marks
4. View analytics and generate charts
5. Search students, view reports

### For Students
1. Register as a new student using the "Register as Student" link on the login page, or
2. Login with existing student credentials (e.g., st001/student123 after seeding)
3. Access Student Dashboard - view personal info, attendance, marks, grades
4. Monitor performance and attendance

## Default Credentials (After Seeding)

- **Teacher/Admin**: username `teacher`, password `teacher123`
- **Students**: username is student ID in lowercase (e.g., `st001`, `st002`...), password `student123`

## Running Tests

```bash
python manage.py test students
```

## Notes

- The project uses matplotlib with 'Agg' backend for non-interactive chart generation
- Charts are saved in the media directory
- All database operations use Django ORM (no raw SQL)
- The UI is responsive using Bootstrap 5
- This is a beginner-friendly project suitable for college viva demonstration

## CI/CD

This project uses GitHub Actions for continuous integration. The CI workflow automatically runs on every push and pull request to ensure code quality.

**CI checks include:**
- Setting up Python environment
- Installing dependencies
- Running Django system checks
- Running database migrations
- Running all tests

The CI uses SQLite for testing to avoid requiring a MySQL server in the CI environment.

## Screenshots

> *Screenshots can be added here to showcase the application interface - Home, Login, Student Registration, Teacher Dashboard, Student Dashboard, Analytics, and Charts.*

## User Stories & Project Management

See [docs/USER_STORIES.md](docs/USER_STORIES.md) for detailed user stories with acceptance criteria.

See [docs/KANBAN.md](docs/KANBAN.md) for the project Kanban board and task tracking.
