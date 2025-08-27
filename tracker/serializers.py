from rest_framework import serializers
from django.utils.crypto import get_random_string
from accounts.models import CustomUser as User
from tracker.models import Patient, PatientInstance
from django.utils import timezone


class PatientCreateSerializer(serializers.ModelSerializer):
    doctor_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'district',
            'email', 'address', 'age', 'nationality', 'contact', 'doctor_id'
        ]

    def validate_doctor_id(self, value):
        """Ensure the doctor exists and has the correct role"""
        try:
            doctor = User.objects.get(id=value)
            if doctor.role not in [User.DOCTOR, User.ADMIN]:
                raise serializers.ValidationError(
                    "Assigned user is not a doctor/admin.")
        except:
            raise serializers.ValidationError(
                "Doctor with this ID does not exist.")
        return value

    def create(self, validated_data):
        # Extract doctor_id for internal use, remove from validated data
        doctor_id = validated_data.pop('doctor_id')

        # Generate unique 6-character code
        code = get_random_string(length=6).upper()
        while Patient.objects.filter(code=code).exists():
            code = get_random_string(length=6).upper()
        validated_data['code'] = code

        # Assign the admin creating this patient
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user

        # Create patient object
        patient = Patient.objects.create(**validated_data)

        # Optionally, you can create the first PatientInstance here and assign doctor
        # patient_instance = PatientInstance.objects.create(
        #     patient=patient,
        #     procedure_name="Initial Case",
        #     created_by=request.user
        # )
        # patient_instance.doctors.add(doctor_id)

        return patient


class PatientInstanceStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientInstance
        fields = ['current_status', 'notes']

    def update(self, instance, validated_data):
        user = self.context['request'].user
        instance.current_status = validated_data.get(
            'current_status', instance.current_status)
        note = validated_data.get('notes', "")
        if note:
            instance.notes = note

        # Append to status_history
        instance.status_history.append({
            "status": instance.current_status,
            "by": user.id,
            "timestamp": timezone.now().isoformat()
        })
        instance.save()
        return instance

class DoctorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','username', 'role')
        read_only_fields = ('id','email','username', 'role')
