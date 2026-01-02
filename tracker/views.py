from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import CustomUser as User
from accounts.permissions import IsAdminOrDoctorUserRole, IsAdminUserRole

from .models import Patient, PatientInstance
from .serializers import (DoctorListSerializer, PatientCreateSerializer,
                          PatientInstanceStatusUpdateSerializer,
                          PatientListSerializer, PatientSearchSerializer)


class PatientCreateView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUserRole]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        # Use a transaction so create patient and instance are consistent
        with transaction.atomic():
            patient = serializer.save()

            # Safely create a PatientInstance linked to the patient
            try:
                PatientInstance.objects.create(
                    patient=patient,
                    procedure_name=request.data.get("procedure_name", "Initial Case"),
                    created_by=request.user if request.user and request.user.is_authenticated else None,
                )
            except Exception as e:
                # Log it but do not destroy the created patient
                # Use your logging system; printing for minimal change
                print(f"[WARN] Failed to create PatientInstance for patient {patient.id}: {e}")

        return Response({
            "message": "Patient created successfully",
            "patient": {
                "id": patient.id,
                "first_name": patient.first_name,
                "last_name": patient.last_name,
                "code": patient.code,
                "assigned_doctor_id": getattr(patient, "assigned_doctor_id", None)
            }
        }, status=status.HTTP_201_CREATED)
# views.py
# views.py


class UpdatePatientStatusView(generics.UpdateAPIView):
    serializer_class = PatientInstanceStatusUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrDoctorUserRole]

    def get_instance_for_patient(self, patient, user):
        """
        Return the appropriate PatientInstance for the patient.
        If none exists, create one **properly** (not orphaned).
        """
        instance = PatientInstance.objects.filter(patient=patient).order_by('-created_at').first()
        if instance:
            return instance

        # If none exists, create a new one (link to patient) — safe defaults
        # Make sure atomic to prevent partial writes
        with transaction.atomic():
            new_instance = PatientInstance.objects.create(
                patient=patient,
                procedure_name="Auto-generated case",
                created_by=user if user and user.is_authenticated else None,
            )
            return new_instance

    def get_object(self):
        patient_code = self.kwargs.get("patient_code")
        if not patient_code:
            raise NotFound("patient_code not provided in URL")

        patient = get_object_or_404(Patient, code__iexact=patient_code)

        # If the request user is a doctor, ensure they are allowed to update this case
        user = self.request.user
        if user.is_authenticated and getattr(user, "role", None) == "DOCTOR":
            # Are they assigned to any instance for this patient? check assignment
            assigned = PatientInstance.objects.filter(patient=patient, doctors=user).exists()
            if not assigned:
                # deny if doctor not assigned
                raise PermissionDenied("You are not assigned to this patient's case.")

        # Fetch or create a proper PatientInstance (always linked to patient)
        return self.get_instance_for_patient(patient, user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True, context={'request': request})

        if not serializer.is_valid():
            print("DEBUG VALIDATION ERRORS:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            self.perform_update(serializer)
        except Exception as e:
            print("DEBUG UPDATE ERROR:", str(e))
            raise e

        return Response({"message": "Status updated successfully"}, status=status.HTTP_200_OK)


class PatientListView(generics.ListAPIView):
    serializer_class = PatientListSerializer
    permission_classes = [IsAdminOrDoctorUserRole]

    def get_queryset(self):
        return Patient.objects.all()


class DoctorsListView(generics.ListAPIView):
    serializer_class = DoctorListSerializer
    permission_classes = [IsAdminOrDoctorUserRole]

    def get_queryset(self):
        return User.objects.filter(role="DOCTOR")

# patient search view


# views.py


class PatientSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        patient_code = request.query_params.get("patientNumber")
        if not patient_code:
            return Response({"detail": "patientNumber query parameter is required."}, status=400)

        # Case-insensitive search
        patient = get_object_or_404(Patient, code__iexact=patient_code)
        serializer = PatientSearchSerializer(patient)
        return Response(serializer.data)
