# accounts/management/commands/bootstrap_admin.py

import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction

class Command(BaseCommand):
    help = "Create an initial superuser if it doesn't exist (idempotent)."

    def handle(self, *args, **options):
        User = get_user_model()

        email = os.getenv("ADMIN_EMAIL")
        password = os.getenv("ADMIN_PASSWORD")
        username = os.getenv("ADMIN_USERNAME", "admin")
        role = os.getenv("ADMIN_ROLE", "ADMIN")

        if not email or not password:
            self.stderr.write("Missing ADMIN_EMAIL or ADMIN_PASSWORD env vars.")
            return

        try:
            with transaction.atomic():
                # Fast path: if already exists, do nothing
                if User.objects.filter(email=email).exists():
                    self.stdout.write(f"Superuser already exists: {email}")
                    return

                # Your manager signature: create_superuser(email, password, username, **extra_fields)
                User.objects.create_superuser(
                    email=email,
                    password=password,
                    username=username,
                    role=role,
                )

                self.stdout.write(f"Superuser created: {email}")

        except IntegrityError:
            # If two processes raced, one will win; the other hits unique constraint
            self.stdout.write(f"Superuser already exists (race handled): {email}")
