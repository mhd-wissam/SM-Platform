from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from rest_framework import exceptions
from .models import User


class CustomJWTAuthentication(JWTAuthentication):
    """Custom JWT authentication that uses submissions.User model"""

    def get_user(self, validated_token):
        """Get user from validated token"""
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
            user = User.objects.get(user_id=user_id)
            return user
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found', code='user_not_found')
