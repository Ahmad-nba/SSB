from django.core.validators import validate_email
from .models import CustomUser
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate


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
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials.")
        else:
            raise serializers.ValidationError("Both email and password are required.")

        attrs['user'] = user
        return attrs

class InviteDoctorSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        # Optional: check if a doctor with this email already exists
        if CustomUser.objects.filter(email=value, role=CustomUser.DOCTOR).exists():
            raise serializers.ValidationError("A doctor with this email already exists.")
        return value

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id, email, username, is_active, is_staff')
        read_only_fields = ('id, is_active, is_staff')
