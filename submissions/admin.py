from django.contrib import admin
from .models import Category, Submission, User, OtpCode


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Category model"""
    list_display = ['category_id', 'name_ar', 'name_en']
    search_fields = ['name_ar', 'name_en']
    list_filter = ['name_ar']
    ordering = ['category_id']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    """Admin interface for Submission model"""
    list_display = ['submission_id', 'user', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['user__phone_number', 'notes']
    readonly_fields = ['submission_id', 'created_at']
    date_hierarchy = 'created_at'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin interface for User model"""
    list_display = ['user_id', 'phone_number', 'created_at']
    search_fields = ['phone_number']
    readonly_fields = ['user_id', 'created_at']
    date_hierarchy = 'created_at'


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    """Admin interface for OtpCode model"""
    list_display = ['id', 'phone_number', 'expires_at']
    search_fields = ['phone_number']
    list_filter = ['expires_at']
    readonly_fields = ['id']
