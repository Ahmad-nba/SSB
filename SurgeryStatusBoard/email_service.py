# services.py
from django.core.mail import send_mail
from django.conf import settings
from .utils import generate_invite_token  # our signing util

def send_doctor_invite(email):
    token = generate_invite_token(email)
    invite_link = f"{settings.FRONTEND_URL}/onboard?token={token}"

    subject = "Doctor Onboarding Invitation"
    message = f"""
    Hello,

    You have been invited to onboard as a doctor.
    Please click the link below to complete your registration:

    {invite_link}

    This link will expire in 7 days.

    Regards,
    Your App Team
    """

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
