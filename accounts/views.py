from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from SurgeryStatusBoard.email_service import send_doctor_invite

from .models import CustomUser
from .permissions import IsAdminUserRole
from .serializers import (CustomUserSerializer, InviteDoctorSerializer,
                          UserLoginSerializer, UserOnboardSerializer)


class InviteDoctorView(generics.GenericAPIView):
    serializer_class = InviteDoctorSerializer
    permission_classes = [IsAdminUserRole]  # only admins can invite

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        send_doctor_invite(email)

        return Response({"message": f"Invite sent to {email}"}, status=status.HTTP_200_OK)



class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        # Validate the serializer
        serializer.is_valid(raise_exception=True)
        # signal the pylance or linter that validated_data is not None and is a dictionary at runtime
        assert serializer.validated_data is not None
        assert isinstance(serializer.validated_data, dict)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'email': user.email,
                'username': user.username,
                'role': user.role
            }
        }, status=status.HTTP_200_OK)

class OnboardView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserOnboardSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "User created successfully",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                },
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            },
            status=status.HTTP_201_CREATED
        )


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()  # requires Blacklist app enabled
            return Response({"message": "Logged out successfully"}, status=200)
        except Exception:
            return Response({"error": "Invalid token"}, status=400)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response({"user": serializer.data}, status=200)
