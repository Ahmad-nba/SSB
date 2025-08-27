from django.db import models
from accounts.models import CustomUser as User


class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    district = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=254)
    address = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField()
    nationality = models.CharField(max_length=50)
    contact = models.CharField(max_length=15, blank=True)
    code = models.CharField(max_length=6, unique=True)  # 6-char ID
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'ADMIN'},  # only Admins
        related_name="patients"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.code})"


class PatientInstance(models.Model):
    STATUS_CHOICES = [
        ("Scheduled", "Scheduled"),
        ("Checked In", "Checked In"),
        ("Pre-Procedure", "Pre-Procedure"),
        ("In-Progress", "In-Progress"),
        ("Recovery", "Recovery"),
        ("Discharged", "Discharged"),
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

    # Optional: store logs/history of status changes
    # e.g., [{"status": "Checked In", "by": 2, "timestamp": "2025-08-24T20:00:00"}]
    status_history = models.JSONField(default=list, blank=True)

    notes = models.TextField(blank=True)  # optional surgical notes

    def __str__(self):
        return f"{self.procedure_name} for {self.patient.first_name} ({self.patient.code})"

    def add_status_update(self, status, user_id):
        """Helper to update status and append to history"""
        self.current_status = status
        self.status_history.append({
            "status": status,
            "by": user_id,
            "timestamp": str(models.DateTimeField.auto_now_add)
        })
        self.save()
