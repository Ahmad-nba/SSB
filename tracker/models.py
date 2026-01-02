from django.db import models

from accounts.models import CustomUser as User


class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    district = models.CharField(max_length=100)
    # removed unique=True unless you truly need it
    email = models.EmailField(max_length=254, unique=True)
    address = models.CharField(max_length=255)
    age = models.PositiveSmallIntegerField(default=0)
    nationality = models.CharField(max_length=50, default="Unknown")
    contact = models.CharField(max_length=15, blank=True)
    patient_number = models.CharField(
        max_length=20, blank=True, null=True)  # removed null=True
    code = models.CharField(max_length=6, unique=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'ADMIN'},
        related_name="patients",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.patient_number})"


class PatientInstance(models.Model):
    STATUS_CHOICES = [
        ("Scheduled", "Scheduled"),
        ("Checked In", "Checked In"),
        ("Pre-Procedure", "Pre-Procedure"),
        ("In-Progress", "In-Progress"),
        ("Closing", "Closing"),
        ("Recovery", "Recovery"),
        ("Complete", "Complete"),
        ("Dismissal", "Dismissal"),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="cases"
    )
    procedure_name = models.CharField(max_length=100)
    current_status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="Scheduled")
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'ADMIN'},
        related_name="created_cases"
    )
    doctors = models.ManyToManyField(
        User,
        limit_choices_to={'role__in': ['DOCTOR', 'ADMIN']},
        related_name="assigned_cases",
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status_history = models.JSONField(default=list, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.procedure_name} for {self.patient.first_name} ({self.patient.code})"

    def add_status_update(self, status, user_id):
        self.current_status = status
        self.status_history.append({
            "status": status,
            "by": user_id,
            "timestamp": str(models.DateTimeField.auto_now_add)
        })
        self.save()
