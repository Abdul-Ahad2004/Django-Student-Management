from django.contrib import admin
from .models import (
    User, TeacherProfile, StudentProfile, 
    Course, Enrollment, Notification
)

admin.site.register(User)
admin.site.register(TeacherProfile)
admin.site.register(StudentProfile)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Notification)
