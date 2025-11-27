import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class UserManager(BaseUserManager):
    """Custom user manager where email is the unique identifier."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password."""
        user=self.create_user(email, password, **extra_fields)
        user.is_staff=True
        user.is_superuser=True
        user.role='ADMIN'
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model with email as username field."""
    
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('TEACHER', 'Teacher'),
        ('STUDENT', 'Student'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'role']
    
    def __str__(self):
        return f"Name: {self.name}, Email: {self.email}, Role: {self.role}"


class TeacherProfile(models.Model):
    """Profile for teachers with additional information."""
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        primary_key=True,
        limit_choices_to={'role': 'TEACHER'}
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    qualification = models.CharField(max_length=255, blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"Teacher: {self.user.name}"


class StudentProfile(models.Model):
    """Profile for students with additional information."""
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        primary_key=True,
        limit_choices_to={'role': 'STUDENT'}
    )
    roll_number = models.CharField(max_length=50, unique=True)
    batch = models.CharField(max_length=50)
    enrollment_year = models.PositiveIntegerField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Student: {self.user.name} ({self.roll_number})"


class Course(models.Model):
    """Course model for managing educational courses."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration_weeks = models.PositiveIntegerField()
    schedule = models.CharField(max_length=500)
    teacher = models.ForeignKey(
        TeacherProfile, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='courses'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


class Enrollment(models.Model):
    """Enrollment model for student-course relationships."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('DROPPED', 'Dropped'),
    )
    student = models.ForeignKey(
        StudentProfile, 
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.user.name} - {self.course.title} ({self.status})"


class Notification(models.Model):
    """Notification model for storing email notification logs."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    TYPE_CHOICES = (
        ('ENROLLMENT', 'Enrollment'),
        ('REMOVAL', 'Removal'),
        ('COURSE_ASSIGNMENT', 'Course Assignment'),
        ('ACCOUNT_CREATED', 'Account Created'),
    )
    
    receiver = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.TextField()
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    sent_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.type} notification for {self.receiver.name}"
