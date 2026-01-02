from django.core import signing

# generate token when inviting


def generate_invite_token(email):
    return signing.dumps({"email": email}, salt="doctor-invite")


# verify token when onboarding


def verify_invite_token(token):
    try:
        data = signing.loads(
            token,
            salt="doctor-invite",
            max_age=60 * 60 * 24 * 7,
        )
        return data["email"]
    except signing.SignatureExpired:
        return None  # or "expired"
    except signing.BadSignature:
        return None  # or "invalid"
