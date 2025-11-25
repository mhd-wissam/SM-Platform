from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
import hashlib
import secrets

from .models import User, OtpCode, Category, Submission


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['user_id', 'phone_number', 'created_at']
        read_only_fields = ['user_id', 'created_at']


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    class Meta:
        model = Category
        fields = ['category_id', 'name_ar', 'name_en']


class SubmissionSerializer(serializers.ModelSerializer):
    """Serializer for Submission model"""
    user = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    image_url = serializers.SerializerMethodField()
    invoice_image = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = [
            'submission_id', 'user', 'category', 'image_url',
            'notes', 'latitude', 'longitude', 'counter_number',
            'consumption_number', 'invoice_image', 'created_at'
        ]
        read_only_fields = ['submission_id', 'created_at']

    def get_image_url(self, obj):
        """Return relative path for image_url"""
        if obj.image_url:
            return obj.image_url.url
        return None

    def get_invoice_image(self, obj):
        """Return relative path for invoice_image"""
        if obj.invoice_image:
            return obj.invoice_image.url
        return None


class SubmissionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new submissions"""
    category_id = serializers.IntegerField(write_only=True)
    created_at = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Submission
        fields = [
            'category_id', 'image_url', 'notes', 'latitude', 'longitude',
            'counter_number', 'consumption_number', 'invoice_image', 'created_at'
        ]

    def validate_created_at(self, value):
        """Validate that created_at is not in the future and not too old"""
        if value:
            from django.utils import timezone
            now = timezone.now()
            
            # لا يمكن أن يكون الوقت في المستقبل
            if value > now:
                raise serializers.ValidationError("تاريخ الإنشاء لا يمكن أن يكون في المستقبل")
            
            # لا يمكن أن يكون أقدم من 30 يوم (لحماية من الأخطاء)
            from datetime import timedelta
            thirty_days_ago = now - timedelta(days=30)
            if value < thirty_days_ago:
                raise serializers.ValidationError("تاريخ الإنشاء لا يمكن أن يكون أقدم من 30 يوم")
        
        return value

    def create(self, validated_data):
        from django.utils import timezone
        
        category_id = validated_data.pop('category_id')
        user = self.context['request'].user
        category = Category.objects.get(category_id=category_id)
        
        # إذا لم يتم إرسال created_at، استخدم الوقت الحالي
        created_at = validated_data.pop('created_at', None)
        if not created_at:
            created_at = timezone.now()
        
        return Submission.objects.create(
            user=user, 
            category=category, 
            created_at=created_at,
            **validated_data
        )


# Authentication Serializers

class OTPSendSerializer(serializers.Serializer):
    """Serializer for sending OTP"""
    phone_number = serializers.CharField(max_length=20)

    def validate_phone_number(self, value):
        """Validate phone number format"""
        if not value.startswith('+'):
            raise serializers.ValidationError("رقم الهاتف يجب أن يبدأ بـ +")
        if len(value) < 10:
            raise serializers.ValidationError("رقم الهاتف قصير جداً")
        return value


class OTPVerifySerializer(serializers.Serializer):
    """Serializer for OTP verification"""
    phone_number = serializers.CharField(max_length=20)
    otp_code = serializers.CharField(max_length=6, min_length=6)

    def validate(self, data):
        phone_number = data.get('phone_number')
        otp_code = data.get('otp_code')

        try:
            # Hash the provided OTP code
            hashed_code = hashlib.sha256(otp_code.encode()).hexdigest()

            # Find valid OTP code
            otp_obj = OtpCode.objects.filter(
                phone_number=phone_number,
                hashed_code=hashed_code,
                expires_at__gt=timezone.now()
            ).first()

            if not otp_obj:
                raise serializers.ValidationError("كود OTP غير صحيح أو منتهي الصلاحية")

            data['otp_obj'] = otp_obj
            return data

        except OtpCode.DoesNotExist:
            raise serializers.ValidationError("كود OTP غير صحيح")


class JWTTokenSerializer(serializers.Serializer):
    """Serializer for JWT token response"""
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()
