from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'enrollment'

router = DefaultRouter()
router.register(r'', views.EnrollmentViewSet, basename='enrollment')

urlpatterns = [
    path('', include(router.urls)),
]
