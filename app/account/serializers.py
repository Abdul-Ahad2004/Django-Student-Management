from rest_framework import serializers
from django.contrib.auth import authenticate
from core.models import User


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user authentication token."""
    
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    
    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )
            
            if not user:
                msg = 'Unable to authenticate with provided credentials'
                raise serializers.ValidationError(msg, code='authorization')
            
            if not user.is_active:
                msg = 'User account is disabled'
                raise serializers.ValidationError(msg, code='authorization')
            
            attrs['user'] = user
            return attrs
        else:
            msg = 'Must include "email" and "password"'
            raise serializers.ValidationError(msg, code='authorization')
