from rest_framework import status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from core.models import User
from core.permissions import IsAdminUser, IsOwnerOrAdminUser, IsStudentUser
from .serializers import (
    UserSerializer, 
    UserProfileSerializer, 
    StudentProfileUpdateSerializer,
    ChangePasswordSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User management - Admin only for creation."""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action in ['create']:
            permission_classes = [IsAdminUser]
        elif self.action in ['list']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsOwnerOrAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action and user role."""
        if self.action == 'create':
            return UserSerializer
        return UserProfileSerializer
    
    def get_queryset(self):
        """Filter queryset based on user role."""
        if self.request.user.role == 'ADMIN':
            return User.objects.all()
        else:
            # Non-admin users can only access their own profile
            return User.objects.filter(id=self.request.user.id)


class ProfileAPIView(APIView):
    """API for user profile management."""
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer 
    
    def get(self, request):
        """Get current user profile."""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        """Update user profile ."""
        serializer = UserProfileSerializer(
                request.user, data=request.data, partial=True
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(APIView):
    """API for changing password."""
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer 
    
    def post(self, request):
        """Change user password."""
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {'error': 'Invalid old password'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response(
                {'message': 'Password changed successfully'}, 
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)