from django.core import signing
from django.conf import settings

# generate token when inviting


def generate_invite_token(email):
    return signing.dumps({"email": email}, salt="doctor-invite")

# verify token when onboarding


def verify_invite_token(token):
    try:
        data = signing.loads(token, salt="doctor-invite",
                             max_age=60*60*24*7)  # 7 days expiry
        return data["email"]
    except signing.BadSignature:
        return None
    except signing.SignatureExpired:
        return None
