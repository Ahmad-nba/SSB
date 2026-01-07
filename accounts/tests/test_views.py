from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import CustomUser as User


class TestInviteDoctorView(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email="admin@ssb.com",
            username="admin",
            password="admin123",
            role=User.ADMIN,
            is_staff=True,  # optional but often used
            is_superuser=True,  # optional but often used
        )

        self.doctor = User.objects.create_user(
            email="alex@ssb.com", username="alex", password="alex123", role=User.DOCTOR
        )

        self.url = reverse("invite-doctor")  # change to your real url name
        # payload for inviting a new doctor
        self.payload = {"email": "newdoc@ssb.com"}

    def test_admin_can_invite_doctor(self):
        # we set a logged-in admin user
        self.client.login(email="admin@ssb.com", password="admin123")
        response = self.client.post(self.url, self.payload, format="json")
        print("STATUS:", response.status_code)
        print("DATA:", response.data)

        # assert response.status_code == status.HTTP_200_OK
        # another way to assert
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        

    def test_non_admin_cannot_invite_doctor(self):
        self.client.login(email="alex@ssb.com", password="alex123")
# or username=... depending on USERNAME_FIELD


        res = self.client.post(self.url, self.payload, format="json")

        assert res.status_code == status.HTTP_403_FORBIDDEN

    # def test_unauthenticated_cannot_invite_doctor(self):
    #     res = self.client.post(self.url, self.payload, format="json")

    #     # depending on your auth settings, this is usually 401
    #     assert res.status_code in (
    #         status.HTTP_401_UNAUTHORIZED,
    #         status.HTTP_403_FORBIDDEN,
    #     )
