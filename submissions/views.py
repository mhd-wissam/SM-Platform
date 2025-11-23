from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import FormParser, MultiPartParser
from datetime import timedelta
import hashlib
import secrets
import random
import string

from .models import User, OtpCode, Category, Submission
from .serializers import (
    UserSerializer, CategorySerializer, SubmissionSerializer,
    SubmissionCreateSerializer, OTPSendSerializer, OTPVerifySerializer,
    JWTTokenSerializer
)
from .services import sms_service


# API Views

class CategoryListView(generics.ListAPIView):
    """List all categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class SubmissionListView(generics.ListCreateAPIView):
    """List and create submissions"""
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser]

    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubmissionCreateSerializer
        return SubmissionSerializer


class SubmissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, delete submission"""
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser]

    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user)


# Authentication Views

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@parser_classes([FormParser, MultiPartParser])
def send_otp(request):
    """Send OTP code to phone number"""
    serializer = OTPSendSerializer(data=request.data)
    if serializer.is_valid():
        phone_number = serializer.validated_data['phone_number']

        # Use fixed OTP code '000000' for development (6 digits)
        otp_code = '000000'

        # Hash the OTP code
        hashed_code = hashlib.sha256(otp_code.encode()).hexdigest()

        # Set expiration time (5 minutes from now)
        expires_at = timezone.now() + timedelta(minutes=5)

        # Create or update OTP record
        OtpCode.objects.update_or_create(
            phone_number=phone_number,
            defaults={
                'hashed_code': hashed_code,
                'expires_at': expires_at
            }
        )

        # Send OTP via SMS service
        sms_sent = sms_service.send_otp(phone_number, otp_code)

        if sms_sent:
            return Response({
                'message': 'تم إرسال كود OTP بنجاح',
                'otp_code': otp_code,  # Remove this line in production
                'expires_in': '5 دقائق'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'فشل في إرسال كود OTP، يرجى المحاولة مرة أخرى'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@parser_classes([FormParser, MultiPartParser])
def verify_otp(request):
    """Verify OTP code and return JWT tokens"""
    serializer = OTPVerifySerializer(data=request.data)
    if serializer.is_valid():
        phone_number = serializer.validated_data['phone_number']

        # Get or create user
        user, created = User.objects.get_or_create(
            phone_number=phone_number,
            defaults={}
        )

        # Delete used OTP
        serializer.validated_data['otp_obj'].delete()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            'message': 'تم التحقق من كود OTP بنجاح',
            'tokens': {
                'access': access_token,
                'refresh': str(refresh)
            },
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])
def refresh_token(request):
    """Refresh JWT access token"""
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({
                'error': 'Refresh token مطلوب'
            }, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)

        return Response({
            'access': access_token,
            'refresh': str(refresh)
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'error': 'Token غير صالح'
        }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    """Get current user profile"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)
