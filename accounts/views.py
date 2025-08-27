from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.conf import settings
from .permissions import IsAdminUserRole
from .models import CustomUser
from .serializers import UserOnboardSerializer, UserLoginSerializer, InviteDoctorSerializer
from SurgeryStatusBoard.email_service import send_doctor_invite


# class InviteDoctorView(APIView):
#     permission_classes = [IsAdminUserRole]

#     def post(self, request):
#         serializer = InviteDoctorSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             token_generator = PasswordResetTokenGenerator()
#             # Create token (not saved in DB, stateless)
#             token = token_generator.make_token(user=CustomUser(email=email))

#             # Compose invite URL
#             invite_link = f"{settings.FRONTEND_URL}/onboard/doctor/?token={token}&email={email}"

#             # Send email (using Django's send_mail or configured email backend)
#             send_mail(
#                 subject="You're invited to join Surgery Status Board",
#                 message=f"Hello! Please complete your onboarding by visiting: {invite_link}",
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 recipient_list=[email],
#                 fail_silently=False,
#             )

#             return Response({"detail": "Invite sent successfully."}, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

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
