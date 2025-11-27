from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import AuthTokenSerializer
from user.serializers import UserSerializer
from rest_framework.generics import GenericAPIView


class LoginUserAPIView(GenericAPIView):
    """Login user and return JWT tokens."""
    serializer_class = AuthTokenSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'accessToken': str(refresh.access_token),
            'refreshToken': str(refresh),
        }, status=status.HTTP_200_OK)

