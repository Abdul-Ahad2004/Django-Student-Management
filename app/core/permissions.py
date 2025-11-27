from rest_framework import permissions
from rest_framework.permissions import BasePermission
from core.models import TeacherProfile, StudentProfile


class IsAdminUser(BasePermission):
    """Permission to only allow admin users to access."""
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'ADMIN'
        )


class IsTeacherUser(BasePermission):
    """Permission to only allow teacher users to access."""
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'TEACHER'
        )


class IsStudentUser(BasePermission):
    """Permission to only allow student users to access."""
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'STUDENT'
        )


class IsOwnerOrAdminUser(BasePermission):
    """Permission to allow owner or admin to access."""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
   
        if request.user.role == 'ADMIN':
            return True
        
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        if hasattr(obj, 'id') and hasattr(request.user, 'id'):
            return obj.id == request.user.id
        
        return False


class IsTeacherOwnerOrAdmin(BasePermission):
    """Permission for teacher to access their own data or admin to access all."""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        
        if request.user.role == 'ADMIN':
            return True
        
        if request.user.role == 'TEACHER':
            if hasattr(obj, 'user'):
                return obj.user == request.user
            return obj == request.user
        
        return False


class IsStudentOwnerOrTeacherOrAdmin(BasePermission):
    """Permission for student owner, their teachers, or admin to access."""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        
        if request.user.role == 'ADMIN':
            return True
        
        if request.user.role == 'STUDENT':
            if hasattr(obj, 'user'):
                return obj.user == request.user
            return obj == request.user
        
        if request.user.role == 'TEACHER':
            try:
                teacher_profile = TeacherProfile.objects.get(user=request.user)
                if hasattr(obj, 'user'):
                    # This is a StudentProfile
                    student_profile = obj
                else:
                    # This is a User with role STUDENT
                    student_profile = StudentProfile.objects.get(user=obj)
                
                teacher_courses = teacher_profile.courses.all()
                student_enrollments = student_profile.enrollments.filter(
                    course__in=teacher_courses,
                    status='ACTIVE'
                )
                return student_enrollments.exists()
            except (TeacherProfile.DoesNotExist, StudentProfile.DoesNotExist):
                return False
        
        return False


class CanManageCourse(BasePermission):
    """Permission for course management - Admin or assigned teacher."""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        
        if request.user.role == 'ADMIN':
            return True
        
        if request.user.role == 'TEACHER':
            try:
                teacher_profile = TeacherProfile.objects.get(user=request.user)
                return obj.teacher == teacher_profile
            except TeacherProfile.DoesNotExist:
                return False
        
        return False


class CanManageEnrollment(BasePermission):
    """Permission for enrollment management - Admin or teacher of the course."""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        
        if request.user.role == 'ADMIN':
            return True
        
        if request.user.role == 'TEACHER':
            try:
                teacher_profile = TeacherProfile.objects.get(user=request.user)
                return obj.course.teacher == teacher_profile
            except TeacherProfile.DoesNotExist:
                return False
            
        if request.user.role == 'STUDENT' and view.action == 'destroy':
            return obj.student.user == request.user
        
        return False


class CanViewEnrollment(BasePermission):
    """Permission to view enrollment - Student can view their own, Teacher their courses, Admin all."""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        
        if request.user.role == 'ADMIN':
            return True
        
        if request.user.role == 'STUDENT':
            return obj.student.user == request.user
        
        if request.user.role == 'TEACHER':
            try:
                teacher_profile = TeacherProfile.objects.get(user=request.user)
                return obj.course.teacher == teacher_profile
            except TeacherProfile.DoesNotExist:
                return False
        
        return False
