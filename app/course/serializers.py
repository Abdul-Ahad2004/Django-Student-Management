from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from core.models import Course, TeacherProfile, Enrollment, StudentProfile


class CourseTeacherSerializer(serializers.ModelSerializer):
    """Minimal serializer for teacher info in courses."""
    
    name = serializers.CharField(source='user.name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = TeacherProfile
        fields = ['name', 'email']


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for Course model."""
    
    teacher = CourseTeacherSerializer(read_only=True)
    teacher_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    enrolled_students_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'duration_weeks', 
            'schedule', 'teacher', 'teacher_id', 'enrolled_students_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    @extend_schema_field(serializers.IntegerField)
    def get_enrolled_students_count(self, obj: Course) -> int:
        """Get count of active enrollments."""
        return obj.enrollments.filter(status='ACTIVE').count()
    
    def create(self, validated_data):
        teacher_id = validated_data.pop('teacher_id', None)
        course = Course.objects.create(**validated_data)
        
        if teacher_id:
            try:
                teacher = TeacherProfile.objects.get(user_id=teacher_id)
                course.teacher = teacher
                course.save()
            except TeacherProfile.DoesNotExist:
                pass
        
        return course
    
    def update(self, instance, validated_data):
        teacher_id = validated_data.pop('teacher_id', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if teacher_id is not None:
            if teacher_id:
                try:
                    teacher = TeacherProfile.objects.get(user_id=teacher_id)
                    instance.teacher = teacher
                except TeacherProfile.DoesNotExist:
                    pass
            else:
                instance.teacher = None
        
        instance.save()
        return instance


class CourseListSerializer(serializers.ModelSerializer):
    """Serializer for course list with minimal info."""
    
    teacher_name = serializers.CharField(source='teacher.user.name', read_only=True)
    enrolled_students_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'duration_weeks', 
            'schedule', 'teacher_name', 'enrolled_students_count'
        ]
    
    @extend_schema_field(serializers.IntegerField)
    def get_enrolled_students_count(self, obj: Course) -> int:
        """Get count of active enrollments."""
        return obj.enrollments.filter(status='ACTIVE').count()
