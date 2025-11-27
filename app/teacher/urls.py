from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'teacher'

router = DefaultRouter()
router.register(r'', views.TeacherProfileViewSet, basename='teacher')

urlpatterns = [
    path('', include(router.urls)),
]
