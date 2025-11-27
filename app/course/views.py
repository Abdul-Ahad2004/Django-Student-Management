from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import Course, TeacherProfile, StudentProfile, Enrollment
from core.permissions import IsAdminUser, CanManageCourse
from .serializers import CourseSerializer, CourseListSerializer
from student.serializers import StudentProfileSerializer
from enrollment.serializers import EnrollmentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet for Course management."""
    
    queryset = Course.objects.all()
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        elif self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return CourseListSerializer
        return CourseSerializer
    
    def get_queryset(self):
        """Filter queryset based on user role."""
        if self.request.user.role == 'ADMIN':
            return Course.objects.all()
        elif self.request.user.role == 'TEACHER':
            try:
                teacher_profile = TeacherProfile.objects.get(user=self.request.user)
                return teacher_profile.courses.all()
            except TeacherProfile.DoesNotExist:
                return Course.objects.none()
        elif self.request.user.role == 'STUDENT':
            try:
                student_profile = StudentProfile.objects.get(user=self.request.user)
                enrolled_courses = Course.objects.filter(
                    enrollments__student=student_profile,
                    enrollments__status='ACTIVE'
                )
                return enrolled_courses
            except StudentProfile.DoesNotExist:
                return Course.objects.none()
        return Course.objects.none()
    
    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def students(self, request, pk=None):
        """Get students enrolled in this course."""
        course = self.get_object()
        
        if request.user.role == 'ADMIN':
            pass  
        elif request.user.role == 'TEACHER':
            try:
                teacher_profile = TeacherProfile.objects.get(user=request.user)
                if course.teacher != teacher_profile:
                    return Response(
                        {'error': 'You can only view students for your assigned courses'}, 
                        status=403
                    )
            except TeacherProfile.DoesNotExist:
                return Response({'error': 'Teacher profile not found'}, status=403)
        else:
            return Response({'error': 'Permission denied'}, status=403)
        
        enrollments = Enrollment.objects.filter(course=course, status='ACTIVE')
        students = StudentProfile.objects.filter(enrollments__in=enrollments).distinct()
        serializer = StudentProfileSerializer(students, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def enrollments(self, request, pk=None):
        """Get all enrollments for this course."""
        course = self.get_object()
        
        if request.user.role == 'ADMIN':
            pass  
        elif request.user.role == 'TEACHER':
            try:
                teacher_profile = TeacherProfile.objects.get(user=request.user)
                if course.teacher != teacher_profile:
                    return Response(
                        {'error': 'You can only view enrollments for your assigned courses'}, 
                        status=403
                    )
            except TeacherProfile.DoesNotExist:
                return Response({'error': 'Teacher profile not found'}, status=403)
        else:
            return Response({'error': 'Permission denied'}, status=403)
        
        enrollments = Enrollment.objects.filter(course=course)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
