from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework import serializers

from accounts.models import CustomUser as User
from tracker.models import Patient, PatientInstance


# -----------------------------------
# CREATE SERIALIZER
# -----------------------------------
class PatientCreateSerializer(serializers.ModelSerializer):
    doctor_id = serializers.IntegerField(write_only=True, required=False)
    patientNumber = serializers.CharField(
        source="patient_number", required=False
    )

    class Meta:
        model = Patient
        fields = [
            "first_name",
            "last_name",
            "date_of_birth",
            "district",
            "email",
            "address",
            "age",
            "nationality",
            "contact",
            "patientNumber",
            "doctor_id",
        ]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "email": {"required": True},
        }

    def create(self, validated_data):
        doctor_id = validated_data.pop("doctor_id", None)

        # Generate unique patient code
        code = get_random_string(length=6).upper()
        while Patient.objects.filter(code=code).exists():
            code = get_random_string(length=6).upper()
        validated_data["code"] = code

        # Assign creator
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["created_by"] = request.user

        # Create patient
        patient = Patient.objects.create(**validated_data)

        # Assign doctor if provided 
        # we have removed this asignment cause our model supports assigning a doctor to a patient instance not a patient
        # if doctor_id:
        #     patient.assigned_doctor_id = doctor_id
        #     patient.save()

        return patient


# -----------------------------------
# LIST SERIALIZER
# -----------------------------------
class PatientListSerializer(serializers.ModelSerializer):
    patientNumber = serializers.CharField(source="patient_number")
    firstName = serializers.CharField(source="first_name")
    lastName = serializers.CharField(source="last_name")
    contactEmail = serializers.EmailField(source="email")
    phoneNumber = serializers.CharField(source="contact", allow_blank=True)
    streetAddress = serializers.CharField(source="address", allow_blank=True)
    city = serializers.CharField(source="district", allow_blank=True)
    country = serializers.CharField(source="nationality", allow_blank=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            "patientNumber",
            "firstName",
            "lastName",
            "streetAddress",
            "city",
            "country",
            "phoneNumber",
            "contactEmail",
            "status",
        ]

    def get_status(self, obj):
        latest_case = obj.cases.order_by("-created_at").first()
        return latest_case.current_status if latest_case else "N/A"


# -----------------------------------
# UPDATE STATUS SERIALIZER
# -----------------------------------
class PatientInstanceStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientInstance
        fields = ["current_status", "notes"]

    def update(self, instance, validated_data):
        request = self.context.get("request")
        user = request.user if request else None

        instance.current_status = validated_data.get(
            "current_status", instance.current_status
        )

        note = validated_data.get("notes")
        if note:
            instance.notes = note

        history = instance.status_history or []
        history.append(
            {
                "status": instance.current_status,
                "by": user.id if user else None,
                "timestamp": timezone.now().isoformat(),
            }
        )
        instance.status_history = history
        instance.save()

        return instance


# -----------------------------------
# DOCTOR LIST SERIALIZER
# -----------------------------------
class DoctorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "username", "role")
        read_only_fields = fields


# -----------------------------------
# PATIENT SEARCH SERIALIZER
# -----------------------------------
class PatientSearchSerializer(serializers.ModelSerializer):
    current_status = serializers.SerializerMethodField()
    procedure_name = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            "code",
            "first_name",
            "last_name",
            "email",
            "contact",
            "address",
            "district",
            "age",
            "nationality",
            "current_status",
            "procedure_name",
            "notes",
        ]

    def _latest_instance(self, obj):
        return obj.cases.last()

    def get_current_status(self, obj):
        instance = self._latest_instance(obj)
        return instance.current_status if instance else None

    def get_procedure_name(self, obj):
        instance = self._latest_instance(obj)
        return instance.procedure_name if instance else None

    def get_notes(self, obj):
        instance = self._latest_instance(obj)
        return instance.notes if instance else None
