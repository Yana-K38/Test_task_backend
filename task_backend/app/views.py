from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser, UserProfile
from .serializers import CustomUserSerializer, UserProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    def perform_create(self, serializer):
        instance = serializer.save()
        UserProfile.objects.create(user=instance)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    http_method_names = ['get', 'post', 'put', 'delete',]