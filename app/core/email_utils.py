from django.core.mail import send_mail
from django.conf import settings
from core.models import Notification


class EmailNotificationService:
    """
    Utility class for sending email notifications and storing notification records.
    """
    
    @staticmethod
    def send_email_notification(receiver, subject, message, notification_type, context=None):
        """
        Send email notification and store notification record.
        """
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[receiver.email],
                fail_silently=False,
            )
            
            # Store notification record
            Notification.objects.create(
                receiver=receiver,
                message=message,
                type=notification_type
            )
            
            return True
            
        except Exception as e:
            print(f"Failed to send email notification to {receiver.email}: {str(e)}") 
            return False
    
    @staticmethod
    def send_enrollment_notification(student, course, teacher):
        """
        Send notification when student is enrolled in a course.
        """
       
        student_subject = f"Enrolled in Course: {course.title}"
        student_message = f"Dear {student.user.name}, you have been successfully enrolled in the course '{course.title}'. The course is taught by {teacher.user.name}. Course Duration: {course.duration_weeks} weeks. Schedule: {course.schedule}"
        
        EmailNotificationService.send_email_notification(
            receiver=student.user,
            subject=student_subject,
            message=student_message,
            notification_type='ENROLLMENT'
        )
        
        teacher_subject = f"New Student Enrolled: {course.title}"
        teacher_message = f"Dear {teacher.user.name}, a new student '{student.user.name}' (Roll No: {student.roll_number}) has been enrolled in your course '{course.title}'."
        
        EmailNotificationService.send_email_notification(
            receiver=teacher.user,
            subject=teacher_subject,
            message=teacher_message,
            notification_type='ENROLLMENT'
        )
    
    @staticmethod
    def send_removal_notification(student, course, teacher):
        """
        Send notification when student is removed from a course.
        """
        
        student_subject = f"Removed from Course: {course.title}"
        student_message = f"Dear {student.user.name}, you have been removed from the course '{course.title}'. If you have any questions, please contact the administration."
        
        EmailNotificationService.send_email_notification(
            receiver=student.user,
            subject=student_subject,
            message=student_message,
            notification_type='REMOVAL'
        )
        
        teacher_subject = f"Student Removed: {course.title}"
        teacher_message = f"Dear {teacher.user.name}, student '{student.user.name}' (Roll No: {student.roll_number}) has been removed from your course '{course.title}'."
        
        EmailNotificationService.send_email_notification(
            receiver=teacher.user,
            subject=teacher_subject,
            message=teacher_message,
            notification_type='REMOVAL'
        )
    
    @staticmethod
    def send_course_assignment_notification(teacher, course):
        """
        Send notification when teacher is assigned to a course.
        """
        subject = f"Course Assignment: {course.title}"
        message = f"Dear {teacher.user.name}, you have been assigned to teach the course '{course.title}'. Course Description: {course.description}. Duration: {course.duration_weeks} weeks. Schedule: {course.schedule}"
        
        EmailNotificationService.send_email_notification(
            receiver=teacher.user,
            subject=subject,
            message=message,
            notification_type='COURSE_ASSIGNMENT'
        )
    
    @staticmethod
    def send_account_created_notification(user, password=None):
        """
        Send notification when user account is created.
        """
        subject = f"Welcome to Student Management System - Account Created"
        
        if password:
            message = f"Dear {user.name}, your account has been created successfully. Your login credentials are:\nEmail: {user.email}\nPassword: {password}\nRole: {user.get_role_display()}\n\nPlease login and change your password for security."
        else:
            message = f"Dear {user.name}, your account has been created successfully. Your login email is: {user.email}. Role: {user.get_role_display()}. Please contact the administrator for your password."
        
        EmailNotificationService.send_email_notification(
            receiver=user,
            subject=subject,
            message=message,
            notification_type='ACCOUNT_CREATED'
        )
