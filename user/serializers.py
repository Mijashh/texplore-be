from .models import CustomUser, CustomUserManager
from rest_framework import serializers

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email',"password", 'is_active', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'is_active': {'read_only': True},
            'is_staff': {'read_only': True},
            'is_superuser': {'read_only': True},
        }
    
    def create(self, validated_data):
        email = validated_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists')
        return CustomUser.objects.create_user(**validated_data)