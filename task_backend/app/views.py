from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .models import CustomUser, UserProfile
from .serializers import CustomUserSerializer, UserProfileSerializer
from rest_framework.views import APIView
from .tasks import send_otp_email, OTPManager
from social_django.models import UserSocialAuth
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action

class OTPSendView(APIView):
    def post(self, request, format=None):
        email = request.data.get('email')
        if email:
            otp = OTPManager.generate_and_store_otp(email)
            send_otp_email(email)
            return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)


class OTPVerifyView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        email = request.data.get('email')
        otp = request.data.get('otp')
        
        if email and otp and OTPManager.validate_otp(email, otp):
            try:
                social_user = UserSocialAuth.objects.get(provider='provider_name', uid=email)
                user = social_user.user
            except UserSocialAuth.DoesNotExist:
                # Если социальный аккаунт не найден, создайте пользователя
                user, created = CustomUser.objects.get_or_create(email=email)
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        UserProfile.objects.get_or_create(user=user, defaults={'email': user.email})


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    http_method_names = ['get', 'put', 'delete']


    def list(self, request, pk=None):
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        profile = UserProfile.objects.get(user=self.request.user)
        serializer.save(user=self.request.user)
    


