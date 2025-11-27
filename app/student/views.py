from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import StudentProfile, Enrollment, TeacherProfile
from core.permissions import IsAdminUser, IsStudentOwnerOrTeacherOrAdmin, IsStudentUser
from .serializers import StudentProfileSerializer, StudentProfileUpdateSerializer, StudentEnrollmentsSerializer


class StudentProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for StudentProfile management."""
    
    queryset = StudentProfile.objects.all()
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action == 'list':
            # Admin can list all, teachers can see students in their courses, students see own
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['create', 'destroy']:
            # Only admin can create/delete student profiles
            permission_classes = [IsAdminUser]
        else:
            # Student can view/update own profile, teachers can view students in their courses, admin can access all
            permission_classes = [IsStudentOwnerOrTeacherOrAdmin]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        # Handle case when user is not authenticated (for schema generation)
        if not hasattr(self.request, 'user') or not self.request.user.is_authenticated:
            return StudentProfileSerializer
            
        if self.action in ['update', 'partial_update'] and self.request.user.role == 'STUDENT':
            return StudentProfileUpdateSerializer
        return StudentProfileSerializer
    
    def get_queryset(self):
        """Filter queryset based on user role."""
        # Handle case when user is not authenticated (for schema generation)
        if not hasattr(self.request, 'user') or not self.request.user.is_authenticated:
            return StudentProfile.objects.none()
            
        if self.request.user.role == 'ADMIN':
            return StudentProfile.objects.all()
        elif self.request.user.role == 'TEACHER':
            # Teachers can see students enrolled in their courses
            try:
                teacher_profile = TeacherProfile.objects.get(user=self.request.user)
                teacher_courses = teacher_profile.courses.all()
                enrolled_students = StudentProfile.objects.filter(
                    enrollments__course__in=teacher_courses,
                    enrollments__status='ACTIVE'
                ).distinct()
                return enrolled_students
            except TeacherProfile.DoesNotExist:
                return StudentProfile.objects.none()
        elif self.request.user.role == 'STUDENT':
            return StudentProfile.objects.filter(user=self.request.user)
        return StudentProfile.objects.none()
    
    @action(detail=True, methods=['get'], permission_classes=[IsStudentOwnerOrTeacherOrAdmin])
    def enrollments(self, request, pk=None):
        """Get student's enrollments."""
        student = self.get_object()
        enrollments = student.enrollments.all()
        serializer = StudentEnrollmentsSerializer(enrollments, many=True)
        return Response(serializer.data)
