from rest_framework import viewsets
from .models import CustomUser, UserProfile
from .serializers import CustomUserSerializer, UserProfileSerializer

# from django.urls import reverse
# from django.shortcuts import redirect

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from .tasks import is_valid_verification_code


class VerifyCodeAPIView(APIView):
    pass
    # def post(self, request):
    #     serializer = VerificationCodeSerializer(data=request.data)
    #     if serializer.is_valid():
    #         entered_code = serializer.validated_data['code']
    #         if is_valid_verification_code(request.user.email, entered_code):
    #             profile_api_url = reverse('app/profiles/')
    #             return Response({'detail': 'Code verified'}, status=status.HTTP_200_OK, headers={'Location': profile_api_url})
    #         else:
    #             return Response({'error': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    


