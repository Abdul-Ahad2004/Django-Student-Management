from rest_framework import serializers
from core.models import Notification
from user.serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model."""
    
    receiver = UserSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'receiver', 'message', 'type', 'sent_at']
        read_only_fields = ['id', 'sent_at']
