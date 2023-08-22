from rest_framework import serializers
from .models import CustomUser, UserProfile
from drf_extra_fields.fields import Base64ImageField
from django.db import transaction

class UserProfileSerializer(serializers.ModelSerializer):
    profile_photo = Base64ImageField()
    user = serializers.CharField(source='user.email')
    
    @transaction.atomic
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.profile_photo = validated_data.get('profile_photo', instance.profile_photo)
        instance.user = validated_data.get('user', instance.user)
        instance.save()      
        return instance
    
    class Meta:
        model = UserProfile
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')

        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь с таким email уже существует.')

        user = CustomUser(
            email=email
        )
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email')
        
class VerificationCodeSerializer(serializers.Serializer):
    code = serializers.CharField()