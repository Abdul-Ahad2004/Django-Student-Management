# Django Student Management System

A comprehensive Django REST API-based student management system that allows administrators to manage students, teachers, courses, and enrollments with automated email notifications.

## 🚀 Features

### Core Features

- **User Management**: Admin, Teacher, and Student role-based access control
- **Course Management**: Create and manage courses with teacher assignments
- **Student Enrollment**: Enroll students in courses and track enrollment status
- **Teacher Profiles**: Manage teacher information with qualifications and experience
- **Student Profiles**: Track student information with roll numbers and batch details
- **Real-time Notifications**: Automated email notifications for various events

### Email Notification System

- **Enrollment Notifications**: Automatic emails when students enroll in courses
- **Removal Notifications**: Alerts when students are removed from courses
- **Course Assignment**: Notifications when teachers are assigned to courses
- **Account Creation**: Welcome emails for new users

### API Features

- RESTful API with JWT authentication
- Interactive Swagger documentation
- Role-based permissions
- Comprehensive CRUD operations
- Automated testing capabilities

## 🏗️ Architecture & Flow

### System Flow

```
1. Admin creates User accounts (Students/Teachers)
2. Teachers get assigned to Courses
3. Students get enrolled in Courses
4. Automated email notifications are sent for all actions
5. All activities are logged in the Notification system
```

### Application Architecture

```
├── Core App (Models & Utilities)
├── Account App (Authentication)
├── User App (User Management)
├── Teacher App (Teacher Profiles)
├── Student App (Student Profiles)
├── Course App (Course Management)
├── Enrollment App (Enrollment Management)
└── Notification App (Email Notifications)
```

## 🗄️ Database Models

### User Model

- **Fields**: id (UUID), email, name, role, is_active, is_staff, created_at, updated_at
- **Roles**: ADMIN, TEACHER, STUDENT
- **Authentication**: Email-based login with JWT tokens

### TeacherProfile Model

- **Fields**: user (OneToOne), phone, address, qualification, experience_years
- **Relationships**: One teacher can have multiple courses

### StudentProfile Model

- **Fields**: user (OneToOne), roll_number, batch, enrollment_year, phone, address
- **Relationships**: One student can have multiple enrollments

### Course Model

- **Fields**: id (UUID), title, description, duration_weeks, schedule, teacher, created_at, updated_at
- **Relationships**: Belongs to one teacher, has many enrollments

### Enrollment Model

- **Fields**: id (UUID), student, course, status (ACTIVE/DROPPED), created_at, updated_at
- **Relationships**: Links students to courses

### Notification Model

- **Fields**: id (UUID), receiver, message, type, sent_at
- **Types**: ENROLLMENT, REMOVAL, COURSE_ASSIGNMENT, ACCOUNT_CREATED

## 🔗 API Endpoints

### Authentication

- `POST /api/auth/login/` - User login with JWT token

### User Management

- `GET /api/users/` - List all users
- `POST /api/users/` - Create new user
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user
- `GET /api/users/profile/` - Get current user profile
- `POST /api/users/change-password/` - Change password

### Teacher Management

- `GET /api/teachers/` - List all teachers
- `POST /api/teachers/` - Create teacher profile
- `GET /api/teachers/{id}/` - Get teacher details
- `PUT /api/teachers/{id}/` - Update teacher profile
- `DELETE /api/teachers/{id}/` - Delete teacher profile

### Student Management

- `GET /api/students/` - List all students
- `POST /api/students/` - Create student profile
- `GET /api/students/{id}/` - Get student details
- `PUT /api/students/{id}/` - Update student profile
- `DELETE /api/students/{id}/` - Delete student profile

### Course Management

- `GET /api/courses/` - List all courses
- `POST /api/courses/` - Create new course
- `GET /api/courses/{id}/` - Get course details
- `PUT /api/courses/{id}/` - Update course
- `DELETE /api/courses/{id}/` - Delete course

### Enrollment Management

- `GET /api/enrollments/` - List all enrollments
- `POST /api/enrollments/` - Create new enrollment
- `GET /api/enrollments/{id}/` - Get enrollment details
- `PUT /api/enrollments/{id}/` - Update enrollment status
- `DELETE /api/enrollments/{id}/` - Delete enrollment

### Notifications

- `GET /api/notifications/` - List user notifications

### API Documentation

- `GET /api/docs/` - Interactive Swagger UI documentation
- `GET /api/schema/` - OpenAPI schema

## 📧 Email Flow

### Email Notification Triggers

1. **Student Enrollment** (`ENROLLMENT`)

   - **To Student**: Welcome message with course details
   - **To Teacher**: Notification of new student enrollment

2. **Student Removal** (`REMOVAL`)

   - **To Student**: Notification of course removal
   - **To Teacher**: Alert about student leaving course

3. **Course Assignment** (`COURSE_ASSIGNMENT`)

   - **To Teacher**: Notification when assigned to a new course

4. **Account Creation** (`ACCOUNT_CREATED`)
   - **To New User**: Welcome email with login credentials

### Email Service Configuration

- Uses Django's built-in email backend
- Supports SendGrid integration
- All notifications are logged in the database
- Configurable email templates

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.8+
- PostgreSQL database
- Git

### Environment Variables (.env)

Create a `.env` file in the app directory with the following variables:


### Installation Steps

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd Django-Student-Management
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   cd app
   pip install -r requirements.txt
   ```

4. **Setup database**

   ```bash
   # Create PostgreSQL database
   createdb your_database_name

   # Run migrations
   python manage.py migrate
   ```

5. **Create superuser**

   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**

   ```bash
   # Method 1: Using the provided script (Recommended)
   ./start_server.sh

   # Method 2: Manual start
   python manage.py runserver 0.0.0.0:8001
   ```

### Running the Project

**Option 1: Using the start script (Recommended)**

```bash
cd app
chmod +x start_server.sh
./start_server.sh
```

This script will:

- Check database connectivity
- Wait for database to be ready (with 60-second timeout)
- Start the development server on port 8001

**Option 2: Manual startup**

```bash
cd app
python manage.py migrate
python manage.py runserver 0.0.0.0:8001
```

### Accessing the Application

- **API Base URL**: `http://localhost:8001/api/`
- **Swagger Documentation**: `http://localhost:8001/api/docs/`
- **Django Admin**: `http://localhost:8001/admin/`

## 🧪 Testing

Run the test suite:

```bash
python manage.py test
```

## 📦 Dependencies

- **Django** (4.2+): Web framework
- **Django REST Framework**: API development
- **PostgreSQL** (psycopg2-binary): Database
- **JWT Authentication**: djangorestframework-simplejwt
- **API Documentation**: drf-spectacular
- **Email Service**: SendGrid
- **Environment Variables**: python-dotenv

## 🔒 Security Features

- JWT-based authentication
- Role-based access control
- Password hashing
- CSRF protection
- SQL injection prevention
- XSS protection


## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 📞 Support

For support and questions:

- Create an issue in the repository
- Check the API documentation at `/api/docs/`
- Review the Django admin interface at `/admin/`
