from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = 'submissions'

urlpatterns = [
    # Authentication endpoints
    path('auth/send-otp/', views.send_otp, name='send_otp'),
    path('auth/verify-otp/', views.verify_otp, name='verify_otp'),
    path('auth/refresh-token/', views.refresh_token, name='refresh_token'),
    path('auth/profile/', views.user_profile, name='user_profile'),

    # API endpoints
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('submissions/', views.SubmissionListView.as_view(), name='submission_list'),
    path('submissions/<int:pk>/', views.SubmissionDetailView.as_view(), name='submission_detail'),
]
