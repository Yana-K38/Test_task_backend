from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserProfileViewSet
from django.contrib.auth import views as auth_views
from app.views import OTPSendView, OTPVerifyView

app_name='app'
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('profiles/', UserProfileViewSet.as_view({'get': 'retrieve'}), name='profiles'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('send-otp/', OTPSendView.as_view(), name='send-otp'),
    path('verify-otp/', OTPVerifyView.as_view(), name='verify-otp'),
]