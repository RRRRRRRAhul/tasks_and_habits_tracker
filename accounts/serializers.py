from accounts.models import CustomUser
from rest_framework import serializers
from django.contrib.auth import authenticate
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email',)
        

class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password1', 'password2')

    def validate_email(self, value):
        # Proper email validation
        try:
            validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError("Enter a valid email address")

        # Gmail restriction (optional business rule)
        if not value.endswith("@gmail.com"):
            raise serializers.ValidationError("Please use a Gmail address")

        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")

        return value

    def validate_username(self, value):
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError(
                "Username can contain only letters, numbers, and underscores"
            )

        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters")

        if len(value) > 15:
            raise serializers.ValidationError("Username must be at most 15 characters")

        return value

    def validate(self, attrs):
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")

        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match")

        if len(password1) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")

        if not re.search(r"[a-z]", password1):
            raise serializers.ValidationError("Password must contain a lowercase letter")

        if not re.search(r"[A-Z]", password1):
            raise serializers.ValidationError("Password must contain an uppercase letter")

        if not re.search(r"[0-9]", password1):
            raise serializers.ValidationError("Password must contain a digit")

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password1")
        validated_data.pop("password2")

        return CustomUser.objects.create_user(
            password=password,
            **validated_data
        )

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only = True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect credentials')


