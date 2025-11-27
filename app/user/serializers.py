from rest_framework import serializers
from core.models import User, TeacherProfile, StudentProfile

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    password = serializers.CharField(write_only=True, min_length=5)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'role', 'password', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Create a new user with encrypted password."""
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        # Create profile based on role
        if user.role == 'TEACHER':
            TeacherProfile.objects.create(user=user)
        elif user.role == 'STUDENT':
            StudentProfile.objects.create(
                user=user,
                roll_number=f'STU{user.id.hex[:8].upper()}',  # Generate a roll number
                batch='2024',  # Default batch, can be customized
                enrollment_year=2024  # Default enrollment year
            )
        
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for viewing/updating user profile with limited fields."""
    
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'role', 'created_at', 'updated_at']
        read_only_fields = ['id', 'email', 'role', 'created_at', 'updated_at']


class StudentProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for students to update their own profile."""
    
    class Meta:
        model = User
        fields = ['name']


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password."""
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=5)