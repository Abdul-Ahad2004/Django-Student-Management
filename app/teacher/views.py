from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import TeacherProfile, Course, Enrollment, StudentProfile
from core.permissions import IsAdminUser, IsTeacherOwnerOrAdmin, IsTeacherUser
from .serializers import TeacherProfileSerializer, TeacherProfileUpdateSerializer, TeacherCoursesSerializer
from student.serializers import StudentProfileSerializer
from enrollment.serializers import EnrollmentSerializer


class TeacherProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for TeacherProfile management."""
    
    queryset = TeacherProfile.objects.all()
    
    def create(self, request, *args, **kwargs):
        """Disable POST requests for teacher profile creation."""
        return Response(
            {"detail": "Teacher profiles are created automatically when users are created with TEACHER role."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['create', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsTeacherOwnerOrAdmin]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if not hasattr(self.request, 'user') or not self.request.user.is_authenticated:
            return TeacherProfileSerializer
            
        if self.action in ['update', 'partial_update'] and self.request.user.role == 'TEACHER':
            return TeacherProfileUpdateSerializer
        return TeacherProfileSerializer
    
    def get_queryset(self):
        """Filter queryset based on user role."""
        if not hasattr(self.request, 'user') or not self.request.user.is_authenticated:
            return TeacherProfile.objects.none()
            
        if self.request.user.role == 'ADMIN':
            return TeacherProfile.objects.all()
        elif self.request.user.role == 'TEACHER':
            return TeacherProfile.objects.filter(user=self.request.user)
        return TeacherProfile.objects.none()
    
    @action(detail=True, methods=['get'], permission_classes=[IsTeacherOwnerOrAdmin])
    def courses(self, request, pk=None):
        """Get courses assigned to this teacher."""
        teacher = self.get_object()
        courses = teacher.courses.all()
        serializer = TeacherCoursesSerializer(courses, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], permission_classes=[IsTeacherOwnerOrAdmin])
    def students(self, request, pk=None):
        """Get students enrolled in teacher's courses."""
        teacher = self.get_object()
        courses = teacher.courses.all()
        enrollments = Enrollment.objects.filter(course__in=courses, status='ACTIVE')
        students = StudentProfile.objects.filter(enrollments__in=enrollments).distinct()
        serializer = StudentProfileSerializer(students, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], permission_classes=[IsTeacherOwnerOrAdmin])
    def enrollments(self, request, pk=None):
        """Get all enrollments for teacher's courses."""
        teacher = self.get_object()
        courses = teacher.courses.all()
        enrollments = Enrollment.objects.filter(course__in=courses)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
