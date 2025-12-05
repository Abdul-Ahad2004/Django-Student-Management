from rest_framework import serializers,status
from rest_framework.response import Response
from core.models import User, TeacherProfile, StudentProfile
from core.email_utils import EmailNotificationService

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
            if StudentProfile.objects.filter(roll_number=roll_number).exists():
                User.objects.filter(id=user.id).delete()  # Clean up created user
                raise serializers.ValidationError({"error": "Student with this roll number already exists."})
            StudentProfile.objects.create(
                user=user,
                roll_number=roll_number or '',
                batch=batch or '',
                enrollment_year=enrollment_year or 0,
                phone=student_phone or '',
                address=student_address or ''
            )
        try:    
            EmailNotificationService.send_account_created_notification(
                user=user,
                password=password
            )
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send account creation notification for user {user.email}: {str(e)}")

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for viewing/updating user profile with limited fields."""
    
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'role', 'created_at', 'updated_at']
        read_only_fields = ['id', 'email', 'role', 'created_at', 'updated_at']



class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password."""
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=5)