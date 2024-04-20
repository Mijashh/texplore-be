from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    contact_no = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise ValidationError("User with this Email already exists")
        return value

    def validate_contact_no(self, value):
        if len(value) > 10:
            raise serializers.ValidationError(
                "Contact number must not be more than 10 characters long"
            )
        return value

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "name",
            "contact_no",
            "email",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
        ]
        extra_kwargs = {
            "is_active": {"read_only": True},
            "is_staff": {"read_only": True},
            "is_superuser": {"read_only": True},
        }
