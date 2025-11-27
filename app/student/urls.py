from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'student'

router = DefaultRouter()
router.register(r'', views.StudentProfileViewSet, basename='student')

urlpatterns = [
    path('', include(router.urls)),
]
