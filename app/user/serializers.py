from rest_framework import serializers
from core.models import User, TeacherProfile, StudentProfile

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    password = serializers.CharField(write_only=True, min_length=5)
    roll_number = serializers.CharField(write_only=True, required=False, allow_blank=True)
    batch = serializers.CharField(write_only=True, required=False, allow_blank=True)
    enrollment_year = serializers.IntegerField(write_only=True, required=False)
    student_phone = serializers.CharField(write_only=True, required=False, allow_blank=True)
    student_address = serializers.CharField(write_only=True, required=False, allow_blank=True) 
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'role', 'password', 'created_at', 'updated_at','roll_number', 'batch', 'enrollment_year', 'student_phone', 'student_address']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Create a new user with encrypted password."""
        password = validated_data.pop('password')
        roll_number = validated_data.pop('roll_number', None)
        batch = validated_data.pop('batch', None)
        enrollment_year = validated_data.pop('enrollment_year', None)
        student_phone = validated_data.pop('student_phone', None)
        student_address = validated_data.pop('student_address', None)

        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        if user.role == 'TEACHER':
            TeacherProfile.objects.create(user=user)
        elif user.role == 'STUDENT':
            StudentProfile.objects.create(
                user=user,
                roll_number=roll_number or '',
                batch=batch or '',
                enrollment_year=enrollment_year or 0,
                phone=student_phone or '',
                address=student_address or ''
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