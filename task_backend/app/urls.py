from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserProfileViewSet, VerifyCodeAPIView
from django.contrib.auth import views as auth_views


app_name='app'
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('verify-email/', VerifyCodeAPIView.as_view(), name='verify_email_api'),
]