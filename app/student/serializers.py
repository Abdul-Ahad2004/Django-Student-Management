from rest_framework import serializers
from core.models import StudentProfile, Enrollment
from user.serializers import UserProfileSerializer


class StudentProfileSerializer(serializers.ModelSerializer):
    """Serializer for StudentProfile model."""
    
    user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = ['user', 'roll_number', 'batch', 'enrollment_year', 'phone', 'address']


class StudentProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating student profile - limited fields."""
    
    class Meta:
        model = StudentProfile
        fields = ['phone', 'address']


class StudentEnrollmentsSerializer(serializers.ModelSerializer):
    """Serializer for student's enrollments."""
    
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_description = serializers.CharField(source='course.description', read_only=True)
    course_schedule = serializers.CharField(source='course.schedule', read_only=True)
    teacher_name = serializers.CharField(source='course.teacher.user.name', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = [
            'id', 'course_title', 'course_description', 'course_schedule',
            'teacher_name', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
