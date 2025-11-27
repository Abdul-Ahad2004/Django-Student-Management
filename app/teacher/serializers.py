from rest_framework import serializers
from core.models import TeacherProfile, Course
from user.serializers import UserProfileSerializer


class TeacherProfileSerializer(serializers.ModelSerializer):
    """Serializer for TeacherProfile model."""
    
    user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = TeacherProfile
        fields = ['user', 'phone', 'address', 'qualification', 'experience_years']


class TeacherProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating teacher profile - excludes user and non-editable fields."""
    
    class Meta:
        model = TeacherProfile
        fields = ['phone', 'address', 'qualification', 'experience_years']


class TeacherCoursesSerializer(serializers.ModelSerializer):
    """Serializer for courses assigned to teacher."""
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'duration_weeks', 'schedule', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
