from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import StudentProfile, Enrollment, TeacherProfile
from core.permissions import IsAdminUser, IsStudentOwnerOrTeacherOrAdmin, IsStudentUser
from .serializers import StudentProfileSerializer, StudentEnrollmentsSerializer


class StudentProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for StudentProfile management."""
    serializer_class= StudentProfileSerializer
    queryset = StudentProfile.objects.all()
    
    def create(self, request, *args, **kwargs):
        """Disable POST requests for student profile creation."""
        return Response(
            {"detail": "Student profiles are created automatically when users are created with STUDENT role."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['create', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsStudentOwnerOrTeacherOrAdmin]
        return [permission() for permission in permission_classes]
    
    
    def get_queryset(self):
        """Filter queryset based on user role."""
        if not hasattr(self.request, 'user') or not self.request.user.is_authenticated:
            return StudentProfile.objects.none()
            
        if self.request.user.role == 'ADMIN':
            return StudentProfile.objects.all()
        elif self.request.user.role == 'TEACHER':
            return StudentProfile.objects.all()
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