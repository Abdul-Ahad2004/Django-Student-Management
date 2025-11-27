from rest_framework import serializers
from core.models import Enrollment, StudentProfile, Course


class EnrollmentStudentSerializer(serializers.ModelSerializer):
    """Minimal student info for enrollments."""
    
    name = serializers.CharField(source='user.name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    roll_number = serializers.CharField(read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = ['name', 'email', 'roll_number']


class EnrollmentCourseSerializer(serializers.ModelSerializer):
    """Minimal course info for enrollments."""
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'schedule']


class EnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for Enrollment model."""
    
    student = EnrollmentStudentSerializer(read_only=True)
    course = EnrollmentCourseSerializer(read_only=True)
    student_id = serializers.UUIDField(write_only=True)
    course_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'course', 'student_id', 'course_id',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate enrollment data."""
        student_id = data.get('student_id')
        course_id = data.get('course_id')
        
        try:
            student = StudentProfile.objects.get(user_id=student_id)
            data['student'] = student
        except StudentProfile.DoesNotExist:
            raise serializers.ValidationError("Student not found")
        
        try:
            course = Course.objects.get(id=course_id)
            data['course'] = course
        except Course.DoesNotExist:
            raise serializers.ValidationError("Course not found")
        
        # Check for existing enrollment
        existing = Enrollment.objects.filter(
            student=student, 
            course=course,
            status='ACTIVE'
        ).exists()
        
        if existing:
            raise serializers.ValidationError(
                "Student is already enrolled in this course"
            )
        
        return data
    
    def create(self, validated_data):
        """Create enrollment."""
        student = validated_data.pop('student')
        course = validated_data.pop('course')
        validated_data.pop('student_id', None)
        validated_data.pop('course_id', None)
        
        enrollment = Enrollment.objects.create(
            student=student,
            course=course,
            **validated_data
        )
        return enrollment


class EnrollmentUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating enrollment status."""
    
    class Meta:
        model = Enrollment
        fields = ['status']
