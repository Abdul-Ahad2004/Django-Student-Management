from rest_framework import serializers
from core.models import TeacherProfile, Course
from user.serializers import UserProfileSerializer


class TeacherProfileSerializer(serializers.ModelSerializer):
    """Serializer for TeacherProfile model with nested user updates."""
    
    user = UserProfileSerializer()
    
    class Meta:
        model = TeacherProfile
        fields = ['user', 'phone', 'address', 'qualification', 'experience_years']
        
    def update(self, instance, validated_data):
        """Custom update method to handle nested user data."""
        user_data = validated_data.pop('user', None)
        
        # Update TeacherProfile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update nested User fields if provided
        if user_data:
            user_serializer = UserProfileSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
        
        return instance


class TeacherCoursesSerializer(serializers.ModelSerializer):
    """Serializer for courses assigned to teacher."""
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'duration_weeks', 'schedule', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
