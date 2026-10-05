# User Stories - Student Performance & Attendance Analytics System

## Teacher User Stories

### US-01: Add Students
**As a** Teacher/Admin  
**I want to** add new students to the system  
**So that** I can manage student records

**Acceptance Criteria:**
- Given I am logged in as Teacher/Admin, when I click "Add Student" and fill required fields with valid data, then student is created
- Given invalid data (missing required fields, invalid email), when submitting, then appropriate validation errors are shown
- Given duplicate Student ID or email, when submitting, then error is shown

### US-02: Manage Students (CRUD)
**As a** Teacher/Admin  
**I want to** view, edit, and delete student records  
**So that** student information stays up to date

**Acceptance Criteria:**
- I can view all students in a list with search functionality
- I can view individual student details
- I can edit student information and save changes
- I can delete a student with confirmation

### US-03: Manage Subjects
**As a** Teacher/Admin  
**I want to** add, view, edit, and delete subjects  
**So that** I can organize academic subjects

**Acceptance Criteria:**
- CRUD operations work for subjects
- Subject fields (ID, name, code, semester) are validated

### US-04: Record Attendance
**As a** Teacher/Admin  
**I want to** record student attendance for subjects on specific dates  
**So that** attendance can be tracked

**Acceptance Criteria:**
- I can mark Present/Absent for students per subject and date
- Attendance percentage is calculated automatically
- Students below 75% attendance are highlighted
- I can edit/delete attendance records

### US-05: Manage Marks
**As a** Teacher/Admin  
**I want to** enter student marks for different assessment types  
**So that** grades can be calculated

**Acceptance Criteria:**
- Can enter Internal, Assignment, Practical, External marks
- Total marks are calculated automatically
- Grade is calculated automatically using defined grading scale (A+, A, B+, B, C, D, F)
- I can edit/delete marks

### US-06: Teacher Dashboard
**As a** Teacher/Admin  
**I want to** see an overview of system statistics  
**So that** I can monitor class performance

**Acceptance Criteria:**
- Dashboard shows total students, subjects, attendance records, marks records
- Shows average class marks
- Shows students below 75% attendance
- Shows recent attendance and marks records

### US-07: Data Analytics
**As a** Teacher/Admin  
**I want to** view academic analytics  
**So that** I can analyze student performance

**Acceptance Criteria:**
- Can view attendance statistics (total, present, absent, rate)
- Can view marks statistics (mean, min, max, median, std dev)
- Can view subject-wise averages
- Can view student rankings by average marks
- Can identify students with low attendance

### US-08: Data Visualization
**As a** Teacher/Admin  
**I want to** view charts of academic data  
**So that** trends are easy to understand

**Acceptance Criteria:**
- Subject-wise average marks bar chart is generated
- Student attendance percentage chart is generated
- Subject-wise attendance chart is generated
- Student performance chart (top 10) is generated
- Charts are dynamically generated from database data

## Student User Stories

### US-09: Student Registration
**As a** New Student  
**I want to** create my own student account  
**So that** I can access my academic information

**Acceptance Criteria:**
- Registration form with all required fields (Name, Student ID, Email, Phone, Course, Semester, Division, Password, Confirm Password)
- Validation: all required fields must be filled
- Validation: Student ID must be unique
- Validation: Email must be unique and valid format
- Validation: Password and Confirm Password must match
- On successful registration, student profile is created and linked to user
- After registration, user is logged in and redirected to Student Dashboard
- Newly registered users have only Student permissions (cannot access Teacher/Admin features)

### US-10: Student Login
**As a** Student  
**I want to** log into the system securely  
**So that** I can view my dashboard

**Acceptance Criteria:**
- Login with valid credentials
- Redirect to Student Dashboard on success
- Cannot access Teacher/Admin features
- Logout functionality works

### US-11: Student Dashboard
**As a** Student  
**I want to** view my academic information  
**So that** I can track my performance

**Acceptance Criteria:**
- View personal information (ID, name, email, phone, course, semester, division)
- View overall attendance percentage
- View subject-wise attendance with status indicators
- View subject-wise marks (all components, total, grade)
- View average marks
- View performance summary

## System User Stories

### US-12: Authentication & Authorization
**As a** System  
**I want to** enforce role-based access control  
**So that** data is secure and users only access appropriate features

**Acceptance Criteria:**
- Teacher/Admin users (staff/superuser) access Teacher features only
- Student users access Student features only
- Unauthenticated users are redirected to login
- Passwords are securely hashed using Django's auth system

### US-13: Sample Data
**As a** System  
**I want to** provide sample data for demonstration  
**So that** the application can be tested/demonstrated easily

**Acceptance Criteria:**
- Management command `seed_data` creates sample data
- Creates 10-15 sample students with linked user accounts
- Creates 5 sample subjects
- Creates attendance records
- Creates marks records
- Creates teacher/admin account

### US-14: Data Validation & Error Handling
**As a** System  
**I want to** validate data and show appropriate messages  
**So that** data integrity is maintained

**Acceptance Criteria:**
- Required field validation
- Valid email format validation
- Marks within valid ranges
- Attendance status restricted to Present/Absent
- Duplicate prevention where appropriate
- Success/error messages displayed via Django messages
