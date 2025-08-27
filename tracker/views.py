from accounts.permissions import IsAdminUserRole,IsAdminOrDoctorUserRole
from accounts.models import CustomUser as User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import PatientCreateSerializer,PatientInstanceStatusUpdateSerializer, DoctorListSerializer
from .models import Patient,PatientInstance
from rest_framework.permissions import IsAuthenticated


class PatientCreateView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUserRole]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        patient = serializer.save()
        return Response({
            "message": "Patient created successfully",
            "patient": {
                "id": patient.id,
                "first_name": patient.first_name,
                "last_name": patient.last_name,
                "code": patient.code,
                "assigned_doctor_id": request.data.get('doctor_id')
            }
        }, status=status.HTTP_201_CREATED)

class UpdatePatientStatusView(generics.UpdateAPIView):
    queryset = PatientInstance.objects.all()
    serializer_class = PatientInstanceStatusUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrDoctorUserRole]  # custom permission class

    def get_queryset(self):
        user = self.request.user
        # Doctors only update assigned cases
        if user.role == 'DOCTOR':
            return self.queryset.filter(doctors=user)
        return self.queryset

class DoctorsListView(generics.ListAPIView):
    serializer_class = DoctorListSerializer
    permission_classes = [IsAdminOrDoctorUserRole]

    def get_queryset(self):
        return User.objects.filter(role="DOCTOR")