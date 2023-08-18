from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserProfileViewSet
from django.contrib.auth import views as auth_views

app_name='app'
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', UserProfileViewSet.as_view({'get': 'retrieve'}), name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

