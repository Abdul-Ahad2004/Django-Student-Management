from rest_framework import serializers
from core.models import StudentProfile, Enrollment
from user.serializers import UserProfileSerializer


class StudentProfileSerializer(serializers.ModelSerializer):
    """Serializer for StudentProfile model with nested user updates."""
    
    user = UserProfileSerializer() 
    
    class Meta:
        model = StudentProfile
        fields = ['user', 'roll_number', 'batch', 'enrollment_year', 'phone', 'address']
        read_only_fields = ['roll_number', 'batch', 'enrollment_year']
        
    def update(self, instance, validated_data):
        """Custom update method to handle nested user data."""
        user_data = validated_data.pop('user', None)
        
        # Update StudentProfile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update nested User fields if provided
        if user_data:
            user_serializer = UserProfileSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
        
        return instance
    
class StudentProfileUpdateSerializer(StudentProfileSerializer):
    """Serializer for StudentProfile model  for Admin pto update non-editable fields."""  
    
    class Meta():
       model = StudentProfile
       fields = ['user', 'roll_number', 'batch', 'enrollment_year', 'phone', 'address']
       read_only_fields = []
        


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
