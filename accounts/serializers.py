from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import CustomUser


class UserOnboardSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=True,
        validators=[validate_password],
        write_only=True
    )
    passwordConfirm = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = ("email", "username", "password", "passwordConfirm")
        read_only_fields = ("email",)

    def validate(self, attrs):
        if attrs["password"] != attrs["passwordConfirm"]:
            raise serializers.ValidationError(
                {"password": "Passwords do not match"}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("passwordConfirm")
        user = CustomUser(
            email=validated_data["email"],   # injected by view
            username=validated_data["username"],
            role=CustomUser.DOCTOR           # enforce role
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")

        request = self.context.get("request")

        # Key fix: authenticate using email (since USERNAME_FIELD = 'email')
        user = authenticate(request=request, email=email, password=password)

        # Fallback (some setups still expect username kwarg)
        if user is None:
            user = authenticate(request=request, username=email, password=password)

        if user is None:
            raise serializers.ValidationError({"detail": "Invalid credentials."})

        attrs["user"] = user
        return attrs

class InviteDoctorSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        # Optional: check if a doctor with this email already exists
        if CustomUser.objects.filter(email=value, role=CustomUser.DOCTOR).exists():
            raise serializers.ValidationError(
                "A doctor with this email already exists.")
        return value


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'role', 'is_active')
        read_only_fields = ('id', 'is_active')
