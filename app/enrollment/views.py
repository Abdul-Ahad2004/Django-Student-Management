from datetime import timedelta
from time import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from core.models import Enrollment, TeacherProfile, StudentProfile
from core.permissions import IsAdminUser, CanManageEnrollment, CanViewEnrollment
from .serializers import EnrollmentSerializer, EnrollmentUpdateSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Enrollment management."""
    
    queryset = Enrollment.objects.all()
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action in ['create', 'destroy', 'update', 'partial_update']:
            permission_classes = [CanManageEnrollment]
        elif self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        else:
            # For retrieve, use view permission
            permission_classes = [CanViewEnrollment]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action in ['update', 'partial_update']:
            return EnrollmentUpdateSerializer
        return EnrollmentSerializer
    
    def get_queryset(self):
        """Filter queryset based on user role."""
        if self.request.user.role == 'ADMIN':
            return Enrollment.objects.all()
        elif self.request.user.role == 'TEACHER':
            try:
                teacher_profile = TeacherProfile.objects.get(user=self.request.user)
                # Teacher can see enrollments for their courses
                return Enrollment.objects.filter(course__teacher=teacher_profile)
            except TeacherProfile.DoesNotExist:
                return Enrollment.objects.none()
        elif self.request.user.role == 'STUDENT':
            try:
                student_profile = StudentProfile.objects.get(user=self.request.user)
                # Student can see their own enrollments
                return Enrollment.objects.filter(student=student_profile)
            except StudentProfile.DoesNotExist:
                return Enrollment.objects.none()
        return Enrollment.objects.none()
    
    def create(self, request, *args, **kwargs):
        """Create enrollment with role-based restrictions."""
        if request.user.role == 'ADMIN':
            pass
        elif request.user.role == 'TEACHER':
            try:
                teacher_profile = TeacherProfile.objects.get(user=request.user)
                course_id = request.data.get('course_id')
                
                if not teacher_profile.courses.filter(id=course_id).exists():
                    return Response(
                        {'error': 'You can only enroll students in your assigned courses'}, 
                        status=status.HTTP_403_FORBIDDEN
                    )
            except TeacherProfile.DoesNotExist:
                return Response(
                    {'error': 'Teacher profile not found'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            return Response(
                {'error': 'Students cannot create enrollments'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().create(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Delete enrollment with role-based restrictions."""
        enrollment = self.get_object()
        
        if request.user.role == 'STUDENT' and enrollment.created_at < timezone.now() - timedelta(days=7):
                return Response(
                    {'error': 'You can only drop course within 7 days of enrollment'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        if enrollment.status != 'ACTIVE':
            return Response(
                    {'error': 'Only active enrollments can be dropped'}, 
                    status=status.HTTP_400_BAD_REQUEST
            )

        enrollment.status = 'DROPPED'
        enrollment.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
