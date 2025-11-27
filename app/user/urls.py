from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'user'

router = DefaultRouter()
router.register(r'', views.UserViewSet, basename='user')

urlpatterns = [
    path('profile/', views.ProfileAPIView.as_view(), name='profile'),
    path('change-password/', views.ChangePasswordAPIView.as_view(), name='change-password'),
    path('', include(router.urls)),
]